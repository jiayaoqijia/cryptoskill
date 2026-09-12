# TALKING POINTS — REALIZED
### For Jiggy's screen recording. Riff from these, don't read them.

All figures verified live 2026-09-11 01:40 UTC. If a number on screen disagrees with this
sheet, **the screen is right** — rebuild happened since. Re-check with `node scripts/demo-refresh.js`.

---

## The one sentence

> "Every DEX shows LPs an APR made only of fees. It has no price term — so it literally cannot
> display a loss. We built the number that can."

If you only get one line out, that's the one.

---

## Opening (~20s) — landing page hero

**On screen:** `realized.drainfun.xyz`, top of page.

- This is USDC/WETH — **the most-used pool in DeFi**, $415M TVL. Not a cherry-picked memecoin.
- It advertised **+0.65% APR**. An LP who put in $100,000 walked out with **$97,027**.
- That's **−2.97% over 30 days**. Fees earned +$329. Impermanent loss −$3,302.
- "The dashboard wasn't lying about the fees. It just has no term for price."

**Why this pool:** chosen by rule — highest-TVL pool currently misleading — not hand-picked.
Worth saying out loud; it pre-empts the cherry-pick objection.

---

## The defect (~25s) — slide 2

**On screen:** `/deck`, "The cause" slide.

- Advertised APR = fees ÷ liquidity, annualized. Fees are always ≥ 0.
- So the number is **positive by construction**. Structurally incapable of reporting a loss.
- What's missing is impermanent loss — the cost of the pool rebalancing you out of whatever went up.
- **Not our discovery that LPs can lose** — Topaze Blue / Bancor showed that in 2021. Our
  contribution is calibrating *the advertised metric itself*, pool by pool, against what happened.

Say that last part. It signals you know the literature and aren't overclaiming.

---

## It's not a cherry-pick (~20s) — slide 3

**On screen:** the range-width table.

- Same pools, same window, **only the assumed range changes**:
  - tight ±1.25× → 59.1% misleading
  - moderate ±2× → 45.4%
  - wide ±4× → 36.0%
  - full-range → 25.6%
- **110 of 110 windows show the defect** at tight and moderate. 108–109/110 at the widest.
- "The direction never flips. The tighter and more realistic your position, the more the
  advertised number lies to you."
- Full-range is **the most generous possible case for the pool** — and it's still there.

---

## Built on — the three integrations (~35s) — slide 4b, NEW

**On screen:** `/deck`, "Built on" slide. This is the sponsor slide. Land all three.

**The Graph — the dataset.**
- Per-day `feesUSD` are **indexer-derived aggregates that exist nowhere on-chain**.
- "You *could* reconstruct fee accrual from RPC — we checked, rather than asserting. What isn't
  tractable is the join: Q128 token-unit accumulators into per-day USD needs an archive node, a
  block lookup per day boundary, and a historical price for both tokens at each one, per pool."
- The claim is **practicality, not impossibility** — say it that way. An earlier draft said
  "impossible" and that was too strong; the README already carries the correction.
- **4 chains indexed: mainnet, arbitrum, polygon, base. 6 venue/chain pairs.**
  (Optimism is queried by `history-run.js` but never clears the canary, so it is NOT quotable —
  `data/history.json` has `optimism.tight: null`. Saying "5 chains" on camera inflates the claim
  with a chain whose numbers we refuse to publish.)

**Uniswap v3 — what we measure.**
- Every number is a Uniswap v3 entity. `poolDayData` for fee and price history.
- The **Position NFT** gives real `tickLower`/`tickUpper` — so pasting an address reads
  **the band you actually set**, not an assumed ±2×.

**Uniswap v4 — and why it's a different KIND of answer.** (say this one carefully, it's the
differentiator)
- Paste an address and we search **v3 and v4 together**. You don't pick a version.
- v4 has **no tick range on the Position entity at all** — only id/tokenId/owner/origin/timestamps.
  So v3 is *asking the chain what you have*; v4 is *replaying every event and deriving it*.
