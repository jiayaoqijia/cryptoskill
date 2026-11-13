---
name: suppressions-and-baselines
domain: software-engineering/suppressions-and-baselines
trigger: "Managing exceptions without letting them become the rule."
anti_trigger: "Not for the fix itself, and not for review practice."
scope: "The honest exception: reason, scope, and expiry."
status: seedling
---

# Suppressions and baselines

## Standard

Every analysis deployment accumulates exceptions, and the difference between a managed tool and a dead one is what its exceptions cost. A suppression with a reason and a scope says why the finding is wrong here; an inline magic comment silencing a line says only that someone was annoyed. The first can be re-examined; the second is invisible debt, and it compounds — a suppressed spot is where the next, real finding lands unreported.

A baseline is the same idea at adoption scale: freeze existing violations, hold new code to the full standard, and burn the baseline down over time. It is honest adoption — a big bang that fixes two thousand findings never ships — and the discipline that makes it honest is measurement: the baseline shrinks or it does not, and a baseline that has not moved in two quarters is a decision nobody made.

Primary source: <https://martinfowler.com/>.

## Decision rules

- Require every suppression to carry a reason and, where supported, an expiry.
- Prefer the narrowest scope: the line, then the file, then the rule — never the tool.
- Track suppression count per rule; a rising count is a rule problem, not a code problem.
- Baseline at adoption with a recorded start size and a burn-down cadence.
- Review expiring suppressions rather than silently renewing them.
- Never suppress in generated code paths; fix the generator.

## Procedure

1. Inventory current suppressions and their stated reasons.
2. Convert bare suppressions to reasoned ones or remove them.
3. Set the baseline at adoption with a recorded count.
4. Hold new and changed code to the full rule set.
5. Schedule expiries so the suppression list resurfaces periodically.
6. Report baseline size per quarter and record the trend.

## Anti-patterns

- Bare suppress-comments with no reason.
- File-wide or tool-wide suppression for a one-line annoyance.
- A baseline that never shrinks, adopted and forgotten.
- Suppressing in generated output instead of fixing generation.
- Suppressing a probable-bug rule without recording why it is wrong here.

## Done checklist

- [ ] Suppression inventory with reasons.
- [ ] Bare suppressions converted or removed.
- [ ] Baseline set with recorded size.
- [ ] New code held to full rules.
- [ ] Expiry review scheduled.
- [ ] Baseline trend reported.

Suppressions in test code deserve their own note: a test that silences a rule is claiming the rule does not apply to a context whose entire purpose is unusual contexts, and the claim deserves a real reason rather than convenience, because tests are where the suppression is most likely to be hiding an actual broken expectation.

## Sources

- Continuous integration quality gates: <https://martinfowler.com/articles/continuousIntegration.html>
- Technical debt framing: <https://martinfowler.com/bliki/TechnicalDebt.html>
- Software quality measurement: <https://dl.acm.org/>
