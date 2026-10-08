---
name: label-observations-vs-inferences
description: Use when reporting findings that mix raw data with your interpretation. Mark what you saw separately from what you conclude, so the reader can judge each.
---

# Label observations vs inferences

A cause stated as a fact is an inference wearing a lab coat. Separating the measurement from the explanation lets the reader trust each on its own evidence.

## Procedure

1. For every claim, decide: is this a measurement or an interpretation? Tag it `observed` or `inferred`.

2. Observations carry a source: command, file, line, and timestamp.

3. Inferences carry the observation they rest on and the alternative explanations you ruled out.

4. Word observations as reported facts ("the log shows 12 timeouts at 14:03"), never as causes.

5. Word inferences as hypotheses ("this suggests the pool exhausted") with a test that would confirm it.

6. Keep the two in separate sections or columns; never let a cause masquerade as a datum.

7. When unsure, downgrade to `inferred` and name the missing evidence.

## Pitfalls

- "The server crashed because of memory" states a cause as fact; that is an inference.
- Stacking inference on inference with no new observation compounds the error.
- Omitting the source makes an observation unverifiable.
- Confirmation bias: collecting only observations that fit the chosen hypothesis.
- Presenting one observation as a pattern; a single timeout is not a trend.

## Verification

    grep -cE "\b(observed|inferred):" findings.md   # every claim tagged

Separate measured facts from conclusions; give each its own evidence line.
