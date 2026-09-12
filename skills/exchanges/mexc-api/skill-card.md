## Description:

Operate MEXC Spot REST APIs through UXC with a curated OpenAPI schema, HMAC query signing, and separate public/signed workflow guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect and execute MEXC Spot REST operations through UXC, starting with public market reads and escalating to signed account or order workflows only when credentials and confirmations are in place.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Connecting an agent to real MEXC Spot credentials can expose account data or enable financial actions.

Mitigation: Use API keys with the minimum required permissions, disable withdrawal and transfer permissions, and keep signed operations separate from public market reads.

Risk: Order placement or cancellation can affect a live trading account.

Mitigation: Require manual confirmation before any signed write operation and query exchange information first so symbol filters and lot sizes are known.

Risk: A mutable remote API schema can change the authenticated actions available after review.

Mitigation: Prefer the bundled schema, or use a commit-pinned and hash-verified schema before enabling signed account or order operations.

## Reference(s):

- [MEXC OpenAPI Skill on ClawHub](https://clawhub.ai/jolestar/skills/mexc-openapi-skill)
- [Usage patterns](references/usage-patterns.md)
- [Curated OpenAPI schema](references/mexc-spot.openapi.json)
- [Official MEXC Spot v3 docs](https://mexcdevelop.github.io/apidocs/spot_v3_en/)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with inline shell commands and JSON signer configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may call live MEXC Spot endpoints, including signed account reads and order create or cancel operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
