---
name: sushiswap-api
description: >
    REST API for optimized token swapping (including executable transaction generation), swap quoting, and pricing using the SushiSwap Aggregator.

    Use this skill when the user wants to:
    - Get a swap quote between two tokens on 40+ evm networks
    - Generate executable swap transaction data
    - Fetch token prices for a specific network or token
    - Retrieve token metadata
    - Discover supported AMM liquidity sources
    - Integrate SushiSwap swapping or pricing logic via HTTP/REST (and not the SushiSwap Javascript API)
---

# SushiSwap REST API Integration

The SushiSwap API provides HTTP access to the SushiSwap Aggregator for
**optimized token swaps**, **price discovery**, and **transaction generation**.
It aggregates liquidity from multiple DEXs to determine the best execution route.

---

## Base URL

```
https://api.sushi.com
```

---

## API Schema

The **active API schema** is defined in:

[references/openapi.yaml](references/openapi.yaml)

Agents must **always rely on the schema contents** rather than hardcoded assumptions.

---

## How To Use

1. Load `references/openapi.yaml`
2. Discover available endpoints, parameters, and response shapes dynamically
3. Select the appropriate endpoint based on user intent and schema tags
    - Quotes → quote endpoints (e.g. `/quote/v7/{chainId}`)
    - Swap execution → swap endpoints (e.g. `/swap/v7/{chainId}`)
    - Prices → price endpoints (e.g. `/price/v1/{chainId}`)
    - Token info → token endpoints (e.g. `/token/v1/{chainId}/{tokenAddress}`)
4. Construct requests that strictly conform to the schema and include a valid `referrer` parameter for all quote and swap endpoints
5. Validate required parameters before execution

---

## Mandatory `referrer` Parameter

- The `referrer` parameter **must be specified** on swap-related endpoints (e.g. `/quote` & `/swap`)
- The agent or integrator **must identify themselves** using this field
- `/quote` or `/swap` requests **must not be sent** without a `referrer` value
- Agents must never attempt to omit, spoof, or auto-generate this value.

---

## Fee Customization

The SushiSwap API supports customized integrator fees on swap-related endpoints (e.g. `/quote` & `/swap`).

### Default fee model

- Swap-related requests follow an **80/20 fee split by default**
    - **80%** to the integrator (referrer)
    - **20%** to SushiSwap
- This split applies unless explicitly overridden by SushiSwap

### Custom fee splits

- Alternative fee splits require a **partnership** with SushiSwap
- Agents and integrators should not assume custom splits are available. If users request alternative fee splits, agents should direct them to the SushiSwap
team rather than attempting to modify request parameters.

---

## Error Handling

- `422`: Request parameters are invalid → fix inputs
- `529`: Server overloaded → retry with backoff
- `500`: Internal error → retry or fail gracefully

---

## Schema Guidance

For schema usage rules and update behavior, see:

[references/OPENAPI.md](references/OPENAPI.md)
