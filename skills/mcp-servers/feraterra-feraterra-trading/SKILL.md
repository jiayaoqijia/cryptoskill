---
name: feraterra-trading
description: Guides autonomous AI agents and developers in discovering CLOB markets, previewing stateless cross-margin orders, quoting with oracle mark pegs, executing authenticated HMAC-SHA256 orders, and verifying cryptographic WAL ledger tips on FeraTerra via MCP (feraterra-mcp v4.9.5), Node.js/TypeScript ESM SDK, Python SDK, or C++23/Rust HFT wire. Use when trading, market-making, calling FeraTerra MCP tools, or building quantitative bots against feraterra.app.
---

# FeraTerra Sovereign CLOB Trading & Quantitative SDK Skill (`v4.9.5`)

Use this skill when interacting with **FeraTerra** (`https://feraterra.app`, public Base Sepolia testnet `https://testnet.feraterra.app`, remote MCP gateway `https://mcp.feraterra.app/mcp`), running the zero-dependency Node.js MCP gateway & ESM SDK (`feraterra-mcp` `v4.9.5`), writing Python bots (`import feraterra_sdk`), or integrating the 64-byte HFT binary wire (`feraterra-wire` / `feraterra::hft_client`).

## 1. Fixed-Point Scales (Zero Floating-Point Drift)

All engine prices, quantities, and collateral balances use deterministic 64-bit integer fixed-point arithmetic:

| Quantity | Integer Unit | Scale Factor | Example Conversion | Node.js ESM (`feraterra-mcp`) | Python (`feraterra_sdk`) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Price** | `1 tick = $0.01` | `100` ticks / `$1.00` | `$70,000.25` = `7_000_025` ticks | `usdToTicks("70000.25")`, `ticksToUsd(ticks)` | `usd_to_price_ticks("70000.25")`, `price_ticks_to_usd_str(ticks)` |
| **Order / Position Size** | `1 lot = 1e-4` base | `10_000` lots / `1.0` base | `0.2500 BTC` = `2_500` lots | `baseToLots("0.2500")`, `lotsToBase(lots)` | `base_to_qty_lots("0.2500")`, `qty_lots_to_base_str(lots)` |
| **USD Collateral / PnL** | `1 micro = $1e-6` | `1_000_000` micro / `$1.00` | `$10,000.00` = `10_000_000_000` micro | `usdToMicro("10000.00")`, `microToUsd(micro)` | `usd_to_micro("10000.00")`, `micro_to_usd_str(micro)` |

MCP tools accept human-readable decimal strings/numbers (`price_usd`, `amount_base`) **or** exact integer units (`price_ticks`, `qty_lots`). Call `feraterra_convert_units` offline whenever you want to double-check exact fixed-point integer representations before submitting orders.

## 2. MCP Connectivity Modes (`feraterra-mcp` `v4.9.5`)

### Mode A — Local Zero-Dependency Node.js `stdio` REST Server (Default)
Runs a local `stdio` MCP server (`2025-11-25` / `2025-06-18`) directly against the FeraTerra REST gateway with client-side `Keccak-256` + `secp256k1` solvency verification and local `X-Arena-*` HMAC-SHA256 signing (credentials never leave your machine):

```json
{
  "mcpServers": {
    "feraterra": {
      "command": "npx",
      "args": ["-y", "feraterra-mcp"],
      "env": {
        "FERATERRA_API_URL": "https://testnet.feraterra.app"
      }
    }
  }
}
```

- Pass `--read-only` (or `FERATERRA_READ_ONLY=true`) to hard-disable mutating tools and mutating prompts.
- Add `FERATERRA_ACCOUNT_ID`, `FERATERRA_API_KEY`, and `FERATERRA_API_SECRET` only when enabling authenticated portfolio inspection (`feraterra_get_account`) and order execution.

### Mode B — Streamable HTTP Proxy (`--remote`) or Direct Remote Gateway
Bridge `stdio`-only MCP hosts (`JSONL` or `Content-Length`) to the hosted Streamable HTTP MCP gateway (`https://mcp.feraterra.app/mcp`) with optional `FERATERRA_BEARER_TOKEN` forwarding:

```json
{
  "mcpServers": {
    "feraterra-remote": {
      "command": "npx",
      "args": ["-y", "feraterra-mcp", "--remote"],
      "env": {
        "FERATERRA_MCP_URL": "https://mcp.feraterra.app/mcp"
      }
    }
  }
}
```

Native Streamable HTTP clients can also connect directly to `https://mcp.feraterra.app/mcp` without a local process.

## 3. Safe Agent Execution Workflow

### Step 1: Inspect Health, Manifest, Terms & Live Markets
1. Call `feraterra_health_and_manifest` (`include_terms: true`) to inspect `GET /health`, `GET /`, and `GET /terms` (`wal_seq`, `conservation_ok`, `chain_id`, `clearinghouse_address` for the L2 collateral vault, and headless protocol disclosures).
2. Call `feraterra_list_markets` (`kind: "perp"` or `""` for all `LinearPerpetual`, `FormulaPerpetual`, `Spot`, `BoundedClaim`, and `SpreadBook` instruments) and `feraterra_get_orderbook` (`depth: 20`) to inspect BBO spreads and resting liquidity.

