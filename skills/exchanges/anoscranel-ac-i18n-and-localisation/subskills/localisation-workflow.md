---
name: localisation-workflow
domain: software-engineering/localisation-workflow
trigger: "Running the process that keeps translations in step with the source."
anti_trigger: "Not for translation quality judgement, and not for copywriting."
scope: "Key stability, translation memory, review, and keeping pace with source."
status: seedling
---

# Localisation workflow

## Standard

A translation is a derived artefact, and it drifts from its source the moment the source changes. The workflow exists to control that drift: keys are extracted automatically, changes are detected by diff rather than by memory, translations are matched through a translation memory so unchanged strings cost nothing, and a review step catches the cases where the machine or the memory produced something wrong.

The failure mode is silent staleness. A string changes in English, the key stays the same, and the old translation continues to display — correctly formatted, grammatically fine, and wrong. Detecting it requires comparing the source's state at translation time with its current state, which means the workflow must record that state rather than assume it.

Primary sources: <https://www.gala-global.org/> and <https://www.w3.org/International/>.

## Decision rules

- Record the extraction mechanism and whether it runs in continuous integration.
- Record the translation memory and how fuzzy matches are accepted.
- Record the review step and who performs it, by locale.
- Record the staleness detection: how a changed source is marked for re-translation.
- Record the release gate: whether incomplete locales block a release or ship with fallback.
- Record the ownership of each locale and the escalation path for a bad translation.

## Procedure

1. Record the extraction pipeline and its trigger.
2. Record the memory and the fuzzy-match threshold.
3. Record the review assignment per locale.
4. Implement staleness detection by comparing source state.
5. Record the release gate policy for incomplete locales.
6. Record the escalation path and test it once.

## Anti-patterns

- Extracting strings manually and hoping nothing was missed.
- Accepting fuzzy matches without review at high similarity.
- Shipping a changed source with the old translation and no marker.
- Treating a hundred percent coverage as evidence of correctness.
- Blocking every release on every locale, which encourages bypassing the gate.

## Done checklist

- [ ] Extraction pipeline recorded.
- [ ] Memory and fuzzy threshold recorded.
- [ ] Review assignment recorded per locale.
- [ ] Staleness detection recorded.
- [ ] Release gate policy recorded.
- [ ] Escalation path recorded.

The staleness problem is worth instrumenting rather than trusting: a count of source strings whose translation is older than the source change is a number that can be watched, and it moves earlier than a customer complaint. Without it, staleness is discovered in the field, where it looks like a translation error rather than a process one.


## Sources

- Localisation industry standards: <https://www.gala-global.org/>
- W3C internationalisation guidance: <https://www.w3.org/International/>
- Unicode CLDR data: <https://cldr.unicode.org/>
