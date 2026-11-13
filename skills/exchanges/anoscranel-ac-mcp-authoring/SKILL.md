---
name: ac-mcp-authoring
description: "Authoring Model Context Protocol servers that expose tools, resources, and prompts to AI agents over an open protocol. Covers protocol models, tool design and schemas, resource URIs and templates, transport layers and stdio/HTTP configuration, security models with OAuth and injection defense, testing and debugging with the MCP inspector, and SemVer versioning and operations. Use when asking \"build an MCP server\", \"expose this as a tool for agents\", \"MCP integration\", \"wrap this API in MCP\", \"add tools to my agent\". Not for human-facing API contracts, nor for prompting models themselves."
license: MIT
metadata:
  domain: software-engineering
---

# MCP Authoring

## Overview

Authoring Model Context Protocol (MCP) servers that expose capabilities to AI agents. The protocol standardizes how agents discover and invoke tools, read resources, and apply parameterized prompts. This skill guides the design, transport configuration, security hardening, testing, and operation of production-ready MCP servers.

## When to use

- Building a new MCP server from scratch to expose backend services or data to AI agents.
- Wrapping an existing API or library into MCP-compatible tools, resources, and prompts.
- Configuring transports, authentication, and secure client-server communication.
- Debugging schema validation failures, transport drops, or agent invocation errors.
- Versioning and publishing MCP servers safely for client consumption.

## When NOT to use

- Designing human-facing REST, GraphQL, or gRPC API endpoints — outside this skill.
- Prompt engineering or writing system instructions for language models themselves — outside this skill.

## Precedence

> The deepest loaded instruction governs its uniquely-claimed scope; every `scope:` string is claimed by exactly one file in this tree; no leaf may widen a prohibition declared by an ancestor — leaves narrow, never override upward.

## Subskill index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/protocol-model.md` | software-engineering/protocol-model | Establishing the foundational architecture of MCP servers, client-server handshake, capability negotiation, and the three primitive categories |
| `subskills/resources-and-prompts.md` | software-engineering/resources-and-prompts | Exposing structured read-only content via URIs and URI templates, and creating dynamic reusable prompt templates for agent workflows |
| `subskills/security-model.md` | software-engineering/security-model | Mitigating server attack surface, HTTP authentication, tool call consent gates, prompt injection defense, and least-privilege secret management |
| `subskills/testing-and-debugging.md` | software-engineering/testing-and-debugging | Systematic validation of tool schemas, transport smoke tests, contract testing, interactive debugging with the MCP inspector, and clean logging |
| `subskills/tool-design.md` | software-engineering/tool-design | Creating robust, self-documenting MCP tools with precise JSON Schemas, deterministic error recovery, and idempotency guarantees |
| `subskills/transport-and-config.md` | software-engineering/transport-and-config | Selecting and configuring MCP transport layers including local stdio and remote HTTP streaming, session lifecycles, and environment wiring |
| `subskills/versioning-and-ops.md` | software-engineering/versioning-and-ops | Operating MCP servers over time, semantic versioning, breaking change management, deprecation headers, and client contract documentation |

## See also

- `subskills/protocol-model.md` — client-server architecture and primitives.
- `subskills/tool-design.md` — schema design and deterministic errors.
- `subskills/resources-and-prompts.md` — resource URIs and prompt templates.
- `subskills/transport-and-config.md` — stdio and HTTP streamable transports.
- `subskills/security-model.md` — OAuth, consent, and injection defense.
- `subskills/testing-and-debugging.md` — MCP inspector and contract testing.
- `subskills/versioning-and-ops.md` — SemVer and capability negotiation.


Additional guidance ensures seamless integration with modern agent runtimes and multi-turn workflows.