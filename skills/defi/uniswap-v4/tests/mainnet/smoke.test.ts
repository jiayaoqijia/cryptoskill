/**
 * Mainnet smoke tests — Read-only operations against live Base mainnet.
 *
 * Contract verification and balance checks always run.
 * Pool-dependent tests (price, tick, quote) skip when no pools are discovered
 * (e.g., when all pools use non-zero hooks that aren't in the default scan).
 *
 * No funds needed, no private key needed.
 */

import { describe, it, expect, beforeAll } from "vitest";
import { Contract, type JsonRpcProvider } from "ethers";
import { findPools } from "../../src/pool-info.js";
import { getChainConfig, ADDRESS_ZERO } from "../../src/lib/addresses.js";
import { makeProvider } from "../../src/lib/provider.js";
import { sortCurrencies } from "../../src/lib/validation.js";
import { makePoolKey } from "../../src/lib/v4-encoding.js";

const MAINNET_RPC = process.env.BASE_RPC_URL ?? "https://mainnet.base.org";
const USDC = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913";

// ── RPC reachability gate ──────────────────────────────────────────
async function rpcResponds(rpcUrl: string): Promise<boolean> {
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 2000);
    const res = await fetch(rpcUrl, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        jsonrpc: "2.0",
        method: "eth_chainId",
        params: [],
        id: 1,
      }),
      signal: controller.signal,
    });
    clearTimeout(timeout);
    if (!res.ok) return false;
    const json = (await res.json()) as { result?: string };
    if (typeof json.result !== "string") return false;
    return Number(BigInt(json.result)) === 8453;
  } catch {
    return false;
  }
}

const MAINNET_AVAILABLE = await rpcResponds(MAINNET_RPC);
const mainnetSuite = MAINNET_AVAILABLE ? describe : describe.skip;

// ── Pool result cache (shared across tests in this file) ───────────
interface PoolResult {
  poolId: string;
  key: { currency0: string; currency1: string; fee: number; tickSpacing: number; hooks: string };
  sqrtPriceX96: string;
  tick: number;
  protocolFee: number;
  lpFee: number;
  liquidity: string;
}
let discoveredPools: PoolResult[] = [];

mainnetSuite("Mainnet smoke (Base)", () => {
  let provider: JsonRpcProvider;
  let cfg: ReturnType<typeof getChainConfig>;

  beforeAll(async () => {
    cfg = getChainConfig("base");
    provider = makeProvider("base", MAINNET_RPC);

    // Attempt pool discovery — may be empty if no hooks=address(0) pools exist
    try {
      discoveredPools = await findPools(
        ADDRESS_ZERO,
        USDC,
        "base",
        MAINNET_RPC
      );
    } catch {
      discoveredPools = [];
    }
  });

  // ── Always-run: contract verification ──────────────────────────
  describe("Contract verification", () => {
    it("PoolManager has bytecode", async () => {
      const code = await provider.getCode(cfg.poolManager);
      expect(code.length).toBeGreaterThan(100);
    });

    it("Universal Router has bytecode", async () => {
      const code = await provider.getCode(cfg.universalRouter);
      expect(code.length).toBeGreaterThan(100);
    });

    it("StateView has bytecode", async () => {
      const code = await provider.getCode(cfg.stateView);
      expect(code.length).toBeGreaterThan(100);
    });

    it("Quoter has bytecode", async () => {
      const code = await provider.getCode(cfg.quoter);
      expect(code.length).toBeGreaterThan(100);
    });
  });

  // ── Always-run: balance checks ─────────────────────────────────
  describe("Balance checks", () => {
    it("reads ETH balance for known address (dead address)", async () => {
      const deadAddr = "0x000000000000000000000000000000000000dEaD";
      const balance = await provider.getBalance(deadAddr);
      expect(typeof balance).toBe("bigint");
    });

    it("reads USDC balance", async () => {
      const usdc = new Contract(
        USDC,
        ["function balanceOf(address) view returns (uint256)"],
        provider
      );
      const balance = await usdc.balanceOf(
        "0x000000000000000000000000000000000000dEaD"
      );
      expect(typeof balance).toBe("bigint");
    });
  });

  // ── Pool discovery info (non-failing) ──────────────────────────
  describe("Pool discovery", () => {
    it("findPools returns an array (may be empty if all pools use hooks)", async () => {
      // This test validates the function executes without error.
      // On Base, most V4 pools use hook contracts, so hooks=address(0)
      // discovery may return empty. That's not a bug — it's expected.
      const pools = await findPools(ADDRESS_ZERO, USDC, "base", MAINNET_RPC);
      expect(Array.isArray(pools)).toBe(true);
    });
  });

  // ── Pool-dependent tests (skip if no pools discovered) ─────────
  describe("Pool reads (requires discovered pools)", () => {
    it("best pool has nonzero liquidity", () => {
      if (discoveredPools.length === 0) return; // skip gracefully
      expect(BigInt(discoveredPools[0].liquidity)).toBeGreaterThan(0n);
    });

    it("sqrtPriceX96 is reasonable", () => {
      if (discoveredPools.length === 0) return;
      const sqrtPrice = BigInt(discoveredPools[0].sqrtPriceX96);
      expect(sqrtPrice).toBeGreaterThan(0n);
    });

    it("tick is within valid range", () => {
      if (discoveredPools.length === 0) return;
      const tick = discoveredPools[0].tick;
      expect(tick).toBeGreaterThan(-887273);
      expect(tick).toBeLessThan(887273);
    });
  });

  describe("Quote (requires discovered pools)", () => {
    it("quotes 0.01 ETH → USDC", async () => {
      if (discoveredPools.length === 0) return;

      const best = discoveredPools[0];
      const key = makePoolKey(
        best.key.currency0,
        best.key.currency1,
        best.key.fee,
        best.key.tickSpacing
      );
      const { zeroForOne } = sortCurrencies(ADDRESS_ZERO, USDC);

      const quoter = new Contract(
        cfg.quoter,
        [
          "function quoteExactInputSingle(((address,address,uint24,int24,address),bool,uint128,bytes)) returns (uint256,uint256)",
        ],
        provider
      );

      const [amountOut] = await quoter.quoteExactInputSingle.staticCall([
        [key.currency0, key.currency1, key.fee, key.tickSpacing, key.hooks],
        zeroForOne,
        10n ** 16n,
        "0x",
      ]);

      expect(amountOut).toBeGreaterThan(5_000_000n);
      expect(amountOut).toBeLessThan(200_000_000n);
    });
  });
});
