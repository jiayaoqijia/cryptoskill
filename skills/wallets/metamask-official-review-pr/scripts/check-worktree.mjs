#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { pathToFileURL } from "node:url";

const runGit = (args) => {
  const result = spawnSync("git", args, {
    encoding: "utf8",
    shell: false,
  });
  if (result.error || result.status !== 0) {
    throw new Error(result.stderr?.trim() || result.error?.message || "git failed");
  }
  return result.stdout;
};

export const checkWorktree = (executeGit = runGit) => {
  const status = executeGit(["status", "--porcelain"]);

  return {
    clean: status.length === 0,
    status,
  };
};

if (process.argv[1] !== undefined && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    process.stdout.write(`${JSON.stringify(checkWorktree(), null, 2)}\n`);
  } catch (error) {
    const detail = error instanceof Error ? error.message : String(error);
    process.stderr.write(`check-worktree: ${detail}\n`);
    process.exitCode = 1;
  }
}
