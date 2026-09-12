## Description:

Operate KuCoin public exchange market APIs through UXC with a curated OpenAPI schema, market-first discovery, and explicit private-auth boundary notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to inspect and run read-only KuCoin public market-data operations, including symbol discovery, tickers, order book snapshots, and candlestick reads. It is intended for public data workflows that do not require KuCoin private account credentials or order execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can reference a remote OpenAPI schema URL, which may create supply-chain integrity risk if strict reproducibility is required.

Mitigation: Use the bundled reviewed OpenAPI schema or a pinned commit URL for workflows that require strict integrity.

Risk: Adding private KuCoin credentials would exceed the reviewed v1 public-data scope.

Mitigation: Keep this release limited to public market-data reads and do not add private credentials or signing flows.

## Reference(s):

- [Usage Patterns](references/usage-patterns.md)
- [Curated OpenAPI Schema](references/kucoin-public.openapi.json)
- [KuCoin Authentication Documentation](https://www.kucoin.com/docs-new/authentication)
- [KuCoin Public API Server](https://api.kucoin.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with inline shell commands and JSON API responses from UXC]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public market-data operations; no private credentials required or supported in v1.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
