# Physical product validation — want vs should

Use when the ask is a **barang** to sell (not a service), when the user rejects a “useful” product as boring, or when he asks for something “menarik buat pasar sekarang”. The failure mode this reference prevents: recommending a product because it is useful and fits his skills, while nobody actually wants to buy it.

## Iron rules

1. **Useful ≠ wanted.** A product bought out of guilt or obligation (“should”) needs an external trigger — a deadline, a fine, a mandatory rule, a visible mess — or it loses in a feed to products that deliver identity, pleasure, status, comfort, or curiosity (“want”). If the only reason to buy is “ini penting”, the product is a should-product.
2. **If the user calls a pick boring, do not defend it.** Reclassify the demand, lower its score, and re-run the shortlist. Defending a should-product with more features wastes the session.
3. **Sell before stock.** Pre-order or consignment first. No MOQ, no import, no printing before cash from strangers.
4. **Contribution margin, not gross margin.** Subtract marketplace fee, ad spend, shipping subsidy, packaging, and expected returns. Require ≥35% net contribution for a first product.
5. **Distribution must match his tolerance, not a label.** Separate the channel from the format: a scripted message-based B2B pitch (IG/WhatsApp/email to 10–30 named venues) is not the same as walk-in cold calls. If he refuses face-to-face selling, rule out walk-ins and daily prospecting, but do not automatically rule out wholesale/consignment; test whether a message channel is acceptable before rejecting a bigger market.
6. **One product, one niche, one 14-day test.** Bundles and line extensions come after the first repeat order.
7. **Mockup before full build.** The product equivalent of a demo is one page, three design images, or one sample. Do not produce the full SKU — every page, every size, packaging, video — before the concept and price get a yes. Build effort is not validation.

## Step 1 — classify the demand

| Type | What the buyer is buying | Evidence it can move |
|---|---|---|
| Want | identity, status, pleasure, comfort, curiosity, belonging | people post about it unprompted; repeat purchase; giftable; visual demo |
| Should | compliance, admin, fear of penalty, “seharusnya rapi” | a real deadline/fine; mandatory purchase; a service provider forcing it |

A should-product can still sell, but only when the trigger is concrete (tax deadline, inspection, mandatory studio rule). Without a trigger it needs a service wrapper or a much stronger brand — both are slower than picking a want-product.

## Step 2 — demand evidence (live, not from memory)

1. **Count the venues, not the TAM.** Association/regulator figures for studios, clubs, courts, clinics, outlets. Venue count is a better proxy for reachable buyers than a consulting TAM.
2. **Price scan the marketplaces.** Query `<product> harga`, `site:shopee.co.id <product>`, `site:tokopedia.com <product>`. Collect 5–10 seller prices and report the range/median. These are **asking prices**, not transaction prices; label them that way.

   **Count saturation, not just price.** When a marketplace page will not render directly, fetch the Tokopedia find page through the Jina reader and read its result count:

   ```bash
   curl -s "https://r.jina.ai/https://www.tokopedia.com/find/<slug>" \
     | grep -o 'Menampilkan [0-9.]* produk'
   ```

   Parse the first page for seller price and `terjual` (sold) counts. Read them as a competition signal: 1.000+ listings plus an incumbent at 1rb+ sold means D2C is a brand/distribution fight, not a price gap. Use the count to choose the channel — custom/wholesale, consignment, or reject — before scoring.
3. **List the incumbents and their price ladder.** Local brands plus imported brands. If the low end is already at your intended price, the opportunity is design/community, not price.
4. **Find the growth proxy.** Store openings, venue count growth, category growth from a named report, search/community chatter. Do not present one consultancy’s precise TAM as fact; use a range with a year.
5. **Check the boring constraints before scoring:** BPOM/halal (food, cosmetics, supplements), izin edar/SNI (medical devices, electronics, toys), batteries/warranty, perishability/cold chain, size/fit returns, shipping weight and damage.

## Step 2b — trend durability: separate buzz from habit

When the user says *“trennya sudah turun”*, do not answer yes/no. Split the signal into two layers:

| Layer | What to measure | If falling | If holding |
|---|---|---|---|
| Buzz | TikTok hashtag peaks, Google Trends, influencer volume | new-customer acquisition gets harder; content-led D2C loses | still a tailwind |
| Habit | venue count, class occupancy, membership retention, repeat purchase, incumbent sold counts | demand is really shrinking; cut stock | installed base still buys; mature market, not dead |

Rules:

