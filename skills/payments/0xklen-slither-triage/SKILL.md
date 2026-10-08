---
name: slither-triage
description: Use when slither produces detector findings and you must decide which are real. Runs the tool, filters noise detectors, and writes a minimised Foundry PoC for each true positive.
---

# Slither triage

Static analysis floods you with findings; the job is not to run it but to separate exploitable true positives from known-benign noise and prove each one.

## Procedure

1. Install and run:

```
slither . --config-file slither.config.json
slither . --print human-summary
```

2. Use a config that fails the build only on chosen detectors:

```json
{ "detectors_to_exclude": "naming-convention,solc-version,pragma,assembly", "exclude_informational": false, "exclude_low": false }
```

3. Triage by severity and reachability: `reentrancy-eth`, `arbitrary-send-erc20`, `delegatecall-loop`, `controlled-delegatecall`, `unprotected-upgrade`, `tx-origin`, `unchecked-transfer`, `incorrect-equality`.
4. For each finding, click to the source line and decide: is the path reachable by an unauthorised caller with attacker input?
5. Suppress a confirmed-benign finding with an inline comment, which the tool respects:

```solidity
// slither-disable-next-line reentrancy-events
emit Refunded(user, amount);
```

6. Re-run and confirm it disappears: `slither . 2>&1 | grep -c "reentrancy-events"` returns 0.
7. For each true positive, write a minimal Foundry test that triggers it — a Slither finding without a PoC is a hypothesis.
8. Cross-check with a second analyser (`aderyn` or `mythril`) so a detector-specific false negative is caught.
9. Run `slither . --print inheritance-graph` to reason about which contract actually owns the flagged function.
10. Record: detector, severity, source line, reachability, verdict, and PoC test name.

## Pitfalls

- `reentrancy-eth` fires on every `.call{value:}` even with a `nonReentrant` guard; check the guard before chasing it.
- `unchecked-transfer` false-positives on `SafeERC20` unless the library path is followed; confirm the return is checked.
- `tx-origin` in a test harness is benign; in a funded contract it is the classic phish.
- Excluding `assembly` wholesale hides real storage bugs; exclude it only per finding.
- Treating informational findings (naming) as zero-value misses the signal that a function name contradicts its behaviour.

## Verification

    slither . --config-file slither.config.json > slither.txt 2>&1; grep -cE "^(INFO|LOW|MEDIUM|HIGH)" slither.txt

Pass: every HIGH/MEDIUM is either annotated with `slither-disable-next-line` and justified, or has a linked PoC test.

Report the detector counts, the true positives with PoC names, and the suppressed lines.
