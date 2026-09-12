## Description:

Operate Alchemy Prices API reads through UXC with a curated OpenAPI schema, path-templated API-key auth, and read-first guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure UXC and run read-only Alchemy Prices API requests for token price lookup by symbol, contract address, or historical range.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Alchemy API key is placed in the request path for this API surface.

Mitigation: Use environment-backed or secret-store-backed credentials such as ALCHEMY_API_KEY and avoid entering API keys as shell history literals.

Risk: Historical price requests can expand into larger backfills than intended.

Mitigation: Keep historical time windows tight unless a larger range is explicitly needed.

Risk: Users may overextend the skill beyond its intended Alchemy Prices API scope.

Mitigation: Treat the skill as read-only and prices-only; do not use it for node RPC, NFT, portfolio, trade execution, or wallet mutation workflows.

## Reference(s):

- [Usage patterns](references/usage-patterns.md)
- [Curated OpenAPI schema](references/alchemy-prices.openapi.json)
- [Alchemy Prices API docs](https://www.alchemy.com/docs/reference/prices-api)
- [Prices API endpoints](https://www.alchemy.com/docs/reference/prices-api-endpoints)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance centers on read-only API calls and stable JSON response fields.]

## Skill Version(s):

1.0.0 (source: server release metadata and OpenAPI info.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
