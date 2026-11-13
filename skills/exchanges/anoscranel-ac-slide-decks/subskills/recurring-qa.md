---
name: recurring-qa
domain: writing/slide-decks
trigger: "make a template for our weekly report deck; name and version these deck files; final check before sending the deck"
anti_trigger: "Restructuring the story (subskills/narrative-spine.md); accessibility checks on the exported file (subskills/accessibility.md)"
scope: "Naming and versioning, recurring-report templates, and the pre-send checklist"
status: seedling
---

# Recurring QA

## Standard

- **Fixed-position dates**: every filename carries an ISO date in the same position, so a same-owner, same-topic series sorts chronologically. <https://www.rfc-editor.org/rfc/rfc3339> for the date-time format.
- **Version discipline**: drafts numbered and the sent copy carries date and state, never the word "final". ⚠️ practitioner convention; no public standard exists.
- **Template as claim skeleton**: a recurring-report template locks structure, not decoration: fixed sections, headline slots worded as claims the decider needs, and one tagged appendix. ⚠️ practitioner convention.
- **The three pre-send tests**: title test, skim test, crash test. ⚠️ practitioner checklist naming, assembled from Duarte's glanceability and Alley's skim reading: <https://www.duarte.com/slideology/>, <https://link.springer.com/book/10.1007/978-1-4419-8279-7>

## Decision rules

1. If a deck recurs weekly or monthly, build the template before the second edition.
2. Filenames follow one pattern pack-wide: owner, topic, date, state. Example: `growth-weekly_2026-10-26_sent.pdf`.
3. The draft counter resets only after a send event. Internal revisions increment it.
4. Template headline slots are placeholders for a claim, worded as the answer the decider needs. Each edition replaces the slot with a statement, never a topic label and never a question.
5. Distribution formats share one base filename. The PDF sent and the source kept.
6. The title test: filename plus slide-one title together state what the deck decides.

## Procedure

1. Write the naming pattern into the template footer note so nobody improvises it.
2. Lock the template: fixed sections, claim-slot headlines, tagged appendix.
3. Run the title test: the slide-one title states the takeaway, not the topic.
4. Run the skim test: a headlines-only read reproduces the argument.
5. Run the crash test: open the exported file on a second machine. Fonts render, charts intact, the file opens in the recipient's likely viewer.
6. Archive every sent copy with its date-and-state name. Never overwrite a sent copy.
7. Log template edits in one line inside the template, so the next editor sees what changed.

## Anti-patterns

- `final_v2_FINAL(2).pptx`. Fix: date plus state, one pattern.
- Last edition's numbers still sitting in a deep appendix. Fix: the template audit before every send.
- A "quick edit" sent with a stale version in the attachment. Fix: send-a-new-name rule.
- Skipping the crash test. Fix: no send without it.
- A template that bakes in one edition's storyline. Fix: slots hold claims, not one edition's answers.
- Sent copies overwritten by later drafts. Fix: append the version, keep the archive.

## Done checklist

- [ ] Every file carries the date in the fixed position and a state suffix.
- [ ] A template exists from the second edition onward.
- [ ] Title test passed.
- [ ] Skim test passed.
- [ ] Crash test passed on a second machine.
- [ ] The sent copy is archived, untouched by later drafts.

## Sources

- RFC 3339, date and time format: <https://www.rfc-editor.org/rfc/rfc3339>
- Duarte, *Slide:ology*: <https://www.duarte.com/slideology/>
- Alley, *The Craft of Scientific Presentations*: <https://link.springer.com/book/10.1007/978-1-4419-8279-7>
- Berinato, *Good Charts* (consistency in recurring reporting): <https://store.hbr.org/product/good-charts-the-hbr-guide-to-making-smarter-more-persuasive-data-visualizations/15005>
