## Description:

Gate Exchange Assets helps agents answer read-only Gate account balance, total asset, and coin holding questions across spot, margin, futures, options, earn, TradFi, wallet, and related account areas.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gate-exchange](https://clawhub.ai/user/gate-exchange)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve read-only Gate asset overviews, account-specific balances, and specific coin holdings through a configured Gate MCP session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad financial account data may be read across Gate account areas, even for narrow or ambiguous balance prompts.

Mitigation: Use tightly scoped read-only API keys and clarify ambiguous account, currency, or scope requests before querying balances.

Risk: Gate API credentials are required for account-level reads.

Mitigation: Use the configured MCP session and do not ask users to paste API keys or secrets into chat.

Risk: Partial MCP failures can produce incomplete asset views.

Mitigation: Mark degraded or unavailable account modules explicitly and do not infer hidden balances.

Risk: Trading, transfer, or other account mutations are outside this skill's read-only scope.

Mitigation: Do not call write tools; route trading or transfer intents to an appropriate separate workflow.

## Reference(s):

- [Gate Exchange Assets Runtime Rules](references/gate-runtime-rules.md)
- [Gate Assets MCP Specification](references/mcp.md)
- [Gate Skills Homepage](https://github.com/gate/gate-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown balance summaries with account and valuation details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only balance snapshots; missing or failed account modules should be marked as degraded.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata; artifact frontmatter version 2026.4.8-1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
