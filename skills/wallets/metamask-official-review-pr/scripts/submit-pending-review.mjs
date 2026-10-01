#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { pathToFileURL } from "node:url";

const ALLOWED_EVENTS = new Set(["COMMENT", "APPROVE", "REQUEST_CHANGES"]);

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

const flattenPages = (pages) => {
  if (!Array.isArray(pages) || pages.some((page) => !Array.isArray(page))) {
    throw new Error("review pagination returned an unexpected payload");
  }
  return pages.flat();
};

const requireEvent = (event) => {
  if (!ALLOWED_EVENTS.has(event)) {
    throw new Error("event must be COMMENT, APPROVE, or REQUEST_CHANGES");
  }
  return event;
};

export const submitPendingReview = (prUrl, event, { executeGh = runGh } = {}) => {
  const reviewEvent = requireEvent(event);
  const target = parsePullRequestUrl(prUrl);
  const pr = parseJson(
    executeGh(["pr", "view", target.url, "--json", "number,url,headRefOid"]),
    "gh pr view",
  );
  if (pr.number !== target.number || pr.url !== target.url) {
    throw new Error("resolved pull request does not match the requested URL");
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
  const pending = reviews.filter(
    (review) => review.state === "PENDING" && review.user?.login === viewer.login,
  );
  if (pending.length !== 1) {
    throw new Error(
      `authenticated reviewer has ${pending.length} pending reviews on this pull request`,
    );
  }

  const review = pending[0];
  if (typeof review.body !== "string" || review.body.trim().length === 0) {
    throw new Error(`pending review ${review.id} has no summary body`);
  }
  if (review.commit_id !== pr.headRefOid) {
    throw new Error(`pull request head moved from ${review.commit_id} to ${pr.headRefOid}`);
  }

  const submitted = parseJson(
    executeGh(
      [
        "api",
        `repos/${target.owner}/${target.repo}/pulls/${target.number}/reviews/${review.id}/events`,
        "--method",
        "POST",
        "--input",
        "-",
      ],
      JSON.stringify({ body: review.body, event: reviewEvent }),
    ),
    "gh api submit pending review",
  );

  return {
    pullRequest: target.url,
    reviewId: submitted.id ?? review.id,
    state: submitted.state,
    url: submitted.html_url,
    event: reviewEvent,
  };
};

const main = ([prUrl, event]) => {
  if (!prUrl || !event) {
    throw new Error(
      "Usage: node scripts/submit-pending-review.mjs <pr-url> <COMMENT|APPROVE|REQUEST_CHANGES>",
    );
  }
  return submitPendingReview(prUrl, event);
};

if (process.argv[1] !== undefined && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    process.stdout.write(`${JSON.stringify(main(process.argv.slice(2)), null, 2)}\n`);
  } catch (error) {
    const detail = error instanceof Error ? error.message : String(error);
    process.stderr.write(`submit-pending-review: ${detail}\n`);
    process.exitCode = 1;
  }
}
