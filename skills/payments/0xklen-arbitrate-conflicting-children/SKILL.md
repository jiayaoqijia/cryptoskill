---
name: arbitrate-conflicting-children
description: Use when two subagents report contradictory facts, results, or recommendations. Decides between them with a reproducible check and an explicit rule rather than averaging or trusting the louder child.
---

# Arbitrate Conflicting Children

Two children disagreeing is information, not noise. Resolve it by weighing their evidence against the same standard — never by averaging claims or trusting the more confident voice.

## Procedure

1. Restate each child's claim as a single falsifiable sentence, side by side.
2. Find what the claims actually disagree about: method, source, scope, or a definition. Many conflicts dissolve once the axis is named.
3. Check each child against its brief: a child that answered a different question is not a valid comparator.
4. Ask each for its evidence — the command run, its output, the source — not just the conclusion.
5. Re-run the decisive check yourself, once, from a neutral process, so neither child's log is taken on faith.
6. Prefer the claim backed by a reproducible command over the claim backed by reasoning alone.
7. If the evidence is genuinely symmetric, examine scope: the narrower, more testable claim usually wins.
8. Where they conflict on a fact neither can settle, mark it UNRESOLVED and escalate; do not fabricate a tiebreak.
9. Write the decision and its basis in `notes/arbitration.md`: axis, winner, evidence, loser-dismissed-because.
10. Feed the resolution back so descendants do not re-litigate the same conflict.

## Pitfalls

- Averaging two contradictory numbers into a third that no child computed and no evidence supports.
- Picking the child whose message sounded more confident or ran longer.
- Letting the child that reported last win, when order has nothing to do with correctness.
- Declaring a tie and shipping both values, leaving the consumer to guess.
- Resolving on a definition dispute without noticing the children meant different things by the same word.

## Verification

```bash
test -s notes/arbitration.md && grep -c 'evidence' notes/arbitration.md
# passes when the decision names the axis, the winning evidence, and the re-run command
```

Report to the user: the axis of disagreement, the winner with its evidence, and any fact left UNRESOLVED.
