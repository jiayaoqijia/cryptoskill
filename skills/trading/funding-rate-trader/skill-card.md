## Description: <br>
Funding Rate Trader scans crypto funding rates for Binance Futures opportunities without an API key and can run a Binance API-backed trader with configurable stop-loss and take-profit controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dagangtj](https://clawhub.ai/user/dagangtj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to scan Binance Futures funding rates, identify negative-rate opportunities, monitor open positions, and optionally run automated leveraged trades through a Binance API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running trader.js can place live leveraged Binance Futures trades with stored API keys without a dry run or confirmation gate. <br>
Mitigation: Require an explicit dry-run or manual confirmation step before live trading, and review leverage, order size, and symbol selection before execution. <br>
Risk: Stored Binance API credentials could expose the account to trading activity if mishandled. <br>
Mitigation: Use a dedicated API key with withdrawals disabled, minimal permissions, IP restrictions, strict local file permissions, and small exchange-side risk limits. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dagangtj/funding-rate-trader) <br>
- [Binance Futures premium index endpoint](https://fapi.binance.com/fapi/v1/premiumIndex) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May also run Node.js scripts that call Binance Futures APIs and print tabular console output.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
