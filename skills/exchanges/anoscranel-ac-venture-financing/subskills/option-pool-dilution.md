---
name: option-pool-dilution
domain: investing/option-pool-dilution
trigger: "Sizing the option pool and computing who bears its dilution."
anti_trigger: "Not for compensation policy, and not for the valuation of the company."
scope: "Creating and refreshing the pool; who bears the dilution."
status: seedling
---

# Option pool dilution

## Standard

The option pool is the reserved share count from which employee option grants are made. When the pool is created or expanded, new shares are authorised, and every existing holder's fully diluted percentage falls. The subtlety that matters in a financing round is who bears that dilution: the pre-money holders, or everyone including the new investors. The common convention — the pool is top-upped in the pre-money — places the entire dilution on the existing holders, and the new investor's quoted ownership is computed after the expansion.

The negotiation consequence is that pool size is a price term disguised as an HR term. A larger pre-money pool means the founders and existing preferred absorb more dilution and the new investor buys the same percentage for the same money. When an investor asks for a "twenty percent pool," the response is not an HR judgement but an arithmetic judgement: how much of the company's pre-existing equity is being transferred to a future hiring plan the investor's own percentage will not bear.

Primary sources: <https://www.fasb.org/> and <https://www.law.cornell.edu/>.

## Decision rules

- Record the pool's size in shares and as a percentage of fully diluted, authorised plus unissued.
- Record whether the pool expansion is pre-money or post-money in each round, and compute both fully diluted tables.
- Compute the dilution transfer in percentage points from pool creation or expansion.
- Reconcile the pool's remaining availability against the hiring plan the pool claims to fund.
- Record the pool's refresh history: each expansion with date and pre/post-money treatment.
- Note that option exercises add shares over time; outstanding grants, not vested grants, are what the pool commits.

## Procedure

1. Record the current pool: authorised, granted, remaining.
2. Obtain or model the planned hiring the pool must fund and its expected grant sizes.
3. Compute the required pool size and compare it with the existing availability.
4. For a round, compute the pool expansion both pre-money and post-money and the resulting fully diluted ownership under each.
5. State the dilution transfer in percentage points per party.
6. Record the expansion with its treatment and date.

## Anti-patterns

- Treating the pool as an HR detail rather than a price term.
- Sizing the pool to "20 percent" without tying it to a hiring plan.
- Missing the pre-money vs post-money distinction and computing the investor's percentage wrong.
- Counting vested rather than outstanding grants against the pool.
- Ignoring that pool dilution compounds with every refresh.

## Done checklist

- [ ] Pool authorised/granted/remaining recorded.
- [ ] Hiring-plan requirement computed.
- [ ] Pre/post-money treatment identified per round.
- [ ] Both fully diluted tables computed.
- [ ] Dilution transfer stated in percentage points.
- [ ] Refresh history recorded.

## Sources

- Share-based compensation accounting: <https://www.fasb.org/>
- Statutory reference on equity plans: <https://www.law.cornell.edu/>
- Investor education on private company equity: <https://www.investor.gov/introduction-investing>
