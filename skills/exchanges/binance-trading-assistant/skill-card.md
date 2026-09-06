## Description: <br>
Monitor Binance spot and futures balances, open positions with P&L, portfolio performance, and price alert requests through an AI assistant. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dagangtj](https://clawhub.ai/user/dagangtj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Crypto traders and developers use this skill to let an AI assistant query Binance balances, futures positions, P&L, and portfolio information from a configured Binance account. It is intended for account monitoring and read-only reporting, not placing trades. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive Binance API credentials and account data, including balances, futures positions, and P&L. <br>
Mitigation: Use read-only API keys with withdrawals and trading disabled, protect local secret storage, rotate keys periodically, and consider Binance IP allowlisting. <br>
Risk: Balance and position details may appear in command output or agent logs. <br>
Mitigation: Run the skill only in trusted agent sessions and avoid sharing transcripts or logs that contain account details. <br>
Risk: The security evidence says the release under-discloses credential and account-data handling. <br>
Mitigation: Review the artifact scripts and data handling before installation, and disclose local credential paths and account data exposure to users before use. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/dagangtj/binance-trading-assistant) <br>
- [Publisher profile](https://clawhub.ai/user/dagangtj) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [JSON command output and concise natural-language responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Binance balances, futures positions, unrealized P&L, and credential setup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
