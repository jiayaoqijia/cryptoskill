# Labelled scales need a deadband (grade jitter → false alerts)

Proven 5 Oct 2026 on the portfolio risk monitor (`porto_risk.py`, cron `*/30` + dashboard).

## Symptom the user reports

"Why did TAO's grade go from B to C?" — nothing about the asset changed. The health score sat
**exactly on the B band boundary (62)**: seven consecutive runs graded it `B` (62, 62, 63, 62, 62),
then one run computed 61 → `C`. Because the grade drives the action text (`B` = *TAHAN*,
`C` = *KURANGI bobot*), the flip looked like a regime change and fired a "grade B→C" alert.

Root cause of the ±1 wobble: a component that is itself a ratio of two live numbers (here "alpha",
the token's 7d return vs BTC's cached 7d return) moves 0.2–0.5 of a point between runs, and the
score's integer rounding then crosses the threshold.

## The fix (10 lines, apply to every discrete scale you grade on)

```python
def band(h):                       # thresholds stay in one place
    if h >= 78: return "A"
    if h >= 62: return "B"
    if h >= 45: return "C"
    return "D"

def grade_for(health, prev_grade):
    """Deadband 1 poin: turun kelas harus jatuh >=1 poin DI BAWAH batas; naik kelas cukup menyentuh."""
    b = band(health)
    if prev_grade and prev_grade in "ABCD" and "ABCD".index(b) > "ABCD".index(prev_grade):
        return band(health + 1)     # masih di dalam toleransi -> tahan grade lama
    return b
```

- Load `prev_grade` (and any portfolio-level grade) from the **history file** before the loop, so
  the comparison is against the last published label, not the last computed number.
- Apply the same helper to aggregate/portfolio grades, not just per-entity ones.
- Unit-test the edges: `61/prev B → B` · `60/B → C` · `62/prev C → B` (upgrade on touch) ·
  `78/prev B → A` · no-prev → raw band. Ten asserts, and they catch the whole class.
- Add the anti-jitter rule to the skill/memory of the pipeline, because a future reader will
  otherwise "simplify" it back to inline thresholds.

## Why it matters beyond this case

Any pipeline that (a) grades into A–F/tiers, (b) alerts on grade *changes*, or (c) maps grade →
recommended action, will produce periodic false alarms whenever a score can hover on a boundary.
The deadband is cheaper than explaining the alert every month — and cheaper than the user losing
trust in the alerts that are real.

## Reporting it honestly

When the user asks "why did it change?", answer with the numbers: the run-by-run score trail, which
component wobbled and why, the band boundary, then the fix and its edge-case tests. Also say what
*would* be a real signal (e.g. score falling to ≤60) so the deadband isn't mistaken for "the alert
will never downgrade".
