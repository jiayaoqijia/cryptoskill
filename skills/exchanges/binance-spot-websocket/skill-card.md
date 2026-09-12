## Description:

Subscribe to Binance Spot public market streams through UXC raw WebSocket support for trades, book ticker, depth, and ticker events with stream-specific guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to subscribe to Binance Spot public market data streams, inspect runtime status, and write event output to local NDJSON sinks without using private account or signed API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Public market data subscriptions can keep consuming network bandwidth and disk space while writing NDJSON files locally.

Mitigation: Confirm sink paths before subscribing, monitor subscription status, and stop jobs when finished.

Risk: The skill is scoped to public read-only Binance Spot streams and does not support private account, order, signed WebSocket, REST, margin, wallet, or futures workflows.

Mitigation: Keep usage limited to documented public stream endpoints and review outputs before adapting them to other Binance product families.

## Reference(s):

- [Usage Patterns](references/usage-patterns.md)
- [Binance Spot WebSocket Streams](https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams)
- [ClawHub Skill Page](https://clawhub.ai/jolestar/skills/binance-spot-websocket-skill)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and endpoint examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public market stream guidance only; output may include local NDJSON sink paths for persistent event storage.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
