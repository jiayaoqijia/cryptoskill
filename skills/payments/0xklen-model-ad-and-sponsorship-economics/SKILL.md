---
name: model-ad-and-sponsorship-economics
description: Use when ad or sponsorship revenue must be valued. Computes CPM and CPC yields and a sponsorship's effective rate, then compares against the opportunity cost of the inventory.
---

# Model ad and sponsorship economics

Ad revenue is priced per thousand impressions or per click; sponsorship is a lump sum for a package. Both must be reduced to a comparable yield, in integer minor units, before you choose.

## Procedure

1. For CPM inventory: `revenue_minor = impressions * cpm_minor // 1000`. Keep CPM in integer minor units of currency per 1000 impressions.
2. Worked example: 480,000 impressions at CPM 12.50 = 1250 minor: `480000*1250//1000 = 600000` minor = USD 6,000.00.
3. For CPC: `revenue_minor = clicks * cpc_minor`. Worked: 3,000 clicks at 85 minor = 255000 minor.
4. Convert a sponsorship lump sum to a comparable yield: `effective_cpm = lump_minor * 1000 // impressions`.
   Worked: USD 4,000 = 400000 minor over 300,000 impressions = `400000*1000//300000 = 1333` minor CPM, versus a 1250 programmatic CPM — the sponsorship pays more if it does not cannibalise programmatic.
5. Subtract the cost to serve the placement: displaced house/programmatic revenue and any guaranteed-inventory break fee. `net_minor = revenue_minor - displaced_revenue_minor`.
6. Compare fill and floor: unsold impressions earn zero, so a floor CPM only competes with the next-best use of the slot.
7. For a sponsorship with deliverables (newsletter, video, podcast), allocate the lump by impression share so per-channel yield is visible.
8. Model seasonality: CPMs rise in Q4, so a yearly average misprices a January campaign.
9. Report effective yield per channel and the floor CPM below which the slot is better left to house content.

10. Model inventory elasticity: a floor CPM set too high leaves impressions unsold and total revenue can fall as CPM rises.
11. Contract sponsorship deliverables with a make-good clause so unserved impressions are credited, not assumed delivered.
12. Segment yield by placement and device; a blended CPM hides a weak mobile slot.
13. Deduct sales cost and ad-ops headcount from ad revenue to get a contribution figure, not a gross.
14. Compare a sponsorship's effective CPM against the floor, not the average, since the slot's alternative is the floor.
15. Re-price seasonally: hold a Q4 rate card separate from the off-season one.

## Pitfalls

- Comparing a lump sponsorship to a CPM without converting; the lump can look large and be a low yield.
- Ignoring displaced revenue: a sponsorship that replaces higher-CPM inventory is a loss dressed as a win.
- Counting billed impressions rather than viewable/served, which overstates the denominator and understates CPM.
- Averaging CPM across the year hides the Q4 spike and misprices off-season deals.
- Float division in CPM yields leaks cents across a campaign report; integer minor units stay exact.

- Raising the floor to chase CPM can leave a third of the inventory unsold, cutting total revenue.
- A sponsorship without a make-good clause for under-delivery becomes a disputed invoice.
- A blended CPM hides a loss-making placement that sells well but underpriced.
- Ignoring ad-ops cost makes gross ad revenue look like contribution margin.

## Verification

    python3 -c "print(480000*1250//1000, 400000*1000//300000)"
    # 600000 1333 -> $6,000 programmatic vs a $1.333 effective CPM sponsorship

Report: revenue per placement, effective CPM, displaced revenue, and the recommended floor CPM.
