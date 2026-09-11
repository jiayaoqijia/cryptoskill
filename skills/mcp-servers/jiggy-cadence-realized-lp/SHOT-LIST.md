# SHOT LIST — REALIZED demo video
### Companion to `TALKING-POINTS.md` (riff sheet + do-not-say list). This is the sequence.

**Target 3:00. Seven shots.** Everything below is live and verified 2026-09-11 14:05 UTC.
If a number on screen differs from this file, **the screen is right** — it recomputes every build.

---

## Before you hit record

- Two browser tabs open: `realized.drainfun.xyz` and `realized.drainfun.xyz/deck`
- One terminal, font size up (judges watch on laptops), `cd` into the repo
- Close notifications. Airplane-mode the phone.
- Have a wallet address in the clipboard for Shot 5
- Do one silent dry run of Shot 5 — it's the only shot with live typing

---

> **ORDERING NOTE (2026-09-11, after adversarial review).** Three independent judge-sims
> converged on one criticism despite scoring us 4/10, 4/10 and "podium contender": *the first
> 60–90 seconds must scream AGENT UTILITY, not dashboard.* Two of them dismissed the project
> as "a human-facing dashboard with an MCP server bolted on for track fit." The track is **AI
> Tooling** — so an agent calling the tools has to come FIRST, before any human clicking a UI.
> That is the single highest-leverage change available without writing new code.

## SHOT 1 — An agent answers the question · 0:00–0:30
**Screen:** terminal or MCP client. **Not** the website.

Open with a machine doing the work, because that is what this track scores.

Ask it, out loud and on screen:

> *"I entered the USDC/WETH 0.05% pool on July 28th at a ±2x range. What did I actually make,
> and what would it cost me to close?"*

Let the tool calls land on camera — `find_pool` → `position_realized` → `simulate_exit`.

> "Seven MCP tools, live against The Graph. No API key — the server proxies its own. The agent
> gets **-$658 net on a $25,000 stake, after $0.28 of gas**, and a reason for every number."

**Why this is shot 1:** a judge watching 50 submissions decides in the first thirty seconds
whether this is AI tooling or a dashboard. Show the tooling.

## SHOT 2 — The defect, in one number · 0:30–0:55
**Screen:** landing page, top.

*Now* bring the human view up, as proof the same engine serves both.

> "This is USDC/WETH — the most-used pool in DeFi. It advertised **+0.65% APR**.
> An LP who put in $100,000 walked out with **$97,027**."

*Beat.*

> "The dashboard wasn't lying about the fees. It just has no term for price."

**Why this pool:** chosen by rule — highest-TVL pool currently misleading — not hand-picked.
Say that out loud; it pre-empts the cherry-pick objection before a judge forms it.

---

## SHOT 2 — Why it can't show a loss · 0:25–0:50
**Screen:** `/deck`, "The cause" slide.

> "Advertised APR is fees ÷ liquidity, annualized. Fees are always ≥ 0. So the number is
> **positive by construction** — structurally incapable of reporting that you lost money."

Then credit the prior work. This buys more than it costs:

> "Not our discovery that LPs can lose — Topaze Blue showed that in 2021. What we did is
> calibrate the advertised metric itself, pool by pool, against what actually happened."

---

## SHOT 3 — Not a cherry-pick · 0:50–1:15
**Screen:** `/deck`, the range-width table.

> "Same pools, same window. Only the assumed range changes."

Point down the column: **59.1% → 45.4% → 36.0% → 25.6%**

> "**110 of 110 windows** show the defect at tight and moderate ranges. The direction never
> flips. Full-range is the most generous possible case for the pool — and it's still there."

---

## SHOT 4 — Built on · 1:15–1:45
**Screen:** `/deck`, "Built on" slide. **This is the sponsor shot. Land all three.**

**The Graph — the dataset**
> "Per-day `feesUSD` are indexer-derived aggregates that exist nowhere on-chain. You can't ask
> a node what an LP earned last Tuesday. Without the decentralized network this isn't harder,
> it's **impossible**."

**Uniswap v3 — what we measure**
> "Every number is a Uniswap entity. `poolDayData` for history, the Position NFT for real tick
> bounds. And concentrated liquidity is *why* the defect exists — range width drives
> impermanent loss."

**1inch — the second opinion**
> "An instrument that grades others has to be graded too. 1inch has never seen our subgraph.
> **99.2% agreement, median divergence 0.078%.**"

---

## SHOT 5 — The live demo · 1:45–2:20 · **THE MONEY SHOT**
**Screen:** landing page, "Your position" → then paste an address.

Paste it, then say the line that no competitor can say casually:

> "**Read-only. No signing, no wallet connection, no permissions.**
> It reads your real tick range off the Position NFT — not an assumed ±2×."

**Linger here.** Where fees were earned but never collected, the page says
**"earned, never collected — not measurable."** Never `$0`.

> "Of 150 positions reading zero collected fees, **71 had real accrued fees**. Showing $0 would
> be wrong 47% of the time. A zero there is a number whose label lies — which is exactly the
> defect this project exists to expose, pointed at the user's own money."

Then `simulate_exit`:

> "And if you're deciding whether to close: **-$658 net on a $25,000 stake, after $0.28 gas.**
> Closing a v3 position isn't a swap — you get both tokens back — so slippage is a **measured
> zero**, not a missing field."

---

## SHOT 6 — What we refused to ship · 2:20–2:45
**Screen:** `/deck`, walk-forward failure table.

**Lead with the failure. Do not apologize for it.** Both outside reviewers independently said
this is the strongest thing we have for a technical track.

> "We tried to predict which pools will pay. One split showed a **+1.64pt edge** — the
> flashiest thing we had. So we tried to break it: same scorer, deliberately not retuned,
> walked forward across real time."

> "**Five runs. Five failures.** The bar was set *before* the runs. Then we went further — built
> a noise decoy, just a hash of the pool address. The decoy scored **62.1%**. Our real signal
> scored **61.8%**. The decoy won, so we deleted the claim."

The line that lands:

> **"REALIZED ships a track record, never a forecast. The interesting result was the one we
> threw away."**

---

## SHOT 7 — Agent surface + close · 2:45–3:00
**Screen:** terminal, one live MCP call.

> "CORS-open JSON, no API key — we proxy our own. MCP server, 7 tools. OpenAPI 3.1 spec.
> And a **test vector ships in the response** — implement the formula, run it, check you match.
> An agent shouldn't have to take our word for it."

Close on the deck's final slide:

> **"The advertised number can't show a loss. So we shipped the one that can."**

---

# If you have to cut

Cut in this order — **never cut 5 or 6.**
1. Shot 3 (cherry-pick table) — the deck carries it
2. Shot 2 (the cause) — Shot 1 implies it
3. Trim Shot 4 to The Graph + 1inch only

Shots 5 and 6 are the two nobody else in the track will have.

---

# Do NOT say

- ❌ **"LPs lose to HODL."** We explicitly don't claim it. Fastest way to lose a technical judge.
- ❌ **"We predict the best pools."** We tested it and killed it. Saying it undoes Shot 6.
- ❌ Any **annualized** number for a short window. A 30-day −81% loss annualizes to −988%, which
  cannot happen. (Real bug, caught and fixed 2026-09-11.)
- ❌ **DefiLlama is not a sponsor.** It's a measurement target. Fine as a finding, not a logo.
- ⚠️ If asked about **fee uplift for concentrated ranges**: we don't model it, so tight-range
  losses shown are **lower bounds**. Saying this unprompted builds credibility.

Full Q&A prep — including "what's the weakest part?" — is in `TALKING-POINTS.md`.
