---
name: swap-execute
description: This skill should be used when the user asks to "execute swap", "broadcast swap", "send transaction", or wants to submit a previously built swap transaction on-chain. Uses Foundry's cast to broadcast the transaction.
metadata:
  tags:
    - defi
    - openocean
    - swap
    - transaction
    - evm
    - foundry
    - cast
  provider: OpenOcean
  homepage: https://openocean.finance
---

# OpenOcean Swap Execute Skill

Execute a previously built swap transaction on-chain using Foundry's `cast send`. This skill takes transaction data from `/swap-build` and broadcasts it to the network.

## Prerequisites

**Required Tools:**
- [Foundry](https://getfoundry.sh/) installed, with the `cast` command available
- RPC endpoint for the target chain
- Wallet access (environment variable, Ledger, Trezor, or keystore)

**Wallet Setup Options:**
1. **Environment variables** — `ETH_RPC_URL` and `ETH_FROM` are set
2. **Ledger** — Hardware wallet connected
3. **Trezor** — Hardware wallet connected
4. **Keystore** — Encrypted keyfile with password

## Input Parsing

The user will provide:
- Transaction data (from previous `/swap-build` output)
- Optional wallet method specification

Common patterns:
- Just `/swap-execute` (uses default environment setup)
- `/swap-execute ledger` (uses Ledger hardware wallet)
- `/swap-execute trezor` (uses Trezor hardware wallet)
- `/swap-execute keystore mykey` (uses keystore file)

## Workflow

### Step 1: Verify Transaction Data

Check that the user has provided complete transaction data. It should include:
- `from` — sender address
- `to` — OpenOcean router address
- `value` — transaction value (wei)
- `data` — encoded calldata
- `gas` — gas limit
- `gasPrice` — gas price (wei)
- `chainId` — chain ID

If any required field is missing, ask the user to run `/swap-build` first.

### Step 2: Confirm Execution

Before broadcasting, show transaction summary:

```
## OpenOcean Swap Execute - Final Confirmation

**⚠️ WARNING: This will broadcast a transaction on-chain. Funds will be transferred.**

### Transaction Summary
- **From**: `{from}`
- **To**: `{to}` (OpenOcean router)
- **Value**: {value} wei ({valueEth} ETH)
- **Gas**: {gas} units
- **Gas Price**: {gasPrice} wei ({gasPriceGwei} Gwei)
- **Chain**: {chainName} (ID: {chainId})
- **Estimated Cost**: {estimatedCost} ETH (~${estimatedCostUsd})

### Funds Impact
- **Input**: {amountIn} {tokenIn}
- **Minimum Output**: {minOutAmount} {tokenOut}
- **Max Gas Cost**: {maxGasCost} ETH

**Are you absolutely sure you want to execute this swap?** (Yes/No)
```

### Step 3: If User Confirms, Execute with `cast`

If user confirms "Yes", execute the transaction.

**Method 1: Environment Variables (Default)**
```bash
cast send --rpc-url $ETH_RPC_URL \
  --from $ETH_FROM \
  --value {value} \
  --gas {gas} \
  --gas-price {gasPrice} \
  --chain {chainId} \
  {to} {data}
```

**Method 2: Ledger**
```bash
cast send --rpc-url $ETH_RPC_URL \
  --ledger \
  --value {value} \
  --gas {gas} \
  --gas-price {gasPrice} \
  --chain {chainId} \
  {to} {data}
```

**Method 3: Trezor**
```bash
cast send --rpc-url $ETH_RPC_URL \
  --trezor \
  --value {value} \
  --gas {gas} \
  --gas-price {gasPrice} \
  --chain {chainId} \
  {to} {data}
```

**Method 4: Keystore**
```bash
cast send --rpc-url $ETH_RPC_URL \
  --keystore /path/to/keystore \
  --value {value} \
  --gas {gas} \
  --gas-price {gasPrice} \
  --chain {chainId} \
  {to} {data}
```

### Step 4: Handle the Execution Result

**If successful:**
```
## ✅ Swap Executed Successfully

**Transaction Hash**: `{txHash}`
**Block Explorer**: {explorerUrl}

### Details
- **Status**: Pending confirmation
- **Gas Used**: {gasUsed} units
- **Effective Gas Price**: {effectiveGasPrice} wei
- **Total Cost**: {totalCost} ETH

### Next Steps
1. Monitor confirmation on block explorer
2. Check token balance after confirmation
3. Verify minimum output was received
```

**If failed:**
```
## ❌ Swap Execution Failed

**Error**: {errorMessage}

### Possible Causes
1. Insufficient balance for gas + value
2. Insufficient token allowance
3. Price moved beyond slippage tolerance
4. Network congestion
5. Wallet not properly configured

### Troubleshooting
1. Check wallet balance and allowances
2. Verify RPC endpoint is working
3. Try with higher slippage
4. Wait for better network conditions
```

### Step 5: If User Declines, Cancel

If user says "No" or cancels:
```
## Swap Execution Cancelled

The transaction was not broadcast. You can:
- Review the transaction details again
- Adjust parameters and rebuild
- Use `/quote` to check current prices
```

## Important Notes

### Safety Warnings
1. **Irreversible**: On-chain transactions cannot be undone
2. **Gas Costs**: Gas will still be charged even if the swap fails
3. **Price Risk**: Prices may change between quote and execution
4. **Slippage**: Minimum output is enforced, but may be less than expected

### Best Practices
1. **Test First**: Always test with small amounts first
2. **Monitor Gas**: Use appropriate gas price for current conditions
3. **Check Allowances**: Ensure ERC-20 approvals are set
4. **Verify Network**: Confirm correct chain and RPC endpoint

### Gas Configuration
- **Gas Limit**: Use the estimate from OpenOcean and add a 20% buffer
- **Gas Price**: Use current market rates
- **Priority Fee**: For EIP-1559 chains, use an appropriate priority fee

## Error Handling

Common execution errors:

1. **`insufficient funds for gas * price + value`**
   - User doesn't have enough native token for gas + value
   - Solution: Add funds or reduce amount

2. **`execution reverted: OpenOcean: insufficient output amount`**
   - Price moved beyond slippage tolerance
   - Solution: Increase slippage or try again

3. **`execution reverted: ERC20: transfer amount exceeds allowance`**
   - Token not approved for spending
   - Solution: Approve token first

4. **`nonce too low`** or **`nonce too high`**
   - Transaction nonce mismatch
   - Solution: Let wallet manage nonces automatically

For detailed troubleshooting, see `skills/error-handling/SKILL.md`.

## Example Workflow

```
User: /swap-build 1 ETH to USDC on ethereum from 0x...
Agent: Shows quote, asks for confirmation
User: Yes
Agent: Returns transaction data

User: /swap-execute
Agent: Shows final confirmation
User: Yes
Agent: Executes with cast, returns tx hash
```

## Alternative: Fast Execution

For automated workflows, consider `/swap-execute-fast` which builds and executes in one step (no confirmation prompts). **Use with extreme caution.**

## Post-Execution

After successful execution:
1. Monitor transaction on block explorer
2. Verify token balances updated
3. Check that minimum output was received
4. Save transaction hash for records

**Remember**: A successful transaction does not necessarily mean the swap outcome was correct. Always verify the final result.