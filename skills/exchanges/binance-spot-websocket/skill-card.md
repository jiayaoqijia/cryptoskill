## Description: <br>
Subscribe to Binance Spot public market streams through UXC raw WebSocket support for trades, book ticker, depth, and ticker events with stream-specific guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to subscribe agents to public Binance Spot market-data streams, persist events to NDJSON sinks, and inspect or stop subscription jobs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a local `uxc` binary and starts network subscription jobs. <br>
Mitigation: Use a trusted `uxc` installation, confirm the endpoint is a public Binance Spot stream, and stop subscription jobs when finished. <br>
Risk: Streaming market data can create growing NDJSON sink files. <br>
Mitigation: Choose a writable sink location with adequate storage and monitor or rotate output files during long-running subscriptions. <br>
Risk: Using this skill outside public market-data streams could imply unsupported account or trading workflows. <br>
Mitigation: Keep usage read-only and do not use it for private user data streams, signed WebSocket methods, account access, or order placement. <br>


## Reference(s): <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [Binance Spot WebSocket Streams](https://developers.binance.com/docs/binance-spot-api-docs/web-socket-streams) <br>
- [ClawHub Skill Page](https://clawhub.ai/jolestar/binance-spot-websocket-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and WebSocket endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance is scoped to public read-only Binance Spot streams and sink-based NDJSON event handling.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
