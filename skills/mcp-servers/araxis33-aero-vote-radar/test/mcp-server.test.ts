import { test } from "node:test";
import assert from "node:assert/strict";
import { resolveVeAeroBudget } from "../src/mcp-server.js";

// resolveVeAeroBudget backs both the recommend_allocation and backtest_strategy
// tools' budget resolution, but had no direct test coverage — same gap
// cli.test.ts already closed for its own veaero/address resolver (resolveBudget).
// A given `address` still hits fetchVeAeroPositions, so that branch is exercised
// live via the MCP server / CLI instead, same as fetchActivePools/
// fetchVeAeroPositions elsewhere; these cover every branch that doesn't require
// a live RPC call.

test("resolveVeAeroBudget rejects passing both veAero and address", async () => {
  await assert.rejects(
    () => resolveVeAeroBudget(25000, "0x1234567890123456789012345678901234567890"),
    /Pass either veAero or address, not both/,
  );
});

test("resolveVeAeroBudget rejects passing neither veAero nor address", async () => {
  await assert.rejects(
    () => resolveVeAeroBudget(undefined, undefined),
    /Provide either veAero .* or address/,
  );
});

test("resolveVeAeroBudget returns the given veAero amount unchanged when no address is given", async () => {
  assert.equal(await resolveVeAeroBudget(25000, undefined), 25000);
});
