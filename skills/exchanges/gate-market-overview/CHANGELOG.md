# Changelog — gate-info-marketoverview

**Note:** Changes are consolidated as one initial entry for now; versioned entries will be used after official release.

---

## [2026.3.12-1] - 2026-03-12

### Added

- Skill: Market overview. Trigger: market-wide questions (e.g. "How is the market now"). Tools: info_marketsnapshot_get_market_overview (or get_market_snapshot fallback), info_coin_get_coin_rankings, info_platformmetrics_get_defi_overview, news_events_get_latest_events, info_macro_get_macro_summary. Tool count: 5.
- SKILL.md: Routing, 5-tool parallel table, 6-section Report Template, Decision Logic, Error Handling, Cross-Skill, Safety. Aligned with docs/pd-vs-skills, docs/PD_VS_SKILLS_OPTIMIZATION_SUMMARY.md.
- README.md, references/scenarios.md.

### Audit

- Read-only; no trading or order execution.
