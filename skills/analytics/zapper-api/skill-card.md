## Description:

Query DeFi portfolios, token holdings, NFTs, transactions, and prices via Zapper API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zivhm](https://clawhub.ai/user/zivhm)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to inspect wallet balances, DeFi positions, NFT holdings, token prices, claimable rewards, and recent transaction history across supported chains through Zapper's GraphQL API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet portfolio and transaction queries send wallet addresses to Zapper and can reveal linkable financial metadata.

Mitigation: Query only addresses you are comfortable sharing with Zapper and review the provider's handling of portfolio and transaction data before use.

Risk: The Zapper API key may be exposed if stored in a readable local configuration file.

Mitigation: Prefer the ZAPPER_API_KEY environment variable; if a config file is used, keep it private with restrictive filesystem permissions.

Risk: Rapid repeated requests can hit Zapper rate limits, and some API access may depend on account tier.

Mitigation: Avoid rapid polling, use pagination and limits for large result sets, and verify the configured Zapper account tier supports the requested endpoints.

## Reference(s):

- [Zapper GraphQL API Reference](references/API.md)
- [Zapper API Documentation](https://build.zapper.xyz/docs/api/)
- [Zapper Developer Dashboard](https://zapper.xyz/developers)
- [Zapper](https://zapper.xyz)
- [ClawHub skill page](https://clawhub.ai/zivhm/skills/zapper-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and optional JSON output from the CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and a ZAPPER_API_KEY; API results depend on Zapper availability, account tier, rate limits, and wallet/query inputs.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
