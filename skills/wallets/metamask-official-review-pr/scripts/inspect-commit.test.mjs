import assert from "node:assert/strict";
import test from "node:test";

import { inspectCommit } from "./inspect-commit.mjs";

const SHA = "a".repeat(40);
const PARENT = "b".repeat(40);

test("inspectCommit returns commit metadata and changed paths", () => {
  const calls = [];
  const executeGit = (args) => {
    calls.push(args);
    return {
      status: 0,
      stdout:
        args[0] === "show"
          ? `${SHA}\0Update package versions\0${PARENT}\n`
          : "package.json\nsrc/file.ts\n",
      stderr: "",
    };
  };

  assert.deepEqual(inspectCommit(SHA, executeGit), {
    sha: SHA,
    subject: "Update package versions",
    parents: [PARENT],
    changedPaths: ["package.json", "src/file.ts"],
  });
  assert.deepEqual(calls[1], ["diff-tree", "--root", "--no-commit-id", "--name-only", "-r", SHA]);
});

test("inspectCommit requires a frozen SHA", () => {
  assert.throws(() => inspectCommit("HEAD"), /40-character lowercase/u);
});
