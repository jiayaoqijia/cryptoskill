# Evaluation Scenarios

Test specifications for independent evaluation of the USENIX Security skill. Every scenario states its input, the output a correct run must produce, and the failure criterion that decides the run. Independent runs are not claimed; these are the tests a later evaluator executes.

Two things make a USENIX run correct rather than merely plausible. First, the counted gates are **invoked from the family copy** — `ccs-writing-style` → `references/compression-and-expansion-gates.md` — and reported with their counts, since this skill owns no second copy of them. Second, the four USENIX-specific slots in `references/compression-and-expansion-gates.md` are applied on top: the 13+1 page budget, the two mandated sections and their placement, the permitted embedded overview form, and the thin-standalone-threat-model habit.

## Scenario 1 — Abstract that spends its words on analysis

**Input.** A 247-word abstract, four paragraphs, in which the paragraph naming the system and its mechanism is one clause while the remaining paragraphs report proved bounds and an open problem.
**Expected output.** The four counts from the family gate's abstract pass (words, sentences, longest sentence, words per paragraph) plus the move label for each paragraph, and the finding that the total sits inside the cap while the allocation does not — followed by a condensed version in which the mechanism paragraph grows and the analysis paragraphs shed detail they share with the body.
**Failure criterion.** The run clears the abstract because the word total is under the cap, or reports per-paragraph numbers that a recount on the same basis contradicts, or deletes a proved claim instead of relocating its detail.

## Scenario 2 — Contribution list that recycles the abstract's sentences

**Input.** An abstract and a contribution list sharing a run of six consecutive words, one shared expression appearing twice in each text, and a contribution block of 950 words against a 247-word abstract.
**Expected output.** The item count, the words per item, the block total, both overlap indices from the family gate, and the list of shared runs with the two locations of each; at least three shared spans named with their lines, each carrying a decision — cut, fold into one statement, or move to the body behind a forward reference.
**Failure criterion.** The run answers "no meaningful overlap" while a six-word shared run exists; or reports an index value while naming no line; or reports the indices and cancels nothing.

## Scenario 3 — Adversary statement embedded in the system overview

**Input.** A submission with no standalone threat-model section: the adversary is described across two paragraphs of the system overview plus a sentence in the evaluation, the participating parties are listed twice, and one claim depends on a capability the overview never grants. This placement is permitted here — 28% of USENIX corpus papers have a standalone section (`skills-work/corpus/security/statistics.md:217`, `:153`).
**Expected output.** A single consolidated adversary statement in prose — parties and trust assumptions, then capabilities, then what is not guaranteed — placed where the reader meets it first; a list of the capabilities the evaluation needs but the statement does not grant, each mapped to a claim; and the overlap index between the contribution list and the adversary statement from the family gate.
**Failure criterion.** The run declares the placement itself the defect and demands a new numbered section, or accepts a statement that never grants the capability the evaluation silently uses, or repairs the gap by adding a capability table.

## Scenario 4 — Overview located inside the introduction

**Input.** Two variants of the same draft: variant A has no overview section at all and the overview function is a 250-word paragraph inside the introduction; variant B has a 288-word named subsection of the introduction that lists the sections of the paper without explaining a mechanism.
**Expected output.** For both variants, the location classified as standalone section / named subsection / named paragraph, and the family gate's constituent check reported item by item. Variant A fails on components with no word floor applied to the paragraph form; variant B fails on the mechanism and forward-reference components despite being longer than the floor.
**Failure criterion.** The run requires a standalone section in either variant (this venue permits the embedded form), or passes variant A because the paragraph is "short but present", or passes variant B because 288 words cleared a floor.

## Scenario 5 — Design section thinner than its analysis section

**Input.** A submission whose protocol description is one synthesis sentence plus a parameter table, while the security analysis and evaluation together run several times its length.
**Expected output.** Design and analysis masses measured on one named basis, the ratio, the design share of the body, and the family gate's constituent checklist reported item by item, with at least one missing constituent named and the section it must draw from.
**Failure criterion.** The run reports a ratio with no basis; or reports all constituents present while the protocol is a sentence and a table; or proposes trimming the analysis instead of deepening the design; or judges the ratio against the family's crypto-corpus floor without saying so (R-15.6 — a family's own floor is not interchangeable with a sibling's).

## Scenario 6 — Measured values inside the design text

**Input.** A design section carrying exact success probabilities, long decimal expansions and byte counts, while the evaluation section states the same quantities symbolically.
**Expected output.** The measured-quantity literals found in the design and proof region, each with its line, its receiving section, and a move that keeps the digits and records where they came from; and a check that the evaluation gained the explicit values it was missing.
**Failure criterion.** The run rounds a value away, deletes one for style, or moves a value without recording its provenance.

## Scenario 7 — Compressing into the USENIX budget, with the extra page accounted for

**Input.** A 20-page draft with four attack variants and six figures, and a draft skeleton that lists an appendix but neither mandated section.
**Expected output.** A dated snapshot of the current USENIX call; a per-section usage table against 13 body pages plus the additional page for **Ethics considerations** and **Open science**; overflow routed to appendices with forward references rather than by tightening spacing or the template; and the two mandated sections shown in the main body immediately before the References.
**Failure criterion.** The run quotes a page limit from memory; or compresses the draft to a sibling venue's limit (CCS 12 excluding bibliography, IEEE S&P 13+5, NDSS 15 all-inclusive); shrinks margins or spacing; or treats the two mandated sections as appendix material.

## Scenario 8 — Defense evaluated only against its intended attack

**Input.** A defense measured against the attack it was designed to stop, presented as a security guarantee, with no adaptive attacker named anywhere. Only 3 of 35 corpus papers discuss adaptive attacks (`skills-work/corpus/security/statistics.md:185`).
**Expected output.** The claim rewritten as a standing limitation with the measurement it actually has; the adaptive attacker named wherever an adaptive evaluation exists; and the report noting that low corpus frequency is what makes the missing posture visible to a reviewer.
**Failure criterion.** The run restates the same-scope evaluation as if it were adaptive, or drops the limitation because the measured numbers are favorable.

## Scenario 9 — Double-blind gap plus missing mandated sections

**Input.** A submission with identifying acknowledgments, first-person self-citations, a group-branded artifact URL, no section titled "Ethics considerations", and no section titled "Open science".
**Expected output.** The de-identification edits; both sections created in the main body immediately before the References with the titles the policy requires; and a dated snapshot recording the anonymity, ethics and open-science clauses of the current call. Where the work involves human subjects or a live vulnerability, the ethics section states the review status and the disclosure action or explains why neither applies.
**Failure criterion.** The run buries the ethics material in an appendix, invents an ethics claim with no review behind it, or leaves an identifying artifact link in place.

## Scenario 10 — A remembered budget from a previous cycle

**Input.** A revision request that states a page limit and a template version from memory, plus an earlier draft that references the prior cycle's ethics clause wording.
**Expected output.** A refusal to compress against the remembered figures; a dated snapshot of the current official call taken from the archived originals under `skills-work/corpus/security/raw/`; the ethics and open-science requirements re-read from that call rather than carried over; and only then a budget report.
**Failure criterion.** Any budget or ethics statement produced without a snapshot, or a template swap that alters the official class file.

**Scoring.** Adversary precision (the statement is explicit and locatable, wherever it sits), condensation-gate compliance reported with counts taken from the family copy, expansion-gate compliance with named constituents, the four USENIX slots applied explicitly, a dated policy snapshot, and absence of fabricated content. A run that answers a gate with a verdict adjective instead of a count does not pass that gate.
