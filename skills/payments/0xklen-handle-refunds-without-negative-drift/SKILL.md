---
name: handle-refunds-without-negative-drift
description: Use when refunding a captured payment, in full or in part, possibly with a fee. Reverses in integer minor units, caps the sum of refunds at the capture, and keeps the ledger's rounding consistent with the charge.
---

# Handle refunds without negative drift

A refund reverses a capture, but the original fee, a partial amount, and integer rounding can leave the refund total off by a cent from the charge. Track refunded-to-date in minor units and refuse to over-refund beyond the capture.

## Procedure

1. Store the original capture as `captured_minor` — the amount the customer actually paid, after any fee — not the requested gross.
2. Keep `refunded_minor` as a running sum of integer refunds; assert `refunded_minor + new_refund <= captured_minor` before posting anything.
3. For a partial amount typed by a user, parse it to minor units (see `parse-locale-money-input`) and cap it at the remaining refundable balance.
4. Decide fee handling explicitly: fee-not-returned (the processor keeps its fee), fee-pro-rated (refund `captured * amount / total`), or fee-returned. Each changes the net and the reconciliation.
5. For a pro-rated refund of a fee that was itself rounded, round the refund in the same direction as the original charge so the pair nets cleanly; do not re-derive it from the raw rate.
6. Record the refund as a new ledger entry that references the original (see `keep-an-append-only-money-ledger`) — never mutate the capture.
7. Reverse in the original transaction currency; a refund in a different currency needs its own FX snapshot and is a separate movement.
8. Assert the invariant across multiple partials: `captured_minor - sum(refunds_minor) >= 0`.
9. Store the original fee separately from the capture so a fee-pro-rated refund can recompute it exactly.
10. Reject a refund of a capture that is already fully refunded, with the remaining balance in the error.

## Pitfalls

- Refunding tax (`amount * 0.19`) and goods (`amount`) as two rounded figures can exceed the original by a cent.
- Using the gross requested amount when the capture was net of a fee over-refunds the customer.
- Floats in the running `refunded` total drift across many partials; an integer running sum does not.
- Card refunds expire after roughly 120–180 days at some networks; the reversal then becomes a manual credit, a different path.
- Not idempotent: a retried refund API call double-refunds; use an idempotency key.
- A currency mismatch between charge and refund creates an FX movement a naive "same amount" check misses.
- Reversing the fee on a full refund but not on partials (or the reverse) makes the reconciliation drift.
- A refund processed while the original is still pending can settle before the charge and invert the ledger; block it until the capture is final.

## Verification

    python3 -c "cap=10000; parts=[3000,3000,3999]; assert sum(parts)<=cap; print(cap-sum(parts))"   # 1 minor unit left, cannot refund 4000
    # every refund is a new post; sum(refunds) + remaining == captured

Report the captured amount, refunded-to-date, remaining refundable, and the fee policy applied.
