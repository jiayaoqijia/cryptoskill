---
name: defi-skills
description: "Build unsigned DeFi transactions from natural language across multiple chains. Use when the user wants to send, transfer, swap, stake, unstake, wrap, unwrap, supply, withdraw, borrow, repay, deposit, delegate, add liquidity, remove liquidity, or trade yield tokens on-chain. Supports Ethereum, Arbitrum, Base, Optimism, Polygon, and Sepolia. Covers ETH, ERC-20, ERC-721, Aave, Lido, Uniswap, Curve, Compound, MakerDAO, Rocket Pool, EigenLayer, Balancer, Pendle, Fibrous, and WETH."
version: "0.2.0"
license: MIT-0
metadata:
  openclaw:
    requires:
      bins:
        - defi-skills
      env:
        - WALLET_ADDRESS
        - ALCHEMY_API_KEY
        - THEGRAPH_API_KEY
    primaryEnv: WALLET_ADDRESS
    homepage: https://defi-skills.nethermind.io/
    source: https://github.com/NethermindEth/defi-skills
    install: "pip install --upgrade defi-skills"
---

# Intent to Transaction

Builds raw unsigned DeFi transactions using the `defi-skills` CLI. The tool is a deterministic, stateless PlaybookEngine. It takes one action at a time with structured input, resolves token addresses, converts amounts to base units, ABI-encodes calldata, and outputs unsigned transactions. It has no memory between calls.

**You are the LLM.** Your job is to understand the user's intent, determine the correct action and arguments, then call the CLI with `--action` and `--args`. No LLM runs inside the CLI. It is purely deterministic. You handle all planning, decomposition, and sequencing.

The output is an unsigned transaction (`to`, `value`, `data`). It never signs or broadcasts.

## Agent Behavior

These are financial transactions. Be collaborative, not autonomous.

**Direct intent**: If the user's request maps to a single action with clear parameters, build it immediately. No discussion needed.
Examples: "Send 0.5 ETH to vitalik.eth", "Supply 100 USDC to Aave", "Wrap 5 ETH".

**Multi-step intent**: If the request requires multiple actions, present your execution plan to the user before building anything. Explain:
- What steps you will execute and in what order
- What tokens and amounts are involved at each step
- Whether you can build all steps upfront (predictable outputs like stake/wrap) or need to execute step-by-step (unpredictable outputs like swaps)
- Any assumptions you are making (e.g., "I will use the same amount for step 2 since Lido staking is roughly 1:1")

Only proceed after the user confirms the plan. If the user modifies the plan, adjust accordingly.

**Ambiguous intent**: If the request is vague or could be interpreted multiple ways, ask clarifying questions before doing anything. Do not assume a protocol, token, or strategy.
Examples:
- "I want to earn yield on my ETH": Which protocol? Lido staking? Aave supply? Rocket Pool? Each has different risk/reward.
- "Move my stables somewhere safe": Which stablecoins? What does "safe" mean to them? Aave supply? MakerDAO DSR?
- "Do something with my USDC": Too vague. Ask what they want to achieve.

**Large amounts or "max"**: If the user is operating with "max" (entire wallet balance) or amounts you consider significant, confirm the details before building. Remind them that "max" means their entire balance of that token, not just a portion.

## Constraints

- **Multi-chain support.** Supported chains: Ethereum Mainnet (1), Arbitrum (42161), Base (8453), Optimism (10), Polygon (137), Sepolia (11155111). Default is mainnet. Use `--chain-id` to target other chains. Not all actions are available on all chains — check with `defi-skills actions --chain-id <id>`.
- **One action per CLI call.** For multi-step intents, decompose into separate build calls. You are the planner.
- **Some actions restrict valid tokens.** If you are unsure whether a token is supported for an action, run `defi-skills actions <name> --json` to check. The CLI will reject unsupported tokens with a clear error listing the valid options.
- **Negative amounts are rejected.** All amounts must be zero or positive.
- **Always check `"success"` in the JSON response.** If `success` is `false`, the `error` field explains what went wrong. Do not proceed with failed builds.
- **Some actions have optional parameters with sensible defaults** (slippage, fee tier, deadline, recipient address). These are visible via `defi-skills actions <name> --json`. Inform the user about relevant defaults before building so they can override if needed.

## Prerequisites

The CLI must be installed:

```bash
pip install --upgrade defi-skills
```

A wallet address is required. The CLI reads it from (in priority order):
1. `--wallet` flag on each command
2. `WALLET_ADDRESS` environment variable
3. Persisted config (`defi-skills config set-wallet`)

