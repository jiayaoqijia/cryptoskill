# DeFi Protocol Review — Agent Skill

> Vet a DeFi protocol before you deposit: admin-key & upgradeability risk,
> audits, yield sustainability, liquidity/TVL quality, oracle dependency, and
> team transparency — into a risk matrix and a clear rug & exploit verdict.

[![GitHub stars](https://img.shields.io/github/stars/Viprasol-Tech/defi-protocol-review?style=social)](https://github.com/Viprasol-Tech/defi-protocol-review)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Compatible-blueviolet)](https://github.com/Viprasol-Tech/defi-protocol-review)
[![Dimensions](https://img.shields.io/badge/Risk%20Dimensions-7-green)](skill.md)
[![Verdict](https://img.shields.io/badge/Low%20%C2%B7%20Moderate%20%C2%B7%20High%20%C2%B7%20Avoid-blue)](skill.md)
[![Version](https://img.shields.io/badge/version-1.0.0-informational)](CHANGELOG.md)

**Works with:** Claude Code · OpenAI Codex · Cursor · GitHub Copilot ·
Gemini CLI · 26+ tools that support portable agent skills.

---

## Quick Install

Clone the skill into your agent's skills directory:

```bash
# Claude Code
git clone https://github.com/Viprasol-Tech/defi-protocol-review \
  ~/.claude/skills/defi-protocol-review

# Cursor / Codex / other tools — clone anywhere your tool loads skills from, e.g.
git clone https://github.com/Viprasol-Tech/defi-protocol-review \
  ~/.config/skills/defi-protocol-review
```

The skill is a single self-contained `skill.md` (plus examples) — no
dependencies, no install step, nothing to build.

## Try It

Paste a protocol's docs, contract addresses, audit status, token, and TVL and
ask:

```
Review this DeFi protocol — is it safe to deposit, or is it a rug risk?
```

The skill will scope the protocol and category, work through all seven risk
dimensions, run the red-flag quick scan, and return a risk matrix with top
risks, an "if you still deposit" mitigation note, and a single
Low / Moderate / High / Avoid verdict.

---

## Why This Exists

DeFi due diligence is a repeatable, methodical process — but it's easy to be
dazzled by a triple-digit APY, trust a "audited" badge that covers the wrong
contract, or miss that a single private key can drain the pool. Experienced
reviewers run the *same* checklist every time: who controls the contracts, is it
really audited, where does the yield come from, can you actually withdraw, can
the oracle be gamed, who's behind it, and what does it depend on. This skill
encodes that checklist so your agent runs it consistently, treats unknowns as
risk, and never skips the admin-key and oracle checks that catch most rugs and
exploits.

## What It Does

1. **Scopes** the protocol, chain(s), category, TVL trend, token, and the exact
   contracts/docs/audits being reviewed.
2. **Applies a severity model** (Critical → Info) where the worst unresolved
   finding caps the verdict.
3. **Reviews seven dimensions** — smart-contract control, audits & track
   record, economic design, liquidity & TVL, oracle dependency, team &
   transparency, and composability/contagion — each with good-vs-bad signals.
4. **Runs a red-flag quick scan** for the classic rug and exploit tells.
5. **Outputs a risk matrix** (dimension × severity) with top risks and the
   evidence behind each.
6. **Adds an "if you still deposit" mitigation note** for anyone proceeding
   anyway.
7. **Returns a single verdict** — **Low / Moderate / High / Avoid**.

## Features

- **Seven-dimension framework** — admin keys & upgradeability, audits & track
  record, yield sustainability, liquidity/TVL quality, oracle resistance, team
  transparency, and composability/contagion.
- **Severity model** — Critical / High / Medium / Low / Info, where one
  funds-at-immediate-risk finding forces **Avoid**.
- **Red-flag quick scan** — EOA owner, no-timelock upgrades, mint/sweep powers,
  unaudited code, emissions-only yield, "guaranteed" APY, concentrated TVL,
  single-source oracle, anon-team rug profile, unexplained TVL spikes.
- **Category-aware** — distinct threat models for DEX, lending, perps,
  stablecoin, and yield/aggregator protocols.
- **On-chain-first** — verify ownership, powers, and claims on-chain, not from
  the marketing page; flag when deployed code doesn't match the audit.
- **Cross-linked** — pairs with Viprasol `smart-contract-audit` (code-level
  review) and `tokenomics-review` (emissions & supply).

### Example severity table

| Dimension | Good signal | Bad signal | Worst-case severity |
|---|---|---|---|
| Smart-contract control | Timelocked multisig / immutable | EOA owner, no-timelock proxy | Critical |
| Audits & track record | Multiple recent audits, fixed | Unaudited / unfixed criticals | Critical |
| Economic design | Real-fee yield, over-collateralized | Emissions-only, "guaranteed" APY | High |
| Oracle dependency | Redundant feeds, TWAP | Single-source spot price | High |
| Team & transparency | Doxxed/reputable, real docs | Anon + custody + no docs | High |

*Severities are heuristics; the skill adjusts for category and context.*

See full worked reports in **[examples/](examples/)**:
- [Lending protocol review](examples/lending-protocol-review.md) —
  multisig + timelock good, but single-source oracle + emissions yield ⇒
  Moderate/High.
- [Yield farm review](examples/yield-farm-review.md) — anon team, EOA owner,
  unaudited, fixed 200% APY ⇒ Avoid.

---

## Not Financial Advice

This skill provides **educational due-diligence analysis only** — not financial,
investment, legal, or security-audit advice, and not a recommendation. A passing
review is **not** a safety guarantee and does not replace a professional
smart-contract audit. **Smart-contract risk is real:** exploits, governance
attacks, oracle manipulation, de-pegs, and rug pulls cause total loss even in
audited, high-TVL protocols. Always verify contracts and claims on-chain
yourself, and **never deposit more than you can afford to lose.**
**Not affiliated with or endorsed by Anthropic.**

---

## Contact — Viprasol Tech Private Limited
- 🌐 Website: [viprasol.com](https://viprasol.com)
- ✉️ Email: [support@viprasol.com](mailto:support@viprasol.com)
- 💬 Telegram: [t.me/viprasol_help](https://t.me/viprasol_help) · 📱 WhatsApp: +91 96336 52112
- 🐙 GitHub: [@Viprasol-Tech](https://github.com/Viprasol-Tech) · 💼 [LinkedIn](https://www.linkedin.com/in/viprasol/) · 𝕏 [@viprasol](https://twitter.com/viprasol)

> *Viprasol Tech — fintech software, AI agents, algorithmic trading systems, and B2B SaaS.*

## License
[MIT](LICENSE) © 2025 Viprasol Tech Private Limited
