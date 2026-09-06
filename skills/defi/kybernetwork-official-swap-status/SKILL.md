---
name: swap-status
description: This skill should be used when the user asks to "check transaction status", "tx status", "did my swap succeed", "check swap result", "transaction receipt", "what happened to my swap", or wants to verify whether a previously submitted swap transaction succeeded or failed on-chain. Uses Foundry's `cast receipt` to retrieve transaction receipts and `cast run` to decode revert reasons for failed transactions.
metadata:
  tags:
    - defi
    - kyberswap
    - swap
    - status
    - receipt
    - foundry
    - evm
  provider: KyberSwap
  homepage: https://kyberswap.com
---

# KyberSwap Swap Status Skill

Check the on-chain status of a submitted swap transaction. Given a transaction hash and chain, retrieve the receipt, report success or failure, and if the transaction reverted, attempt to decode the revert reason.

## Prerequisites

- **Foundry installed**: `cast` must be available in PATH
- **RPC access**: Public RPCs are used by default (no API key required)

## Input Parsing

The user will provide input like:
- `check tx 0xabc123... on ethereum`
- `did my swap succeed? 0xabc123... on arbitrum`
- `what happened to 0xabc123...`
- `tx status 0xabc123... base`

Extract these fields:
- **txHash** -- the transaction hash
- **chain** -- the chain slug (default: `ethereum`)

## Workflow

### Step 1: Validate Input

**Transaction hash:**
- Must match `^0x[a-fA-F0-9]{64}$`
- If the hash does not match, show the expected format (`0x` followed by 64 hex characters) and ask the user to provide a valid hash

**Chain:**
- Must be one of the 18 supported chains listed below
- If the chain is not supported, report the error and list supported chains
- If the user does not specify a chain, default to `ethereum` and mention the assumption: *"No chain specified -- defaulting to ethereum. If this transaction is on a different chain, please specify."*

**If the transaction hash is not provided**, ask the user for it before proceeding.

### Step 2: Determine RPC URL

Use the appropriate RPC endpoint for the chain:

| Chain | RPC URL |
|-------|---------|
| ethereum | `https://ethereum-rpc.publicnode.com` |
| arbitrum | `https://arb1.arbitrum.io/rpc` |
| polygon | `https://polygon-rpc.com` |
| optimism | `https://mainnet.optimism.io` |
| base | `https://mainnet.base.org` |
| bsc | `https://bsc-dataseed.binance.org` |
| avalanche | `https://api.avax.network/ext/bc/C/rpc` |
| linea | `https://rpc.linea.build` |
| mantle | `https://rpc.mantle.xyz` |
| sonic | `https://rpc.soniclabs.com` |
| berachain | `https://rpc.berachain.com` |
| ronin | `https://api.roninchain.com/rpc` |
| unichain | `https://rpc.unichain.org` |
| hyperevm | `https://rpc.hyperliquid.xyz/evm` |
| plasma | `https://plasma.drpc.org` |
| etherlink | `https://node.mainnet.etherlink.com` |
| monad | `https://rpc.monad.xyz` |
| megaeth | `https://rpc.megaeth.com` |

Or the user can specify a custom RPC with `--rpc-url`.

### Step 3: Get Transaction Receipt

```bash
cast receipt {txHash} --rpc-url {RPC_URL} --json
```

Parse the JSON output for:
- `status` -- `"0x1"` (success) or `"0x0"` (reverted)
- `gasUsed` -- Gas consumed
- `blockNumber` -- Block where the transaction was included
- `effectiveGasPrice` -- Actual gas price paid
- `from` -- Sender address
- `to` -- Contract called (router)

### Step 4: Handle Results

#### Transaction Not Found

If `cast receipt` returns an error or empty result, the transaction may be pending, on a different chain, or the hash may be invalid.

Check if the transaction exists but has not been mined:

```bash
cast tx {txHash} --rpc-url {RPC_URL} --json
```

- If `cast tx` returns data, the transaction exists but is **pending** (not yet included in a block). Inform the user and suggest waiting.
- If `cast tx` also fails, the transaction does not exist on this chain. Suggest:
  - Verify the chain is correct
  - Double-check the transaction hash
  - The transaction may have been dropped from the mempool

#### Successful Transaction (status 0x1)

Calculate gas cost:
```
gasCostWei = gasUsed * effectiveGasPrice
gasCostEth = gasCostWei / 10^18
```

Present:

```
## Transaction Status: Success

| Field | Value |
|-------|-------|
| Transaction Hash | `{txHash}` |
| Status | Success |
| Block | {blockNumber} |
| Gas Used | {gasUsed} |
| Gas Price | {effectiveGasPrice} gwei |
| Gas Cost | {gasCostEth} {nativeToken} |
| From | `{from}` |
| To (Router) | `{to}` |

**Explorer:** {explorerUrl}/tx/{txHash}
```

