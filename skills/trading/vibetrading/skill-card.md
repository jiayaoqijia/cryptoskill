## Description: <br>
Build, backtest, and deploy cryptocurrency trading strategies using the vibetrading Python framework. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crabbytt](https://clawhub.ai/user/crabbytt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and trading agents use this skill to generate, validate, backtest, compare, and deploy crypto trading strategies within the vibetrading framework. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated strategies or live-trading examples can place real crypto trades using private keys. <br>
Mitigation: Start with backtests or testnet/paper trading, manually review generated strategy logic, and deploy only with explicit position and loss limits. <br>
Risk: Exchange credentials and private keys may be exposed if copied into chat, code, or repositories. <br>
Mitigation: Keep secrets out of chat and source control, store them in local environment files, and use least-privilege, low-balance accounts. <br>
Risk: The external vibetrading package controls backtesting and live-trading behavior. <br>
Mitigation: Verify the package and its dependencies before installation, then test behavior in an isolated environment before any funded deployment. <br>


## Reference(s): <br>
- [vibetrading API Details](references/api-details.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python code snippets, shell commands, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include strategy code, backtest instructions, live deployment setup, credential handling guidance, and risk controls.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
