---
name: money-radar
description: "Use when asked what to sell or how to earn money."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [monetization, opportunity-validation, outreach, umkm, indonesia, cashflow, accountability, first-revenue]
    related_skills: [lynk-id, threads-marketing-automation, job-listing-hunter]
---

# Money Radar — opportunity validation & first-revenue engine

The user's standing directive: act as an economic weapon, not a chatbot producing ideas. Convert his time, skills, capital, network, and AI stack into **cash flow**. Optimize for `FIND → VALIDATE → BUILD → SELL → OPTIMIZE → SCALE`, never for feeling productive.

## Trigger

- "menurut lu gw jual apa", "cara cari duit", "peluang apa yang bagus", "what should I sell"
- User pastes a "money-making strategic agent" / accountability-partner directive
- A recurring MONEY RADAR request (report or scheduled run)
- **User starts building a product, framework, dashboard, or feature with no paying customer** — intervene here, this is the highest-value moment for this skill

## Iron rules (apply in this order)

1. **Verify before advising.** Never accept a claim about revenue, readiness, or audience. Find the evidence on disk (see Step 1). A store with 0 sales is not a product problem.
2. **Score before recommending.** Use the 11-criteria sheet in Step 2, computed with a script, never mentally.
3. **Sell before build.** Nothing new gets built until one person says yes. If a demo is needed to close, build the demo, not the product.
4. **Every answer ends with ONE action doable today plus the metric to report back** — count of *outreach messages sent*, never count of ideas.
5. **Name the trap out loud, once, warmly.** He will drift toward building/researching within the same session (asked "what do we do next" and then "let's build the framework tonight" minutes later). Say it plainly, then convert the urge: build the *demo* for him and take the build off his plate. Standing division of labor: **he sells and runs the audit calls; the agent builds the system.**

## Step 1 — revenue audit (evidence, not claims)

Find what already exists and is monetizable-but-unmonetized before proposing anything new:

```bash
# sales/webhook logs: separate REAL transactions from the user's own test payloads
grep -aiE "grandTotal|SALE|PAID|signature" ~/.hermes/lynk_webhook/sales.log | head
grep -av "\[http\]" ~/.hermes/lynk_webhook/sales.log | sort -u    # non-HTTP lines = real events only
systemctl --user is-active <service>; ls -la ~/.hermes/data/ | grep -iE "sale|order|lead|customer"
```

Report the finding as a sentence with numbers: *"Mesin jalan sempurna, pasar kosong — toko 3 produk, 7 minggu, 0 pembeli asli (semua entri di log ternyata payload tes sendiri)."* Then the conclusion: **the bottleneck is distribution, not technology.** Cite market-ready assets (store, webhook, alerts, dashboards, scripts) and how many rupiah each has produced.

## Step 2 — opportunity score

Score 1–10 on each, sum /110, present as /100: Demand · Willingness to Pay · Competition (low = high score) · Speed to First Revenue · Low Capital · Technical Fit · Scalability · Recurring Potential · Skill Fit · Distribution Advantage · Low Risk.

Then rank candidates against the hierarchy: existing customer with urgent problem → existing skill monetizable now → productized service → AI automation → digital product → SaaS → content/distribution → speculative investment → pure speculation.

Always sanity-check the EV per hour of the winner and the unit economics (cost per client vs price). Say plainly when a path *cannot* reach the user's stated target (e.g. "Rp100jt needs ~27 clients/yr on this pricing — the service alone isn't that path unless it productizes").

## Step 3 — market benchmarks (verify live, never from memory)

Quote only prices looked up in the same session. Indonesian SME benchmarks, verified pricing, the bookkeeping-retainer market, and the WhatsApp gateway comparison: `references/indonesia-sme-market-benchmarks.md`.

