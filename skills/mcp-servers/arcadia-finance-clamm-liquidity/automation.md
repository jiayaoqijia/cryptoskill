# Automation Setup

All automation on Arcadia uses V3/V4 accounts only. Arcadia's backend bots do the work once configured.

Automations are configured as **intents**: you describe the outcome you want and the backend resolves which asset-manager contracts are needed, checks that the combination is valid, encodes their metadata and returns the finished `setAssetManagers` calldata. There is no client-side contract encoding, and no asset-manager addresses to pick.

## Agent Workflow

```
1. read.account.info               → find the LP position id and what is already automated
2. read.asset_manager.current      → decoded per-manager config, plus superseded managers to clear
3. read.asset_manager.intents      → which intents this account can enable, and why any are blocked
4. write.account.automations       → pass the full intents array, get back the unsigned tx
```

Pass the LP position's `position_id` and the backend fetches the protocol, staked flag, pool tokens and reward tokens for you. Only supply `protocol` / `token0` / `token1` by hand when you have no position id. `claim_merkl` needs no position context at all.

## The five intents

| Intent          | What it does                                                                   | Needs position context |
| --------------- | ------------------------------------------------------------------------------ | ---------------------- |
| `compound_fees` | Reinvest earned fees and rewards back into the LP                              | yes                    |
| `claim_rewards` | Claim yield out, as-earned or converted to one token via CowSwap               | yes                    |
| `add_to_lp`     | Fold idle pool-token balances (deposits, rebalance leftovers) back into the LP | yes                    |
| `rebalance`     | Reposition the LP: out-of-range, take-profit, or POL strategy                  | yes                    |
| `claim_merkl`   | Auto-claim Merkl incentive rewards                                             | no                     |

Every intent takes `enabled` (default true) and an optional `position_id`.

## Full desired state vs delta

`write.account.automations` takes the **complete desired state**. Any automation not in the `intents` array gets disabled, so include everything the user wants kept, not just what is new. To turn everything off, pass a single intent with `enabled: false`.

`mode: "save"` (the default) diffs the desired state against what is on-chain and returns a signable transaction that both enables what you asked for and disables what you left out.

`mode: "preview"` resolves and validates the intents **without** reading chain state, and deliberately returns **no transaction** (`preview_only: true`). Because it does not diff, its calldata contains no disable entries: broadcasting it would enable the new managers while leaving omitted automations running. Use preview to check that a combination is legal or to show a plan, then re-run with `save` to get something signable.

`write.account.automations_delta` is the **change-only** variant: `enable` switches intents on, `disable` takes asset-manager addresses (from `read.asset_manager.current`) to switch off, and anything unmentioned is left alone. Use it to flip one automation without restating the rest.

Example: add rebalancing to an account that is already compounding, without disturbing the compounder:

```
write.account.automations_delta(
  account_address: "0x...",
  position_id: 12345,
  enable: [{ kind: "rebalance" }]
)
```

Same thing expressed as full desired state:

```
write.account.automations(
  account_address: "0x...",
  position_id: 12345,
  intents: [{ kind: "compound_fees" }, { kind: "rebalance" }]
)
```

## Per-token scoping

`compound_fees`, `claim_rewards` and `add_to_lp` accept a `tokens` array (`token0`, `token1`, and `reward` for the yielding intents) so different tokens can be routed differently. Omitting `tokens` means all yielding tokens for the compound/claim intents.

`reward` only exists on a staked position whose reward token is not one of the pool tokens. When the reward token _is_ a pool token it collapses into that token.

**Every yielding token must be assigned to exactly one of `compound_fees` or `claim_rewards`.** Scoping one intent to a subset without covering the rest is rejected, and no token may appear in both. So `compound_fees` with `tokens: ["token0"]` on its own is invalid: token1's yield would be unassigned.

A mixed partition is valid and common: compound token0's fees while claiming token1's out.

```
write.account.automations(
  account_address: "0x...",
  position_id: 12345,
  intents: [
    { kind: "compound_fees", tokens: ["token0"] },
    { kind: "claim_rewards", config: { tokens: ["token1"], destination: "account" } }
  ]
)
```

Note the `destination: "account"`. A **wallet** (or custom `recipient`) payout is only allowed for a pure as-earned claim: nothing converted, and every yielding token claimed. A partial claim like the one above must settle in the account.

