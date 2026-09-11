# REALIZED — demo video script (2:00 target, 2:20 hard ceiling)

**ETHOnline 2026 · The Graph — Best AI Tooling or AI Use Case (net-new pool)**
Requirement: 2–4 min. We aim ~2:00 — judges watch ~40 of these. Short and dense beats long.

> **Every number below was pulled live from the running site/API on 2026-09-10 18:32 UTC.**
> They drift as the window slides. **Re-run `node scripts/demo-refresh.js` right before you
> record** and use whatever it prints. Do not read these off the page from memory.

---

## Before you hit record (5 min of setup, saves 30 min of retakes)

1. `node scripts/demo-refresh.js` — prints the current on-screen numbers. Keep it open.
2. Browser at **https://realized.drainfun.xyz**, hard-refresh, zoom **110%**, dark mode.
3. Second tab: **https://realized.drainfun.xyz/llms.txt**
4. Terminal: big font (18pt+), dark, `cd` into the repo, screen cleared.
5. Close Telegram/Discord/mail. No notification banners in frame.
6. Record 1080p. **Do a 10-second test clip and actually watch it back** — check the audio
   isn't clipping and the terminal text is legible when scaled down.

---

## THE SCRIPT

### [0:00–0:15] COLD OPEN — the defect, on screen, no preamble

**ON SCREEN:** the live shock card, full width. Do not scroll yet.

> "This is the biggest pool on Uniswap v3. USDC/WETH, four hundred million dollars in it.
> The interface advertises **plus zero point six five percent APR**.
>
> Anyone who put a hundred grand in thirty days ago is **down about three thousand dollars**."

*(beat — let the red number sit)*

> "Both of those are true at the same time. That's not a bug in the dashboard. It's arithmetic."

**WHY THIS OPENS:** No "hi, we built." The contradiction is the hook, and it's on screen in
under ten seconds.

---

### [0:15–0:35] THE CAUSE — why every DEX has this

**ON SCREEN:** slowly scroll so the green/red fee-vs-IL bar fills the frame.

> "Advertised APR is fee income, annualised. That's it. There's **no price term in it**.
>
> So it is **positive by construction** — a pool literally cannot advertise a loss, no matter
> what happened to the people inside it.
>
> The fees here were real: **plus three hundred and twenty nine dollars**. But impermanent loss
> was **minus three thousand three hundred**. Fees were never the whole story, and the number
> everyone shops on only shows you the fees."

**DELIVERY:** "positive by construction" is the thesis. Slow down on it.

---

### [0:35–0:55] IT'S SYSTEMIC — not one cherry-picked pool

**ON SCREEN:** scroll to leaderboards / honesty tables. Keep moving, don't dwell.

> "It's not one pool. Across the live corpus, **thirty-three percent** of pools are advertising
> a profit right now while LPs went backwards.
>
> We measured it across **five venues on four chains**, in rolling thirty-day windows over seven
> months, and every window carries its own canary — stable-pair positions have to show
> approximately zero impermanent loss, or we treat the instrument as broken and refuse to
> publish the number."

**WHY:** pre-empts "you cherry-picked" and "it's just a dashboard" in one breath.

---

### [0:55–1:15] YOUR position — the interactive beat

**ON SCREEN:** click **"Check your own position ↓"**, type `WETH/USDC`, pick it, set entry
date **2026-07-28**, land on the verdict card.

> "And you can ask it about your own position. Pool, entry date, range width.
>
> Forty-five days in USDC/WETH: fees **plus zero point four eight percent**, impermanent loss
> **minus two point six**, realized **minus seventeen point two percent annualised** — and it
> tells you it stayed in range the whole time, so this isn't a liquidation story. That's just
> what LPing that pair actually paid."

**IF THE LIVE CALL IS SLOW:** keep talking over it — the spinner says "Fetching live from
The Graph", which is the point. Don't cut to a cached screenshot; a judge can tell.

---

### [1:15–1:45] THE GRAPH + THE AGENT SURFACE — the track requirement

**ON SCREEN:** cut to terminal. Run the MCP call (command below). Let real JSON scroll.

> "All of this comes from The Graph, and it has to. Per-day fee totals in USD are **derived
> aggregates the indexer produces** — they don't exist on-chain. There's no RPC path to this
> dataset. Take The Graph out and there is no product.
>
> So we shipped it as infrastructure, not a website. An **MCP server** with six tools, a public
> **HTTP API**, and an **npm package**."

**ON SCREEN:** the `rank_pools` output.

> "The important one is `rank_pools`. Sorting by advertised APR puts **UNI/USDC** on top —
> thirty point eight percent advertised, **minus ninety percent realized**. Sorting by what LPs
> *actually took home* puts **wTAO/WETH** on top, at **plus thirty-eight percent**.
>
> Because the point isn't that yield is fake. It's that **the industry ranks on the wrong
> number.** This is the call a dashboard should make instead."

