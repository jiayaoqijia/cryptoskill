/**
 * Fork tests — Integration tests on Anvil Base mainnet fork.
 *
 * Tests pool discovery, quoting, approval, and swap execution against real pool state.
 * Requires: anvil running with --fork-url <Base RPC>
 *
 * Run:
 *   anvil --fork-url https://mainnet.base.org --port 8545 &
 *   npx vitest run tests/fork/
 */

import { describe, it, expect, beforeAll } from "vitest";
import { JsonRpcProvider, Wallet, Contract, parseEther } from "ethers";
import { findPools } from "../../src/pool-info.js";
import { makePoolKey, buildExecuteCalldata } from "../../src/lib/v4-encoding.js";
import { sortCurrencies, applySlippage } from "../../src/lib/validation.js";
import { getChainConfig, ADDRESS_ZERO } from "../../src/lib/addresses.js";

const FORK_RPC = process.env.FORK_RPC_URL ?? "http://127.0.0.1:8545";
const USDC = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913";

// Anvil default account #0 (funded with 10000 ETH)
const ANVIL_KEY =
  "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80";

const STATE_VIEW_ABI = [
  "function getSlot0(bytes32 poolId) view returns (uint160, int24, uint24, uint24)",
  "function getLiquidity(bytes32 poolId) view returns (uint128)",
];

const QUOTER_ABI = [
  "function quoteExactInputSingle(((address,address,uint24,int24,address),bool,uint128,bytes)) returns (uint256, uint256)",
];

const ROUTER_ABI = [
  "function execute(bytes commands, bytes[] inputs, uint256 deadline) payable",
];

const ERC20_ABI = ["function balanceOf(address) view returns (uint256)"];

async function rpcResponds(rpcUrl: string): Promise<boolean> {
  try {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 1500);

    const res = await fetch(rpcUrl, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        jsonrpc: "2.0",
        method: "eth_blockNumber",
        params: [],
        id: 1,
      }),
      signal: controller.signal,
    });

    clearTimeout(timeout);
    if (!res.ok) return false;

    const json = (await res.json()) as { result?: string };
    return typeof json.result === "string";
  } catch {
    return false;
  }
}

const FORK_AVAILABLE = await rpcResponds(FORK_RPC);
const forkSuite = FORK_AVAILABLE ? describe : describe.skip;

