# Changelog — gate-info-trendanalysis

**Note:** Changes are consolidated as one initial entry for now; versioned entries will be used after official release.

---

## [2026.3.12-1] - 2026-03-12

### Added

- Skill: Trend / technical analysis. Trigger: technical/trend analysis (e.g. "Technical analysis for BTC"). Tools: info_markettrend_get_kline, info_markettrend_get_indicator_history, info_markettrend_get_technical_analysis, info_marketsnapshot_get_market_snapshot. Tool count: 4.
- SKILL.md: Routing, 4-tool parallel table, parameter extraction, Judgment Logic (Bollinger/volume/divergence/funding), 7-section Report Template, Error Handling, Cross-Skill, Safety. Aligned with docs/pd-vs-skills, docs/PD_VS_SKILLS_OPTIMIZATION_SUMMARY.md.
- README.md, references/scenarios.md.

### Audit

- Read-only; no trading or order execution.
