---
name: tax-aware-policy
domain: investing/tax-aware-policy
trigger: "Writing the tax-aware rules that govern portfolio decisions."
anti_trigger: "Not for tax advice, and not for the investment policy itself."
scope: "The written policy: location rules, harvesting rules, and review triggers."
status: seedling
---

# Tax-aware policy

## Standard

The tax-aware policy states the rules in advance: which assets belong in which accounts, when losses are harvested, how much drift is tolerated before a sale, and which lots are sold first. Writing them down turns a series of ad hoc decisions into a consistent approach, and it prevents the two failure modes that recur — harvesting in a year when it provides no benefit, and selling the wrong lot because nobody recorded which had the highest basis.

The policy also carries the review triggers specific to tax: a change in the rules, a change in the bracket, a large realised gain arriving from elsewhere, or a change in the account structure. Those are the events that invalidate the arithmetic, and naming them means the policy is revisited when it should be rather than when someone remembers.

Primary sources: <https://www.irs.gov/> and <https://osf.io/prereg/>.

## Decision rules

- The policy states the location rule and the exceptions it permits.
- The harvesting rule states the threshold, the replacement approach, and the window.
- The rebalancing rule states the tolerance band and the flow-first preference.
- The lot selection rule is explicit, not left to the broker's default.
- Review triggers are dated and specific.
- The policy names the professional who reviews it and the questions reserved for them.

## Procedure

1. Write the location rule and its exceptions.
2. Write the harvesting rule with threshold and replacement.
3. Write the rebalancing and lot-selection rules.
4. Set the review triggers.
5. Name the professional and the reserved questions.
6. File with the investment policy and review on the triggers.

## Anti-patterns

- Leaving lot selection to the default.
- A harvesting rule with no threshold, so it is applied when convenient.
- No review triggers, so the policy silently expires.
- Presenting a rule of thumb as a jurisdiction's requirement.
- Filing the policy apart from the investment policy it constrains.

## Done checklist

- [ ] Location rule and exceptions written.
- [ ] Harvesting rule written.
- [ ] Rebalancing and lot rules written.
- [ ] Review triggers dated.
- [ ] Professional and reserved questions named.
- [ ] Filed with the investment policy.

A useful last section is the list of things the policy does not cover: a policy that states its own boundaries is easier to review than one that implies completeness, and the items it excludes are precisely the ones that require a professional rather than a rule.


## Sources

- Tax administration guidance: <https://www.irs.gov/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Investor education on tax-aware investing: <https://www.investor.gov/introduction-investing>