• A content peak is not a demand collapse. A trend can be past its viral top while the installed base still attends and replaces gear.
• A venue-count peak is the real warning for derived products: socks, mats, and studio merch fall when studios close.
• Entering after the buzz peak means the fight is brand, channel, and retention, not novelty. Price the higher CAC into the model.
• If the user's read is directionally right, say so before defending the product; then show which layer still pays.

## Step 3 — score 10 criteria, total /100

Score each 1–10. Competition, capital, regulation, and shipping are scored **inversely** (easy/light = 10).

| Criterion | What a 10 means |
|---|---|
| Want factor | Buyer wants it before being told why |
| Demand growth | Venue/category growth is visible now |
| Competition | Fragmented, no dominant local brand at your price |
| Capital | First test fits under Rp10jt |
| Regulation | No permit, no halal/BPOM, no izin edar |
| Shipping | Light, unbreakable, no cold chain |
| Repeat | Consumable, wear-out, or collectible |
| Content | Demonstrable in 3 seconds; before/after or identity |
| Skill fit | Uses an existing skill or 30–60 days of learnable content |
| Margin | ≥35% contribution after all fees |

Cutoffs: **<60 reject**; **60–69 only with an existing distribution channel**; **70+ test**. A 72/100 product with no buyer is still zero; the score ranks candidates, it does not prove demand.

## Step 4 — unit economics

Compute per unit, in `execute_code`, never mentally:

```
price
− COGS (including packaging and label)
− marketplace fee (8–12%)
− ad spend (10–20% of revenue)
− shipping subsidy
− expected returns/write-off
= contribution (require ≥35%)
```

Then compute:
- **Bundle economics** (3-pack, starter kit) — raises AOV but lowers percentage margin; show both.
- **Wholesale/consignment economics** — sell-in price, venue margin, who carries returns.
- **Capital** = MOQ × COGS + samples + content/photo + first packaging. Keep the first test under Rp10jt; under Rp5jt is better.
- **Break-even units** = fixed test cost / contribution per unit.
- **Ceiling** = category units/year × a realistic share (1–5%). If 300 units/month is already 2% of the category, say plainly that this is a starter business, not the path to the user's target. A high margin on a tiny niche is still a tiny profit.

## Step 5 — manufacturing and channel

- **Local manufacturing first** for low MOQ, sampling speed, and size changes. Ask for: MOQ per design, sample lead time, size chart, material weight, grip/quality test, label and packaging options.
- **Import only if the margin survives** duty, MOQ, 4–8 week lead time, and defect rate. A 55% gross margin that becomes 25% after import and ads is not a product.
- **Custom/wholesale as the wedge when D2C is saturated.** Local factories often start at 24–50 units per design; sell logo'd product to venues at 50–60% of retail and let the venue keep the rest. It trades ad spend for a finite list of named buyers and repeat orders. Propose it only if the user accepts a scripted message channel; do not smuggle in daily cold calls.
- **D2C**: short-form content + marketplace listing; one hero demo, three use-case videos, UGC.
- **Consignment**: 5–10 units at studios/shops; the venue keeps 30–40%; unsold stock returns. This validates a physical channel without cold B2B selling.
- **B2B/wholesale** only when the user accepts the format it requires — walk-in visits or a scripted message channel. Do not build the plan around cold visits if he refuses them, and do not reject wholesale merely because it is B2B.

## Step 5b — venue audit: requirement is not supply

When demand is derived (studio socks, gym accessories, clinic supplies), audit the venues before choosing D2C. Sample 15–20 venues from ClassPass, Google Maps, and Instagram; record each as:

• **A** sells own-brand product
• **B** sells a third-party brand at the front desk
• **C** requires the item but tells members to bring their own
• **D** no requirement or no information

Read the class-preparation text (“grip socks required / available for purchase”) and recent venue posts, not the homepage. A common result: most venues require the item, few carry own-brand, and third-party or bring-your-own dominates. That is evidence for the custom/wholesale wedge, not proof that D2C demand is untapped.

Separate the end customer’s installed base too. If the item is mandatory, regulars already own one or two; repeat demand is replacement, a new colour, and the forgotten-kit emergency, not a first purchase. Message and price accordingly.

## Step 5b.1 — sourcing venue contacts (verified numbers, not guesses)

Goal: a list the user can WhatsApp today, split by what each visit proves.

