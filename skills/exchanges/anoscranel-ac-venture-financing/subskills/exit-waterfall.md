---
name: exit-waterfall
domain: investing/exit-waterfall
trigger: "Distributing exit proceeds across preferred, common, and options."
anti_trigger: "Not for predicting an exit, and not for tax computation."
scope: "Distributing exit proceeds across preferred, common, and options."
status: seedling
---

# Exit waterfall

## Standard

The exit waterfall is a calculation run almost nowhere else: given a sale price, distribute the proceeds across the preference stack, the participation rights, and the option holders — some of whom are underwater and receive nothing. The waterfall is deterministic; the uncertainty is entirely in the sale price. That division of labour is why the analysis is done on a grid of exit values, not a single number: the interesting transitions — where a series converts rather than takes its preference, where options go in the money — are visible only across a range.

The mechanics are layered. First the preference stack in seniority order; then each series' choice of preference or conversion; then participation rights where they exist; then common; then options, which participate only when the per-share proceeds exceed their strike, and then only for the spread. A covered company with participating preferences can leave common with a small fraction of the proceeds even at prices that sound like successes, and the founders' percentage of the cap table is not their percentage of the exit until the waterfall says so.

Primary sources: <https://www.law.cornell.edu/> and <https://www.sec.gov/edgar/search/>.

## Decision rules

- Take the cap table's current conversion terms, including anti-dilution adjustments, as the input.
- Compute the exit grid across prices from a lowball outset to a high outcome, not a single value.
- At each grid point, decide each series' preferred-outcome choice: take the preference or convert.
- Include option strikes: at every price, the in-the-money grants receive the spread above strike.
- State the conversion crossovers — the price at which each series' outcome changes character.
- Report the per-share outcome of common as the headline, since common is the class most people actually hold or think they hold.

## Procedure

1. Assemble the current cap table with each series' current conversion terms.
2. Build the exit grid across price points.
3. At each price, proceed down the seniority order with each series' preference-or-convert decision.
4. Distribute the residual to participating claims and then to common.
5. Compute the option spread at each price for every strike in the table.
6. Publish the grid and mark the crossovers.

## Anti-patterns

- Running the waterfall at one price.
- Using the conversion ratio at issue rather than the currently adjusted one.
- Excluding underwater options rather than marking them zero.
- Forgetting that participating without a cap removes the conversion decision entirely.
- Expecting a percentage ownership to predict exit proceeds without the stack.

## Done checklist

- [ ] Grid of exit prices computed.
- [ ] Series-by-series decision logic applied at each price.
- [ ] Participation applied before common.
- [ ] Option spreads computed per strike.
- [ ] Crossovers identified and marked.
- [ ] Per-share common outcome stated as the headline.

## Sources

- Statutory reference on distributions: <https://www.law.cornell.edu/>
- Deal disclosure for exit structures: <https://www.sec.gov/edgar/search/>
- Investor education on distributions: <https://www.investor.gov/introduction-investing>
