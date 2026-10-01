#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { pathToFileURL } from "node:url";

const SHA_PATTERN = /^[0-9a-f]{40}$/u;

const readJsonFile = (sha, path) => {
  if (!SHA_PATTERN.test(sha)) {
    throw new Error("sha must be a 40-character lowercase commit SHA");
  }
  if (
    path.length === 0 ||
    path.startsWith("/") ||
    path.split("/").includes("..") ||
    path.includes("\0")
  ) {
    throw new Error("path must be a repository-relative path");
  }

  const result = spawnSync("git", ["show", `${sha}:${path}`], {
    encoding: "utf8",
    maxBuffer: 100 * 1024 * 1024,
    shell: false,
  });
  if (result.error || result.status !== 0) {
    throw new Error(result.stderr?.trim() || result.error?.message || "git failed");
  }
  return { commitSha: sha, path, content: result.stdout };
};

const parseJson = (value, source) => {
  try {
    return JSON.parse(value);
  } catch (error) {
    const detail = error instanceof Error ? error.message : String(error);
    throw new Error(`${source} returned invalid JSON: ${detail}`);
  }
};

const decodePointerPart = (part) => part.replaceAll("~1", "/").replaceAll("~0", "~");

export const readJsonPointer = (document, pointer) => {
  if (pointer === "") {
    return document;
  }
  if (!pointer.startsWith("/")) {
    throw new Error(`JSON Pointer must start with /: ${pointer}`);
  }

  return pointer
    .slice(1)
    .split("/")
    .map(decodePointerPart)
    .reduce((value, key) => {
      if (value === null || typeof value !== "object" || !Object.hasOwn(value, key)) {
        throw new Error(`JSON Pointer does not exist: ${pointer}`);
      }
      return value[key];
    }, document);
};

export const readFrozenJson = (sha, path, pointers, readFile = readJsonFile) => {
  if (pointers.length === 0) {
    throw new Error("at least one JSON Pointer is required");
  }

  const file = readFile(sha, path);
  const document = parseJson(file.content, `${file.commitSha}:${file.path}`);

  return {
    commitSha: file.commitSha,
    path: file.path,
    values: Object.fromEntries(
      pointers.map((pointer) => [pointer, readJsonPointer(document, pointer)]),
    ),
  };
};

const main = ([sha, path, ...pointers]) => {
  if (!sha || !path || pointers.length === 0) {
    throw new Error(
      "Usage: node scripts/read-frozen-json.mjs <commit-sha> <repository-path> <json-pointer> [json-pointer...]",
    );
  }

  return readFrozenJson(sha, path, pointers);
};

if (process.argv[1] !== undefined && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    process.stdout.write(`${JSON.stringify(main(process.argv.slice(2)), null, 2)}\n`);
  } catch (error) {
    const detail = error instanceof Error ? error.message : String(error);
    process.stderr.write(`read-frozen-json: ${detail}\n`);
    process.exitCode = 1;
  }
}
