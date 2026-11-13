---
name: pre-trade-memo
domain: crypto-trading/pre-trade-memo
trigger: "Writing the trade memo before exposure; recording thesis, evidence, invalidation, size, and book state"
anti_trigger: "Entering a trade without a written record; executing on intuition or live price movement"
scope: "The decision record written before exposure: thesis, evidence, invalidation, size, and book state"
status: seedling
---

# Pre-Trade Memo

## Standard

- **Klein, _Sources of Power_ (1998)**: decision makers rely on structured mental simulation and explicit written scenarios rather than unverified intuition. <https://mitpress.mit.edu/9780262611485/>
- **Schoemaker & Tetlock, "Building a Decision-Analytic Framework" (2012)**: recording rationale before an event prevents hindsight bias and post-hoc rationalisation. <https://www.jstor.org/stable/23253303>
- **Malkiel, _A Random Walk Down Wall Street_ (1973)**: documentation of assumptions protects capital from emotional momentum. <https://wwnorton.com/books/9780393358440>
- **Tversky & Kahneman, "Judgment under Uncertainty" (1974)**: decision records counter availability heuristics by forcing exhaustive enumeration of assumptions. <https://www.science.org/doi/10.1126/science.185.4157.1124>
- ⚠️ House convention: a trade executed without a pre-trade memo is recorded as an unassigned risk event.

## Decision rules

1. Exposure never precedes documentation; the memo must be committed before any order reaches an execution interface.
2. The thesis must state the directional hypothesis, time horizon, and required market condition.
3. Every claim of evidence must cite a verifiable data source; unverified beliefs are inadmissible.
4. Invalidation conditions must be specified numerically before entry.
5. Intended size must be derived from the risk budget, not from conviction.
6. Existing book state and correlation limits must be recorded.
7. ⚠️ House: any memo altered after placement invalidates the audit trail.

## Procedure

1. Open a new record in the trading journal repository with a timestamp identifier.
2. Draft the thesis paragraph: state expected market conditions and time horizons.
3. List supporting evidence with source URLs or data references.
4. Define the numeric invalidation price level and time threshold.
5. Record entry zone, stop distance, and risk-derived target structure.
6. Audit existing open positions against aggregate correlation caps.
7. Review memo against decision rules and commit the file before ordering.

## Anti-patterns

- **Memo written after entry.** Entering on price movement and writing justification afterward. Fix: stop trading and close untracked risk immediately.
- **Vague thesis.** Writing broad statements without conditions. Fix: specify exact structural triggers.
- **Missing source.** Asserting data without naming where observed. Fix: attach exact URLs.
- **Floating invalidation.** Moving stops further away. Fix: invalidation is fixed at entry.
- **Ignoring book state.** Opening positions while blind to existing exposure. Fix: review aggregate risk first.

## Done checklist

- [ ] Memo timestamp precedes execution timestamp.
- [ ] Thesis is stated in one paragraph with a time horizon.
- [ ] Supporting evidence includes verifiable sources.
- [ ] Invalidation conditions are defined numerically.
- [ ] Position size is derived from the risk budget.
- [ ] Existing book state and correlation limits are recorded.

## Sources

- Klein, _Sources of Power_: <https://mitpress.mit.edu/9780262611485/>
- Schoemaker & Tetlock, "Building a Decision-Analytic Framework": <https://www.jstor.org/stable/23253303>
- Malkiel, _A Random Walk Down Wall Street_: <https://wwnorton.com/books/9780393358440>
- Tversky & Kahneman, "Judgment under Uncertainty": <https://www.science.org/doi/10.1126/science.185.4157.1124>

⚠️ Gaps: behavioral compliance with pre-trade documentation under high volatility remains dependent entirely on operator self-enforcement.
