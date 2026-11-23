# Pre-event binary risk decisions: "cut all position or biarin aja"

Companion to `drawdown-and-trim-decisions.md` (§2 trim sizing in ATR units, §3 hedge-instead-of-argue).
Worked 7 Okt 2026 — ~$1,3k alt book, asked ~6 hours before the FOMC **minutes** print (01:00 WIB).
Script: `scripts/cut_or_hold_scenarios.py` (stdlib, runnable offline against the snapshot).

Trigger: the user drops a *binary* within hours of a scheduled macro event. Answer with a four-option
matrix and a recommendation, never with a vote on direction.

## 1. The reframe that ends the panic

A full exit does **not** reduce what was already lost. It converts unrealized into realized — i.e. it is a
**100 % directional bet**, not capital protection. Prove it with the recovery math, both ways, in the same
message:

| setelah | modal $1.401,02 butuh |
| --- | --- |
| CUT-ALL (semua jadi USDT $1.286,81) | **+8,9 %** |
| DIAM (porto $1.288,65) | **+8,7 %** |

The $1,71 round-trip fee is the *entire* difference. Say that line out loud; it usually closes the question.

## 2. Build the matrix instead of picking a side

Four options × the macro scenarios, in **$ totals** (read: the two tails must be compared side by side):

| skenario (book = 2,4x BTC) | HOLD | TRIM-TO-CAP | EXIT-THESIS-DEAD | CUT-ALL |
| --- | --- | --- | --- | --- |
| hawkish BTC −5 % | $1.134 | $1.218 | $1.252 | **$1.287** |
| hawkish dalam BTC −8 % | $1.044 | $1.177 | $1.232 | **$1.287** |
| netral (event-study rata-rata) | $1.271 | $1.280 | $1.283 | $1.287 |
| bounce BTC +3 % | $1.379 | $1.328 | $1.308 | $1.287 |
| squeeze BTC +5 % | **$1.430** | $1.352 | $1.319 | $1.287 |

Near-symmetric tails (≈$150 down vs ≈$143 up) ⇒ cut-all is a coin flip, and the *middle* options beat it on
both sides. That asymmetry check is the whole analysis; print it as a table, don't narrate it.

## 3. Rank options by the user's own rules, not by feeling

The 12 % cap plus check-6 (thesis/control) state decide which coin goes where:

| coin | weight | state | action |
| --- | --- | --- | --- |
| ONDO | 41,4 % | over cap **and** thesis-dead (control/succession) | cut to cap, or exit fully |
| TAO | 22,7 % | over cap, thesis alive | trim only the over-cap |
| WLD | 15,1 % | over cap, no catalyst | trim |
| VIRTUAL / BOME | 7,8 % / 1,3 % | inside cap | leave, or include in a dead-thesis sweep |

Cap-first trim executed: sell $556,32 (ONDO 816,65 unit + TAO 0,4715 + WLD 78,41) ⇒ realized −$57,35, fee
$0,83, USDT 11,7 % → **54,8 %**. Give **exact unit quantities** — this user clicks in the app himself — plus
one line: *"kalau masih nggak bisa tidur, tambahin keluar penuh dari &lt;thesis-dead coin&gt; — bukan jual
&lt;best-conviction coin&gt;."*

## 4. What to say about the event itself

- Round-trip cost is never the driver at this size (0,1 % + ~0,05 % spread ≈ $1,7 on a $1,3k book).
- State when cut-all IS right — all three, and make him say them back: believes a macro leg down is starting
  (name the *driver*: 10Y 5,307 %, Brent $101,63, Hormuz tanker attacks), has a written re-entry level,
  accepts the coin flip.
- And the data against: minutes are 3 weeks stale, P(BTC < $82k) 15,3 % from the Polymarket ladder, funding
  already negative (froth partly out), ETF flow back to +$118,8 M. Pair with `prediction-market-odds` so the
  user sees the market's own ~50:50 before deciding.
- Behavioural close: execute **now, in tranches**, never one "sell all" click at the release minute; name the
  trigger that would change the recommendation (2 daily closes below $0,46 etc.).

## 5. Pitfall

Do not answer a binary with a third framework that dodges the question ("sebagian aja"). Name the option you
recommend, then show the two neighbours it beat and by how many dollars. The user asked for a decision; the
matrix is the evidence for it, not a substitute for it.
