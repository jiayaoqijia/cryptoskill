---
name: protocol-model
domain: software-engineering/mcp-authoring
trigger: "Explaining the Model Context Protocol architecture; deciding between tools, resources, and prompts; structuring a server versus a library"
anti_trigger: "Writing JSON schemas for tools (subskills/tool-design.md); configuring transport layers (subskills/transport-and-config.md)"
scope: "Establishing the foundational architecture of MCP servers, client-server handshake, capability negotiation, and the three primitive categories"
status: seedling
---

# Protocol Model

## Standard

- **Model Context Protocol Specification**: standardizing how clients connect to servers and exchange capabilities. <https://modelcontextprotocol.io>
- **JSON-RPC 2.0 Specification**: the foundational messaging protocol underlying MCP request, notification, and response frames. <https://www.jsonrpc.org/specification>
- ⚠️ Transport layers and capability negotiation identifiers evolve across protocol drafts; always verify active spec versions against official documentation.

## Decision rules

1. If the client needs to trigger side effects or write data, expose it as a tool, never as a resource.
2. If data is read-only reference material without side effects, expose it as a resource using standard URI schemes.
3. If a workflow requires parameterized text templates for agent context injection, use prompts rather than hardcoding strings.
4. If business logic is self-contained without external client-host integration, implement it as a plain library before wrapping in MCP.
5. If capability negotiation fails during initialization, reject the connection cleanly rather than operating with degraded assumptions.
6. ⚠️ Every MCP server must implement initialization handshakes correctly within the timeout window defined by the client runtime.

## Procedure

1. Define the boundary between your core application library and the MCP server wrapper layer.
2. Implement the initialization handler to exchange server capabilities and protocol version metadata during connection startup.
3. Classify all domain operations into the three core primitives: tools for actions, resources for read-only data, and prompts for guidance.
4. Set up asynchronous request handlers to process JSON-RPC messages and return structured responses or standard error objects.
5. Verify client capability declarations before serving specialized resources or accepting advanced tool calls.
6. Handle client disconnect and teardown signals gracefully to release underlying database connections and worker threads.

## Anti-patterns

- **God-server pattern.** Bundling unrelated domains and databases into a single monolithic MCP server. Fix: modularize servers by business domain.
- **Tools for reading static data.** Using tool calls to fetch static documentation instead of URI-addressable resources. Fix: map static files to resources.
- **Ignoring capability negotiation.** Assuming all clients support advanced streaming features without checking initialization parameters. Fix: validate capabilities on connect.
- **Tight coupling to host application.** Embedding MCP protocol code directly inside core domain logic instead of a thin wrapper layer. Fix: maintain a strict boundary.

## Done checklist

- [ ] Core architecture separates domain logic from the MCP server wrapper layer.
- [ ] Initialization handshake correctly exchanges protocol versions and capabilities.
- [ ] Domain operations are accurately mapped across tools, resources, and prompts.
- [ ] JSON-RPC message handlers return valid responses or standard error payloads.
- [ ] Connection teardown and resource release are handled cleanly.

## Sources

- Model Context Protocol Specification: <https://modelcontextprotocol.io>
- JSON-RPC 2.0 Specification: <https://www.jsonrpc.org/specification>
