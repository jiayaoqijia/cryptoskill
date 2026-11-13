---
name: corpus-audit
domain: writing/brand-guidelines
trigger: "Running corpus audits across a document set, logging verbatim quotes, locations, and severities"
anti_trigger: "Constructing audit checklists (subskills/checklist-construction.md); detecting recurring style slips across text (subskills/slip-detection.md)"
scope: "Run corpus audits across a document set, logging verbatim quotes, locations, and severities."
status: seedling
---

# Corpus Audit

## Standard

- **GOV.UK Content Audit Standards**: systematic methodology for reviewing large document corpuses against published style and terminology standards. <https://www.gov.uk/guidance/style-guide>
- **Microsoft Writing Style Guide**: enterprise editorial practices for conducting comprehensive documentation and content reviews. <https://learn.microsoft.com/en-us/style-guide/>
- **ISO 24495-1 Plain Language Principles**: evaluation frameworks ensuring structured, evidence-based assessment of communication clarity. <https://www.iso.org/standard/78907.html>
- **AP Stylebook**: professional guidance on maintaining rigorous inspection records and editorial logging standards. <https://www.apstylebook.com/>
- ⚠️ House convention: audit findings must be recorded as objective evidence consisting of verbatim quotes and exact file locations; unsupported opinions or vague summaries invalidate the audit log.

## Decision rules

1. Define the precise scope of the audit, specifying whether a full sweep or a representative sample of documents is required.
2. Evaluate every document in scope systematically against every item in the constructed audit checklist.
3. Log every finding as a structured record containing verbatim quote, rule ID, file location, and severity class.
4. Rank the final audit report by finding frequency and severity to direct downstream remediation priorities.

## Procedure

1. Establish audit boundaries by listing all target documents, directories, or publication repositories in scope.
2. Determine the audit sampling strategy: full corpus sweep for critical policy releases or stratified sampling for large documentation archives.
3. Execute the checklist review sequentially for each document, noting mechanical matches and evaluating judgment criteria.
4. When a failure is detected, extract the exact offending text as a verbatim quote without alteration.
5. Record the finding in the audit ledger alongside its file path, line number or section heading, rule ID, and assigned severity.
6. Aggregate all logged findings into a summary report ranked by total frequency and maximum severity level.
7. Deliver the completed audit report to editorial and product stakeholders as the definitive baseline for remediation.

## Anti-patterns

- Conducting audits without defining clear scope boundaries, resulting in incomplete document coverage.
- Recording findings as vague paraphrases or general impressions rather than exact verbatim quotes.
- Omitting file locations and line numbers, making it impossible for remediators to locate the flagged text.
- Publishing audit reports without severity ranking, leaving critical brand blockers buried beneath minor typos.

## Done checklist

- [ ] Audit scope and sampling strategy are explicitly defined.
- [ ] All target documents are reviewed against the complete checklist.
- [ ] Every finding is recorded with an exact verbatim quote.
- [ ] File locations and section references are logged for all findings.
- [ ] Severity classes and rule IDs are attached to every record.
- [ ] Audit ledger is aggregated into a frequency- and severity-ranked report.
- [ ] Report is delivered to stakeholders as the remediation baseline.

## Sources

- GOV.UK Style Guide. <https://www.gov.uk/guidance/style-guide>
- Microsoft Writing Style Guide. <https://learn.microsoft.com/en-us/style-guide/>
- ISO 24495-1: Plain language - Part 1: Governing principles and guidelines. <https://www.iso.org/standard/78907.html>
- AP Stylebook. <https://www.apstylebook.com/>
