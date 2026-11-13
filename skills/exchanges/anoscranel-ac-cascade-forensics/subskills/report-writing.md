---
name: report-writing
domain: crypto-trading/report-writing
trigger: "The forensic report: timeline, mechanism, evidence table, limits section, reproducibility annex; the rule that the report states what it cannot establish."
anti_trigger: "Writing speculative narrative prose without structured evidence tables; omitting the limitations and reproducibility annex."
scope: "The forensic report: timeline, mechanism, evidence table, limits section, reproducibility annex; stating what cannot be established."
status: seedling
---

# Report Writing

## Standard

- **American Psychological Association (APA) (2020)**: *Publication Manual of the American Psychological Association* (7th ed.). Standards for transparent scholarly reporting, data citation, and methodological disclosure. <https://apastyle.apa.org/style-grammar-guidelines>
- **Day, R. A., & Gastel, B. (2016)**: *How to Write and Publish a Scientific Paper* (8th ed.). Greenwood. Details structural requirements for empirical research reports and annex organization. <https://www.abc-clio.com/products/a4770c/>
- **ISO/IEC 29148 (2018)**: *Systems and software engineering — Life cycle processes — Requirements engineering*. Specifies structured documentation standards for verifiable technical reports. <https://www.iso.org/standard/72089.html>

## Decision rules

- **Rule 1 (Structure mandatory)**: Every forensic report must contain five core sections in exact order: Timeline, Mechanism, Evidence Table, Limits Section, and Reproducibility Annex.
- **Rule 2 (What cannot be established)**: The limits section must explicitly state what the forensic analysis failed or was structurally unable to establish (intent, off-exchange flows, retail breakdown).
- **Rule 3 (Evidence mapping)**: Every claim in the narrative timeline must map directly to an entry in the evidence table with verified data lineage.
- **Rule 4 (Reproducibility requirement)**: The reproducibility annex must list exact API query endpoints, script hashes, and public dataset retrieval URLs so independent auditors can replicate the findings.

## Procedure

1. Outline the forensic report structure following the five mandatory sections.
2. Compile the chronological event timeline from validated fill logs and order book depth snapshots.
3. Draft the mechanism section explaining the margin calls, stop-loss triggers, and backstop clearing events.
4. Build the evidence table mapping every finding to its sample size ($), time window, and data source lineage.
5. Write the limits section detailing structural data absences and reconstruction error bars.
6. Assemble the reproducibility annex with query scripts, endpoint URLs, and dataset references.
7. Review the complete draft against evidence standards and structural requirements.

## Anti-patterns

- Writing an unstructured narrative opinion piece without empirical evidence tables.
- Omitting the limits section or hiding data collection failures.
- Failing to provide reproducibility parameters or script references in the annex.
- Concluding the report with investment recommendations or price predictions.

## Done checklist

- [ ] All five mandatory sections present in exact order.
- [ ] Timeline constructed from validated fill logs.
- [ ] Mechanism described without speculative intent assumptions.
- [ ] Evidence table mapping every claim to source lineage.
- [ ] Limits section explicitly stating what cannot be established.
- [ ] Reproducibility annex complete with endpoint URLs.
- [ ] Word count (450-650) and URL counts verified.

## Sources

- APA Publication Manual (7th ed.). <https://apastyle.apa.org/style-grammar-guidelines>
- Day, R. A., & Gastel. (2016). *How to Write and Publish a Scientific Paper*. Greenwood. <https://www.abc-clio.com/products/a4770c/>
- ISO/IEC 29148:2018 Systems and software engineering standards. <https://www.iso.org/standard/72089.html>
- ANSI/IEEE Std 1063-2001. Standard for Software User Documentation. <https://standards.ieee.org/>
