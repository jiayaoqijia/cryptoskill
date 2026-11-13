---
name: pension-and-opeb-liabilities
domain: investing/pension-and-opeb-liabilities
trigger: "Reading a municipality's unfunded pension and OPEB obligations."
anti_trigger: "Not for actuarial advice, and not for predicting a default."
scope: "Unfunded obligations and how they compete with bondholders."
status: seedling
---

# Pension and OPEB liabilities

## Standard

An unfunded pension obligation is a claim on the same tax and revenue base that supports the bonds, and it ranks behind them legally while competing with them economically. The claim does not appear on the balance sheet as debt, which is why a municipality can look conservatively leveraged and still face an obligation that consumes a growing share of its budget.

Three inputs decide the size. The discount rate is the assumption that matters most: a higher assumed return reduces the reported liability, so a plan assuming eight percent shows a smaller unfunded position than the same plan assuming five. The amortisation period determines how quickly contributions must rise, and the funded ratio measured on a market-consistent basis is a very different number from the one reported under the plan's own assumption.

Primary sources: <https://www.gfoa.org/> and <https://www.msrb.org/>.

## Decision rules

- Record the funded ratio on the plan's own basis and, where disclosed, on a market-consistent basis.
- Record the discount rate assumed and compare it with a risk-free rate.
- Record the amortisation period and the contribution as a percentage of the budget.
- Record the OPEB liability separately from pensions, since the funding mechanisms differ.
- Record the trend in the unfunded balance over several years.
- Record any legal protections that limit the issuer's ability to reduce benefits.

## Procedure

1. Obtain the pension and OPEB disclosure from the financial statements.
2. Record the funded ratio and the discount rate.
3. Record the contribution and its share of the budget.
4. Record the multi-year trend.
5. Record the legal framework for benefit changes.
6. Write the analysis with the sensitivity to the discount rate.

## Anti-patterns

- Reading the reported funded ratio as the economic position.
- Ignoring the discount rate assumption.
- Treating pensions and OPEB as a single obligation.
- Looking at one year rather than the trend.
- Assuming benefits can be reduced at will.

## Done checklist

- [ ] Funded ratios recorded on both bases.
- [ ] Discount rate recorded.
- [ ] Contribution and budget share recorded.
- [ ] OPEB recorded separately.
- [ ] Trend recorded.
- [ ] Legal framework recorded.

The sensitivity worth stating explicitly is what happens to the funded ratio under a lower discount assumption and a weaker return year: those two move together in practice, so a plan that looks adequately funded on its own assumptions can look materially short on a market-consistent one, and the record should carry both rather than only the reported figure.


## Sources

- Public finance standards and guidance: <https://www.gfoa.org/>
- Municipal disclosure and market information: <https://www.msrb.org/>
- Investor education on municipal credit: <https://www.investor.gov/introduction-investing>
