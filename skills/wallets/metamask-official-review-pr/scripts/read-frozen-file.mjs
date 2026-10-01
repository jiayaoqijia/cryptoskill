#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { pathToFileURL } from "node:url";

const SHA_PATTERN = /^[0-9a-f]{40}$/u;

const requireSha = (value) => {
  if (typeof value !== "string" || !SHA_PATTERN.test(value)) {
    throw new Error("sha must be a 40-character lowercase commit SHA");
  }
  return value;
};

const requireRepositoryPath = (value) => {
  if (
    typeof value !== "string" ||
    value.length === 0 ||
    value.startsWith("/") ||
    value.split("/").includes("..") ||
    value.includes("\0")
  ) {
    throw new Error("path must be a repository-relative path");
  }
  return value;
};

const runGit = (args) => {
  const result = spawnSync("git", args, {
    encoding: "utf8",
    maxBuffer: 100 * 1024 * 1024,
    shell: false,
  });
  if (result.error || result.status !== 0) {
    throw new Error(result.stderr?.trim() || result.error?.message || "git failed");
  }
  return { stdout: result.stdout };
};

export const readFrozenFile = (sha, path, executeGit = runGit) => {
  const commitSha = requireSha(sha);
  const repositoryPath = requireRepositoryPath(path);

  return {
    commitSha,
    path: repositoryPath,
    content: executeGit(["show", `${commitSha}:${repositoryPath}`]).stdout,
  };
};

const main = ([sha, path]) => {
  if (!sha || !path) {
    throw new Error("Usage: node scripts/read-frozen-file.mjs <commit-sha> <repository-path>");
  }

  return readFrozenFile(sha, path);
};

if (process.argv[1] !== undefined && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    process.stdout.write(`${JSON.stringify(main(process.argv.slice(2)), null, 2)}\n`);
  } catch (error) {
    const detail = error instanceof Error ? error.message : String(error);
    process.stderr.write(`read-frozen-file: ${detail}\n`);
    process.exitCode = 1;
  }
}
