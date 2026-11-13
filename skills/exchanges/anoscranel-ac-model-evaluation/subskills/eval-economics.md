---
name: eval-economics
domain: prompt-engineering/eval-economics
trigger: "Sizing evaluation spend to the decision it serves."
anti_trigger: "Not for cloud cost attribution, and not for API rate-limit operations."
scope: "Cost, cadence, and how much eval a decision needs."
status: seedling
---

# Eval economics

## Standard

Evaluation costs money on every run — tokens for outputs, tokens for any model judge, human time for the residue — and the suite's size sets that recurring bill. The right size follows from the decision's stakes: an infrequent adopt-decision between two frontier models deserves a deep, human-graded suite run once; an upgrade-guard suite guarding every model release runs cheaply forever and keeps only what catches regressions at that cadence. A giant suite run on every change is a cost defect, and a two-case suite guarding a revenue-critical product is an evidence defect.

Cost per run is a design variable with several levers: case count, output length, judge usage, and sampling `n` all scale the bill, and each can be trimmed against its measurement value. The record of an eval's economics — cost per run, cadence, and what each slice buys — belongs beside the results, because the expense of a suite is the usual reason it silently rots: unaffordable suites stop running, and a suite that stops running is a suite lying that it passed last time.

Primary sources: <https://docs.anthropic.com/en/docs/about-claude/evaluate> and <https://github.com/EleutherAI/lm-evaluation-harness>.

## Decision rules

- State the decision's stakes and choose suite depth from them.
- Separate the deep one-time adopt suite from the cheap recurring regression suite.
- Compute the cost per run before the first run, not after the invoice.
- Trim cost levers by their measurement value: case count, output length, judge tiers, sampling n.
- Record cadence with cost, and mark what each cadence can and cannot detect.
- Retire cases that have not changed a decision in their lifetime.

## Procedure

1. Write the decisions the suite serves and their cadence.
2. Price a full run: tokens, judge calls if any, and human grading time.
3. Compare the recurring budget to the price; trim levers until they match.
4. Split deep suites from recurring suites rather than running one size for both.
5. Record per-run cost, cadence, and coverage per suite.
6. Audit the suite yearly for cases that never discriminate; retire them.

## Anti-patterns

- A suite whose size was never priced.
- Deep human grading re-run on every minor release.
- Judging outputs a deterministic check could score, forever.
- A giant suite that quietly stopped running.
- A two-case guard on a revenue-critical path.

## Done checklist

- [ ] Decision cadence stated per suite.
- [ ] Cost per run computed before adoption.
- [ ] Levers trimmed by measurement value.
- [ ] Deep and recurring suites split.
- [ ] Cadence recorded with cost.
- [ ] Dead cases retired on audit.

## Sources

- Claude evaluation guidance: <https://docs.anthropic.com/en/docs/about-claude/evaluate>
- Harness execution practice: <https://github.com/EleutherAI/lm-evaluation-harness>
- Ragas evaluation documentation: <https://docs.ragas.io/en/latest/>
