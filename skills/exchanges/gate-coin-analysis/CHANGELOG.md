# Changelog — gate-info-coinanalysis

**Note:** Changes are consolidated as one initial entry for now; versioned entries will be used after official release.

---

## [2026.3.12-2] - 2026-03-11 — Initialization

### Added

- **Skill**: Coin comprehensive analysis. Trigger: single-coin analysis (e.g. "Analyze SOL", "How is BTC"). Tools: `info_coin_get_coin_info`, `info_marketsnapshot_get_market_snapshot`, `info_markettrend_get_technical_analysis`, `news_feed_search_news`, `news_feed_get_social_sentiment` (optional when no news MCP). Tool count: 5.
- **SKILL.md**: Workflow (5 tools in parallel + LLM aggregation), Decision Logic (RSI / volume / funding / fear_greed / unlock), Report Template (5 sections), Routing, Error Handling, Cross-Skill, Safety. Aligned with `docs/pd-vs-skills` and `docs/PD_VS_SKILLS_OPTIMIZATION_SUMMARY.md`.
- **README.md**, **references/scenarios.md**.

### Changed

- **info_marketsnapshot_get_market_snapshot**: Parameters use `timeframe="1d"` and `source="spot"` (aligned with PD; same as gate-info-coincompare and gate-news-listing).

### Audit

- Read-only; no trading or order execution.
