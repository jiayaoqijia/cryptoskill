# Agent Prompt Test Cases (English)

Manual test prompts for OpenOcean skills. Use these as user messages to verify that the correct skill is triggered and behavior matches expectations.

---

## Quote

**Expected skill:** `quote` — fetch best swap route and price from OpenOcean Aggregator.

| # | User prompt | Notes |
|---|-------------|--------|
| 1 | Get a swap quote for 1 ETH to USDC on ethereum | Standard quote |
| 2 | Check swap price: 100 USDC to WBTC on arbitrum | Price check phrasing |
| 3 | How much would I get for 0.5 WBTC to DAI on polygon? | Question form |
| 4 | Compare token rates — 1000 USDT to ETH | Default chain (ethereum) |
| 5 | See exchange rates for 10 ETH to USDC on base | Alternative phrasing |
| 6 | Price check: 50 USDC to ETH on optimism | Short form |

---

## Swap build

**Expected skill:** `swap-build` — build full swap transaction with calldata; show quote and ask for confirmation before building.

| # | User prompt | Notes |
|---|-------------|--------|
| 1 | Build a swap: 100 USDC to ETH on arbitrum from 0x742d35Cc6634C0532925a3b844Bc9e90F1b6fB28 | With sender |
| 2 | Prepare swap transaction — 1 ETH to USDC on ethereum from 0xYourAddress | Prepare phrasing |
| 3 | Get swap calldata for 0.5 WBTC to DAI on polygon from 0xYourAddress | Calldata focus |
| 4 | I want to create a transaction to swap 200 USDC to ETH on base from 0xYourAddress slippage 2 | With slippage |

---

## Swap execute

**Expected skill:** `swap-execute` — execute a previously built swap using Foundry cast; ask for confirmation before broadcasting.

| # | User prompt | Notes |
|---|-------------|--------|
| 1 | Execute the swap | After swap-build |
| 2 | Broadcast the swap transaction | Alternative |
| 3 | Send the transaction | Short form |

---

## Swap execute fast

**Expected skill:** `swap-execute-fast` — build and execute in one step, no confirmation. Use with caution.

| # | User prompt | Notes |
|---|-------------|--------|
| 1 | Swap fast: 1 ETH to USDC on base from 0xYourAddress | One-step |
| 2 | Execute swap immediately — 100 USDC to ETH on arbitrum from 0xYourAddress | Immediate |
| 3 | Automated swap: 0.5 WBTC to DAI on polygon from 0xYourAddress | Automated |

---

## Error handling

**Expected skill:** `error-handling` — when API returns an error, token resolution fails, or execution fails.

| # | User prompt / scenario | Notes |
|---|------------------------|--------|
| 1 | (After a failed quote) What does code 429 mean? | Rate limit |
| 2 | (After swap-build fails) Token resolution failed for XYZ | Troubleshooting |
| 3 | Transaction reverted — what should I do? | Execution failure |

---

## Negative / out-of-scope

These should **not** trigger swap/quote skills (or should trigger error-handling / clarification):

| # | User prompt | Expected behavior |
|---|-------------|-------------------|
| 1 | What is OpenOcean? | Informational, no swap API call |
| 2 | Swap 1 ETH to USDC on ethereum | Missing sender for build/execute; quote is OK |
| 3 | Execute swap (no prior build) | Should ask for prior swap-build output or decline |

---

*Run these prompts in an agent session and confirm the right skill runs and output format matches the skill docs.*
