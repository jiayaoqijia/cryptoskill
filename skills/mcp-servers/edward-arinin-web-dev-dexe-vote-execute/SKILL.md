---
name: dexe-vote-execute
description: |
  Vote on and execute a DeXe proposal with `dexe_proposal_vote_and_execute`.
  Covers deposit-first, the canonical ProposalState ordering, and the
  "tokens locked after execute — withdraw between proposals" trap. Use when the
  user says "vote on proposal N", "execute proposal N", "pass this proposal".
---

# dexe-vote-execute

`dexe_proposal_vote_and_execute` reads proposal state, optionally deposits,
votes, and (when `autoExecute`) executes once the proposal succeeds. With
`DEXE_PRIVATE_KEY` it broadcasts; otherwise it returns ordered `TxPayload`s.

## Recipe

Call **`dexe_context`** first for the signer, active chain, recent proposals,
and your deposited power in the most recent DAO.

```jsonc
dexe_proposal_vote_and_execute({
  govPool: "0x…",
  chainId: 97,
  proposalId: 1,            // 1-indexed
  isVoteFor: true,
  depositFirst: "auto",     // the default — deposits the shortfall automatically
  autoExecute: true         // execute automatically once it passes
})
```

- **`depositFirst` is `boolean | "auto"`, default `"auto"`:** when your deposited
  power is short of `voteAmount`, the tool deposits **exactly the missing
  amount** from your wallet (approve UserKeeper → deposit → vote). Pass `false`
  to never deposit (the old behavior), `true` to force a deposit.
- Already past voting (state `SucceededFor` / `SucceededAgainst` / `Locked`) →
  the tool skips the vote and goes straight to execute. Any other non-`Voting`
  state errors with a **per-state remedy** (execute / wait / new proposal).
- `voteAmount` defaults to all available deposited power. Pass it to vote with
  less — human units (`"250.5"`) or raw wei both work.

## Validator round — driven automatically (`driveValidatorRound`, default true)

DAOs with validators use **two-stage** voting: members first, then validators.
After the member vote a proposal lands in `WaitingForVotingTransfer (1)` or
`ValidatorVoting (2)` — NOT directly executable. With `autoExecute` +
`driveValidatorRound` (both default true) the tool now drives that stage for you:

1. `GovPool.moveProposalToValidators(id)` (member-passed → validator queue), then
2. if the **configured signer is itself a validator** with a balance:
   `GovValidators.voteExternalProposal(id, balance, isVoteFor)`
   ⚠ arg order differs from `GovPool.vote` — **amount BEFORE isVoteFor**, then
3. re-reads state; if `SucceededFor/Against` → `execute`.