### Step 2: Always Dry-Run First with Stateless `feraterra_preview_order`
Before placing any live order, simulate execution via `feraterra_preview_order` (alias `arena_preview_order`, `POST /order/preview`). It performs **zero WAL, L3 order book, or balance mutation**:

- **Zero-Key Stateless Mode (`account_id: 0` or omitted when unauthenticated):** Simulates immediate L3 fills, effective price, resting remainder, net maker/taker fee or rebate, and standalone Eigen-SPAN `IMR` / `MMR` impact with **zero API keys**.
- **Authenticated Portfolio Mode (`account_id >= 1`):** Computes exact pre-trade and post-trade cross-margin requirements (`pre_imr_usd`, `post_imr_usd`, `imr_delta_usd`, `post_free_margin_usd`) against your live positions.

```json
{
  "name": "feraterra_preview_order",
  "arguments": {
    "account_id": 0,
    "symbol": "BTC-USD-PERP",
    "side": "buy",
    "price_usd": "70000.00",
    "amount_base": "0.0500",
    "tif": "post_only"
  }
}
```

### Step 3: Execute Bounded Single-Leg Orders or Two-Sided Maker Quotes
Only after confirming `would_accept === true` and `imr_delta_usd` within risk limits:
- Use `feraterra_place_order` (`POST /order`) for directional or single-leg `gtc` / `ioc` / `fok` / `post_only` orders (set `reduce_only: true` when closing exposure).
- Use `feraterra_replace_quote` (`POST /quote`, default `tif: "post_only"`) to atomically cancel and replace both Bid and Ask maker quotes in a single WAL step.
- Use `feraterra_cancel_order` (`POST /cancel`) or `feraterra_cancel_all_orders` (`POST /cancel_all`) to pull resting liquidity.

## 4. Critical Pegging Rule: `mark_peg: true` vs. `quote_peg_mode: 3`

Single-leg order placement and atomic two-sided quote replacement encode oracle mark pegging differently:

1. **Single-Leg Orders (`POST /order`, `POST /order/preview`, `FeraTerraClient.placeOrder`):**
   Use boolean peg flags (`primary_peg`, `midpoint_peg`, **`mark_peg: true`**, `trailing_peg`, `dark_midpoint`) plus optional signed `peg_offset_ticks` (`-500..+500`).
2. **Atomic Two-Sided Quotes (`POST /quote`, `FeraTerraClient.replaceQuote`):**
   Pass integer **`quote_peg_mode`** (`0..4`) instead of a boolean `mark_peg` flag:
   - `0` — Unpegged static limit prices (supports inventory `auto_skew_ticks` or `auto_flip_ticks`)
   - `1` — Primary peg (same-side BBO)
   - `2` — Midpoint peg (BBO mid)
   - **`3` — Oracle Mark Peg** (re-anchors both Bid and Ask to live oracle mark moves natively in the engine)
   - `4` — One-way ratchet trailing peg

## 5. Cryptographic Solvency Verification (`ARENA_LEDGER_TIP_V2_1`)

Every deterministic engine transition advances a hash-chained WAL (`wal_seq`, `ledger_chain_hash`, `state_root`) signed by the operator over the **`ARENA_LEDGER_TIP_V2_1`** `Keccak-256` domain (`GET /ledger/tip`) and bound to `chain_id` and the L2 collateral vault address (`clearinghouse_address`).

- **MCP Verification:** Call `feraterra_verify_ledger_tip` (pass `expected_operator_address` from out-of-band operator configuration or `GET /` / `GET /status` -> `operator_eth_address` to pin the expected `secp256k1` signer, plus optional `expected_chain_id` and `expected_clearinghouse_address`).
- **Node.js ESM SDK Verification (`import { FeraTerraClient, verifyLedgerTip } from "feraterra-mcp"`):**
  ```js
  import { FeraTerraClient } from "feraterra-mcp";

  const client = new FeraTerraClient({
    baseUrl: "https://testnet.feraterra.app",
    expectedOperatorAddress: process.env.FERATERRA_EXPECTED_OPERATOR,
  });
  const solvency = await client.verifySolvency({ includeHealth: true });
  if (!solvency.solvent) {
    throw new Error(`Ledger tip verification failed: ${solvency.reason ?? "insolvent"}`);
  }
  ```
- **Non-Custodial L2 Escape Disclosures:** Read MCP resource `feraterra://protocol/terms` (`GET /terms`) to inspect headless protocol disclosures and L2 collateral vault Merkle emergency escape guarantees.

## 6. Offline Portable Skill Installer (`install-skill`)

Install this bundled `SKILL.md` (`v4.9.5`) offline into your agent workspace with zero network requests:

```bash
# Default (.agents/skills/feraterra-trading/SKILL.md)
npx -y feraterra-mcp install-skill

# Agent-specific skill directories (--claude, --cursor, --codex) and custom workspace (--dir)
npx -y feraterra-mcp install-skill --claude --cursor --codex --dir ./my-trading-bot
```
