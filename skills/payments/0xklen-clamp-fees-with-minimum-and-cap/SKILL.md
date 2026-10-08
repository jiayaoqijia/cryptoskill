---
name: clamp-fees-with-minimum-and-cap
description: Use when a fee has a floor, a ceiling, or both (payment-processor minimum, percentage capped). Applies the clamp in integer minor units and keeps the fee inside the allowed band.
---

# Clamp fees with minimum and cap

Fees are rarely a clean percentage: processors charge `max(min_fee, min(cap_fee, bps_fee))`. Apply the clamp after the rate, in minor units, and make the order (floor then cap) match the contract.

## Procedure

1. Compute the percentage part exactly: `raw = mulDiv(amount, fee_bps, 10_000)` with the chosen rounding.
2. Apply the floor, then the cap: `fee = min(cap, max(floor, raw))`. State the order — `min(max(...))` and `max(min(...))` differ once `floor > cap`.
3. Reject an impossible band at load: if `floor > cap` the config is wrong; fail loudly when reading config, not at charge time.
4. Confirm cap semantics: a cap is usually a fixed amount per transaction ($0.50), not a rate. Record its currency and minor unit with it.
5. Check the clamped fee against the amount: a $0.50 floor on a $0.30 charge exceeds the principal — either allow `fee > amount` or reject the transaction explicitly.
6. For cumulative caps ("first $100 of fees waived"), track usage in integer minor units and decrement a counter; never accumulate a float total.
7. Store the band as integer minor units in config, e.g. `{"floor_minor": 30, "cap_minor": 50, "bps": 290}`.
8. Log all four numbers — amount, raw, clamped, and which bound bound — so an auditor sees why the fee is what it is.
9. Return the bound that applied in the API response (`fee: {amount_minor: 30, reason: 'floor'}`) so support can explain a charge.
10. Version the fee config and snapshot it per transaction; a floor change must not retroactively alter historical fees.
11. Test the exact boundaries: the amount where the bps fee crosses the floor, and where it crosses the cap.

## Pitfalls

- Applying the cap before the floor silently neuters the floor whenever `cap < floor`.
- A cap written as "$5.00" parsed with `parseFloat` is a float `5.0`; store `500` cents.
- Off-by-one on `>=` vs `>`: a fee exactly at the cap should pass unchanged, not be clamped a second time.
- Currency blindness: a USD cap applied to a EUR charge without conversion clamps by the wrong magnitude.
- An accumulated float "fees waived so far" drifts; use integer minor units and a hard compare.
- A floor that is a percentage of a different base than the fee (a per-transaction minimum vs a monthly rate) is not a clamp at all — it is two fees.
- A cap stored as a rate (`0.005%`) rather than a fixed amount gets applied as a percentage and never binds correctly.

## Verification

    python3 -c "raw=45; floor=30; cap=50; print(min(cap, max(floor, raw)))"   # 45, inside the band
    # boundary: raw=10 -> 30 (floor), raw=99 -> 50 (cap)

Report the floor, cap, raw fee and clamped fee in minor units, plus the clamp order used.
