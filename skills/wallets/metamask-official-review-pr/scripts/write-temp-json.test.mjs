import assert from "node:assert/strict";
import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { dirname, join } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { writeTempJson } from "./write-temp-json.mjs";

const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
const SHA = "a".repeat(40);
const ignored = () => true;
const roots = [];

const repositoryRoot = () => {
  const root = mkdtempSync(join(SCRIPT_DIR, ".write-temp-json-"));
  roots.push(root);
  return root;
};

test.after(() => {
  for (const root of roots) {
    rmSync(root, { recursive: true, force: true });
  }
});

test("writeTempJson creates an empty JSON file in the repository temp directory", () => {
  const repoRoot = repositoryRoot();
  const path = writeTempJson({
    basename: `review-pr-${SHA}.json`,
    repoRoot,
    isIgnored: ignored,
  });

  assert.equal(path, join(repoRoot, "temp", `review-pr-${SHA}.json`));
  assert.equal(readFileSync(path, "utf8"), "{}\n");
});

test("writeTempJson accepts a pending-review manifest name", () => {
  const repoRoot = repositoryRoot();
  const path = writeTempJson({
    basename: `review-pr-pending-${SHA}.json`,
    repoRoot,
    isIgnored: ignored,
  });

  assert.equal(readFileSync(path, "utf8"), "{}\n");
});

test("writeTempJson refuses a repository that does not ignore temp/", () => {
  const repoRoot = repositoryRoot();

  assert.throws(
    () =>
      writeTempJson({
        basename: `review-pr-${SHA}.json`,
        repoRoot,
        isIgnored: () => false,
      }),
    /temp\/ is not gitignored/u,
  );
});

test("writeTempJson rejects a basename outside the two report names", () => {
  assert.throws(
    () =>
      writeTempJson({
        basename: "../review-pr.json",
        repoRoot: "/repository",
        isIgnored: ignored,
      }),
    /basename must be review-pr-/u,
  );
});
