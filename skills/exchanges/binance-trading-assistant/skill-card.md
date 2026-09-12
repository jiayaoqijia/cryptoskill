## Description:

Monitor Binance spot and futures balances, open positions with P&L, portfolio performance, and price alerts through an AI assistant.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dagangtj](https://clawhub.ai/user/dagangtj)

### License/Terms of Use:

MIT-0

## Use Case:

External crypto traders use this skill to check Binance account balances, review futures positions and unrealized P&L, and monitor portfolio status from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles high-value Binance API credentials and account data.

Mitigation: Use a dedicated API key with withdrawals disabled, read-only permissions where possible, IP restrictions, and strong local file protection.

Risk: The documentation claims keys and data stay local, but the scripts make authenticated Binance API calls and print account data for assistant consumption.

Mitigation: Treat Binance balances and positions as sensitive data, review assistant logs and sharing settings, and correct the safety documentation before broad deployment.

Risk: The exchange dependency is unpinned.

Mitigation: Pin and review the ccxt dependency before installation or production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dagangtj/skills/binance-trading-assistant)
- [Publisher Profile](https://clawhub.ai/user/dagangtj)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance and JSON command output from Binance account-check scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces account balances, futures position summaries, timestamps, and unrealized P&L for assistant consumption.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
