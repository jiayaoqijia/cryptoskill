---
name: priority-and-waterfall
domain: investing/priority-and-waterfall
trigger: "Mapping claim seniority and where recovery stops in a capital structure."
anti_trigger: "Not for predicting a court outcome, and not for ordinary credit scoring."
scope: "Claim seniority, secured versus unsecured, and the order recovery reaches each layer."
status: seedling
---

# Priority and waterfall

## Standard

Priority is a legal ordering, not an economic intuition. Secured claims reach their collateral ahead of unsecured claims; administrative and priority claims reach the estate ahead of general unsecured claims; subordinated debt sits behind unsecured debt by contract; and equity stands last. Within that ordering, a claim is worth the value that remains at its layer and nothing more, which is why the same enterprise value produces very different recoveries across the queue.

The waterfall is a claim-by-claim subtraction rather than a percentage allocation. Enterprise value is applied to the most senior claim first, then to the next, and so on, until the value is exhausted. That arithmetic produces the finding that matters: claims above the exhaustion point are money-good and trade near par, claims below it are options, and claims at the point itself determine the reorganized company's ownership.

Primary sources: <https://www.uscourts.gov/> and <https://www.law.cornell.edu/>.

## Decision rules

- Record every claim with its instrument, face amount, seniority, security, and guarantees.
- Separate secured from unsecured and, within secured, first-lien from junior-lien.
- Record administrative and priority claims, which reach the estate before general unsecured.
- Apply enterprise value down the waterfall and record the layer where it is exhausted.
- Record intercreditor agreements, which can change the ordering between lenders.
- State the valuation range used and the date, because the answer moves with it.

## Procedure

1. Build the claim schedule from the capital structure and the disclosure statement.
2. Classify each claim by seniority, security, and guarantee.
3. Obtain an enterprise value range, with its source and date.
4. Apply value down the waterfall at the low and high ends.
5. Identify the exhausted layer and the claims just above and below it.
6. Record the recovery by claim at both ends of the range.

## Anti-patterns

- Allocating value pro rata across all claims.
- Treating a guarantee as equivalent to a first lien.
- Ignoring administrative claims, which consume value before unsecured creditors see any.
- Using a single point estimate of enterprise value.
- Forgetting that intercreditor agreements can reorder what the statute would otherwise dictate.

## Done checklist

- [ ] Claim schedule built with seniority and security.
- [ ] Secured and unsecured separated.
- [ ] Administrative claims recorded.
- [ ] Value applied down the waterfall at two ends.
- [ ] Exhaustion layer identified.
- [ ] Valuation range and date recorded.

## Sources

- Court information on bankruptcy processes: <https://www.uscourts.gov/>
- Statutory and case law reference: <https://www.law.cornell.edu/>
- Filing search for capital structure disclosure: <https://www.sec.gov/edgar/search/>