forkSuite("Fork (Anvil Base mainnet fork)", () => {
  let provider: JsonRpcProvider;
  let wallet: Wallet;
  let cfg: ReturnType<typeof getChainConfig>;

  beforeAll(async () => {
    provider = new JsonRpcProvider(FORK_RPC);
    wallet = new Wallet(ANVIL_KEY, provider);
    cfg = getChainConfig("base");
  });

  describe("Pool Discovery", () => {
    it("finds ETH/USDC pools on Base fork", async () => {
      const pools = await findPools(ADDRESS_ZERO, USDC, "base", FORK_RPC);
      expect(pools.length).toBeGreaterThan(0);

      // Best pool (highest liquidity) should be first
      const best = pools[0];
      expect(BigInt(best.liquidity)).toBeGreaterThan(0n);
      expect(BigInt(best.sqrtPriceX96)).toBeGreaterThan(0n);
      expect(best.tick).toBeDefined();
    });

    it("returns pools sorted by liquidity (highest first)", async () => {
      const pools = await findPools(ADDRESS_ZERO, USDC, "base", FORK_RPC);
      if (pools.length >= 2) {
        expect(BigInt(pools[0].liquidity)).toBeGreaterThanOrEqual(
          BigInt(pools[1].liquidity)
        );
      }
    });

    it("returns empty for non-existent pair", async () => {
      const fakeToken = "0x0000000000000000000000000000000000000001";
      const pools = await findPools(fakeToken, USDC, "base", FORK_RPC);
      expect(pools.length).toBe(0);
    });
  });

  describe("StateView reads", () => {
    it("reads slot0 from StateView contract", async () => {
      const stateView = new Contract(cfg.stateView, STATE_VIEW_ABI, provider);
      const pools = await findPools(ADDRESS_ZERO, USDC, "base", FORK_RPC);
      expect(pools.length).toBeGreaterThan(0);

      const poolId = pools[0].poolId;
      const [sqrtPrice, tick, _protocolFee, lpFee] = await stateView.getSlot0(
        poolId
      );
      expect(sqrtPrice).toBeGreaterThan(0n);
      expect(typeof tick).toBe("bigint");
      expect(typeof lpFee).toBe("bigint");
    });

    it("reads liquidity from StateView contract", async () => {
      const stateView = new Contract(cfg.stateView, STATE_VIEW_ABI, provider);
      const pools = await findPools(ADDRESS_ZERO, USDC, "base", FORK_RPC);
      expect(pools.length).toBeGreaterThan(0);

      const poolId = pools[0].poolId;
      const liquidity = await stateView.getLiquidity(poolId);
      expect(liquidity).toBeGreaterThan(0n);
    });
  });

  describe("Quoter", () => {
    it("quotes ETH→USDC swap via V4Quoter", async () => {
      const pools = await findPools(ADDRESS_ZERO, USDC, "base", FORK_RPC);
      expect(pools.length).toBeGreaterThan(0);

      const best = pools[0];
      const key = makePoolKey(
        best.key.currency0,
        best.key.currency1,
        best.key.fee,
        best.key.tickSpacing
      );
      const { zeroForOne } = sortCurrencies(ADDRESS_ZERO, USDC);

      const quoter = new Contract(cfg.quoter, QUOTER_ABI, provider);
      const [amountOut, gasEstimate] =
        await quoter.quoteExactInputSingle.staticCall([
          [key.currency0, key.currency1, key.fee, key.tickSpacing, key.hooks],
          zeroForOne,
          parseEther("0.01"),
          "0x",
        ]);

      // 0.01 ETH should quote to roughly $25-50 of USDC (6 decimals)
      expect(amountOut).toBeGreaterThan(0n);
      expect(amountOut).toBeGreaterThan(10_000_000n); // > $10 USDC
      expect(amountOut).toBeLessThan(100_000_000n); // < $100 USDC
      expect(gasEstimate).toBeGreaterThan(0n);
    });
  });

  describe("Swap Execution", () => {
    it(
      "swaps ETH→USDC via Universal Router",
      async () => {
        // Get initial USDC balance
        const usdc = new Contract(USDC, ERC20_ABI, provider);
        const balanceBefore = (await usdc.balanceOf(wallet.address)) as bigint;

        // Discover best pool
        const pools = await findPools(ADDRESS_ZERO, USDC, "base", FORK_RPC);
        expect(pools.length).toBeGreaterThan(0);

        const best = pools[0];
        const key = makePoolKey(
          best.key.currency0,
          best.key.currency1,
          best.key.fee,
          best.key.tickSpacing
        );
        const { zeroForOne } = sortCurrencies(ADDRESS_ZERO, USDC);

        // Quote
        const quoter = new Contract(cfg.quoter, QUOTER_ABI, provider);
        const [expectedOut] = await quoter.quoteExactInputSingle.staticCall([
          [key.currency0, key.currency1, key.fee, key.tickSpacing, key.hooks],
          zeroForOne,
          parseEther("0.001"),
          "0x",
        ]);

        const minOut = applySlippage(expectedOut as bigint, 100); // 1% slippage

        // Build and send swap
        const deadline = BigInt(Math.floor(Date.now() / 1000) + 300);
        const { commands, inputs } = buildExecuteCalldata(
          key,
          zeroForOne,
          parseEther("0.001"),
          minOut,
          deadline
        );

        const router = new Contract(cfg.universalRouter, ROUTER_ABI, wallet);
        const tx = await router.execute(commands, inputs, deadline, {
          value: parseEther("0.001"),
        });
        const receipt = await tx.wait();
        expect(receipt?.status).toBe(1);

        // Verify USDC balance increased
        const balanceAfter = (await usdc.balanceOf(wallet.address)) as bigint;
        expect(balanceAfter).toBeGreaterThan(balanceBefore);

        const received = balanceAfter - balanceBefore;
        expect(received).toBeGreaterThanOrEqual(minOut);
      },
      30_000
    );

    it("reverts with insufficient balance for large amount", async () => {
      const pools = await findPools(ADDRESS_ZERO, USDC, "base", FORK_RPC);
      expect(pools.length).toBeGreaterThan(0);

      const best = pools[0];
      const key = makePoolKey(
        best.key.currency0,
        best.key.currency1,
        best.key.fee,
        best.key.tickSpacing
      );
      const { zeroForOne } = sortCurrencies(ADDRESS_ZERO, USDC);

      // Use a new wallet with zero balance
      const emptyWallet = Wallet.createRandom().connect(provider);
      const deadline = BigInt(Math.floor(Date.now() / 1000) + 300);
      const { commands, inputs } = buildExecuteCalldata(
        key,
        zeroForOne,
        parseEther("1000"),
        0n,
        deadline
      );

      const router = new Contract(cfg.universalRouter, ROUTER_ABI, emptyWallet);
      await expect(
        router.execute(commands, inputs, deadline, { value: parseEther("1000") })
      ).rejects.toThrow();
    });

    it("reverts on invalid pool (non-existent pair)", async () => {
      const fakeToken = "0x0000000000000000000000000000000000000001";
      const { currency0, currency1, zeroForOne } = sortCurrencies(
        ADDRESS_ZERO,
        fakeToken
      );
      const key = makePoolKey(currency0, currency1, 500, 10);
      const deadline = BigInt(Math.floor(Date.now() / 1000) + 300);
      const { commands, inputs } = buildExecuteCalldata(
        key,
        zeroForOne,
        1000n,
        0n,
        deadline
      );

      const router = new Contract(cfg.universalRouter, ROUTER_ABI, wallet);
      await expect(
        router.execute(commands, inputs, deadline, { value: 1000n })
      ).rejects.toThrow();
    });
  });
});
