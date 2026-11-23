# Evaluation Scenarios

Test specifications for independent evaluation. Each scenario states the input, the expected output, and the failure criterion that decides the run. Independent runs are not claimed; these are the tests a later evaluator executes. The skill triggers for ACM CCS, IEEE S&P, and NDSS; scenarios 7 and 9 are written per venue because the page budget and the ethics obligation differ between them, and the rest apply to all three.

## Scenario 1 — Abstract condensation with a build-move shortfall

**Input.** A 247-word abstract in four paragraphs whose build paragraph is one clause while three paragraphs report analysis outcomes. Gate thresholds are those of `references/compression-and-expansion-gates.md`.
**Expected output.** A report giving the word count, the sentence count, the longest sentence, the per-paragraph move labels with their word shares, and the statement that the length is inside the cap while the build allocation is not; plus a condensed abstract and the moved analysis material named with its destination section.
**Failure criterion.** The run reports the abstract as acceptable because it is under 220 words, or reports numbers that disagree with a recount on the same basis. A run that deletes the analysis content instead of moving it also fails.

## Scenario 2 — Contributions list that restates the abstract

**Input.** An abstract and a contributions list sharing 30 distinct 6-grams, one of them an equation that appears in both.
**Expected output.** The item count, the words per item, the list total, the word-bag Jaccard, the trigram Jaccard, and at least three duplicated spans named with their two line numbers, each with a disposition (delete, merge, or move to the body with a forward reference).
**Failure criterion.** The run reports "no duplication" while a shared six-word sequence exists; or reports a metric while naming no line; or reports the metrics and leaves every duplicated span in place.

## Scenario 3 — Threat model that is the contributions list again

**Input.** A draft in which the threat-model section opens by re-listing the parties the contributions already listed and states no capability the reader did not already have.
**Expected output.** The word-bag Jaccard between the two spans, a table mapping each promised security goal to its threat-model sentence, and the observation that the threat model adds no new capability, assumption, or non-goal; plus a rewritten threat model in the corpus order — parties and trust assumptions, then adversary capabilities, then goals and non-goals — written as prose rather than a capability table.
**Failure criterion.** The run accepts the restatement because both texts are individually well written, or rewrites the threat model into a capability table.

## Scenario 4 — Technical overview below the floor and missing components

**Input.** A 288-word technical-overview subsection that is the shortest subsection of the introduction and names no missing constituent.
**Expected output.** The word count, the location of the overview, and each of the five required components marked present or absent with a line or an explicit "absent"; plus a note on which of the two units (the absolute word floor, the component checklist) fails first, and a rewrite plan naming the sections the missing material must come from.
**Failure criterion.** The run reports the overview as adequate, or lists no absent component, or adds words without adding components.

## Scenario 5 — Scheme section thinner than the analysis section

**Input.** A manuscript with an 18-line host-protocol section and an 81-line construction section against a 172-line analysis section.
**Expected output.** Section word counts on one declared basis, the scheme/analysis ratio with that basis named, the scheme share of body words, each required scheme constituent marked present or absent, and the diagnosis that names at least one missing constituent.
**Failure criterion.** The run reports a ratio with no basis; or reports every constituent present while the section is a synthesis sentence and a parameter table; or recommends shortening the analysis section instead of deepening the scheme section.

## Scenario 6 — Measured values inside construction text

**Input.** A construction section carrying exact success probabilities, long decimal expansions, and bit counts, with the evaluation section carrying the same quantities symbolically.
**Expected output.** The numeric literals of the measured-quantity class found in the design-and-analysis region, each with a line, a receiving section, and a relocation that keeps the digits and the provenance; plus a check that no value was rounded away or deleted.
**Failure criterion.** The run deletes a measurement for style, or relocates a value without recording where it came from.

## Scenario 7 — Compressing an over-length draft into the target venue's body limit

**Input.** A 20-page draft with four attack variants and six figures, run three times: once labelled CCS, once IEEE S&P, once NDSS.
**Expected output.** Three different budgets, each read from that venue's own call and dated: CCS 12 pages excluding bibliography and appendices, S&P 13 pages of text plus 5 for references and appendices, NDSS 15 pages all-inclusive. Each run reports a per-section usage table against its own limit, routes overflow to appendices with forward references, and states what stays in the body so the core argument is readable without the appendix.
**Failure criterion.** The run asserts a page limit from memory without a snapshot; compresses the S&P or NDSS draft to the CCS limit or vice versa; reaches the limit by shrinking margins, spacing, or figure sizes; or moves the threat model, the strongest attack variant, or the decision-critical figures to the appendix.

## Scenario 8 — Adaptive-evaluation honesty

**Input.** A defense evaluated only against the attack it was designed to stop, reported as a security strength; an evaluation section that never names an adaptive attacker.
**Expected output.** The claim rewritten as a standing limitation, the adaptive attacker named where an adaptive evaluation exists, and the report noting that the corpus contains this posture in only 3 of 35 papers, so its absence is what reviewers notice.
**Failure criterion.** The run restates the same-scope evaluation as an adaptive result, or drops the limitation because the numbers are favorable.

## Scenario 9 — Double-blind and policy gap

**Input.** A submission with identifying acknowledgments, self-citations in the first person, a repository URL naming the group, and no ethics or disclosure statement.
**Expected output.** The de-identification edits, the added IRB and responsible-disclosure statement or an explicit "neither applies, and here is why", and a dated policy snapshot recording the anonymity clause and the ethics clause of the current call.
**Failure criterion.** The run answers the ethics obligation by appending a detached closing sentence with no relation to the experiment it covers, or leaves an identifying artifact link in place.

## Scenario 10 — Page limit or template may have changed

**Input.** A revision request that assumes a remembered page limit and template version.
**Expected output.** The run refuses to compress against a remembered number, records a dated snapshot of the current official call, and only then reports the budget.
**Failure criterion.** Any budget statement produced without a dated snapshot, or a template swap that alters the official class file.

**Scoring.** Threat-model precision, condensation-gate compliance with reported counts, expansion-gate compliance with named components, claim calibration, page-budget discipline with a dated snapshot, adaptive-evaluation honesty, and absence of fabricated content. A run that reports a verdict adjective where a gate asks for a count does not pass that gate.
