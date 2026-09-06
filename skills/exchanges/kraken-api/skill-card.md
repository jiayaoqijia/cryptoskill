## Description: <br>
Operate Kraken public market APIs through UXC with a curated OpenAPI schema, market-first discovery, and explicit private-auth boundary notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to inspect and run Kraken public market-data operations through UXC, including server time, asset pairs, ticker reads, OHLC candles, and order book snapshots. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is documented as public Kraken market data, but it ships a separate schema containing private account and live trading operations. <br>
Mitigation: Use only the public OpenAPI schema for this release, and remove the private/trading schema or split it into a clearly named trading skill. <br>
Risk: Agent environments with access to Kraken API credentials could use private or trading operations if the broader schema is exposed. <br>
Mitigation: Require explicit user confirmation and least-privilege credential guidance before any private or trading workflow is enabled. <br>


## Reference(s): <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [Curated Public OpenAPI Schema](references/kraken-public.openapi.json) <br>
- [Shipped Spot REST Schema](references/kraken-spot-futures.openapi.json) <br>
- [Official Kraken API Intro](https://docs.kraken.com/api/docs/guides/global-intro) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Public-market workflows should stay on the JSON output envelope and parse stable fields such as ok, kind, protocol, data, and error.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
