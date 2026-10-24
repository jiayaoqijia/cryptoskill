---
name: doomsday-openai-agents
description: Verify on-chain Doomsday Proof-of-Escrow collateral (DOOM L1 UTXOs & Base Mainnet wDOOM) before executing GitHub bounty tasks using the OpenAI Agents SDK, Smolagents, or MCP.
---

# Doomsday Proof-of-Escrow Skill (`doomsday-openai-agents`)

Use this skill to cryptographically verify that a GitHub bounty issue has real on-chain locked collateral (`DOOM` on Doomsday L1 or `wDOOM` on Base Mainnet `0x623c84A5E04bF715018203334b0eFE41696eBC3E`) before investing agent compute.

## Core Verification Workflow

1. **Discover Active Escrowed Bounties (`GET /escrow/list`)**:
   ```bash
   python integrations/openai-agents/doomsday_tool.py list
   ```
2. **Verify a Specific GitHub Issue (`GET /escrow/{owner}/{repo}/{issue}`)**:
   ```bash
   python integrations/openai-agents/doomsday_tool.py verify doomsday-network/doomsday#11
   ```
   - Proceed immediately when `verified: true` and `status == "SAFE_WITH_ESCROW"`.
   - Treat `status == "SAFE_NO_ESCROW"` as unescrowed prior to merge.
3. **Claim Onboarding Faucet Tokens (`POST /faucet/claim`)**:
   ```bash
   python integrations/openai-agents/doomsday_tool.py claim <doom1_or_0x_address>
   ```

## OpenAI Function-Calling / Agents SDK Integration

```python
from integrations.openai_agents_example import (  # or import directly from integrations/openai-agents/doomsday_tool.py
    OPENAI_TOOLS_SCHEMA,
    dispatch_tool_call,
    verify_doomsday_escrow,
)

# Direct verification call
verdict_json = verify_doomsday_escrow("doomsday-network", "doomsday", 11)
```

## MCP Server Configuration (Claude Code / Cursor / Codex / Antigravity)

```json
{
  "mcpServers": {
    "doomsday-openai-agents": {
      "command": "python",
      "args": ["integrations/openai-agents/doomsday_tool.py", "--mcp"]
    }
  }
}
```

## Settlement Rails

- **Base Mainnet (`wDOOM`, Chain ID `8453`)**: Contract `0x623c84A5E04bF715018203334b0eFE41696eBC3E` (Uniswap v3 Pool `0xf7217329574249d7b389404aECF2C582662F3659`).
- **Doomsday Layer-1 (`DOOM`)**: Escrow Vault `doom1caea0957fb471c2b83940cc2feb421abad938dfbdef662de`.
