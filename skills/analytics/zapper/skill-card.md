## Description: <br>
Query DeFi portfolio data across 50+ chains via Zapper's GraphQL API for wallet balances, DeFi positions, NFT holdings, token prices, and transaction history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spirosrap](https://clawhub.ai/user/spirosrap) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to query Zapper for wallet portfolio summaries, token holdings, DeFi app positions, NFTs, token prices, recent transactions, and claimable rewards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet address and portfolio queries are sent to Zapper and may reveal portfolio-related activity. <br>
Mitigation: Use the skill only for wallet lookups you are comfortable sending to Zapper, consistent with the security guidance. <br>
Risk: The skill requires a locally stored Zapper API key. <br>
Mitigation: Use a dedicated, revocable API key and keep the config file permissions restrictive; never store seed phrases, private keys, or wallet credentials in the skill config. <br>


## Reference(s): <br>
- [Zapper Skill Page](https://clawhub.ai/spirosrap/skills/zapper) <br>
- [Zapper Homepage](https://zapper.xyz) <br>
- [Zapper API Reference](references/api.md) <br>
- [Zapper API Docs](https://build.zapper.xyz/docs/api) <br>
- [Zapper Dashboard](https://dashboard.zapper.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, API calls, Guidance] <br>
**Output Format:** [Plain text summaries and setup guidance from shell commands that call Zapper's GraphQL API] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, python3, and a Zapper API key stored in the user's local skill config.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
