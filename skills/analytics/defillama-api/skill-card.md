## Description:

Operate DefiLlama public analytics APIs through UXC with a curated OpenAPI schema and read-first guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to inspect and execute read-only DefiLlama public protocol and chain analytics operations through UXC. It supports protocol TVL lists, per-protocol details, and chain overview reads without authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup flow references an external OpenAPI schema URL that can change over time.

Mitigation: Prefer the bundled schema or a schema URL pinned to a specific commit before installation or automation.

Risk: Users may mistake the skill for wallet, trading, admin, or authenticated DefiLlama Pro tooling.

Mitigation: Keep use limited to unauthenticated, read-only public analytics operations on api.llama.fi.

## Reference(s):

- [Usage Patterns](references/usage-patterns.md)
- [Curated OpenAPI Schema](references/defillama-public.openapi.json)
- [DefiLlama API Documentation](https://defillama.com/docs/api)
- [Skill Page](https://clawhub.ai/jolestar/skills/defillama-openapi-skill)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown with inline shell commands and JSON-oriented API usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance is scoped to public read-only DefiLlama endpoints on api.llama.fi and favors stable JSON output handling.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
