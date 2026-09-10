## Description:

Query DeFi portfolio data across 50+ chains via Zapper's GraphQL API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spirosrap](https://clawhub.ai/user/spirosrap)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to inspect wallet balances, DeFi positions, NFT holdings, token prices, transaction history, and unclaimed rewards through Zapper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses and related DeFi, NFT, and transaction data are sent to Zapper.

Mitigation: Use the skill only when that data sharing is acceptable for the wallet and workflow.

Risk: The skill stores and uses a Zapper API key.

Mitigation: Store the API key with restrictive file permissions and avoid shared machines.

Risk: Untrusted address or symbol strings may increase command and request handling risk.

Mitigation: Avoid passing untrusted address or symbol strings until JSON construction and config-path handling are fixed.

## Reference(s):

- [Zapper API Reference](references/api.md)
- [Zapper API Docs](https://build.zapper.xyz/docs/api)
- [Zapper Dashboard](https://dashboard.zapper.xyz)
- [Zapper Homepage](https://zapper.xyz)
- [ClawHub Skill Page](https://clawhub.ai/spirosrap/skills/zapper)
- [Publisher Profile](https://clawhub.ai/user/spirosrap)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and shell command guidance with tabular command output from the Zapper API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, python3, and a Zapper API key.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
