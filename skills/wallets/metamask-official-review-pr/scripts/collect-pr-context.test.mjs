import assert from "node:assert/strict";
import test from "node:test";

import { collectPrContext, normalizeChecks, repositoryFromUrl } from "./collect-pr-context.mjs";

const BASE_SHA = "1".repeat(40);
const HEAD_SHA = "2".repeat(40);

test("repositoryFromUrl extracts the repository from a pull request URL", () => {
  assert.equal(
    repositoryFromUrl("https://github.example.com/MetaMask/metamask-mobile/pull/123"),
    "MetaMask/metamask-mobile",
  );
});

test("normalizeChecks keeps one name and state per check", () => {
  assert.deepEqual(
    normalizeChecks([
      { name: "lint", conclusion: "SUCCESS" },
      { context: "unit", state: "PENDING" },
      { workflowName: "build", status: "IN_PROGRESS" },
    ]),
    [
      { name: "lint", state: "SUCCESS" },
      { name: "unit", state: "PENDING" },
      { name: "build", state: "IN_PROGRESS" },
    ],
  );
});

test("collectPrContext returns normalized frozen review data", () => {
  const calls = [];
  const executeGh = (args) => {
    calls.push(args);

    if (args[0] === "pr" && args[1] === "view") {
      return JSON.stringify({
        number: 123,
        url: "https://github.com/MetaMask/metamask-mobile/pull/123",
        title: "Test pull request",
        body: null,
        baseRefName: "main",
        headRefName: "feature",
        baseRefOid: BASE_SHA,
        headRefOid: HEAD_SHA,
        statusCheckRollup: [{ name: "lint", conclusion: "SUCCESS" }],
        reviews: [{ state: "APPROVED" }],
        comments: [{ id: "comment-1" }],
        commits: [{ oid: HEAD_SHA, messageHeadline: "Test commit" }],
        closingIssuesReferences: [{ number: 42 }],
      });
    }

    if (args[0] === "pr" && args[1] === "diff") {
      return "diff --git a/file.ts b/file.ts\n";
    }

    return JSON.stringify([[{ id: 1 }], [{ id: 2 }]]);
  };

  const context = collectPrContext("123", executeGh);

  assert.equal(context.repository, "MetaMask/metamask-mobile");
  assert.equal(context.baseRefOid, BASE_SHA);
  assert.equal(context.headRefOid, HEAD_SHA);
  assert.equal(context.body, "");
  assert.equal(context.workingTree, "excluded");
  assert.deepEqual(context.checks, [{ name: "lint", state: "SUCCESS" }]);
  assert.deepEqual(context.commits, [{ oid: HEAD_SHA, messageHeadline: "Test commit" }]);
  assert.deepEqual(context.inlineComments, [{ id: 1 }, { id: 2 }]);
  assert.deepEqual(calls[2], [
    "api",
    "repos/MetaMask/metamask-mobile/pulls/123/comments",
    "--paginate",
    "--slurp",
  ]);
});

test("collectPrContext rejects a missing frozen SHA", () => {
  const executeGh = () =>
    JSON.stringify({
      number: 123,
      url: "https://github.com/MetaMask/metamask-mobile/pull/123",
      baseRefOid: "main",
      headRefOid: HEAD_SHA,
    });

  assert.throws(
    () => collectPrContext("123", executeGh),
    /baseRefOid must be a 40-character lowercase commit SHA/u,
  );
});
