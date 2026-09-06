## Description: <br>
Operate Alchemy Prices API reads through UXC with a curated OpenAPI schema, path-templated API-key auth, and read-first guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jolestar](https://clawhub.ai/user/jolestar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure an agent for read-only Alchemy Prices API calls through UXC, including token price lookup by symbol or contract address and historical price requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Alchemy API keys are sensitive and this integration places the key in the request path. <br>
Mitigation: Use UXC secret-backed credentials such as ALCHEMY_API_KEY, avoid literal secrets in shell history or logs, and verify the auth binding after setup. <br>
Risk: The referenced OpenAPI schema URL points at a mutable main-branch location. <br>
Mitigation: Prefer a bundled or pinned schema copy when repeatability matters. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jolestar/alchemy-openapi-skill) <br>
- [Usage patterns](references/usage-patterns.md) <br>
- [Curated OpenAPI schema](references/alchemy-prices.openapi.json) <br>
- [Alchemy Prices API docs](https://www.alchemy.com/docs/reference/prices-api) <br>
- [Alchemy Prices API endpoints](https://www.alchemy.com/docs/reference/prices-api-endpoints) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides read-only API calls and expects JSON API responses from UXC-managed commands.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
