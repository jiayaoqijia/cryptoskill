import { mkdirSync, readFileSync, writeFileSync, existsSync } from "node:fs";
import { join, resolve } from "node:path";

type RepoConfig = {
  name: string;
  relPath: string;
};

type RepoReport = {
  name: string;
  path: string;
  exitCode: number;
  errorCount: number;
  durationMs: number;
};

const REPOS: RepoConfig[] = [
  { name: "eoa-agent-skills", relPath: "portkey/eoa-agent-skills" },
  { name: "portkey-agent-skills", relPath: "portkey/portkey-agent-skills" },
  { name: "awaken-agent-skills", relPath: "awaken/awaken-agent-skills" },
  { name: "eforest-agent-skills", relPath: "eforest-finance/eforest-agent-skills" },
  { name: "tomorrowDAO-skill", relPath: "TomorrowDAOProject/tomorrowDAO-skill" },
  { name: "aelf-node-skill", relPath: "AElf/aelf-node-skill" },
];

const repoRoot = resolve(import.meta.dir, "..");
const skillsBase = process.env.SKILLS_BASE ?? resolve(repoRoot, "..", "..");
const outDir = join(repoRoot, "docs", "type-safety");
const latestPath = join(outDir, "type-debt-latest.json");
const historyPath = join(outDir, "type-debt-history.json");

function runTypecheck(repo: RepoConfig): RepoReport {
  const cwd = join(skillsBase, repo.relPath);
  const startedAt = Date.now();
  const proc = Bun.spawnSync({
    cmd: ["bun", "run", "typecheck"],
    cwd,
    stdout: "pipe",
    stderr: "pipe",
  });
  const durationMs = Date.now() - startedAt;
  const output = `${new TextDecoder().decode(proc.stdout)}\n${new TextDecoder().decode(proc.stderr)}`;
  const errors = output.match(/error TS\d+:/g) ?? [];

  return {
    name: repo.name,
    path: cwd,
    exitCode: proc.exitCode,
    errorCount: errors.length,
    durationMs,
  };
}

function loadHistory(): unknown[] {
  if (!existsSync(historyPath)) return [];
  try {
    const parsed = JSON.parse(readFileSync(historyPath, "utf-8"));
    return Array.isArray(parsed) ? parsed : [];
  } catch {
    return [];
  }
}

function formatDuration(ms: number): string {
  if (ms < 1000) return `${ms}ms`;
  return `${(ms / 1000).toFixed(2)}s`;
}

function main() {
  const generatedAt = new Date().toISOString();
  const reports = REPOS.map(runTypecheck);
  const failed = reports.filter((item) => item.exitCode !== 0).length;
  const totalErrors = reports.reduce((sum, item) => sum + item.errorCount, 0);

  const report = {
    generatedAt,
    skillsBase,
    summary: {
      repos: reports.length,
      failed,
      totalErrors,
    },
    repos: reports,
  };

  mkdirSync(outDir, { recursive: true });
  writeFileSync(latestPath, JSON.stringify(report, null, 2));

  const history = loadHistory();
  history.push(report);
  const maxHistory = 100;
  const compactHistory = history.slice(-maxHistory);
  writeFileSync(historyPath, JSON.stringify(compactHistory, null, 2));

  console.log("Type Debt Report");
  console.log(`generatedAt: ${generatedAt}`);
  for (const item of reports) {
    const status = item.exitCode === 0 ? "PASS" : "FAIL";
    console.log(
      `${status} ${item.name.padEnd(24)} errors=${String(item.errorCount).padStart(3)} duration=${formatDuration(item.durationMs)}`,
    );
  }
  console.log(`summary: failed=${failed}/${reports.length}, totalErrors=${totalErrors}`);
  console.log(`latest: ${latestPath}`);
  console.log(`history: ${historyPath}`);

  if (failed > 0) {
    process.exit(1);
  }
}

main();
