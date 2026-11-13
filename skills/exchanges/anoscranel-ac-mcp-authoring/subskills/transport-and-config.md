---
name: transport-and-config
domain: software-engineering/mcp-authoring
trigger: "Configuring MCP transport layers; setting up stdio versus HTTP streaming; managing server configuration and environment"
anti_trigger: "Designing tool schemas (subskills/tool-design.md); auditing server security (subskills/security-model.md)"
scope: "Selecting and configuring MCP transport layers including local stdio and remote HTTP streaming, session lifecycles, and environment wiring"
status: seedling
---

# Transport and Config

## Standard

- **Model Context Protocol Transport Specification**: standardizing communication channels across local process pipes and remote HTTP streams. <https://modelcontextprotocol.io>
- **JSON-RPC Over HTTP Guidelines**: structuring streamable message payloads for remote client-server connectivity. <https://www.jsonrpc.org/specification>
- ⚠️ Stdio transports require strict stdout hygiene; any stray logging printed to stdout corrupts the JSON-RPC message stream.

## Decision rules

1. If the MCP server runs locally as a companion process to the client host, use stdio transport for maximum simplicity and zero network overhead.
2. If the server operates remotely across network boundaries, use streamable HTTP transports with appropriate connection pooling.
3. If logging debug messages during stdio transport, direct all logs exclusively to stderr to protect the stdout JSON-RPC channel.
4. If configuring server parameters, load all runtime secrets and connection strings from environment variables rather than hardcoded files.
5. If session lifecycles time out under heavy load, implement robust keep-alive pings and automatic reconnection logic.
6. ⚠️ Never output unformatted stack traces or debugging banners to standard output when running on stdio transport.

## Procedure

1. Choose the appropriate transport layer based on deployment topology (stdio for local, HTTP for remote).
2. Configure standard input and output streams for stdio servers, ensuring all logging is redirected to stderr.
3. Set up HTTP server routing and streamable endpoints for remote transport configurations.
4. Implement connection initialization and session management handlers to track active client states.
5. Load configuration options and environment variables securely at startup.
6. Test transport stability under simulated network latency and process interruption conditions.

## Anti-patterns

- **Logging to stdout on stdio transport.** Printing debug statements that corrupt the JSON-RPC message framing. Fix: route all logs to stderr.
- **Hardcoding connection parameters.** Embedding ports, hostnames, or credentials directly in source code. Fix: use environment configuration.
- **Neglecting session cleanup.** Leaving stale sessions open indefinitely without resource reclamation. Fix: implement timeout handlers.
- **Ignoring transport errors.** Failing to handle sudden pipe closures or network disconnects gracefully. Fix: add robust error recovery.

## Done checklist

- [ ] Transport layer is correctly chosen (stdio for local, HTTP for remote).
- [ ] Stdio stdout is strictly reserved for clean JSON-RPC messaging; logs go to stderr.
- [ ] Environment variables handle runtime configuration securely.
- [ ] Session lifecycles and timeouts are managed effectively.
- [ ] Transport error handling recovers gracefully from unexpected disconnections.

## Sources

- Model Context Protocol Transport Specification: <https://modelcontextprotocol.io>
- JSON-RPC Over HTTP Guidelines: <https://www.jsonrpc.org/specification>
