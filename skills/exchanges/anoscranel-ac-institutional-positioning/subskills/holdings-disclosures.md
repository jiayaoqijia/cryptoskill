---
name: holdings-disclosures
domain: investing/holdings-disclosures
trigger: "Reading a 13F or similar holdings filing for what it does and does not show."
anti_trigger: "Not for inferring intent, and not for real-time positioning."
scope: "13F scope, the 45-day lag, and what a long-only snapshot misses."
status: seedling
---

# Holdings disclosures

## Standard

A 13F reports the long equity positions of institutional managers exercising investment discretion over at least one hundred million dollars in qualifying securities, at a quarter end, filed within forty-five days. Those four facts define its value and its limits: it covers long positions only, it is a snapshot, it is at least six weeks stale when published, and it omits short positions, options economics, and any position held in a form the filing does not capture.

The practical consequence is that a 13F tells you what a manager owned at a date, not what they think or what they are doing now. A manager can be long a stock in the filing and hedged with options, or have sold the entire position in the weeks before publication. Reading the filing as a live view is the most common error in this data, and it produces conclusions that were wrong before they were published.

Primary sources: <https://www.sec.gov/investor> and <https://www.sec.gov/edgar/search/>.

## Decision rules

- Record the filing date, the period of report, and the manager's identity.
- Record the position size and its share of the manager's reported portfolio.
- Record the change from the prior filing, and note that both are stale.
- Record what the filing cannot show: shorts, options economics, intra-quarter trades.
- Treat a new position as information about a quarter, not as a recommendation.
- Where several managers hold the same name, record the aggregate and the concentration.

## Procedure

1. Identify the manager and pull the filing from the regulator's database.
2. Record the period of report and the filing date, and compute the lag.
3. Record positions and their changes against the prior filing.
4. Note the omissions the filing permits.
5. Aggregate across managers where the question needs a broader view.
6. Write the summary with the lag stated prominently.

## Anti-patterns

- Treating a 13F as a current position.
- Assuming a long position is unhedged.
- Ignoring that smaller managers may not file at all.
- Reading one manager's filing as a market signal.
- Comparing filings with different report dates as if simultaneous.

## Done checklist

- [ ] Manager and period recorded.
- [ ] Filing date and lag recorded.
- [ ] Positions and changes recorded.
- [ ] Omissions noted.
- [ ] Aggregation done where needed.
- [ ] Summary states the lag.

## Sources

- SEC filings and full-text search: <https://www.sec.gov/edgar/search/>
- Investor education on institutional disclosure: <https://www.investor.gov/introduction-investing>
- Market structure context: <https://www.sec.gov/investor>
