#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { pathToFileURL } from "node:url";

const PR_FIELDS = [
  "number",
  "url",
  "title",
  "body",
  "baseRefName",
  "headRefName",
  "baseRefOid",
  "headRefOid",
  "statusCheckRollup",
  "reviews",
  "comments",
  "commits",
  "closingIssuesReferences",
];

const SHA_PATTERN = /^[0-9a-f]{40}$/u;

const runGh = (args) => {
  const result = spawnSync("gh", args, {
    encoding: "utf8",
    maxBuffer: 100 * 1024 * 1024,
    shell: false,
  });
  if (result.error || result.status !== 0) {
    throw new Error(result.stderr?.trim() || result.error?.message || "gh failed");
  }
  return result.stdout;
};

const parseJson = (value, source) => {
  try {
    return JSON.parse(value);
  } catch (error) {
    const detail = error instanceof Error ? error.message : String(error);
    throw new Error(`${source} returned invalid JSON: ${detail}`);
  }
};

const requireSha = (value, field) => {
  if (typeof value !== "string" || !SHA_PATTERN.test(value)) {
    throw new Error(`${field} must be a 40-character lowercase commit SHA`);
  }
  return value;
};

export const repositoryFromUrl = (url) => {
  const segments = new URL(url).pathname.split("/").filter(Boolean);
  const pullIndex = segments.indexOf("pull");

  if (pullIndex !== 2 || segments.length < 4) {
    throw new Error(`Unexpected pull request URL: ${url}`);
  }

  return `${segments[0]}/${segments[1]}`;
};

export const normalizeChecks = (rollup) =>
  rollup.map((check) => ({
    name: check.name ?? check.context ?? check.workflowName ?? "unknown",
    state: check.conclusion ?? check.state ?? check.status ?? check.bucket ?? "unknown",
  }));

const flattenPages = (pages) => {
  if (!Array.isArray(pages) || pages.some((page) => !Array.isArray(page))) {
    throw new Error("gh api pagination returned an unexpected payload");
  }

  return pages.flat();
};

export const collectPrContext = (target, executeGh = runGh) => {
  const metadata = parseJson(
    executeGh(["pr", "view", target, "--json", PR_FIELDS.join(",")]),
    "gh pr view",
  );
  const repository = repositoryFromUrl(metadata.url);
  const number = metadata.number;

  if (!Number.isInteger(number)) {
    throw new Error("gh pr view returned an invalid pull request number");
  }

  const baseRefOid = requireSha(metadata.baseRefOid, "baseRefOid");
  const headRefOid = requireSha(metadata.headRefOid, "headRefOid");
  const diff = executeGh(["pr", "diff", target]);

  if (!diff.trim()) {
    throw new Error("gh pr diff returned an empty diff");
  }

  const inlineCommentPages = parseJson(
    executeGh(["api", `repos/${repository}/pulls/${number}/comments`, "--paginate", "--slurp"]),
    "gh api pull request comments",
  );

  return {
    schemaVersion: 1,
    provider: "gh",
    repository,
    number,
    url: metadata.url,
    title: metadata.title,
    body: metadata.body ?? "",
    baseRefName: metadata.baseRefName,
    headRefName: metadata.headRefName,
    baseRefOid,
    headRefOid,
    workingTree: "excluded",
    closingIssuesReferences: metadata.closingIssuesReferences ?? [],
    checks: normalizeChecks(metadata.statusCheckRollup ?? []),
    reviews: metadata.reviews ?? [],
    comments: metadata.comments ?? [],
    commits: (metadata.commits ?? []).map((commit) => ({
      oid: requireSha(commit.oid, "commit oid"),
      messageHeadline: commit.messageHeadline ?? "",
    })),
    inlineComments: flattenPages(inlineCommentPages),
    diff,
  };
};

const main = ([target]) => {
  if (!target) {
    throw new Error("Usage: node scripts/collect-pr-context.mjs <pull-request-url-or-number>");
  }

  return collectPrContext(target);
};

if (process.argv[1] !== undefined && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    process.stdout.write(`${JSON.stringify(main(process.argv.slice(2)), null, 2)}\n`);
  } catch (error) {
    const detail = error instanceof Error ? error.message : String(error);
    process.stderr.write(`collect-pr-context: ${detail}\n`);
    process.exitCode = 1;
  }
}
