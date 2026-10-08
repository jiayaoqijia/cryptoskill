---
name: unwind-vesting-schedule-to-circulating-supply
description: Use when projecting circulating supply month by month from a vesting schedule, finding unlock dates, or checking a token's float trajectory. Handles cliffs, linear vesting, and unlocked-but-unsold balances.
---

# Unwind vesting schedule to circulating supply

Circulating supply is not "what is not in a vault"; it is initial float plus everything whose cliff has passed and linear vesting accrued, and the schedule must be reconstructed month by month to see the unlock cliff.

## Procedure

1. Bucket the allocations with (share, cliff_months, vest_months): e.g. seed 15% / 12 / 36, team 20% / 12 / 48, community 40% / 0 / 48, treasury 25% / 0 / 0.

2. For each bucket, vested at month m = `0` if `m < cliff`, else `share * min(m - cliff, vest) / vest`.

3. Worked example, 1,000,000,000 supply:
   - seed 150M, cliff 12, vest 36 → m=12: 0; m=24: `150M*12/36 = 50M`; m=48: 150M.
   - team 200M, cliff 12, vest 48 → m=24: `200M*12/48 = 50M`; m=48: 150M; m=60: 200M.
   - community 400M, vest 48 → m=24: `400M*24/48 = 200M`.

4. Sum per month and divide by total supply for the float. Python the whole schedule rather than hand-summing:

   python3 -c "sup=1e9; [print(m, round(1e6*(150*min(max(m-12,0),36)/36 + 200*min(max(m-12,0),48)/48 + 400*min(m,48)/48),1)) for m in (12,24,36,48,60)]"

5. Find the cliff: the month where `Δcirculating / circulating` is largest. Seed + team unlock together at m=24 adds 100M to an otherwise ~400M float — a classic 25% cliff.

6. Distinguish vested from circulating: vested-but-still-in-a-contract is not float; "circulating" per aggregators excludes team/treasury inconsistently. Track both and the tradeable float separately.

## Pitfalls

- Assuming an aggregator's "circulating" equals tradeable float — it often double-counts or inconsistently excludes staking locks.
- Treating a cliff as linear: the month after the cliff vests the whole cliff amount at once, not spread across the vest.
- Ignoring unlocked-but-unsold treasury: not float now, but a standing overhang the moment it moves.

## Verification

    python3 -c "print(150e6*12/36 + 200e6*12/48 + 400e6*24/48)"
    300000000.0

Month-24 vested sums to 300M; compare to the project's stated float for that month.

Report the float curve, the largest single-month unlock, and its % of float.
