---
name: audit-marketing-attribution-model
description: Use when channel or campaign performance is reported. Checks the attribution model, tracking loss, and windows before crediting or defunding a channel.
---

# Audit a Marketing Attribution Model

Every attribution model is a set of arbitrary rules that redistribute the same conversions. Before cutting spend on a "bad" channel, know what the model chose to ignore.

## Procedure

1. Identify the model: last-touch, first-touch, linear, position-based, or data-driven. Each gives one channel credit the others lose.
2. Re-run the same conversions under a second model and diff the per-channel results. Large diffs are definition, not performance:
   ```python
   import pandas as pd
   d = pd.read_csv('touchpoints.csv').sort_values('ts')
   last  = d.groupby('conv_id').tail(1).groupby('channel').size()
   first = d.groupby('conv_id').head(1).groupby('channel').size()
   print(pd.concat([last.rename('last'), first.rename('first')], axis=1).fillna(0))
   ```
3. Quantify tracking loss: cookie and ID decay, iOS ATT opt-out, ad-blockers, cross-device gaps. Missing upper-funnel touchpoints make direct or none swell and paid look heroic.
4. Check the lookback window: a 30-day click window versus view-through credits different channels; state which is set and whether it matches the sales cycle.
5. Separate new-customer from returning-customer conversions — brand-search wins are often existing demand, not incremental.
6. Where possible, triangulate with an incrementality test (geo holdout or public service announcement) rather than trusting the model.
7. Report the credit and the unattributed share together; a big direct bucket is a measurement gap.

## Pitfalls

- Last-touch overcredits bottom-funnel (brand, retargeting) and undercredits the prospecting that started the journey.
- "Direct / none" balloons when app or cross-device tracking breaks; it is a hole, not a channel.
- Post-ATT iOS loss depresses paid-social's attributed share without any change in real performance.
- Changing the lookback window mid-quarter rewrites history and makes a real spend change look like a result.
- Attribution is not incrementality; the model can credit a conversion that would have happened anyway.

## Verification

    python3 -c "import pandas as pd; d=pd.read_csv('touchpoints.csv'); print(d.groupby('channel').size()/len(d))"
    # then diff last-touch vs first-touch shares; a ranking flip makes the model the finding

Report: "Last-touch ranks paid-social #1; first-touch ranks organic-search #1 — ranking flips, so channel 'performance' is a model artefact. 38% of conversions unattributed; recommend a geo incrementality test before any budget cut."
