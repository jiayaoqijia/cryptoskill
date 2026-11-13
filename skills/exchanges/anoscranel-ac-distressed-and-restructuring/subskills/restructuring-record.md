---
name: restructuring-record
domain: investing/restructuring-record
trigger: "Writing the record of a distressed position and its recovery scenarios."
anti_trigger: "Not for recommending a distressed security, and not for the legal file."
scope: "The written record: waterfall, fulcrum, recovery scenarios, and process triggers."
status: seedling
---

# Restructuring record

## Standard

The distressed record states the waterfall, the fulcrum at each valuation point, the recovery under each scenario, and the process events that would change the analysis. It is written before the position, and its function is to make the recovery argument explicit enough that a later disagreement is about the enterprise value assumption rather than about what was believed at the time.

The process triggers are what distinguish this record from a credit file. A filing date, a DIP motion, a valuation motion, a plan filing, a confirmation hearing, and an effective date each change the position's economics, and recording them in advance converts a sequence of surprises into a calendar. The record also states what the position is worth if the process fails, which is usually the liquidation case.

Primary sources: <https://www.uscourts.gov/> and <https://osf.io/prereg/>.

## Decision rules

- The record contains the claim schedule and the waterfall at two valuation points.
- The fulcrum is named at each point and its stability stated.
- Recovery is computed per instrument under each scenario, including liquidation.
- Process triggers are dated: filing, DIP, plan, confirmation, effective date.
- The valuation assumption is stated with its source and date.
- The record is append-only, amended by dated entries as the process advances.

## Procedure

1. Record the claim schedule and waterfall.
2. Record the fulcrum and its sensitivity.
3. Compute recovery per instrument by scenario.
4. Record the liquidation case.
5. Set the process triggers with dates.
6. Amend at each trigger and record what changed.

## Anti-patterns

- Recording a single recovery number without scenarios.
- Omitting the liquidation case.
- Leaving the valuation assumption implicit.
- No dated triggers, so the analysis is never revisited.
- Editing the entry record as the process unfolds.

## Done checklist

- [ ] Claim schedule and waterfall recorded.
- [ ] Fulcrum named with stability stated.
- [ ] Recovery computed per scenario.
- [ ] Liquidation case recorded.
- [ ] Triggers dated.
- [ ] Amendments dated.

The record should also carry the position's liquidity: claims in a distressed situation can be far easier to buy than to sell, and an exit that depends on a plan distribution rather than a market sale has a different time horizon from one that does not. Stating the exit route alongside the recovery makes the comparison between two positions honest.


## Sources

- Court process information: <https://www.uscourts.gov/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Filing search for process documents: <https://www.sec.gov/edgar/search/>