When the ask is *"hasilnya di real market minta yang kayak gimana"*, derive the demand list from two live sources, never from theory: (a) **job descriptions for the in-house equivalent role** (Jobstreet/Glints/LinkedIn/Kalibrr) — they expose the recurring core of the work, which is narrower than the vendor deliverable list (accounting-staff postings keep naming bank reconciliation and AR/aging, not "monthly reports"); (b) **active vendor package pages** — they expose the deliverable bundle, the tier prices, and the delivery-date convention the buyer already expects. Then say explicitly which items the buyer asks for and which they need but never ask for.

Frame the quote honestly: *"agency ngejar korporat (Rp15–50jt), UMKM mikro cuma diladenin freelancer Rp60rb → celahnya harga mikro dengan kualitas sistem."*

## Step 3b — cross-country trend transfer ("ramai di luar, belum di sini")

When the ask is *"tren/barang/jasa yang ramai di US/Jepang/Korea tapi di Indonesia belum ramai"*, do not brainstorm a list. Run a transfer test, then score.

1. **Name the driver, not the product.** A trend moves only if its driver exists locally: household structure, pet ownership, ageing, women in the workforce, traffic, labour cost, tax/compliance deadline, climate. Cold plunge fails in a tropical market with no sauna culture; self-storage needs small urban flats, not just US success.
2. **Prove both sides with numbers.** Foreign side: market size + growth from a named report. Indonesian side: supply count, local asking price, and an adoption marker (national ad campaign, outlet count, marketplace listings). A market with 400k+ outlets of the adjacent category is already a price war, not a gap.
3. **Kill on the driver before scoring.** State the rejected trends and the mechanism in one line each; this is what separates analysis from a listicle.
4. **Score with the Step 2 sheet, computed by script**, then group by capital: under Rp5jt / Rp10–100jt / Rp300jt+. The winner must be runnable at the user's current capital, not just attractive.
5. **Deliver top 3 + rejected list + a 30-day validation with a funnel metric** (visits → replies → pilots → paid). Same closing rule as Step 5: one action, one metric.

Data hygiene for this kind of report:

• Market-size firms disagree by definition — quote a range with the year ("US$2,5–3,1 miliar, 2025–2026"), never one precise-looking number.
• **Open the page for every figure you cite.** A growth rate often belongs to the neighbouring category (green-tea imports get quoted as matcha); read the report's own sentence, not the search snippet.
• Prices scraped from seller/operator pages are asking prices — label them as such.
• Dates and local specifics beat generic growth: a compliance deadline explains *why now* better than a CAGR.

Long report output: write the markdown to `~/obsidian-vault/`, render with `scripts/md_to_pdf.py`, and send the PDF in chat (numbers-first summary in the message, full detail in the file).

## Step 3c — candidate deep search (before committing to one pick)

When the shortlist narrows to one candidate, or the user says *"deep search X"*, the job changes from ranking to **killing or sharpening**. A broad pass overrates candidates because absence of evidence looks like absence of competitors.

1. **Search for named competitors before repeating the score.** `category + vertical + harga` in Indonesian, then English for the global ceiling. Open every pricing page — a snippet cannot tell a plan price from a setup fee or an example calculation.
2. **Count incumbents' adjacent features as competition.** An EMR that already bundles WhatsApp reminders is a competitor even without an AI agent.
3. **Revise the score in public.** If competitor density beats the assumption, lower the Competition criterion, restate the total, and open the report with a correction section. Silently keeping the old number destroys the report's credibility.
4. **Anchor price three ways:** replaced salary, value of one recovered high-ticket customer, and competitor price floor. Then compute scenarios in `execute_code`.
5. **End with 5 assumptions, pass thresholds, and a 90-day kill criterion**, not with a build plan.

Full procedure, competitor-matrix columns, regulated-vertical checklist, and report skeleton: `references/candidate-deep-search.md`.

## Step 3d — physical product (barang), not service

When the ask is a product to sell, or the user rejects a service/product pick as “kurang menarik”, run `references/physical-product-validation.md` before re-ranking.

The gate is **useful ≠ wanted**. A product bought out of obligation needs a concrete trigger (deadline, fine, mandatory rule); without one it loses to products that deliver identity, pleasure, or curiosity. If the user calls a pick boring, do not defend it — classify the demand, lower its score, and re-run the shortlist.

