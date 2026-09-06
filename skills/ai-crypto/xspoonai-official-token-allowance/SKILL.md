---
name: token-allowance
description: Manage ERC20 token approvals and allowances.
version: 1.0.0
author: SpoonOS Contributor
tags: [web3, erc20, defi, security, allowance]
---

# Token Allowance Manager

A security-focused skill to manage ERC20 token approvals. It allows agents to check current allowances, approve spenders (like DEX routers), and revoke permissions to secure funds.

## Quick Start

```python
# Check if Uniswap Router has access to my USDC
allowance = await agent.run_tool(
    "manage_allowance",
    action="check",
    token_address="0xA0b8...",
    spender_address="0xE592..."
)

# Approve 100 USDC
await agent.run_tool(
    "manage_allowance",
    action="approve",
    token_address="0xA0b8...",
    spender_address="0xE592...",
    amount=100.0
)
```

## Scripts

| Script | Purpose |
|--------|---------|
| [allowance.py](scripts/allowance.py) | Checks and manages ERC20 allowances |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `WEB3_RPC_URL` | Yes | RPC URL for the blockchain |
| `PRIVATE_KEY` | Yes | Required for 'approve' and 'revoke' actions |

## Best Practices

1. Always check allowance before approving (avoid unnecessary txs).
2. Approve exact amounts rather than infinite (security best practice).
3. Revoke allowances for unused DApps to prevent hacks.
