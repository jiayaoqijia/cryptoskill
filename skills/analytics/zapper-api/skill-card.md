## Description: <br>
Query DeFi portfolios, token holdings, NFTs, transactions, and prices via Zapper API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zivhm](https://clawhub.ai/user/zivhm) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to ask an agent for wallet portfolio summaries, token holdings, DeFi positions, NFT holdings, token prices, claimable rewards, and recent transaction history through Zapper's API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Zapper API key and may read that key from the ZAPPER_API_KEY environment variable or ~/.config/zapper/addresses.json. <br>
Mitigation: Keep the API key and local config file private, avoid committing them, and use environment or file permissions appropriate for secrets. <br>
Risk: Wallet addresses, labels, portfolio requests, NFT requests, and transaction-history requests are sent to Zapper as part of normal operation. <br>
Mitigation: Query only addresses you are comfortable associating with your Zapper API usage and local agent session, and use wallet labels carefully. <br>
Risk: Returned balances, NFT valuations, token prices, and transaction summaries depend on Zapper API availability, rate limits, and data freshness. <br>
Mitigation: Treat results as informational, avoid rapid repeated requests, and verify important financial decisions against authoritative sources. <br>


## Reference(s): <br>
- [Zapper GraphQL API Reference](references/API.md) <br>
- [Zapper API Documentation](https://build.zapper.xyz/docs/api/) <br>
- [Zapper Developer Dashboard](https://zapper.xyz/developers) <br>
- [Zapper Homepage](https://zapper.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and optional raw JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and a ZAPPER_API_KEY or local Zapper config file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
