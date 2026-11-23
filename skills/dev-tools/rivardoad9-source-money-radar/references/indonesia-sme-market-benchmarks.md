# Indonesia SME / automation market — verified prices & competition

All figures looked up live during the 8 Oct 2026 session. Re-verify before quoting; prices move.

## Service pricing (what the market already pays)

| service | price | source shape |
|---|---|---|
| Jasa pembukuan UMKM — mikro (omzet < Rp100jt) | **Rp500.000 – 1.000.000 / bulan** | consultant blog (magnificat.id, 2026) |
| Jasa pembukuan — kecil (Rp100–500jt omzet) | Rp1.000.000 – 2.000.000 / bulan | same |
| Jasa pembukuan — menengah | Rp2.000.000 – 3.000.000+ / bulan | same |
| Paket Starter "AI Agent basic untuk UMKM" (1 nomor WA, live chat, workflow n8n dasar, 1 sesi training) | **Rp5.000.000 setup + Rp380.000 / bulan** | vendor product page (backlinktier) |
| Jasa workflow n8n — sederhana (2–4 node, 1 integrasi) | mulai Rp300.000 / workflow | vendor FAQ (yajada) |
| Jasa workflow n8n — kompleks / terintegrasi | Rp3.000.000 – 10.000.000 | same |
| Agency n8n tiered (basic / professional / enterprise) | Rp5–8jt / Rp15–25jt / Rp50jt+ | vendor pricing table (mixist) |
| Floor / race-to-bottom freelance | dari **Rp60.000** | marketplace listing (fastwork) |

**Positioning conclusion to reuse:** agencies chase corporate & mid-market (Rp15–50jt scope) while micro-SMEs are served by Rp60rb freelancers. The gap is **micro pricing with system quality** — that is where a student with an AI stack can enter. Entry price for the first 1–2 clients: low (Rp250rb) to buy proof, then Rp750rb setup + Rp250rb/month.

Delivery-time benchmarks vendors themselves publish: simple workflow 2–4 hours, medium 1–3 days, complex 1–2 weeks. Use this to justify the setup fee.

## Jasa pembukuan (retainer) — what buyers actually ask for, and the package anchors

Re-verified 16 Oct 2026. Two sources, deliberately different:
**Demand side — accounting-staff job descriptions** (Jobstreet / Glints / LinkedIn / Kalibrr). The recurring core is
narrower than the deliverable list vendors advertise: **bank reconciliation** and **AR / piutang + aging** appear in
almost every posting, then daily transaction recording, jurnal + buku besar, monthly statements, tax-period recaps
(e-faktur, ID billing, bukti potong, PPh 21/23, PPN in/out), and archiving of evidence. Secondary: kartu stok /
persediaan, petty cash, per-branch reports, cashflow projection, budgeting.
**Supply side — active vendor package pages:**

| item | price | source shape |
|---|---|---|
| Jasa Pembukuan Bulanan | **Rp2.700.000 / bulan** | vendor page (pajakumkm.id) |
| Jasa Perpajakan Bulanan (hitung + lapor masa, ID billing, bukti potong, faktur pajak) | **Rp2.280.000 / bulan** | same |
| Tier dengan konsultasi strategis finance | Rp2.000.000 dan Rp6.000.000 / bulan | vendor page (pakarbisnis.co.id) |
| "Laporan bulanan lengkap + analisis transaksi" | Rp4–6jt / bulan (benchmark figure in the vendor's own article) | Mekari Jurnal blog |
| Marketplace floor for the same words (pembukuan / data entry) | Rp60–77rb (Fastwork), Rp99rb (Sribu) | marketplace listings |

**Conventions the market already assumes** (mirror them, don't invent): reports land **tanggal 5–10 bulan
berikutnya** (one vendor states "laporan selesai tanggal 10 bulan berikutnya"); delivery in **Excel + PDF** (Excel
because the tax office may ask to unpack it); a chat/consult channel is part of the retainer; tax-period work is
priced as a separate package.

**Sellable framing that follows:** "rapiin laporan" sits in the Rp60rb pool; **"laporan siap pajak & siap kredit
bank"** holds at 5–10×. The mess a micro client actually has, in their own words: uang di rekening nggak cocok
dengan catatan · siapa ngutang belum ketahuan · stok nggak balance · pajak nggak jelas · nota nggak diarsip. Lead
with those, not with the accounting process.

**Where the entry price goes:** mikro Rp500rb–1jt/bulan → Rp750rb/bulan standard, Rp1,5jt with the tax package,
Rp1,5–3jt once-off per backlogged month for catch-up work (the easiest thing to sub-contract from an accounting
firm). Delivery design, SOP, onboarding form, QC checklist: `bookkeeping-service-delivery.md`.

## WhatsApp gateway economics & the ban-risk trap

| option | cost | risk |
|---|---|---|
| **WhatsApp Cloud API (official, Meta)** — recommended | **first 1.000 service replies per business number per month FREE**, then Rp356,65 per service reply in Indonesia (effective 1 Oct 2026). Outbound Indonesia templates: utility $0,0250 · marketing $0,0411 per message | none — official |
| Wablas (unofficial) | Rp22.000/month (Nano); 15-day free trial, watermarked | client's number can be banned |
| Fonnte (unofficial) | free tier 1.000 msgs/month, then ~$13/month | Fonnte's own site states it takes no responsibility for bans and that **ban risk is the same on free and paid plans** |
| RuangWA (unofficial) | ~$3,04/month | same ban risk class |

**Rules that follow from this:**
- Use the official Cloud API for a client's production number: the first 1.000 inbound service replies/month are free, which covers nearly every micro-SME. Cost per client ≈ Rp0 → selling at Rp250rb/month is ~90% margin.
- **Never put a client's main number on an unofficial gateway** — if their number gets banned, that is the agent's fault and it kills the relationship. If a fast unofficial path is used at all, it must be with the client's explicit informed consent on a secondary number.
- The Cloud API number must be a dedicated number — it cannot simultaneously run in the normal WhatsApp app. Say this at the start of the sale, not on installation day.
- Recap delivery to the owner can be sent over Telegram instead of WhatsApp to keep message costs at Rp0, if the owner is fine with it.

## Where the buyers are (distribution reality)

The recurring finding on this account: a store/funnel with zero traffic is the bottleneck, not the product. Order of channels that actually work here: warm personal contacts who already run a business → campus/organization network → sellers the user has personally bought from → businesses near home/campus → cold DM last. The ask is always a free 30-minute audit, never a purchase.
