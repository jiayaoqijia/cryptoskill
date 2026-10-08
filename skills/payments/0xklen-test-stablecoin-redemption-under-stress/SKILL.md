---
name: test-stablecoin-redemption-under-stress
description: Use when you must know whether a stablecoin will actually redeem to fiat when it matters. Walks the issuer's redemption path, its gates and limits, and rehearses it before a stress event.
---

# Test stablecoin redemption under stress

The peg promises par redemption, but the promise has conditions: minimum size, KYC, business-day settlement, and per-day caps. Test the path when calm so you are not discovering the gates during a run.

## Procedure

1. Read the issuer's current terms: minimum and maximum redemption, fee, whitelist/KYC requirement, and settlement (T+0 wire or T+N).
2. Establish the redemption counterparty: the issuer's own portal, a primary dealer, or a bank. Confirm your entity is eligible *before* you need it.
3. Rehearse a small redemption end to end and time it: submit, confirm instructions, receive fiat. Record the actual elapsed time, not the advertised quote.
4. Identify the caps: per-transaction, per-day, and per-entity limits. An entity capped at $1M/day cannot exit $20M in a week.
   `python3 -c "cap=1e6; need=20e6; print(-(-need//cap))"`  -> 20 days.
5. Check the on-chain leg for crypto-backed coins: PSM `tout()` fee, and whether the PSM debt ceiling is full (`line` vs `Art*rate`), which blocks redemption at par.
6. Model a stress case: 10% of supply redeeming in 48h against per-day caps and available stable reserves.
7. Write the exit plan: who calls whom, what the caps are, and the realistic time-to-fiat for your size.

## Pitfalls

- Reading the fee schedule but not the business-day clock: a Friday 4pm submission settles Tuesday.
- Assuming your entity is whitelisted because a sibling entity is.
- A PSM at its debt ceiling offers no par redemption regardless of the advertised 0% fee.
- Redemption that requires burning the token you already lent out or posted as collateral.
- Treating a primary-dealer relationship as portable across issuers and jurisdictions.
- Testing with a whitelisted entity while your production entity is not; the rehearsal passes and the real run fails.
- Redemption minimums can exceed your test size, forcing a larger test than intended.
- A bank holiday in the issuer's jurisdiction adds a day the schedule does not mention.

## Verification

    python3 -c "cap=1e6; need=20e6; print(-(-need//cap))"
    20
    # rehearse a live small redemption and record actual time-to-fiat

Report the redemption gates, the real settlement time, the per-day cap, and the days-to-exit for your position.
