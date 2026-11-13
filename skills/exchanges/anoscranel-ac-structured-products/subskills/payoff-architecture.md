---
name: payoff-architecture
domain: investing/payoff-architecture
trigger: "Reading the payoff a structured note actually promises, and drawing it."
anti_trigger: "Not for recommending a product, and not for pricing it."
scope: "Capital protection, participation, barriers, and the payoff diagram the note actually promises."
status: seedling
---

# Payoff architecture

## Standard

Every structured payoff is built from three choices: how much of the principal is exposed, how the return participates in the underlying, and what conditions switch the participation on or off. Capital protection is the first choice. Participation is the second: a note may pay a fixed multiple of the index's gain, a capped share of it, or an uncapped share with a fee. Barriers are the third: a level at which protection or participation changes, often discontinuously.

Drawing the payoff is the test of understanding. A payoff diagram plotted against the underlying at maturity shows, in one picture, the loss the holder can take, the cap on the gain, and the kink where a barrier changes the rule. A note whose payoff cannot be drawn, or whose diagram has a vertical step the seller has not explained, is a note whose risks have not been communicated.

Primary sources: <https://www.sec.gov/investor> and <https://www.finra.org/>.

## Decision rules

- Draw the payoff at maturity against the underlying, including the barrier levels.
- Record the participation rate, the cap, and whether participation is on the full gain or the average.
- Record the protection level and whether it applies at maturity only or throughout.
- Identify every discontinuity: a barrier that removes protection is a step, not a slope.
- Record what happens on early redemption, and whether the holder or the issuer controls it.
- Where averaging applies, record the observation dates and their effect.

## Procedure

1. Extract the payoff formula from the terms, not the summary.
2. Plot the payoff across a range of underlying levels, including the barrier.
3. Mark the participation, cap, and protection levels on the plot.
4. Note every point where the slope or level changes.
5. Re-plot for the early-redemption cases where applicable.
6. Record the diagram and the formula it came from.

## Anti-patterns

- Reading the marketing payoff and assuming it is the terms.
- Missing a barrier that removes protection rather than reducing it.
- Assuming a cap applies only to the upside when it also affects recovery.
- Confusing protection at maturity with protection throughout the term.
- Ignoring averaging, which changes the payoff in fast markets.

## Done checklist

- [ ] Payoff formula extracted from the terms.
- [ ] Diagram drawn across the full range.
- [ ] Participation, cap, and protection levels marked.
- [ ] Discontinuities identified.
- [ ] Early-redemption payoffs recorded.
- [ ] Diagram and formula cross-checked.

## Sources

- Structured product disclosure context: <https://www.sec.gov/investor>
- Retail product guidance and investor alerts: <https://www.finra.org/>
- Investor education on complex products: <https://www.investor.gov/introduction-investing>
