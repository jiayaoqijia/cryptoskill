# Tokenomics Review — Agent Skill

> Review a crypto token's economics for red flags — supply & FDV, insider
> allocation & vesting, emissions, unlock overhang, liquidity, and rug vectors —
> and get a risk scorecard with a clear verdict.

[![GitHub stars](https://img.shields.io/github/stars/Viprasol-Tech/tokenomics-review?style=social)](https://github.com/Viprasol-Tech/tokenomics-review)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Compatible-blueviolet)](https://github.com/Viprasol-Tech/tokenomics-review)
[![Dimensions](https://img.shields.io/badge/Checks-11%2B-green)](skill.md)
[![Verdict](https://img.shields.io/badge/Healthy%20%E2%86%92%20Likely--rug-blue)](skill.md)
[![Version](https://img.shields.io/badge/version-1.0.0-informational)](CHANGELOG.md)

**Works with:** Claude Code · OpenAI Codex · Cursor · GitHub Copilot · Gemini CLI · 26+ tools
that support portable agent skills.

---

## Quick Install

Clone the skill into your agent's skills directory:

```bash
# Claude Code
git clone https://github.com/Viprasol-Tech/tokenomics-review \
  ~/.claude/skills/tokenomics-review

# OpenAI Codex
git clone https://github.com/Viprasol-Tech/tokenomics-review \
  ~/.codex/skills/tokenomics-review

# Cursor / Copilot / other tools — clone anywhere your tool loads skills from, e.g.
git clone https://github.com/Viprasol-Tech/tokenomics-review \
  ~/.config/skills/tokenomics-review
```

The skill is a single self-contained `skill.md` (plus examples) — no
dependencies, no install step, nothing to build.

## Try It

Paste a token's tokenomics (or a link to its distribution + vesting) and ask:

```
Review these tokenomics for red flags — is this token healthy or a rug?
```

The skill will scope the token and chain, lay out supply/FDV and the allocation
& unlock schedule, work the 11+-dimension checklist, run a red-flags quick scan,
and return a risk scorecard with a one-paragraph verdict
(Healthy / Caution / High-risk / Likely-rug).

---

## Why This Exists

Most token blow-ups are not surprises — they're scheduled. A 55% insider
allocation, a short cliff before a cliff-dump, an FDV ten times the market cap,
emissions-funded "yield", or LP the deployer never locked: each is visible *before*
the drawdown, if you run the same checklist every time. The problem is that
"tokenomics" is easy to skim and easy to dress up, so people eyeball a headline
APY or a pretty pie chart and miss the unlock overhang or the mint authority. This
skill encodes the due-diligence checklist — supply & FDV, insider allocation &
vesting, emissions/inflation, unlock cliffs, liquidity, and rug vectors — so your
agent runs it consistently, shows the math, and never skips the contract-permission
and liquidity-lock checks.

## What It Does

1. **Scopes** the token, chain(s), contract address, supply (total/max/
   circulating), FDV vs market cap, and the allocation breakdown.
2. **Lays out** the allocation and the vesting / unlock schedule — cliffs,
   linear release, and the % of float unlocking in the next 30 / 90 days.
3. **Works an 11+-dimension checklist** — supply concentration, insider
   allocation & vesting, FDV/MC overhang, emissions vs sinks, unlock cliffs,
   real vs reflexive utility, liquidity depth & LP lock, admin/rug functions,
   transfer tax/honeypot, treasury runway, and governance centralization.
4. **Grades severity** on a Critical → Info model so a single rug vector caps the
   verdict.
5. **Runs a red-flags quick scan** (insiders > 50%, FDV/MC > 10, big near-term
   unlock, unlocked LP, mintable supply, anon + unaudited, high transfer tax…).
6. **Outputs a scorecard** plus allocation & unlock tables, a prioritized top-
   risks list, and a single **Healthy / Caution / High-risk / Likely-rug**
   verdict.

## Features

- **Full red-flag checklist** — supply concentration & top-holder %, insider
  (team+investor) allocation & vesting, FDV/MC dilution overhang, emission/
  inflation vs demand sinks, upcoming unlock cliffs, real vs ponzi yield, DEX
  liquidity depth & LP lock/burn, mint/pause/blacklist/owner functions, transfer
  tax/honeypot, treasury runway, governance centralization.
- **Severity model** — Critical / High / Medium / Low / Info, where a Critical
  rug vector disqualifies the token regardless of the rest.
- **Allocation & unlock tables** — bucket-by-bucket distribution with cliff,
  vesting, and near-term unlock load.
- **Risk scorecard** — every metric flagged 🔴 / 🟡 / 🟢 with the value behind it.
- **Clear verdict** — one of Healthy / Caution / High-risk / Likely-rug, with a
  one-paragraph justification.
- **Cross-links** — pairs with Viprasol's `smart-contract-audit` (code safety)
  and `defi-protocol-review` (mechanism soundness).

### Example red-flag table

| Red flag | Threshold | Severity |
|---|---|---|
| Insider (team + investor) allocation | > 50% of supply | 🔴 |
| FDV / MC ratio | > 10× | 🔴 |
| Float unlocking next 30 days | > 10% | 🔴 |
| LP not locked or burned | deployer holds LP | 🔴 |
| Transfer tax | > 10% (or sell-only) | 🔴 |

*Thresholds are general heuristics; the skill adjusts for token context.*

See full worked reports in **[examples/](examples/)**:
- [Governance token review](examples/governance-token-review.md) — 55% insider
  allocation, short cliff then a big unlock, FDV/MC 15× ⇒ **High-risk**.
- [DeFi yield token review](examples/defi-yield-token-review.md) —
  emissions-funded "ponzi" yield, unlocked LP, mintable supply ⇒ **Likely-rug**.

---

## Not Financial Advice

This skill provides **educational tokenomics analysis only** — not financial,
investment, legal, or tax advice. Crypto is a **high-risk** asset class: tokens
can go to zero, contracts can be exploited, and tokenomics can be engineered to
look healthy while extracting value. Benchmarks here are heuristics with false
positives and false negatives; a clean scorecard does not make a token safe.
Always verify every figure **on-chain** against the token and vesting contracts,
read any audit in full, and **do your own research (DYOR)** before interacting
with or investing in any token. **Not affiliated with or endorsed by Anthropic.**

---

## Contact — Viprasol Tech Private Limited
- 🌐 Website: [viprasol.com](https://viprasol.com)
- ✉️ Email: [support@viprasol.com](mailto:support@viprasol.com)
- 💬 Telegram: [t.me/viprasol_help](https://t.me/viprasol_help) · 📱 WhatsApp: +91 96336 52112
- 🐙 GitHub: [@Viprasol-Tech](https://github.com/Viprasol-Tech) · 💼 [LinkedIn](https://www.linkedin.com/in/viprasol/) · 𝕏 [@viprasol](https://twitter.com/viprasol)

> *Viprasol Tech — fintech software, AI agents, algorithmic trading systems, and B2B SaaS.*

## License
[MIT](LICENSE) © 2025 Viprasol Tech Private Limited
