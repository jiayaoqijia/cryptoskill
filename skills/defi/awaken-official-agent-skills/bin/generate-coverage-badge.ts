import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { resolve } from 'node:path';

type HitMap = Map<string, number>;

type CoverageMetric = {
  total: number;
  covered: number;
  pct: number;
};

type MetricBundle = {
  lines: CoverageMetric;
  functions: CoverageMetric;
  branches: CoverageMetric;
};

type FileMetric = {
  file: string;
  lines: CoverageMetric;
  functions: CoverageMetric;
  branches: CoverageMetric;
};

type SectionHits = {
  lines: HitMap;
  functions: HitMap;
  branches: HitMap;
};

function pct(covered: number, total: number): number {
  if (total === 0) return 0;
  return (covered / total) * 100;
}

function avg(values: number[]): number {
  if (values.length === 0) return 0;
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

function toMetric(hits: HitMap): CoverageMetric {
  const total = hits.size;
  const covered = [...hits.values()].filter((v) => v > 0).length;
  return { total, covered, pct: pct(covered, total) };
}

function colorForCoverage(linesPct: number): string {
  if (linesPct >= 90) return 'brightgreen';
  if (linesPct >= 80) return 'green';
  if (linesPct >= 70) return 'yellow';
  return 'red';
}

function getOrCreateSection(store: Map<string, SectionHits>, file: string): SectionHits {
  let section = store.get(file);
  if (section) return section;

  section = {
    lines: new Map(),
    functions: new Map(),
    branches: new Map(),
  };
  store.set(file, section);
  return section;
}

function parseLcov(lcovText: string) {
  const fileHits = new Map<string, SectionHits>();
  let currentFile = '';

  for (const raw of lcovText.split('\n')) {
    const line = raw.trim();
    if (!line) continue;

    if (line.startsWith('SF:')) {
      currentFile = line.slice(3);
      getOrCreateSection(fileHits, currentFile);
      continue;
    }

    if (!currentFile) continue;

    const section = getOrCreateSection(fileHits, currentFile);

    if (line.startsWith('DA:')) {
      const [lineNoStr, hitStr] = line.slice(3).split(',');
      const lineNo = Number(lineNoStr);
      const hits = Number(hitStr);
      if (!Number.isFinite(lineNo) || !Number.isFinite(hits)) continue;

      const key = String(lineNo);
      const prev = section.lines.get(key) ?? 0;
      section.lines.set(key, Math.max(prev, hits));
      continue;
    }

    if (line.startsWith('FN:')) {
      const fnPart = line.slice(3);
      const commaIndex = fnPart.indexOf(',');
      if (commaIndex === -1) continue;

      const fnName = fnPart.slice(commaIndex + 1);
      if (!section.functions.has(fnName)) section.functions.set(fnName, 0);
      continue;
    }

    if (line.startsWith('FNDA:')) {
      const [hitStr, fnName] = line.slice(5).split(',');
      const hits = Number(hitStr);
      if (!fnName || !Number.isFinite(hits)) continue;

      const prev = section.functions.get(fnName) ?? 0;
      section.functions.set(fnName, Math.max(prev, hits));
      continue;
    }

    if (line.startsWith('BRDA:')) {
      const [lineNo, blockNo, branchNo, takenStr] = line.slice(5).split(',');
      const key = `${lineNo}:${blockNo}:${branchNo}`;
      const taken = takenStr === '-' ? 0 : Number(takenStr);
      if (!Number.isFinite(taken)) continue;

      const prev = section.branches.get(key) ?? 0;
      section.branches.set(key, Math.max(prev, taken));
    }
  }

  const files: FileMetric[] = [];

  let linesCovered = 0;
  let linesTotal = 0;
  let functionsCovered = 0;
  let functionsTotal = 0;
  let branchesCovered = 0;
  let branchesTotal = 0;

  for (const [file, section] of fileHits.entries()) {
    const lines = toMetric(section.lines);
    const functions = toMetric(section.functions);
    const branches = toMetric(section.branches);

    linesCovered += lines.covered;
    linesTotal += lines.total;
    functionsCovered += functions.covered;
    functionsTotal += functions.total;
    branchesCovered += branches.covered;
    branchesTotal += branches.total;

    files.push({ file, lines, functions, branches });
  }

  files.sort((a, b) => a.file.localeCompare(b.file));

  const linesPctByFile = files
    .filter((entry) => entry.lines.total > 0)
    .map((entry) => entry.lines.pct);
  const functionsPctByFile = files
    .filter((entry) => entry.functions.total > 0)
    .map((entry) => entry.functions.pct);
  const branchesPctByFile = files
    .filter((entry) => entry.branches.total > 0)
    .map((entry) => entry.branches.pct);

  return {
    files,
    weighted: {
      lines: {
        total: linesTotal,
        covered: linesCovered,
        pct: pct(linesCovered, linesTotal),
      },
      functions: {
        total: functionsTotal,
        covered: functionsCovered,
        pct: pct(functionsCovered, functionsTotal),
      },
      branches: {
        total: branchesTotal,
        covered: branchesCovered,
        pct: pct(branchesCovered, branchesTotal),
      },
    } satisfies MetricBundle,
    byFileAverage: {
      lines: {
        total: linesPctByFile.length,
        covered: linesPctByFile.length,
        pct: avg(linesPctByFile),
      },
      functions: {
        total: functionsPctByFile.length,
        covered: functionsPctByFile.length,
        pct: avg(functionsPctByFile),
      },
      branches: {
        total: branchesPctByFile.length,
        covered: branchesPctByFile.length,
        pct: avg(branchesPctByFile),
      },
    } satisfies MetricBundle,
  };
}

function main() {
  const inputFile = process.env.COVERAGE_LCOV_FILE || 'coverage/lcov.info';
  const outputDir = process.env.COVERAGE_BADGE_DIR || 'badge';

  const inputPath = resolve(process.cwd(), inputFile);
  const outputPath = resolve(process.cwd(), outputDir);
  mkdirSync(outputPath, { recursive: true });

  const lcovText = readFileSync(inputPath, 'utf8');
  const summary = parseLcov(lcovText);

  if (summary.byFileAverage.lines.total === 0) {
    throw new Error(`No line coverage data found in ${inputPath}`);
  }

  const badge = {
    schemaVersion: 1,
    label: 'coverage',
    message: `${summary.byFileAverage.lines.pct.toFixed(2)}%`,
    color: colorForCoverage(summary.byFileAverage.lines.pct),
  };

  const detail = {
    source: inputFile,
    coverageModel: 'bun-text-all-files-by-file-average',
    byFileAverage: summary.byFileAverage,
    weighted: summary.weighted,
    files: summary.files,
  };

  writeFileSync(
    resolve(outputPath, 'coverage.json'),
    `${JSON.stringify(badge, null, 2)}\n`,
    'utf8',
  );
  writeFileSync(
    resolve(outputPath, 'coverage-detail.json'),
    `${JSON.stringify(detail, null, 2)}\n`,
    'utf8',
  );

  console.log(
    `Coverage badge generated: ${badge.message}, color=${badge.color} (model=${detail.coverageModel})`,
  );
}

main();
