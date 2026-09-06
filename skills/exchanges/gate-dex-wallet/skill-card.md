## Description: <br>
Gate DEX Wallet helps agents manage Gate DEX wallet authentication, balances, wallet addresses, transaction history, transfers, on-chain withdrawals, x402 payments, DApp interactions, and related CLI workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gate-exchange](https://clawhub.ai/user/gate-exchange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External wallet users and developers use this skill to manage Gate DEX wallet identity and assets through MCP or CLI workflows, including authentication, balances, transfers, withdrawals, x402 payments, and DApp signing flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan describes this as a real wallet skill with broad financial, credential, installer, and agent-routing authority. <br>
Mitigation: Install only when the full Gate DEX wallet and CLI suite is intended, and review installer and routing changes before deployment. <br>
Risk: The skill can guide transaction signing, payments, approvals, and other wallet actions. <br>
Mitigation: Verify every transaction, payment, approval, and signing request before confirming, and require the documented terminal tx-checkin flow before signing. <br>
Risk: The scan guidance identifies the tx-checkin binary, npm CLI, Gate MCP endpoint, OAuth session files, and AGENTS.md or CLAUDE.md edits as persistent trusted components. <br>
Mitigation: Treat those components as trusted installation surface, keep them under review, and remove or rotate them when the skill is no longer needed. <br>
Risk: OpenAPI keys may be configured for hybrid swap workflows. <br>
Mitigation: Avoid configuring OpenAPI keys unless hybrid swap is required, and protect any configured credentials according to the user's credential-management policy. <br>


## Reference(s): <br>
- [Gate DEX Wallet on ClawHub](https://clawhub.ai/gate-exchange/gate-dex-wallet) <br>
- [Gate DEX Wallet README](README.md) <br>
- [Gate DEX Auth](references/auth.md) <br>
- [Gate DEX Asset Query](references/asset-query.md) <br>
- [Gate DEX Transfer](references/transfer.md) <br>
- [Gate DEX Withdraw](references/withdraw.md) <br>
- [Gate DEX x402 Payment](references/x402.md) <br>
- [Gate DEX DApp](references/dapp.md) <br>
- [Gate DEX Tx Check-in](references/tx-checkin.md) <br>
- [Gate DEX CLI](references/cli.md) <br>
- [Gate DEX Wallet MCP Specification](references/mcp.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline commands, configuration snippets, and MCP tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include transaction, payment, approval, authentication, and CLI instructions that require user review before execution.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
