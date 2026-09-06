# Gas Price Oracle Skill

The **Gas Price Oracle** gives SpoonOS agents financial intelligence regarding network costs. Instead of blindly sending transactions, agents can analyze the `eth_feeHistory` to pay fair prices and avoid spikes.

## Features

- **Fee History Analysis**: Fetches the last N blocks of gas data.
- **Percentile Calculation**: Determines 'Slow', 'Average', and 'Fast' gas bids.
- **Trend Detection**: Identifies if gas prices are trending up or down.

## Usage

### Parameters

- `action` (string): `get_recommendation` or `check_status`.
- `rpc_url` (string, optional): Blockchain RPC endpoint.
- `blocks` (int, optional): Number of blocks to analyze (default: 10).
- `percentiles` (list, optional): Percentiles for aggregation (default: [25, 50, 75]).

### Example Agent Prompts

> "What is the recommended gas price for a fast transaction?"
> "Is the network congested right now?"

### Output

```json
{
  "base_fee_current": 15.4,
  "trends": "stable",
  "recommendations": {
    "slow": 15.5,
    "average": 16.2,
    "fast": 18.0
  }
}
```

## Setup

Requires `web3` python library.
