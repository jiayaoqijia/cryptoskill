# Changelog

All notable changes to the gate-exchange-marketanalysis skill are documented here.

Format: date-based versioning (`YYYY.M.DD`). Same-day releases may use a sequential suffix: `YYYY.M.DD-1`, `YYYY.M.DD-2`, etc.

---

## [2026.3.11-1] - 2026-03-11

### Changed

- **MCP tool names** — Aligned with new Gate MCP interface naming:
  - Spot: `get_spot_*` → `cex_spot_get_spot_*` (e.g. `get_spot_order_book` → `cex_spot_get_spot_order_book`, `get_spot_tickers` → `cex_spot_get_spot_tickers`, `get_spot_candlesticks` → `cex_spot_get_spot_candlesticks`, `get_spot_trades` → `cex_spot_get_spot_trades`).
  - Futures: `get_futures_*` / `list_futures_*` → `cex_fx_*` (e.g. `get_futures_contract` → `cex_fx_get_fx_contract`, `get_futures_order_book` → `cex_fx_get_fx_order_book`, `get_futures_tickers` → `cex_fx_get_fx_tickers`, `get_futures_candlesticks` → `cex_fx_get_fx_candlesticks`, `get_futures_trades` → `cex_fx_get_fx_trades`, `get_futures_funding_rate` → `cex_fx_get_fx_funding_rate`, `list_futures_liq_orders` → `cex_fx_list_fx_liq_orders`, `get_futures_premium_index` → `cex_fx_get_fx_premium_index`).
  - Updated in `SKILL.md`, `references/scenarios.md`, `README.md`, and `CHANGELOG.md`.

---

## [2026.3.7-1] - 2026-03-07

### Scope

- Case 8 adds **slippage simulation**: market-order fill vs order book, slippage reported as deviation from best ask (points and %). Spot and futures supported. **Requires both currency pair and quote amount** from the user; no defaults — when either is missing, prompt the user instead of running the simulation.
- Case 9 adds **K-line breakout / support–resistance** analysis from candlesticks and tickers.
- Case 10 adds **liquidity + weekend vs weekday** comparison using order book, 90d candlesticks, and tickers.

### Added

- **Case 8: Slippage simulation** — market-order slippage vs best ask
  - Trigger: e.g. "slippage simulation", "market buy $10K, how much slippage?", "ADA_USDT slippage simulation"
  - **Spot:** `cex_spot_get_spot_order_book` → `cex_spot_get_spot_tickers`; **Futures:** `cex_fx_get_fx_contract` → `cex_fx_get_fx_order_book` → `cex_fx_get_fx_tickers`
  - Logic: walk ask ladder for quote amount Q; volume-weighted avg price; slippage = avg price − ask1 (points and %)
  - Output: simulation inputs, fill summary, slippage vs best ask, conclusion
- Scenario 8.1: spot slippage simulation (e.g. ADA_USDT / ETH market buy $10K)
- Scenario 8.2: futures slippage simulation (perpetual/contract market long)
- Scenario 8.3: missing pair or amount — prompt user (do not call MCP; ask for pair and/or quote amount; do not default to $10K)
- **Case 9: K-line breakout / support–resistance** — analyze breakout and support/resistance from recent K-line
  - Trigger: e.g. "Based on recent K-line, does SOL/USDT show signs of breaking out upward? Analyze support and resistance."
  - **Spot:** `cex_spot_get_spot_candlesticks` → `cex_spot_get_spot_tickers`; **Futures:** `cex_fx_get_fx_candlesticks` → `cex_fx_get_fx_tickers`
  - Logic: historical candlesticks for support/resistance; 24h price, volume, change for momentum and breakout signs
  - Output: K-line context, support & resistance table, momentum (24h), breakout assessment
- **Case 10: Liquidity + weekend vs weekday** — evaluate liquidity and compare weekend vs weekday
  - Trigger: e.g. "Evaluate ETH liquidity on the exchange and compare weekend vs weekday."
  - **Spot:** `cex_spot_get_spot_order_book` → `cex_spot_get_spot_candlesticks`(90d) → `cex_spot_get_spot_tickers`; **Futures:** `cex_fx_get_fx_contract` → `cex_fx_get_fx_order_book` → `cex_fx_get_fx_candlesticks`(90d) → `cex_fx_get_fx_tickers`
  - Logic: order book for current depth; 90d candlesticks split by weekend vs weekday for volume and return; compare and summarize
  - Output: current liquidity, 90-day weekend vs weekday table, comparison, conclusion

### Changed

- **MCP tool names** — Corrected to match Gate MCP: `list_futures_funding_rate` → `get_futures_funding_rate`; `list_futures_premium_index` → `get_futures_premium_index`. Updated in `references/scenarios.md` and README.md. (`list_futures_liq_orders` is correct per MCP.)
- **Pure English** — all trigger phrases and report templates in SKILL.md and `references/scenarios.md` are in English.
- **Versioning** — version and `updated` follow current date (`YYYY.M.DD`).
- **Case 8 required inputs** — currency pair and quote amount both required; if either missing, prompt user (no default pair, no default amount e.g. $10K). SKILL.md Execution step 3 and Domain Knowledge (Case 8) updated accordingly.

### Audit

- Case 8 uses Gate MCP only (cex_spot_get_spot_order_book / cex_fx_get_fx_order_book, cex_spot_get_spot_tickers / cex_fx_get_fx_tickers).
- No MCP calls when pair or amount is missing; user is prompted first.
- All analysis is read-only; no trading operations.

---

## [2026.3.5-1] - 2026-03-05

### Scope

This skill supports **market tape analysis only** (read-only): liquidity, momentum, liquidation, funding arbitrage, basis, manipulation risk, order book explainer. No trading operations.

### Added
- Initial release (market tape analysis, seven scenarios)
- Routing-based SKILL.md with document loading from `references/scenarios.md`
- **Seven analysis modules:** Liquidity, Momentum, Liquidation monitoring, Funding arbitrage, Basis, Manipulation risk, Order book explainer
- Smart spot/futures market detection (perpetual/contract keywords)
- MCP call order and Report Template defined in `references/scenarios.md`
- Domain knowledge and safety rules

### Audit

- Uses Gate MCP tools only; all analysis is read-only
- No trading operations or credential handling in this skill

