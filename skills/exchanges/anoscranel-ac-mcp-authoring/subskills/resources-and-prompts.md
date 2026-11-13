---
name: resources-and-prompts
domain: software-engineering/mcp-authoring
trigger: "Exposing read-only data as MCP resources; defining URI templates; creating parameterized prompt templates for agents"
anti_trigger: "Writing tools with side effects (subskills/tool-design.md); configuring server transports (subskills/transport-and-config.md)"
scope: "Exposing structured read-only content via URIs and URI templates, and creating dynamic reusable prompt templates for agent workflows"
status: seedling
---

# Resources and Prompts

## Standard

- **Model Context Protocol Resource Specification**: addressing and streaming read-only data using standard URI schemes. <https://modelcontextprotocol.io>
- **RFC 6570 URI Template Specification**: defining parameterized URI patterns for dynamic resource discovery. <https://datatracker.ietf.org/doc/html/rfc6570>
- ⚠️ Resource URIs must be stable and deterministic so clients can reliably cache and reference them across multi-turn agent interactions.

## Decision rules

1. If data is read-only reference material without side effects, expose it as a resource rather than a tool result.
2. If resources vary by parameters, define RFC 6570 URI templates so clients can construct valid target addresses dynamically.
3. If prompt instructions require dynamic context injection, implement prompt templates with named arguments rather than hardcoded strings.
4. If resource payloads are large, support pagination or chunked streaming via content blocks to prevent memory exhaustion.
5. If resource mime types are ambiguous, explicitly declare correct content types so clients can parse payloads properly.
6. ⚠️ Never expose sensitive credentials or internal configuration files through public resource endpoints.

## Procedure

1. Identify static or read-only datasets in the application that benefit from direct agent inspection.
2. Design stable URI schemes and URI templates following RFC 6570 standards for resource identification.
3. Implement resource read handlers that fetch data efficiently and return structured content blocks with correct mime types.
4. Define parameterized prompt templates with clear argument descriptions to guide agent interaction workflows.
5. Register resource and prompt endpoints with the MCP server capability manager during initialization.
6. Test resource URI resolution and prompt template rendering with mock client requests to verify correctness.

## Anti-patterns

- **Resources with side effects.** Modifying database state inside a resource read handler. Fix: use tools for mutations.
- **Hardcoded resource paths.** Using opaque IDs instead of hierarchical, discoverable URI structures. Fix: adopt semantic URI schemes.
- **Unbounded resource payloads.** Returning multi-gigabyte datasets in a single resource response. Fix: implement chunking or pagination.
- **Undocumented prompt arguments.** Creating prompt templates without explaining required input parameters. Fix: document all arguments clearly.

## Done checklist

- [ ] Read-only data is successfully exposed via stable resource URIs.
- [ ] URI templates comply with RFC 6570 standards for dynamic resolution.
- [ ] Parameterized prompt templates provide clear guidance for agent workflows.
- [ ] Resource responses include correct mime types and content blocks.
- [ ] Sensitive internal data is strictly excluded from resource endpoints.

## Sources

- Model Context Protocol Resource Specification: <https://modelcontextprotocol.io>
- RFC 6570 URI Template Specification: <https://datatracker.ietf.org/doc/html/rfc6570>