**WHY THIS IS THE CLOSER:** it's a correction, not just a diagnosis — and it ends on a pool
that genuinely made money, which is far more credible than "everything is a lie."

---

### [1:45–2:00] HONESTY + CLOSE

**ON SCREEN:** briefly the "what we do NOT claim" README section or the honesty box, then the
hero again.

> "What we don't claim: that LPs always lose to holding. Sometimes they don't. Fee uplift for
> tight ranges isn't modelled yet, so those figures are **lower bounds** — we say so on the page.
>
> The narrow claim is the strong one: **the metric the whole industry advertises is
> systematically uninformative about what you actually made** — and now there's a live
> measurement, an API, and an MCP server so agents and dashboards can stop repeating it.
>
> Realized. Open source, MIT, running on The Graph."

---

## EXACT COMMANDS TO RUN ON CAMERA

**Terminal beat 1 — the personal question (fast, always works):**

```bash
curl -s "https://realized.drainfun.xyz/api/position/0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640?entry=2026-07-28&range=2" | jq '{pair, daysHeld, feeReturnPct, impermanentLossPct, realizedAprPct, outOfRange, verdict}'
```

**Terminal beat 2 — the agent/MCP beat (the money shot):**

```bash
export GRAPH_API_KEY=$(jq -r .api_key ~/.config/cadence-secure/thegraph.json)

printf '%s\n%s\n' \
 '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"demo","version":"1"}}}' \
 '{"jsonrpc":"2.0","id":2,"method":"tools/call","params":{"name":"rank_pools","arguments":{"limit":150,"top":5}}}' \
 | node bin/mcp-server.js | tail -1 | jq -r '.content[0].text' | jq '{counts, soWhat, ranking: .ranking[:5], worst: .worstOffenders[:3]}'
```

⏱ **takes ~60–90s to return.** Either pre-run it and have the output on screen, or start it,
keep narrating, and cut the dead air in the edit. **Do not sit in silence waiting.**

**Optional third beat — the npm/library angle (only if under time):**

```bash
node -e "import('@realized-lp/core').then(m=>console.log('IL at 2x, full-range:', m.impermanentLossPct(2).toFixed(2)+'%', '| ranged ±2x:', m.concentratedIlPct(2,2).toFixed(2)+'%'))"
```

---

## LIVE NUMBERS AS OF 2026-09-10 18:32 UTC (re-verify before recording)

| beat | number | source |
|---|---|---|
| shock card advertised | **+0.65% APR** | hero, USDC/WETH 0.05% |
| shock card loss | **−$2,973 per $100k** | hero |
| fees vs IL | **+$329** vs **−$3,302** | hero |
| net | **−2.97% / 30d** (−36.2% annualised) | hero |
| corpus | **33%** of live pools misleading | corpus.json |
| your position | fees **+0.48%**, IL **−2.60%**, realized **−17.2%** ann., in range | /api/position, entry 2026-07-28 |
| rank_pools counts | 26 honest / 12 gap-prone / 34 misleading (of 72) | MCP rank_pools |
| naive top | **UNI/USDC** +30.77% adv → **−90.4%** realized | rank_pools soWhat |
| honest top | **wTAO/WETH** **+37.78%** realized | rank_pools ranking |
| worst gap | **HEX/WETH** +0.31% adv → **−150.5%** realized | rank_pools worstOffenders |

---

## THINGS THAT WILL COST US POINTS — avoid

- ❌ Saying "LPs always lose money." We explicitly don't claim it, and a judge who knows DeFi
  will switch off. The claim is about **the metric**, not about LPing.
- ❌ Quoting a tight-range loss as exact. Fee uplift is unmodelled → **lower bound**. Say so.
- ❌ Mixing timeframes. Window return and annualised are different numbers; label which one.
- ❌ Dead air waiting on the MCP call. Narrate over it or pre-run it.
- ❌ Reading numbers from this file without re-running the refresh script. They drift daily.
- ❌ Going past 4:00. Hard disqualifier risk.

## SUBMISSION CHECKLIST

- [ ] Video 2:00–4:00, 1080p, audio checked on playback
- [ ] Repo public: github.com/jiggy-cadence/realized
- [ ] README TL;DR + "what we do NOT claim" visible without scrolling far
- [ ] Live site up: realized.drainfun.xyz (+ `/llms.txt`, `/api/pools`)
- [ ] Track: **The Graph — Best AI Tooling or AI Use Case, NET-NEW pool**
- [ ] Say "The Graph" out loud in the video (sponsors check)
- [ ] Deadline **Sun Sep 13 2026, 12:00pm EDT**
