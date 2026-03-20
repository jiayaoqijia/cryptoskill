# Changelog

## [2026.3.14-3] - 2026-03-14

### Changed

- Tightened the skill's analysis-side mappings to reflect real runtime payload quality, not just tool-name availability.
- Reworked single-coin, event, and new-listing scenarios so they rely primarily on tools that return analyzable outputs in the current runtime.
- Downgraded `info_marketsnapshot_get_market_snapshot` to supplementary context when its payload is sparse.
- Replaced default coin-level `news_feed_get_social_sentiment` usage with `news_feed_search_news(platform_type=\"social_ugc\")` for generic social context.
- Added explicit chain/address resolution requirements before `info_compliance_check_token_security`.
- Documented that `info_markettrend_get_indicator_history` may require array-form `indicators`.

## [2026.3.14-2] - 2026-03-14

### Changed

- Rebased the skill's portable baseline on the documented Gate MCP surfaces from the official repo:
  - `info_*` -> Gate Info MCP
  - `news_feed_*` -> Gate News MCP
  - read-only `cex_spot_*` / `cex_fx_*` market data -> Gate public market MCP or local combined Gate MCP
  - private `cex_*` trading/account tools -> authenticated Gate Exchange MCP or local authenticated Gate MCP
- Removed `news_events_*` as a required dependency from baseline scenarios and routing rules, so the skill stays portable across documented runtimes.
- Updated scenario call patterns to use the documented news/feed and info tools with more portable example parameters.
- Added `references/runtime-dependencies.md` so runtime requirements are now explicit inside the skill package.
- Fixed `info_marketsnapshot_get_market_snapshot` scenario examples to include the required `timeframe` and `source` parameters.

## [2026.3.14-1] - 2026-03-14

### Changed

- Normalized `references/scenarios.md` prompt examples to English-only wording for release consistency.
- Replaced relative Markdown links in `SKILL.md` and `README.md` with plain file-path references to reduce renderer and packaging ambiguity.
- Aligned analysis-tool references with the currently exposed Gate MCP tool surface:
  - replaced stale `info_marketsnapshot_get_market_overview` references with `info_marketsnapshot_get_market_snapshot`
  - removed stale `info_coin_get_coin_rankings` and `info_macro_get_macro_summary` assumptions
  - replaced stale `info_onchain_trace_fund_flow` references with available tx-level on-chain tools
- Added explicit fallback guidance for runtime tool-name drift so the skill degrades honestly instead of overclaiming unavailable analysis depth.

## [2026.3.13-1] - 2026-03-13

### Added

- Added the first public release of `gate-exchange-trading-copilot`.
- Included the formal skill package:
  - `SKILL.md`
  - `README.md`
  - `CHANGELOG.md`
  - `references/scenarios.md`
  - `references/routing-and-analysis.md`
  - `references/execution-and-guardrails.md`
- Included shared runtime-rule referencing through `../exchange-runtime-rules.md`.
- Included the end-to-end closed loop for cryptocurrency trading on Gate Exchange:
  - trade judgment
  - risk control
  - order draft generation
  - explicit confirmation
  - execution
  - post-trade management

### Audit

- ✅ The public changelog reflects the first release only.
- ✅ No credentials, private paths, or unpublished internal wording are exposed in the formal release files.
- ✅ The public release aligns on Gate Exchange cryptocurrency scope and explicit-confirmation execution rules.
