## Description:

Operate Moralis EVM wallet and token reads through UXC with a curated OpenAPI schema, API-key auth, and wallet-intelligence guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure and run read-only Moralis EVM wallet and token data queries through UXC, including balances, token holdings, history, swaps, net worth, metadata, and prices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default setup can pull a mutable remote API schema.

Mitigation: Prefer linking UXC to the bundled schema or an immutable pinned commit before using the skill.

Risk: Wallet addresses and analysis patterns are disclosed to Moralis when queries are sent.

Mitigation: Treat queried wallet data as shared with a third-party service, especially for private investigations or client work.

Risk: The skill requires a Moralis API key.

Mitigation: Use a Moralis API key with limited intended use and review the binding before installing or running commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jolestar/skills/moralis-openapi-skill)
- [Usage Patterns](references/usage-patterns.md)
- [Curated OpenAPI Schema](references/moralis-evm.openapi.json)
- [Moralis Wallet API Documentation](https://docs.moralis.com/data-api/evm/wallet)
- [Moralis Token API Documentation](https://docs.moralis.com/data-api/evm/token)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented API output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only EVM wallet and token operations; requires MORALIS_API_KEY and explicit chain parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
