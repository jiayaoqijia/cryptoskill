import assert from "node:assert/strict";
import test from "node:test";

import { readFrozenJson, readJsonPointer } from "./read-frozen-json.mjs";

const SHA = "a".repeat(40);

test("readFrozenJson returns selected values from a frozen JSON file", () => {
  const readFile = () => ({
    commitSha: SHA,
    path: "package.json",
    content: JSON.stringify({
      dependencies: {
        expo: "1.0.0",
        "react/native": "2.0.0",
      },
    }),
  });

  assert.deepEqual(
    readFrozenJson(
      SHA,
      "package.json",
      ["/dependencies/expo", "/dependencies/react~1native"],
      readFile,
    ),
    {
      commitSha: SHA,
      path: "package.json",
      values: {
        "/dependencies/expo": "1.0.0",
        "/dependencies/react~1native": "2.0.0",
      },
    },
  );
});

test("readJsonPointer rejects a missing value", () => {
  assert.throws(() => readJsonPointer({}, "/dependencies/expo"), /JSON Pointer does not exist/u);
});

test("readFrozenJson requires at least one pointer", () => {
  assert.throws(() => readFrozenJson(SHA, "package.json", []), /at least one JSON Pointer/u);
});
