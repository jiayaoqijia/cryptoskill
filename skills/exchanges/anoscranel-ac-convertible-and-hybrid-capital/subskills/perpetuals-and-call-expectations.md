---
name: perpetuals-and-call-expectations
domain: investing/perpetuals-and-call-expectations
trigger: "Analysing a perpetual hybrid where the market expects a call."
anti_trigger: "Not for predicting the call, and not for plain bond pricing."
scope: "Perpetual structures and the call the market expects."
status: seedling
---

# Perpetuals and call expectations

## Standard

A perpetual hybrid has no maturity, and the market prices it as though it will be called on the first call date. That convention makes the yield to call the relevant yield, and it makes the instrument sensitive to the issuer's refinancing conditions: if refinancing becomes expensive or impossible, the call does not happen, the instrument extends, and its duration extends with it.

Extension risk is the whole of the analysis. A perpetual trading at a yield to call of six percent and a yield to perpetuity of nine percent is telling you that the market assigns a probability to extension, and that probability moves with the issuer's credit and with the level of rates. Reading the yield to call alone hides the outcome that hurts.

Primary sources: <https://www.bis.org/> and <https://www.sec.gov/investor>.

## Decision rules

- Record the first call date, the call price, and any step-up in coupon after it.
- Compute yield to call, yield to the next call, and yield to perpetuity.
- Record the difference between them as the market's extension premium.
- Record the issuer's refinancing conditions and any regulatory constraint on calling.
- Record the coupon step-up or reset mechanics after the call date.
- Record the duration under the extension scenario.

## Procedure

1. Extract the call schedule and any coupon step-up.
2. Compute yield to each call date and to perpetuity.
3. Record the spread between them.
4. Record the issuer's refinancing capacity.
5. Compute duration under extension.
6. Write the analysis with the extension scenario.

## Anti-patterns

- Quoting yield to call as the instrument's yield without the alternative.
- Assuming the call happens because it is expected.
- Ignoring a coupon step-up that makes calling expensive.
- Treating duration as short when extension is possible.
- Forgetting regulatory permission as a condition on the call.

## Done checklist

- [ ] Call schedule and step-up recorded.
- [ ] Yields computed to each date and to perpetuity.
- [ ] Extension premium recorded.
- [ ] Refinancing conditions recorded.
- [ ] Duration under extension computed.
- [ ] Extension scenario written.

The extension scenario deserves a number rather than an adjective: computing the price at which the instrument would trade if the call were not exercised, at the current credit spread and a longer duration, converts an abstract risk into a mark that can be compared with the market's, and the comparison is what makes the extension premium legible.

## Sources

- Hybrid capital standards: <https://www.bis.org/>
- Instrument disclosure: <https://www.sec.gov/investor>
- Rate data: <https://fred.stlouisfed.org/>
