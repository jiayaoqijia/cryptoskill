---
name: checklist-construction
domain: writing/brand-guidelines
trigger: "Turning rules into a deterministic audit checklist separating automated checks from evidenced judgment calls"
anti_trigger: "Ingesting external style guides (subskills/style-sheet-intake.md); running corpus audits across a document set (subskills/corpus-audit.md)"
scope: "Turn rules into a deterministic audit checklist separating automated checks from evidenced judgment calls."
status: seedling
---

# Checklist Construction

## Standard

- **ISO 24495-1 Plain Language Principles**: structural design standards for clear, verifiable criteria in document evaluation. <https://www.iso.org/standard/78907.html>
- **GOV.UK Publishing Standards**: operational checklists ensuring consistent terminology, formatting, and structural compliance across public content. <https://www.gov.uk/guidance/style-guide>
- **Microsoft Writing Style Guide**: enterprise reference for defining clear, testable editorial standards and verification procedures. <https://learn.microsoft.com/en-us/style-guide/>
- **AP Stylebook**: authoritative guidance on standardized rule formulation and consistent checklist categorization. <https://www.apstylebook.com/>
- ⚠️ House convention: audit checklists must cleanly separate deterministic mechanical checks from subjective judgment checks; judgment checks require explicit source citation to remain valid.

## Decision rules

1. Every rule from the ingested specification must map to exactly one checklist item with a defined severity class.
2. Separate deterministic checks (terminology, banned words, capitalization, formatting) from judgment checks (tone fit, clarity).
3. Judgment checks must mandate that the auditor cite verbatim quote evidence supporting any failure finding.
4. Assign each checklist item a fix category (replace, delete, rephrase, reformat) to guide remediation passes.

## Procedure

1. Review the consolidated rule set and group rules into functional categories: terminology, mechanics, tone, and structure.
2. Translate each rule into a concise audit check with a unique identifier and clear pass or fail condition.
3. Classify each check into a severity level: blocker, major, minor, or suggestion.
4. Designate deterministic checks where automated scripts or simple string matching can verify compliance.
5. Designate judgment checks where human review is required, appending mandatory evidence citation rules.
6. Assign a standard fix category to every checklist item to streamline downstream remediation.
7. Test the constructed checklist against sample documents to verify inter-rater reliability and operational clarity.

## Anti-patterns

- Mixing deterministic mechanical checks with subjective judgment checks into ambiguous composite items.
- Omitting severity classifications, treating minor capitalization slips with the same weight as critical brand violations.
- Writing judgment checks that allow failure findings without requiring verbatim quote evidence.
- Leaving fix categories unassigned, forcing remediators to guess the correct correction method.

## Done checklist

- [ ] All ingested rules are mapped to unique checklist items.
- [ ] Checklist items are categorized into deterministic and judgment types.
- [ ] Severity classes (blocker, major, minor, suggestion) are assigned to every item.
- [ ] Judgment checks explicitly mandate verbatim quote evidence citation.
- [ ] Fix categories (replace, delete, rephrase, reformat) are assigned to all items.
- [ ] Inter-rater reliability is verified against test document samples.
- [ ] Final checklist is formatted for execution in corpus audits.

## Sources

- ISO 24495-1: Plain language - Part 1: Governing principles and guidelines. <https://www.iso.org/standard/78907.html>
- GOV.UK Style Guide. <https://www.gov.uk/guidance/style-guide>
- Microsoft Writing Style Guide. <https://learn.microsoft.com/en-us/style-guide/>
- AP Stylebook. <https://www.apstylebook.com/>
