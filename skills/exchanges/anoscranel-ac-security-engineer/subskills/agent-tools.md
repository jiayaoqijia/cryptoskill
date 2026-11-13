---
name: agent-tools
domain: security-hardening/agent-tools
trigger: "Wiring an agent to tools, MCP servers, skills or plugins: what it may call, with which credentials, what needs a human."
anti_trigger: "Attacks arriving through model input (subskills/llm-prompt-injection.md); the general authorization model (subskills/authorization.md)."
scope: "Tool permissions, MCP and skill vetting, sandboxing, human gates"
status: "seedling"
---

# Agent Tool Security

## Standard

- The MCP specification calls tool descriptions **"untrusted"** and states **"MCP itself cannot enforce these security principles at the protocol level"** (https://modelcontextprotocol.io/specification/2026-07-28/).
- The description is the payload. Invariant Labs' Tool Poisoning Attack (1 Apr 2025): a tool labelled "Adds two numbers" whose model-visible description told the agent to read the user's SSH private key. A rug pull (description changes after approval) is the same failure; no hash covers it (https://invariantlabs.ai/blog/mcp-security-notification-tool-poisoning-attacks).
- OWASP MCP Top 10 (2025, beta): MCP01 secrets · MCP02 scope creep · MCP03 tool poisoning · MCP07 weak authz · MCP09 shadow servers.

## Decision rules

1. Narrow tools beat flexible ones: prefer `get_open_invoices(id)` over `query(sql)`.
2. Enforce at the server boundary, not in the prompt — the server refuses a dangerous call regardless of what the model was talked into. That is the real injection backstop.
3. Per-tool tiers — **allow** (read-only, in-scope), **ask** (write, external, first-time), **deny** (destructive, financial, credential-handling); destructive, financial, public and cross-tenant actions always re-confirm with a human.
4. Give the agent its own identity with time-bound, least-privilege scopes (OWASP ASI03), not the user's session; validate return values against strict schema so a compromised backend cannot smuggle fresh instructions into context.
5. Pin approved tool definitions and re-prompt on change — hash the `tools/list` result and alert on drift: 40.6% of multi-version registry servers silently changed what they advertise, 370 redirected their endpoint to another host (arXiv:2609.14119 ⚠️).
6. Composition defeats per-unit review: CapFlow reached 33.6% attack success from skills benign in isolation (arXiv:2606.15242). Vet the activated path.

## Procedure

1. List every tool, server, skill and plugin the agent can reach; remove what the task does not need.
2. Per tool: what private data can it read, send, or change? A private-data read plus an external send is a trifecta violation — split it (`subskills/llm-prompt-injection.md`).
3. Encode the allow/ask/deny tiers in the permission config; scan new descriptions for MCP03 tells, then pin the hash and alert on change.
4. Issue a dedicated agent credential — scope-bound, short-lived, revocable; never a root key, cloud role, or shared service account.
5. Add spend and rate caps per token and per tool (OWASP LLM10), timeouts, and max result sizes — a retained tool return re-metered at 14,293× the first call (arXiv:2609.28585).
6. Sandbox with default-deny egress, off the production-credential host; log every invocation (actor, tool, args hash, result) to the security log (`subskills/security-logging.md`); approval records cover transitive effects (arXiv:2609.28586).

## Anti-patterns

- "It is in the public registry, so it is vetted" — the registry binds publisher identity and a URL, never behaviour.
- One broad `run_command` tool with human approval as the only guard.
- An approval dialog showing the request but not what the workflow does afterwards.

## Done checklist

- [ ] Tool inventory current; unused tools removed.
- [ ] Trifecta check per tool; split or egress-cut done.
- [ ] allow/ask/deny encoded; destructive actions re-confirmed by a human.
- [ ] Dedicated scoped credential; definitions pinned; drift alert armed.
- [ ] Spend/rate/timeout/result-size caps; default-deny egress sandbox.
- [ ] Invocation log records actor, tool, transitive effects.

## Sources

- Primary: MCP specification rev 2026-07-28 (modelcontextprotocol.io); OWASP MCP Top 10; Invariant Labs (2025-04-01). Research: arXiv:2609.14119 (⚠️), arXiv:2606.15242, arXiv:2609.28585, arXiv:2609.28586.
- <https://genai.owasp.org>
- <https://modelcontextprotocol.io>