Note also that `add_to_lp` is opt-in per token: folding an idle balance happens only for tokens you name.

## Validation

The backend enforces compatibility rules rather than letting an invalid combination reach the chain. When one fires the tool returns an error with the rule name and reason, and no transaction. The full set:

| Rule                                       | Meaning                                                                                                                      |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| `duplicate_intent_kind`                    | Each intent kind may appear only once. Two rebalance strategies is ambiguous.                                                |
| `token_double_assigned`                    | A token cannot be both compounded and claimed.                                                                               |
| `incomplete_partition`                     | Every yielding token must be assigned to compound or claim.                                                                  |
| `empty_token_scope`                        | A `tokens` list must not be explicitly empty. Omit it to mean "all".                                                         |
| `tokens_out_of_scope`                      | Named a token this position does not yield (e.g. `reward` on an unstaked position, or a reward that is itself a pool token). |
| `claim_to_wallet_requires_pure_claim`      | A wallet/custom-recipient payout requires claiming every yielding token as-earned, nothing converted.                        |
| `convert_tokens_out_of_scope`              | `convert_tokens` must be a subset of the claimed tokens.                                                                     |
| `convert_settles_in_account`               | Converted rewards must settle in the account.                                                                                |
| `claim_convert_missing_buy_token`          | Converting requires a `buy_token`.                                                                                           |
| `convert_target_is_compounded`             | `buy_token` cannot be a token you also compound.                                                                             |
| `convert_target_in_convert_set`            | `buy_token` cannot be one of the tokens being converted.                                                                     |
| `convert_target_is_folded`                 | `buy_token` cannot also be folded by `add_to_lp`, or the converted rewards get re-added immediately.                         |
| `compound_reward_buy_token_not_pool_token` | The compound CowSwap leg must buy one of the position's underlyings.                                                         |
| `multiple_convert_targets`                 | One account has a single CowSwapper metadata slot, so a compound-reward swap leg and a claim-and-convert leg cannot coexist. |

Read `errors[].reason`, adjust the intents, retry. `read.asset_manager.intents` with an account address tells you up front which intents are currently blocked.

## Simulation

`mode: "save"` and the delta tool simulate the resulting `setAssetManagers` call on Tenderly when an `owner` is supplied, and return `tenderly_sim_status`:

- `success`: the simulation ran and passed.
- `failure`: the simulation ran and the call would revert. The tool returns an error and **no** transaction, with the Tenderly link so you can read the revert reason. Do not broadcast.
- `unavailable`: no simulation ran, or the result was inconclusive. Typically `owner` was not supplied. The transaction is returned; this status neither endorses nor condemns it.

`preview` is never simulated, so it always reports `unavailable`, which is one reason it returns no transaction.

## When there is no transaction

Three success-path cases return no `transaction`, and an agent must not treat any of them as "nothing to do but broadcast anyway":

| Field                                    | Meaning                                                   |
| ---------------------------------------- | --------------------------------------------------------- |
| `preview_only: true`                     | Preview mode. Re-run with `save`.                         |
| `no_changes_needed: true`                | The account already matches the request. Nothing to send. |
| (error) `tenderly_sim_status: "failure"` | The call would revert. Fix the cause, do not broadcast.   |

## Superseded managers

Asset managers are redeployed over time. An account registered on an older deployment keeps working, but `read.asset_manager.current` lists those under `deprecated` (and `read.account.info` under `automation.deprecated_managers`). They should be cleared: `write.account.automations` disables them as part of a save, or pass their addresses to `write.account.automations_delta`.

---

## Rebalance

**What it does:** When the LP position goes out of range, Arcadia's bot repositions it to a new range centered on the current price. Pending fees and staking rewards are claimed and compounded as part of the rebalance.

**Strategies** (`strategy.kind`):

- `out_of_range` (default): repositions based on range triggers and cooldowns
- `take_profit`: runs on the dedicated profit-taker contract, takes profit in `profit_token`
- `protocol_owned_liquidity`: POL strategy

**Key `out_of_range` params:**

| Param                      | Default  | Description                                                                      |
| -------------------------- | -------- | -------------------------------------------------------------------------------- |
| `optimal_token0_ratio`     | `500000` | Target token0 composition (1e6-scaled: 500000 = 50%)                             |
| `trigger_lower_tick_ratio` | `0`      | Offset from tick_lower as a fraction of tick range (1e6-scaled, 0 = at boundary) |
| `trigger_upper_tick_ratio` | `0`      | Offset from tick_upper, same scaling. Asymmetric values are valid                |
| `min_rebalance_time`       | `3600`   | Cooldown in seconds                                                              |
| `max_rebalance_time`       | `1e12`   | Max time before a forced rebalance (effectively disabled)                        |

