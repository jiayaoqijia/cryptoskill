---
name: debt-funded-buybacks
domain: investing/debt-funded-buybacks
trigger: "Testing the arithmetic of repurchasing shares with borrowed money."
anti_trigger: "Not for recommending a capital structure, and not for predicting rates."
scope: "Leverage, interest coverage, and the arithmetic of repurchasing with borrowed money."
status: seedling
---

# Debt-funded buybacks

## Standard

Repurchasing shares with debt is a swap: the company replaces equity with borrowing, which raises the return on equity if the borrowing cost is below the after-tax return on the assets and lowers it if not. The arithmetic is the same as any leveraged recapitalisation, and the risk is the same: the higher earnings per share comes with a fixed obligation that must be met in a downturn.

The tests are coverage and maturity. Interest coverage after the transaction, the maturity profile of the new debt against the cash generation of the business, and the covenant headroom that remains are the numbers that decide whether the swap is prudent. A company that funds a buyback at a low fixed rate for a long maturity has made a different decision from one that funds it with short-dated floating debt.

Primary sources: <https://www.sec.gov/investor> and <https://www.bis.org/>.

## Decision rules

- Record the amount borrowed, the rate, the maturity, and whether it is fixed or floating.
- Compute interest coverage before and after the transaction.
- Record the covenant headroom and the tests that measure it.
- Record the earnings-per-share effect at the current rate.
- Record the effect of a rate rise on floating-rate funding.
- Record the maturity wall against the business's cash generation.

## Procedure

1. Record the financing terms of the transaction.
2. Compute pro forma interest coverage.
3. Record covenant headroom and the tests.
4. Compute the EPS effect and the return-on-equity effect.
5. Test a rate rise on floating debt.
6. Write the arithmetic with the coverage and maturity tests.

## Anti-patterns

- Treating EPS accretion as proof the transaction was sound.
- Ignoring the maturity profile of the new debt.
- Assuming the rate stays at the level achieved at issuance.
- Overlooking covenants that restrict further distributions.
- Comparing leverage across companies with different business cyclicality.

## Done checklist

- [ ] Financing terms recorded.
- [ ] Coverage before and after computed.
- [ ] Covenant headroom recorded.
- [ ] EPS and ROE effects computed.
- [ ] Rate sensitivity tested.
- [ ] Maturity wall recorded.

The comparison that matters is with the company's own cost of equity rather than with the rate alone: borrowing at a rate below the return the business earns on its assets raises the return to shareholders, and borrowing above it lowers the return while raising the risk, which is why the spread between the two numbers, not the absolute rate, decides the arithmetic.

## Sources

- Debt and repurchase disclosure: <https://www.sec.gov/investor>
- Leverage and capital standards: <https://www.bis.org/>
- Rate data: <https://fred.stlouisfed.org/>
