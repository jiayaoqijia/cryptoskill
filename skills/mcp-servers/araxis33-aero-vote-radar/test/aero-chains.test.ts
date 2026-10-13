import { test } from "node:test";
import assert from "node:assert/strict";
import { CHAINS, classifyChainFile, matchChainKey } from "../scripts/aero-chains.mjs";

test("matchChainKey recognises every chain's plain file name", () => {
  for (const key of Object.keys(CHAINS)) {
    assert.equal(matchChainKey(`${key}.json`), key, `${key}.json should match ${key}`);
  }
});

test("matchChainKey accepts the documented ethereum/optimism/arbitrum aliases", () => {
  assert.equal(matchChainKey("eth.json"), "ethereum");
  assert.equal(matchChainKey("mainnet.json"), "ethereum");
  assert.equal(matchChainKey("op.json"), "optimism");
  assert.equal(matchChainKey("arb.json"), "arbitrum");
});

test("matchChainKey is case-insensitive", () => {
  assert.equal(matchChainKey("BASE.JSON"), "base");
  assert.equal(matchChainKey("Arc.json"), "arc");
});

test("matchChainKey returns undefined for a file naming no known chain", () => {
  assert.equal(matchChainKey("polygon.json"), undefined);
  assert.equal(matchChainKey("README.json"), undefined);
});

test("classifyChainFile reports pools true for a factory registry or a pool factory, false otherwise", () => {
  assert.deepEqual(classifyChainFile(["factoryregistry"]), { pools: true, allocation: false });
  assert.deepEqual(classifyChainFile(["clpoolfactory", "voter"]), { pools: true, allocation: true });
  assert.deepEqual(classifyChainFile(["votingescrow"]), { pools: false, allocation: false });
});

test("classifyChainFile reports allocation true only when a voter contract is named", () => {
  assert.deepEqual(classifyChainFile(["leafvoter"]), { pools: false, allocation: true });
  assert.deepEqual(classifyChainFile([]), { pools: false, allocation: false });
});
