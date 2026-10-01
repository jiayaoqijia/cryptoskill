import assert from "node:assert/strict";
import test from "node:test";

import { collectSelfReviewContext } from "./collect-self-review-context.mjs";

const BASE_SHA = "1".repeat(40);
const HEAD_SHA = "2".repeat(40);

const createGit = (calls) => (args) => {
  calls.push(args);
  const key = args.join(" ");
  const values = {
    "rev-parse --show-toplevel": "/repo\n",
    "remote get-url origin": "git@github.com:MetaMask/repo.git\n",
    "rev-parse HEAD": `${HEAD_SHA}\n`,
    [`merge-base ${HEAD_SHA} origin/main`]: `${BASE_SHA}\n`,
    [`log --format=%H%x09%s ${BASE_SHA}..${HEAD_SHA}`]: `${HEAD_SHA}\tChange review flow\n`,
    [`diff --name-only ${BASE_SHA}...${HEAD_SHA}`]: "src/file.ts\n",
    [`diff ${BASE_SHA}...${HEAD_SHA}`]: "committed diff\n",
    "status --porcelain": " M src/file.ts\n",
    "diff --cached": "staged diff\n",
    diff: "unstaged diff\n",
  };

  return {
    status: 0,
    stdout: values[key] ?? "",
    stderr: "",
  };
};

test("collectSelfReviewContext includes working-tree evidence when requested", () => {
  const calls = [];
  const context = collectSelfReviewContext("included", createGit(calls));

  assert.equal(context.baseSha, BASE_SHA);
  assert.equal(context.headSha, HEAD_SHA);
  assert.deepEqual(context.changedPaths, ["src/file.ts"]);
  assert.deepEqual(context.commits, [{ oid: HEAD_SHA, messageHeadline: "Change review flow" }]);
  assert.equal(context.stagedDiff, "staged diff\n");
  assert.equal(context.unstagedDiff, "unstaged diff\n");
  assert.ok(calls.some((args) => args.join(" ") === "status --porcelain"));
});

test("collectSelfReviewContext omits working-tree commands for branch scope", () => {
  const calls = [];
  const context = collectSelfReviewContext("excluded", createGit(calls));

  assert.equal(context.status, "");
  assert.equal(context.stagedDiff, "");
  assert.equal(context.unstagedDiff, "");
  assert.equal(
    calls.some((args) => args.join(" ") === "status --porcelain"),
    false,
  );
});

test("collectSelfReviewContext validates the requested scope", () => {
  assert.throws(
    () => collectSelfReviewContext("maybe", createGit([])),
    /working tree must be included or excluded/u,
  );
});