Trigger ratios are **tick distance, not price**: a ratio of 50000 shifts the trigger by 5% of `(tick_upper - tick_lower)` ticks. Positive values delay the rebalance until price travels further beyond the range; negative values fire preemptively while price is still in range.

`max_tolerance` and `min_liquidity_ratio` (both 1e18-scaled) override the MEV/slippage and value-loss caps. Omit them for the pool's defaults. AAA pools floor `max_tolerance` at 5% because they are thin and volatile.

**Free rebalance quota (per owner across all accounts):**

| stAAA held | Daily | Weekly |
| ---------- | ----- | ------ |
| 0          | 1     | 3      |
| 3,000      | 2     | 10     |
| 6,000      | 3     | 17     |
| 9,000      | 4     | 24     |
| 30,000     | 11    | 73     |

Quota is bypassed when: gas cost < pending fees / 2, or position value >= $50k.

**Pay for extra rebalances with AAA:** Deposit AAA tokens into the account, then approve them to the gas relayer `0xD938C8d04cF91094fecAF0A2018EAac483a40137`. The relayer is an asset manager but no intent configures it, so it sits outside the intent model: `read.account.info` reports it as `automation.gas_relayer`.

**Fees:** 7.5% of yield earned, max 1% liquidity decrease per rebalance (MDL).

---

## Compound fees

**What it does:** Claims accumulated LP fees and staking rewards and reinvests them into the position.

**When to add on top of a rebalance:** The rebalance compounds at rebalance time. Adding `compound_fees` also compounds between rebalances, which means more frequent compounding and higher effective APY.

**Staked positions:** a staked position earns staking emissions (for example AERO), not LP fees. When the reward token is not one of the pool tokens, the backend routes it through the CowSwapper automatically: the reward is swapped to a pool token via a CoW Protocol batch auction (MEV-protected) and folded into the LP. You do not enable a CowSwapper yourself and you do not pick the sell/buy tokens. When the reward token _is_ a pool token no swap is needed and none is configured.

---

## Claim rewards

**What it does:** Claims pending fees and emissions out of the position instead of reinvesting them.

**Config:**

| Field            | Default        | Description                                                            |
| ---------------- | -------------- | ---------------------------------------------------------------------- |
| `mode`           | `as_earned`    | `as_earned` pays the tokens as-is, `convert_to` swaps them via CowSwap |
| `destination`    | `account`      | `account` or `wallet` (the owner EOA)                                  |
| `buy_token`      | none           | ERC20 to swap into. Required whenever anything is being converted      |
| `recipient`      | none           | Explicit payout address, overrides `destination`                       |
| `tokens`         | all yielding   | Which tokens' yield to claim out                                       |
| `convert_tokens` | defers to mode | Subset of `tokens` to swap; the rest are claimed as-earned             |

CowSwap settles inside the account, so a converted claim cannot pay out to a wallet. `convert_tokens` is what enables a partial convert: swap the reward to USDC while claiming token0 and token1 as-earned.

---

## Add to LP

**What it does:** Folds idle pool-token balances sitting in the account (from deposits, or left over after a rebalance) into the LP position.

Opt-in per token via `tokens`: a token's balance is folded only when named. This is independent of compounding, so "compound yield without folding" and "fold without compounding" are both valid configurations.

Both a rebalance and a compound may carry the same fold instruction. The amount is read from the live account balance at execution time, so whichever runs first consumes it and the other folds nothing. There is no double-add.

---

## Claim Merkl

**What it does:** Claims external Merkl protocol incentive rewards into the account, which are additional rewards paid by token teams on top of regular LP fees.

**When to enable:** When the pool has active Merkl campaigns (check the APY breakdown in `read.strategy.list`).

**Always combine with a rebalance** when both are relevant: no conflict, extra free yield.

Merkl authorization is the Merkl distributor whitelist, not `isAssetManager`, so it is reported separately. `read.asset_manager.current` returns a `merkl` block with `connected`, `active` and `tokens_missing`. When `tokens_missing` is true the user still has to register reward tokens with Merkl before claims land.
