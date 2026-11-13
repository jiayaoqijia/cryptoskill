---
name: outlooks-watches-and-notches
domain: investing/outlooks-watches-and-notches
trigger: "Reading an outlook or a watch and knowing what it commits the agency to."
anti_trigger: "Not for predicting a downgrade, and not for credit analysis."
scope: "Outlook, watch, and the operational meaning of each."
status: seedling
---

# Outlooks, watches and notches

## Standard

An outlook is the agency's view of the direction of a rating over one to two years, expressed as stable, positive, or negative. It is a statement about direction and carries no commitment to a date. A watch is stronger and shorter: a rating placed on watch is under review for a change, usually within months, and the review is triggered by a specific event or a specific analysis.

The distinction matters operationally because a watch signals that a committee is already engaged. A negative watch on a name near an investment-grade threshold is therefore a live risk for any mandate that references the threshold, not a distant possibility, and the record should treat it as a scheduled event rather than as an opinion. Outlooks, by contrast, often resolve to stable without any rating change.

Primary sources: <https://www.sec.gov/investor> and <https://www.bis.org/>.

## Decision rules

- Record the outlook and the date it was assigned.
- Record any watch, its direction, and the stated reason.
- Record the expected timeframe the agency has given.
- Record the rating level and the threshold it sits relative to.
- Record the event that triggered the watch where disclosed.
- Record the last time an outlook resolved without a rating change.

## Procedure

1. Record the current rating and its outlook.
2. Record any watch with its direction and stated reason.
3. Record the agency's timeframe.
4. Compute the distance to any relevant threshold.
5. Record the triggering event.
6. Write the status summary with the watch as a scheduled risk.

## Anti-patterns

- Treating an outlook as a forecast with a date.
- Ignoring a watch because no rating change has occurred.
- Assuming a negative outlook must resolve to a downgrade.
- Missing the threshold distance when a watch is live.
- Treating different agencies' watches as equivalent in timing.

## Done checklist

- [ ] Outlook recorded with date.
- [ ] Watch recorded with direction and reason.
- [ ] Timeframe recorded.
- [ ] Threshold distance computed.
- [ ] Triggering event recorded.
- [ ] Status summary written.

The timing asymmetry is the part worth recording: outlooks frequently resolve to stable without a rating change, which trains readers to discount them, while watches resolve to a change more often than not, which means the two should be weighted differently in any assessment of near-term risk even though both are described as opinions about direction.

## Sources

- Rating agency actions and disclosure: <https://www.sec.gov/investor>
- Regulatory framework for ratings: <https://www.bis.org/>
- Investor education on credit risk: <https://www.investor.gov/introduction-investing>
