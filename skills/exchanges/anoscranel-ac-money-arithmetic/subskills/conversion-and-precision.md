---
name: conversion-and-precision
domain: software-engineering/conversion-and-precision
trigger: "Converting between currencies and choosing display precision."
anti_trigger: "Not for FX trading decisions, and not for rate sourcing policy."
scope: "Currency conversion, the rounding sequence, and display precision."
status: seedling
---

# Conversion and precision

## Standard

Converting an amount between currencies requires a rate and a rounding decision, and the order of those two operations changes the result. Converting then rounding is the common convention; rounding then converting can lose a unit in either direction. When several conversions chain, the intermediate precision and the rounding points decide whether the original amount can be recovered.

Display precision is a separate decision from calculation precision. An amount may be calculated to six decimals and displayed to two, and the display rounding must not feed back into stored values. The record states the rate's source and direction, the conversion rounding, and the precision retained internally.

Primary sources: <https://www.iso20022.org/> and <https://www.iso.org/>.

## Decision rules

- Record the rate source, its quotation direction, and its timestamp.
- Record the precision retained in the rate itself, since a rounded rate introduces error.
- Record the conversion rounding and the order relative to other operations.
- Record the intermediate precision for chained conversions.
- Record the display precision and confirm it never affects stored values.
- Record the tolerance within which a round-trip conversion is considered to have recovered the original.

## Procedure

1. Record the rate source, direction, and timestamp.
2. Record the rate's precision and its effect on the result.
3. Record the conversion rounding and its position in the calculation.
4. Record intermediate precision for chains.
5. Separate display rounding from stored values.
6. Test a round-trip conversion and record the discrepancy.

## Anti-patterns

- Converting with a rate rounded to fewer digits than the result requires.
- Rounding before converting and again after.
- Displaying a rounded value and storing the displayed value.
- Chaining conversions through the display currency.
- No round-trip test, so the error is discovered in reconciliation.

## Done checklist

- [ ] Rate source, direction, timestamp recorded.
- [ ] Rate precision recorded.
- [ ] Conversion rounding recorded with position.
- [ ] Intermediate precision recorded.
- [ ] Display precision separated.
- [ ] Round-trip tested.

The rate's own precision is the input that most often limits the result: a rate quoted to four decimals applied to a large amount produces an error far larger than the rounding of the converted amount, and the record should state the rate's precision alongside the conversion's.


The direction of a quoted rate is worth recording explicitly because the cost of an inverted rate is enormous and the error is not visible in testing: a system that applies the reciprocal without checking produces amounts off by the square of the rate, which for most pairs is a discrepancy no reconciliation tolerance would absorb.


## Sources

- Payment messaging and currency standards: <https://www.iso20022.org/>
- Currency representation standards: <https://www.iso.org/>
- Market rate reference: <https://www.bis.org/>
