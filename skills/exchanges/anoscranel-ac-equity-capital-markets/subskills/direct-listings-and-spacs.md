---
name: direct-listings-and-spacs
domain: investing/direct-listings-and-spacs
trigger: "Reading a direct listing or a SPAC transaction and its dilution."
anti_trigger: "Not for predicting the aftermarket, and not for the investment case."
scope: "No-bookbuild listings, SPAC redemption, and de-SPAC dilution."
status: seedling
---

# Direct listings and SPACs

## Standard

A direct listing admits existing shares to trading without a bookbuild and without raising primary capital. The opening price is discovered by the exchange's auction from the sell orders that arrive, and there is no syndicate stabilising the price and no greenshoe. The absence of those mechanisms is the defining difference: a direct listing has no coordinated bid underneath it and no lock-up unless the company imposes one.

A SPAC is the reverse: a shell raises cash in a blind pool, holds it in trust, and later combines with a private company. The dilution is layered — sponsor promote, warrants, and redemptions — and each layer is disclosed but easy to miss in aggregate. The arithmetic that matters is the cash left in trust after redemptions against the enterprise value being acquired, because that ratio determines how much of the deal is funded by the public and how much by the sponsor's own economics.

Primary sources: <https://www.sec.gov/investor> and <https://www.finra.org/>.

## Decision rules

- Record for a direct listing: the reference price, the auction mechanics, and any lock-up imposed.
- Record for a SPAC: the trust size, the redemption terms, and the deadline for redeeming.
- Record the sponsor promote as a percentage of post-combination shares.
- Record the warrants and their exercise price and dilution.
- Record the minimum cash condition in the combination agreement.
- Record the redemption outcome and the cash actually available at closing.

## Procedure

1. Identify whether the transaction is a direct listing or a SPAC combination.
2. Record the pricing and auction mechanics, or the trust and redemption terms.
3. Record the promote, warrants, and any other dilution.
4. Record the minimum cash condition.
5. Compute post-redemption cash and the implied funding gap.
6. Write the summary with the dilution shown as a percentage.

## Anti-patterns

- Treating a direct listing as an IPO with a different name.
- Ignoring the sponsor promote when computing post-deal ownership.
- Assuming the trust cash survives to closing.
- Overlooking the minimum cash condition, which can fail the deal.
- Reading warrants as free upside without their dilution.

## Done checklist

- [ ] Transaction type recorded.
- [ ] Pricing or trust terms recorded.
- [ ] Promote and warrants recorded.
- [ ] Minimum cash condition recorded.
- [ ] Post-redemption cash computed.
- [ ] Dilution expressed as a percentage.

## Sources

- Offering and combination disclosure: <https://www.sec.gov/investor>
- Market conduct guidance: <https://www.finra.org/>
- Investor education on listings: <https://www.investor.gov/introduction-investing>
