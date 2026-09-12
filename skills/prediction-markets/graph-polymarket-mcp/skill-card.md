## Description:

Query Polymarket prediction market data via The Graph subgraphs and Polymarket REST APIs for market search, live prices, order books, on-chain analytics, trader P&L, open interest, resolution status, and CLOB V2 builder attribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paulieb14](https://clawhub.ai/user/paulieb14)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this MCP server to let agents inspect Polymarket prediction markets, live CLOB data, trader analytics, open interest, and market resolution data. Subgraph tools require a Graph API key; REST market and price tools use public Polymarket endpoints without an API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional HTTP/SSE transport can expose unauthenticated tools to reachable clients.

Mitigation: Prefer stdio/local use. If HTTP/SSE is required, bind or firewall it to trusted clients and place authentication and TLS in front of any reachable endpoint.

Risk: Remote callers that can reach HTTP/SSE endpoints can consume the configured Graph API quota.

Mitigation: Limit network exposure, monitor usage, and use a pinned package version in client configuration.

Risk: The server uses a Graph API key for subgraph queries.

Mitigation: Provide GRAPH_API_KEY only in trusted runtime environments and avoid forwarding it outside gateway.thegraph.com.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paulieb14/skills/graph-polymarket-mcp)
- [ClawHub publisher profile](https://clawhub.ai/user/paulieb14)
- [npm package](https://www.npmjs.com/package/graph-polymarket-mcp)
- [MCP Registry entry](https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.PaulieB14/graph-polymarket-mcp)
- [Smithery server page](https://smithery.ai/servers/paulieb14/graph-polymarket-mcp)
- [Glama server page](https://glama.ai/mcp/servers/@PaulieB14/graph-polymarket-mcp)
- [The Graph Studio](https://thegraph.com/studio/)
- [Polymarket](https://polymarket.com/)
- [The Graph](https://thegraph.com/)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown and structured MCP tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >= 18. GRAPH_API_KEY is required for The Graph subgraph tools; public Polymarket REST tools do not require credentials.]

## Skill Version(s):

2.1.2 (source: SKILL.md frontmatter, package.json, ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