- We rebuild the range from `ModifyLiquidity` events. That gives the range and in/out-of-range —
  and it **cannot** support realized return or exit pricing, so **we refuse to compute them.**
  `/api/venues` publishes `realizedReturn:false` for v4 so an agent checks instead of assumes.
- **Do NOT call the math novel.** Summing signed deltas is bookkeeping. The real result is a
  reasoning one: *event-derived state is a strictly weaker evidence class than a state read, and
  you can detect exactly where it's weaker.*
- Three guards worth naming if asked: ~48% of v4 events are `amount:0` fee no-ops (counting them
  invents positions); removals with no matching add = transferred in, reported as
  `incompleteHistory` with size withheld; over 5000 events we return **nothing** rather than a
  truncated sum — found when 5 test wallets all "passed" while two reported 1471 phantom positions.
- **Aerodrome is pool-level only** — no per-owner Position entity, so no wallet lookup. Our own
  capability map claimed otherwise until we tested it.
- **Concentrated liquidity is *why* the defect exists** — range width drives impermanent loss.
  That's the connection worth making; it's not just "we used their data."

**1inch — the second opinion.**
- "An instrument that grades others has to be graded too."
- Spot Price Aggregator has **never seen our subgraph**. Independent check on every pool price.
- **99.2% agree, median divergence 0.078%** (255 pools compared).
- It audits *our price leg* — the half of realized return that doesn't come from fees.

---

## The demo — live wallet check (~30s)

**On screen:** landing page, scroll to "Your position."

1. Paste any address → **"Read-only. No signing, no wallet connection, no permissions."**
   Say that out loud. It's a real differentiator and it's on screen.
2. It reads your **real tick range** off the Position NFT.
3. Feed that range into the position check → realized return **at your actual band**.

**The money moment — do not skip this:**
- Where a position earned fees but never collected them, we show
  **"earned, never collected — not measurable."** Never `$0`.
- "A zero there would be a number whose label lies — which is the exact defect this whole
  project exists to expose, pointed at the user's own money."
- Measured: of 150 positions with `collectedFeesToken0 == 0`, **71 had non-zero fee growth.**
  They earned and never collected. Showing $0 would be wrong 47% of the time.

This is the most defensible thing in the project on camera. Linger here.

---

## What we refused to ship (~30s) — slide 5

**On screen:** the walk-forward failure table.

- "We tried to predict which pools will pay. It failed. So we killed it."
- One formation/holdout split said we had a **+1.64pt edge**. That would've been the flashiest
  thing in the submission.
- We tried to break it: same scorer, **deliberately not retuned**, walked forward across real time.
- **Five runs. Five failures.** Median edge never reached the pre-registered 0.5pt bar; p never
  got near 0.05.
- Bar was set **before** the runs. Cost model charged on every pick.
- "So REALIZED ships a **track record** — what already happened, measured — and **never a forecast**.
  The interesting result was the one we threw away."

Judges see a hundred projects claiming alpha. This is the slide that separates you.

---

## Why you can trust it (~20s) — slide 6

- **Stable-pair canary:** stable/stable pairs must show ~0 IL or the build **refuses to write
  output**. Worst |IL| = 0.0005%.
- **Three cutoffs, always:** every headline reported at 3 liveness cutoffs. If it flips across
  them we label it **a parameter, not a finding**.
- **Unmeasurable ≠ zero.** Missing price returns `measurable: false`, never a fabricated 0.
- The two pools that disagree with 1inch — USDC/UST, WBTC/PAX — are **dead tokens with stale
  subgraph prices**. "Finding them is the audit working."

---

## For the AI-tooling track (~15s)

- CORS-open JSON, **no API key required** — we proxy our own Graph key server-side.
- **MCP server**, 6 tools: `find_pool`, `realized_return`, `position_realized`, `audit_pools`,
  `rank_pools`, `explain_gap`.
