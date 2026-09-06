---
name: swap-simulate
description: This skill should be used when the user asks to "simulate swap", "dry run swap", "test swap transaction", "check if swap would succeed", "simulate before executing", "dry run the trade", "preview swap on-chain", or wants to verify a previously built swap transaction would succeed without actually sending it. Uses Foundry's `cast call` to run an eth_call simulation. Requires swap calldata from swap-build skill output.
metadata:
  tags:
    - defi
    - kyberswap
    - swap
    - simulate
    - dry-run
    - foundry
    - evm
  provider: KyberSwap
  homepage: https://kyberswap.com
---

# KyberSwap Simulate Skill

Simulate (dry-run) a swap transaction using Foundry's `cast call`. This skill takes the output from `swap-build` and runs an `eth_call` against the target chain to verify the transaction would succeed — without signing, broadcasting, or spending gas.

## Prerequisites

- **Foundry installed**: `cast` must be available in PATH
- **Network access**: Must be able to reach the chain's RPC endpoint

No wallet or private key is required. Simulation uses `eth_call`, which is a read-only operation.

## Input

This skill requires the JSON output from `swap-build`:

```json
{
  "type": "kyberswap-swap",
  "chain": "ethereum",
  "tx": {
    "to": "0x6131B5fae19EA4f9D964eAc0408E4408b66337b5",
    "data": "0x...",
    "value": "1000000000000000000",
    "gas": "250000"
  },
  "sender": "0x...",
  "tokenIn": { "symbol": "ETH", "amount": "1" },
  "tokenOut": { "symbol": "USDC", "amount": "2345.67" }
}
```

## Workflow

### Step 1: Validate Input

Ensure the user has provided or you have access to the swap output JSON containing:
- `tx.to` — Router address
- `tx.data` — Encoded calldata
- `tx.value` — Transaction value in wei (for native token swaps)
- `tx.gas` — Gas estimate
- `chain` — Chain to simulate on
- `sender` — Sender address

If any required field is missing or the JSON is not available, ask the user to run `/swap-build` first.

### Step 2: Validate Router Address

Verify that `tx.to` matches the expected KyberSwap router address:

```
0x6131B5fae19EA4f9D964eAc0408E4408b66337b5
```

If the address does **not** match, display a prominent warning:

```
WARNING: The router address in this transaction (`{tx.to}`) does NOT match the
expected KyberSwap router (`0x6131B5fae19EA4f9D964eAc0408E4408b66337b5`).

This could indicate:
- The swap was built for a different protocol
- The build output was modified after generation
- A different router version is in use

Do you want to proceed with the simulation anyway? (yes/no)
```

Wait for explicit confirmation before continuing.

### Step 3: Determine RPC URL

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

### Step 4: Run Simulation

Execute the `cast call` command to simulate the transaction:

```bash
cast call \
  --rpc-url {RPC_URL} \
  --from {sender} \
  --value {tx.value} \
  --gas-limit {tx.gas} \
  {tx.to} \
  {tx.data}
```

**Example:**

```bash
cast call \
  --rpc-url https://ethereum-rpc.publicnode.com \
  --from 0xAbc123...def456 \
  --value 1000000000000000000 \
  --gas-limit 250000 \
  0x6131B5fae19EA4f9D964eAc0408E4408b66337b5 \
  0x...calldata...
```

### Step 5: Interpret Result

**On success** (cast returns data without error), present:

```
## Simulation Result: PASSED

| Field | Value |
|-------|-------|
| Status | Passed |
| Chain | {chain} |
| Router | `{tx.to}` |
| Sender | `{sender}` |
| Value | {tx.value} wei |
| Gas Limit | {tx.gas} |
| Return Data | `{returnData}` |

The transaction simulation succeeded. The swap is expected to execute
successfully on-chain with the current blockchain state.

### Next Steps

- **Execute the swap:** Run `/swap-execute` to broadcast the transaction
- **Act promptly:** Routes expire in ~30 seconds — execute soon after simulation
- **Note:** A passing simulation does not guarantee on-chain success (see Important Notes below)
```