1. Build the list from ClassPass city/category pages, Google Maps, and IG. ClassPass exposes the class-prep rule (“grip socks required / available for purchase”) and often a WhatsApp number in the contact block.
2. For a phone number, read the **Google Maps place panel**, not a search snippet: open `https://www.google.com/maps/search/<venue>+<area>` and read `document.body.innerText`. The number sits under the address and hours, works without login, and is the most reliable public source.
3. Cross-check every number before sending: search the exact quoted number plus the venue name. A truncated snippet can belong to a different business, and a 10-digit number missing its last digits is not a contact. If the number cannot be tied to the venue, give IG/website instead of a fake number.
4. Label it `WA/telepon`: a Maps landline may not have WhatsApp. Tell the user to try one message and fall back to IG DM.
5. Tier the list, 8–10 venues maximum for a 48-hour test:
   - **Benchmark** — already sells third-party or own-brand; tells you the price ladder and model.
   - **Prospect** — requires the item but tells members to bring their own; this is the wedge.
   - **Volume** — large review/member count even if the selling status is unknown.
6. Record per venue: requirement, sells?, brand, price, own logo?, responsiveness, tier. A list without these fields is not research.

## Step 5b.2 — admin outreach without impersonation

Ask as a **prospective member**, not as an existing member, a competitor, or a buyer with a purchase history. Do not invent an identity. If asked, “lagi cari studio dan bandingin kelas” is true and sufficient.

- One question per message. Admins answer short when hit with five at once.
- First message: grip socks mandatory? If I don’t own a pair, does the studio sell them, what brand, what price? Then follow up: when a member forgets, do they usually buy on site or bring their own?
- Do not ask the admin for aggregate member behaviour (“mayoritas punya sendiri?”). They do not have that data. Observe the front desk and the class instead.
- Do not pitch in the same thread as the research question. Wait a day or visit; a sudden pivot from prospective member to supplier burns the contact.
- Natural ask for own-brand: “Ada kaos kaki berlogo studio nggak? Saya suka ngumpulin merch studio.”

## Step 5b.3 — 48-hour venue sprint and decision rules

Day 1: WhatsApp 4 benchmark + 4 prospect venues; record replies. Day 2: visit the two closest venues, count what members wear, what the front desk sells and at what price, then fill the table.

Decision heuristic, not market proof:

- **≥5 of 8 sell third-party and ≤1 own-brand** → custom/wholesale wedge is open; proceed to blank samples and one mockup.
- **≥3 own-brand** → the shelf is taken; do not lead with custom. Test generic D2C or another category.
- **Most require but do not sell** → consignment first (5–10 units), not a 24-unit wholesale ask.

Report: replies/8, venues selling, price range, own-brand count. Five or six replies from eight messages is enough to decide; no replies means the list or channel is wrong, not that the product is dead.

## Step 5b.4 — holding the thread, and the living venue sheet

An admin answer often turns into a class-sales conversation ("mau ikut kelas yang mana?", "sudah pernah pilates?"). Answer in one line and put the product question back:

• "Masih nyocokin jadwal, belum bisa fix. Nanti aku kabarin ya. Btw grip socks yang dijual di sini biasanya merek apa kak?"
• "Belum pernah kak, mau coba beginner dulu. Kalau murid baru biasanya disaranin yang mana?"

Never name a date, never ask to be booked, never request the full class price list. A date gets logged and followed up, and the more he sounds like a lead the faster the shelf question disappears. "Nanti aku kabarin" is what every receptionist hears daily and raises nothing.

Close the thread with the decision-maker question, which is the actual asset: "Kalau soal merch atau produk retail biasanya yang handle siapa ya, kakak juga atau ada tim lain?" The admin knows the rule and the front-desk price, not who buys stock.

Deliverable is one living workbook, not a chat log. Sheets that earn their place:

1. per-venue row — requirement, sells?, brands, price min/max, own logo?, contact, status, notes
2. price benchmark per SKU with MIN/MEDIAN/MAX — the **median venue retail price** anchors the wholesale ask; a spread like 99k entry / 185–199k mid / 300k premium inside each studio is the ladder, not noise
3. supply quote and per-unit margin formulas — wholesale at 50–60% of retail must still clear COGS + shipping + the venue's own margin
4. market numbers with source and date, kept apart from venue data
5. the chat scripts themselves, so the next venue gets the tested wording

Publish it as an editable Google Sheet (see `google-workspace`, `references/drive-live-spreadsheet.md`) so replies get added from his phone, and write formulas over ranges with headroom. **Transcribe the same day a reply arrives** — a chat screenshot that never lands in a row is not research, and the brand/price detail is gone once the thread scrolls.

## Step 5c — sample, logo, and cash sequence

1. Order **blank** samples from three factories, not one. Test quality before spending on design.
2. Wash 10× as a fast screen; 30× for the final standard. Pass: grip loss under 20%, shrinkage under 5%, no colour bleed, seams intact, elastane recovers.
3. Make a venue-branded mockup only **after** the venue says yes. Never produce branded samples on spec; most mockups never become orders.
4. Collect a 50% deposit before production. At wholesale Rp70k and COGS Rp35k, a 50% deposit equals COGS, so the venue order funds its own batch.
5. Order per venue (24 units), not a generic 60-unit batch. A 60-unit batch belongs to a D2C pre-order with cash collected first.

