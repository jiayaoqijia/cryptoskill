## Description:

Zerion API queries real-time crypto wallet portfolios, transactions, DeFi positions, NFTs, token prices, and gas fees across EVM chains and Solana using Zerion's API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abishekdharshan](https://clawhub.ai/user/abishekdharshan)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and agent users use this skill to inspect authorized wallet portfolios, transaction histories, DeFi positions, NFT holdings, token prices, and gas fees through Zerion's MCP/API integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet histories, portfolio composition, DeFi positions, and NFT holdings can expose sensitive financial behavior.

Mitigation: Use the skill only for lawful, approved analysis of wallets you own or are clearly authorized to review.

Risk: The skill requires a Zerion API key for the remote MCP server.

Mitigation: Protect the API key in MCP configuration and avoid exposing it in prompts, logs, or shared outputs.

Risk: Security review flagged the release as suspicious because sensitive third-party financial profiling use cases are under-scoped.

Mitigation: Review the skill before installation and apply the provided security guidance before analyzing third-party wallets.

## Reference(s):

- [Zerion API Documentation](https://developers.zerion.io)
- [Building with AI](https://developers.zerion.io/reference/building-with-ai)
- [Zerion Dashboard](https://dashboard.zerion.io)
- [Zerion llms.txt](https://developers.zerion.io/llms.txt)
- [ClawHub Skill Page](https://clawhub.ai/abishekdharshan/skills/zerion-api-skill)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, Configuration]

**Output Format:** [Markdown with JSON configuration snippets and natural-language API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Zerion API key and configured remote HTTP MCP server.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
