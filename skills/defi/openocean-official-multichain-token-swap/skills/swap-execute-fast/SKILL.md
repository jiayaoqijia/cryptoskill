---
name: swap-execute-fast
description: This skill should be used when the user asks to "swap fast", "execute swap immediately", "automated swap", or wants to build and execute a swap in one step without confirmation prompts. EXTREMELY DANGEROUS: no confirmation, executes immediately.
metadata:
  tags:
    - defi
    - openocean
    - swap
    - transaction
    - evm
    - foundry
    - cast
    - dangerous
    - automation
  provider: OpenOcean
  homepage: https://openocean.finance
  warning: "⚠️ EXTREMELY DANGEROUS: Builds and executes immediately without any confirmation. Only use when you fully trust the parameters and understand the risks."
---

# OpenOcean Swap Execute Fast Skill

Build and execute a swap in one step with no confirmation prompts. This skill is intended for automation use cases where the user wants immediate execution without manual approval.

## ⚠️ EXTREME DANGER WARNING

**This skill is extremely dangerous because:**
1. **No confirmation prompts** — executes immediately
2. **No review of parameters** — assumes everything is correct
3. **Irreversible** — on-chain transactions cannot be undone
4. **Gas costs incurred even if swap fails**

**Only use when:**
- You are automating a trusted workflow
- You have thoroughly tested with small amounts
- You understand and accept all risks
- You have proper error handling in place

## Prerequisites

