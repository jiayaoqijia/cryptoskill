# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-06-12

### Added
- Initial release of the **tokenomics-review** Agent Skill.
- `skill.md` methodology with a 5-step workflow: scope & data, severity model,
  red-flag checklist, red-flags quick scan, and a structured output format with
  a risk scorecard and verdict.
- **11+ checklist dimensions** — supply concentration & top-holder %, insider
  (team+investor) allocation & vesting, FDV/MC dilution overhang, emission/
  inflation vs demand sinks, upcoming unlock cliffs, real vs reflexive/ponzi
  yield, DEX liquidity depth & LP lock/burn, mint/pause/blacklist/owner admin
  functions, transfer tax/honeypot patterns, treasury runway, and governance
  centralization.
- **Severity model** (Critical → Info) where a single Critical rug vector caps
  the verdict at Likely-rug.
- **Red-flags quick scan** covering insider dominance, FDV/MC overhang,
  near-term unlocks, unlocked LP, mintable supply, anon + unaudited teams, and
  high transfer taxes.
- **Output format** with a risk scorecard, allocation & unlock-schedule tables,
  a prioritized top-risks list, and a Healthy / Caution / High-risk / Likely-rug
  verdict.
- Two worked example reports: a governance token (insider-heavy, FDV/MC 15× →
  High-risk) and a DeFi yield token (emissions-funded yield, unlocked LP,
  mintable supply → Likely-rug).
- Cross-links to Viprasol's `smart-contract-audit` and `defi-protocol-review`
  skills.
- "Not financial advice" / DYOR disclaimer in both `skill.md` and `README.md`.
- CI validator (`scripts/validate_skill.py`) and GitHub Actions workflow
  (`.github/workflows/validate.yml`).

[1.0.0]: https://github.com/Viprasol-Tech/tokenomics-review/releases/tag/v1.0.0
