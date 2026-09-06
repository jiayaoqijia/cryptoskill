---
name: gas-optimization
description: Gas optimization skill for EVM chains. Use when batching txs, optimizing gas estimates, predicting base fee, or deciding when and how to send transactions cheaper (EIP-4844 blob, batch vs separate).
version: 1.0.0
author: XSpoonAi Team
tags:
  - gas
  - optimization
  - eip-4844
  - batch
  - base fee
  - ethereum
  - evm
triggers:
  - type: keyword
    keywords:
      - gas optimize
      - batch transaction
      - base fee predict
      - when to send
      - blob gas
      - eip-4844
      - gas estimate
      - multicall
      - gas cheaper
    priority: 90
  - type: pattern
    patterns:
      - "(?i)(optimize|reduce|lower|save) .*(gas|fee)"
      - "(?i)(batch|multicall) .*(transaction|tx|gas)"
      - "(?i)(when|best time) .*(send|submit|broadcast)"
      - "(?i)(blob|eip-4844) .*(gas|cost)"
    priority: 85
parameters:
  - name: chain
    type: string
    required: false
    default: ethereum
    description: EVM chain (ethereum, polygon, arbitrum, optimism, base)
  - name: to
    type: string
    required: false
    description: Contract address for estimate_optimize
  - name: data
    type: string
    required: false
    description: Calldata hex for estimate_optimize
  - name: operations
    type: array
    required: false
    description: Operation types for batch_quote (e.g. erc20_transfer, uniswap_swap)
prerequisites:
  env_vars: []
  skills: []
composable: true
persist_state: false

scripts:
  enabled: true
  working_directory: ./scripts
  definitions:
    - name: base_fee_predict
      description: Base fee history and when-to-send recommendation via eth_feeHistory
      type: python
      file: base_fee_predict.py
      timeout: 30
    - name: batch_quote
      description: Compare batch vs separate transaction gas and savings
      type: python
      file: batch_quote.py
      timeout: 30
    - name: estimate_optimize
      description: Estimate gas for a tx and suggest limit + EIP-1559 fees
      type: python
      file: estimate_optimize.py
      timeout: 30
    - name: blob_quote
      description: EIP-4844 blob gas cost on Ethereum (Cancun+)
      type: python
      file: blob_quote.py
      timeout: 30
    - name: optimization_report
      description: All-in-one gas optimization report (when/how to send cheaper)
      type: python
      file: optimization_report.py
      timeout: 45
---

# Gas Optimization Skill

Help agents decide **when** to send and **how** to send cheaper: base fee prediction, batch vs separate gas comparison, per-tx estimation with suggested limits and EIP-1559 fees, and EIP-4844 blob quotes on Ethereum.

## Quick Start

**Base fee prediction and when-to-send:**
```json
{"chain": "ethereum", "blocks": 20}
```

**Batch vs separate gas:**
```json
{"chain": "ethereum", "operations": ["erc20_transfer", "erc20_transfer", "uniswap_swap"]}
```

**Estimate and optimize a specific tx:**
```json
{"chain": "ethereum", "to": "0x...", "data": "0x...", "value": "0"}
```

**EIP-4844 blob quote (Ethereum):**
```json
{"chain": "ethereum"}
```

**All-in-one report:**
```json
{"chain": "ethereum", "priority": "medium"}
```

## Scripts

| Script | Purpose |
|--------|---------|
| [base_fee_predict.py](scripts/base_fee_predict.py) | Base fee history, simple prediction, when-to-send advice |
| [batch_quote.py](scripts/batch_quote.py) | Batch vs separate gas and savings (multicall-style) |
| [estimate_optimize.py](scripts/estimate_optimize.py) | eth_estimateGas + suggested gas limit and EIP-1559 fees |
| [blob_quote.py](scripts/blob_quote.py) | EIP-4844 blob base fee and cost per blob (Ethereum) |
| [optimization_report.py](scripts/optimization_report.py) | Combined report: gas now, base fee, batch hint, recommendations |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ETHEREUM_RPC` | No | Override Ethereum RPC (default public RPC) |
| `POLYGON_RPC` | No | Override Polygon RPC |
| `ARBITRUM_RPC` | No | Override Arbitrum RPC |
| `OPTIMISM_RPC` | No | Override Optimism RPC |
| `BASE_RPC` | No | Override Base RPC |
| `ETHERSCAN_API_KEY` | No | For ETH price USD conversion (optional) |

## Best Practices

1. **Check base fee trend** before large txs; avoid peak hours when possible.
2. **Batch** multiple operations (e.g. multicall) to save on repeated base fee and overhead.
3. **Use estimate_optimize** for contract calls; use suggested gas limit with ~10–15% buffer.
4. **EIP-4844 blobs** are for large data (e.g. L2 batches); use only when needed.
