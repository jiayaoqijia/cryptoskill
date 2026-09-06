## Description: <br>
Operate DefiLlama public yield APIs through UXC with a curated OpenAPI schema and read-first guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover public DefiLlama yield pools and retrieve per-pool chart history through UXC using a curated read-only OpenAPI schema. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow depends on trusting UXC and a remote OpenAPI schema URL. <br>
Mitigation: Confirm trust in UXC and verify or pin the OpenAPI schema before linking it in stricter supply-chain environments. <br>


## Reference(s): <br>
- [Usage Patterns](references/usage-patterns.md) <br>
- [Curated OpenAPI Schema](references/defillama-yields.openapi.json) <br>
- [DefiLlama API Docs](https://defillama.com/docs/api) <br>
- [ClawHub Skill Page](https://clawhub.ai/jolestar/defillama-yields-openapi-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON API responses from the linked CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only public API access; no authentication required; keep automation on the JSON output envelope.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and OpenAPI schema) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
