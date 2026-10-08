---
name: separate-correlation-from-causation
description: Use when two measurements move together and you are tempted to say one caused the other. List the rival explanations and test one before asserting any mechanism.
---

# Separate correlation from causation

Co-movement is cheap; mechanism is expensive. This skill forces the rival explanations onto the page and demands a test before a causal sentence leaves your mouth.

## Procedure

1. Write the correlation as measured, with the numbers: "X and Y both rose between t1 and t2".

2. Compute the association rather than eyeballing it: `python3 -c "import numpy as np; print(np.corrcoef(x,y)[0,1])"`.

3. Before claiming cause, enumerate the rivals: reverse causality (Y drives X), a common cause (Z drives both), selection effects, coincidence, and a shared time trend.

4. For each rival, name the observation that would support it. If you cannot imagine one, the rival is not testable and should be dropped.

5. Test at least one rival directly if you can: hold Z constant, or find a period where X moved and Y stayed flat.

6. Check the number of observations. Report n alongside the coefficient; a correlation from four points is noise.

7. Assert "X causes Y" only when you have a stated mechanism AND evidence that varying X while holding confounders still moves Y. Otherwise report the association with the word "associated".

## Pitfalls

- Two rising time series correlate near-automatically; detrend before believing any slope.
- A plausible story is not a mechanism; the story must predict a checkable outcome you then ran.
- Selecting the window after seeing the graph is p-hacking by hand; fix the window first.
- Ignoring a shared seasonal or launch event invents a cause out of calendar alignment.
- A single before/after change is confounded by everything else that changed at that time.

## Verification

    python3 -c "import numpy as np; print(np.corrcoef(X, Y)[0,1])"

Report the coefficient, the n, and the untested rivals; say "associated", not "caused", unless tested.
