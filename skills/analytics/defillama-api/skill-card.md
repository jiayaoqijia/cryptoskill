## Description: <br>
Operate DefiLlama public analytics APIs through UXC with a curated OpenAPI schema and read-first guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to inspect and run read-only DefiLlama public analytics operations for protocol TVL, per-protocol details, and chain overview data through UXC. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill links a local CLI command to a GitHub-hosted OpenAPI schema source. <br>
Mitigation: Confirm trust in UXC and the referenced schema source before use, and remove the created CLI link when it is no longer needed. <br>
Risk: The curated schema covers only selected read-only endpoints on api.llama.fi. <br>
Mitigation: Use the documented operations for protocol and chain reads, and choose a separate DefiLlama skill or API surface for Pro, wallet, trading, admin, coins, or yields workflows. <br>
Risk: Automation that parses free-text output can mis-handle API responses. <br>
Mitigation: Keep automation on the JSON output envelope and parse stable fields such as ok, kind, protocol, data, and error. <br>


## Reference(s): <br>
- [Usage patterns](references/usage-patterns.md) <br>
- [Curated OpenAPI schema](references/defillama-public.openapi.json) <br>
- [DefiLlama API docs](https://defillama.com/docs/api) <br>
- [Hosted curated schema source](https://raw.githubusercontent.com/holon-run/uxc/main/skills/defillama-openapi-skill/references/defillama-public.openapi.json) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only public DefiLlama API operations; no authentication required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and OpenAPI info.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
