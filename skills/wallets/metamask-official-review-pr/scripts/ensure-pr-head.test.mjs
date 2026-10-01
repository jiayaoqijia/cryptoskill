import assert from "node:assert/strict";
import test from "node:test";

import { ensurePrHead } from "./ensure-pr-head.mjs";

const HEAD_SHA = "2".repeat(40);

test("ensurePrHead reuses an available frozen commit", () => {
  const calls = [];
  const executeGit = (args) => {
    calls.push(args);
    return { status: 0, stdout: "", stderr: "" };
  };

  assert.deepEqual(ensurePrHead("123", HEAD_SHA, executeGit), {
    headSha: HEAD_SHA,
    fetched: false,
  });
  assert.equal(calls.length, 1);
});

test("ensurePrHead fetches and validates a missing pull request head", () => {
  const calls = [];
  const executeGit = (args) => {
    calls.push(args);
    if (args[0] === "cat-file") {
      return { status: 1, stdout: "", stderr: "missing" };
    }
    if (args[0] === "rev-parse") {
      return { status: 0, stdout: `${HEAD_SHA}\n`, stderr: "" };
    }
    return { status: 0, stdout: "", stderr: "" };
  };

  assert.deepEqual(ensurePrHead("123", HEAD_SHA, executeGit), {
    headSha: HEAD_SHA,
    fetched: true,
  });
  assert.deepEqual(calls[1], ["fetch", "--no-tags", "origin", "refs/pull/123/head"]);
});

test("ensurePrHead rejects a moved pull request head", () => {
  const executeGit = (args) => ({
    status: args[0] === "cat-file" ? 1 : 0,
    stdout: args[0] === "rev-parse" ? `${"3".repeat(40)}\n` : "",
    stderr: "",
  });

  assert.throws(() => ensurePrHead("123", HEAD_SHA, executeGit), /does not match frozen head/u);
});
