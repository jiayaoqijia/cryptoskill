# Gas Optimization Skill

Gas optimization tools for EVM chains: base fee prediction, batch vs separate gas comparison, per-tx estimation with EIP-1559 suggestions, and EIP-4844 blob quotes. Helps agents decide **when** to send and **how** to send cheaper.

## Scripts

| Script | Purpose |
|--------|---------|
| `base_fee_predict` | Base fee history via `eth_feeHistory`, simple next-block prediction, when-to-send advice |
| `batch_quote` | Compare batch (multicall-style) vs separate tx gas and savings |
| `estimate_optimize` | `eth_estimateGas` plus suggested gas limit and EIP-1559 fees |
| `blob_quote` | EIP-4844 blob base fee and cost per blob (Ethereum only) |
| `optimization_report` | All-in-one report: current gas, base fee, when/how to send cheaper |

## Input / Output

All scripts read JSON from stdin and write JSON to stdout.

### base_fee_predict

**Input:**
```json
{ "chain": "ethereum", "blocks": 20 }
```

**Output:** `base_fee_gwei` (min, max, avg, last, next_block_prediction), `base_fee_level`, `when_to_send`.

### batch_quote

**Input:**
```json
{
  "chain": "ethereum",
  "operations": ["erc20_transfer", "erc20_transfer", "uniswap_swap"]
}
```

`operations` can be preset names (see `GAS_LIMITS` in `common.py`) or explicit gas limits (integers).

**Output:** `separate` / `batched` gas and cost, `savings`, `recommendation`.

### estimate_optimize

**Input:**
```json
{
  "chain": "ethereum",
  "to": "0x...",
  "data": "0x...",
  "value": "0",
  "from": "0x...",
  "buffer_pct": 1.15
}
```

`to` and `data` are required. `value`, `from`, and `buffer_pct` are optional.

**Output:** `estimated_gas`, `suggested_gas_limit`, `eip1559` (base_fee, max_priority_fee, max_fee_per_gas), `cost_eth`, `cost_usd`.

### blob_quote

**Input:**
```json
{ "chain": "ethereum", "blob_count": 1 }
```

**Output:** `blob_base_fee_gwei`, `cost_per_blob_eth` / `cost_per_blob_usd`, `total_blob_*`. On non-Ethereum, returns `blob_supported: false`.

### optimization_report

**Input:**
```json
{ "chain": "ethereum", "priority": "medium" }
```

**Output:** `gas_prices_gwei`, `base_fee_history`, `operation_costs`, `when_to_send`, `how_to_send_cheaper`, `related_tools`.

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ETHEREUM_RPC` | No | Override Ethereum RPC URL |
| `POLYGON_RPC` | No | Override Polygon RPC |
| `ARBITRUM_RPC` | No | Override Arbitrum RPC |
| `OPTIMISM_RPC` | No | Override Optimism RPC |
| `BASE_RPC` | No | Override Base RPC |
| `ETHERSCAN_API_KEY` | No | Used for gas oracle and ETH price (optional) |

## Supported Chains

Ethereum, Polygon, Arbitrum, Optimism, Base. Blob quote is Ethereum-only (EIP-4844).

## Error Handling

Scripts return `{"error": "..."}` and exit with code 1 on invalid input or upstream failures. Always check `success` or `error` in output.

## References

- [EIP-1559](https://eips.ethereum.org/EIP-1559) – Base fee and priority fee
- [EIP-4844](https://eips.ethereum.org/EIP-4844) – Blob transactions
- [eth_feeHistory](https://docs.infura.io/api/networks/ethereum/json-rpc-methods/eth_feehistory)
- [eth_estimateGas](https://ethereum.org/en/developers/docs/apis/json-rpc/#eth_estimategas)
