---
name: security-model
domain: software-engineering/mcp-authoring
trigger: "Securing MCP servers; implementing OAuth for HTTP transports; defending against prompt injection and privilege escalation"
anti_trigger: "Configuring server transports (subskills/transport-and-config.md); testing server contracts (subskills/testing-and-debugging.md)"
scope: "Mitigating server attack surface, HTTP authentication, tool call consent gates, prompt injection defense, and least-privilege secret management"
status: seedling
---

# Security Model

## Standard

- **OWASP Top 10 for LLM Applications**: identifying and mitigating agent-specific vulnerabilities such as prompt injection and insecure tool execution. <https://genai.owasp.org>
- **Model Context Protocol Security Guidance**: securing server endpoints, enforcing authorization, and managing credentials. <https://modelcontextprotocol.io>
- ⚠️ Tool results returned to agents can carry indirect prompt injection attacks; never treat tool outputs as trusted system instructions.

## Decision rules

1. If an MCP server exposes destructive or financial tool actions, enforce explicit human-in-the-loop consent gates before execution.
2. If using HTTP transport across network boundaries, require robust OAuth 2.0 or token-based authentication for all connection requests.
3. If processing text inputs from tool results or external resources, sanitize and validate payloads to prevent indirect prompt injection.
4. If managing database or API credentials, adhere strictly to the principle of least privilege using scoped environment secrets.
5. If logging request payloads or error messages, redact sensitive API keys, tokens, and personally identifiable information.
6. ⚠️ Never execute shell commands or dynamic code evaluation derived directly from untrusted tool arguments.

## Procedure

1. Threat-model the MCP server to identify high-risk tool actions and sensitive resource endpoints.
2. Implement authentication middleware for remote HTTP transports to verify client identity and tokens.
3. Add explicit validation and sanitization layers to neutralize prompt injection vectors in tool inputs and outputs.
4. Enforce principle of least privilege on all database connections and external API credentials.
5. Configure redaction filters on all logging sinks to ensure secrets never leak into log files.
6. Establish approval workflows or consent gates for sensitive mutations and financial operations.

## Anti-patterns

- **Implicit trust of tool results.** Feeding untrusted external web scraping results directly into agent context as executable commands. Fix: sanitize content.
- **Unauthenticated remote endpoints.** Exposing MCP HTTP streaming endpoints without token verification or encryption. Fix: enforce OAuth.
- **Over-privileged database tokens.** Running MCP server operations with root database privileges. Fix: use scoped, restricted credentials.
- **Leaking secrets in logs.** Printing raw headers or full request objects containing API keys. Fix: implement strict redaction.

## Done checklist

- [ ] Threat model covers high-risk tool actions and resource endpoints.
- [ ] Authentication and token verification are enforced on remote transports.
- [ ] Prompt injection defense sanitizes tool inputs and outputs.
- [ ] Principle of least privilege governs all credential usage.
- [ ] Logging sinks redact sensitive tokens and PII automatically.

## Sources

- OWASP Top 10 for LLM Applications: <https://genai.owasp.org>
- Model Context Protocol Security Guidance: <https://modelcontextprotocol.io>
