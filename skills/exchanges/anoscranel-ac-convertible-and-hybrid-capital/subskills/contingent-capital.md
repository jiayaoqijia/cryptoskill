---
name: contingent-capital
domain: investing/contingent-capital
trigger: "Reading a bank AT1 or other contingent capital instrument and its trigger."
anti_trigger: "Not for predicting a trigger event, and not for bank equity analysis."
scope: "AT1, CoCo triggers, coupon cancellation, and the loss path."
status: seedling
---

# Contingent capital

## Standard

A contingent convertible converts to equity, or is written down, when a specified trigger is breached. In bank capital the common form is the additional tier one instrument: perpetual, callable, with a trigger typically set at a common equity tier one ratio, and with full discretion for the issuer to cancel the coupon. The instrument exists to absorb losses before senior creditors and after equity.

The loss path is what distinguishes it from a bond. The coupon is discretionary and cancellation is not an event of default; the trigger can be accounting-based or point-of-non-viability; and the conversion price is usually set at a level that transfers value from the holder. A holder who models the instrument as a high-yield bond with a call has modelled the wrong payoff.

Primary sources: <https://www.bis.org/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the trigger type, level, and the ratio it references.
- Record the conversion or write-down mechanics and the price at which conversion occurs.
- Record the coupon cancellation terms and whether they are cumulative.
- Record the call schedule and the regulatory permission required to call.
- Record the instrument's position in the resolution hierarchy.
- Compute the loss at the trigger under the stated conversion terms.

## Procedure

1. Extract the trigger definition and level.
2. Record the conversion or write-down mechanism.
3. Record coupon terms and cancellation.
4. Record the call schedule and its conditions.
5. Compute the loss at the trigger.
6. Write the structure summary with the loss path.

## Anti-patterns

- Treating a discretionary coupon as an obligation.
- Assuming the trigger is the only loss mechanism.
- Ignoring point-of-non-viability powers that can act before the trigger.
- Modelling conversion at par rather than at the stated price.
- Treating a call as certain because the market expects it.

## Done checklist

- [ ] Trigger type and level recorded.
- [ ] Conversion mechanics recorded.
- [ ] Coupon terms recorded.
- [ ] Call terms recorded.
- [ ] Hierarchy position recorded.
- [ ] Loss at trigger computed.

The comparison that matters is with the issuer's own equity and senior debt: a contingent capital instrument should compensate for the loss path between them, and when its spread compresses towards senior debt while the trigger remains live, the instrument is being priced as though the loss path did not exist, which is exactly the condition under which holders discover it.

## Sources

- Bank capital standards: <https://www.bis.org/>
- Instrument disclosure: <https://www.sec.gov/investor>
- Regulatory context: <https://www.federalreserve.gov/>
