---
name: concentration-caps
domain: investing/concentration-caps
trigger: "Reading a concentration cap and the mechanics that enforce it."
anti_trigger: "Not for predicting returns, and not for fund selection."
scope: "Caps, capping mechanics, and the drift between reviews."
status: seedling

---

# Concentration caps

## Standard

A cap limits the weight any single security or group can carry. It is described as a diversification safeguard, and its mechanics matter more than its existence: a hard cap requires a redistribution process when breached, which moves the excess weight to the other constituents and changes their weights in a way the methodology must specify.

The alternative is a capped-weighting scheme that scales all weights proportionally, which preserves relative weights while respecting the limit. The two produce different portfolios, and a methodology that states a cap without stating which mechanism applies has not described its own result. The record should state the cap level, the mechanism, and the review frequency at which the cap is enforced.

Primary sources: <https://www.sec.gov/investor> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the cap level and whether it applies to securities, groups, or sectors.
- Record the mechanism: redistribution to others, or proportional scaling.
- Record the review frequency at which the cap is tested.
- Record the drift allowed between reviews.
- Record the effect on the non-capped constituents' weights.
- Record whether the cap can be breached intra-period and by how much.

## Procedure

1. Record the cap levels and their scope.
2. Record the enforcement mechanism.
3. Record the review frequency.
4. Compute the weights after capping.
5. Record the drift allowance.
6. Write the capping summary.

## Anti-patterns

- Assuming a cap is enforced continuously.
- Ignoring which mechanism is used, since they produce different portfolios.
- Overlooking the effect on the other constituents' weights.
- Treating a sector cap as equivalent to a security cap.
- Reading a cap level without the drift allowance.

## Done checklist

- [ ] Cap levels and scope recorded.
- [ ] Mechanism recorded.
- [ ] Review frequency recorded.
- [ ] Post-capping weights computed.
- [ ] Drift allowance recorded.
- [ ] Summary written.

The redistribution detail is where two capped indices diverge most: moving excess weight to the next largest names concentrates the remainder, while scaling all weights proportionally preserves the original ranking, and a review that compares two capped indices on their cap alone will treat these as the same construction.


The drift allowance is also a hidden exposure: an index that permits a single name to reach double its cap between reviews is, at that moment, a less diversified index than its stated cap suggests.


## Sources

- Index methodology disclosure: <https://www.sec.gov/investor>
- Investor education on index rules: <https://www.investor.gov/introduction-investing>
- Market data for weight computation: <https://fred.stlouisfed.org/>
