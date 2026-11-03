---
name: spectra-yields
description: Find, compare and explain Spectra fixed-rate yields, liquidity pools and MetaVaults across chains, and read a wallet's Spectra positions. Use when the user asks about fixed rates, Principal Tokens (PT), Yield Tokens (YT), "best yield on USDC/ETH/XRP", stablecoin yields, Spectra markets or MetaVaults, or what they hold on Spectra.
---

# Spectra yields

Spectra splits interest-bearing tokens into a **Principal Token (PT)**, which redeems 1:1 for the underlying at maturity (so buying it at a discount locks a fixed rate), and a **Yield Token (YT)**, which collects the variable yield until maturity. PT/IBT pools pay LPs; **MetaVaults** are curated vaults that allocate across pools and roll maturities.

## Get the data (in order of preference)

1. **Spectra MCP tools**, if connected: `spectra_find_yields`, `spectra_get_market`, `spectra_get_market_history`, `spectra_get_metavault`, `spectra_get_portfolio`, `spectra_protocol_info`. The server is `https://mcp.spectra.finance/mcp` (no account or key).
2. **REST API** directly, see [references/api.md](references/api.md).

## Workflow for "where should I earn yield on X?"

1. `spectra_find_yields` with `asset` (and `chain` / `product` if the user said so). Default ranking is by APY and hides thin or anomalous markets.
2. For the top 2–3 candidates call `spectra_get_market` (or `spectra_get_metavault`) to check liquidity, maturity, the APY breakdown and flags.
3. If the user names an amount and `spectra_prepare_pt_trade` is available (the trade endpoint), quote it without a receiver (quote only): the fixed APY for size can be lower than the headline rate. Without that tool, say so and link the market in the app.
4. Answer with a compact table: product, asset, network, APY (fixed or variable), maturity, liquidity, link. State the `as_of` time.

## How to present numbers

- APYs are **percent** (4.8 = 4.8%). Say which kind: *fixed* (PT held to maturity), *variable* (LP, vault, underlying), *implied* (market-priced).
- A fixed rate is only fixed if the PT is **held to maturity**; selling early realises the market price.
- Always include the app link from the result so the user can verify, and the timestamp.
- Surface flags in plain words: `low_liquidity` → price impact on size; `near_maturity` → little time left; `apy_outlier` → data looks wrong, do not recommend; `expired` → redeem, do not buy.
- Mention the main risks briefly (smart contract, underlying protocol, liquidity, curator for MetaVaults). Never call returns guaranteed; this is information, not financial advice.
- Tokenized-equity markets are not offered to persons in the US, UK, Canada, Australia or Singapore; the tools hide them.

## Comparing with variable rates

Fixed APY vs the market's `variable_apy_pct` tells the user what the market expects: fixed above variable means they lock in more than the current floating yield (as long as it stays below). Use `spectra_get_market_history` (implied APY) to show the trend.

## Portfolio questions

`spectra_get_portfolio` returns PT, YT (with claimable yield) and LP positions with USD values and suggested actions. Highlight matured PTs to redeem, claimable YT yield and positions maturing soon. For any action, hand off to the `spectra-transactions` skill if it is installed; otherwise give the app link from the result.

See [references/concepts.md](references/concepts.md) for definitions and edge cases.
