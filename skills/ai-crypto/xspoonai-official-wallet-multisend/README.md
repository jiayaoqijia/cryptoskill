# Wallet Multisend

Real batch ERC20 token transfer preparation with actual transaction calldata encoding and gas estimation across multiple EVM chains.

## Quick Start

### Installation

```bash
pip install web3>=6.0.0
```

### Basic Usage

```bash
echo '{
  "token": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
  "chain": "ethereum",
  "sender": "0x1111111254fb6c44bac0bed2854e76f90643097d",
  "recipients": [
    {"address": "0x2222222254fb6c44bac0bed2854e76f90643097d", "amount": "100.50"},
    {"address": "0x3333333254fb6c44bac0bed2854e76f90643097d", "amount": "250.75"}
  ]
}' | python3 scripts/main.py
```

## Features

- ✅ Real ERC20 transfer calldata generation
- ✅ Actual gas price queries from blockchain
- ✅ Multi-chain support (Ethereum, Arbitrum, Optimism, Base, BSC)
- ✅ Batch validation (up to 100 recipients)
- ✅ Sender balance checking
- ✅ Token decimal auto-detection
- ✅ Real block information

## Example Response

```json
{
  "success": true,
  "multisend": {
    "token": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
    "chain": "ethereum",
    "sender": "0x1111111254fb6c44bac0bed2854e76f90643097d",
    "decimals": 6,
    "transfers": [
      {
        "to": "0x2222222254Fb6c44BAC0BeD2854e76F90643097d",
        "amount": "100.500000",
        "amount_wei": "100500000",
        "calldata": "0xa9059cbb0000000000000000000000002222222254Fb6c44BAC0BeD2854e76F90643097d0000000000000000000000000000000000000000000000000000000005fd8220"
      }
    ],
    "success_count": 2,
    "failed_count": 0,
    "total_amount": "351.250000",
    "total_amount_wei": "351250000",
    "current_block": 24399021,
    "gas_estimate": "131000",
    "gas_price_gwei": "1.26",
    "estimated_cost_eth": "0.000166"
  }
}
```

## Batch Transfer Examples

### Send USDC to 2 Recipients on Ethereum

```bash
python3 scripts/main.py << 'EOF'
{
  "token": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
  "chain": "ethereum",
  "sender": "0x1111111254fb6c44bac0bed2854e76f90643097d",
  "recipients": [
    {
      "address": "0x2222222254fb6c44bac0bed2854e76f90643097d",
      "amount": "500"
    },
    {
      "address": "0x3333333254fb6c44bac0bed2854e76f90643097d",
      "amount": "750"
    }
  ]
}
EOF
```

### Send USDC on Arbitrum (Lower Gas)

```bash
python3 scripts/main.py << 'EOF'
{
  "token": "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5F86",
  "chain": "arbitrum",
  "sender": "0x1111111254fb6c44bac0bed2854e76f90643097d",
  "recipients": [
    {
      "address": "0x2222222254fb6c44bac0bed2854e76f90643097d",
      "amount": "100"
    },
    {
      "address": "0x3333333254fb6c44bac0bed2854e76f90643097d",
      "amount": "200"
    }
  ]
}
EOF
```

## Transaction Calldata

The skill returns ERC20 `transfer()` calldata ready to send:

```
Selector: 0xa9059cbb (transfer function)
Parameter 1: recipient address (padded to 32 bytes)
Parameter 2: amount in wei (padded to 32 bytes)
```

Use the returned calldata with any web3 library to sign and send the transaction.

## Gas Estimation

Gas is calculated based on batch size:

- Base: 21,000
- First transfer: 65,000
- Each additional: +45,000

Examples:
- 1 transfer: 86,000 gas
- 2 transfers: 131,000 gas
- 3 transfers: 176,000 gas

## Supported Chains

| Chain | Token Example |
|-------|---------------|
| Ethereum | USDC (0xA0b8...) |
| Arbitrum | USDC (0xFF97...) |
| Optimism | USDC (0x0b2c...) |
| Base | USDC (0x833...) |
| BSC | USDC (0x8AC7...) |

## Error Handling

Invalid inputs return error responses:

```json
{
  "success": false,
  "error": "validation_error",
  "message": "batch size limited to 100 recipients"
}
```

See SKILL.md for complete error code reference.

## Dependencies

- **web3.py** - ERC20 encoding and RPC queries
- **No API keys required** - Public RPC endpoints

## See Also

- [SKILL.md](SKILL.md) - Full specification
- [pull.md](pull.md) - Test results
