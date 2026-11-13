---
name: merger-model-synergies
domain: investing/merger-model-synergies
trigger: "Combining buyer and target financials and modelling synergies."
anti_trigger: "Not for recommending a deal, and not for trading the spread."
scope: "Combining the models, synergies as an arithmetic with a cost."
status: seedling
---

# Merger model and synergies

## Standard

The merger model combines the buyer's and target's financials and asks what the combination looks like. The core mechanic is accretion and dilution: pro forma earnings per share with and without the target. That requires building the combined income statement, completing the consideration structure's financing effects, and — the part that carries the most judgement — the synergies.

Synergies are an arithmetic with a cost and a schedule. Cost synergies from reducing duplicated functions are the most reliable; revenue synergies from cross-selling are the least reliably achieved and should be discounted steeply in any model. The discipline is to state each synergy as an amount, a year, and a cost-to-achieve — and to verify the aggregate against the premium paid: the present value of synergies must be compared with the premium, not with the purchase price, because the market price already embeds the standalone business.

Primary sources: <https://www.sec.gov/edgar/search/> and <https://www.law.cornell.edu/>.

## Decision rules

- Model cost synergies with their phase-in schedule, distinguishing run-rate from realised amounts.
- Discount revenue synergies more heavily than cost synergies, reflecting their historical realisation rates.
- Record both the cost-to-achieve and any dis-synergies — lost customers from the integration itself.
- Compare synergy value against the premium paid over the market price, never against the purchase price.
- Track the model effects through to the buyer's post-closing income statement.
- Assume the target's balance sheet and income statement will need normalisation before combination.

## Procedure

1. Normalise the target's financials and reconcile the two companies' accounting conventions.
2. Build the combined statement: revenues, costs, financing effects of the consideration structure.
3. Insert synergies with amount, year, phase-in, and cost-to-achieve lines.
4. Compute pro forma earnings per share and compare them against the buyer's standalone EPS.
5. Compare the present value of the synergy schedule against the premium.
6. Write the combined statement with every modelling assumption dated.

## Anti-patterns

- Treating run-rate synergies as realised on the closing date.
- Full-credit revenue synergies.
- Omitting dis-synergies and integration costs because they are "one-time".
- Comparing synergies to the purchase price rather than to the premium.
- Leaving the target's one-off items in the base-year for combination.

## Done checklist

- [ ] Target financials normalised.
- [ ] Combined statement built with financing effects.
- [ ] Synergies scheduled with costs to achieve.
- [ ] Revenue synergies discounted appropriately.
- [ ] Synergies compared against the premium.
- [ ] Pro forma EPS compared and dated.

## Sources

- Deal disclosures and pro forma filings: <https://www.sec.gov/edgar/search/>
- Statutory reference: <https://www.law.cornell.edu/>
- Investor education on acquisitions: <https://www.investor.gov/introduction-investing>
