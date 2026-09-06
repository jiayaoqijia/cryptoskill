## Description: <br>
Subscribe to OKX public exchange WebSocket channels through UXC raw WebSocket mode for ticker, trade, book, and candle events with explicit subscribe frames. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to prepare UXC raw WebSocket subscription commands for OKX public market-data channels and inspect the resulting NDJSON event stream. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Subscriptions can keep a network connection open and continue growing local output files. <br>
Mitigation: Choose sink paths intentionally, monitor subscription status, and stop jobs when finished. <br>
Risk: Using an untrusted local UXC binary or mixing this public-channel workflow with private trading flows could create operational risk. <br>
Mitigation: Trust the local UXC installation before use and keep this skill limited to OKX public market-data endpoints and subscribe frames. <br>


## Reference(s): <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [OKX WebSocket API](https://www.okx.com/docs-v5/en/) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces commands and subscribe frames for public OKX WebSocket channels; sink output is NDJSON when executed through UXC.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
