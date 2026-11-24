# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-06-12

### Added
- Initial release of the **defi-protocol-review** Agent Skill.
- `skill.md` methodology with a 5-step workflow: scope & data, severity model,
  seven review dimensions, red-flag quick scan, and a structured output format
  with a risk matrix and verdict.
- **Seven review dimensions:** smart-contract control (admin keys &
  upgradeability), audits & track record, economic design (yield/peg
  sustainability), liquidity & TVL quality, oracle dependency, team &
  transparency, and composability/contagion — each with what-to-check, why, and
  good-vs-bad signals.
- **Severity model** (Critical → Info) where the worst unresolved finding caps
  the verdict.
- **Red-flag quick scan** for the classic rug and exploit tells (EOA owner,
  no-timelock upgrades, mint/sweep powers, unaudited code, emissions-only yield,
  "guaranteed" APY, concentrated TVL, single-source oracle, anon-team profile).
- **Risk matrix output** and a single **Low / Moderate / High / Avoid** verdict
  with an "if you still deposit" mitigation note.
- Cross-links to the Viprasol `smart-contract-audit` and `tokenomics-review`
  skills.
- Two worked example reviews: a lending protocol (Moderate/High) and a yield
  farm (Avoid).
- "Not financial advice" disclaimer in both `skill.md` and `README.md`.
- CI validator (`scripts/validate_skill.py`) and GitHub Actions workflow
  (`.github/workflows/validate.yml`).

[1.0.0]: https://github.com/Viprasol-Tech/defi-protocol-review/releases/tag/v1.0.0
