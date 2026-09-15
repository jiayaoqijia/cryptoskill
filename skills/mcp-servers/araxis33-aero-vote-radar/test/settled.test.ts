import { test } from "node:test";
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { snapshotsFromGit } from "../src/settled.js";

/** Runs `fn` with console.error silenced, returning its return value and everything logged. */
function captureStderr<T>(fn: () => T): { result: T; logged: string[] } {
  const original = console.error;
  const logged: string[] = [];
  console.error = (...parts: unknown[]) => {
    logged.push(parts.join(" "));
  };
  try {
    return { result: fn(), logged };
  } finally {
    console.error = original;
  }
}

/** Runs `fn` with the process cwd temporarily switched to `dir`, always restoring it after. */
function withCwd<T>(dir: string, fn: () => T): T {
  const original = process.cwd();
  process.chdir(dir);
  try {
    return fn();
  } finally {
    process.chdir(original);
  }
}

function git(dir: string, ...args: string[]): void {
  execFileSync("git", args, { cwd: dir, encoding: "utf8" });
}

/** A fresh git repo under the OS temp dir, with `git` and a clean commit identity configured. */
function freshRepo(): string {
  const dir = mkdtempSync(join(tmpdir(), "settled-test-"));
  git(dir, "init", "-q");
  git(dir, "config", "user.email", "test@example.com");
  git(dir, "config", "user.name", "Test");
  return dir;
}

test("snapshotsFromGit returns every committed revision of the file, newest first", () => {
  const dir = freshRepo();
  try {
    writeFileSync(join(dir, "snapshot.json"), '{"generatedAt":"2026-08-01T00:00:00.000Z"}', "utf8");
    git(dir, "add", "snapshot.json");
    git(dir, "commit", "-q", "-m", "first");

    writeFileSync(join(dir, "snapshot.json"), '{"generatedAt":"2026-08-08T00:00:00.000Z"}', "utf8");
    git(dir, "add", "snapshot.json");
    git(dir, "commit", "-q", "-m", "second");

    const result = withCwd(dir, () => snapshotsFromGit("snapshot.json")) as { generatedAt: string }[];
    assert.deepEqual(
      result.map((s) => s.generatedAt),
      ["2026-08-08T00:00:00.000Z", "2026-08-01T00:00:00.000Z"],
    );
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("snapshotsFromGit skips a commit whose file content doesn't parse as JSON rather than throwing", () => {
  const dir = freshRepo();
  try {
    writeFileSync(join(dir, "snapshot.json"), "{not valid json", "utf8");
    git(dir, "add", "snapshot.json");
    git(dir, "commit", "-q", "-m", "corrupt");

    writeFileSync(join(dir, "snapshot.json"), '{"generatedAt":"2026-08-08T00:00:00.000Z"}', "utf8");
    git(dir, "add", "snapshot.json");
    git(dir, "commit", "-q", "-m", "good");

    const result = withCwd(dir, () => snapshotsFromGit("snapshot.json")) as { generatedAt: string }[];
    assert.equal(result.length, 1);
    assert.equal(result[0].generatedAt, "2026-08-08T00:00:00.000Z");
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("snapshotsFromGit returns an empty array for a path with no history in this repo", () => {
  const dir = freshRepo();
  try {
    writeFileSync(join(dir, "unrelated.json"), '{"a":1}', "utf8");
    git(dir, "add", "unrelated.json");
    git(dir, "commit", "-q", "-m", "unrelated");

    const result = withCwd(dir, () => snapshotsFromGit("snapshot.json"));
    assert.deepEqual(result, []);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("snapshotsFromGit returns an empty array and reports the failure when run outside a git repository", () => {
  const dir = mkdtempSync(join(tmpdir(), "settled-test-nogit-"));
  try {
    const { result, logged } = withCwd(dir, () => captureStderr(() => snapshotsFromGit("snapshot.json")));
    assert.deepEqual(result, []);
    assert.ok(
      logged.some((line) => line.includes("Could not read the snapshot history from git")),
      "should explain why it came back empty",
    );
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});
