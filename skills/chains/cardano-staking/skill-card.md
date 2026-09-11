## Description:

Check stake delegation and available ADA rewards for the connected wallet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adacapo21](https://clawhub.ai/user/adacapo21)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to check whether a connected Cardano wallet is delegated to a stake pool and to report claimable ADA staking rewards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a wallet seed phrase for a read-only staking check, and a seed phrase can grant control over wallet funds.

Mitigation: Use a public stake address, reward address, or another read-only identifier instead of a seed phrase whenever possible.

Risk: The staking check depends on an external MCP package that handles wallet-related input.

Mitigation: Review and pin the MCP package to a trusted version before installation, and only provide sensitive wallet material if the package and runtime are fully trusted.

## Reference(s):

- [Cardano Staking ClawHub Page](https://clawhub.ai/adacapo21/skills/cardano-staking)
- [adacapo21 Publisher Profile](https://clawhub.ai/user/adacapo21)
- [@indigoprotocol/cardano-mcp package](https://www.npmjs.com/package/@indigoprotocol/cardano-mcp)
- [Staking Concepts](references/concepts.md)
- [Staking MCP Tools Reference](references/mcp-tools.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or concise text summary of stake pool ID and available ADA rewards]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the connected MCP server's get_stake_delegation response; rewards are reported in ADA.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
