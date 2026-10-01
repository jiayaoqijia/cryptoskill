#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { mkdirSync, writeFileSync } from "node:fs";
import { resolve, sep } from "node:path";
import { pathToFileURL } from "node:url";

const REPORT_NAME = /^review-pr-[0-9a-f]{40}\.json$/u;
const MANIFEST_NAME = /^review-pr-pending-[0-9a-f]{40}\.json$/u;

const runGit = (args, cwd) =>
  spawnSync("git", args, {
    cwd,
    encoding: "utf8",
    shell: false,
  });

export const repositoryRoot = (cwd = process.cwd()) => {
  const result = runGit(["rev-parse", "--show-toplevel"], cwd);
  if (result.status !== 0) {
    throw new Error(result.stderr?.trim() || "could not resolve the git repository root");
  }
  return result.stdout.trim();
};

const gitignoresTempFile = (repoRoot, relativePath) => {
  const result = runGit(["check-ignore", "-q", "--", relativePath], repoRoot);
  return result.status === 0;
};

export const writeTempJson = ({
  basename,
  repoRoot,
  isIgnored = gitignoresTempFile,
} = {}) => {
  if (!REPORT_NAME.test(basename) && !MANIFEST_NAME.test(basename)) {
    throw new Error(
      "basename must be review-pr-<40-hex-sha>.json or review-pr-pending-<40-hex-sha>.json",
    );
  }
  if (typeof repoRoot !== "string" || repoRoot.length === 0) {
    throw new Error("repoRoot is required");
  }
  const relativePath = `temp/${basename}`;
  if (!isIgnored(repoRoot, relativePath)) {
    throw new Error("temp/ is not gitignored in this repository");
  }
  const directory = resolve(repoRoot, "temp");
  const target = resolve(directory, basename);
  if (!target.startsWith(`${directory}${sep}`)) {
    throw new Error("refusing to write outside temp/");
  }
  // An empty object gives the file tool an existing path to read before it writes the report.
  mkdirSync(directory, { recursive: true });
  writeFileSync(target, "{}\n");
  return target;
};

const main = (args) => {
  const basename = args.find((arg) => !arg.startsWith("--"));
  const init = args.includes("--init");
  if (!basename || !init || args.length !== 2) {
    throw new Error("Usage: node scripts/write-temp-json.mjs <basename> --init");
  }
  return { path: writeTempJson({ basename, repoRoot: repositoryRoot() }) };
};

if (process.argv[1] !== undefined && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    process.stdout.write(`${JSON.stringify(main(process.argv.slice(2)), null, 2)}\n`);
  } catch (error) {
    const detail = error instanceof Error ? error.message : String(error);
    process.stderr.write(`write-temp-json: ${detail}\n`);
    process.exitCode = 1;
  }
}
