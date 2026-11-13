---
name: style-sheet-intake
domain: writing/brand-guidelines
trigger: "Ingesting external corporate style guides into a testable rule set with explicit precedence and gap flagging"
anti_trigger: "Codifying a brand specification from scratch (subskills/brand-specification.md); building an audit checklist from rules (subskills/checklist-construction.md)"
scope: "Ingest external corporate style guides into a testable rule set with explicit precedence and gap flagging."
status: seedling
---

# Style Sheet Intake

## Standard

- **AP Stylebook Principles**: standard guidance on editorial intake, consistency, and conflict resolution across varied source documents. <https://www.apstylebook.com/>
- **Chicago Manual of Style (CMOS) Online**: authoritative reference for punctuation, compound words, and document hierarchy rules. <https://www.chicagomanualofstyle.org/>
- **ISO 24495-1 Plain Language Principles**: international standard for transforming complex source rules into clear, structured requirements. <https://www.iso.org/standard/78907.html>
- **Microsoft Writing Style Guide**: enterprise reference for managing terminology intake and resolving stylistic collisions. <https://learn.microsoft.com/en-us/style-guide/>
- ⚠️ House convention: when corporate style guides conflict with public standards, local project precedence governs, but unaddressed gaps must be explicitly flagged rather than guessed.

## Decision rules

1. Enforce strict precedence hierarchy: brand specification overrides corporate guide, which overrides public style guide, which overrides general convention.
2. Every external rule ingested must be translated into a testable statement with a boolean pass or fail outcome.
3. Identify and document explicit conflicts between incoming source documents before starting corpus audits.
4. Flag policy gaps where the incoming guide remains silent on critical formatting, terminology, or tone questions.

## Procedure

1. Collect all incoming corporate style guides, brand manuals, and legacy documentation requirements.
2. Review each source document to extract normative rules regarding spelling, punctuation, capitalization, and tone.
3. Establish the precedence order: brand specification, corporate guide, public style guide, general convention.
4. Cross-reference ingested rules against existing standards to detect direct contradictions or policy overlaps.
5. Resolve identified conflicts by applying the precedence hierarchy and documenting the rationale for each decision.
6. Compile an explicit gap analysis list noting areas where the ingested guide provides no instruction.
7. Publish the consolidated, conflict-free rule set as the intake baseline for checklist construction.

## Anti-patterns

- Ingesting external guides without establishing precedence, leading to unresolved contradictions during audits.
- Translating vague stylistic preferences into mandatory rules without testable verification criteria.
- Ignoring policy gaps in incoming guides and improvising ad-hoc rules during active corpus audits.
- Overwriting established brand specifications with incoming corporate guidelines without stakeholder review.

## Done checklist

- [ ] All incoming corporate style guides and manuals have been collected and reviewed.
- [ ] Normative rules are extracted as testable statements.
- [ ] Precedence hierarchy is explicitly documented and applied.
- [ ] Direct conflicts between sources are resolved and justified.
- [ ] Policy gaps are cataloged in an explicit gap analysis report.
- [ ] Consolidated rule set is formatted for downstream checklist construction.
- [ ] Intake baseline is approved for operational use.

## Sources

- AP Stylebook. <https://www.apstylebook.com/>
- Chicago Manual of Style. <https://www.chicagomanualofstyle.org/>
- ISO 24495-1: Plain language - Part 1: Governing principles and guidelines. <https://www.iso.org/standard/78907.html>
- Microsoft Writing Style Guide. <https://learn.microsoft.com/en-us/style-guide/>
