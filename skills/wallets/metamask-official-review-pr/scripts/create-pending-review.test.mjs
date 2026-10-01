import assert from "node:assert/strict";
import { join } from "node:path";
import { tmpdir } from "node:os";
import test from "node:test";

import { createPendingReview, validateManifest } from "./create-pending-review.mjs";

const HEAD_SHA = "a".repeat(40);
const PR_URL = "https://github.com/MetaMask/metamask-mobile/pull/123";
const REPO_ROOT = join(tmpdir(), "review-pr-repo");
const MANIFEST_PATH = join(REPO_ROOT, "temp", `review-pr-pending-${HEAD_SHA}.json`);

const manifest = (overrides = {}) => ({
  schemaVersion: 1,
  headSha: HEAD_SHA,
  body: "Review summary",
  comments: [
    {
      path: "app/file.ts",
      line: 12,
      side: "RIGHT",
      body: "Please validate this branch.",
      startLine: 10,
      startSide: "RIGHT",
    },
  ],
  ...overrides,
});

const createAdapters = ({
  manifestValue = manifest(),
  headSha = HEAD_SHA,
  reviews = [],
  postError,
} = {}) => {
  const calls = [];
  const executeGh = (args, input) => {
    calls.push({ args, input });
    if (args[0] === "pr") {
      return JSON.stringify({
        number: 123,
        url: PR_URL,
        headRefOid: headSha,
      });
    }
    if (args[1] === "user") {
      return JSON.stringify({ login: "reviewer" });
    }
    if (args.includes("--paginate")) {
      return JSON.stringify([reviews]);
    }
    if (postError) {
      throw new Error(postError);
    }
    return JSON.stringify({
      id: 456,
      state: "PENDING",
      html_url: `${PR_URL}#pullrequestreview-456`,
    });
  };
  return {
    calls,
    executeGh,
    readFile: () => JSON.stringify(manifestValue),
    repoRoot: REPO_ROOT,
  };
};

test("createPendingReview creates an atomic pending review payload", () => {
  const adapters = createAdapters();
  const result = createPendingReview(PR_URL, MANIFEST_PATH, adapters);
  const post = adapters.calls.at(-1);
  const payload = JSON.parse(post.input);

  assert.equal(post.args[0], "api");
  assert.equal(post.args.includes("POST"), true);
  assert.equal(Object.hasOwn(payload, "event"), false);
  assert.deepEqual(payload, {
    commit_id: HEAD_SHA,
    body: "",
    comments: [
      {
        path: "app/file.ts",
        line: 12,
        side: "RIGHT",
        body: "Please validate this branch.",
        start_line: 10,
        start_side: "RIGHT",
      },
    ],
  });
  assert.deepEqual(result, {
    pullRequest: PR_URL,
    reviewId: 456,
    state: "PENDING",
    url: `${PR_URL}#pullrequestreview-456`,
    commentCount: 1,
  });
});

test("createPendingReview keeps the summary out of the GitHub payload", () => {
  const adapters = createAdapters();
  assert.equal(validateManifest(manifest()).body, "Review summary");

  createPendingReview(PR_URL, MANIFEST_PATH, adapters);

  assert.equal(JSON.parse(adapters.calls.at(-1).input).body, "");
});

test("createPendingReview rejects an empty review summary", () => {
  assert.throws(
    () => validateManifest(manifest({ body: "  " })),
    /manifest body must be non-empty text/u,
  );
});

test("createPendingReview rejects a review with no inline comments", () => {
  const adapters = createAdapters({
    manifestValue: manifest({ comments: [] }),
  });

  assert.throws(
    () => createPendingReview(PR_URL, MANIFEST_PATH, adapters),
    /at least one inline comment/u,
  );
  assert.equal(adapters.calls.length, 0);
});

test("createPendingReview stops when the frozen head moved", () => {
  const adapters = createAdapters({ headSha: "b".repeat(40) });

  assert.throws(
    () => createPendingReview(PR_URL, MANIFEST_PATH, adapters),
    /pull request head moved/u,
  );
  assert.equal(adapters.calls.length, 1);
});

test("createPendingReview stops when the reviewer has a pending review", () => {
  const adapters = createAdapters({
    reviews: [
      {
        id: 789,
        state: "PENDING",
        html_url: `${PR_URL}#pullrequestreview-789`,
        user: { login: "reviewer" },
      },
    ],
  });

  assert.throws(
    () => createPendingReview(PR_URL, MANIFEST_PATH, adapters),
    /already has pending review/u,
  );
  assert.equal(adapters.calls.length, 3);
});

test("validateManifest rejects inconsistent multiline placement", () => {
  const value = manifest();
  delete value.comments[0].startSide;

  assert.throws(() => validateManifest(value), /provide startLine and startSide together/u);
});

test("createPendingReview propagates the API write failure", () => {
  const adapters = createAdapters({ postError: "API denied the review" });

  assert.throws(
    () => createPendingReview(PR_URL, MANIFEST_PATH, adapters),
    /API denied the review/u,
  );
});
