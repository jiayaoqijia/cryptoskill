---
name: dexe-staking
description: |
  Set up DeXe DAO staking end-to-end: resolve/deploy the StakingProposal
  contract, pass a `create_staking_tier` proposal via `dexe_proposal_create`,
  then holders stake/claim/reclaim. Covers the two traps that silently eat
  tiers — a PAST deadline is rejected on-chain with a SUCCESSFUL execute
  (StakingRejected, no tier), and staking does not exist on BSC testnet (97)
  at all. Use when the user says "staking", "stake", "staking tier",
  "staking rewards", "let holders stake".
---

# DeXe staking setup

Staking is MAINNET-ONLY (chain 56): every testnet (97) GovUserKeeper predates
the staking implementation — do not attempt staking transactions there; plan
that leg for mainnet and tell the user why.

The `dexe_proposal_create` composite (proposalType `create_staking_tier`)
auto-resolves the StakingProposal address the way the frontend does
(`GovPool.getHelperContracts().userKeeper` → `stakingProposalAddress()`).
If the contract isn't deployed yet, the error returns the EXACT one-off
`dexe_tx_send` payload for the permissionless `deployStakingProposal()` call —
send it, then re-run the SAME create call. Never wrap that deploy in a
governance proposal (custom/custom_abi).

After the tier proposal executes, holders use `dexe_vote_build_staking_stake`
/ `_claim` / `_claim_all` / `_reclaim` (vote toolset) and anyone can read the
live tiers with `dexe_read_staking_info`.

## Canonical recipe (generated from src/knowledge/ — edit there, then `npm run gen:knowledge`)

<!-- BEGIN GENERATED: flow-recipe -->
### Set up staking (reward tier) (`staking_setup`)

Create a staking reward tier: resolve/deploy the StakingProposal contract, pass a create_staking_tier proposal, then holders stake and claim.
- **chain 97:** STAKING DOES NOT EXIST ON TESTNET (97) — every testnet GovUserKeeper predates it and stakingProposalAddress() reverts. Do NOT attempt staking transactions on 97; run this flow on mainnet (chain 56) and tell the user why.

**Ask the user:**
- `govPool` — Which DAO (govPool address)?
- `rewardToken` — Which token funds the staking rewards (address, or native BNB)?
- `rewardAmount` — Total reward pool for this tier? · ⚠ The reward amount must actually be available — an unfunded tier pays nothing.
- `window` — Staking start (startedAt) and deadline? (ask in the user's words, then compute Unix seconds from the CURRENT time; never guess the date) · ⚠ A deadline in the past is SILENTLY rejected on-chain: the execute succeeds but NO tier is created and the reward returns to the treasury. Deadline must be in the future at EXECUTE time (add voting-period headroom).

**Steps:**
1. `dexe_proposal_create` — Create the staking tier proposal. Omit stakingProposal — the composite resolves it via GovUserKeeper.stakingProposalAddress(); if the contract isn't deployed yet the error returns the EXACT dexe_tx_send payload for the one-off permissionless deployStakingProposal() transaction (it is NOT a governance proposal — never wrap it in custom/custom_abi). Send it, then re-run this SAME call.
2. `dexe_proposal_vote_and_execute` — Vote + execute — the staking tier goes live.
3. `dexe_read_staking_info` — Read the live tier back (reward pool, window) and show it to the user.

**Pitfalls (danger first):**
- 🔴 CHAIN-ASYMMETRIC (verified 2026-07-23): on fresh TESTNET (97) pools, EXECUTING a proposal whose action is GovSettings.addSettings reverts 'disallowed tx pattern' — deterministically, re-running never helps. This hits change_voting_settings WITHOUT settingsIds, new_proposal_type, and enable_staking. On current MAINNET (56) fresh pools addSettings EXECUTES fine (proven 2026-07-22) — testnet runs an older protocol deployment. On 97: EDIT existing settings instead (pass settingsIds) — editSettings is always allowed — and do NOT use testnet to validate addSettings-based flows.
- 🔴 Staking DOES NOT EXIST on BSC testnet (chain 97): every testnet GovUserKeeper predates the staking implementation and stakingProposalAddress() reverts. Do not attempt staking transactions on 97 — plan the staking leg on mainnet (chain 56) and tell the user so.
- 🔴 NEVER guess dates for sale/staking windows — compute Unix timestamps from the CURRENT time (ask the user or read the latest block; your idea of 'now' may be a stale year). Windows must be in the future AT EXECUTE TIME (add headroom for the voting period). A staking tier with a past deadline is SILENTLY rejected on-chain (the execute succeeds, a StakingRejected event fires, NO tier exists, the reward bounces back); a sale tier with a past window is created dead-on-arrival (every buy reverts 'TSP: token sale is over'). The builders refuse past end-times before any transaction.
- ℹ The StakingProposal contract address is NOT in the registry or predicted addresses. Resolve it the way the frontend does: GovPool.getHelperContracts().userKeeper → GovUserKeeper.stakingProposalAddress(). Zero address = not deployed yet → deploying it is ONE permissionless direct transaction (GovUserKeeper.deployStakingProposal(), selector 0x82e97c92) sent via dexe_tx_send — NEVER a governance proposal, never custom/custom_abi. dexe_proposal_create(create_staking_tier) auto-resolves when stakingProposal is omitted and its error returns the exact paste-able TxPayload; then re-run the SAME call.
- ℹ Amount strings: digits-only = RAW smallest units (wei); a decimal point ("12.5") = human units scaled by the token's REAL on-chain decimals (never assumed 18). Durations and delays are SECONDS (86400 = 1 day). Composite quorum/percent params are plain percent numbers (51).

_For the machine-readable plan (interview questions with risk notes, step templates with `flowContext` chaining), call the `dexe_guide` tool with `flow:"staking_setup"`._
<!-- END GENERATED: flow-recipe -->

Related: [[dexe-create-proposal]], [[dexe-vote-execute]].
