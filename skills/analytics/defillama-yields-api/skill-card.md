## Description:

Operate DefiLlama public yield APIs through UXC with a curated OpenAPI schema and read-first guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover DefiLlama yield pools and retrieve per-pool chart history through UXC against public read-only APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: UXC creates a reusable local CLI alias and fetches the OpenAPI schema from the listed GitHub URL.

Mitigation: Review the schema URL before linking the CLI alias and keep usage limited to the documented public read-only yield endpoints.

Risk: Automation could become brittle if it relies on non-JSON output or undocumented response fields.

Mitigation: Keep automation on the JSON output envelope and parse stable fields first, including ok, kind, protocol, data, and error.

## Reference(s):

- [Usage Patterns](references/usage-patterns.md)
- [Curated OpenAPI Schema](references/defillama-yields.openapi.json)
- [DefiLlama API Docs](https://defillama.com/docs/api)
- [DefiLlama Yields API Host](https://yields.llama.fi)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, API Calls, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public DefiLlama yield queries through UXC; no credentials required.]

## Skill Version(s):

1.0.0 (source: server release evidence and OpenAPI schema)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
