# Wallet Health Analyzer Skill

The **Wallet Health Analyzer** provides a "Trust Score" for blockchain addresses. By aggregating basic on-chain metrics, SpoonOS agents can make safer decisions about who they interact with.

## Features

- **Activity Profiling**: Checks transaction count (Nonce).
- **Liquidity Check**: Checks native token balance.
- **Contract Detection**: Identifies if the target is a smart contract.
- **Scoring Engine**: Calculates a 0-100 score based on weighted metrics.

## Usage

### Parameters

- `target_address` (string): The ETH address to analyze.
- `rpc_url` (string, optional): RPC Endpoint.

### Example Agent Prompts

> "Is 0xABC... a real user or a fresh burner wallet?"
> "Check the reputation of this address."

### Output

```json
{
  "address": "0x...",
  "is_contract": false,
  "metrics": {
    "nonce": 450,
    "balance_eth": 1.5
  },
  "score": 85,
  "verdict": "Trusted / High Activity"
}
```

## Setup

Requires `web3` python library.
