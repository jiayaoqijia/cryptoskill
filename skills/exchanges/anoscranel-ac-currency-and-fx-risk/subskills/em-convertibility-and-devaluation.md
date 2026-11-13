---
name: em-convertibility-and-devaluation
domain: investing/em-convertibility-and-devaluation
trigger: "Assessing emerging-market currency risk beyond the exchange rate."
anti_trigger: "Not for predicting devaluations, and not for sovereign analysis."
scope: "Capital controls, convertibility, and the mechanics of a devaluation."
status: seedling
---

# EM convertibility and devaluation

## Standard

An emerging-market currency carries risks that a developed-market one does not: convertibility can be restricted, capital can be trapped, and a devaluation can be administered rather than traded. A hedge executed in a domestic account may not reach the exposure at all, because the constraint is on moving money, not on pricing it.

The mechanics of a devaluation are usually policy-driven: a peg is defended until reserves run out, then adjusted, often with controls introduced alongside. The investor's exposure is sequential — first the asset price, then the currency, then the ability to repatriate — and each layer can fail separately.

Primary sources: <https://fred.stlouisfed.org/> and <https://www.investor.gov/introduction-investing>.

## Decision rules

- Record the currency regime: floating, managed, pegged, or controlled.
- Record convertibility limits: repatriation rules, approval requirements, and any history of controls.
- Record reserves and their trend where published.
- Treat the exposure as layered: asset, currency, repatriation.
- Record which layer each hedge instrument reaches, and which it does not.
- Size the position for the case where the currency cannot be converted at any price.

## Procedure

1. Classify the currency regime.
2. Record convertibility limits and their history.
3. Record reserves and trend.
4. Map the layered exposure.
5. Record the reach of each hedge.
6. Record the unhedgeable case and the size it implies.

## Anti-patterns

- Hedging the currency while ignoring repatriation.
- Treating a peg as a fixed fact.
- Ignoring the reserve trend.
- Sizing for the tradeable case only.
- Assuming a domestic hedge reaches an offshore exposure.

## Done checklist

- [ ] Regime classified.
- [ ] Convertibility limits and history recorded.
- [ ] Reserves and trend recorded.
- [ ] Layered exposure mapped.
- [ ] Hedge reach recorded per layer.
- [ ] Unhedgeable case and size recorded.

## Sources

- Rate and reserve data: <https://fred.stlouisfed.org/>
- Investor education on emerging-market risk: <https://www.investor.gov/introduction-investing>
- Regulatory context for cross-border disclosure: <https://www.sec.gov/investor>

The historical pattern is consistent: reserves fall, the peg is defended with borrowing and controls, and the adjustment arrives with restrictions that make the currency less useful precisely when the investor wants it. Recording the reserve trend is the cheapest early signal available.

Convertibility has a practical test that costs nothing: try a small repatriation before committing size. The answer — whether it clears, at what rate, and with what documentation — is more informative than any published rule, and it is worth recording with its date.
