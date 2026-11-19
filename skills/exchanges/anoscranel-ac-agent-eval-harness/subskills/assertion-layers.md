---
name: assertion-layers
domain: software-engineering/assertion-layers
trigger: "Choosing what the harness asserts and at what depth."
anti_trigger: "Not for guardrail enforcement, and not for live-run metrics."
scope: "What to assert at each depth, from answer to tool call."
status: seedling
---

# Assertion layers

## Standard

Agent runs can be asserted at four depths, and each catches a different defect class. Final answer: the user-visible result — semantic match against a reference, not string equality. Tool-call sequence: which tools were called, in what order, with what key arguments. Per-call behaviour: did a specific call use correct parameters, respect its contract, get handled when it errored. Internal bookkeeping: guardrail checks fired, budget respected, loop terminated by design.

Depth choice is the discipline. Deep assertions catch more and flake more: an exact tool-call sequence pins the agent's exploration strategy and fails on harmless variation. The working posture is strict on the invariants — irreversible actions never called, budget never crossed, required calls always made — and loose on the path: semantic answer match constrained-set assertions on calls whose order is free. Assert the contract, not the improvisation.

Primary sources: <https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html> and <https://testing.googleblog.com/>.

## Decision rules

- Choose assertion depth per scenario, recorded with the scenario, not at authoring whim.
- Assert invariants strictly: irreversible calls absent, budgets respected, required calls present.
- Assert the path loosely: sets or DAGs over strict sequences where order is free.
- Semantic match on answers, graded by explicit rubric, never raw string equality.
- Every failed assertion links to a defect class to make triage mechanical.
- A scenario whose assertion cannot fail is deleted — it is decoration.

## Procedure

1. Mark each scenario's invariants: calls that must/must-not happen, budgets, terminals.
2. Choose the answer assertion: exact, semantic rubric, or property.
3. Choose the path assertion: sequence, set, or per-call checks.
4. Write assertions as named rules linked to defect classes.
5. Dry-run each scenario once; verify it can actually fail against a plausible mutant.
6. Record assertion depth and rationale with the scenario.

## Anti-patterns

- String equality against a live model's answer.
- Exact sequence assertion on an exploration phase that is free to vary.
- Assertions that cannot fail — always green means always meaningless.
- Depth chosen by copy-paste from the previous scenario.
- Answer-only assertions on scenarios whose point is the tool behaviour.

## Done checklist

- [ ] Invariants identified per scenario.
- [ ] Depth chosen and recorded.
- [ ] Semantic rubric on answers.
- [ ] Set/DAG where order is free.
- [ ] Mutant dry-run proves each assertion can fail.
- [ ] Defect-class linkage on every assertion.

## Sources

- Test intent over implementation coupling: <https://testing.googleblog.com/2015/04/just-say-no-to-more-end-to-end-tests.html>
- Testing blog archive: <https://testing.googleblog.com/>
- Testing craft: <https://en.wikipedia.org/wiki/Software_testing>
