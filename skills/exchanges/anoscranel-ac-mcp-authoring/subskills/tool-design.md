---
name: tool-design
domain: software-engineering/mcp-authoring
trigger: "Designing tool schemas for MCP agents; writing orthogonal tool interfaces; handling tool execution errors and retries"
anti_trigger: "Setting up resource URIs (subskills/resources-and-prompts.md); configuring server transports (subskills/transport-and-config.md)"
scope: "Creating robust, self-documenting MCP tools with precise JSON Schemas, deterministic error recovery, and idempotency guarantees"
status: seedling
---

# Tool Design

## Standard

- **JSON Schema Specification**: defining strict input validation rules for agent tool parameters. <https://json-schema.org>
- **Model Context Protocol Tool Guidelines**: designing descriptive, orthogonal tool interfaces for LLM consumption. <https://modelcontextprotocol.io>
- ⚠️ LLM interpretation depends heavily on descriptive parameter names and explicit type constraints in schemas; ambiguous schemas cause execution failures.

## Decision rules

1. If a tool performs multiple unrelated actions, split it into small, orthogonal tools rather than a single god-tool.
2. If tool inputs can be invalid or incomplete, specify comprehensive JSON Schemas with explicit required fields and descriptive types.
3. If an operation is non-idempotent, design the tool schema to accept unique idempotency tokens or return explicit conflict signals.
4. If a tool execution fails due to user input error, return a structured error result with recovery guidance rather than crashing the server.
5. If parameter descriptions are vague, expand them with concrete examples so the model understands expected formats.
6. ⚠️ Never trust raw string inputs from tool calls; validate every payload against the compiled JSON Schema before execution.

## Procedure

1. Identify the exact atomic action the agent needs to perform and draft its functional scope.
2. Write a precise JSON Schema defining all required and optional input parameters, types, and validation constraints.
3. Craft clear, descriptive docstrings and parameter descriptions specifically tailored for LLM reasoning and comprehension.
4. Implement input validation guards that intercept malformed payloads before invoking core business logic.
5. Structure execution output to return clean text or structured content blocks alongside explicit success or error flags.
6. Test tool responses against edge cases to ensure error messages guide the agent toward correct retry strategies.

## Anti-patterns

- **God-tool design.** Creating a single tool with dozens of boolean flags and overloaded parameters. Fix: split into dedicated single-purpose tools.
- **Vague parameter descriptions.** Leaving parameter descriptions blank or ambiguous, leading to incorrect agent arguments. Fix: include format examples in descriptions.
- **Unstructured error responses.** Crashing the server or returning raw stack traces on invalid inputs instead of structured error payloads. Fix: catch errors and return guidance.
- **Non-deterministic outputs.** Returning non-reproducible data formats that confuse subsequent agent reasoning steps. Fix: standardize output schemas.

## Done checklist

- [ ] Tools are scoped to single, atomic, orthogonal responsibilities.
- [ ] JSON Schemas rigorously define all parameter types, constraints, and required fields.
- [ ] Parameter descriptions include clear examples for LLM comprehension.
- [ ] Input validation prevents malformed payloads from reaching domain logic.
- [ ] Execution errors return structured recovery guidance to the agent.

## Sources

- JSON Schema Specification: <https://json-schema.org>
- Model Context Protocol Tool Guidelines: <https://modelcontextprotocol.io>
