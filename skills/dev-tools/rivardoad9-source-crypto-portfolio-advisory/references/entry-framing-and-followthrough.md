# After the screen: re-pricing, late-vs-early framing, and wiring the exit

Extends `entry-screen-liquid-majors.md` (the mechanical screen → structure verification → HBAR worked
example). This file covers what happened *after* that write-up went out: the pick decayed within the hour,
the user challenged the framing, and then decided to enter. Worked 2 Okt 2026.

## 1 — Re-price the pick before the user acts (it decays within the hour)

Twenty minutes after the HBAR message the tape had moved: 0,1068 → **0,1063**, doing **+1,6% while BTC did
+3,1%**. Re-check unprompted and fold the update into the fill plan in the *same* message. A recommendation
that has quietly rotted is worse than no recommendation.

Grade a "post-spike flag" with three numbers, never a vibe:

1. **Retracement of the spike** (Fib over spike low→high). 0,0941→0,1310 with price 0,1063 = **66%
   retraced**, i.e. *below* the 61,8% rung (0,1082) → the pullback is already **deep**, not textbook
   healthy. Report it as "flag-nya dalem", not as "flag".
2. **Volume vs its own 30d average** that day: $10,7jt vs $22,5jt → below-average volume means nobody is
   accumulating yet. That is a *watch*, not an entry.
3. **Relative strength vs BTC on the day** — up 1,6% inside a +3,1% BTC tape is the opposite of the flow you
   want going into a breakout entry; say it explicitly.

## 2 — Framing: "pullback after the run" is NOT "early"

Best R:R on the board answers **what**, not **when**. HBAR was already +43%/30d with a +27,2% single-day
spike, so the honest label is **"pullback setelah lari"** — a *continuation* bet, not an early position.
Quantify with 30d %, pos90, and distance/retracement from the spike high.

The user will ask exactly *"brrti skrng <X> lebih oke dan ga telat ya?"* — and "lebih oke" (R:R) must not
be allowed to answer "ga telat" (timing). Answer in two halves, plainly: R:R better = yes; not-late = no,
with the numbers.

**Disclose a lane change explicitly.** When the new pick lives in a **different narrative** than the one
under discussion (gaming/NFT/metaverse → RWA/AI-enterprise), open by saying the lane changed *and why* (the
old lane is late: pos90 85–100%). The user tracks continuity across messages and calls it out — *"naratifnya
ga sesuai yg tdi lu blg?"*. The fix is to state the switch + the data reason, never to defend the old pick
or pretend the new one came from the same thesis.

## 3 — After the user decides ("oke gw entry X"): wire the exit side

The deliverable is not "entry 0,103–0,107". One message carries all of:

- **Limit ladder, not market.** R:R at each rung is the argument: market 0,1063 → 1,89 · 0,1050 → 2,39 ·
  0,1025 → 4,08. Name which rung is the plan and note that a market order on a thin CEX book pays the
  spread for nothing.
- **Sizing table by risk** — position = (risk % × modal) ÷ stop-distance %. Modal $1.400 → risk $28 (2%) →
  ~$340-390 · risk $42 (3%) → ~$500-590. Add the liquidity ceiling: an order ≈ 1-2% of the pair's 24h
  volume is safe **with limits** ($300-500 vs HBAR's $23jt/day).
- **Then wire the SL/TP** — the position goes into the holdings watchdog so the user gets delta-only pings
  at the stop and at each target instead of watching charts. Recipe:
  `hermes-cron-automation → references/post-entry-sltp-wiring.md`.
- **Say the monitor is live and was test-fired** (fires once, silent on repeat). This user reads wiring as
  proof of action.
- **Ask for the actual fill price** and update the record — the alert prints % vs the planned entry, so a
  different fill makes those percentages wrong.
- Repeat the honest caveat: if the limit never fills and price breaks the confirmation shelf, the remaining
  option is a breakout entry with a worse R:R (~1,4) — say the number before it happens, not after.
