## Description:

Subscribe to OKX public exchange WebSocket channels through UXC raw WebSocket mode for ticker, trade, book, and candle events with explicit subscribe frames.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to subscribe agents to OKX public market-data WebSocket channels and inspect ticker, trade, book, and candle events written to NDJSON sinks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A running public market-data subscription can continue writing NDJSON records and grow local disk usage.

Mitigation: Choose an appropriate sink path, monitor output size, and stop the subscription when finished.

Risk: Adapting this public-channel workflow to private authentication or trading could introduce credential and transaction risk outside the reviewed scope.

Mitigation: Keep usage limited to public OKX WebSocket channels unless a separate review covers private login, trading, account, or order-management workflows.

## Reference(s):

- [Usage Patterns](references/usage-patterns.md)
- [OKX WebSocket API](https://www.okx.com/docs-v5/en/)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON subscribe frames]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides public OKX market-data subscriptions that write NDJSON sink files; excludes private authentication, trading, account, order-management, and REST workflows.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
