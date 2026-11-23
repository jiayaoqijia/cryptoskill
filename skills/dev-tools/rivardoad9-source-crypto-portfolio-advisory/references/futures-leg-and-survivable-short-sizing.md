# Futures leg & survivable short sizing (worked session, 8 Okt 2026)

## 1. Verify the chart claim before agreeing or disagreeing

"Order block / demand zone" claim — recipe straight from daily klines, no opinions:

1. Find the **pre-breakout consolidation**: the range just before an impulsive up candle.
   Session: BTC **18–20 Sep range 80.126 – 81.951** (three days, ~10k volume/day).
2. Find the **impulse day + volume multiple**: 21 Sep breakout to 86.620 on **31.963** (≈3x daily).
   The consolidated range *is* the zone.
3. Check **retested or not**: post-breakout low 82.228 → the zone had never been touched again.
4. Look for **confluence**: daily EMA50 at **79.634** sat right under the zone, so 79,6–81,9k is
   order block + EMA50, not just a hand-drawn line.
5. Do the same for the coin actually traded: ETH basis 18–20 Sep **2.437–2.564** (impulse 21 Sep
   to 2.807) → downside targets **2.503** (EMA50d, inside the zone) and **2.440** (basis low).
6. Translate index level → alt with beta: BTC 81.500 → ETH ≈ 2.507; BTC 80.100 → ETH ≈ 2.454
   (ETH/BTC beta ≈ 1,22 on these moves).

A *correct* user read gets said out loud, with the numbers that prove it. Reflexive disagreement
annoys this user; invented support does too.

## 2. "Harus" is not a position — convert it to a probability

Replace conviction words with market pricing: Polymarket *touch* markets + Deribit strike ladder gave
touch-80k-in-October ≈ **69,5%**, touch-82,5k ≈ **93,5%**, touch-77,5k ≈ **44,5%**. So the read was
"likely", not "certain" — and that distinction carries the whole lesson, because the failure mode lives
on the other path.

## 3. Price the thesis being RIGHT (the check people skip)

Replay the *whole* book at the target, not just the short leg. Session ($1.286 equity: longs TAO $380 /
SUI $257 / BOME $29 · short ETH 0,312 = $798 · betas TAO 1,57 · SUI 1,53 · BOME 1,45 · ETH 1,22):

| BTC path | long sleeve | short ETH | net |
|---|---|---|---|
| → 81.500 (−1,7%) | −$17,82 | +$16,55 | **−$1,28** |
| → 80.100 (−3,4%) | −$35,56 | +$33,02 | **−$2,55** (−0,20%) |

Being right earned nothing, because the long-alt sleeve and the short leg are *one trade*:
30d correlation ETH↔SOL **0,82** · ETH↔TAO **0,61** · ETH↔SUI **0,60** · ETH↔BOME 0,44 (BTC↔ETH 0,91).
Say it plainly: *bener soal arah ≠ dapet duit*.

## 4. Price the other path — the squeeze

Same book, BTC +5,5% first → ETH ≈ 2.735 while liq sat at **2.708,92**. Right thesis, dead account.
This is how "arah dulu, baru ukuran" gets taught with numbers instead of a lecture.

## 5. Shape delivery

- 3 size options as a table (qty / margin / lev / liq / risk $ / TP $), computed live. Isolated short
  liq: `liq ≈ mark × (1 + 1/lev − mmr)`, ETHUSDT bracket 1 mmr 0,40%. SL always *inside* liq.
- Set ISOLATED **before** opening (CROSS makes the whole futures wallet the collateral behind a leg).
- Trim the sleeve that contradicts the stated thesis (TAO 29,6% → 20% = −$122,87) so cash becomes the
  real bearish position (~54% of equity) — and name what actually earns: the cash buying the zone,
  not the small short. The short is just so something feels the move.
- Invalidation written *before* entry: BTC daily close > 85.500 · ETH 4H close > 2.615 (EMA200 4H).
  Plus "satu ide satu stop, jangan rata-rata bawah" and "kalau kena SL bukan tanda salah baca".
- State the read-only boundary: this agent reads the exchange, the user clicks, verification afterwards
  comes from trade history (`references/executed-trade-verification-and-gaps.md`).
- Close by naming what's still net (long $543 vs short $256 ⇒ net long ±$287, 22% equity) so the user
  knows the book is *resilient with ammo*, not aggressively short.

## Pitfalls

- An f-string that builds a format spec from arithmetic can raise
  `ValueError: Invalid format specifier` — precompute into a variable first.
- Don't call leverage conviction: 150x cross with liq 5,8% away is an expiry date, not a stronger view.
