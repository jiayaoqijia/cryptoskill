# Decomposing the portfolio health score ("kenapa skor porto gw N?")

Companion to `portfolio-risk-monitor.md` §1 (which defines the component weights and grades). This file
covers the *follow-up question the user actually asks after seeing the number* — and the trap of
answering it with a recommendation that will not move the number at all.

Reference implementation: `~/.hermes/scripts/porto_risk.py --save` → `~/.hermes/data/porto_risk.json`,
served at `/api/risk` on the board server (`localhost-dashboard-serving`).

## 1. The formula

```python
port_score = Σ (health_i × usd_i) / Σ usd_i     # summed ONLY over assets that have a health value
```

Two consequences that decide how you answer:

1. **It is size-weighted**, so the biggest positions own the score — a small position cannot rescue it.
2. **Cash is not in the roll-up at all.** Stablecoin balance changes `idle_pct` and the allocation chart,
   never `port_score`.

## 2. Answer it as arithmetic, per holding

Never say "the score is a blend". Print the legs and multiply them out.

Worked 8 Okt 2026 (live `/api/risk`: score **56**, grade **C**, total $1.287,29, idle 40,2%):

| leg | weight (ex-cash) | health | grade |
|---|---|---|---|
| TAO | 49,7% | 52 | C |
| SUI | 33,6% | 57 | C |
| SOL | 13,0% | 63 | B |
| BOME | 3,8% | 74 | B |

`0,497×52 + 0,336×57 + 0,130×63 + 0,038×74 = 56`

The sentence that carried the explanation: **two grade-C names held 83% of invested capital and therefore
own the score, while the two healthiest positions were the two smallest** — 74 (BOME) and 63 (SOL) sat at
3,8% and 13,0%. The score is *inverted relative to what is working*, and that — not the number — is the
actionable finding.

Then name the per-token reasons straight from `assets[].flags`: TAO 52 = "tren campur (belum konfirmasi
arah)" + whale signal thin ($2,4M across 3 wallets) + weight 29,7% of equity; SUI 57 = whale thin ($8,8M,
2 wallets) + weight 20,1%; BOME 74 would grade higher but is capped at B by small market cap (MC $74,3M,
rank #361).

## 3. SIMULATE before you recommend — this is the load-bearing rule

Because cash is outside the roll-up, "trim into cash" is close to a no-op. Verified on that book:

| scenario | score |
|---|---|
| now | **56** |
| trim TAO to 20% of equity (≈$125 sold into cash) | **57** |
| trim TAO **and** SUI to 20% each (cash → $643) | **57** |
| TAO 52→62, SUI 57→65 (trend confirms, size unchanged) | **64** |

**Do not tell the user "trimming will improve your health score."** It moves 1 point, because the moment
TAO shrinks, SUI becomes the largest weight and SUI is also grade C. Only two things move the score:

- (a) the **heavy** holdings confirming their trend — needs price back above entry plus whale confirmation
  that is more than 2–3 wallets; or
- (b) **replacing composition** with genuinely healthier names — not shrinking into cash.

So when the honest answer to "should I trim?" is yes, justify it with the concentration cap / structural
reasons, *and explicitly say it will not lift the health score*. Promising a score fix that the arithmetic
cannot deliver is the failure mode here. Run the simulation in Python and print the rows; the user reads
tables as proof.

## 4. Decompose the `risk.why` list — it mixes two currencies

`risk` carries portfolio-level flags that are **not** part of the score. Separate them out when asked:

| field | meaning | in the score? |
|---|---|---|
| `hhi`, `eff_n` | concentration / effective number of names (worked: HHI 0,38 → 2,6 names) | no |
| `n` tokens grade C/D in `why` | holdings-quality line — this one IS the score's driver | indirectly |
| `weighted_beta`, `weighted_vol_d`, `stress.btc_-15pct / -30pct` | direction risk (worked: β 1,51, σ 5,35%/day, BTC −30% ⇒ −45,3%) | no |
| idle cash % | **drag, not direction risk** | no |
| `macro.verdict` | regime headwind, e.g. "duit ngumpul di BTC" (BTC.D 58,75%, +1,60pp/7d) | no |

Call out the asymmetry explicitly: an unlabelled "40% modal nganggur" reads to the user as a warning when
it is the *opposite* of leverage risk. Say which line is drag and which is danger.

## 5. ±1 wobble is noise, not a discrepancy

The score and the grade move a point between ticks (1-point deadband at grade boundaries so a 61↔62 jitter
doesn't flip the class). When the user quotes a number slightly off the live one ("skor gw 57" vs live 56),
give the fresh live value and say the wobble is the deadband — do not go hunting for a missing point.
