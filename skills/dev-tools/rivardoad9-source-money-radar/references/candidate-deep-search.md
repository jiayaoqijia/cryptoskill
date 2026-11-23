# Candidate deep search — one shortlisted opportunity, before commit

Use after a broad trend/candidate list narrows to one or two, or when the user says "deep search <candidate>". The goal is to kill or sharpen the pick with named competitors, real price anchors, and unit economics — not to re-rank the list.

## Iron rule

**"No dominant player" is not "empty market."** Before repeating a score, search for named competitors selling the same outcome to the same vertical. A candidate that looked open at 30,000 feet usually has 3–7 local vendors once you search the vertical plus "harga". If the scan finds them, lower the Competition score and say the score changed and why — never silently re-rank.

## Search passes (run in this order)

1. **Category + vertical + price, local language.** `chatbot klinik harga`, `AI resepsionis klinik`, `software klinik gigi harga`. Open the pricing page; snippets hide whether the number is a plan, a setup fee, or an example calculation.
2. **Category + vertical, English.** `AI receptionist dental pricing` — establishes the global price ceiling and feature baseline (usually $99–800/month per location).
3. **Incumbent adjacency.** `EMR klinik fitur WhatsApp`, `<clinic software> booking reminder`. The incumbent's bundled feature is your real competitor, even when it is not an AI product.
4. **Local supply and unit counts.** `jumlah <unit> Indonesia`, `jumlah klinik gigi`, `data <industry> 2025`. Use the regulator/association figure, not a blog roundup.
5. **Replaced-role cost.** Salary page for the person the product replaces (Jobstreet/Indeed). This is the buyer's mental price anchor.
6. **Platform pass-through cost.** Messaging/API rate card for the country (per-message price, free tier, VAT). Separate what the client pays the platform from what you charge.
7. **Value per transaction.** Average ticket and frequency in the vertical. A recovered customer worth Rp250k supports a very different fee than one worth Rp5jt.

## Competitor matrix (required in the report)

| Player | Focus | Price | Strength | Weakness to attack |

Rules: one row per real vendor found in-session, with the price as published (mark "tidak publik" when hidden); include incumbents whose adjacent feature overlaps; no invented vendors, no estimated prices dressed as list prices. Then write one paragraph: is the market crowded at the low end, the high end, or both, and where the remaining wedge is.

## Pricing the offer

- Anchor the fee against **the replaced salary** (receptionist/admin) and against **value recovered** (one saved high-ticket customer).
- Keep the fee at roughly 2–5% of the client's monthly revenue for a micro-business; above that, churn bites.
- Compute three scenarios (conservative/base/optimistic) in `execute_code`, not mentally: clients × price, fixed + variable cost, gross margin, ARR, CAC hours, payback months.
- State the price floor set by competitors and what happens if you match it (usually: 3–4× more clients for the same income — the trap to name out loud).

## Validation before build

Five assumptions, each with a test and a pass threshold, e.g.: buyer pays ≥ Rp750k → offer to 10 after pilot → ≥3 yes; demand exists → audit 20 prospects → ≥50% have the pain. Plus a 90-day kill criterion with numbers (audits, pilots, paid). If two assumptions fail, change segment or stop; do not add features.

## Regulated verticals (health, finance, education)

- Stay out of the regulated record: appointment/chat layer only, never the medical record or diagnosis. If the product stores clinical notes it becomes an EMR and inherits the whole compliance stack.
- Keep the guardrail in the product: no diagnosis, no promised outcomes, human takeover, audit log.
- Data: consent, minimization, retention limit, server in-country, processing agreement; quote the actual statute (UU PDP fines/breach window) only after opening the source.
- Name the compliance answer in the sales script, because the buyer will ask before signing.

## Report shape

0 correction of any earlier claim · 1 verdict + score change · 2 key numbers table · 3 TAM/SAM/SOM arithmetic · 4 the pain that gets paid · 5 competitor matrix · 6 remaining wedge · 7 MVP vs deliberately-not-built · 8 unit economics + scenarios · 9 GTM 90 days · 10 objections · 11 regulation · 12 risk table · 13 moat · 14 assumptions + kill criteria · 15 recommendation · 16 sources with URLs.

Deliver: markdown to `~/obsidian-vault/`, PDF via `scripts/md_to_pdf.py`, and a chat message that leads with the correction and the verdict, then 5–7 numbers, the wedge, the economics, and one concrete next action. Full detail stays in the file.
