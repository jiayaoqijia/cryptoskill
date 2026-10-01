#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { pathToFileURL } from "node:url";

const SHA_PATTERN = /^[0-9a-f]{40}$/u;

const requireSha = (value, field = "sha") => {
  if (typeof value !== "string" || !SHA_PATTERN.test(value)) {
    throw new Error(`${field} must be a 40-character lowercase commit SHA`);
  }
  return value;
};

const runGit = (args) => {
  const result = spawnSync("git", args, {
    encoding: "utf8",
    shell: false,
  });
  if (result.error || result.status !== 0) {
    throw new Error(result.stderr?.trim() || result.error?.message || "git failed");
  }
  return { stdout: result.stdout };
};

export const inspectCommit = (sha, executeGit = runGit) => {
  const requestedSha = requireSha(sha);
  const fields = executeGit(["show", "-s", "--format=%H%x00%s%x00%P", requestedSha])
    .stdout.trimEnd()
    .split("\0");
  const [resolvedSha, subject = "", parentList = ""] = fields;

  return {
    sha: requireSha(resolvedSha, "resolved commit SHA"),
    subject,
    parents: parentList
      .split(" ")
      .filter(Boolean)
      .map((parent) => requireSha(parent, "parent SHA")),
    changedPaths: executeGit([
      "diff-tree",
      "--root",
      "--no-commit-id",
      "--name-only",
      "-r",
      requestedSha,
    ])
      .stdout.split("\n")
      .filter(Boolean),
  };
};

const main = ([sha]) => {
  if (!sha) {
    throw new Error("Usage: node scripts/inspect-commit.mjs <commit-sha>");
  }

  return inspectCommit(sha);
};

if (process.argv[1] !== undefined && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    process.stdout.write(`${JSON.stringify(main(process.argv.slice(2)), null, 2)}\n`);
  } catch (error) {
    const detail = error instanceof Error ? error.message : String(error);
    process.stderr.write(`inspect-commit: ${detail}\n`);
    process.exitCode = 1;
  }
}
