# Example: Full Swap Execution Flow

## Step 1: Build the Swap

User runs:
```
/swap-build 0.01 ETH to USDC on arbitrum from 0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045
```

Output JSON:
```json
{
  "type": "kyberswap-swap",
  "chain": "arbitrum",
  "tokenIn": {
    "symbol": "ETH",
    "address": "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE",
    "decimals": 18,
    "amount": "0.01",
    "amountWei": "10000000000000000",
    "amountUsd": "23.45"
  },
  "tokenOut": {
    "symbol": "USDC",
    "address": "0xaf88d065e77c8cC2239327C5EDb3A432268e5831",
    "decimals": 6,
    "amount": "23.42",
    "amountWei": "23420000",
    "amountUsd": "23.42"
  },
  "tx": {
    "to": "0x6131B5fae19EA4f9D964eAc0408E4408b66337b5",
    "data": "0xe21fd0e9000000000000000000000000...",
    "value": "10000000000000000",
    "gas": "350000",
    "gasUsd": "0.12"
  },
  "sender": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
  "recipient": "0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045",
  "slippageBps": 50
}
```

## Step 2: Execute the Swap

User runs:
```
/swap-execute
```

Agent confirms:
```
## Swap Execution — Final Confirmation

**0.01 ETH → 23.42 USDC** on arbitrum

| Field | Value |
|-------|-------|
| Router | `0x6131B5fae19EA4f9D964eAc0408E4408b66337b5` |
| Value | 10000000000000000 wei (0.01 ETH) |
| Gas Limit | 350000 |
| Sender | `0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045` |

⚠️ **WARNING: This action is IRREVERSIBLE.**

**Do you want to execute this swap?** (yes/no)
```

User confirms: `yes`

Agent asks for wallet method:
```
How do you want to sign this transaction?

1. Environment variable ($PRIVATE_KEY)
2. Ledger hardware wallet
3. Keystore file
4. Interactive (enter key when prompted)
```

User selects: `1` (Environment variable)

## Step 3: Cast Command Executed

```bash
cast send \
  --rpc-url https://arb1.arbitrum.io/rpc \
  --private-key $PRIVATE_KEY \
  --gas-limit 350000 \
  --value 10000000000000000 \
  0x6131B5fae19EA4f9D964eAc0408E4408b66337b5 \
  0xe21fd0e9000000000000000000000000...
```

## Step 4: Success Output

```
## Transaction Submitted ✅

| Field | Value |
|-------|-------|
| Transaction Hash | `0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef` |
| Block Number | 178234567 |
| Gas Used | 285432 |

**Explorer Link:** https://arbiscan.io/tx/0x1234567890abcdef...

Your swap of 0.01 ETH → 23.42 USDC has been submitted.
```

---

## ERC-20 Swap Example (Requires Approval)

For swapping USDC → ETH, an approval step is needed:

### Check Allowance First

```bash
cast call \
  --rpc-url https://arb1.arbitrum.io/rpc \
  0xaf88d065e77c8cC2239327C5EDb3A432268e5831 \
  "allowance(address,address)(uint256)" \
  0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045 \
  0x6131B5fae19EA4f9D964eAc0408E4408b66337b5
```

If allowance is less than `amountInWei`, approve first:

### Approve Router

```bash
cast send \
  --rpc-url https://arb1.arbitrum.io/rpc \
  --private-key $PRIVATE_KEY \
  0xaf88d065e77c8cC2239327C5EDb3A432268e5831 \
  "approve(address,uint256)" \
  0x6131B5fae19EA4f9D964eAc0408E4408b66337b5 \
  115792089237316195423570985008687907853269984665640564039457584007913129639935
```

The large number is `type(uint256).max` for unlimited approval. **Security tradeoff:** unlimited approvals are convenient but allow the spender to transfer your entire token balance if the contract is compromised. For large holdings, prefer approving the exact `amountIn` instead.

### Then Execute Swap

```bash
cast send \
  --rpc-url https://arb1.arbitrum.io/rpc \
  --private-key $PRIVATE_KEY \
  --gas-limit 350000 \
  --value 0 \
  0x6131B5fae19EA4f9D964eAc0408E4408b66337b5 \
  0x...calldata...
```

Note: `--value 0` because input is ERC-20, not native token.
