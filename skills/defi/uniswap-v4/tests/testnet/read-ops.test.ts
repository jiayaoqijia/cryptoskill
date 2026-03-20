/**
 * Testnet tests — Read-only operations on Base Sepolia.
 *
 * Verifies that contracts exist and respond on the testnet.
 * No funds needed, no private key needed.
 */
import { describe, it, expect, beforeAll } from "vitest";
import { JsonRpcProvider, Contract } from "ethers";
import { getChainConfig } from "../../src/lib/addresses.js";
import { makeProvider, fetchRpcChainId } from "../../src/lib/provider.js";

const TESTNET_RPC = process.env.BASE_SEPOLIA_RPC_URL ?? "https://sepolia.base.org";

let provider: JsonRpcProvider;
let cfg: ReturnType<typeof getChainConfig>;

beforeAll(() => {
  cfg = getChainConfig("base-sepolia");
  provider = makeProvider("base-sepolia", TESTNET_RPC);
});

describe("Testnet: Contract existence", () => {
  it("PoolManager has bytecode", async () => {
    const code = await provider.getCode(cfg.poolManager);
    expect(code.length).toBeGreaterThan(2); // "0x" means no code
  });

  it("StateView has bytecode", async () => {
    const code = await provider.getCode(cfg.stateView);
    expect(code.length).toBeGreaterThan(2);
  });

  it("V4Quoter has bytecode", async () => {
    const code = await provider.getCode(cfg.quoter);
    expect(code.length).toBeGreaterThan(2);
  });

  it("Universal Router has bytecode", async () => {
    const code = await provider.getCode(cfg.universalRouter);
    expect(code.length).toBeGreaterThan(2);
  });

  it("Permit2 has bytecode", async () => {
    const code = await provider.getCode(cfg.permit2);
    expect(code.length).toBeGreaterThan(2);
  });
});

describe("Testnet: StateView responds", () => {
  it("getSlot0 returns zeros for non-existent pool (no revert)", async () => {
    const stateView = new Contract(
      cfg.stateView,
      ["function getSlot0(bytes32) view returns (uint160, int24, uint24, uint24)"],
      provider
    );
    const fakePoolId = "0x" + "00".repeat(32);
    const [sqrtPrice] = await stateView.getSlot0(fakePoolId);
    expect(sqrtPrice).toBe(0n);
  });

  it("getLiquidity returns zero for non-existent pool", async () => {
    const stateView = new Contract(
      cfg.stateView,
      ["function getLiquidity(bytes32) view returns (uint128)"],
      provider
    );
    const fakePoolId = "0x" + "00".repeat(32);
    const liq = await stateView.getLiquidity(fakePoolId);
    expect(liq).toBe(0n);
  });
});

describe("Testnet: Chain config validation", () => {
  it("chain ID matches", async () => {
    const chainId = await fetchRpcChainId(provider);
    expect(chainId).toBe(cfg.chainId);
  });
});