Before scoring, count the supply side too: marketplace listing count, incumbent sold counts, and the price ladder. A category with 1.000+ listings and an incumbent at 1rb+ sold is a brand/distribution fight, not a price gap; test custom/wholesale or consignment instead of head-on D2C.

When the user says the trend is cooling, separate **buzz** from **habit** (Step 2b in the reference): TikTok/Google Trends can peak while venue count, class occupancy, and repeat purchase still hold. Say which layer is falling before defending or rejecting the product.

Never order stock or pay an MOQ before a 14-day pre-order/consignment test (30–60 units, 3–5 venues). The test is demand, not production; failing it is a stop, not a reason to add designs.

Compute the per-unit numbers with `scripts/product_unit_econ.py` (price, COGS, fee %, ad %, shipping, returns, units, capital) instead of mental arithmetic; require ≥35% contribution.

A one-page mockup or three design images is the product equivalent of the demo: do not build the full SKU before the concept and price are accepted.

Before choosing D2C, audit 15–20 venues: requirement is not supply. If most require the item but few carry own-brand, the wedge is custom/wholesale, not another listing. Full venue-audit and sample/logo/deposit sequence: Steps 5b–5c in the reference. For the WhatsApp-ready venue list — verified phone sourcing, benchmark/prospect tiering, and the prospective-member script — use Steps 5b.1–5b.3.

## Step 4 — offer design

WHO + PROBLEM + SOLUTION + DELIVERABLE + PRICE + WHY BUY NOW. Entry pricing deliberately low for the first 1–2 clients — **buying proof and a testimonial, not margin** — then raise and never discount again. Demand a 50% deposit before any work; no deposit, no work.

**Sell the outcome the buyer would name, not the activity.** "Rapiin laporan" sits in the Rp60rb marketplace pool; "laporan siap pajak & siap kredit bank" holds at 5–10× that. Describe the mess the way the owner experiences it (uang di rekening nggak cocok dengan catatan · siapa ngutang belum ketahuan · stok nggak balance · pajak nggak jelas · nota nggak diarsip), not the accounting process behind it. Same rule for tools: reselling "AI" is a commodity — the scarce part is the domain read (which numbers matter, what a gap means, who signs).

**Do not sell technical vocabulary to SME buyers.** "AI agent" makes the price feel expensive and abstract; sell the outcome ("chat kejawab otomatis", "tiap jam 9 malam lu dapet angka penjualan hari ini di WA"). Say honestly which parts are plain automation vs AI when asked.

## Step 5 — distribution before build

- Warm list first: 18 of the first 20 messages go to people he already knows who *already have transactions* (not business ideas).
- The ask is a **free 30-minute audit**, not money. Nothing is bought, nothing is promised.
- Funnel math to hold him to: 20 messages → 6 replies → 4 audits → 1–2 clients. Scripts, follow-up, and the audit call structure: `templates/outreach-wa-id.md`.
- If 20 messages get 0 replies, the list is wrong (wrong people), not the product.

## Step 6 — the demo, not the product

Anti-scope list for v0: no real platform integration, no AI parsing, no dashboard/database/login, no PDF automation. Reason to state out loud: *every item there adds 3–10 hours and Rp0 while nobody is paying.*

Hard gate: **the demo may only be upgraded after a client pays a deposit.** Upgrading it before that is a sign of hiding from selling — call it out.

## Output format

MONEY RADAR: **3 opportunities · 3 threats · 3 actions.** Then `WHAT DO WE DO NEXT` = the single highest-EV move inside 24 hours. Threats must be concrete and quantified (e.g. "2 jam/hari × 30 = 60 jam/bulan untuk Rp0; 60 jam itu = 4 audit + 40 outreach ≈ 1–2 klien"). Three actions maximum, never twenty.

## Communication preferences (this user)

