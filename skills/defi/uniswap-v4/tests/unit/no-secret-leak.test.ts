/**
 * CI-safe regression test: ensure PRIVATE_KEY is never printed.
 *
 * Rationale:
 * - CI logs and stdout/stderr should be treated as public.
 * - If any script ever starts logging env/config objects, we want a hard failure.
 */

import { describe, it, expect } from "vitest";
import { spawnSync } from "node:child_process";
import path from "node:path";
import { fileURLToPath } from "node:url";

const CANARY_PRIVATE_KEY = "0x" + "c0ffee".repeat(10) + "c0ff"; // 64 hex chars

function runCli(scriptRel: string, args: string[]) {
  const testDir = path.dirname(fileURLToPath(import.meta.url));
  const repoRoot = path.resolve(testDir, "../..");

  const tsxCli = path.join(repoRoot, "node_modules", "tsx", "dist", "cli.mjs");
  const scriptPath = path.join(repoRoot, scriptRel);

  const res = spawnSync(process.execPath, [tsxCli, scriptPath, ...args], {
    cwd: repoRoot,
    env: {
      ...process.env,
      PRIVATE_KEY: CANARY_PRIVATE_KEY,
    },
    encoding: "utf8",
  });

  const output = `${res.stdout ?? ""}${res.stderr ?? ""}`;
  return { res, output };
}

describe("security: no PRIVATE_KEY leakage", () => {
  it("never prints PRIVATE_KEY value to stdout/stderr", () => {
    const cases: Array<{ script: string; args: string[]; expectedStatus: number }> = [
      // Help paths (exit 0)
      { script: "src/pool-info.ts", args: ["--help"], expectedStatus: 0 },
      { script: "src/quote.ts", args: ["--help"], expectedStatus: 0 },
      { script: "src/approve.ts", args: ["--help"], expectedStatus: 0 },
      { script: "src/swap.ts", args: ["--help"], expectedStatus: 0 },

      // Error paths (exit 1) — should still never leak env vars
      { script: "src/pool-info.ts", args: [], expectedStatus: 1 },
      { script: "src/quote.ts", args: [], expectedStatus: 1 },
      { script: "src/approve.ts", args: [], expectedStatus: 1 },
      { script: "src/swap.ts", args: [], expectedStatus: 1 },
    ];

    for (const { script, args, expectedStatus } of cases) {
      const { res, output } = runCli(script, args);

      expect(res.error, `${script} failed to spawn`).toBeUndefined();
      expect(
        res.status,
        `${script} exited with status=${res.status} (expected ${expectedStatus}). Output:\n${output}`
      ).toBe(expectedStatus);

      expect(output, `${script} leaked PRIVATE_KEY value`).not.toContain(
        CANARY_PRIVATE_KEY
      );
    }
  });
});
