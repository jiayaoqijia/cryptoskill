---
name: market-field-research
description: Research a market via seller outreach or live trend and job data.
version: 1.0.0
author: Nous Research
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [market-research, outreach, pricing, vendor-diligence, whatsapp]
    category: research
    related_skills: [xlsx, product-price-monitor]
---

# Market Field Research

Get prices, brands, policies and buyer contacts that are not published
anywhere, by messaging the businesses as a prospective customer.

## When to Use

- The user is validating a product or service and needs to know what
  competitors actually charge, what they stock, and whether the thing is
  mandatory.
- Published data exists but is stale or aggregated; the real answer is in
  a WhatsApp or DM reply.
- The user is sourcing from factories and needs MOQ, price and spec.
- The market is too new for published size figures and you need defensible
  demand signals instead: search-interest series, share of job postings naming
  the skill, and the prices competitors publish.

## The Core Rule

The research chat has exactly two jobs: **collect data** and **identify
who decides**. Never sell in it. Pitching before you have a sample
converts the contact into a sales objection and closes the door for the
follow-up that matters.

## Procedure

1. **Pick 6–8 targets and log them before messaging.** Name, area, number,
   channel, status. A contact list that lives only in the conversation is
   lost at the next compaction.
2. **Open with a plausible reason for not knowing.** First class, first
   order, comparing two locations. Without that reason, four questions in
   a row read as a market survey and get answered with a flyer.
3. **Ask in this order:** is it mandatory, can I borrow it or must I buy
   here, which brand and what price, can you send a photo. Four asks max;
   each extra question lowers the reply rate.
4. **Probe the consequence, not the label.** "Wajib" and "disarankan" get
   used interchangeably by front-desk staff; "kalau nggak bawa boleh
   pinjam atau harus beli di tempat" produces the answer that actually
   matters.
5. **Stay in persona on logistics.** No dates, no booking, no price list
   for the core service. Deflect schedule questions vaguely and pivot back
   to the product question in the same message, so the answer still
   arrives.
6. **Vary the wording and stagger the batches.** Identical text sent to
   ten businesses the same day is recognisably a survey.
7. **Close by asking which team handles that product category.** Front
   desk is not the buyer; the name or account is the real deliverable of
   the first contact.
8. **Log each answer as data, not prose:** mandatory yes/no, sold on site,
   brand, price floor and ceiling, own label or third party, contact
   person. Anything unanswered goes in as `perlu konfirmasi`, never filled
   in by inference.

## Reading the Answers

- **Price floor with no brand** = generic volume player. Not a competitor;
  do not race it, and do not price against it.
- **Third-party brands at mid-high price** = the open gap is branded or
  private-label product at that same price point.
- **A seller that already carries its own label** = proof the model sells,
  a reference price, and a lead: ask who produces it.
- **Vendor MOQ** is the number that decides whether a first batch is
  possible at all. A quote showing one MOQ on the landing page and a much
  larger one in the body copy is unresolved until it is written down.
- **Spec questions from a vendor** (plain vs terry, knit weight) are the
  vendor asking you to decide — answer in terms of the end use, not the
  cheapest option.

## Supplier Inquiries (the buying half of the same chat)

- **List what the reply already answered before writing the next message:**
  unit price, MOQ, sample fee, tooling/screen cost, lead time, payment terms,
  branding options. Ask only the blanks. Re-asking something already answered
  proves you did not read the quote and makes every later question cheaper.
- **Never open with production intent.** "I want to start production" turns you
  into a buyer the rep chases for a deposit and removes your ability to walk.
  Open as "comparing a few factories for a first batch" and stay there until a
  written quote exists.
- **Never supply an MOQ the vendor did not state.** When a landing page shows
  one number and the body copy another, that is an unresolved number, not a
  number to pick.
- **Price the whole path to the first sellable unit,** not the unit price:
  sample fee + tooling/screen + shipping + packaging. A sample fee credited
  against the down payment later is still cash out now and is forfeited if the
  order is cancelled — treat it as sunk until the order exists.
- **Convert lead times to working days and add a buffer.** Long sample lead
  times usually mean small orders sit behind bulk ones. If speed matters, ask
  what a different specification does to the timeline (existing tooling instead
  of a new screen) rather than asking them to hurry.
- **Ask the consequence, not the label,** on the buying side too: not "is the
  price negotiable" but "what does the price become at 48 pairs in two designs".

## Market Size Numbers

- Category-size figures from different research houses often disagree several
  fold for the same category. Treat any single global figure as a direction of
  travel, never as the size of the user's opportunity.
- Size the opportunity from field data: how many sellers were contacted, how
  many stock the product, what the price floor and median are. That dataset is
  small, defensible, and actually about the user's market.
- Mark every figure as field data or estimate in the deliverable. When a new
  number contradicts one you gave earlier, say plainly that the earlier number
  was wrong and restate it — never swap it quietly, the user may already have
  planned around it.

## Screenshot Data

Chat screenshots are compressed and small. Read the full image, then
re-read a crop of the region when a price or brand is going to drive a
conclusion. If two reads disagree or the label is illegible, record
`perlu konfirmasi` and say plainly to the user what you can and cannot
confirm. Never quietly flip a headline finding on one low-confidence OCR
pass — the user is looking at the same image and will notice.

## Vendor Due Diligence Before Any Transfer

Written quote covering MOQ, unit price, spec and lead time; one paid
sample first; company NPWP and a company bank account rather than a
personal one; never 100% down payment. Public reputation (review count,
marketplace presence, export claims) is a filter, not a guarantee — small
review samples hide B2B complaints that get settled in DMs.

