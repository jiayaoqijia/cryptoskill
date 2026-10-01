#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { resolve, sep } from "node:path";
import { pathToFileURL } from "node:url";

const SHA_PATTERN = /^[0-9a-f]{40}$/u;
const MANIFEST_NAME = /^review-pr-pending-[0-9a-f]{40}\.json$/u;
const ALLOWED_SIDES = new Set(["LEFT", "RIGHT"]);

const runGh = (args, input) => {
  const result = spawnSync("gh", args, {
    encoding: "utf8",
    input,
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

const assertExactKeys = (value, keys, label) => {
  const expected = new Set(keys);
  const extras = Object.keys(value).filter((key) => !expected.has(key));
  if (extras.length > 0) {
    throw new Error(`${label} contains unsupported fields: ${extras.join(", ")}`);
  }
};

const requireText = (value, field) => {
  if (typeof value !== "string" || value.trim().length === 0) {
    throw new Error(`${field} must be non-empty text`);
  }
  return value;
};

const requireLine = (value, field) => {
  if (!Number.isInteger(value) || value < 1) {
    throw new Error(`${field} must be a positive integer`);
  }
  return value;
};

const requireSide = (value, field) => {
  if (!ALLOWED_SIDES.has(value)) {
    throw new Error(`${field} must be LEFT or RIGHT`);
  }
  return value;
};

const requirePath = (value) => {
  if (
    typeof value !== "string" ||
    value.length === 0 ||
    value.startsWith("/") ||
    value.split("/").includes("..") ||
    value.includes("\0")
  ) {
    throw new Error("comment path must be repository-relative");
  }
  return value;
};

const normalizeComment = (comment, index) => {
  if (comment === null || typeof comment !== "object" || Array.isArray(comment)) {
    throw new Error(`comments[${index}] must be an object`);
  }
  assertExactKeys(
    comment,
    ["path", "line", "side", "body", "startLine", "startSide"],
    `comments[${index}]`,
  );

  const normalized = {
    path: requirePath(comment.path),
    line: requireLine(comment.line, `comments[${index}].line`),
    side: requireSide(comment.side, `comments[${index}].side`),
    body: requireText(comment.body, `comments[${index}].body`),
  };
  const hasStartLine = comment.startLine !== undefined;
  const hasStartSide = comment.startSide !== undefined;
  if (hasStartLine !== hasStartSide) {
    throw new Error(`comments[${index}] must provide startLine and startSide together`);
  }
  if (hasStartLine) {
    const startLine = requireLine(comment.startLine, `comments[${index}].startLine`);
    if (startLine > normalized.line) {
      throw new Error(`comments[${index}].startLine must not exceed line`);
    }
    normalized.start_line = startLine;
    normalized.start_side = requireSide(comment.startSide, `comments[${index}].startSide`);
  }
  return normalized;
};

export const validateManifest = (manifest) => {
  if (manifest === null || typeof manifest !== "object" || Array.isArray(manifest)) {
    throw new Error("manifest must be an object");
  }
  assertExactKeys(manifest, ["schemaVersion", "headSha", "body", "comments"], "manifest");
  if (manifest.schemaVersion !== 1) {
    throw new Error("manifest schemaVersion must be 1");
  }
  if (typeof manifest.headSha !== "string" || !SHA_PATTERN.test(manifest.headSha)) {
    throw new Error("manifest headSha must be a 40-character lowercase commit SHA");
  }
  if (!Array.isArray(manifest.comments)) {
    throw new Error("manifest comments must be an array");
  }
  if (manifest.comments.length === 0) {
    throw new Error("manifest comments must include at least one inline comment");
  }
  return {
    headSha: manifest.headSha,
    body: requireText(manifest.body, "manifest body"),
    comments: manifest.comments.map(normalizeComment),
  };
};

const parsePullRequestUrl = (value) => {
  const url = new URL(value);
  const parts = url.pathname.split("/").filter(Boolean);
  if (
    url.protocol !== "https:" ||
    url.hostname !== "github.com" ||
    parts.length !== 4 ||
    parts[2] !== "pull" ||
    !/^[1-9][0-9]*$/u.test(parts[3])
  ) {
    throw new Error("pr-url must be an https://github.com/<owner>/<repo>/pull/<number> URL");
  }
  return {
    owner: parts[0],
    repo: parts[1],
    number: Number(parts[3]),
    url: `https://github.com/${parts[0]}/${parts[1]}/pull/${Number(parts[3])}`,
  };
};

const readTemporaryManifest = (manifestPath, readFile, repoRoot) => {
  const resolvedPath = resolve(manifestPath);
  const allowedDir = resolve(repoRoot, "temp");
  const basename = resolvedPath.slice(allowedDir.length + 1);
  if (!resolvedPath.startsWith(`${allowedDir}${sep}`) || !MANIFEST_NAME.test(basename)) {
    throw new Error(
      "manifest path must be temp/review-pr-pending-<40-hex-sha>.json inside the repository",
    );
  }
  return parseJson(readFile(resolvedPath, "utf8"), "pending review manifest");
};

const flattenPages = (pages) => {
  if (!Array.isArray(pages) || pages.some((page) => !Array.isArray(page))) {
    throw new Error("review pagination returned an unexpected payload");
  }
  return pages.flat();
};

export const createPendingReview = (
  prUrl,
  manifestPath,
  { executeGh = runGh, readFile = readFileSync, repoRoot } = {},
) => {
  if (typeof repoRoot !== "string" || repoRoot.length === 0) {
    throw new Error("repoRoot is required");
  }
  const target = parsePullRequestUrl(prUrl);
  const manifest = validateManifest(readTemporaryManifest(manifestPath, readFile, repoRoot));
  const pr = parseJson(
    executeGh(["pr", "view", target.url, "--json", "number,url,headRefOid"]),
    "gh pr view",
  );
  if (pr.number !== target.number || pr.url !== target.url) {
    throw new Error("resolved pull request does not match the requested URL");
  }
  if (pr.headRefOid !== manifest.headSha) {
    throw new Error(`pull request head moved from ${manifest.headSha} to ${pr.headRefOid}`);
  }

  const viewer = parseJson(executeGh(["api", "user"]), "gh api user");
  const reviews = flattenPages(
    parseJson(
      executeGh([
        "api",
        `repos/${target.owner}/${target.repo}/pulls/${target.number}/reviews`,
        "--paginate",
        "--slurp",
      ]),
      "gh api pull request reviews",
    ),
  );
  const existing = reviews.find(
    (review) => review.state === "PENDING" && review.user?.login === viewer.login,
  );
  if (existing) {
    throw new Error(
      `authenticated reviewer already has pending review ${existing.html_url ?? existing.id}`,
    );
  }

  const payload = {
    commit_id: manifest.headSha,
    // The summary stays in the manifest. GitHub's submit box replaces a pending review body, so the request leaves it empty.
    body: "",
    comments: manifest.comments,
  };
  const created = parseJson(
    executeGh(
      [
        "api",
        `repos/${target.owner}/${target.repo}/pulls/${target.number}/reviews`,
        "--method",
        "POST",
        "--input",
        "-",
      ],
      JSON.stringify(payload),
    ),
    "gh api create pending review",
  );

  return {
    pullRequest: target.url,
    reviewId: created.id,
    state: created.state,
    url: created.html_url,
    commentCount: manifest.comments.length,
  };
};

const repositoryRoot = () => {
  const result = spawnSync("git", ["rev-parse", "--show-toplevel"], {
    encoding: "utf8",
    shell: false,
  });
  if (result.status !== 0) {
    throw new Error(result.stderr?.trim() || "could not resolve the git repository root");
  }
  return result.stdout.trim();
};

const main = ([prUrl, manifestPath]) => {
  if (!prUrl || !manifestPath) {
    throw new Error("Usage: node scripts/create-pending-review.mjs <pr-url> <manifest-path>");
  }
  return createPendingReview(prUrl, manifestPath, { repoRoot: repositoryRoot() });
};

if (process.argv[1] !== undefined && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    process.stdout.write(`${JSON.stringify(main(process.argv.slice(2)), null, 2)}\n`);
  } catch (error) {
    const detail = error instanceof Error ? error.message : String(error);
    process.stderr.write(`create-pending-review: ${detail}\n`);
    process.exitCode = 1;
  }
}
