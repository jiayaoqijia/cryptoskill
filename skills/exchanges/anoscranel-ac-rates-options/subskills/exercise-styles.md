---
name: exercise-styles
domain: investing/exercise-styles
trigger: "Working out when a rates option can be exercised and what that implies."
anti_trigger: "Not for predicting rates, and not for model calibration."
scope: "European, Bermudan, and American exercise, and mid-curve expiries."
status: seedling
---

# Exercise styles

## Standard

A European swaption is exercised once, at expiry. A Bermudan swaption can be exercised on a schedule of dates, which is what a callable bond or a cancellable swap contains, and its value depends on the optimal exercise strategy across all of those dates. An American option can be exercised at any time, which in rates is rare outside specific instruments.

Bermudan structures are where the modelling matters most. The exercise decision at each date depends on the future path of rates and on the remaining exercise opportunities, so the value is a function of the whole schedule rather than of a single date. Two models that agree on a European swaption can disagree materially on a Bermudan, and the record should name the model and its calibration.

Mid-curve options are a separate convention: they expire into a swaption rather than into a swap, so the buyer acquires the right to enter an option later. They are quoted by expiry and by the underlying swaption's expiry and tenor, and that double dating is a common source of error.

Primary sources: <https://www.cmegroup.com/> and <https://www.bis.org/>.

## Decision rules

- Record the exercise style and, for Bermudan, the full schedule of dates.
- Record the model used and its calibration instruments.
- Record the sensitivities with the model named.
- For mid-curve options, record both expiries and the underlying tenor.
- Record the notice period required for exercise and any automatic exercise rule.
- Record whether exercise is cash or physical into the swap.

## Procedure

1. Record the exercise style and dates.
2. Record the underlying and its tenor.
3. Record the model and calibration.
4. Record notice requirements and settlement.
5. For mid-curve, record the double dating explicitly.
6. Write the exercise summary with its assumptions.

## Anti-patterns

- Valuing a Bermudan as a single European swaption.
- Reporting a model's greeks without naming the model.
- Confusing a mid-curve option's expiry with the underlying's.
- Ignoring the notice period for exercise.
- Assuming physical settlement when the confirmation says cash.

## Done checklist

- [ ] Exercise style and dates recorded.
- [ ] Underlying and tenor recorded.
- [ ] Model and calibration recorded.
- [ ] Notice and settlement recorded.
- [ ] Mid-curve dating recorded where applicable.
- [ ] Assumptions written.

## Sources

- Exchange and market conventions for rate options: <https://www.cmegroup.com/>
- Market standards: <https://www.bis.org/>
- Rate and volatility data: <https://www.federalreserve.gov/>
