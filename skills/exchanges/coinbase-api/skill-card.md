## Description:

Operate Coinbase Advanced Trade REST APIs through UXC with a curated OpenAPI schema, products-first discovery, and explicit JWT bearer auth guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to discover Coinbase Advanced Trade products, inspect account and order data, and execute selected order workflows through UXC. It is intended for agents that need structured Coinbase API guidance with explicit authentication and write-operation guardrails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide live Coinbase order creation and cancellation.

Mitigation: Use read-only Coinbase credentials for discovery and require explicit review of exact order or cancellation parameters before any write operation.

Risk: Trading-enabled API credentials may allow unintended financial actions.

Mitigation: Avoid trading-enabled keys unless live order placement is intended, and scope credentials as narrowly as Coinbase allows.

Risk: A mutable remote schema URL can change behavior after installation.

Mitigation: Use the bundled OpenAPI schema or another pinned schema reference instead of a mutable main-branch URL.

## Reference(s):

- [Usage Patterns](references/usage-patterns.md)
- [Curated Coinbase Advanced Trade OpenAPI Schema](references/coinbase-advanced-trade.openapi.json)
- [Coinbase Advanced Trade API Overview](https://docs.cdp.coinbase.com/coinbase-app/advanced-trade-apis/overview)
- [ClawHub Skill Page](https://clawhub.ai/jolestar/skills/coinbase-openapi-skill)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, text]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance emphasizes stable JSON output envelopes and narrow Coinbase product, account, and order queries.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