**On failure** (cast returns an error or revert), decode the revert reason and provide actionable diagnosis:

```
## Simulation Result: FAILED

| Field | Value |
|-------|-------|
| Status | Reverted |
| Chain | {chain} |
| Router | `{tx.to}` |
| Sender | `{sender}` |
| Value | {tx.value} wei |
| Gas Limit | {tx.gas} |
| Revert Reason | {decoded revert reason} |

### Diagnosis

{See diagnosis table below}

### Recommended Action

{Specific fix based on the revert reason}
```

**Common revert reasons and diagnoses:**

| Revert Pattern | Diagnosis | Recommended Action |
|----------------|-----------|-------------------|
| `TRANSFER_FROM_FAILED` | Router cannot pull input tokens from sender | Approve the router (`0x6131B5fae19EA4f9D964eAc0408E4408b66337b5`) to spend at least `amountInWei` of the input token. Check that sender's token balance >= `amountIn`. |
| `insufficient funds` / `insufficient balance` | Sender does not have enough native token | Check native token balance with `cast balance --rpc-url {RPC_URL} {sender}`. Top up wallet before executing. |
| `Return amount is not enough` | Price moved beyond slippage tolerance since route was built | Route is stale. Re-run `/swap-build` with a fresh quote and simulate again. |
| `ETH_TRANSFER_FAILED` | Not enough ETH for swap value + gas | Verify wallet holds enough ETH for both `tx.value` and gas fees. |
| `execution reverted` (generic) | Various causes — pool state changed, liquidity removed, or route expired | Re-run `/swap-build` to get a fresh route. If persistent, try a different token pair amount or use `excludedSources` to skip the failing DEX. |
| Out of gas | Gas limit too low for the route's execution path | Retry with a higher gas limit: `gas_limit = tx.gas + tx.gas / 5` (20% buffer). |

For errors not covered above, refer to **`${CLAUDE_PLUGIN_ROOT}/skills/error-handling/SKILL.md`** for the comprehensive error reference.

## Alternative: ethers.js Simulation

For agents or environments without Foundry installed, use ethers.js to perform the same simulation:

```javascript
const { ethers } = require("ethers");

const RPC_URL = "https://ethereum-rpc.publicnode.com"; // Use appropriate chain RPC
const provider = new ethers.JsonRpcProvider(RPC_URL);

try {
  const result = await provider.call({
    from: sender,
    to: tx.to,
    data: tx.data,
    value: tx.value,
    gasLimit: tx.gas
  });
  console.log("Simulation passed:", result);
} catch (error) {
  console.error("Simulation would revert:", error.reason || error.message);
}
```

This performs the same `eth_call` as `cast call` and returns either the return data (success) or a decoded revert reason (failure). The same diagnosis table above applies to ethers.js errors.

## Important Notes

- **`cast call` does NOT send a transaction or spend gas.** It runs a read-only `eth_call` against the current blockchain state. No private key or wallet is needed.
- **Routes expire in ~30 seconds.** Simulate promptly after building. If too much time passes between `/swap-build` and simulation, the route may be stale and the simulation may fail even though the swap was valid at build time. Re-build before re-simulating.
- **A passing simulation does not guarantee on-chain success.** Blockchain state can change between the simulation and the actual transaction broadcast (new blocks, other transactions affecting pool liquidity, MEV). Treat simulation as a strong signal, not a certainty.
- **If simulation fails, always suggest rebuilding with a fresh route before retrying.** Most simulation failures are caused by stale routes or changed on-chain state, not permanent issues.
- **Verify chain ID when using custom RPCs.** Before simulating, run `cast chain-id --rpc-url {RPC_URL}` and confirm it matches the expected chain to avoid simulating against the wrong network.
- **Never expose private keys.** Simulation does not require a private key. If a user provides one, do not use it — `cast call` only needs `--from`, not `--private-key`.

## Troubleshooting

For errors not covered in Step 5 (API errors during build, PMM/RFQ failures, full error code catalog), refer to **`${CLAUDE_PLUGIN_ROOT}/skills/error-handling/SKILL.md`**.
