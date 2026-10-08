---
name: rounding-direction-truncation
description: Use when auditing integer maths in a contract that divides, multiplies with scaling, or converts between decimals. Checks each division rounds in the protocol's favour and guards against truncation to zero.
---

# Rounding direction and truncation

Solidity integer division truncates toward zero, so every `a / b` silently favours one party — the review is to decide which party and whether that is the safe one.

## Procedure

1. Find all divisions and scale conversions: `grep -nE '/ *[0-9a-zA-Z_(]|/ 1e|mulDiv|wadDiv|rayDiv' -r src/`.
2. For each, name the direction that is *safe*: shares minted to a user round DOWN, assets paid out to a user round DOWN, debt owed by a user rounds UP.
3. Confirm the wrap: in OpenZeppelin `Math.mulDiv`, pass `Math.Rounding.Floor` when the user receives the result and `Math.Rounding.Ceil` when the protocol receives it.
4. Check the multiply-before-divide rule: `(a * b) / c` must not overflow; use `mulDiv`, which widens to 512-bit.
5. Hunt truncation-to-zero: any `amount / rate` where `rate > amount` returns 0, letting a user pay zero for a non-zero asset.
6. Check fee maths: `fee = amount * feeBps / 10_000` rounds down, so the protocol under-collects; verify a dust attacker cannot loop with `amount = 1` and pay `fee = 0`.
7. Test the boundary with a fuzz test that asserts monotonicity:

```solidity
function testFuzz_noFreeShares(uint96 assets) public {
    uint256 shares = vault.previewDeposit(assets);
    if (assets > 0) assertGt(shares + vault.totalSupply(), 0);
}
```

8. Confirm rounding is applied *after* aggregation, not per-leg, in multi-hop conversion functions.
9. Verify a decimal conversion (`1e6` USDC to `1e18` shares) uses `10 ** (18 - 6)` and cannot be reversed by rounding.
10. Record each division, its direction, and the party that benefits.

## Pitfalls

- `previewX` (view) and `X` (state-changing) use different rounding; integrators trust the wrong one and over-withdraw.
- `mulDiv` default rounding is Floor; using it for a debt calculation rounds the attacker's debt down every block.
- Percentage fee computed on a per-second drip: truncation to zero makes a flash-loan in-out free in the same block.
- Casting `uint256` to `uint128`/`int128` without a bounds check wraps silently.
- Combining two truncated values (`a/b + c/d`) when `(a*d + b*c)/(b*d)` was intended.

## Verification

    forge test --match-test "testFuzz.*[Rr]ound" -vv

Pass: the fuzz run reports 256+ runs with no counterexample. Add `fail_on_revert = true` under `[fuzz]` in `foundry.toml` so a revert is a failure, not a skip.

Report each division site, its rounding direction, and the benefiting party.
