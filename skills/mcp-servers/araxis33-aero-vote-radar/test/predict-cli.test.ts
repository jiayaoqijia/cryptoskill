import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { snapshotsFromDir } from "../src/predict-cli.js";

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

/** A fresh directory under the OS temp dir, cleaned up after the test runs. */
function withTempDir(files: Record<string, string>): string {
  const dir = mkdtempSync(join(tmpdir(), "predict-cli-test-"));
  for (const [name, contents] of Object.entries(files)) {
    writeFileSync(join(dir, name), contents, "utf8");
  }
  return dir;
}

test("snapshotsFromDir parses every .json file in the directory", () => {
  const dir = withTempDir({
    "a.json": '{"generatedAt":"2026-08-01T00:00:00.000Z","pools":[]}',
    "b.json": '{"generatedAt":"2026-08-08T00:00:00.000Z","pools":[]}',
  });
  try {
    const result = snapshotsFromDir(dir) as { generatedAt: string }[];
    assert.deepEqual(
      result.map((s) => s.generatedAt).sort(),
      ["2026-08-01T00:00:00.000Z", "2026-08-08T00:00:00.000Z"],
    );
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("snapshotsFromDir ignores non-.json files", () => {
  const dir = withTempDir({
    "snapshot.json": '{"generatedAt":"2026-08-01T00:00:00.000Z","pools":[]}',
    "README.md": "not a snapshot",
  });
  try {
    const result = snapshotsFromDir(dir);
    assert.equal(result.length, 1);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("snapshotsFromDir skips a file that fails to parse rather than throwing, matching snapshotsFromGit's tolerance for an unreadable commit", () => {
  const dir = withTempDir({
    "good.json": '{"generatedAt":"2026-08-01T00:00:00.000Z","pools":[]}',
    "corrupt.json": "{not valid json",
  });
  try {
    const { result, logged } = captureStderr(() => snapshotsFromDir(dir) as { generatedAt: string }[]);
    assert.equal(result.length, 1);
    assert.equal(result[0].generatedAt, "2026-08-01T00:00:00.000Z");
    assert.ok(logged.some((line) => line.includes("corrupt.json")), "should report which file it skipped");
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("snapshotsFromDir returns an empty array for a directory with no .json files", () => {
  const dir = withTempDir({ "notes.txt": "nothing here" });
  try {
    assert.deepEqual(snapshotsFromDir(dir), []);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});
