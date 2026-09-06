## Description:

Query Polymarket prediction market data via The Graph subgraphs and Polymarket REST APIs for market search, live prices, on-chain analytics, trader P&L, open interest, resolution status, and CLOB V2 builder attribution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paulieb14](https://clawhub.ai/user/paulieb14)

### License/Terms of Use:

MIT

## Use Case:

Developers and external agent users use this MCP server to give agents read-only access to Polymarket market discovery, live CLOB prices, order books, subgraph analytics, trader profiles, P&L, open interest, and resolution data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional HTTP/SSE mode is unauthenticated, so anyone who can reach the port can call tools and consume the user's GRAPH_API_KEY quota.

Mitigation: Prefer the default stdio transport for local agents; if HTTP/SSE is enabled, bind it to localhost or protect it with firewalling, TLS, and authentication through a reverse proxy.

Risk: Subgraph tools send GRAPH_API_KEY to The Graph gateway.

Mitigation: Provide the key only through the GRAPH_API_KEY environment variable and avoid exposing HTTP/SSE endpoints to untrusted clients.

Risk: The skill returns market, price, trader, P&L, and resolution data that may be stale or incomplete when upstream subgraphs lag or are unavailable.

Mitigation: Use freshness and status tools before relying on current values, and treat returned data as analytical context rather than trading or financial advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paulieb14/skills/graph-polymarket-mcp)
- [npm package](https://www.npmjs.com/package/graph-polymarket-mcp)
- [MCP Registry entry](https://registry.modelcontextprotocol.io/v0.1/servers?search=io.github.PaulieB14/graph-polymarket-mcp)
- [Smithery server page](https://smithery.ai/servers/paulieb14/graph-polymarket-mcp)
- [Glama server page](https://glama.ai/mcp/servers/@PaulieB14/graph-polymarket-mcp)
- [The Graph Studio](https://thegraph.com/studio/)
- [Polymarket](https://polymarket.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [MCP text responses containing JSON-formatted market, pricing, order book, subgraph, trader, and resolution data, plus setup guidance in Markdown and shell/configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only data access; subgraph tools require GRAPH_API_KEY, while Polymarket REST tools do not require credentials.]

## Skill Version(s):

2.1.2 (source: SKILL.md frontmatter, package.json, and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
