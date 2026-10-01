import assert from "node:assert/strict";
import test from "node:test";

import { searchFrozenTree } from "./search-frozen-tree.mjs";

const SHA = "a".repeat(40);

test("searchFrozenTree returns structured fixed-string matches", () => {
  const executeGit = (args) => {
    assert.deepEqual(args, ["grep", "-n", "-I", "-F", "-e", "expo", SHA, "--", "package.json"]);
    return {
      status: 0,
      stdout: `${SHA}:package.json:10:    "expo": "1.0.0"\n`,
      stderr: "",
    };
  };

  assert.deepEqual(searchFrozenTree(SHA, "expo", ["package.json"], executeGit), {
    commitSha: SHA,
    pattern: "expo",
    paths: ["package.json"],
    matches: [
      {
        commitSha: SHA,
        path: "package.json",
        line: 10,
        text: '    "expo": "1.0.0"',
      },
    ],
    truncated: false,
  });
});

test("searchFrozenTree treats status one as an empty result", () => {
  const executeGit = () => ({ status: 1, stdout: "", stderr: "" });

  assert.deepEqual(searchFrozenTree(SHA, "missing", [], executeGit).matches, []);
});

test("searchFrozenTree validates search paths", () => {
  assert.throws(() => searchFrozenTree(SHA, "value", ["../outside"]), /repository-relative/u);
});