## Desk Data That Refreshes (trend + job signals)

When the market is too new for published figures, build the report on
signals that can be pulled again on a schedule, and ship the puller with
the report.

- **Google Trends via pytrends on modern Python breaks with `retries>0`**
  (`Retry(..., method_whitelist=...)` -> TypeError). Pass `retries=0` and
  handle 429 with your own 30–120 s backoff.
- **Never put more than five keywords in one payload** — Google answers 400.
- **Values are normalised to the highest point in that payload**, so they are
  only comparable *inside* one pull. Do not merge batches by rescaling on a
  shared keyword's mean: ratios drift and a term can end up double-counted.
  Put every term the chart compares into a single payload.
- **Check `max()==100` before interpreting.** Dropping the `isPartial` row can
  remove the peak and leave a series topping out at 57 — that is a broken
  scale, not a finding. Re-pull and confirm the ratio between two terms is
  stable across two pulls before writing any number down.
- **Say what the index is not:** relative interest, not search volume, and
  not revenue. Report growth rates (YoY) which survive rescaling, rather than
  absolute index points.
- **Free job feeds for demand share:** Arbeitnow (`/api/job-board-api?page=N`,
  ~300 rows/page), RemoteOK (`/api`, ~100 recent). Remotive and Himalayas
  silently cap results — fine for keyword share, useless for market totals.
- **Count share of postings, not postings.** "5.2% of 2,499 remote postings
  mention AI agent" is defensible; "there are N jobs" is not, because the
  feeds are a sample of global remote boards, not the local market.
- **Verify reproducibility:** run the refresh script twice; the percentages
  must match before the snapshot goes into the report.

## Choosing the niche (before the earnings model)

The ask "niche apa yang potential buat gw" is a comparison, not a request to confirm the obvious one.
Never anchor on the user's degree or current job — their background is one input, and they will say
so ("jangan cuma berdasarkan basic gw accounting"). Score at least four alternatives, two of them
outside their field.

1. **Check who already automates the core.** If SaaS and cheap service firms already sell the obvious
   version (AI OCR bookkeeping, chatbot platforms), the product layer is closed. The opening left is
   implementation and retainer work inside businesses that must adopt it, or a different niche. Name
   which layer is taken instead of pitching the taken one.
2. **Build the price ladder from live listings** — local gig floor, local monthly retainer, local
   salary per hour, global freelance rate. A service priced beside a Rp60k gig or a Rp399k/month SaaS
   cannot be defended by skill; it has to be sold as an outcome with a number on it.
3. **Score 1–5 on demand, competition, ticket, delivery ease, fit with the user's assets, moat,** and
   label the matrix as judgment, not measurement — put the evidence (listed price, open-job count, a
   named competitor) next to each high score.
4. **Multiply by probability, not optimism:** expected value = midpoint of the range × a stated chance
   of it happening. Sometimes the honest answer is that employment beats every service path; write
   that, and keep the service as the portfolio/upside play rather than forcing a business answer.
5. **Give kill criteria** (N conversations with no buyer, hours saved under X, refusal to pay above Y,
   months without a new retainer) so stopping reads as a decision, not a failure.
6. **When new evidence contradicts your earlier recommendation, open by saying so** and name what
   changed — the user may already have planned around the old answer.

## Potential Earnings (required section)

Every market report carries a section on what one person can actually bill.
The user asks for it if it is missing, so write it before delivery, and
build it from the package prices in the offer section — never from
industry averages.

- **Unit economics per client:** setup fee, monthly retainer, hours to
deliver, effective rupiah per hour, direct cost per month, gross margin.
  State the hours explicitly; they are the assumption everything else rests
  on.
- **Three or four 12-month scenarios** (conservative / realistic / aggressive,
  plus a year-2 row with a price step). For each: new clients, active
  retainers, revenue, and hours per week — so the reader sees that the ceiling
  is sales capacity, not delivery capacity.
- **Do the arithmetic to the user's stated goal** (e.g. Rp100 juta a year) and
  say which year it is realistic in. If it needs 2.5 new clients a month at
  today's price, say that instead of implying the goal is a straight line.
- **Compare the effective hourly rate to the global benchmark** for the same
  work (USD/hour × live FX) to show the headroom — then say plainly not to
  raise price before proof exists.
- **Close with the downside.** The first client does not exist yet; if the
  first N contacts produce zero buyers, every number in the table is zero, and
  that is information about the segment, not a mistake in the maths.
- Label package prices in the table caption as a hypothesis to test in the
  first ten conversations, not as a final price list.
- **One hours assumption per path, everywhere.** A narrative line that says
  "120–180 billable hours at $25 = Rp54–81 jt" must reproduce the same range
  its own scenario table shows; if the table says Rp45–70 jt, one of the two
  is using different utilisation. Recompute the narrative from the table's
  hours before shipping — two ranges for the same path read as a broken model,
  and the user will spot it.

## Deliverable

Keep everything in one living workbook so the research compounds: raw
sheet per source, benchmark with statistics, vendor comparison, market
context, action plan, and the scripts themselves. Build and sync it with
the `xlsx` skill, whose living-research-workbook reference file carries
the sheet blueprint and the stable-link Drive upload procedure
(`skill_view` that skill with `file_path` set to the reference name).

When the research is a standalone report rather than a workbook, ship a PDF
(the user reads it on the phone) plus the DOCX source and the data-refresh
script in the same folder — never only a chat summary.
