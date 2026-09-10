## Description:

Build, backtest, and deploy cryptocurrency trading strategies using the vibetrading Python framework.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crabbytt](https://clawhub.ai/user/crabbytt)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to generate Python crypto trading strategies, backtest them on historical data, compare performance, and prepare deployments for supported live exchanges. It is limited to the vibetrading framework and crypto trading workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports ready-to-run live crypto trading, which can place real orders and cause financial losses.

Mitigation: Review generated strategies before use, start with paper trading or testnet where possible, and run live examples only when intending to trade and accepting possible losses.

Risk: Exchange credentials and private keys may be needed for live deployment.

Mitigation: Use least-privilege exchange keys with withdrawals disabled, keep secrets out of chat, logs, and source control, and prefer isolated environments.

Risk: Package or environment changes can affect strategy execution and trading behavior.

Mitigation: Use a virtual environment or container and pin package versions before backtesting or deployment.

## Reference(s):

- [vibetrading API Details](references/api-details.md)
- [ClawHub Skill Page](https://clawhub.ai/crabbytt/skills/vibetrading)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include trading strategy code, backtest setup, live exchange configuration guidance, and risk-management checks.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
