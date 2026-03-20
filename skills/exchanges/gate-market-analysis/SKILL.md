---
name: gate-exchange-marketanalysis
version: "2026.3.11-1"
updated: "2026-03-11"
description: "The market analysis function of Gate Exchange, such as liquidity, momentum, liquidation, funding arbitrage, basis, manipulation risk, order book explainer, slippage simulation. Use when the user asks about liquidity, depth, slippage, buy/sell pressure, liquidation, funding rate arbitrage, basis/premium, manipulation risk, order book explanation, or slippage simulation (e.g. market buy $X slippage). Trigger phrases: liquidity, depth, slippage, momentum, buy/sell pressure, liquidation, squeeze, funding rate, arbitrage, basis, premium, manipulation, order book, spread, slippage simulation."
---

# gate-exchange-marketanalysis

Market tape analysis covering thirteen scenarios, such as liquidity, momentum, liquidation monitoring, funding arbitrage, basis monitoring, manipulation risk, order book explanation, slippage simulation, K-line breakout/support–resistance, and liquidity with weekend vs weekday. This skill provides structured market insights by orchestrating Gate MCP tools; call order and judgment logic are defined in `references/scenarios.md`.

---

## Sub-Modules

| Module | Purpose | Document |
|--------|---------|----------|
| **Liquidity** | Order book depth, 24h vs 30d volume, slippage | `references/scenarios.md` (Case 1) |
| **Momentum** | Buy vs sell share, funding rate | `references/scenarios.md` (Case 2) |
| **Liquidation** | 1h liq vs baseline, squeeze, wicks | `references/scenarios.md` (Case 3) |
| **Funding arbitrage** | Rate + volume screen, spot–futures spread | `references/scenarios.md` (Case 4) |
| **Basis** | Spot–futures price, premium index | `references/scenarios.md` (Case 5) |
| **Manipulation risk** | Depth/volume ratio, large orders | `references/scenarios.md` (Case 6) |
| **Order book explainer** | Bids/asks, spread, depth | `references/scenarios.md` (Case 7) |
| **Slippage simulation** | Market-order slippage vs best ask | `references/scenarios.md` (Case 8) |
| **K-line breakout / support–resistance** | Candlesticks + tickers; support/resistance; breakout momentum | `references/scenarios.md` (Case 9) |
| **Liquidity + weekend vs weekday** | Order book + 90d candlesticks + tickers; weekend vs weekday volume/return | `references/scenarios.md` (Case 10) |
| **Technical analysis / what to do** | Short + long timeframe K-line, support/resistance, momentum (price vs volume), funding rate; spot + futures; separate short/long-term advice | `references/scenarios.md` (Case 11) |
| **Multi-asset buy & allocation** | Per-asset ticker + order book + 7d daily candles; futures add funding rate; allocation % and rationale | `references/scenarios.md` (Case 12) |
| **Portfolio allocation review** | Same data as Case 12; assess if allocation is reasonable, adjustment advice, what else to buy if no change | `references/scenarios.md` (Case 13) |

---

## Routing Rules

Determine which module (case) to run based on user intent:

| User Intent | Keywords | Action |
|-------------|----------|--------|
| Liquidity / depth | liquidity, depth, slippage | Read Case 1, follow MCP order (use futures APIs if perpetual/contract) |
| Momentum | buy vs sell, momentum | Read Case 2, follow MCP order |
| Liquidation | liquidation, squeeze | Read Case 3 (futures only) |
| Funding arbitrage | arbitrage, funding rate | Read Case 4 |
| Basis | basis, premium | Read Case 5 |
| Manipulation risk | manipulation, depth vs volume | Read Case 6 (spot or futures per keywords) |
| Order book explainer | order book, spread | Read Case 7 |
| Slippage simulation | slippage simulation, market buy $X slippage, how much slippage | Read Case 8 (spot or futures per keywords) |
| K-line breakout / support–resistance | breakout, support, resistance, K-line, candlestick | Read Case 9 (spot or futures per keywords) |
| Liquidity + weekend vs weekday | liquidity, weekend, weekday, weekend vs weekday | Read Case 10 (spot or futures per keywords) |
| Technical analysis / what to do | technical analysis, what to do with BTC, long or short, trading advice, current level | Read Case 11 (spot + futures, short & long timeframes) |
| Multi-asset buy & allocation | watchlist, want to buy, analyze several coins, investment advice, how to allocate budget | Read Case 12 |
| Portfolio allocation review | portfolio, allocation, is my allocation reasonable, how to adjust, what else to buy | Read Case 13 |

---

## Execution

1. **Match user intent** to the routing table above and determine case (1–13) and market type (spot/futures).
2. **Read** the corresponding case in `references/scenarios.md` for MCP call order and required fields.
3. **Case 8 only:** If the user did **not** specify a **currency pair** or did **not** specify a **quote amount** (e.g. $10K), do not assume defaults — **prompt the user** to provide the missing input(s); see Scenario 8.3 in `references/scenarios.md`.
4. **Call Gate MCP** in the exact order defined for that case.
5. **Apply judgment logic** from scenarios (thresholds, flags, ratings).
6. **Output the report** using that case’s Report Template.
7. **Suggest related actions** (e.g. “For basis, ask ‘What is the basis for XXX?’”).

