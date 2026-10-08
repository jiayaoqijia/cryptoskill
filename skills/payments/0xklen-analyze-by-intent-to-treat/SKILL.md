---
name: analyze-by-intent-to-treat
description: Use when treatment compliance is imperfect. Reports the intent-to-treat effect as primary and dilution-corrects the per-protocol view.
---

# Analyze by Intent to Treat

Randomisation is preserved only if you analyse units in the arm they were assigned to, whether or not they complied. Dropping non-compliers re-introduces the selection bias the experiment existed to remove.

## Procedure

1. Primary analysis: include everyone assigned, in their assigned arm, regardless of whether they saw the feature or completed the flow.
2. Report the compliance rate per arm. Low compliance shrinks the intent-to-treat effect toward zero by design.
3. Present per-protocol or complier-average effects only as secondary, and label the population they describe.
4. Estimate the dilution: ITT effect is roughly the complier effect times the exposure rate. Use it to sanity-check a null:
   ```sql
   SELECT arm,
          count(*)                                AS assigned,
          count(*) FILTER (WHERE exposed)         AS exposed,
          round(count(*) FILTER (WHERE exposed)::numeric/count(*), 3) AS compliance
   FROM exp_assignment GROUP BY 1;
   ```
5. For non-compliance driven by a defect (the feature never rendered), fix and re-run rather than reasoning around it.
6. Check that the compliance rate is not itself different between arms — differential exposure is a bug, not a behaviour.

## Pitfalls

- Trigger-based analysis ("users who used the feature") compared to all controls is a biased contrast.
- Instrumenting exposure only in treatment makes compliance look asymmetric and biases every funnel metric.
- A null ITT with 30% compliance can still hide a real effect; compute the dilution before declaring no effect.
- Per-protocol sub-setting breaks randomisation; the groups differ on the very thing that drives compliance.
- Attrition after assignment (uninstall, churn) is part of the ITT population, not a reason to exclude.

## Verification

    psql "$DSN" -c "SELECT arm, count(*) AS n, count(*) FILTER (WHERE exposed) AS exposed FROM exp_assignment GROUP BY 1;"

Report: "ITT lift +0.9pt (95% CI 0.3 to 1.5); compliance 62% treatment / 98% control — differential exposure flagged. Per-protocol CACE is +1.6pt but is secondary only."
