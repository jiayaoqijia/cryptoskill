---
name: structured-pre-audit-pass
description: Use when starting a security review of a codebase before a formal audit or a deploy. Runs a fixed pre-audit checklist across build, scope, invariants and known vulnerability classes.
---

# Structured pre-audit pass

A pre-audit pass is a fixed, ordered sweep that produces a scope map and a triaged finding list — it exists so a formal audit (or a deploy) starts from known state, not a blank page.

## Procedure

1. Freeze scope: record the commit hash (`git rev-parse HEAD`), the file list under audit, and out-of-scope dependencies.
2. Build and test clean: `forge build && forge test` must pass with 0 failures before any manual review.
3. Run the size and layout checks: `forge build --sizes` and `forge inspect <C> storage-layout` for every contract holding funds.
4. Map the system: for each contract, list external entry points, privileged functions, and assets it controls. Write the result to `scope.md`.
5. Walk the known-vuln checklist against the map (SWC / OWASP SCSVS): reentrancy, access control, oracle, flash loan, rounding, ERC-20 quirks, proxy, size.
6. Run the automated tools and record raw output: `slither .`, `forge test --match-test invariant`, `forge test --fuzz-runs 5000`.
7. For each candidate finding, write the *reachability* argument: who calls it, with what input, at what cost.
8. Rank findings: critical (funds at risk, no preconditions), high (funds at risk with a precondition), medium (griefing/DoS), low/informational.
9. Produce a PoC or a written trace for every critical/high; skip nothing above medium without a stated reason.
10. Write handover notes: what was tested, what was not, open questions for the auditors, and the tool versions.

## Pitfalls

- Reviewing against `main` while the deploy branch differs; freeze the exact commit.
- Trusting the test suite: 100% line coverage says nothing about adversarial paths, only that lines executed.
- Skipping the storage-layout check on a proxy upgrade because "nothing changed" — an inherited base reorder breaks it.
- Running Slither once and treating zero HIGH as "safe"; it is a floor, not a ceiling.
- No written scope, so the auditors double-check the boring parts and miss the novel logic.
- Forgetting to record the Solidity version and dependency versions (`forge --version`, `git submodule status`), so a finding cannot be reproduced later.

## Verification

    forge build && forge test && slither . --config-file slither.config.json

Pass: build and tests clean, Slither output captured to a file, `scope.md` lists every in-scope contract with its entry points, and each critical/high has a PoC link.

Report the commit hash, the finding counts by severity, and what was left unverified.