---

## Domain Knowledge (short)

- **Spot vs futures:** Keywords “perpetual”, “contract”, “future”, “perp” → use futures MCP APIs; “spot” or unspecified → spot.
- **Liquidity (Case 1):** Depth &lt; 10 levels → low liquidity; 24h volume &lt; 30-day avg → cold pair; slippage = 2×(ask1−bid1)/(bid1+ask1) &gt; 0.5% → high slippage risk.
- **Momentum (Case 2):** Buy share &gt; 70% → buy-side strong; 24h volume &gt; 30-day avg → active; funding rate sign + order book top 10 for bias.
- **Liquidation (Case 3):** 1h liq &gt; 3× daily avg → anomaly; one-sided liq &gt; 80% → long/short squeeze; price recovered → wick/spike.
- **Arbitrage (Case 4):** |rate| &gt; 0.05% and 24h vol &gt; $10M → candidate; spot–futures spread &gt; 0.2% → bonus; thin depth → exclude.
- **Basis (Case 5):** Current basis vs history; basis widening/narrowing for sentiment.
- **Manipulation (Case 6):** Top-10 depth total / 24h volume &lt; 0.5% → thin depth; consecutive same-direction large orders → possible manipulation. Use spot by default; use futures when user says perpetual/contract.
- **Order book (Case 7):** Show bids/asks example, explain spread with last price, depth and volatility.
- **Slippage simulation (Case 8):** **Requires both a currency pair and a quote amount** (e.g. ETH_USDT, $10K). If user does not specify either, prompt them — do not assume defaults (e.g. do not default to $10K). Spot: cex_spot_get_spot_order_book → cex_spot_get_spot_tickers. Futures: cex_fx_get_fx_contract → cex_fx_get_fx_order_book → cex_fx_get_fx_tickers (use quanto_multiplier from contract for ladder notional). Simulate market buy by walking ask ladder; slippage = volume-weighted avg price − ask1 (points and %).
- **K-line breakout / support–resistance (Case 9):** Trigger: e.g. “breakout, support, resistance”, “K-line”, “does X show signs of breaking out?”. Spot: cex_spot_get_spot_candlesticks → cex_spot_get_spot_tickers. Futures: cex_fx_get_fx_candlesticks → cex_fx_get_fx_tickers. Use candlesticks for support/resistance levels; use tickers for 24h price, volume, change (momentum).
- **Liquidity + weekend vs weekday (Case 10):** Trigger: e.g. “liquidity”, “weekend vs weekday”, “compare weekend and weekday”. Spot: cex_spot_get_spot_order_book → cex_spot_get_spot_candlesticks(90d) → cex_spot_get_spot_tickers. Futures: cex_fx_get_fx_contract → cex_fx_get_fx_order_book → cex_fx_get_fx_candlesticks(90d) → cex_fx_get_fx_tickers (use quanto_multiplier for depth notional). Order book for current depth; 90d candlesticks to split weekend vs weekday volume and return; compare and summarize.
- **Technical analysis / what to do (Case 11):** Trigger: e.g. "technical analysis, what should I do with BTC", "long or short at current level". Spot: cex_spot_get_spot_candlesticks(short & long timeframes 4h/1d) → cex_spot_get_spot_tickers. Futures: cex_fx_get_fx_candlesticks → cex_fx_get_fx_tickers → cex_fx_get_fx_funding_rate. Use history for support/resistance; compare current price and 24h volume to past for momentum; funding rate for long/short bias; give separate short- and long-term advice.
- **Multi-asset buy & allocation (Case 12):** Trigger: e.g. "I'm watching BTC, ETH, GT and want to buy; analyze and give allocation for $5000". Per asset: cex_spot_get_spot_candlesticks(7d) → cex_spot_get_spot_tickers → cex_spot_get_spot_order_book; futures: cex_fx_get_fx_candlesticks → cex_fx_get_fx_tickers → cex_fx_get_fx_order_book → cex_fx_get_fx_funding_rate. Spot ticker + order book + 7d daily; add funding for futures; output allocation % and rationale.
- **Portfolio allocation review (Case 13):** Trigger: e.g. "I hold 30% BTC, 30% ETH, 20% DOGE, 15% LTC, 5% USDT; is this allocation reasonable, how to adjust, what else to buy?". Same MCP order as Case 12 (per-asset spot candlesticks + tickers + order_book; futures + funding_rate). Assess allocation, suggest adjustments, or suggest what else to buy if no change.

---

## Important Notes

- All analysis is read-only — no trading operations are performed.
- Gate MCP must be configured (use `gate-mcp-installer` skill if needed).
- MCP call order and output format are in `references/scenarios.md`; follow them for consistent behavior.
- Always include a disclaimer: analysis is data-based, not investment advice.
