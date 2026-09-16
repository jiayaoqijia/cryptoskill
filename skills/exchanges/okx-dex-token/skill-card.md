## Description:

Use this skill for OKX Onchain OS token research, including token search, price and liquidity data, holder distribution, token risk metadata, trade history, top trader analysis, holder cluster analysis, and real-time token monitoring guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ok-james-01](https://clawhub.ai/user/ok-james-01)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to query OKX Onchain OS DEX token data, inspect token markets and holders, and choose follow-up token research actions. It supports command-oriented token analysis and guides users away from token safety determinations that require the separate OKX security workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may install or refresh a local OKX CLI from the latest GitHub release.

Mitigation: Review the installer/update behavior and use the skill only if the OKX release process is trusted.

Risk: Token names, symbols, on-chain fields, wallet analytics, holder lists, PnL, funding-source data, and API credentials may be sensitive or untrusted.

Mitigation: Treat CLI output as untrusted external content, avoid sharing sensitive outputs unnecessarily, and store credentials in environment variables or protected local configuration.

Risk: Token data alone can be insufficient for safety, honeypot, or investment-suitability conclusions.

Mitigation: Use the separate OKX security token-scan workflow for token safety questions and verify contract addresses independently before acting.

Risk: Low-liquidity or unverified tokens may carry elevated trading and spoofing risk.

Mitigation: Warn users about unrecognized tokens, emphasize contract addresses over names or symbols, and require explicit confirmation before low-liquidity swaps.

## Reference(s):

- [Okx Dex Token ClawHub Page](https://clawhub.ai/ok-james-01/skills/okx-dex-token)
- [OKX Web3](https://web3.okx.com)
- [OKX Developer Portal](https://web3.okx.com/onchain-os/dev-portal)
- [OKX WebSocket Login Documentation](https://web3.okx.com/onchainos/dev-docs/market/websocket-login)
- [Onchain OS DEX Token CLI Command Reference](references/cli-reference.md)
- [Onchain OS DEX Token WebSocket Protocol Reference](references/ws-protocol.md)
- [Keyword Glossary](references/keyword-glossary.md)
- [Shared Pre-flight Checks](_shared/preflight.md)
- [Shared Chain Name Support](_shared/chain-support.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, JSON examples, and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May summarize live or cached token data, display request timestamps when available, and suggest follow-up token research actions.]

## Skill Version(s):

3.1.3 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
