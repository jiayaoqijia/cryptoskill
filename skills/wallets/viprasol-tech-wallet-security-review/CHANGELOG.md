# Changelog

All notable changes to this project are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-06-12

### Added
- Initial release of the **wallet-security-review** Agent Skill.
- `skill.md` methodology with a 6-step workflow: scope & context, severity
  model, signature & approval taxonomy, wallet approval audit, red-flags quick
  scan, and a structured output format with a sign/don't-sign verdict.
- **Full signature & approval taxonomy** (8 types): ERC-20 `approve`
  (finite vs unlimited), `increaseAllowance`, Permit (EIP-2612), Permit2,
  `setApprovalForAll`, `eth_sign` blind signing, `personal_sign`/`signTypedData`
  disguised intents, and EIP-7702 authorization/delegation.
- **Severity model** (🔴 Critical / 🟠 High / 🟡 Medium / 🟢 Low / ℹ️ Info)
  scored by blast radius × likelihood.
- **Approval-audit mode** — flags unlimited allowances, unknown spenders, stale
  approvals, `setApprovalForAll` grants, Permit2 allowances, and 7702
  delegations; covers address poisoning and drainer-kit delayed draining.
- **Remediation playbook** — revoke.cash / Etherscan revocation order,
  fresh-wallet move for compromise, hardware wallet + clear signing (ERC-7730),
  vault/burner split, seed-phrase and authenticator-2FA hygiene.
- Verdict banners: ✅ LIKELY SAFE / ⚠️ CAUTION / ⛔ DO NOT SIGN /
  🚨 WALLET MAY BE COMPROMISED.
- Two worked example reports: a Permit2 phishing signature and a wallet approval
  audit with an unknown EIP-7702 delegation.
- "Educational security guidance, not financial advice" disclaimer in both
  `skill.md` and `README.md`.
- CI validator (`scripts/validate_skill.py`) and GitHub Actions workflow
  (`.github/workflows/validate.yml`).

[1.0.0]: https://github.com/Viprasol-Tech/wallet-security-review/releases/tag/v1.0.0
