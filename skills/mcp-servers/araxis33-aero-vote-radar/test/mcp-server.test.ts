import { test } from "node:test";
import assert from "node:assert/strict";
import { resolveSAero } from "../src/mcp-server.js";

// A valid `address` reads the wallet over RPC, so that branch is exercised live
// via the MCP server and the CLI; these cover every branch that doesn't.

test("resolveSAero rejects passing both amount and address", async () => {
  await assert.rejects(() => resolveSAero(25000, "0x1234567890123456789012345678901234567890"), /Pass either amount or address, not both/);
});

test("resolveSAero rejects passing neither", async () => {
  await assert.rejects(() => resolveSAero(undefined, undefined), /Provide either amount .* or address/);
});

test("resolveSAero rejects something that is not an address", async () => {
  await assert.rejects(() => resolveSAero(undefined, "0x123"), /Not a wallet address/);
});

test("resolveSAero returns the given amount unchanged when no address is given", async () => {
  assert.deepEqual(await resolveSAero(25000, undefined), { amount: 25000, wallet: undefined });
});
