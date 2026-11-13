---
name: follow-up-boundary
domain: software-engineering/architecture-survey
trigger: "Handling post-survey requests after the report is delivered; handing off candidate evidence trails to design or implementation phases without starting work"
anti_trigger: "Writing the survey report (subskills/report-discipline.md); scoping the repository (subskills/survey-scope.md)"
scope: "After candidate selection: recording the chosen candidate and its evidence trail for subsequent design, migration, or implementation phases without starting them uninvited."
status: seedling
---

# Follow-Up Boundary

## Standard

- **IEEE Std 12207-2017**: software life cycle processes require clear handoff boundaries between diagnostic review phases and subsequent design or construction activities. ⚠️ cited without URL.
- **Brügge & Dutoit, _Object-Oriented Software Engineering_ (2009)**: architectural analysis outputs serve as inputs to design decision records, but analysis roles must not unilaterally execute implementation changes. <https://www.pearson.com/en-us/subject-catalog/p/Bruegge-Object-Oriented-Software-Engineering-Using-UML-Patterns-and-Java-3rd-Edition/P200000003319>
- ⚠️ House convention: once the survey report is delivered and the user selects a candidate, the survey role terminates; further work requires explicit transition to a distinct architectural design or coding workflow.

## Decision rules

1. If the user selects a candidate from the survey shortlist, record its evidence trail and boundary specification as the handoff artifact for subsequent work.
2. If the user asks for design alternatives for the chosen candidate, transition explicitly to architectural design rather than improvising design choices inside the survey context.
3. If the user asks for code implementation patches after candidate selection, refuse to write code in this session and direct the work to appropriate code construction workflows.
4. If no candidate is selected, close the survey session cleanly without generating residual stub files or scratch scripts.

## Procedure

1. Present the delivered survey report and await user selection of a prioritized improvement candidate from the shortlist.
2. Upon user selection of a candidate, package its cited evidence trail, proposed boundary, risk profile, and validation strategy into a clean handoff summary.
3. Explicitly state the termination of the survey phase and outline what subsequent workflows (architectural design, decision record drafting, or code refactoring) are required to proceed.
4. Stop execution and refuse automated code generation requests, maintaining strict separation between diagnostic review and implementation execution.
5. Archive the survey findings and handoff summary in accordance with project archiving standards without modifying production source trees.

## Anti-patterns

- Automatically starting code refactoring or writing implementation patches immediately after delivering the survey report.
- Conflating survey diagnostic findings with finalized architectural design decisions.
- Leaving dangling temporary files or modifying repository files during the follow-up transition.
- Proceeding with implementation tasks without verifying that the user approved a specific shortlist candidate.

## Done checklist

- [ ] Survey report delivered and user selection awaited.
- [ ] Selected candidate evidence trail and boundary packaged for handoff.
- [ ] Termination of survey phase explicitly stated.
- [ ] Subsequent design or coding workflows separated from survey review.
- [ ] Execution stopped without uninvited code modifications.

## Sources

- Institute of Electrical and Electronics Engineers. _IEEE Std 12207-2017: Systems and software engineering — Software life cycle processes_. IEEE, 2017. ⚠️ cited without URL.
- Brügge, Bernd, and Allen H. Dutoit. _Object-Oriented Software Engineering: Using UML, Patterns, and Java_. 3rd ed., Prentice Hall, 2009. <https://www.pearson.com/en-us/subject-catalog/p/Bruegge-Object-Oriented-Software-Engineering-Using-UML-Patterns-and-Java-3rd-Edition/P200000003319>
