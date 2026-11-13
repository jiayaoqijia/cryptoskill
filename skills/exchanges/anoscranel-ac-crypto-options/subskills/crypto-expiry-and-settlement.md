---
name: crypto-expiry-and-settlement
domain: crypto-trading/crypto-expiry-and-settlement
trigger: "Working out when a crypto option expires and against which price."
anti_trigger: "Not for predicting the price, and not for generic option theory."
scope: "Daily to quarterly expiries, the settlement time, and the mark price."
status: seedling
---

# Crypto expiry and settlement

## Standard

Crypto options expire on a dense grid: daily, weekly, monthly, and quarterly, with settlement at a fixed time — commonly eight in the morning UTC — rather than at a market close. That fixed time matters because the market trades continuously, so the settlement price is a snapshot rather than the end of a session, and a position can be in the money at one moment and out of it minutes later.

Settlement uses an index price computed from several spot venues, not the last trade on one exchange. The venue publishes the index and its composition, and the difference between the index and the venue's own last price can decide an expiry. A trader who watches one venue's chart through expiry is watching a proxy for the number that settles the contract.

Primary sources: <https://www.cftc.gov/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the expiry date and the exact settlement time in UTC.
- Record the settlement index and its composition.
- Record the last trading time, which may precede settlement.
- Record the expiry grid used, since daily and quarterly contracts behave differently.
- Record whether exercise is automatic for in-the-money options.
- Record the settlement currency and the fee applied at settlement.

## Procedure

1. Record the expiry and settlement time.
2. Record the index and its source.
3. Record the last trading time.
4. Note the expiry grid and its effect on liquidity.
5. Record the automatic exercise rule.
6. Write the settlement summary.

## Anti-patterns

- Assuming settlement at the venue's last trade.
- Treating the last trading time as the settlement time.
- Ignoring the index composition when several venues disagree.
- Overlooking the fee at settlement.
- Planning an exit after trading has stopped.

## Done checklist

- [ ] Expiry and time recorded in UTC.
- [ ] Index and composition recorded.
- [ ] Last trading time recorded.
- [ ] Expiry grid recorded.
- [ ] Automatic exercise recorded.
- [ ] Settlement currency and fee recorded.

The index's construction deserves a note: it averages prices across several venues, sometimes excluding outliers and sometimes weighting by volume, so a dislocation on one exchange that would settle a single-venue contract has no effect on the index. A trader watching the wrong chart through expiry is watching a number that does not settle the position.


## Sources

- Regulatory information on crypto derivatives: <https://www.cftc.gov/>
- Market structure context: <https://www.sec.gov/investor>
- Investor education on derivatives: <https://www.investor.gov/introduction-investing>
