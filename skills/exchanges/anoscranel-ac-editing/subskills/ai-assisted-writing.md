---
name: ai-assisted-writing
domain: writing/ai-assisted-writing
trigger: "\"disclose AI use\", \"can I use AI for this\", \"AI disclosure statement\", \"is this allowed\"."
anti_trigger: "Removing machine tells from finished text; verifying claims to sources."
scope: "Where AI may touch text, verification duty, disclosure rules by venue"
status: "seedling"
---

# AI-assisted writing

## Standard

- **AI is never an author.** ICMJE (Apr 2025): chatbots "should not be listed as authors because they cannot be responsible for the accuracy, integrity, and originality of the work"; disclose use in the cover letter and the manuscript (https://www.icmje.org/recommendations/browse/artificial-intelligence/ai-use-by-authors.html). COPE (13 Feb 2023): AI tools "cannot meet the requirements for authorship"; disclose in Methods (https://publicationethics.org/guidance/cope-position/authorship-and-ai-tools). ⚠️ The two routes disagree: ICMJE sends writing-stage use to the acknowledgements, COPE sends everything to Methods.
- **Venue tests differ, and the strictest is an originality test.** NIH NOT-OD-25-132: applications "substantially developed by AI, or contain[ing] sections substantially developed by AI" are not original ideas of applicants and "will not be considered" — disclosure does not cure it (https://grants.nih.gov/grants/guide/notice-files/NOT-OD-25-132.html). ICLR 2026 desk-rejects extensive *undisclosed* use — disclosure suffices there (https://blog.iclr.cc/2025/11/19/iclr-2026-response-to-llm-generated-papers-and-reviews). Wellcome quarantines disclosure from scoring (https://wellcome.org/grant-funding/guidance/policies-grant-conditions/use-of-generative-ai). NSF asks proposers to "indicate the extent and manner of use" (https://nsf.gov/policies/ai/merit-review).
- **EU AI Act Art. 50(4).** Deployers of a system generating text "published with the purpose of informing the public on matters of public interest shall disclose that the text has been artificially generated or manipulated" — unless it passed human review or editorial control with a named responsible person. Applies from 2 August 2026 (https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32024R1689; ⚠️ omnibus deferral details from secondaries).
- **Detection is not a gate.** False positives run 61% on non-native writing (https://pmc.ncbi.nlm.nih.gov/articles/PMC10382961) and 0–100% across 13 detectors on 135,389 human manuscripts (https://arxiv.org/abs/2608.26710).

## Decision rules

1. Read the venue's test first: originality (NIH), disclosure (ICLR), quarantined-from-scoring (Wellcome), or a retraction ground (COPE).
2. Disclose what the venue asks. The measured cost is small: a disclosure statement lowered perceived writing quality by under 0.15 points on a 7-point scale (https://arxiv.org/abs/2507.01418 ⚠️ preprint).
3. **Human-gated:** every disclosure statement, attestation or submission is prepared by the agent and made by a human.
4. Sections, claims and references stay yours. Never claim model-written substance as your own at an originality-testing venue.
5. Never fabricate a reference. Every retrieved regime punishes fabrication identically.
6. Keep drafts and version history — what a fair review weighs, not a detector.
7. EU deployers: Art. 50(4) binds public-interest text lacking human editorial control.

## Procedure

1. Get the venue's AI policy in writing before drafting. Record the test type and deadline.
2. Log every AI touch: tool, task (ideation, drafting, editing, translation), span.
3. Verify every claim the AI produced against its source span. Untraceable claims come out.
4. Draft the disclosure in the venue's shape: tool, extent, manner.
5. Where Art. 50(4) applies, mark the text at first exposure.
6. Hand the human the log, the verification record and the draft.

## Anti-patterns

- Treating disclosure as optional because detectors are unreliable.
- Claiming origination of AI-drafted substance at an originality-testing venue.
- A fabricated citation "to fill the gap".
- Uploading a confidential manuscript to a public tool.

## Done checklist

- [ ] Venue test identified and recorded.
- [ ] AI-touch log complete: tool, task, span.
- [ ] Every claim verified to a source span.
- [ ] Disclosure drafted in the venue's shape.
- [ ] Art. 50(4) checked; draft history retained.
- [ ] **Human-gated** submission by a named person.

## Sources

- <https://arxiv.org/abs/2608.26710>
- <https://grants.nih.gov/grants/guide/notice-files/NOT-OD-25-132.html>
- https://grants.nih.gov/grants/guide/notice-files/NOT-OD-25-132.html · https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32024R1689
