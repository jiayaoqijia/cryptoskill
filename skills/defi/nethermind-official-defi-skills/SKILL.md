---
name: nethermind-official-defi-skills
description: "Build unsigned DeFi transactions from natural language. Use when the user wants to send, transfer, swap, stake, unstake, wrap, unwrap, supply, withdraw, borrow, repay, deposit, delegate, add liquidity, remove liquidity, or trade yield tokens on-chain. Covers ETH, ERC-20, ERC-721, Aave, Lido, Uniswap, Curve, Compound, MakerDAO, Rocket Pool, EigenLayer, Balancer, Pendle, and WETH."
version: "0.1.0"
license: MIT-0
metadata:
  openclaw:
    requires:
      bins:
        - defi-skills
      env:
        - WALLET_ADDRESS
    primaryEnv: WALLET_ADDRESS
    homepage: https://defi-skills.nethermind.io/
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

- **Mainnet only (chain_id 1).** All contract addresses in playbooks are for mainnet. Do not pass `--chain-id`. The CLI will reject mismatches.
- **One action per CLI call.** For multi-step intents, decompose into separate build calls. You are the planner.
- **Some actions restrict valid tokens.** If you are unsure whether a token is supported for an action, run `defi-skills actions <name> --json` to check. The CLI will reject unsupported tokens with a clear error listing the valid options.
- **Negative amounts are rejected.** All amounts must be zero or positive.
- **Always check `"success"` in the JSON response.** If `success` is `false`, the `error` field explains what went wrong. Do not proceed with failed builds.
- **Some actions have optional parameters with sensible defaults** (slippage, fee tier, deadline, recipient address). These are visible via `defi-skills actions <name> --json`. Inform the user about relevant defaults before building so they can override if needed.

## Prerequisites

The CLI must be installed and a wallet address configured:

```bash
pip install defi-skills --extra-index-url https://nethermind.jfrog.io/artifactory/api/pypi/kyoto-pypi-local-prod/simple
defi-skills config set-wallet "$WALLET_ADDRESS"
```

If `WALLET_ADDRESS` is not set, ask the user to provide their wallet address before continuing.

### API keys

**Most actions that involve on-chain data need `ALCHEMY_API_KEY`** (ENS resolution, swap quotes, "max" balance queries, EigenLayer strategy verification, etc.). Simple actions with known tokens and fixed amounts (like `aave_supply` with USDC) work without it.

If a build fails with "no web3 instance" or "no RPC provider available", instruct the user to set their key using the CLI:

```bash
defi-skills config set alchemy_api_key "<YOUR_ALCHEMY_KEY>"
```

Balancer actions additionally need `THEGRAPH_API_KEY`.

Do not attempt to pass keys via environment variables. Use the config command.

## Workflow

### Step 1: Identify the Action

Determine the correct action from the supported actions table below. If unsure:

```bash
defi-skills actions --json
```

### Step 2: Check Parameters (when needed)

If you are unsure about required parameters or valid tokens for an action:

```bash
defi-skills actions aave_supply --json
```

### Step 3: Build the Transaction

```bash
TX=$(defi-skills build --action aave_supply --args '{"asset":"USDC","amount":"500"}' --json)
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

| Protocol | Actions |
|----------|---------|
| Native ETH | `transfer_native` |
| ERC-20 | `transfer_erc20` |
| ERC-721 | `transfer_erc721` |
| Aave V3 | `aave_supply`, `aave_withdraw`, `aave_borrow`, `aave_repay`, `aave_set_collateral`, `aave_repay_with_atokens`, `aave_claim_rewards` |
| Lido | `lido_stake`, `lido_wrap_steth`, `lido_unwrap_wsteth`, `lido_unstake`, `lido_claim_withdrawals` |
| Uniswap V3 | `uniswap_swap`, `uniswap_lp_mint`, `uniswap_lp_collect`, `uniswap_lp_decrease`, `uniswap_lp_increase` |
| Curve 3pool | `curve_add_liquidity`, `curve_remove_liquidity` |
| Curve Gauges | `curve_gauge_deposit`, `curve_gauge_withdraw`, `curve_mint_crv` |
| WETH | `weth_wrap`, `weth_unwrap` |
| Compound V3 | `compound_supply`, `compound_withdraw`, `compound_borrow`, `compound_repay`, `compound_claim_rewards` |
| MakerDAO DSR | `maker_deposit`, `maker_redeem` |
| Rocket Pool | `rocketpool_stake`, `rocketpool_unstake` |
| EigenLayer | `eigenlayer_deposit`, `eigenlayer_delegate`, `eigenlayer_undelegate`, `eigenlayer_queue_withdrawals`, `eigenlayer_complete_withdrawal` |
| Balancer V2 | `balancer_swap`, `balancer_join_pool`, `balancer_exit_pool` |
| Pendle V2 | `pendle_swap_token_for_pt`, `pendle_swap_pt_for_token`, `pendle_swap_token_for_yt`, `pendle_swap_yt_for_token`, `pendle_add_liquidity`, `pendle_remove_liquidity`, `pendle_mint_py`, `pendle_redeem_py`, `pendle_claim_rewards` |

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

### Multi-step: Stake then Restake

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
- **Chain ID mismatch**: All playbooks are mainnet-only. Do not pass `--chain-id`.
- **Negative amount**: Amounts must be zero or positive.
- **ENS resolution failed**: The user needs to run `defi-skills config set alchemy_api_key <KEY>`, or provide a hex address instead.
- **Missing wallet**: Run `defi-skills config set-wallet <address>`.
- **CLI not found**: Run `npm install defi-skills --registry https://nethermind.jfrog.io/artifactory/api/npm/`.

## Safety

- Output is an unsigned transaction. The tool never signs or broadcasts.
- No private keys are involved at any stage.
- The deterministic build path (`--action` + `--args`) uses zero LLM tokens.
- Always review the `raw_tx` before signing. Verify `to`, `value`, and `data`.
