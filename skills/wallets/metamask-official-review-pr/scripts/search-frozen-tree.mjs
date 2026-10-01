#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { pathToFileURL } from "node:url";

const MATCH_LIMIT = 500;
const SHA_PATTERN = /^[0-9a-f]{40}$/u;

const requireSha = (value, field = "sha") => {
  if (typeof value !== "string" || !SHA_PATTERN.test(value)) {
    throw new Error(`${field} must be a 40-character lowercase commit SHA`);
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
  return {
    status: result.status ?? 1,
    stdout: result.stdout ?? "",
    stderr: result.stderr ?? result.error?.message ?? "",
  };
};

const parseMatch = (line) => {
  const match = /^(?<commit>[^:]+):(?<path>.*?):(?<line>[0-9]+):(?<text>.*)$/u.exec(line);
  if (!match?.groups) {
    throw new Error(`unexpected git grep output: ${line}`);
  }

  return {
    commitSha: requireSha(match.groups.commit, "match commit SHA"),
    path: match.groups.path,
    line: Number(match.groups.line),
    text: match.groups.text,
  };
};

export const searchFrozenTree = (sha, pattern, paths = [], executeGit = runGit) => {
  const commitSha = requireSha(sha);
  if (typeof pattern !== "string" || pattern.length === 0) {
    throw new Error("search pattern must be a non-empty fixed string");
  }

  const repositoryPaths = paths.map(requireRepositoryPath);
  const args = ["grep", "-n", "-I", "-F", "-e", pattern, commitSha];
  if (repositoryPaths.length > 0) {
    args.push("--", ...repositoryPaths);
  }

  const result = executeGit(args, { allowFailure: true });
  if (result.status === 1) {
    return { commitSha, pattern, paths: repositoryPaths, matches: [] };
  }
  if (result.status !== 0) {
    throw new Error(result.stderr.trim() || "git grep failed");
  }

  const allMatches = result.stdout.split("\n").filter(Boolean).map(parseMatch);

  return {
    commitSha,
    pattern,
    paths: repositoryPaths,
    matches: allMatches.slice(0, MATCH_LIMIT),
    truncated: allMatches.length > MATCH_LIMIT,
  };
};

const main = ([sha, pattern, ...paths]) => {
  if (!sha || !pattern) {
    throw new Error(
      "Usage: node scripts/search-frozen-tree.mjs <commit-sha> <pattern> [repository-path...]",
    );
  }

  return searchFrozenTree(sha, pattern, paths);
};

if (process.argv[1] !== undefined && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    process.stdout.write(`${JSON.stringify(main(process.argv.slice(2)), null, 2)}\n`);
  } catch (error) {
    const detail = error instanceof Error ? error.message : String(error);
    process.stderr.write(`search-frozen-tree: ${detail}\n`);
    process.exitCode = 1;
  }
}
