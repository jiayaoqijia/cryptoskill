---
name: uniswap-v4
description: >
  Swap tokens and read pool state on Uniswap V4 (Base, Ethereum). Use when the agent
  needs to: (1) swap ERC20 tokens or ETH via Uniswap V4, (2) get pool info (price, tick,
  liquidity, fees), (3) find the best pool for a token pair, (4) quote expected swap output
  via the on-chain V4Quoter, (5) set up Permit2 approvals for the Universal Router, or
  (6) execute exact-input swaps with proper slippage protection. Supports Base and Ethereum
  mainnet, plus Base Sepolia testnet. TypeScript with strict types. Write operations
  need a private key via env var.
---

# Uniswap V4 🦄

Swap tokens and read pool state on Uniswap V4 via the Universal Router.

**Chains:** Base (8453), Ethereum (1), Base Sepolia (84532)

| Contract         | Base                                         | Ethereum                                     |
|------------------|----------------------------------------------|----------------------------------------------|
| PoolManager      | `0x498581fF718922c3f8e6A244956aF099B2652b2b` | `0x000000000004444c5dc75cB358380D2e3dE08A90` |
| UniversalRouter  | `0x6ff5693b99212da76ad316178a184ab56d299b43` | `0x66a9893cC07D91D95644AEDD05D03f95e1dBA8Af` |
| Permit2          | `0x000000000022D473030F116dDEE9F6B43aC78BA3` | `0x000000000022D473030F116dDEE9F6B43aC78BA3` |
| StateView        | `0xa3c0c9b65bad0b08107aa264b0f3db444b867a71` | `0x7ffe42c4a5deea5b0fec41c94c136cf115597227` |
| V4Quoter         | `0x0d5e0f971ed27fbff6c2837bf31316121532048d` | `0x52f0e24d1c21c8a0cb1e5a5dd6198556bd9e1203` |

