## Description:

End-to-end Solana development playbook (Jan 2026). Prefer Solana Foundation framework-kit (@solana/client + @solana/react-hooks) for React/Next.js UI. Prefer @solana/kit for all new client/RPC/transaction code. When legacy dependencies require web3.js, isolate it behind @solana/web3-compat (or @solana/web3.js as a true legacy fallback). Covers wallet-standard-first connection (incl. ConnectorKit), Anchor/Pinocchio programs, Codama-based client generation, LiteSVM/Mollusk/Surfpool testing, and security checklists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h4rkl](https://clawhub.ai/user/h4rkl)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to build and review Solana dApps, wallet flows, transactions, on-chain programs, generated clients, tests, and security checklists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples used directly on mainnet or in payment flows could cause production-impacting transaction or settlement behavior if not reviewed.

Mitigation: Pin tool versions, isolate dependency installation from secrets, and manually review generated or adapted code before mainnet or payment use.

Risk: Smart-contract examples may need project-specific account closing, zero-copy read, and batch input validation checks before production use.

Mitigation: Review generated program code against the skill's Solana security checklist and run focused tests before deployment.

## Reference(s):

- [Solana Documentation](https://solana.com/docs)
- [Next.js + Solana React Hooks](https://solana.com/docs/frontend/nextjs-solana)
- [@solana/web3-compat](https://solana.com/docs/frontend/web3-compat)
- [Solana Kit Docs](https://solana.com/docs/clients/kit)
- [framework-kit Repository](https://github.com/solana-foundation/framework-kit)
- [@solana/kit Repository](https://github.com/anza-xyz/kit)
- [Anchor Documentation](https://www.anchor-lang.com/)
- [Pinocchio Repository](https://github.com/anza-xyz/pinocchio)
- [LiteSVM Repository](https://github.com/LiteSVM/litesvm)
- [Mollusk Repository](https://github.com/buffalojoec/mollusk)
- [Surfpool Documentation](https://docs.surfpool.dev/)
- [Codama Generating Clients](https://solana.com/docs/programs/codama-generating-clients)
- [Solana Security Best Practices](https://solana.com/docs/programs/security)
- [ClawHub Skill Release](https://clawhub.ai/h4rkl/skills/solana-dev-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include file diffs, install/build/test commands, and risk notes for signing, fees, CPIs, token transfers, and mainnet or payment flows.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
