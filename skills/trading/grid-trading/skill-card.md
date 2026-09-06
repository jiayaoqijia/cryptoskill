## Description: <br>
Create and manage grid trading strategies with OpenMM. Automated buy/sell around center price. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adacapo21](https://clawhub.ai/user/adacapo21) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to configure and run OpenMM grid-trading strategies on supported crypto exchanges, including dry runs, balance checks, and risk controls before placing live orders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automate crypto trading and place real exchange orders. <br>
Mitigation: Run in dry-run mode first, start with small sizes and conservative limits, and monitor the bot while it is running. <br>
Risk: Live exchange use requires API credentials. <br>
Mitigation: Use trade-only exchange API keys with withdrawals disabled and provide only the exchange key needed for the selected exchange. <br>
Risk: Grid trading can perform poorly in strong trends, low-liquidity markets, or high-fee environments. <br>
Mitigation: Check balances, current price, exchange minimum order values, fees, and market conditions before enabling live trading. <br>


## Reference(s): <br>
- [OpenMM Grid Trading on ClawHub](https://clawhub.ai/adacapo21/openmm-grid-trading) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides OpenMM command usage, exchange selection, grid parameters, dry runs, and risk controls.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
