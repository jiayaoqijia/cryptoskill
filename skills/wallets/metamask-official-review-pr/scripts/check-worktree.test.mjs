import assert from "node:assert/strict";
import test from "node:test";

import { checkWorktree } from "./check-worktree.mjs";

test("checkWorktree reports a clean checkout", () => {
  const executeGit = (args) => {
    assert.deepEqual(args, ["status", "--porcelain"]);
    return "";
  };

  assert.deepEqual(checkWorktree(executeGit), {
    clean: true,
    status: "",
  });
});

test("checkWorktree returns the exact dirty status", () => {
  const executeGit = () => " M app/file.ts\n";

  assert.deepEqual(checkWorktree(executeGit), {
    clean: false,
    status: " M app/file.ts\n",
  });
});
