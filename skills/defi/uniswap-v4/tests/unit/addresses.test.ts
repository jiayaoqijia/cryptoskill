/**
 * Unit tests for address resolution and chain config.
 */
import { describe, it, expect } from "vitest";
import {
  getChainConfig,
  isSupportedChain,
  resolveRpcUrl,
  ADDRESS_ZERO,
  FEE_TIERS,
} from "../../src/lib/addresses.js";

describe("getChainConfig", () => {
  it("base has correct PoolManager", () => {
    const cfg = getChainConfig("base");
    expect(cfg.poolManager).toBe("0x498581fF718922c3f8e6A244956aF099B2652b2b");
    expect(cfg.chainId).toBe(8453);
  });

  it("base has canonical Universal Router (H-01 fix)", () => {
    const cfg = getChainConfig("base");
    // Canonical address from docs.uniswap.org/contracts/v4/deployments
    expect(cfg.universalRouter.toLowerCase()).toBe(
      "0x6ff5693b99212da76ad316178a184ab56d299b43"
    );
  });

  it("base has canonical Permit2 (H-01 fix)", () => {
    const cfg = getChainConfig("base");
    expect(cfg.permit2).toBe("0x000000000022D473030F116dDEE9F6B43aC78BA3");
  });

  it("ethereum has correct addresses", () => {
    const cfg = getChainConfig("ethereum");
    expect(cfg.poolManager).toBe("0x000000000004444c5dc75cB358380D2e3dE08A90");
    expect(cfg.universalRouter.toLowerCase()).toBe(
      "0x66a9893cc07d91d95644aedd05d03f95e1dba8af"
    );
    expect(cfg.chainId).toBe(1);
  });

  it("base-sepolia has testnet addresses", () => {
    const cfg = getChainConfig("base-sepolia");
    expect(cfg.chainId).toBe(84532);
    expect(cfg.poolManager).toBe("0x05E73354cFDd6745C338b50BcFDfA3Aa6fA03408");
  });

  it("Permit2 is the same on all chains", () => {
    const base = getChainConfig("base");
    const eth = getChainConfig("ethereum");
    const sep = getChainConfig("base-sepolia");
    expect(base.permit2).toBe(eth.permit2);
    expect(base.permit2).toBe(sep.permit2);
  });
});

describe("isSupportedChain", () => {
  it("base is supported", () => expect(isSupportedChain("base")).toBe(true));
  it("ethereum is supported", () => expect(isSupportedChain("ethereum")).toBe(true));
  it("base-sepolia is supported", () => expect(isSupportedChain("base-sepolia")).toBe(true));
  it("solana is not", () => expect(isSupportedChain("solana")).toBe(false));
  it("empty is not", () => expect(isSupportedChain("")).toBe(false));
});

describe("resolveRpcUrl", () => {
  it("explicit URL takes priority", () => {
    expect(resolveRpcUrl("base", "http://localhost:8545")).toBe("http://localhost:8545");
  });

  it("falls back to env var", () => {
    const old = process.env.BASE_RPC_URL;
    process.env.BASE_RPC_URL = "https://test-rpc.example.com";
    expect(resolveRpcUrl("base")).toBe("https://test-rpc.example.com");
    if (old !== undefined) process.env.BASE_RPC_URL = old;
    else delete process.env.BASE_RPC_URL;
  });

  it("throws if no URL available", () => {
    const old = process.env.BASE_RPC_URL;
    delete process.env.BASE_RPC_URL;
    expect(() => resolveRpcUrl("base")).toThrow("No RPC URL");
    if (old !== undefined) process.env.BASE_RPC_URL = old;
  });
});

describe("constants", () => {
  it("ADDRESS_ZERO is 42 chars", () => {
    expect(ADDRESS_ZERO).toBe("0x0000000000000000000000000000000000000000");
    expect(ADDRESS_ZERO.length).toBe(42);
  });

  it("FEE_TIERS includes dynamic fee with multiple tick spacings (M-04 fix)", () => {
    const dynamicFee = 8388608; // 2^23
    const dynamicTiers = FEE_TIERS.filter(([f]) => f === dynamicFee);
    expect(dynamicTiers.length).toBeGreaterThanOrEqual(2);
    const tickSpacings = dynamicTiers.map(([, ts]) => ts);
    expect(tickSpacings).toContain(60);  // Clanker-style
    expect(tickSpacings).toContain(200);
  });
});