Before choosing a factory, collect a quote matrix: price at 24/60/150 units, MOQ per design and per colour, material and elastane percentage, grip type, logo setup fee and file format, sample cost, lead time, payment terms, PIC, factory address, and account name (PT/CV, never a personal account).

## Step 6 — 14-day validation gate

Run one test, with numbers agreed before it starts:

- 30–60 units offered as pre-order at a discount (e.g. normal Rp129k, pre-order Rp99k).
- 3–5 venues asked to take 5–10 units on consignment.
- 3 short videos and one landing/order form; no paid ads beyond a small boost.

**Pass:** ≥40% of the pre-order target sold + ≥2 venues accept; reorder 2–3× the first batch.
**Fail:** stop. Do not print/import more, do not add designs, do not “fix” it with a new colorway.

Report back the metric the user can actually count: units sold, venues accepting, cost per acquisition, return rate.

## Step 7 — report shape

0 why the previous pick failed (demand type, not product quality) · 1 verdict + score · 2 market numbers (venue count, price range, growth proxy) · 3 top 3 + rejected list with the kill reason · 4 unit economics table · 5 14-day test with pass/fail · 6 sources.

Deliver markdown to `~/obsidian-vault/`, render with `scripts/md_to_pdf.py`, and put the numbers-first verdict in chat.

When the ask is explicitly **“supply and demand”**, use a different order: 1 demand layers (category growth, buzz, retention, willingness to pay, TAM) · 2 trend verdict (which layer is falling) · 3 supply (manufacturers, MOQ, wholesale benchmark, listing count, incumbents, price ladder, quality threshold) · 4 unit economics and ceiling · 5 channel choice (D2C vs custom/wholesale vs consignment) · 6 validation gate and kill criteria · 7 sources.

## Pitfalls

- **Selling “useful” as “wanted”.** A product that solves a real problem but has no visual, identity, or urgency hook will lose in a feed. Diagnose the demand type before defending the product.
- **Quoting marketplace “terjual” counts as market size.** Sold counts are cumulative and can be gamed; they are a competition signal, not a demand forecast.
- **Treating asking prices as transaction prices.** Marketplace prices are seller asks; discount and fee structures change the real clearing price.
- **Choosing a product whose only channel is face-to-face.** Match the channel to the user's tolerance before scoring; a bigger market he will not work is not an opportunity.
- **Ordering MOQ before a pre-order.** Inventory is the most common way a first product dies; the test is demand, not production.
- **Importing a trend without the local driver.** A sport or hobby grows only if the local venue count, climate, income, and culture support it. Count venues before believing a global CAGR.
- **Calling a niche “too small” without arithmetic.** Venue count × members × units/year × price is often a real business; do the multiplication before rejecting it.
- **Building the full product before the concept is accepted.** A finished template, book, or prototype feels like progress but spends the same hours as a small batch; show a one-page mockup or three images first and ask for a reaction, not applause.
- **Calling a trend dead because the content peak passed.** Social buzz and habitual demand move on different clocks; check venue count, occupancy, and repeat purchase before writing off the category.
- **Entering D2C in a category with 1.000+ listings and a dominant incumbent.** Listing count plus sold counts tells you whether the fight is price, brand, or distribution; pick the channel accordingly.
- **Confusing a market with a business.** TAM × realistic share is the ceiling; a 40% margin on 300 units/month is not a path to a large target.
- **Treating a mandatory product as an unserved market.** A venue requiring the item does not mean it will buy from you; audit whether it already sells own-brand or a third-party brand.
- **Designing venue logos before commitment.** Most spec mockups never become orders; keep one template and swap the logo only after a yes.
- **Producing a generic batch before a venue order.** Use a per-venue 24-unit order with a 50% deposit; reserve a larger batch for a D2C pre-order with cash already collected.
- **Assuming end users are first-time buyers.** When the item is mandatory, the installed base already owns it; sell replacement, new colour, or emergency stock rather than education.
- **Sending a phone number copied from a truncated snippet.** A missing digit can point to an unrelated business; verify the exact number against the venue before putting it in a chat template.
- **Pretending to be an existing member or a competitor to get information.** Ask as a prospective member instead; a later supplier pitch from the same fake identity destroys the contact.
- **Asking an admin for aggregate member data.** Front-desk staff know the rule and the price, not the share of members who own the item; observe the class for that.
