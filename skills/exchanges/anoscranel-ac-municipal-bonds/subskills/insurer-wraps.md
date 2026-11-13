---
name: insurer-wraps
domain: investing/insurer-wraps
trigger: "Assessing what a municipal bond insurance wrap is actually worth."
anti_trigger: "Not for assessing the insurer's solvency in depth, and not for recommending a bond."
scope: "What a wrap guarantees, its cost, and its residual value after a downgrade."
status: seedling
---

# Insurer wraps

## Standard

A municipal bond insurer guarantees scheduled principal and interest, which converts the credit exposure into the weaker of the issuer and the insurer. That "weaker of" is the whole analysis: a wrap on a strong issuer adds nothing, a wrap on a weak issuer substitutes the insurer's credit, and a wrap on a moderately strong issuer gives the bondholder the better of two credits only in the sense that the insurer must pay if the issuer does not.

The pricing of the wrap explains why the market's view of it changed. Before the financial crisis, wrapped bonds traded at the insurer's rating regardless of the underlying, so issuers with weak credits could borrow at strong prices. After the insurers were downgraded, the market began pricing the underlying credit, and wrapped bonds began trading at the weaker of the two — which is what a guarantee actually delivers.

Primary sources: <https://www.msrb.org/> and <https://www.naic.org/>.

## Decision rules

- Record the insurer, its current financial strength rating, and the date of that rating.
- Record the underlying issuer's rating without the wrap.
- Record which of the two is weaker, since that is the effective credit.
- Record the wrap's cost to the issuer, where disclosed.
- Record whether the bond can trade on the insurer's rating in the market.
- Record any conditions on the guarantee, such as a failure to pay only after a grace period.

## Procedure

1. Identify the insurer and its current rating.
2. Record the underlying issuer's own rating.
3. Determine the effective credit as the weaker of the two.
4. Record the wrap's terms and any conditions.
5. Check how comparable wrapped bonds trade.
6. Write the analysis with the effective credit named.

## Anti-patterns

- Treating a wrapped bond as carrying the insurer's rating by default.
- Assuming a wrap improves a strong issuer's credit.
- Ignoring the guarantee's conditions.
- Using a stale insurer rating.
- Comparing a wrapped bond's yield with an unwrapped one without noting the credit difference.

## Done checklist

- [ ] Insurer and rating recorded with date.
- [ ] Underlying rating recorded.
- [ ] Effective credit identified.
- [ ] Wrap terms and conditions recorded.
- [ ] Trading behaviour checked.
- [ ] Analysis written.

## Sources

- Municipal disclosure and insurer information: <https://www.msrb.org/>
- Insurance regulation and company data: <https://www.naic.org/>
- Investor education on insured bonds: <https://www.investor.gov/introduction-investing>