**Required Tools:**
- [Foundry](https://getfoundry.sh/) installed (`cast` command)
- `curl` and `jq` for API calls
- RPC endpoint configured
- Wallet access (environment variable, Ledger, Trezor, or keystore)

## Input Parsing

The user will provide input like:
- `1 ETH to USDC on base from 0xYourAddress`
- `100 USDC to ETH on arbitrum from 0xYourAddress keystore mykey`
- `0.5 WBTC to DAI on polygon from 0xYourAddress ledger`

Extract these fields:
- **amount** — amount to swap
- **tokenIn** — input token symbol
- **tokenOut** — output token symbol
- **chain** — chain slug or ID
- **sender** — sender wallet address
- **walletMethod** — optional: `ledger`, `trezor`, `keystore {name}`
- **slippage** — optional slippage in basis points (default: 100 = 1%)
- **enabledDexIds / disabledDexIds** 鈥?optional comma-separated DEX index list for route control (set only one). User input can be natural language (for example: "enable dex ids 1,2,3"), then map to API query parameters `enabledDexIds` or `disabledDexIds`.

## Workflow

### Step 0: Normalize Chain Input

Before any API call, normalize user chain input to OpenOcean-supported `Chain Code` (or keep numeric chain ID).

Examples:
- `ethereum` -> `eth`
- `binance smart chain` / `bnb` -> `bsc`
- `polygon` -> `polygon`
- `arbitrum` -> `arbitrum`

### Step 1: Resolve Token Addresses

Resolve token registry with glob first (do not read fixed path first): `**/token-registry.md`. Read the unique matched path directly.

Look up `tokenIn` and `tokenOut` for the chain. Use native token address for native tokens.

If token not found, use OpenOcean Token API fallback.

### Step 2: Get Gas Price

```
GET https://open-api.openocean.finance/v4/:chain/gasPrice
```

Use **standard** gas price. Response: Ethereum uses `data.standard.legacyGasPrice` or `data.base` (wei); other EVM chains may use `data.standard` as a number (wei). All values are **in wei**.

### Step 3: Convert Amount to Wei

```
amountInWei = amount * 10^(tokenIn decimals)
```

Use a deterministic conversion method.

### Step 4: Call the Swap API

```
GET https://open-api.openocean.finance/v4/:chain/swap?inTokenAddress={tokenInAddress}&outTokenAddress={tokenOutAddress}&amountDecimals={amountInWei}&gasPriceDecimals={gasPriceWei}&slippage={slippage_api}&account={sender}
```

Convert slippage from basis points to percentage before calling the API:

```
slippage_api = slippage_bps / 100
```

For example, `slippage 100` means `1`, and `slippage 50` means `0.5`.

Optional DEX route controls:
- `enabledDexIds=1,2,3` (only allow selected DEX indexes)
- `disabledDexIds=4,5` (exclude selected DEX indexes)

Use only one of `enabledDexIds` or `disabledDexIds`.

To get chain-supported DEX indexes, call:
```
GET https://open-api.openocean.finance/v4/:chain/dexList
```

### Step 5: Execute Immediately with `cast`

**No confirmation — executes immediately!**

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

### Step 6: Return Result

**If successful:**
```
## ✅ Swap Executed Successfully (Fast Path)

**Transaction Hash**: `{txHash}`
**Block Explorer**: {explorerUrl}

### Details
- **Input**: {amount} {tokenIn}
- **Minimum Output**: {minOutAmount} {tokenOut}
- **Gas Used**: {gasUsed} units
- **Total Cost**: {totalCost} ETH

**⚠️ No confirmation was shown — transaction was executed immediately.**
```

**Gas fee calculation (must be correct to avoid display bugs):**
- `gasPrice` from the API/script is **in wei**. Do not treat it as Gwei.
- **Gas price in Gwei** = `gasPrice / 10^9`
- **Total gas fee (ETH)** = `(gas × gasPrice) / 10^18`
- **Total cost in USD** = `totalCostEth × nativeTokenUsdPrice`

The script outputs `gasPrice` (wei), `gasPriceGwei`, `gasFeeWei`, and `gasFeeEth`; use these when displaying to avoid unit confusion.

**If failed:**
```
## ❌ Swap Execution Failed (Fast Path)

**Error**: {errorMessage}

### Transaction Details
- **Attempted**: {amount} {tokenIn} → {tokenOut}
- **From**: `{sender}`
- **Chain**: {chain}

**⚠️ No confirmation was shown — execution was attempted immediately.**
```

## Script Implementation

For reliable automation, this skill uses shell scripts:

### `fast-swap.sh` — token resolution and route building

Location: `skills/swap-execute-fast/scripts/fast-swap.sh`. Run from workspace root.

- Calls `GET /v4/:chain/gasPrice` for initial quote, then `GET /v4/:chain/swap` with `amountDecimals` and `gasPriceDecimals` (wei) per [OpenOcean API v4](https://apis.openocean.finance/developer/apis/swap-api/api-v4).
- **Uses `data.gasPrice` from the swap response** for the transaction (not the initial gasPrice call) so the built tx matches the quote.
- Outputs `gasPrice` (wei), `gasPriceGwei`, `gasFeeWei`, `gasFeeEth` to prevent unit confusion when displaying gas fee.

```bash
# Usage: ./fast-swap.sh <chain> <tokenIn> <tokenOut> <amount> <sender> [slippageBps] [--enabled-dex-ids <csv>] [--disabled-dex-ids <csv>]
# Slippage in basis points (100 = 1%). API expects percentage; script converts automatically.
# All progress goes to stderr; only JSON is printed to stdout for piping.
```

### `execute-swap.sh` — build then broadcast

Location: `skills/swap-execute-fast/scripts/execute-swap.sh`. Calls `fast-swap.sh` then broadcasts via `cast send`.

```bash
# Usage: ./execute-swap.sh <chain> <tokenIn> <tokenOut> <amount> <sender> [slippageBps] [walletMethod] [keystoreName] [--enabled-dex-ids <csv>] [--disabled-dex-ids <csv>]
# Wallet methods: env (default), ledger, trezor, keystore
```

**Script location:** `skills/swap-execute-fast/scripts/` (relative to workspace root). Invoke from project root so `references/token-registry.md` and API base URL are consistent.

## Safety Considerations

### When to Use
- Automated trading bots
- Scheduled swaps (DCA)
- Integration with other automation tools
- High-frequency, low-value trades

### When Not to Use
- Large value swaps (>$1,000)
- First time using a token pair
- Unfamiliar chains or tokens
- When market conditions are volatile

### Risk Mitigation
1. **Test with small amounts** first
2. **Set conservative slippage** (higher than normal)
3. **Monitor gas prices** to avoid overpaying
4. **Implement circuit breakers** in automation
5. **Regularly review and audit** automation logic

## Error Handling

The fast path has limited error recovery:

1. **API failures** — retry with exponential backoff
2. **Insufficient balance** — abort immediately
3. **No route found** — try alternative token or chain
4. **Wallet errors** — check connection and configuration

For critical failures, the script should abort rather than retry indefinitely.

## Example Usage

### Basic (environment variables)
```
/swap-execute-fast 1 ETH to USDC on base from 0x742d35Cc6634C0532925a3b844Bc9e90F1b6fB28
```

### With Ledger
```
/swap-execute-fast 100 USDC to ETH on arbitrum from 0x742d35Cc6634C0532925a3b844Bc9e90F1b6fB28 ledger
```

### With Keystore
```
/swap-execute-fast 0.5 WBTC to DAI on polygon from 0x742d35Cc6634C0532925a3b844Bc9e90F1b6fB28 keystore mykey
```

## Testing

**Always test before using in production:**

1. **Manual prompt tests** — use `test/agent-test-cases.md`
2. **Live tests with tiny amounts** — verify the full workflow on-chain with minimal value
3. **Integration tests** — verify the end-to-end workflow after setting up Foundry, RPC, and wallet access

Test files in `test/`:
- `agent-test-cases.md` — manual test prompts

## Alternatives

For safer workflows, use:
- **`/quote`** — Check prices only
- **`/swap-build`** — Build with confirmation
- **`/swap-execute`** — Execute with confirmation

The fast path should only be used when the benefits of automation outweigh the risks of immediate, unconfirmed execution.
