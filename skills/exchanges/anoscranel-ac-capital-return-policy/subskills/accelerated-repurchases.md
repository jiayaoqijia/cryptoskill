---
name: accelerated-repurchases
domain: investing/accelerated-repurchases
trigger: "Reading an accelerated share repurchase and what price it locks in."
anti_trigger: "Not for recommending a programme, and not for share price prediction."
scope: "ASR mechanics, the initial and final delivery, and the price it locks in."
status: seedling
---

# Accelerated repurchases

## Standard

An accelerated share repurchase delivers a large block of shares to the company immediately, borrowed from a dealer, against an upfront payment. The final number of shares is settled later, based on the volume-weighted price over a stated period, so the company receives more shares if the price falls and fewer if it rises.

That structure means the company is not buying at the announcement price; it is buying at an average over the settlement window, with a cap and a floor that determine the range. The upfront payment divided by the initial share delivery gives a headline price that is not the economic price, which is why an ASR announcement that looks like a purchase at a premium can settle at a discount to the eventual average.

Primary sources: <https://www.sec.gov/investor> and <https://www.cfainstitute.org/>.

## Decision rules

- Record the upfront payment, the initial shares delivered, and the implied initial price.
- Record the settlement period and the price reference used.
- Record the collar: the minimum and maximum number of shares.
- Record the final settlement when it occurs, and compute the effective price paid.
- Record the dilution effect of the initial delivery versus the final count.
- Record the dealer counterparty and any termination provisions.

## Procedure

1. Record the announcement terms and the initial delivery.
2. Compute the implied initial price.
3. Record the settlement window and reference.
4. Record the collar bounds.
5. Compute the effective price at final settlement.
6. Write the ASR summary with the effective price.

## Anti-patterns

- Treating the initial delivery as the completed purchase.
- Quoting the headline price as the price paid.
- Ignoring the collar that bounds the outcome.
- Forgetting that the final share count is unknown at announcement.
- Treating an ASR as equivalent to an open-market programme.

## Done checklist

- [ ] Terms and initial delivery recorded.
- [ ] Implied initial price computed.
- [ ] Settlement window and reference recorded.
- [ ] Collar recorded.
- [ ] Effective price computed at settlement.
- [ ] Dilution effect recorded.

The economics also depend on what the dealer does with the borrowed shares: the initial delivery is a real transfer of ownership, so the company's share count falls immediately while the final count remains open, and any metric computed from the interim count overstates the eventual reduction. The record should carry both the interim and final counts rather than whichever is available at the time.

## Sources

- Repurchase agreement disclosure: <https://www.sec.gov/investor>
- Investment analysis standards: <https://www.cfainstitute.org/>
- Market price data: <https://fred.stlouisfed.org/>
