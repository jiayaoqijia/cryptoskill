## Description: <br>
Operates Binance Web3 public market and research APIs through UXC with a curated OpenAPI schema for token search, market snapshots, address holdings, rankings, token audit, and smart money signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query Binance Web3 public data for token discovery, market research, wallet holdings, token audit, rankings, and smart-money signals without account trading access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet-address lookups can expose or aggregate public holdings for a specific address. <br>
Mitigation: Query wallet addresses only when the user clearly asks or has authority, and avoid treating address data as private user context beyond the task. <br>
Risk: Token audit, market, ranking, and smart-money data may be incomplete, stale, or misread as financial advice. <br>
Mitigation: Present results as informational research data, avoid investment recommendations, and encourage verification against authoritative market sources. <br>
Risk: Some endpoints require operation-specific details such as UUID request IDs or scoped browser-style headers. <br>
Mitigation: Inspect operation help before calling endpoints, generate a fresh UUID for each audit request, and scope required headers only to the address holdings operation. <br>


## Reference(s): <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [Curated OpenAPI Schema](references/binance-web3.openapi.json) <br>
- [Binance Web3 API Host](https://web3.binance.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/jolestar/binance-web3-openapi-skill) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only Binance Web3 public API operations; agents should parse JSON output envelopes before presenting results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