#### Failed Transaction (status 0x0)

```
## Transaction Status: Failed

| Field | Value |
|-------|-------|
| Transaction Hash | `{txHash}` |
| Status | Reverted |
| Block | {blockNumber} |
| Gas Used | {gasUsed} (wasted -- reverted transactions still consume gas) |
| Gas Cost | {gasCostEth} {nativeToken} |
| From | `{from}` |
| To (Router) | `{to}` |

**Explorer:** {explorerUrl}/tx/{txHash}
```

Then proceed to Step 5 to decode the revert reason.

### Step 5: Decode Revert Reason (Failed Transactions Only)

Use `cast run` to trace the transaction and extract the revert reason:

```bash
cast run {txHash} --rpc-url {RPC_URL}
```

**Common revert reasons and their diagnosis:**

| Revert Reason | Diagnosis | Fix |
|---------------|-----------|-----|
| `TRANSFER_FROM_FAILED` | Router could not pull tokens from sender | Check approval and token balance. Re-approve the router for at least `amountIn`. |
| `ETH_TRANSFER_FAILED` | Not enough ETH sent with the transaction | Check native token balance covers `tx.value` + gas fees. |
| `Return amount is not enough` | Slippage exceeded -- price moved between build and execution | Rebuild with a fresh route from `/swap-build`. Increase slippage tolerance. For MEV protection, use a private RPC (e.g., Flashbots). |
| Out of gas | Gas limit was too low for the route | Use the gas estimate from the build response + 20% buffer. Do not cap gas limit below the build estimate. |
| `Call failed` | Pool state changed or a pool in the route failed | Rebuild with a fresh route. Use `excludedSources` to skip the failing DEX. |

**If `cast run` fails or is unavailable:**
- `cast run` requires an archive node for historical transactions. Public RPCs may not support it.
- Suggest checking the transaction on the block explorer, which often shows decoded revert reasons.
- Provide the explorer link: `{explorerUrl}/tx/{txHash}`

For detailed error diagnosis beyond the table above, refer to **`${CLAUDE_PLUGIN_ROOT}/skills/error-handling/SKILL.md`**.

## ethers.js Alternative

For environments without Foundry, use ethers.js to check transaction status:

```javascript
const { ethers } = require("ethers");

const provider = new ethers.JsonRpcProvider(RPC_URL);

// Get receipt
const receipt = await provider.getTransactionReceipt(txHash);
if (!receipt) {
  console.log("Transaction not found or still pending");
} else if (receipt.status === 1) {
  console.log("Success! Gas used:", receipt.gasUsed.toString());
} else {
  console.log("Reverted. Gas wasted:", receipt.gasUsed.toString());

  // Decode revert reason
  const tx = await provider.getTransaction(txHash);
  try {
    await provider.call(
      {
        from: tx.from,
        to: tx.to,
        data: tx.data,
        value: tx.value,
        blockTag: receipt.blockNumber,
      }
    );
  } catch (error) {
    console.log("Revert reason:", error.reason || error.message);
  }
}
```

## Explorer URLs by Chain

| Chain | Explorer |
|-------|----------|
| ethereum | https://etherscan.io |
| arbitrum | https://arbiscan.io |
| polygon | https://polygonscan.com |
| optimism | https://optimistic.etherscan.io |
| base | https://basescan.org |
| bsc | https://bscscan.com |
| avalanche | https://snowtrace.io |
| linea | https://lineascan.build |
| mantle | https://mantlescan.xyz |
| sonic | https://sonicscan.io |
| berachain | https://berascan.com |
| ronin | https://app.roninchain.com |
| unichain | https://uniscan.xyz |
| hyperevm | https://explorer.hyperliquid.xyz |
| plasma | https://plasmascan.io |
| etherlink | https://explorer.etherlink.com |
| monad | https://explorer.monad.xyz |
| megaeth | https://explorer.megaeth.com |

## Important Notes

- **Transaction receipts are only available after the transaction is mined.** If the transaction is still pending, `cast receipt` will not return data. Use `cast tx` to check if it exists in the mempool.
- **`cast run` requires an archive node** for historical transactions. Public RPCs may not support tracing old transactions. If it fails, fall back to the block explorer.
- **Gas cost = gasUsed * effectiveGasPrice.** This is the actual amount spent, not the gas limit. The gas limit is the maximum the sender was willing to pay; `gasUsed` is what was actually consumed.
- **Reverted transactions still cost gas.** The sender pays for all computation up to the revert point. Warn the user about wasted gas on failed transactions.
- **Wrong chain = no results.** If the user provides a valid hash but gets "not found", the most common cause is querying the wrong chain. Suggest trying other chains the user may have used.

## Troubleshooting

For errors not covered above (API errors, on-chain revert details, PMM/RFQ failure analysis), refer to **`${CLAUDE_PLUGIN_ROOT}/skills/error-handling/SKILL.md`**.