If the signer is **not** a validator, it moves the proposal and stops with a
skipped-step note (the DAO's own validators must cast their votes). Set
`driveValidatorRound: false` to stop after the member vote and drive the
validator round manually (`dexe_vote_build_move_to_validators` →
`dexe_vote_build_validator_vote` → `dexe_vote_build_execute`). A **re-run** of
`vote_and_execute` on a proposal already sitting in state 1/2 also advances it.

## Partial failure → fix and re-run the SAME call

A failed step returns `mode: "failed"` with a `failure` ledger:
`failedStep`, an actionable `error`, `landedSteps` (txs that DID land — gas
already spent), and `resume` guidance. Fix the cause and re-run the same call —
completed steps (approve/deposit) are detected on-chain and skipped.

## Canonical ProposalState ordering (failure mode 9)

Never hardcode a different order — `Locked` comes **after** `SucceededFor`:

```
0 Voting  1 WaitingForVotingTransfer  2 ValidatorVoting  3 Defeated
4 SucceededFor  5 SucceededAgainst  6 Locked  7 ExecutedFor  8 ExecutedAgainst  9 Undefined
```

Executable states: **4, 5, 6**.

## Tokens locked after vote/execute (failure mode 5)

After you vote/execute, your deposited tokens stay **locked** until you withdraw
them. If you try to create or vote on the *next* proposal while locked, available
power reads 0 and the action under-counts. Between proposals:

```jsonc
dexe_vote_build_withdraw({ govPool: "0x…", amount: "…" })   // then broadcast
```

Then deposit again for the next proposal (or let `dexe_proposal_create` /
`depositFirst` re-deposit).

**Locked power blocks delegation too.** A proposal that is not yet in a terminal
state (`Defeated/ExecutedFor/ExecutedAgainst`) keeps your **entire** deposited
balance locked. `GovPool.delegate` (and `withdraw`) then reverts
`GovUK: overdelegation` even for a small amount. Before delegating, make sure
every proposal you voted on is terminal — e.g. move a leftover
`WaitingForVotingTransfer` proposal to validators and let it resolve (pass or
Defeat it). `delegate()` self-unlocks terminal proposals; only active ones hold
the lock.

## Preview without broadcasting

Pass `dryRun: true` (or run with no signer) to get the ordered `TxPayload`s.

Prerequisite: [[dexe-create-proposal]].

## Canonical recipe (generated from src/knowledge/ — edit there, then `npm run gen:knowledge`)

<!-- BEGIN GENERATED: flow-recipe -->
### Vote on / pass / execute a proposal (`vote_execute`)

Vote and execute in one dexe_proposal_vote_and_execute call — auto-deposits when power is short and auto-drives the validator round.

**Ask the user:**
- `govPool` — Which DAO (govPool address)?
- `proposalId` — Which proposal id?
- `support` (optional) — Vote FOR or AGAINST? · default `for`

**Steps:**
1. `dexe_proposal_state` — Read the current ProposalState first — the valid action depends on it.
2. `dexe_proposal_vote_and_execute` — Vote with full available power (auto-deposit if needed), then — when quorum passes — move to validators, drive the validator round (if the signer is a validator), and execute.
3. `dexe_vote_build_withdraw` — After execution, withdraw the voted tokens so they're free for the next proposal. _(skip when: the user will create/vote more proposals right away — otherwise skippable)_

**Pitfalls (danger first):**
- ⚠ Canonical ProposalState order: 0 Voting, 1 WaitingForVotingTransfer, 2 ValidatorVoting, 3 Defeated, 4 SucceededFor, 5 SucceededAgainst, 6 Locked, 7 ExecutedFor, 8 ExecutedAgainst, 9 Undefined. Execute is only valid from SucceededFor/SucceededAgainst; use dexe_proposal_state to check, never guess from the number.
- ⚠ DAOs with validators add a second voting chamber: Voting → (member quorum) WaitingForVotingTransfer → moveProposalToValidators → ValidatorVoting → (validator quorum) SucceededFor → execute. Voting in the validator chamber BEFORE the move reverts 'Validators: proposal does not exist'. dexe_proposal_vote_and_execute auto-drives the whole validator round when the signer is a validator; pass driveValidatorRound:false to stop after the member vote.
- ⚠ Tokens you voted with stay LOCKED per-proposal even after the proposal executes, and votingPower() reads 0 while locked (it shows available, not deposited, power). Between proposals run dexe_vote_build_withdraw to unlock, or the next create/vote fails with 'No voting power available'.
- ⚠ On fresh (SphereX-era) pools a cast VALIDATOR vote cannot be cancelled — GovValidators has no multicall, and raw cancelVote{Internal,External}Proposal is blocked in every shape. Top-up re-votes ARE allowed. Warn validators before they vote.
- ⚠ Raw top-level vote()/delegate() calls REVERT on fresh (SphereX-era) pools — the frontend always wraps them as GovPool.multicall([call]) even for a single call, and the dexe-mcp builders emit that shape since v0.24.1. If you hand-craft calldata, wrap it. Raw deposit/withdraw/cancelVote/undelegate/createProposal(AndVote) remain allowed.
- ℹ Delegation is ONE level: a delegator delegates only their OWN deposited balance; received delegations cannot be re-delegated (hub-and-spoke, never chains). Effective voting power = own deposited + incoming delegations — verify with dexe_vote_user_power (totalBalance).

_For the machine-readable plan (interview questions with risk notes, step templates with `flowContext` chaining), call the `dexe_guide` tool with `flow:"vote_execute"`._
<!-- END GENERATED: flow-recipe -->
