# Changelog

## 2026.3.12-3 (2026-03-12)

- Translated all Chinese content to English in scenarios.md, SKILL.md, and CHANGELOG.md.

## 2026.3.12-2 (2026-03-12)

- Removed deposit history and withdrawal history from skill scope.
- Removed `cex_wallet_list_deposits` and `cex_wallet_list_withdrawals` from MCP tool mapping.
- Removed Scenario 8 (Deposit History) and Scenario 9 (Withdrawal History) from scenarios.

## 2026.3.12-1 (2026-03-12)

- Replaced REST API endpoints with Gate gate-mcp tool names: `cex_wallet_get_total_balance`, `cex_spot_get_spot_accounts`, `cex_unified_get_unified_accounts`, `cex_fx_get_fx_accounts`, `cex_delivery_list_delivery_accounts`, `cex_options_list_options_account`, `cex_margin_list_margin_accounts`, `cex_tradfi_query_user_assets`, `cex_earn_list_dual_balance`/`cex_earn_list_dual_orders`/`cex_earn_list_structured_orders`, `cex_spot_list_spot_account_book`.
- Added comprehensive cases from asset query skills (external) PDF specification.
- **Case 1**: Total asset query (GET /wallet/total_balance) with account/coin distribution, TradFi/payment isolation.
- **Case 2**: Specific currency query (concurrent multi-account aggregation).
- **Case 3**: Specific account + currency query (spot/unified).
- **Case 4**: Spot account query.
- **Case 5**: Futures account query (USDT/BTC perpetual, delivery, unified handling).
- **Case 6**: Trading account (unified) query with margin_mode branching.
- **Case 7**: Options account query.
- **Case 8**: Finance account query.
- **Case 9**: Alpha account query.
- **Case 12**: Isolated margin account query.
- **Case 15**: TradFi account query (USDx, isolated display).
- Added API mapping table, account name mapping, output templates.
- Added special scenario handling (small assets, unified migration, dust, TradFi, ST/delisted tokens).
- Added acceptance test queries for validation.
- Added recommendation engine (P1–P4) and transfer path restrictions.
- Expanded `references/scenarios.md` with full scenario templates and edge cases.

## 2026.3.11-1 (2026-03-11)

- Initialized the `gate-exchange-assets` skill directory and documentation structure.
- Added `SKILL.md`, covering 9 read-only asset and balance query scenarios.
- Added `references/scenarios.md`, with per-case examples for inputs, API calls, and decision logic.
- Read-only skill: total balance, spot balance, account valuation, account book.
