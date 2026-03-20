# Changelog — gate-news-briefing

**Note:** Changes are consolidated as one initial entry for now; versioned entries will be used after official release.

---

## [2026.3.12-1] - 2026-03-12

### Added

- Skill: News briefing. Trigger: "What happened recently", "Today's hot topics". MCP tools (order): news_feed_search_news, news_feed_get_social_sentiment, news_events_get_latest_events (3 in parallel).
- SKILL.md: Routing, 3-tool parallel table, 3-section Report Template (strong constraint), Decision Logic, Error Handling, Cross-Skill, Safety. Aligned with docs/SKILL_SPEC_TABLE.md, docs/PD_VS_SKILLS_OPTIMIZATION_SUMMARY.md.
- README.md, references/scenarios.md.

### Audit

- Read-only; no trading or order execution.
