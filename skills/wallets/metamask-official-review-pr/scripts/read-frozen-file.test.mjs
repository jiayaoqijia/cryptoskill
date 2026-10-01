import assert from "node:assert/strict";
import test from "node:test";

import { readFrozenFile } from "./read-frozen-file.mjs";

const SHA = "a".repeat(40);

test("readFrozenFile reads a validated path at a frozen commit", () => {
  const executeGit = (args) => {
    assert.deepEqual(args, ["show", `${SHA}:package.json`]);
    return { status: 0, stdout: '{"name":"fixture"}\n', stderr: "" };
  };

  assert.deepEqual(readFrozenFile(SHA, "package.json", executeGit), {
    commitSha: SHA,
    path: "package.json",
    content: '{"name":"fixture"}\n',
  });
});

test("readFrozenFile rejects repository traversal", () => {
  assert.throws(() => readFrozenFile(SHA, "../package.json"), /repository-relative/u);
});
