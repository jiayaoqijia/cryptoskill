---
name: service-offer-page
description: Sellable offer page + outreach for UMKM services.
version: 0.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [marketing, landing-page, offers, umkm, income]
    related_skills: [offers, cro, copywriting, pricing, cold-email, prospecting]
---

# Offer page for a small-business service

Use when the user wants to sell a service to local businesses — bookkeeping, dashboards, admin
automation, web setup — and needs the thing that makes it sellable: packages, a page, and the
first message. The deliverable is a **single-file page + preview screenshots + outreach script**,
not a description of what the page could say.

Load `offers` (package design), `cro` (page structure), `pricing`, `prospecting` before writing copy.
They supply the frameworks; this skill supplies the order of work and the local rules.

## When to Use

- user wants to sell a service to local businesses and asks for a page, paket, harga, or "halaman penawaran"
- user has the service running but no way to present it to a prospective client
- the ask is "siap dikirim ke N calon klien" — page plus outreach copy, not one or the other
- not for: portfolio/CV pages, product landing pages that already have real customers, or copy-only
  requests where the offer itself is settled (`copywriting` alone is enough)

## Rules that override the marketing playbooks

- **No fabricated proof.** No invented testimonials, client logos, "500+ usaha", star ratings, or
  case-study numbers. If there are no clients yet, the proof section carries the user's *operating
  rules* instead ("every number must trace to a receipt; unexplained gaps are written as selisih,
  never rounded away"). That converts better than fake reviews and it is true.
- **Sample numbers must be labelled contoh.** A mock P&L inside a hero card is fine; a mock P&L
  presented as a client result is fraud. Label it in the card itself, not the footer.
- **Scarcity only from real capacity.** "3 usaha per bulan" is honest when one person does the work.
  Countdown timers and fake "slot tersisa 2" are out.
- **Only promise guarantees that can be honoured.** A 30-day money-back needs the user to actually
  refund; state the condition precisely ("kalau laporan pertama tidak bisa menjawab untung bulan ini").
- **Scope honesty in the FAQ.** Bookkeeping does not file taxes; say tax filing goes through a
  konsultan/DJP. Overpromising here is the fastest way to lose a client later.
- **Indonesian, casual-professional.** Match the user's own voice; ban "solusi revolusioner",
  "tingkatkan bisnis Anda", "di era digital".

## Market calibration (Indonesia, 2026)

Check these before fixing prices, or the offer lands below market without any advantage:

- Market range for UMKM bookkeeping is **Rp500rb–3jt/month**. Tiering usually follows omzet
  (under 100 jt → 500rb–1jt; 100–500 jt → 1–2jt; above 500 jt → 2–3jt) or transaction volume
  (under 50/month → ~850rb; 50–200 → ~1,5jt; 200–500 → ~2,8jt). A middle tier at 900rb is under
  market for 50–200 transactions; price it at 1,2jt.
- The F&B niche is **already occupied** (Katabix, Debit.id, FA Indonesia, situneo). "Bookkeeping for
  cafes" alone is not a differentiator. What none of them sell is **picking up the receipts** — they
  all run on upload-your-own-documents plus a dashboard.
- Differentiators that survive price competition: on-site pickup inside a 5 km radius, WhatsApp
  delivery instead of a login, menu-pricing decisions not just records, public pricing on the page,
  a refundable first month, and traceable numbers (every line points to a receipt).
- Do NOT sell on "cheap" (marketplace freelancers start at Rp60rb), "AI", or "fast".

## Delivery capacity (one person, still studying)

Price against the hours the tier actually consumes, not against how simple it sounds. Measured ranges for
a café-sized client:

| Tier | Setup (once) | Monthly | What it buys |
|---|---|---|---|
| Records only | ~2 h | 7–8 h | daily entry, weekly recap, one-page monthly PDF |
| Records + cost per menu | 4–6 h | 9–10 h | plus HPP per item, P&L, cash flow, dashboard refresh |
| Above + monthly session | 6 h | 14–16 h | plus price analysis, 3-month projection, 60-min review, bank-ready report |

Budget ceiling: **~30 h/month total**. Three mixed clients already land at 32–34 h, so the fourth client
only fits after a rate increase or automation — never by adding hours on top of class and internship.
That ceiling is also why the entry tier is a doorway, not the product: three entry-tier clients pay roughly
half of one mixed book for the same calendar time.

State these hours to the user when they ask how a package works, and split the answer into two views:
**operator** (what is done, how long, which tool) and **buyer** (what they send, what lands in their
WhatsApp, and which decision it lets them make). The buy-in comes from the second, the pricing from the first.

## Procedure

1. **Fix the offer before the page.** Three tiers, middle one featured and clearly the default. The
   middle must be the package the user actually wants to sell; the cheap tier exists to make it look
   reasonable, the top tier to anchor. Differentiate tiers by depth of analysis and access, not by
   withholding basics that make the cheap tier useless.
2. **Name the outcome in the headline**, not the activity: "Tahu persis untung kafe lu bulan ini,
   tanpa buka Excel" beats "Jasa Pembukuan Profesional". One primary CTA, one secondary.
3. **Write the objection section as FAQ, not features.** Data security (no PIN, no m-banking
   password), stop-anytime, "usaha saya masih kecil", existing cashier app, handwritten notes. Each
   answer admits a limit.
4. **Build one HTML file with inline CSS.** No CDN fonts, no framework, no build step — it has to
   open from a file:// path on the user's phone. System font stack for body, Georgia for headings,
   tabular-nums for every rupiah figure. Sticky mobile CTA bar at the bottom.
5. **Set the WhatsApp number in exactly one place.** `var WA_NUMBER = "62XXXXXXXXXX"` in the script
   block, and have every `[data-wa]` link rewritten from it; visible hrefs stay placeholders until
   the user supplies the real number.
6. **QA with real rendering, then look at it.** `browser_exec` → `new_tab("file:///…/index.html")`,
   capture at 1440×900 and 390×844 via
   `cdp("Emulation.setDeviceMetricsOverride", width=…, height=…, deviceScaleFactor=…, mobile=…)`,
   then `vision_analyze` each shot asking about clipped text, overlap and horizontal overflow. Do
   not declare a page done from reading the HTML.
7. **Deliver the outreach script too**: opening message, reply to "berapa biayanya", reply to "nanti
   saya tanya pasangan", one follow-up only, post-audit nudge, target profile, do-not-contact list.
   The page without the message is not sendable.
8. **Stop before publishing.** A public link with a placeholder phone number is worse than no link.
   Ask for the number, then deploy; list the pending items in the hand-off.

## Pitfalls

- **`capture_screenshot()` writes to the same temp path every call.** Copy the file into the project
  dir immediately after each capture, or the desktop and mobile previews end up identical.
- **Mobile header breaks first.** Hide the brand suffix on small screens, shrink the nav CTA to
  ~13px, and add `padding-bottom: calc(78px + env(safe-area-inset-bottom))` to `body` so the sticky
  bar never covers the last section.
- **Pricing in round rupiah.** Rp 500rb / 900rb / 1,5jt reads as a real quote to a small-business
  owner; Rp 899.000 reads like an e-commerce promo.
- **Vision OCR misreads Indonesian labels** ("pembukuan" → "pembukaan"). Verify a suspected typo with
  `search_files` in the source before editing copy.
- **Don't add a contact form.** WhatsApp is where this market converts; a form adds a backend and a
  reason to bail.

## Verification

- [ ] three tiers, middle featured, each with different depth not just a longer list
- [ ] zero invented proof; sample numbers labelled contoh
- [ ] page opens from file://, no external requests, screenshots checked at 1440 and 390
- [ ] WA number comes from one variable; pending deploy and number stated to the user
- [ ] outreach script exists and names the do-not-contact cases
