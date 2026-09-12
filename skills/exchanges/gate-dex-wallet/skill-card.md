## Description:

Gate DEX Wallet helps agents manage Gate DEX wallet authentication, balances, wallet addresses, transaction history, token transfers, on-chain withdrawals, x402 payments, DApp signing, and CLI/MCP setup with mandatory terminal tx-checkin before signing actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route wallet-related requests through Gate DEX MCP or CLI flows for authentication, asset lookup, transfers, withdrawals, x402 payment, and DApp interaction. It is intended for wallet identity and asset management, not market data lookup, token security audit, or token swap execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles wallet credentials, local signing helpers, signing requests, and automatic payment flows.

Mitigation: Require exact payment terms, explicit user confirmation, and successful terminal tx-checkin before any signing, transfer, withdrawal, DApp, or x402 payment action.

Risk: Installation can persistently change agent and MCP configuration files.

Mitigation: Review proposed changes to MCP configuration, CLAUDE.md, and AGENTS.md before use, and prefer project-scoped configuration where available.

Risk: The release depends on local tx-checkin binaries whose provenance should be verified before execution.

Mitigation: Verify the presence, source, and integrity of tx-checkin binaries before running them, and do not substitute compiled or unverified binaries.

Risk: Authorization headers and wallet tokens could be exposed if forwarded to arbitrary URLs.

Mitigation: Only send Authorization headers and wallet credentials to the configured Gate wallet service endpoints, and keep tokens redacted in user-facing output.

Risk: Global npm installation and elevated privileges can broaden the impact of a compromised CLI or package.

Mitigation: Avoid sudo and global npm installation where possible; prefer least-privilege, pinned, and reviewed installation paths.

## Reference(s):

- [Gate DEX Wallet ClawHub Page](https://clawhub.ai/gate-exchange/skills/gate-dex-wallet)
- [Authentication Reference](references/auth.md)
- [Asset Query Reference](references/asset-query.md)
- [Transfer Reference](references/transfer.md)
- [Withdraw Reference](references/withdraw.md)
- [DApp Reference](references/dapp.md)
- [x402 Payment Reference](references/x402.md)
- [Terminal tx-checkin Reference](references/tx-checkin.md)
- [Gate Wallet CLI Reference](references/cli.md)
- [MCP Reference](references/mcp.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with inline shell commands, MCP call parameters, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation and terminal tx-checkin before signing or x402 payment actions.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata; artifact frontmatter reports 2026.4.3-2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
