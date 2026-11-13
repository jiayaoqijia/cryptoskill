---
name: ac-agent-tool-design
description: 'Deciding what tools an agent gets and shaping each one so the model uses it correctly: which capabilities deserve to be tools at all, writing descriptions the model actually reads, result payloads sized for a context window, the tool menu and its confusion costs, error returns that teach recovery instead of dead ends, and the written tool-surface record. It teaches the craft of the tool interface seen from the model''s side; it never recommends a framework and never promises an agent will behave. Use when asking "should this be a tool", "tool description writing", "how many tools is too many", "tool naming", "tool result format", "tool menu design", "agent tool design", "tool error messages", "tool schema design", "when not to give an agent a tool". Not for the client-side agent loop and multi-turn plumbing (ac-llm-api-integration), not for MCP server protocol and transport (ac-mcp-authoring), not for sandboxing what a tool may touch (ac-wasm-and-sandboxes).'
license: MIT
metadata:
  domain: prompt-engineering
status: seedling
---

# Agent tool design

## Overview

A tool is an interface read by a model rather than a person, and everything a person would get from layout, help text, and convention must arrive through the description, the name, and the shape of the result. The model chooses from the description alone, decides what to pass from the name and parameters, and interprets the result from its payload shape. Badly shaped tools misfire exactly where a badly designed human interface confuses.

This skill covers the design of the tool surface as seen from the model's side: which capabilities should be tools at all, how descriptions and names work on a model reader, how menu size and near-duplicates create confusion costs, what a result payload should carry and omit, and what an error return owes the caller. The protocol plumbing behind it — the client loop, the MCP transport, the sandbox around execution — belong to three other skills, each named in every leaf.

Primary sources: <https://docs.anthropic.com/en/docs/agents-and-tools/tool-use> and <https://platform.openai.com/docs/guides/function-calling>.

## When to use

- When deciding whether a capability becomes a tool at all.
- When writing or repairing tool descriptions, names, and parameter schemas.
- When an agent picks the wrong tool, misuses a tool, or calls nothing when it should act.
- When a growing tool menu starts degrading selection accuracy.

## When NOT to use

- For the client-side loop, retries, and multi-turn plumbing (use ac-llm-api-integration).
- For the MCP protocol, transports, and server structure (use ac-mcp-authoring).
- For sandboxing and limiting what a tool may touch (use ac-wasm-and-sandboxes).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/what-becomes-a-tool.md` | `prompt-engineering/what-becomes-a-tool` | Capabilities that earn tool status, and those that should stay prompt or workflow. |
| `subskills/reading-descriptions.md` | `prompt-engineering/reading-descriptions` | Descriptions and names written for a model reader. |
| `subskills/tool-menu-design.md` | `prompt-engineering/tool-menu-design` | Menu size, near-duplicates, grouping, and the confusion cost of breadth. |
| `subskills/result-payloads.md` | `prompt-engineering/result-payloads` | What a tool returns to a context window, and what it omits. |
| `subskills/errors-as-lessons.md` | `prompt-engineering/errors-as-lessons` | Error returns that tell the model what to do next. |
| `subskills/choosing-parameters.md` | `prompt-engineering/choosing-parameters` | Parameter sets the model can fill correctly from what it knows. |
| `subskills/tool-surface-record.md` | `prompt-engineering/tool-surface-record` | The written record: tool inventory, misfire log, and change history. |

## Status and honest limits

Tool selection behaviour varies across models and changes with model updates, so every claim here is a design discipline with a rationale, not a guarantee: misfire rates improve under testing, and the misfire log is the evidence. The protocol skills (MCP, raw API integration) evolve faster than this craft; where a provider adds a mechanism like tool search, this skill stays at the design layer above it. Nothing here recommends a framework — the craft is provider-neutral by design.
