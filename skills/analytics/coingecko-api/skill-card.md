## Description:

Operate CoinGecko and GeckoTerminal market data APIs through UXC with a curated OpenAPI schema, API-key auth, and read-first guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jolestar](https://clawhub.ai/user/jolestar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to configure UXC and perform read-only CoinGecko market data and GeckoTerminal onchain queries through a curated OpenAPI surface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the skill sends requested asset IDs, token addresses, and normal API metadata to CoinGecko.

Mitigation: Confirm the user intends to query CoinGecko, keep requests narrow, and avoid submitting sensitive or unnecessary asset and address data.

Risk: The skill requires CoinGecko API-key authentication for Demo or Pro environments.

Mitigation: Use a limited CoinGecko API key, store it through the documented environment-backed credential flow, and keep Demo and Pro credentials separate.

## Reference(s):

- [Usage Patterns](references/usage-patterns.md)
- [Curated OpenAPI Schema](references/coingecko-market.openapi.json)
- [CoinGecko API Docs](https://docs.coingecko.com/reference/endpoint-overview)
- [CoinGecko Authentication Docs](https://docs.coingecko.com/reference/authentication)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and API operation examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces read-only market data guidance and UXC command patterns; API responses are expected as JSON envelopes.]

## Skill Version(s):

1.0.0 (source: server release metadata and OpenAPI schema)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
