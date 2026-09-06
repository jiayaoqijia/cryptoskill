## Description: <br>
Query Hyperliquid DEX for account balances, positions, PnL, and margin data via ClawdBot API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Chipagosfinest](https://clawhub.ai/user/Chipagosfinest) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to query public Hyperliquid wallet account data, including balances, open perpetual positions, unrealized PnL, margin usage, leverage, and liquidation prices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried wallet addresses and returned Hyperliquid balances, positions, PnL, margin, and liquidation details pass through ClawdBot's disclosed API path. <br>
Mitigation: Use only wallet addresses and account data you are comfortable sending through that API path. <br>
Risk: Private keys or signing credentials are unnecessary for this read-only lookup. <br>
Mitigation: Do not provide private keys, seed phrases, signing credentials, or trading authority to the skill. <br>


## Reference(s): <br>
- [Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs) <br>
- [Hyperliquid Public Info API](https://api.hyperliquid.xyz/info) <br>
- [ClawHub Skill Page](https://clawhub.ai/Chipagosfinest/hyperliquid-dex) <br>
- [Publisher Profile](https://clawhub.ai/user/Chipagosfinest) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown or text summaries of JSON account and position data.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only account lookup; wallet address input is optional when TRADING_WALLET_ADDRESS is configured.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
