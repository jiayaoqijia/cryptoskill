---
name: capital-protection
domain: investing/capital-protection
trigger: "Testing what a note's capital protection actually protects."
anti_trigger: "Not for recommending a protected product, and not for assessing the issuer's solvency."
scope: "What \"protected\" means, at what level, from what, and subject to whose credit."
status: seedling
---

# Capital protection

## Standard

Capital protection is a promise with three qualifiers that are usually printed smaller than the word itself: the level, the timing, and the guarantor. The level may be ninety percent rather than a hundred; the timing may be at maturity only, so an interim sale can lose money; and the guarantor is the issuing bank, so the protection is only as good as its credit.

A protected note is therefore a deposit-like claim on a bank plus a call option on the underlying, with the option paid for out of the coupon the principal would otherwise earn. That framing explains the cost: in a high-rate environment, a protected note gives up the risk-free yield to buy participation, and the participation it buys should be compared with what the same money would buy in listed options.

Primary sources: <https://www.sec.gov/investor> and <https://www.bis.org/>.

## Decision rules

- Record the protection level as a percentage of the issue price, and the date at which it applies.
- Record whether protection applies on early sale, on issuer default, or only at maturity.
- Identify the guarantor and its credit standing, with a date.
- Compute the opportunity cost: the risk-free yield forgone over the term.
- Compare the participation obtained with the participation the forgone yield would buy in listed options.
- Record any condition that removes protection, such as a barrier or a basket averaging rule.

## Procedure

1. Extract the protection level and timing from the terms.
2. Identify the guarantor and record its credit assessment with a date.
3. Compute the risk-free yield forgone over the term.
4. Price the participation as a share of that forgone yield.
5. Compare with a listed alternative of the same term.
6. Record the protection summary and its conditions.

## Anti-patterns

- Reading "capital protected" without the level.
- Assuming protection applies to interim sales.
- Treating the issuer's credit as irrelevant because the note is "protected".
- Ignoring the yield forgone in a high-rate environment.
- Comparing participation across notes with different terms.

## Done checklist

- [ ] Protection level and timing recorded.
- [ ] Guarantor identified with a dated credit assessment.
- [ ] Forgone yield computed.
- [ ] Participation cost measured against the forgone yield.
- [ ] Listed alternative compared.
- [ ] Conditions that remove protection recorded.

## Sources

- Structured product disclosure and investor guidance: <https://www.sec.gov/investor>
- Bank capital and counterparty standards: <https://www.bis.org/>
- Investor education on product risk: <https://www.investor.gov/introduction-investing>
