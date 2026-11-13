---
name: report-discipline
domain: software-engineering/architecture-survey
trigger: "Writing the final architecture survey report; scaling content to repository size; omitting empty sections; stating survey coverage and unknowns"
anti_trigger: "Ranking candidates (subskills/ranking-criteria.md); handling follow-up design or implementation work (subskills/follow-up-boundary.md)"
scope: "The report as the sole permitted write: scale to the repository, omit empty sections, state coverage and unknowns, write only to the specified path, and stop after delivery."
status: seedling
---

# Report Discipline

## Standard

- **ISO/IEC/IEEE 29148:2018**: requirements and technical reports must be structured unambiguously, omitting speculative material and explicitly documenting constraints and limitations. <https://www.iso.org/standard/72089.html>
- **Swartout & Balzer, "On the Inevitable Embeddings of Software Development"**: technical reports must reflect actual observed state without conflating aspirations with current implementation facts. <https://ieeexplore.ieee.org/document/1484/>
- ⚠️ House convention: the survey report is the sole permitted write operation; generating code patches or modifying configuration files violates read-only doctrine.

## Decision rules

1. If a repository section contains no material findings, omit the corresponding report subsection rather than including placeholder text.
2. If survey coverage omits major subdirectories due to access limits or exclusion rules, list those omissions explicitly in the report's coverage statement.
3. If output targets are specified by user instructions, write the report strictly to that path and nowhere else.
4. If completion of the report occurs, stop execution immediately without prompting for refactoring implementation.

## Procedure

1. Compile the survey scope summary, verified evidence trails, structured smells, and ranked improvement candidates into a single cohesive report document.
2. Structure the report with clear headings: Executive Summary, Survey Coverage & Limitations, Observed Structural Smells, Prioritized Improvement Candidates, and Unresolved Unknowns.
3. Review every claim against the evidence file paths and line ranges gathered during sampling; remove any statement lacking concrete support.
4. Scale the length and depth of the report to match the size of the repository (concise summaries for small codebases, structured tables for large monorepos).
5. Write the final report to the designated path on disk, verify its integrity, and conclude the survey session without initiating implementation.

## Anti-patterns

- Modifying source code files, configuration sheets, or build scripts during the survey run.
- Padding the report with generic software engineering best practices that lack repository-specific evidence.
- Hiding sampling blind spots or unexamined subdirectories from the coverage statement.
- Continuing past report delivery to offer unsolicited coding assistance or refactoring execution.

## Done checklist

- [ ] Survey report compiled with required standard headings.
- [ ] All claims anchored to verified evidence citations.
- [ ] Coverage limits and unexamined subdirectories stated explicitly.
- [ ] Report written exclusively to the designated target path.
- [ ] Execution stopped immediately after report delivery without implementation.

## Sources

- International Organization for Standardization. _ISO/IEC/IEEE 29148:2018 Systems and software engineering — Life cycle processes — Requirements engineering_. ISO, 2018. <https://www.iso.org/standard/72089.html>
- Swartout, William, and Robert Balzer. "On the Inevitable Embeddings of Software Development." _IEEE Transactions on Software Engineering_, vol. SE-8, no. 4, 1982, pp. 386-397. <https://ieeexplore.ieee.org/document/1484/>
