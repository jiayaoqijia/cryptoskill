# Evaluation Scenarios

Test specifications for independent evaluation. Each scenario states its **input**, the **expected output**, and the **failure criterion** that makes the run count as failed. Independent runs are not claimed here; a scenario is a specification, not a result.

The scenarios are ordered so that the two reported defect classes are each tested twice: once on a realistic draft and once on the frozen calibration manuscript whose numbers are already published in the contract. A scenario that passes only on synthetic input has not been tested.

## Scenario 1 — Wordy abstract whose allocation is wrong

**Input.** A draft with a 247-word abstract in four paragraphs. Paragraph 1 describes the construction in one sentence; paragraphs 2 to 4 report proved bounds, a conditional theorem, and an open problem. The contribution list is 902 words in six bullets and shares 30 six-grams with the abstract.

**Expected output.** The diagnosis table reports the abstract's total words, its per-paragraph `context`/`gap`/`build`/`result` labels, its build share, and its longest sentence, each against the bound the instrument prints for that axis. The compression pass reports every breach by naming the gate and the two numbers it printed (the draft's value and the bound), on the length, allocation, contribution-block and duplication axes alike. The migration ledger gives a destination for every removed span, and no destination is "deleted" except with the reason recorded.

**Failure criterion.** Reported as acceptable, or reported with word counts but no build share, or with the allocation breach missing. A run that says only "abstract too long, trim it" fails even though the length finding is correct.

## Scenario 2 — Thin technical overview that reads complete

**Input.** A draft whose technical overview is 288 words in 8 source lines, making up about 0.14 of the introduction's words, with no named sub-blocks, no statement of a failed first attempt, and no pointer to the formal statement. The author reports it as "an intuitive sketch, complete for a reader who knows the area".

**Expected output.** The expansion pass reports the overview's words, lines, and share of the introduction against the floors gate `overview` prints, and names each absent mandatory constituent. It does not require the overview to live under a particular heading, and it records which of the three corpus placement forms was used and the `file:line` span.

**Failure criterion.** Reported as adequate; or reported as thin with a recommendation to "expand it" without naming which constituents are absent; or a run that fails the draft solely because there is no section titled "Technical Overview", since only 29% of corpus papers have one.

## Scenario 3 — Thin construction next to an over-thick analysis

**Input.** A draft whose construction section is 1040 words and whose largest analysis subsection is 2762 words and 65% of its parent section. The construction has a variant list, a masking-layer description, a design-condition table, and a non-claims paragraph, but no worked parameter instance and no per-round algorithm box. **Both the construction section and the analysis section carry direct prose of their own, so the `direct` basis is not degenerate for either** — every section whose `direct` count enters the ratio, numerator and denominator alike, returns `measured`, and the ratio is therefore reported as a real band verdict. The largest analysis subsection sits under a parent that also has direct prose, so the ceiling pass compares hierarchical child and parent counts and returns `measured` rather than `degenerate`.

**Expected output.** The construction constituent checklist reports which of the five required items are present, with the parameter list, the step ordering, and the correctness statement each marked. The ratio is printed in words on the `direct` basis, with its band named as the gate printed it (the two boundary VALUES are not in the gate's output; read them from `--constants`), and the basis named. The relocation pass reports the largest-child share against the majority ceiling and produces a relocation ledger that carries every claim, status label, and number.

**Failure criterion.** A verdict of "thin" with no named missing constituent; a ratio printed with no basis; a recommendation to delete any claim or status label rather than relocate it; or a rule of the form "the construction must be longer than the analysis", which the corpus does not support.

## Scenario 4 — Measured values leaking into a theory section while the construction is expanded

**Input.** A construction section being expanded, into which the author has added the paper's measured table sizes, a measured margin in bits, and two measured band boundaries, each as a decimal literal.

**Expected output.** The numeric-placement pass lists each concrete literal with its `file:line` and region, and requires a filed reason of one of the five classes (analytic not measured; design-point or defining arithmetic; symbolic scale; superseded and retained once; stated paper target). Hits without a filed reason are findings. Each relocated value keeps its digits exactly, travels with its provenance, and leaves a pointer behind. The pass reports that no value is present in neither region.

**Failure criterion.** Reported as fine because "the numbers are needed for the argument"; or a relocation that rounds a value, drops its provenance, or deletes it; or a scan that reports a hit count without the region boundaries it used.

## Scenario 5 — Correct length, wrong everywhere else

**Input.** A draft that satisfies every word cap — 208-word abstract, 140-word contribution list in 4 bullets each at or under the per-item cap (`corpus/crypto/statistics.md:198`, n=214) — but whose abstract gives the construction one sentence and spends the rest on analysis, whose overview is 300 words, and whose contribution list reproduces the abstract's framing in different words.

**Expected output.** The pass reports the caps as satisfied **and** reports the allocation breach (build share below the floor gate `abstract-build-share` prints), the overview breach (below the floors gate `overview` prints), and the duplication breach on the 6-gram metric if any span survives paraphrase. The overall verdict is not "within budget".

**Failure criterion.** A verdict of `within budget` or "caps met", on the strength of the word counts alone. This is the scenario that tests whether the skill can catch the reported defect rather than a length symptom of it.

## Scenario 6 — Calibration on the frozen manuscript

**Input.** The frozen calibration manuscript, specified only by its path, with the task "tell me whether it is thin where it must be deep and wordy where it must be tight".

**Expected output.** The diagnosis reproduces the contract's published measurements: the abstract at 247 words with build share 0.33 and the contribution list at 902 words with a 3.65 block/abstract ratio and 30 shared 6-grams; the overview at 288 words, below the corpus minimum gate `overview` prints (its n and row are on that gate's output); the construction-to-analysis ratios 0.9524 on tex lines, 1.3120 on md lines, and 1.1243 on md words, each with its basis named; and the largest-child share 0.5659 for the analysis subsection. It names at least four of the five absent overview constituents and at least two relocatable ledger classes present in the over-thick subsection.

**Failure criterion.** Numbers that do not match the contract's on the same basis; any ratio reported without its basis; a report of "balanced" for the over-thick subsection; or a recommendation to delete a claim. A run that produces no numbers at all fails, and so does one that produces numbers matching on a different basis without saying so.

## Scenario 7 — Venue rules that may have changed

**Input.** A request to format a draft for a named venue, with the submitter asserting a remembered page limit and template.

**Expected output.** The skill fetches the venue's current official call, records a dated snapshot with its source, checks the page limit, template, anonymity, ethics, AI-disclosure, and artifact requirements against that snapshot, and reports any difference from the remembered value explicitly. No format claim is made from memory.

**Failure criterion.** A page limit or template asserted without a fetched snapshot and a date; or a format pass run before the anonymity check.

## Scoring

A run is scored on: diagnosis-before-rewrite (the diagnosis table exists and carries numbers), allocation discipline (build share and block/abstract ratio reported, not only totals), expansion substance (floors cleared and absent constituents named), basis discipline (every ratio and budget names its twin, unit, and basis), preservation (no claim, status label, number, or provenance lost in any relocation), and absence of fabricated content (every threshold traceable to a `file:line`, no invented citation, number, or review outcome).
