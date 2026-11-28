# Wallet Security Review — Agent Skill

> Before you sign anything: read the signature/approval request, name its blast
> radius, and get a blunt sign / don't-sign verdict — drainers, Permit2,
> setApprovalForAll, eth_sign, and EIP-7702 delegations included.

[![GitHub stars](https://img.shields.io/github/stars/Viprasol-Tech/wallet-security-review?style=social)](https://github.com/Viprasol-Tech/wallet-security-review)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Compatible-blueviolet)](https://github.com/Viprasol-Tech/wallet-security-review)
[![Vectors](https://img.shields.io/badge/Signature%20Types-8-green)](skill.md)
[![Covers](https://img.shields.io/badge/Permit2%20%2B%20EIP--7702-blue)](skill.md)
[![Version](https://img.shields.io/badge/version-1.0.0-informational)](CHANGELOG.md)

**Works with:** Claude Code · OpenAI Codex · Cursor · GitHub Copilot · Gemini
CLI · 26+ tools that support portable agent skills.

---

## Quick Install

Clone the skill into your agent's skills directory:

```bash
# Claude Code
git clone https://github.com/Viprasol-Tech/wallet-security-review \
  ~/.claude/skills/wallet-security-review

# OpenAI Codex
git clone https://github.com/Viprasol-Tech/wallet-security-review \
  ~/.codex/skills/wallet-security-review

# Cursor / Gemini CLI / other tools — clone anywhere your tool loads skills from, e.g.
git clone https://github.com/Viprasol-Tech/wallet-security-review \
  ~/.config/skills/wallet-security-review
```

The skill is a single self-contained `skill.md` (plus examples) — no
dependencies, no install step, nothing to build.

## Try It

Paste a signature request (or your approval list) and ask:

```
Is this safe to sign? — {"method":"eth_signTypedData_v4", ...}
```

The skill will scope what's being signed and on which chain, classify the exact
signature/approval type, name its blast radius, scan for drainer red flags, and
return a verdict banner (✅ / ⚠️ / ⛔ / 🚨) with a remediation playbook.

---

## Why This Exists

Most wallet losses aren't broken cryptography — they're a user clicking
**"Confirm"** on a request they didn't understand. A single off-chain Permit2
signature can authorize draining **every token you ever approved to Permit2**; a
"mint" that asks for `setApprovalForAll` can take your whole NFT collection; an
`eth_sign` is a blank check; and an EIP-7702 delegation can hand over your entire
account. Approval-based attacks drained **$200M+ in 2024–2025**, and **>90% of
observed EIP-7702 delegations are malicious**. The defense is a *consistent*
pre-sign checklist — recognize the request type, state what it grants, and refuse
the dangerous ones. This skill encodes that checklist so your agent runs it the
same way every time.

## What It Does

1. **Scopes** the review — a live signature, an existing wallet's approvals, or a
   suspicious site — and on which chain(s) and signer (hardware?).
2. **Classifies** the request against the full **signature & approval taxonomy**
   (approve / increaseAllowance / Permit / Permit2 / setApprovalForAll /
   eth_sign / personal_sign · signTypedData / EIP-7702).
3. **Names the blast radius** — one token, a whole NFT collection, every Permit2
   token, or the entire EOA.
4. **Audits approval lists** — flags unlimited allowances, unknown spenders,
   stale grants, Permit2 allowances, and 7702 delegations; covers address
   poisoning and delayed draining.
5. **Runs a red-flag quick scan** — eth_sign, wrong-site Permit2, mint asking
   setApprovalForAll, urgency, blind signing, lookalike domains, DM delivery.
6. **Outputs a verdict** (✅ / ⚠️ / ⛔ / 🚨), a findings table, and a
   **remediation playbook** (revoke.cash, fresh-wallet move, hardware + clear
   signing, vault/burner split).

## Features

- **Full signature taxonomy** — every common request a wallet shows, each with
  what it does, how to recognize it in the payload, and safe-vs-dangerous.
- **Severity model** — 🔴 Critical / 🟠 High / 🟡 Medium / 🟢 Low / ℹ️ Info, scored
  by blast radius × likelihood.
- **EIP-7702 aware** — treats an unknown delegation as full compromise, not a
  routine revoke, with the fresh-wallet remediation path.
- **Approval-audit mode** — turns a revoke.cash / Etherscan export into a ranked
  findings table.
- **Remediation playbook** — revoke order, fresh-wallet move, hardware + clear
  signing (ERC-7730), vault/burner split, seed-phrase and 2FA hygiene.

### Signature blast-radius table

| Request | What it grants | Blast radius |
|---|---|---|
| `approve` (finite) | spend up to a cap | one token, capped |
| `approve` (unlimited) | spend any amount, forever | one token, **uncapped** |
| Permit / Permit2 | off-chain spend authorization | one token → **all Permit2 tokens** |
| `setApprovalForAll` | operator over a collection | **whole NFT collection** |
| `eth_sign` | sign an arbitrary hash | **unbounded — never sign** |
| EIP-7702 delegation | delegate the EOA's code | **entire account** |

*Recognize the type first; the verdict follows from the blast radius.*

See full worked reports in **[examples/](examples/)**:
- [Permit2 phishing signature](examples/permit2-phishing-signature.md) — a fake
  "airdrop claim" Permit2 sig with full-balance blast radius → ⛔ DO NOT SIGN.
- [Wallet approval audit](examples/wallet-approval-audit.md) — unlimited USDC,
  a dead-marketplace setApprovalForAll, a Permit2 allowance, and an unknown
  EIP-7702 delegation → 🚨 compromised, fresh-wallet remediation.

---

## Not Security-Audited Advice

This skill provides **educational security guidance only** — not financial,
legal, or investment advice, and **not a guarantee of safety**. On-chain
transactions are **irreversible**, and the skill reasons only over the
information you provide; it cannot see live chain state. A "looks safe" result is
not a warranty — always verify the spender, the domain, and the decoded payload
yourself, and if you believe your wallet is compromised, act immediately and
consult a qualified professional. **Not affiliated with or endorsed by
Anthropic.**

---

## Contact — Viprasol Tech Private Limited
- 🌐 Website: [viprasol.com](https://viprasol.com)
- ✉️ Email: [support@viprasol.com](mailto:support@viprasol.com)
- 💬 Telegram: [t.me/viprasol_help](https://t.me/viprasol_help) · 📱 WhatsApp: +91 96336 52112
- 🐙 GitHub: [@Viprasol-Tech](https://github.com/Viprasol-Tech) · 💼 [LinkedIn](https://www.linkedin.com/in/viprasol/) · 𝕏 [@viprasol](https://twitter.com/viprasol)

> *Viprasol Tech — fintech software, AI agents, algorithmic trading systems, and B2B SaaS.*

## License
[MIT](LICENSE) © 2025 Viprasol Tech Private Limited
