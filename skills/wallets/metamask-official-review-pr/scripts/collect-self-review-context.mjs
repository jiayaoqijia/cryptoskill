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
    maxBuffer: 100 * 1024 * 1024,
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

const output = (executeGit, args, options) => executeGit(args, options).stdout.trim();

const resolveBase = (executeGit, head) => {
  const originMain = executeGit(["merge-base", head, "origin/main"], {
    allowFailure: true,
  });

  if (originMain.status === 0) {
    return {
      baseRef: "origin/main",
      baseSha: requireSha(originMain.stdout.trim(), "base SHA"),
    };
  }

  return {
    baseRef: "main",
    baseSha: requireSha(output(executeGit, ["merge-base", head, "main"]), "base SHA"),
  };
};

const parseCommits = (value) =>
  value
    .split("\n")
    .filter(Boolean)
    .map((line) => {
      const [oid, ...subject] = line.split("\t");
      return {
        oid: requireSha(oid, "commit oid"),
        messageHeadline: subject.join("\t"),
      };
    });

export const collectSelfReviewContext = (workingTree, executeGit = runGit) => {
  if (!["included", "excluded"].includes(workingTree)) {
    throw new Error("working tree must be included or excluded");
  }

  const repositoryRoot = output(executeGit, ["rev-parse", "--show-toplevel"]);
  const remoteUrl = output(executeGit, ["remote", "get-url", "origin"]);
  const headSha = requireSha(output(executeGit, ["rev-parse", "HEAD"]), "head SHA");
  const { baseRef, baseSha } = resolveBase(executeGit, headSha);
  const range = `${baseSha}...${headSha}`;
  const commitRange = `${baseSha}..${headSha}`;

  return {
    schemaVersion: 1,
    provider: "local-git",
    repositoryRoot,
    remoteUrl,
    baseRef,
    baseSha,
    headSha,
    workingTree,
    commits: parseCommits(output(executeGit, ["log", "--format=%H%x09%s", commitRange])),
    changedPaths: output(executeGit, ["diff", "--name-only", range]).split("\n").filter(Boolean),
    committedDiff: executeGit(["diff", range]).stdout,
    status: workingTree === "included" ? executeGit(["status", "--porcelain"]).stdout : "",
    stagedDiff: workingTree === "included" ? executeGit(["diff", "--cached"]).stdout : "",
    unstagedDiff: workingTree === "included" ? executeGit(["diff"]).stdout : "",
  };
};

const main = ([workingTree]) => {
  if (!workingTree) {
    throw new Error("Usage: node scripts/collect-self-review-context.mjs <included-or-excluded>");
  }

  return collectSelfReviewContext(workingTree);
};

if (process.argv[1] !== undefined && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    process.stdout.write(`${JSON.stringify(main(process.argv.slice(2)), null, 2)}\n`);
  } catch (error) {
    const detail = error instanceof Error ? error.message : String(error);
    process.stderr.write(`collect-self-review-context: ${detail}\n`);
    process.exitCode = 1;
  }
}
