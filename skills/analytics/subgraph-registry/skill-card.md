## Description:

Use to discover The Graph subgraphs by chain, protocol, entity or contract and turn a goal into a bounded GraphQL query. Bring-your-own Studio key (set up by a human operator) for execution; discovery never executes queries or signs payments, and x402 is an explicitly paid external option.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paulieb14](https://clawhub.ai/user/paulieb14)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this MCP server to discover and compare The Graph subgraphs, inspect their metadata, and prepare bounded GraphQL queries for a selected deployment. Live schema checks and query execution require an operator-configured Studio API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reports a benign verdict with medium confidence because some code analysis was incomplete; the server can make optional network requests when enabled.

Mitigation: Install the pinned 0.13.7 release and review its package and source before enabling opt-in network tools.

Risk: A configured Studio API key enables live schema, health, and query operations against The Graph gateway.

Mitigation: Have the operator store the key in the MCP host secret store; never put it in chat, tool arguments, source files, or logs.

Risk: The optional HTTP/SSE listener can expose server routes when bound beyond loopback.

Mitigation: Keep the listener on 127.0.0.1 unless remote access is needed; for a non-loopback bind, configure SUBGRAPH_REGISTRY_HTTP_TOKEN.

## Reference(s):

- [Project homepage](https://github.com/PaulieB14/subgraph-registry)
- [The Graph supported networks](https://thegraph.com/docs/en/supported-networks/)
- [The Graph Studio API keys](https://thegraph.com/studio/apikeys/)

## Skill Output:

**Output Type(s):** [JSON, GraphQL queries, Guidance]

**Output Format:** [Structured JSON tool responses with bounded GraphQL query strings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Discovery is local to the bundled registry; live schema checks and query execution require an operator-configured Studio API key.]

## Skill Version(s):

0.13.7 (source: package.json, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
