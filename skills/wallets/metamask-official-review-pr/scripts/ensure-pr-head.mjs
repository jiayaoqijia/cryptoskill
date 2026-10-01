#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { pathToFileURL } from "node:url";

const SHA_PATTERN = /^[0-9a-f]{40}$/u;

const requireSha = (value, field) => {
  if (typeof value !== "string" || !SHA_PATTERN.test(value)) {
    throw new Error(`${field} must be a 40-character lowercase commit SHA`);
  }
  return value;
};

const runGit = (args, options = {}) => {
  const result = spawnSync("git", args, {
    encoding: "utf8",
    shell: false,
  });
  if (result.error || (result.status !== 0 && !options.allowFailure)) {
    throw new Error(result.stderr?.trim() || result.error?.message || "git failed");
  }
  return {
    status: result.status ?? 1,
    stdout: result.stdout,
    stderr: result.stderr,
  };
};

export const ensurePrHead = (number, expectedSha, executeGit = runGit) => {
  if (!/^[1-9][0-9]*$/u.test(String(number))) {
    throw new Error("pull request number must be a positive integer");
  }

  const headSha = requireSha(expectedSha, "expected head SHA");
  const existing = executeGit(["cat-file", "-e", `${headSha}^{commit}`], {
    allowFailure: true,
  });

  if (existing.status === 0) {
    return { headSha, fetched: false };
  }

  executeGit(["fetch", "--no-tags", "origin", `refs/pull/${number}/head`]);
  const fetchedSha = requireSha(
    executeGit(["rev-parse", "FETCH_HEAD"]).stdout.trim(),
    "fetched head SHA",
  );

  if (fetchedSha !== headSha) {
    throw new Error(`fetched head ${fetchedSha} does not match frozen head ${headSha}`);
  }

  return { headSha, fetched: true };
};

const main = ([number, expectedSha]) => {
  if (!number || !expectedSha) {
    throw new Error("Usage: node scripts/ensure-pr-head.mjs <pr-number> <expected-head-sha>");
  }

  return ensurePrHead(number, expectedSha);
};

if (process.argv[1] !== undefined && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    process.stdout.write(`${JSON.stringify(main(process.argv.slice(2)), null, 2)}\n`);
  } catch (error) {
    const detail = error instanceof Error ? error.message : String(error);
    process.stderr.write(`ensure-pr-head: ${detail}\n`);
    process.exitCode = 1;
  }
}