For agents, prefer the env var or `--wallet` flag — no file writes needed. If no wallet is available, ask the user to provide their address before continuing.

### API keys

**Most actions that involve on-chain data need `ALCHEMY_API_KEY`** (ENS resolution, swap quotes, "max" balance queries, EigenLayer strategy verification, etc.). Simple actions with known tokens and fixed amounts (like `aave_supply` with USDC) work without it.

If a build fails with "no web3 instance" or "no RPC provider available", the user needs to set their Alchemy key via environment variable or CLI config:

```bash
# Environment variable (preferred for agents)
export ALCHEMY_API_KEY="<KEY>"

# Or persist via CLI config
defi-skills config set alchemy_api_key "<KEY>"
```

**Balancer actions** additionally need `THEGRAPH_API_KEY`:

```bash
export THEGRAPH_API_KEY="<KEY>"
# Or persist via CLI config
defi-skills config set thegraph_api_key "<KEY>"
```

## Workflow

### Step 1: Identify the Action

Determine the correct action from the supported actions table below. If unsure, or to check availability on a specific chain:

```bash
defi-skills actions --json
defi-skills actions --chain-id 42161 --json   # Arbitrum actions only
```

### Step 2: Check Parameters (always)

Always check parameters before building. The call is instant (local lookup) and prevents errors from wrong field names:

```bash
defi-skills actions aave_supply --json
```

### Step 3: Build the Transaction

```bash
TX=$(defi-skills build --action aave_supply --args '{"asset":"USDC","amount":"500"}' --json)

# On L2 chains, pass --chain-id
TX=$(defi-skills build --action aave_supply --args '{"asset":"USDC","amount":"500"}' --chain-id 42161 --json)
```

Always check the response before proceeding:

```bash
echo "$TX" | jq '.success'        # must be true
echo "$TX" | jq '.transactions'   # ordered array: approvals first, then action
```

## Response Format

The response is a JSON object with `success` and either `transactions` (on success) or `error` (on failure).

On success, `transactions` is an ordered array. **Execute them in order**: approval transactions first, then the main action. Some actions need no approval (1 transaction), others need 1 approval (2 transactions), and USDT needs a reset-to-zero step (3 transactions).

```json
{
  "success": true,
  "transactions": [
    {
      "type": "approval",
      "token": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
      "spender": "0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2",
      "raw_tx": {
        "chain_id": 1,
        "to": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "value": "0",
        "data": "0x095ea7b3..."
      }
    },
    {
      "type": "action",
      "action": "aave_supply",
      "target_contract": "0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2",
      "function_name": "supply",
      "arguments": {
        "asset": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
        "amount": "500000000",
        "onBehalfOf": "0x..."
      },
      "raw_tx": {
        "chain_id": 1,
        "to": "0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2",
        "value": "0",
        "data": "0x617ba037..."
      }
    }
  ]
}
```

On failure: `{"success": false, "error": "description of what went wrong"}`.

## Supported Actions

| Protocol | Actions | Chains |
|----------|---------|--------|
| Transfers | `transfer_native`, `transfer_erc20`, `transfer_erc721` | All chains |
| WETH | `weth_wrap`, `weth_unwrap` | Mainnet, Arbitrum, Base, Optimism, Sepolia |
| Aave V3 | `aave_supply`, `aave_withdraw`, `aave_borrow`, `aave_repay`, `aave_set_collateral`, `aave_repay_with_atokens`, `aave_claim_rewards` | Mainnet, Arbitrum, Base, Optimism, Polygon, Sepolia |
| Uniswap V3 | `uniswap_swap`, `uniswap_lp_mint`, `uniswap_lp_collect`, `uniswap_lp_decrease`, `uniswap_lp_increase` | Mainnet, Arbitrum, Base, Optimism, Polygon, Sepolia |
| Compound V3 | `compound_supply`, `compound_withdraw`, `compound_borrow`, `compound_repay`, `compound_claim_rewards` | Mainnet, Arbitrum, Base, Optimism, Polygon, Sepolia |
| Balancer V2 | `balancer_swap`, `balancer_join_pool`, `balancer_exit_pool` | Mainnet, Arbitrum, Base, Optimism, Polygon |
| Lido | `lido_stake`, `lido_wrap_steth`, `lido_unwrap_wsteth`, `lido_unstake`, `lido_claim_withdrawals` | Mainnet only |
| Curve 3pool | `curve_add_liquidity`, `curve_remove_liquidity` | Mainnet only |
| Curve Gauges | `curve_gauge_deposit`, `curve_gauge_withdraw`, `curve_mint_crv` | Mainnet only |
| MakerDAO DSR | `maker_deposit`, `maker_redeem` | Mainnet only |
| Rocket Pool | `rocketpool_stake`, `rocketpool_unstake` | Mainnet only |
| EigenLayer | `eigenlayer_deposit`, `eigenlayer_delegate`, `eigenlayer_undelegate`, `eigenlayer_queue_withdrawals`, `eigenlayer_complete_withdrawal` | Mainnet only |
| Pendle V2 | `pendle_swap_token_for_pt`, `pendle_swap_pt_for_token`, `pendle_swap_token_for_yt`, `pendle_swap_yt_for_token`, `pendle_add_liquidity`, `pendle_remove_liquidity`, `pendle_mint_py`, `pendle_redeem_py`, `pendle_claim_rewards` | Mainnet only |
| Fibrous | `fibrous_swap` | Base only |

