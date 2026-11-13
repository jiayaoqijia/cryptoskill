---
name: academic-papers
domain: writing/academic-papers
trigger: "\"structure this paper\", \"IMRaD\", \"thesis chapter\", \"pick a reporting guideline\", \"respond to reviewers\"."
anti_trigger: "A synthesis of others' studies (subskills/literature-review.md); the claim-evidence grammar; disclosure policy by venue."
scope: "IMRaD papers, theses, reporting guidelines, submission and reviewer response"
status: "seedling"
---

# Academic papers

## Standard

- **Protect the submission from the desk-reject bucket first.** Average desk rejection is about 40%; >90% of editors endorse rejecting for scope mismatch (<https://sciencedirect.com/science/article/pii/S1049096521000573>). P(ever accepted | first-round minor revision) is 98.3%, and 84.7% after major revision.
- **IMRaD is the spine; the reporting guideline is the checklist.** EQUATOR holds 706 records; CONSORT is 2025, SPIRIT 2025 (34 items), STROBE (22), ARRIVE 2.0, COREQ (32), SRQR (21). ⚠️ Source not cited inline; check the Sources list before relying on this figure.
- **A submitted checklist is not compliance.** In the IICARus trial, 0 of 762 manuscripts achieved full ARRIVE compliance and the median rose only 36.8% → 39.5%. The intervention that works is editor-side expert checking. ⚠️ Source not cited inline; check the Sources list before relying on this figure.
- **The agent flags; the human signs.** An agent may select the guideline and locate each item. It reports each one `missing`, `present`, `unverifiable` or `inconsistent`, with a page reference. It may never emit "compliant".
- **Citations resolve before the bibliography is written.** 20–50% of AI-generated citations are fabricated (<https://arxiv.org/pdf/2607.22693>). Resolve every reference against Crossref, OpenAlex or the DOI resolver, then spot-check unflagged ones.
- **The response letter concedes in shape, not in fact.** Only 6% of letters fully accommodate every suggestion. The default is agree-and-hedge, and tone is the top failure mode with no detector. ⚠️ Source not cited inline; check the Sources list before relying on this figure.

## Decision rules

1. Check scope fit against the journal's aims and recent contents before drafting — a boolean attribute, not a judgement.
2. Select the guideline by design and discipline and record the version; where none covers the genre, say so rather than invent a rubric.
3. Run presence checks (numbers, effect size with interval, registration, funding, conflicts, data availability) and consistency checks (n's agree across abstract, body and tables).
4. Draft the rebuttal as: comment quoted verbatim and numbered, change described with its location, concession call flagged.
5. In a thesis, the advisor signs the outline before chapter one.
6. Disclosure follows the venue; ICMJE bars chatbots from authorship.

## Procedure

1. Confirm scope fit; pick the guideline and version.
2. Outline section by section; draft each section against the outline.
3. Draft methods and results first, the introduction last.
4. Resolve every reference against a resolver; keep the log.
5. Run presence and consistency checks; report each item with a page reference.
6. Build the packet: required statements, cover letter, checklist, disclosure.
7. Map every comment to a location, restate the change, flag declined items.
8. Hand the human the draft, check log and flag list. **The human submits.**

## Anti-patterns

- Ticking checklist items the manuscript does not contain.
- Submitting to a journal whose recent contents miss the topic.
- A bibliography assembled from model recall.
- Rebuttal padding that admits more than the comment implies.

## Done checklist

- [ ] Scope fit confirmed against aims and recent contents.
- [ ] Guideline and version recorded; absences stated.
- [ ] Presence and consistency checks reported by page reference.
- [ ] Every reference resolved and logged.
- [ ] Required statements complete, including disclosure.
- [ ] Declined items flagged; tone left to a human reader.
- [ ] **Human-gated:** submitted by a named person.

## Sources

- <https://sciencedirect.com/science/article/pii/S1049096521000573>
- <https://www.equator-network.org/reporting-guidelines/>
- <https://arxiv.org/pdf/2607.22693>
