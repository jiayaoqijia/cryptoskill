---
name: state-confidence-plainly
description: Use when reporting something you are not fully sure of. Say how sure you are in plain words tied to evidence, instead of vague hedging or false certainty.
---

# State confidence plainly

"I think" tells the reader nothing about how much to rely on you. A plain label tied to the evidence, or the gap in it, is what they can act on.

## Procedure

1. For each claim, set a level: `certain` (verified by a command), `likely` (strong indirect evidence), or `unsure`.

2. Tie the label to a reason: "certain — `pytest` passes on the changed module".

3. Replace unquantified hedges (`I think`, `maybe`, `probably`) with a label; the hedge carries no information.

4. When unsure, name the missing evidence and how to obtain it.

5. Never round `unsure` up to `certain` to look decisive; say what you actually checked.

6. Separate verified facts from assumptions across the whole report.

7. If asked to bet on an outcome, give the bet and the odds plainly.

## Pitfalls

- "Fairly confident" with no basis is noise; give the evidence or the gap.
- Hedging every claim equally makes the verified ones indistinguishable from guesses.
- False certainty on an unverified claim is the expensive error; label it down.
- Saying "not sure" without the missing piece leaves the reader with no next step.
- Confusing confidence with importance; a certain trivial fact still needs its context.

## Verification

    grep -cE "\b(certain|likely|unsure)\b" report.md   # each claim labelled with its basis

Label each claim's confidence with the evidence behind it; never inflate certainty.
