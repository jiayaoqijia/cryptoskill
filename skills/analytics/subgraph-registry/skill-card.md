## Description:

Use to discover The Graph subgraphs by chain, protocol, entity or contract and turn a goal into a bounded GraphQL query. Bring-your-own Studio key (set up by a human operator) for execution; discovery never executes queries or signs payments, and x402 is an explicitly paid external option.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paulieb14](https://clawhub.ai/user/paulieb14)

### License/Terms of Use:

MIT

## Use Case:

Developers use the MCP server to find and compare The Graph subgraphs, inspect registry metadata, and prepare bounded GraphQL queries for an intended chain or data goal. With an operator-managed Studio API key, they can opt in to live schema checks, health checks, and query execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Security scan coverage is partial: 7 of 11 components were fully scanned, and some JavaScript could not be fully interpreted.

Mitigation: Review the published package source and confirm you trust it and its documented network and environment-variable capabilities before installation.

Risk: Opt-in live query and schema tools use an operator-provided Studio API key, which could be exposed if placed in chat, tool arguments, source files, or logs.

Mitigation: Have the operator provide the key through the MCP host's secret store or process environment; never paste or log the key.

Risk: The optional HTTP/SSE listener can expose access beyond the local machine if configured to bind on a non-loopback address.

Mitigation: Keep the listener on 127.0.0.1, or configure SUBGRAPH_REGISTRY_HTTP_TOKEN before using a non-loopback bind.

Risk: An external x402 client may make paid requests, although the MCP server does not sign payments or pay automatically.

Mitigation: Use an external signing client only after the owner explicitly approves the payment amount and route.

## Reference(s):

- [Project homepage](https://github.com/PaulieB14/subgraph-registry)
- [The Graph supported networks](https://thegraph.com/docs/en/supported-networks/)
- [The Graph Studio API keys](https://thegraph.com/studio/apikeys/)

## Skill Output:

**Output Type(s):** [Text, JSON, GraphQL queries, Configuration guidance]

**Output Format:** [Structured MCP tool responses, bounded GraphQL query strings, and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Discovery and query preparation are keyless; live schema, health, and execution actions require explicit opt-in and an operator-provided Studio API key.]

## Skill Version(s):

0.13.6 (source: package.json, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
