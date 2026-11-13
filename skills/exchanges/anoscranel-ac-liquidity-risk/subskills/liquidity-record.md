---
name: liquidity-record
domain: investing/liquidity-record
trigger: "Writing the liquidity budget and its trigger levels."
anti_trigger: "Not for recommending a position, and not for predicting needs."
scope: "The written record: the ladder, the assumptions, and the trigger levels."
status: seedling
---

# Liquidity record

## Standard

The liquidity record holds the ladder, the assumptions behind it, the requirements mapped to buckets, and the trigger levels at which the portfolio must act. It is written before the need arises, because the moment a cash requirement appears is the moment when the measurement is least likely to be done carefully.

The trigger levels are what make the record operational. A buffer that falls below a stated level, a bucket that becomes short, or a days-to-liquidate figure that crosses a threshold are all observable conditions, and naming them converts the record from a description into a rule. The record also carries the stress case, so that the comparison between calm and stressed is available whenever it is queried.

Primary sources: <https://www.bis.org/> and <https://osf.io/prereg/>.

## Decision rules

- The record contains both the calm and the stress ladder.
- Assumptions are stated per bucket: participation rate, haircut, and volume basis.
- Requirements are mapped to the buckets they fall in.
- Trigger levels are stated as observable conditions with numbers.
- Each trigger has an action attached, decided in advance.
- The record is reviewed on a schedule and whenever the portfolio's composition changes materially.

## Procedure

1. Record the calm ladder with its assumptions.
2. Record the stress ladder with its assumptions.
3. Map the requirements to buckets.
4. State the trigger levels and their actions.
5. Set the review schedule and the composition trigger.
6. File the record and reference it from the investment policy.

## Anti-patterns

- A ladder without its assumptions.
- Trigger levels with no action attached.
- Recording only the calm case.
- Reviewing only on a calendar rather than on composition change.
- Filing the record apart from the policy it constrains.

## Done checklist

- [ ] Calm ladder recorded with assumptions.
- [ ] Stress ladder recorded.
- [ ] Requirements mapped.
- [ ] Triggers with actions written.
- [ ] Review schedule set.
- [ ] Filed and cross-referenced.

A final field worth adding is the owner of each trigger: a level with an action but no person attached is a condition that will be noticed and not acted upon, and the record's purpose is to make the action automatic rather than discretionary.


The record is also the place where the portfolio's liquidity is compared with its own stated tolerance, so that a change in composition shows up as a change against a fixed standard rather than as a fresh judgement each time.

## Sources

- Liquidity and collateral standards: <https://www.bis.org/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- Market data for volume and haircut bases: <https://fred.stlouisfed.org/>
