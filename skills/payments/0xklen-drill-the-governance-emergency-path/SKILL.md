---
name: drill-the-governance-emergency-path
description: Use when rehearsing a DAO's emergency response before it is needed. Runs a malicious proposal through a fork, exercises the cancel and guardian path, and times the response.
---

# Drill the governance emergency path

An emergency power that has never been used is a rumour, not a control. Rehearse the whole path on a fork: propose the attack, detect it, cancel it, and measure how long the drill took.

## Procedure

1. Fork mainnet (or the DAO's chain) at the current head into a test:
   `forge test --match-contract EmergencyDrill --fork-url $RPC -vvv`
2. In the test, impersonate a proposer with enough weight and submit a payload that looks benign but transfers treasury funds to an attacker address:
   `vm.prank(proposer); governor.propose(targets, values, calldatas, description);`
3. Run detection: decode the calldata and assert your check flags the unknown recipient. If the check does not fire, the detector is the finding.
4. Exercise the cancel path exactly as it would run in production, via the guardian:
   `vm.prank(guardian); governor.cancel(targets, values, calldatas, descHash);`
   then `assertEq(uint8(governor.state(proposalId)), uint8(IGovernor.ProposalState.Canceled));`
5. Measure the response window: the test timestamps between propose and cancel must fit inside the timelock delay; assert it.
6. Also test the failure case: a payload the governor cannot cancel (already executed) should assert the state is Executed and the drill records that the window was missed.
7. Record the drill: who detects, who cancels, the elapsed blocks, and the venue (forum or council chat) within one page.

8. Time the detection and cancel steps separately, and assert each fits the real-world SLA the DAO agreed.
9. Restore the fork and re-run to confirm the result is deterministic, not a one-off.
10. File the drill result against the emergency runbook so the next responder reads a rehearsed path, not a guess.

## Pitfalls

- Drilling with a benign payload so the cancel path is never actually needed; use the malicious shape or the rehearsal proves nothing.
- Forgetting to impersonate the right caller; the guard `onlyGuardian` reverts and the test hides a broken cancel function.
- Assuming the guardian's key is available in an emergency; a drill should include retrieving the key or reaching the signer.
- Measuring the delay with `block.timestamp` left untouched; advance time explicitly (`vm.warp`) so the timelock boundary is tested.
- A drill that only tests cancel and never tests "the attack already executed", so nobody knows what the recovery is.

- A drill that cancels with unlimited gas and no mempool competition overstates the real response speed.
- Assuming the guardian is a single EOA when it is a council multisig; the drill must collect the real threshold.
- Forgetting to assert the attacker's payload never executed; a green cancel with a fired execute is a failed drill.

## Verification

    forge test --match-contract EmergencyDrill --fork-url $RPC -vvv
    # expect PASS on detection, cancellation before the timelock, and an explicit record of the elapsed blocks

Report the drill outcome: payload detected, cancelled before execution, elapsed time within the delay, and any step that failed, with the test output quoted.
