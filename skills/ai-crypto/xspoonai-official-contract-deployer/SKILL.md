---
name: contract-deployer
description: Compile and deploy Solidity smart contracts to EVM chains.
version: 1.0.0
author: SpoonOS Contributor
tags: [web3, smart-contracts, solidity, deployment, evm]
---

# Smart Contract Deployer

A skill to compile and deploy Solidity smart contracts. It supports compiling source code or files and deploying to any EVM-compatible blockchain.

## Quick Start

```python
# Deploy a simple contract
result = await agent.run_tool(
    "deploy_contract",
    source_code="contract Hello { string public message = 'Hello'; }",
    contract_name="Hello",
    rpc_url="http://localhost:8545",
    private_key="0x..."
)
print(result)
```

## Scripts

| Script | Purpose |
|--------|---------|
| [deploy.py](scripts/deploy.py) | Compiles and deploys Solidity contracts |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `WEB3_RPC_URL` | No | Default RPC URL (can be passed as arg) |
| `PRIVATE_KEY` | No | Default Private Key (can be passed as arg) |

## Best Practices

1. Use specific compiler versions (e.g., `0.8.19`).
2. Always verify the RPC URL and Chain ID before deploying to mainnet.
