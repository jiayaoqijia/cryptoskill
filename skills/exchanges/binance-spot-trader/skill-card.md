## Description: <br>
Autonomous Binance spot trading bot with LLM-powered market analysis for momentum, mean reversion, and DCA strategies on Binance spot pairs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[srikanthbellary](https://clawhub.ai/user/srikanthbellary) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to configure and run automated Binance spot trading workflows, including technical-analysis strategies, LLM sentiment filtering, and portfolio checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place live Binance spot market orders from the configured account. <br>
Mitigation: Use a Binance sub-account, disable withdrawals, IP-restrict API keys, begin with read-only or testnet/paper trading when available, and review order limits and confirmation behavior before providing trading-enabled keys. <br>
Risk: The skill requires private Binance and LLM API credentials. <br>
Mitigation: Store credentials only in a secured environment, restrict exchange-key permissions to the minimum needed for spot trading, and do not enable withdrawal permissions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/srikanthbellary/binance-spot-trader) <br>
- [Publisher homepage](https://github.com/srikanthbellary) <br>
- [Binance REST API Reference](references/binance-api.md) <br>
- [Technical Indicators](references/indicators.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration, Code] <br>
**Output Format:** [Markdown guidance with bash commands, environment configuration, and Python script execution] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Binance and LLM API credentials; may write local trade history and logs during operation.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
