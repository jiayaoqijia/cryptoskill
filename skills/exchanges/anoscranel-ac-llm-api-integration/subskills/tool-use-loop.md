---
name: tool-use-loop
domain: software-engineering/llm-api-integration
trigger: "Implementing the client-side agent loop, tool schemas, function execution, and multi-turn tool result submission"
anti_trigger: "Setting basic completion parameters without tool declarations (subskills/request-shape.md); handling raw API errors (subskills/error-and-resilience.md)"
scope: "Client-side agent loop, tool schema definition, tool result submission, iteration guards, and parallel execution"
status: "seedling"
---

# Tool Use Loop

## Standard

- **JSON Schema Specification**: defining structured input parameters and type validation rules for executable tool declarations. <https://json-schema.org>
- **Anthropic Tool Use Guide**: multi-turn conversational loops, function calling schemas, and handling model-requested tool executions. <https://docs.anthropic.com/en/docs/build-with-claude/tool-use>

## Decision rules

- Implement the tool use loop on the client side: the model requests tool execution, the client validates parameters and executes code, and the client submits tool results back to the model in the subsequent conversational turn.
- Enforce strict iteration guards (maximum turn counts) on agentic loops to prevent runaway execution and infinite dialogue cycles when models fail to resolve a task.
- Validate all model-provided tool arguments against the defined JSON schema before passing them to internal functions or external APIs.
- Support parallel tool execution when the model requests multiple independent function calls in a single turn, aggregating results into a single response message array.

## Procedure

1. Define available tools in the request payload using formal JSON schemas for parameter types, descriptions, and required fields.
2. Send the initial completion request containing user instructions and tool declarations.
3. Inspect the response stop reason; if the model requests a tool call, extract the tool identifier and arguments.
4. Execute the corresponding local function or API call using the extracted arguments within strict sandbox boundaries.
5. Append the tool execution result back to the conversation history message array with matching identifiers and dispatch the next completion turn.

## Anti-patterns

- Trusting model-generated tool arguments without schema validation before execution.
- Executing unrestricted shell commands or dangerous database operations directly from model-requested tool calls.
- Omitting maximum iteration limits, allowing runaway loops to consume unbounded API tokens and compute time.
- Failing to return error messages as tool results when local execution fails, leaving the model blind to the exception.

## Done checklist

- [ ] Tool parameters are defined using valid JSON schema specifications.
- [ ] Model-requested tool arguments are validated before local execution.
- [ ] Tool execution results are correctly appended to conversation history.
- [ ] Iteration guards prevent infinite agentic execution loops.

## Sources

- JSON Schema, "Core Specification", <https://json-schema.org>
- Anthropic, "Tool Use (Function Calling) Guide", <https://docs.anthropic.com/en/docs/build-with-claude/tool-use>

⚠️ Tool schema declaration formats and multi-turn message role naming conventions vary across provider APIs; verify exact syntax requirements for each integrated model family.


⚠️ Provider API pricing models and parameter default behaviors vary across releases; always verify operational metrics against current production traffic.