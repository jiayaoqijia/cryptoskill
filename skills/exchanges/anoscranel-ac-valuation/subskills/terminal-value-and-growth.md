---
name: terminal-value-and-growth
domain: investing/terminal-value-and-growth
trigger: "Setting and testing the terminal assumptions that dominate a valuation."
anti_trigger: "Not for the forecast period itself, and not for discount-rate choice."
scope: "Why terminal assumptions dominate the answer, and the sanity checks that keep them honest."
status: seedling
---

# Terminal value and growth

## Standard

In most discounted cash-flow models the terminal value is the majority of the answer. That is not a flaw in the modelling; it is a statement about what the model actually claims: that the business continues past the explicit forecast, and that its value then is the capitalised value of a steady state. The problem is that this largest component is the least examined.

The discipline is to make the terminal assumption explicit, small in number, and bounded by arithmetic. A business cannot grow faster than the economy forever; a terminal margin cannot exceed the best competitor's; a terminal return on capital cannot exceed what competition allows without a defended moat.

Primary sources: <https://pages.stern.nyu.edu/~adamodar/> and <https://www.sec.gov/edgar/search/>.

## Decision rules

- Terminal growth is stated as a single number with a justification tied to long-run nominal growth, never to the company's recent growth.
- Terminal growth is below the long-run growth of the economy the business operates in; a number above it requires a written argument and a warning.
- Terminal margins are justified against the best competitor and the historical range.
- Terminal return on capital is consistent with the competitive analysis; an above-cost-of-capital return forever implies a permanent moat.
- Terminal value is reported as a percentage of the total; above three quarters, the model is a terminal-value model and should say so.
- The sensitivity of the answer to terminal growth is computed and shown.

## Procedure

1. Set terminal growth with a justification sentence and a source.
2. Set terminal margin with a competitive reference.
3. Compute the terminal value with the formula stated.
4. Compute terminal value as a share of total value.
5. Run the sensitivity of value to terminal growth plus or minus one percentage point.
6. Record the assumption and the share in the valuation record.

## Anti-patterns

- Choosing terminal growth to make the answer match the current price.
- Setting terminal growth above the economy's long-run rate without a written argument.
- Assuming terminal margins above the best competitor's.
- Reporting a point value without showing the terminal share.
- Ignoring that a higher terminal growth rate and a lower discount rate both inflate the answer in the same direction.

## Done checklist

- [ ] Terminal growth set with justification and source.
- [ ] Terminal margin justified against competitors.
- [ ] Terminal return on capital consistent with the moat analysis.
- [ ] Terminal share of total value computed and reported.
- [ ] Sensitivity to terminal growth shown.
- [ ] Assumptions recorded in the record.

## Sources

- Valuation reference material on terminal value and growth: <https://pages.stern.nyu.edu/~adamodar/>
- Full-text filing search for competitive and margin history: <https://www.sec.gov/edgar/search/>
- Investor education on long-term growth assumptions: <https://www.investor.gov/introduction-investing>