> Addresses from [docs.uniswap.org/contracts/v4/deployments](https://docs.uniswap.org/contracts/v4/deployments), verified 2026-02-08.

## Decision Tree

1. **Read pool state?** → `src/pool-info.ts` (free, no gas, no key)
2. **Get swap quote?** → `src/quote.ts` (free, uses on-chain V4Quoter)
3. **Approve tokens?** → `src/approve.ts` (write, ~100K gas, needs `PRIVATE_KEY`)
4. **Execute swap?** → `src/swap.ts` (write, ~300-350K gas, needs `PRIVATE_KEY`)
5. **First time with an ERC20?** → Run approve first, or use `--auto-approve` on swap

## Scripts Reference

All scripts in `src/`. Run with `npx tsx`. Pass `--help` for usage.

### pool-info.ts — Read Pool State (free)

Returns pool ID, sqrtPriceX96, tick, liquidity, fees, token symbols/decimals.
Auto-detects the best pool by liquidity (or specify `--fee`/`--tick-spacing`).

```bash
npx tsx src/pool-info.ts --token0 ETH --token1 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 --chain base --rpc $BASE_RPC_URL
```

**Env:** `BASE_RPC_URL` or `ETH_RPC_URL` (or pass `--rpc`)

### quote.ts — Quote Swap Amounts (free)

Quotes exact input amounts via the on-chain V4Quoter contract (simulation, no tx).
Returns expected output amount and gas estimate.

```bash
npx tsx src/quote.ts \
  --token-in ETH \
  --token-out 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 \
  --amount 10000000000000000 \
  --chain base \
  --rpc $BASE_RPC_URL
```

**Env:** `BASE_RPC_URL` or `ETH_RPC_URL`

### approve.ts — Set Up Token Approvals (write)

Two-step Permit2 flow: ERC20 → Permit2, then Permit2 → Universal Router.
Skips if already approved. Only needed for ERC20 tokens (not ETH).

```bash
PRIVATE_KEY=0x... npx tsx src/approve.ts \
  --token 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 \
  --chain base \
  --rpc $BASE_RPC_URL \
  --json
```

**Env:** `PRIVATE_KEY` (required), `BASE_RPC_URL`

### swap.ts — Execute Swap (write)

Exact-input swap via Universal Router. Quotes expected output first, applies slippage,
then sends the transaction.

```bash
PRIVATE_KEY=0x... npx tsx src/swap.ts \
  --token-in ETH \
  --token-out 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 \
  --amount 10000000000000000 \
  --slippage 50 \
  --chain base \
  --rpc $BASE_RPC_URL \
  --json
```

With auto-approval (sets up Permit2 if needed):
```bash
PRIVATE_KEY=0x... npx tsx src/swap.ts \
  --token-in 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 \
  --token-out ETH \
  --amount 25000000 \
  --slippage 100 \
  --auto-approve \
  --chain base \
  --rpc $BASE_RPC_URL
```

**Options:** `--slippage <bps>` (default 50 = 0.5%), `--recipient <addr>`, `--auto-approve`, `--json`
**Env:** `PRIVATE_KEY` (required), `BASE_RPC_URL`

## Token Input

- `ETH` or `eth` → native ETH (address(0) in V4)
- Contract address → ERC20 token
- Common Base tokens: USDC `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`, WETH `0x4200000000000000000000000000000000000006`

## Environment Variables

| Variable              | Used By        | Required | Description                     |
|-----------------------|----------------|----------|---------------------------------|
| `PRIVATE_KEY`         | approve, swap  | Yes*     | Wallet private key (never CLI!) |
| `BASE_RPC_URL`        | all (Base)     | No       | Base mainnet RPC URL            |
| `ETH_RPC_URL`         | all (Ethereum) | No       | Ethereum mainnet RPC URL        |
| `BASE_SEPOLIA_RPC_URL`| all (testnet)  | No       | Base Sepolia RPC URL            |

\* Only required for write operations. Read operations (pool-info, quote) don't need a key.

## V4 Architecture Notes

- **Singleton PoolManager** holds all pools in one contract
- **State read** via StateView contract (wraps PoolManager storage)
- **Swaps:** Universal Router → PoolManager via V4_SWAP command
- **Approvals:** ERC20 → Permit2 → Universal Router (two-step)
- **Pool ID:** `keccak256(abi.encode(currency0, currency1, fee, tickSpacing, hooks))`
- **Currency ordering:** `currency0 < currency1` by numeric value. ETH = address(0)
- **Action sequence:** SWAP_EXACT_IN_SINGLE (0x06) + SETTLE_ALL (0x0c) + TAKE_ALL (0x0f)
- See `references/v4-encoding.md` for full encoding reference

## Error Handling

| Error                        | Cause                                      | Fix                                |
|------------------------------|--------------------------------------------|------------------------------------|
| `No V4 pool found`          | Pair not listed on V4 for this chain       | Check token addresses              |
| `Quote failed`              | Pool exists but can't simulate swap        | Check amount, pool may lack liq    |
| `PRIVATE_KEY required`      | Missing env var for write operation        | `export PRIVATE_KEY=0x...`         |
| `No RPC URL`                | Missing RPC config                         | Pass `--rpc` or set env var        |
| Tx reverts                  | Insufficient balance, expired, slippage    | Check balance, increase slippage   |
| `uint128 max`               | Amount too large for V4                    | Use smaller amount                 |

## SECURITY

- `PRIVATE_KEY` must be provided via an environment variable or secret manager only.
- **NEVER** paste or send `PRIVATE_KEY` in chat.
- **NEVER** commit `PRIVATE_KEY` (or `.env` files) to git.
- Treat **stdout/stderr as public logs** (CI, terminals, chat). CI tests ensure the `PRIVATE_KEY` value is never printed.

- **NEVER** pass private keys as CLI arguments (rejected by all scripts)
- Private keys accepted via `PRIVATE_KEY` env var only
- All inputs validated: addresses (format), amounts (BigInt bounds), slippage (0-10000)
- No `eval()`, no `exec()`, no shell commands — pure TypeScript
- BigInt used everywhere for token amounts (no floating point, no overflow)

## Testing

```bash
npm run test:unit      # Unit tests (no network)
npm run test:fork      # Fork tests (needs: anvil --fork-url https://mainnet.base.org)
npm run test:testnet   # Testnet reads (Base Sepolia)
npm run test:mainnet   # Mainnet smoke tests (read-only)
npm run security       # Security scan
```

## References

- V4 encoding reference: `references/v4-encoding.md`
- Contract addresses: `references/addresses.md`
- V4 architecture: `references/v4-architecture.md`
