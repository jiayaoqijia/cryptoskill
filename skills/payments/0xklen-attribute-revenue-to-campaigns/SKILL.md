---
name: attribute-revenue-to-campaigns
description: Use when spend must be judged by revenue, not clicks. Attributes realised revenue to campaigns with a stated model and window and reconciles attributed revenue back to booked revenue.
---

# Attribute revenue to campaigns

Clicks are a leading indicator; revenue is the scoreboard. Attribute realised revenue to campaigns with an explicit model, then reconcile the attributed total to the ledger — if attribution claims more revenue than exists, the model is lying.

## Procedure

1. Define the model (last-touch, first-touch, linear) and the lookback window up front, and hold them fixed for the quarter.
2. Join touchpoints to revenue, not to conversions: a user's revenue is the sum of their paid invoices in integer minor units during the window.
3. For last-touch, credit the campaign of the final touchpoint before the revenue event:
   ```
   touch = touchpoints.sort_values('ts').groupby('user_id').last()
   rev = invoices[invoices.status == 'paid'].groupby('user_id').amount_minor.sum()
   attributed = touch.join(rev, how='inner').groupby('campaign').amount_minor.sum()
   ```
4. Reconcile: `sum(attributed) + unattributed == total booked revenue`. If attributed exceeds booked, a join double-counted.
5. Worked example: booked revenue 900000 minor; last-touch attributes 620000; unattributed 280000 (31%) — that is a measurement gap or real organic share, and must be labelled.
6. For recurring revenue, credit the acquisition campaign at first payment, then hold it responsible for the lifetime value it produced, not just the first invoice.
7. Compute return per campaign: `roas = attributed_revenue_minor / spend_minor`. Segment new vs returning; brand campaigns mostly harvest returning demand.
8. Compare two models on the same data; a ranking flip means the "winner" is a model artefact.
9. Report attributed revenue, unattributed share, ROAS and the model used, always together.

10. Store the touchpoint ids behind each attribution so a result can be re-derived and a dispute answered.
11. Cross-check attributed revenue against a short incrementality test (geo holdout) at least quarterly for the top channel.
12. Attribute net revenue, not gross charges, so refunds do not inflate a campaign's credit.
13. Keep a control bucket of unattributed users to estimate the harvest baseline.
14. Reconcile per-campaign ROAS to the marketing spend ledger before publishing.
15. Report the model's stability: re-run last quarter's data under the current model and note any ranking change.

## Pitfalls

- Attributing to conversions and then pricing them with revenue mixes two denominators.
- Letting attributed revenue exceed booked revenue because a multi-touch join counted one invoice once per touchpoint.
- Crediting brand search with revenue from customers who would have converted anyway; it harvests, it does not create.
- Changing the lookback window mid-quarter rewrites history and flatters the newest campaign.
- Reporting ROAS without the unattributed bucket hides that a third of revenue has no campaign at all.

- Without stored touchpoint ids, a channel's result cannot be recomputed when the model changes.
- Never testing incrementality means a harvest channel keeps its attribution indefinitely.
- Attributing gross rather than net revenue credits a campaign for refunded sales.
- Publishing ROAS that does not reconcile to the spend ledger makes the marketing number unfalsifiable.

## Verification

    python3 -c "import pandas as pd; d=pd.read_csv('joins.csv'); print(d.groupby('campaign').amount_minor.sum().sum(), 'vs booked', d.amount_minor.sum())"
    # attributed total must be <= booked; a larger number proves double-counting

Report: model and window, attributed revenue, unattributed share, and per-campaign ROAS including the harvest-only ones.
