---
name: verification-loops
domain: collaboration/verification-loops
trigger: "Accepting or auditing work produced by another agent; checking files on disk; running independent validation passes"
anti_trigger: "Trusting chat return text without inspecting disk files; having the producer grade its own output"
scope: "Accepting agent work: verify file on disk; validator differs from producer; adversarial passes for load-bearing claims; cost trade-off"
status: seedling
---

# Verification Loops

## Standard

- **ISO/IEC/IEEE 29148 Requirements Engineering**: verification requires independent inspection of deliverables against pre-stated acceptance criteria, distinct from the generation process. <https://iso.org/standard/45171.html>
- **Producer-validator independence**: validation must be executed by an entity with no authorship stake in the artifact to prevent confirmation bias and blind spot propagation.
- **House rule on returns**: an empty or truncated chat return is not a failure if the target file on disk is complete and passes verification checks. ⚠️ House threshold.

## Decision rules

1. Never accept a subagent's work based solely on its chat summary; always inspect the output file on disk.
2. The validator agent or review pass must be executed independently of the producer agent.
3. For load-bearing claims or critical artifacts, run an adversarial review pass to test assertions against counter-evidence.
4. If the cost and time of independent validation exceed the cost of re-performing the task directly, perform a lightweight structural check instead. ⚠️ House threshold.
5. If an output file is missing or truncated, treat it as a task failure and initiate recovery procedures rather than accepting partial prose.
6. Verify that all hard constraints (word caps, format rules, negative boundaries) were obeyed in the final file.

## Procedure

1. Locate the output file path specified in the subagent delegation contract.
2. Check file existence, size, and incremental completion markers on disk.
3. Dispatch an independent validator agent or review pass with the requirements and the output file.
4. Run verification checks: test assertions, check citation links, verify constraint adherence.
5. If validation passes, record the success and archive the artifact.
6. If validation fails, compile specific defect notes and route back to recovery.

## Anti-patterns

- **Taking chat word for it.** Believing the agent's claim that "the task is complete" without checking disk files. Fix: inspect the file.
- **Self-certification.** Allowing the producing agent to sign off on its own deliverable. Fix: assign an independent validator.
- **Ignoring truncation.** Accepting a truncated report because the chat message sounded polite. Fix: treat truncation as failure.
- **Infinite review loops.** Spending more time validating a minor script than writing it. Fix: apply cost proportionality.

## Done checklist

- [ ] Output file inspected directly on disk.
- [ ] Independent validator reviewed the artifact.
- [ ] Hard constraints and format rules verified.
- [ ] Adversarial checks run on load-bearing claims.
- [ ] Verification result recorded in operation ledger.

## Sources

- ISO/IEC/IEEE 29148 Requirements Engineering: <https://iso.org/standard/45171.html>
- Internal operational standards for independent verification and artifact acceptance.
