## Description:

Operate DefiLlama public price APIs through UXC with a curated OpenAPI schema and read-first guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to inspect and run read-only DefiLlama current price lookups for one or more assets through a curated OpenAPI interface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates or uses a UXC CLI link and reaches public network endpoints for DefiLlama price data.

Mitigation: Install only when public network access to coins.llama.fi and the referenced schema URL is acceptable.

Risk: Price responses may be unsuitable as the sole basis for financial decisions.

Mitigation: Use the returned data as one input and verify critical prices against authoritative or redundant sources before acting.

## Reference(s):

- [DefiLlama Prices OpenAPI schema](references/defillama-prices.openapi.json)
- [Usage patterns](references/usage-patterns.md)
- [DefiLlama API docs](https://defillama.com/docs/api)
- [ClawHub skill page](https://clawhub.ai/jolestar/skills/defillama-prices-openapi-skill)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public price lookups; no authentication required.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
