---
name: stranded-assets-and-carbon-price
domain: investing/stranded-assets-and-carbon-price
trigger: "Testing whether an asset becomes uneconomic under a carbon price."
anti_trigger: "Not for predicting carbon prices, and not for the investment case."
scope: "Asset write-down arithmetic under a carbon price."
status: seedling
---

# Stranded assets and carbon price

## Standard

An asset is stranded when a change in policy, technology, or demand makes it uneconomic before the end of its useful life. The arithmetic is direct: take the asset's emissions per unit of output, multiply by the carbon price, subtract that from the unit margin, and see whether the margin survives. When it does not, the asset's book value is a claim on a business that no longer earns its cost of capital.

The carbon price is the assumption that carries the answer, and it is worth running as a range rather than a point. A price that is below the level at which the asset becomes uneconomic tells you the asset is safe under that scenario; a price above it tells you the write-down is a question of timing. Recording the break-even carbon price — the level at which the asset stops earning — inverts the analysis and makes it independent of any price forecast.

Primary sources: <https://www.eia.gov/> and <https://www.bis.org/>.

## Decision rules

- Record the asset's emissions per unit of output.
- Record the unit margin before carbon cost.
- Compute the break-even carbon price at which the margin reaches zero.
- Compare the break-even with the range of prices in relevant scenarios.
- Record the asset's remaining life and the capital not yet recovered.
- Record the write-down if the asset stops earning earlier than its book life.

## Procedure

1. Record emissions intensity and unit margin.
2. Compute the break-even carbon price.
3. Record the scenario price range.
4. Compare break-even with the range.
5. Compute the write-down for an early stop.
6. Write the analysis with the break-even stated.

## Anti-patterns

- Assuming a single carbon price rather than a range.
- Ignoring the asset's remaining life when estimating the write-down.
- Treating a break-even above current prices as a forecast.
- Applying a global price to a jurisdiction with no mechanism.
- Overlooking technology change that strands the asset without a carbon price.

## Done checklist

- [ ] Intensity and margin recorded.
- [ ] Break-even price computed.
- [ ] Scenario range recorded.
- [ ] Comparison made.
- [ ] Write-down computed.
- [ ] Analysis written with break-even.

The break-even also has a timing dimension that the price alone hides: an asset with two years of life left is barely exposed to a policy that arrives in five, while one with twenty years is exposed to every policy that could arrive within its life. Dividing the break-even price by the years of exposure gives a rough sense of how much policy movement per year would be needed to make the asset unviable, which is easier to judge than an absolute price.


## Sources

- Energy and emissions data: <https://www.eia.gov/>
- Climate risk analysis: <https://www.bis.org/>
- Disclosure requirements: <https://www.sec.gov/investor>
