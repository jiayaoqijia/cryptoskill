---
name: scale-amounts-between-token-decimals
description: Use when converting an amount between currencies or tokens with different decimal scales (USDC 6, ETH 18, cents 2). Scales by integer powers of ten and refuses lossy conversions.
---

# Scale amounts between token decimals

Moving an amount between scales — 6-decimal USDC, 18-decimal ETH, 2-decimal cents — is a multiply by `10 ** (to_exp - from_exp)` that must never silently drop a digit. Convert with integer powers of ten and prove no unit was lost.

## Procedure

1. Read the real exponent from the source, not from memory: `cast call $TOKEN "decimals()(uint8)" --rpc-url $RPC`; for fiat keep the ISO-4217 minor-unit table `{"USD":2,"USDC":6,"ETH":18}`.
2. Scaling **up** (fewer decimals -> more) is exact: `amount * 10 ** (to_exp - from_exp)`. `1234` cents -> `1234 * 10**4` = `12_340_000` at 6 dp.
3. Scaling **down** (more -> fewer) truncates and can lose value: `amount // 10 ** (from_exp - to_exp)`. `1234` wei -> cents is `0`; refuse or round explicitly — never let it vanish.
4. Branch on the sign of the delta: `d = to_exp - from_exp; amount * 10**d if d >= 0 else round(amount / 10**(-d))`.
5. Guard overflow: at 18 dp, `amount * 10**12` can exceed uint256 or int64. Check `amount <= MAX // 10**delta` first, or use bigint.
6. When a rate is involved, do it in one expression and round once: `out = mulDiv(amount, rate, 10**rate_exp)`, not scale-then-multiply-then-scale.
7. Never scale by a float literal: `int(amount * 1e6)` multiplies by a float first and is wrong past 2^53. Multiply by the integer `10**6`.
8. Record the input exponent, output exponent and both amounts in the log so a mismatch is auditable.
9. When both exponents are equal, return the amount unchanged; the `10**0` branch documents intent but the early return avoids a pointless multiply.
10. For a cross-chain bridge, convert to the canonical 18-dp base unit at the boundary and keep the source decimals in metadata only.
11. Snapshot the token's `decimals()` alongside the transfer — a proxy upgrade can change it beneath you.
12. Test the extremes: a 0-decimal token and a 24-decimal token must both round-trip through your conversion.

## Pitfalls

- Assuming every ERC-20 is 18 decimals: USDC is 6, WBTC is 8, some are 0 or non-standard. `decimals()` is authoritative.
- Scaling down with truncation on a payout shortchanges the recipient by up to `10**(from-to) - 1` base units; round in the payer's favour or refuse.
- Double-scaling: cents -> dollars -> wei applies the exponent twice, turning a $1 order into 100x.
- A rate stored at 18 dp multiplied by an amount at 6 dp without aligning scales is off by 10^12.
- Treating a wrapped token's decimals as the underlying's when the two differ.
- A custom ERC-20 whose `decimals()` reverts or returns a huge value breaks a naive `10**d`; clamp and validate the range (0-30).

## Verification

    cast call $TOKEN "decimals()(uint8)" --rpc-url $RPC
    python3 -c "from decimal import Decimal as D; a=D('1234'); print(a*10**4, a.scaleb(4))"   # both 12340000

Pass when the up-scale round-trips exactly and every down-scale carries an explicit rounding. Report the exponents read on-chain and the conversion factor used.
