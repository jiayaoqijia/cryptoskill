---
name: pik-and-amortisation
domain: investing/pik-and-amortisation
trigger: "Reading a loan whose interest can be paid in kind rather than in cash."
anti_trigger: "Not for predicting default, and not for the borrower's equity case."
scope: "Payment-in-kind, deferred interest, and the cash flow illusion."
status: seedling
---

# PIK and amortisation

## Standard

Payment-in-kind interest is added to the principal rather than paid in cash, so the lender receives a higher balance instead of cash flow. The economics are real — the lender's claim grows and the coupon is typically higher — but the cash flow is not, and a fund reporting a yield that includes PIK is reporting an accrual rather than a receipt.

The risk compounds in a deteriorating credit. A borrower that cannot pay cash interest is a borrower whose cash generation is short of its obligations, and PIK converts that shortfall into more debt rather than a default. That deferral helps both sides in a temporary squeeze and hurts the lender in a permanent one, because the claim grows while the enterprise's ability to service it does not.

Primary sources: <https://www.federalreserve.gov/> and <https://www.cfainstitute.org/>.

## Decision rules

- Record the cash-pay portion and the PIK portion of the coupon.
- Record whether PIK can be elected by the borrower or is mandatory.
- Record the amortisation schedule and any extension options.
- Compute the cash yield and the total yield separately, and state both.
- Record the capitalised balance at each period and its effect on the claim.
- Record the trigger at which PIK election signals distress rather than flexibility.

## Procedure

1. Record the coupon structure and its components.
2. Compute cash yield and total yield.
3. Record amortisation and maturity extensions.
4. Track the capitalised balance over time.
5. Record the circumstances of PIK election.
6. Write the analysis with both yields stated.

## Anti-patterns

- Reporting total yield as if it were cash yield.
- Treating PIK election as neutral when it accompanies a cash shortfall.
- Ignoring the growth of the claim in a recovery analysis.
- Assuming amortisation occurs when it can be extended.
- Comparing a PIK loan's yield with a cash-pay loan's without adjustment.

## Done checklist

- [ ] Coupon components recorded.
- [ ] Cash and total yields computed.
- [ ] Amortisation recorded.
- [ ] Capitalised balance tracked.
- [ ] Election circumstances recorded.
- [ ] Analysis written with both yields.

The capitalisation also affects covenant tests, because a growing principal changes the leverage ratio that the borrower must maintain. A PIK election therefore tends to tighten the borrower's own tests as it relieves its cash flow, which is why the feature is often accompanied by an amendment rather than used on its own, and the amendment is the signal worth recording.

## Sources

- Credit market data: <https://www.federalreserve.gov/>
- Financial analysis standards: <https://www.cfainstitute.org/>
- Fund disclosure: <https://www.sec.gov/investor>
