#!/usr/bin/env node
import { writeSnapshot } from "./snapshot.js";
import { formatError } from "./util.js";

/**
 * Entrypoint for the scheduled snapshot job. Kept separate from snapshot.js so
 * the pure helpers there stay importable from tests without the import itself
 * kicking off a live chain scan — the same split cli.ts and mcp-server.ts use.
 */
async function main() {
  const outPath = process.argv[2] ?? "docs/data/snapshot.json";
  const snapshot = await writeSnapshot(outPath);
  console.error(`wrote ${snapshot.poolCount} pools to ${outPath}`);
}

main().catch((err) => {
  console.error(`Error: ${formatError(err)}`);
  process.exitCode = 1;
});
