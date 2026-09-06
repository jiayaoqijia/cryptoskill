## Description: <br>
Operate DefiLlama public price APIs through UXC with a curated OpenAPI schema and read-first guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect and execute read-only DefiLlama current price lookups for one or more public asset identifiers through UXC and OpenAPI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on UXC and a referenced OpenAPI schema to issue public network reads. <br>
Mitigation: Install only when UXC and the schema source are trusted, and review generated commands before execution. <br>
Risk: Price data from the public DefiLlama endpoint may be unavailable, stale, or unsuitable as sole decision support. <br>
Mitigation: Use narrow read validation first and cross-check important financial or operational decisions against additional sources. <br>
Risk: The workflow does not require credentials, wallet secrets, or private local data. <br>
Mitigation: Do not provide API keys, wallet secrets, or private files when using this read-only price lookup skill. <br>


## Reference(s): <br>
- [Usage patterns](references/usage-patterns.md) <br>
- [Curated OpenAPI schema](references/defillama-prices.openapi.json) <br>
- [DefiLlama API docs](https://defillama.com/docs/api) <br>
- [Curated schema source URL](https://raw.githubusercontent.com/holon-run/uxc/main/skills/defillama-prices-openapi-skill/references/defillama-prices.openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, API Calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only DefiLlama price queries; no authentication required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and OpenAPI schema) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
