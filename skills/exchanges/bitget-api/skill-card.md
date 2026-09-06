## Description: <br>
Operate Bitget public exchange market APIs through UXC with a curated OpenAPI schema, market-first discovery, and explicit private-auth boundary notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect and run read-only Bitget public spot market-data requests for symbols, tickers, candles, and order book snapshots. It is scoped away from private account access, order placement, and other authenticated trading workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates a reusable UXC link and depends on a referenced remote OpenAPI schema. <br>
Mitigation: Install only when UXC and the schema source are trusted, and inspect operation help before execution. <br>
Risk: Adding credentials, private endpoints, or trading actions would exceed the reviewed public-read scope. <br>
Mitigation: Keep usage to the documented public GET market-data operations unless a separate Bitget signing and authentication flow is reviewed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jolestar/bitget-openapi-skill) <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [Curated Bitget V2 OpenAPI Schema](references/bitget-v2.openapi.json) <br>
- [Official Bitget API Intro](https://www.bitget.com/api-doc/common/intro) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands; API responses are JSON envelopes from UXC.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only public market-data operations; no credentials are required for the documented endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