- **OpenAPI 3.1 spec** at `/openapi.json` — agents never have to guess a request shape.
- **A test vector ships in the API response** — real inputs, real expected output. "Implement the
  formula, run it, check you match. An agent shouldn't have to take our word for it."
- npm: `@realized-lp/core`. The math is installable, not a repo you read.

---

## Close

> "The advertised number can't show a loss. So we shipped the one that can."

---

# THINGS TO AVOID SAYING

- ❌ **"LPs lose to HODL."** We explicitly do *not* claim that. Sometimes they do, often they
  don't. Overclaiming here is the easiest way to lose a technical judge.
- ❌ **"We predict the best pools."** We tested that and killed it. Saying it undoes slide 5.
- ❌ Don't quote **annualized** numbers for short windows. A 30-day −81% loss annualizes to
  −988%, which is impossible — an LP can't lose more than the stake. The site now shows window
  returns for exactly this reason. (This was a real bug, caught 2026-09-11 and fixed.)
- ❌ Don't call DefiLlama a sponsor. It's a measurement target — where people shop for LP yield,
  which we graded. Fine to mention as a finding, not as an integration.
- ⚠️ If asked about **fee uplift for concentrated ranges**: we don't model it. Tighter positions
  earn more fees than we credit, so tight-range losses shown are **lower bounds**. Direction is
  robust; magnitudes are bounded by that caveat. Saying this *unprompted* builds credibility.

---

# IF A JUDGE PUSHES

**"Isn't this just impermanent loss, which everyone knows?"**
> IL is well known. What's not measured is that the advertised metric is *systematically*
> uninformative about realized outcomes — pool by pool, across 4 chains, at every range width.
> We publish the calibration, not the concept.

**"Why The Graph and not an RPC node?"**
> Per-day fee aggregates don't exist on-chain. There's no RPC call for "what did this pool earn
> on August 3rd." It's indexer-derived. That's not a preference, it's the only path.

**"How do I know your numbers are right?"**
> Three ways. The stable-pair canary refuses to build if the instrument can't find a known
> signal. 1inch independently checks every price — 99.2% agreement. And a test vector ships in
> the API so you can verify our math yourself instead of trusting it.

**"What's the weakest part?"**
> Fee uplift for concentrated ranges is unmodeled, so tight-range magnitudes are lower bounds.
> And adjacent walk-forward windows share market regime, so they're not fully independent. Both
> are in the README.

Answering that last one straight is worth more than dodging it.

**"Can you show what an LP actually EARNED, not just what was claimed?"** — likely question, have this ready
> Partly, and we know exactly how far. Three routes, all checked live:
> - `collectedFees*` on the Position entity looks like earnings and isn't — it's a *withdrawal*
>   record, only populated when the LP calls `collect()`. 71 of 150 positions reading “0 collected”
>   had real accrued fees. That's why we refuse to print $0.
> - `collect` **events** would be ideal — timestamped, with USD amounts. They're in the schema but
>   **not populated** in this subgraph. Confirmed with a control: `mints` and `burns` returned rows
>   in the same query where `collects` returned zero.
> - **`positionSnapshot` deltas do work.** Snapshots are written when a position changes, so the
>   change in `collectedFees` between two snapshots is a real, timestamped earnings figure.
>   Measured on 1,000 live snapshots: 818 distinct positions, **135 of them (16.5%) have 2+
>   snapshots**. For those, we can show what was actually collected.
>
> So it's a **coverage problem, not a dead end**: real earnings for roughly 1 in 6 positions.
> We haven't shipped it because a number that works 16% of the time, presented as if it works
> always, is the exact defect this project exists to expose. Next step is shipping it **behind a
> coverage gate** — the real figure where snapshots exist, the honest refusal everywhere else.

That answer is strong *because* it ends in a limit. Don't round it up to “yes we can.”
