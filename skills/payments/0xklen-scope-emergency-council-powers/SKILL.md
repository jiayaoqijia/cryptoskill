---
name: scope-emergency-council-powers
description: Use when designing or reviewing a DAO's emergency council or guardian role. Constrains it to pause and cancel, denies it treasury and parameter power, and encodes the boundary in a test.
---

# Scope an emergency council's powers

An emergency council earns its place by stopping damage fast, but if it can also move funds it becomes an unaccountable treasury. Grant the minimum: cancel or pause, never spend or upgrade.

## Procedure

1. Enumerate candidate powers and split them into reversible-stop and value-moving:
   - STOP: `cancel()` a malicious proposal, `pause()` a pausable contract, a guardian veto on the governor.
   - SPEND/UPGRADE: transfer treasury funds, grant roles, upgrade a proxy, change parameters.
2. Grant only STOP powers to the council; hold SPEND behind the full governance process.
3. Read the current guardian and its privileges on-chain:
   `cast call $GOV "guardian()(address)" --rpc-url $RPC`
   `cast call $TIMELOCK "hasRole(bytes32,address)(bool)" $CANCELLER_ROLE $COUNCIL --rpc-url $RPC`
4. Verify the council cannot execute: it should hold `CANCELLER_ROLE` but not `EXECUTOR_ROLE` or `PROPOSER_ROLE` on the timelock.
5. Bound the council in time: powers expire unless renewed, or require a governance vote each term.
6. Write a test asserting the boundary — a fork test that attempts a spend from the council and expects a revert:
   `forge test --match-test testCouncilCannotSpend --fork-url $RPC`
7. Require public disclosure of every use of emergency power within one epoch, with the proposal id cancelled.

## Pitfalls

- Giving the council `PROPOSER_ROLE` "for emergencies"; it can then queue arbitrary transactions and the emergency framing is gone.
- A guardian that is a single EOA: an emergency power concentrated in one key is an attack surface equal to the risk it guards.
- Unlimited-duration emergency powers that are never reviewed; scope creep is invisible without a term limit.
- Pausing without a plan to unpause; a council that can stop but not restart becomes a permanent censor.
- Silent use of the veto; an unexplained cancel is indistinguishable from censorship.

## Verification

    cast call $TIMELOCK "hasRole(bytes32,address)(bool)" $CANCELLER_ROLE $COUNCIL --rpc-url $RPC
    # true for CANCELLER, false for EXECUTOR and PROPOSER

Report the powers held, the role booleans read, and the test name proving a spend reverts, with the commands behind them.
