---
name: triggers-and-amortisation
domain: investing/triggers-and-amortisation
trigger: "Reading the performance triggers that can redirect cash in a securitisation."
anti_trigger: "Not for predicting whether a trigger will breach, and not for rating the deal."
scope: "Performance triggers, early amortisation, and the redistribution they cause."
status: seedling
---

# Triggers and amortisation

## Standard

A trigger is a test that, when failed, changes the waterfall. The common ones are delinquency and loss ratios above stated levels, excess spread below a floor, or an overcollateralisation test failing. When a trigger breaches, cash that would have gone to the equity tranche is diverted to a reserve or to pay down senior notes, and in the extreme the deal enters early amortisation and returns principal to investors faster than the underlying assets repay.

The consequence for a holder is that the trigger converts an expected cash-flow stream into a different one. A junior tranche that relied on excess spread as its return can lose that spread entirely while the senior tranches are unaffected, and the diversion can happen months before the loss itself appears in the pool. The record should state each trigger, its threshold, its current level, and the consequence of breach.

Primary sources: <https://www.sec.gov/investor> and <https://www.bis.org/>.

## Decision rules

- Record each trigger, its definition, and its threshold.
- Record the current level against the threshold and the distance to breach.
- Record the consequence of each breach: diversion, accelerated paydown, or a rating event.
- Record who monitors the trigger and how often it is tested.
- Record any cure or waiver mechanism available to the issuer.
- Record the past breach history where disclosed.

## Procedure

1. Extract the trigger definitions and thresholds.
2. Record the latest reported level for each.
3. Compute the buffer to breach.
4. Record the consequence of breach per trigger.
5. Record the monitoring and waiver provisions.
6. Write the trigger summary with the nearest breach named.

## Anti-patterns

- Reading only the loss trigger and ignoring the spread trigger.
- Assuming a breach is visible only when losses appear.
- Treating a waiver as a permanent change.
- Ignoring the issuer's ability to cure by adding collateral.
- Comparing thresholds across deals with different asset quality.

## Done checklist

- [ ] Triggers and thresholds recorded.
- [ ] Current levels recorded.
- [ ] Buffers computed.
- [ ] Consequences recorded per trigger.
- [ ] Monitoring and waivers recorded.
- [ ] Nearest breach named.

The other consequence worth recording is that a breach can be self-reinforcing: diverting cash to the senior notes reduces the spread available to absorb further losses, which pushes the spread trigger closer, which diverts more cash. A structure with several interlinked triggers can deteriorate faster than any single threshold suggests.

## Sources

- Securitisation trigger and performance disclosure: <https://www.sec.gov/investor>
- Securitisation standards: <https://www.bis.org/>
- Regulatory reporting context: <https://www.federalreserve.gov/>