Not all actions are available on all chains. Use `defi-skills actions --chain-id <id> --json` to check.

## How to Build Any Action

For every action, follow these three steps in order:

**1. Find the action name** from the table above. If unsure, list all:
```bash
defi-skills actions --json | jq '.by_protocol'
```

**2. Check its parameters** (always do this before building):
```bash
defi-skills actions <action_name> --json
```
This returns `required` and `optional` fields with exact parameter names and valid tokens. Use these names in `--args`.

**3. Build the transaction:**
```bash
TX=$(defi-skills build --action <action_name> --args '{"param":"value"}' --json)
echo "$TX" | jq '.success'
echo "$TX" | jq '.transactions'
```

## Examples

### Simple: Aave Supply

```bash
defi-skills actions aave_supply --json    # check params first
TX=$(defi-skills build --action aave_supply --args '{"asset":"USDC","amount":"1000"}' --json)
```

Returns 2 transactions: ERC-20 approval, then `supply()`.

### ENS Transfer (needs ALCHEMY_API_KEY)

```bash
TX=$(defi-skills build --action transfer_native --args '{"to":"vitalik.eth","amount":"0.5"}' --json)
```

### L2: Supply USDC on Arbitrum

```bash
defi-skills actions aave_supply --chain-id 42161 --json   # check params on Arbitrum
TX=$(defi-skills build --action aave_supply --args '{"asset":"USDC","amount":"1000"}' --chain-id 42161 --json)
```

### Multi-step: Stake then Restake (Mainnet)

Lido staking is predictable (~1:1), so build both upfront:

```bash
TX1=$(defi-skills build --action lido_stake --args '{"amount":"10"}' --json)
TX2=$(defi-skills build --action eigenlayer_deposit --args '{"asset":"stETH","amount":"10"}' --json)
```

## Multi-Step Planning

The CLI is stateless. Each build call is independent with no memory of previous calls and no way to reference the output of a prior transaction. When planning multi-step intents:

- **Predictable outputs** (stake, wrap, supply): input roughly equals output. Build all steps upfront with the same amount. Example: stake 10 ETH on Lido produces ~10 stETH, so pass `"amount":"10"` to the EigenLayer deposit.
- **Unpredictable outputs** (swaps, complex withdrawals): the output depends on live prices or on-chain state. You cannot know the exact amount at build time. Build and execute step 1 first, then ask the user for the result or check on-chain before building step 2. Do not guess amounts.
- **`"max"` means entire wallet balance**, not "whatever came from the last step." If the user already holds the token, `"max"` will include their existing balance plus the new amount. Make sure the user understands this before using it.

## Error Handling

- **`success: false`**: Read the `error` field. Do not retry blindly. Fix the input based on the error message.
- **Unknown action**: Run `defi-skills actions` to see all supported actions.
- **Unsupported token**: The error lists valid tokens for the action.
- **Action not available on chain**: The action exists but not on the requested chain. Use `defi-skills actions --chain-id <id>` to see what's available. Suggest mainnet if the action is mainnet-only (e.g., Lido, EigenLayer, Curve).
- **Negative amount**: Amounts must be zero or positive.
- **ENS resolution failed**: The user needs to run `defi-skills config set alchemy_api_key <KEY>`, or provide a hex address instead. Note: ENS is only available on Ethereum Mainnet and Sepolia. On L2 chains, always use hex addresses (0x...).
- **Missing wallet**: Run `defi-skills config set-wallet <address>`.
- **CLI not found**: Run `pip install defi-skills`.

## Safety

- Output is an unsigned transaction. The tool never signs or broadcasts.
- No private keys are involved at any stage.
- The deterministic build path (`--action` + `--args`) uses zero LLM tokens.
- Always review the `raw_tx` before signing. Verify `to`, `value`, and `data`.
