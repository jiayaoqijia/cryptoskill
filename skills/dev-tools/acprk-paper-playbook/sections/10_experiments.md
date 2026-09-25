# 10 Implementation and evaluation

Full procedure, table rules and fairness statements:
[experiments-writing](../../experiments-writing/SKILL.md).

## Nine-part structure

```
[opening]        "We evaluate <objects> inside <library>, changing only <stage>; everything
                 else is that of <baseline>, so every gain below is due to <object> alone."
                 Artifact footnote. Signpost: §x.1 fixes the setup, §x.2 reports results.
[baselines]      One bullet per baseline: name + citation + what it is + where it runs
                 (our pipeline vs their artifact) + third-party repository link.
                 Paragraph on why some methods are "reported for context" only.
[platform]       CPU model and frequency, threads, compiler and library versions/commits,
                 repetitions and statistic, "every run is decryption-verified / output
                 checked against a cleartext reference".
[parameters]     Table: one row per parameter set with every parameter and a security
                 column. Text: provenance of sets, coverage, estimator + commit, binding
                 attack, excluded instances and why.
[derived params] How the instance determines the configuration; tie-breaking.
[configurations] Evaluators (i)(ii)(iii): which equals prior work, which is new.
[results]        Signpost sentence + figure (stage breakdown / vs baselines) + main table.
                 Three bold-headed claims, e.g.
                 \textbf{Speedup.} scope → range → two concrete points.
                 \textbf{The components compose, and neither suffices alone.} ablation.
                 \textbf{Coverage and overhead.} new cases covered + capacity/memory cost.
[comparison]     Table vs published implementations on the same parameters; incomparable
                 rows marked with a symbol and "—" in the ratio column; measured vs claimed
                 numbers both given.
[limitations]    Remarks: metric orientation, parallelism policy, where we lose.
```

## Number discipline (summary)

1. Single data source (EVIDENCE rows → json/csv → tables); no hand-typed numbers.
2. Scope sentence before every range.
3. Exclusions stated explicitly.
4. Reproduced vs claimed baseline numbers both reported.
5. Incomparable is not forced into a ratio.
6. Attribute each gain to the right component.
7. Disclose overheads (capacity, memory, key size, setup).
8. The ablation is the strongest evidence; include it in the body.
9. Keep measured ratios; normalised variants go to the appendix.
10. Baseline configuration details that favour or disfavour the baseline are
    disclosed (appendix is fine).

## Checklist

- [ ] Opening sentence isolates the changed component.
- [ ] Platform paragraph has the five elements (library+version, CPU, threads,
      repetitions+statistic, correctness check).
- [ ] Parameter table has a security column; excluded rows justified.
- [ ] Ablation in the body.
- [ ] Every table cell traceable to an EVIDENCE row.
