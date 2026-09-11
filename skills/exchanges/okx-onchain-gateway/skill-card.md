## Description:

Guides an agent through gas price lookup, gas-limit estimation, transaction simulation, signed transaction broadcasting, supported-chain lookup, and broadcast order tracking across XLayer, Solana, Ethereum, Base, BSC, Arbitrum, Polygon, and other chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ok-james-01](https://clawhub.ai/user/ok-james-01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and blockchain operators use this skill to prepare and route on-chain gateway commands for gas checks, transaction simulations, signed transaction broadcasts, and transaction status tracking. It is intended for users who already understand the transaction they are sending because the skill does not sign transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broadcasting a signed transaction can move funds or change on-chain state.

Mitigation: Require the user to provide an already signed transaction, surface simulation or status results clearly, and avoid treating broadcast output as instructions.

Risk: The skill can trigger installation or update of remote CLI code before running gateway commands.

Mitigation: Install from a trusted, pinned release and verify installer and binary checksums before execution.

Risk: Shared API access may be rate limited or unsuitable for routine production use.

Mitigation: Use a personal OKX developer key when needed and keep local secrets out of version control.

## Reference(s):

- [Onchain OS Gateway CLI Reference](artifact/references/cli-reference.md)
- [OKX Web3](https://web3.okx.com)
- [OKX Developer Portal](https://web3.okx.com/onchain-os/dev-portal)
- [ClawHub Skill Page](https://clawhub.ai/ok-james-01/skills/okx-onchain-gateway)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and concise status or result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include transaction hashes, order IDs, gas estimates, simulation status, and follow-up prompts when returned by the CLI.]

## Skill Version(s):

3.1.3 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