- Indonesian, santai-akrab, "lu/gw". No `-` bullets — use `•`.
- Never close with "mau gw buatkan?" — give the directive and the metric he must report back.
- He wants proof of action: do the work (research, scripts, files) and paste real output, not plans.
- When he asks for suppliers or vendors, send verified contacts plus a copy-paste first message and the exact quote fields to collect. A raw list without a script is homework, not help.
- He does not believe he can sell services yet. If he says “nggak pede jual jasa”, pivot to a product without pretending products are free of selling: listing, content, reviews, and ads still apply. Do not answer the confidence problem with another service plan.
- Correct **gently**: a direct rebuttal makes him feel defeated. Name the trap once, then hand him a version of what he wanted that also moves the money. Do not moralize twice.
- Own errors immediately and precisely — he values the correction more than the smooth answer.
- Trading/crypto is never the base income layer: barbell = BASE (service cash flow) + UPSIDE (productized/software) + OPTIONALITY (crypto), and crypto is optionality only unless there is a demonstrable edge.

## Pitfalls

- **Don't let "let's build a framework tonight" pass unchecked** — that's the recurring failure mode. Redirect to demo + outreach; do the building yourself.
- Don't propose expensive software, ads, hires, or courses to a student with limited capital. Free tier / existing server / existing network first. When he asks which tool or subscription to buy ("misal gw subscribe Claude deh"), answer plainly: **the tool is not the gap** — anyone can rent the same model — and no spend until a client pays; the client's money buys the tool.
- **Never sit in the client's legal seat:** the client signs and files their own tax returns, and the agent never holds their banking credentials. Write the liability boundary into the offer, not into a post-mortem.
- **Put the client's obligation in the contract, not in goodwill:** data received by date X → deliverable by date Y, and late data moves the deadline. Otherwise their delay becomes your fault.
- Don't confuse research, tool-shopping, or refactoring with progress. The sentence to use is literal: *"Lu sedang melakukan aktivitas, bukan progress."*
- Don't quote a market price or a competitor claim not verified in-session.
- **Don't call a market empty without a named-competitor scan.** "Belum ada pemain dominan" is true of almost every fragmented SME market and says nothing about whether vendors exist; search `<category> <vertical> harga` and open pricing pages before scoring or pitching.
- When he asks a *technical* question mid-campaign ("jadi AI agent implementation untuk UMKM ya"), answer it in a few lines **and** point out that the unanswered thing is the outreach — technical questions are how the drift starts.

## Files

- `references/indonesia-sme-market-benchmarks.md` — verified IDR pricing, service-competition map, WhatsApp gateway/Cloud API cost + ban-risk comparison.
- `templates/outreach-wa-id.md` — copy-paste outreach scripts (5 variants), follow-up, price-deflection phrasing, 30-minute audit question set.
- `templates/factory-outreach-wa-id.md` — first message, quote matrix, sample request, red flags, and follow-up for local manufacturers.
- `scripts/md_to_pdf.py` — markdown → A4 PDF via headless Chromium (tables, code, page margins); pass absolute paths, Chromium's `as_uri()` rejects relative ones.
- `references/candidate-deep-search.md` — deep-diving one shortlisted opportunity: competitor/price scan, score revision, unit economics, validation gates, regulated-vertical rules.
- `references/physical-product-validation.md` — want-vs-should demand test, marketplace saturation count, buzz-vs-habit trend check, 10-criteria product score, per-unit contribution and ceiling, local manufacturing, D2C vs custom/wholesale, 14-day pre-order gate.
- `scripts/product_unit_econ.py` — per-unit contribution, margin, break-even units, monthly profit and payback for a physical product; prints JSON.
- `references/bookkeeping-service-delivery.md` — the bookkeeping retainer end to end: package tiers + prices, the dated monthly SOP, onboarding questionnaire, pre-send QC checklist, out-of-scope list, capacity/revenue math.
- Live implementation of the first offer on this server: `~/rapel-usaha/` (`engine.py demo` = 20 auto-reply rules, free-form order parsing, ongkir/minimal checks, 21:00 daily recap to CSV; `README.md` has the 4 go-live questions and the "is this AI?" answer).
