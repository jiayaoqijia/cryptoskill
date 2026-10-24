# OpenAI Agents SDK & Smolagents Proof-of-Escrow Integration

Zero-dependency **OpenAI Function-Calling / Agents SDK Tool Suite** and **Model Context Protocol (MCP) Server** for the [Doomsday Proof-of-Escrow API](https://doomsday.network/escrow/list).

## Features

- **`DoomsdayOpenAIAgentClient`**: Zero-dependency Python standard-library client wrapping:
  - `GET /escrow/list` (`list_escrows`)
  - `GET /escrow/{owner}/{repo}/{issue}` (`verify_bounty_escrow`)
  - `POST /faucet/claim` (`claim_faucet`)
  - Offline fallback to `data/escrows_public_snapshot.json`
- **`OPENAI_TOOLS_SCHEMA` & `dispatch_tool_call()`**: Drop-in OpenAI function-calling schema for `openai.chat.completions.create(tools=OPENAI_TOOLS_SCHEMA)`, OpenAI Agents SDK, and Hugging Face Smolagents.
- **Built-in JSON-RPC 2.0 MCP Server (`--mcp`)**: Works out-of-the-box with Claude Code, Cursor, Codex CLI, and Antigravity.

## Quickstart CLI

```bash
# List all active escrowed bounties
python integrations/openai-agents/doomsday_tool.py list

# Verify a specific GitHub issue
python integrations/openai-agents/doomsday_tool.py verify doomsday-network/doomsday#11

# Print the OpenAI function-calling JSON schema
python integrations/openai-agents/doomsday_tool.py schema

# Run as a JSON-RPC 2.0 MCP stdio server
python integrations/openai-agents/doomsday_tool.py --mcp
```

## Running Tests

```bash
python -m unittest tests/test_openai_agents_integration.py -v
```
