# Changelog

**Note:** Changes are consolidated as one initial entry for now; versioned entries will be used after official release.

---

## [2026.4.3-1] - 2026-04-03

### Changed

- Added `.clawhubignore` so repository-only maintenance scripts are excluded from published skill bundles.
- Clarified in `SKILL.md` that local maintenance steps apply only to the repository copy.
- No MCP workflow or business logic changes.

---

## [2026.4.1-1] - 2026-04-01

### Changed

- **info-news-runtime-rules.md**: Align version-check UX — do not surface technical failure details to end users; forbid auto-download of `update-skill.sh` / `update-skill.ps1` (manual copy from gate/gate-skills allowed); success paths (`update_available` / strict exit 3) still require per-skill confirmation before `apply`.
- **SKILL.md — Trigger update**: Document ClawHub packages may omit `update-skill.ps1`; agent rules for Bash vs PowerShell vs WSL/Git Bash vs silent skip; use the same shell family for Steps 1–2; do not run `apply` / `revoke-pending` when Step 1 is skipped; dual-arg `DEST` / `name` order with script auto-swap when only one path contains `SKILL.md`.
- **scripts/update-skill.sh**, **scripts/update-skill.ps1**: Strict `check` (`GATE_SKILL_CHECK_STRICT=1`, exit 3, `GATE_SKILL_CONFIRM_TOKEN`, `revoke-pending`); expanded default install-root resolution (Cursor, Codex, OpenClaw, `.agents`, Antigravity).

---

## [2026.3.25-1] - 2026-03-25

### Added

- **Runtime rules**: SKILL.md references shared `info-news-runtime-rules.md` with `gate-runtime-rules.md`; **Trigger update** (check / confirm / apply) and **Routing Rules** aligned to the gate-info / gate-news rollout.
- **Update scripts**: `scripts/update-skill.sh`, `scripts/update-skill.ps1` (same pilot implementation as sibling Info/News skills).

---

## [2026.3.12-1] - 2026-03-12

### Added

- Skill: Trend / technical analysis. Trigger: technical/trend analysis (e.g. "Technical analysis for BTC"). Tools: info_markettrend_get_kline, info_markettrend_get_indicator_history, info_markettrend_get_technical_analysis, info_marketsnapshot_get_market_snapshot. Tool count: 4.
- SKILL.md: Routing, 4-tool parallel table, parameter extraction, Judgment Logic (Bollinger/volume/divergence/funding), 7-section Report Template, Error Handling, Cross-Skill, Safety. Aligned with docs/pd-vs-skills, docs/PD_VS_SKILLS_OPTIMIZATION_SUMMARY.md.
- README.md, references/scenarios.md.

### Audit

- Read-only; no trading or order execution.
