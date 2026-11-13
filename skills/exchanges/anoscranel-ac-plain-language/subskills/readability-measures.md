---
name: readability-measures
domain: writing/readability-measures
trigger: "\"is this readable\", \"what grade level is this\", \"run a readability score\", \"test this with readers\"."
anti_trigger: "Applying plain-language principles while writing (subskills/plain-language.md); tools that claim to judge tone or authorship."
scope: "When formulas help or mislead; user testing of text"
status: "seedling"
---

# Readability measures

## Standard

- **What the formulas count.** Flesch Reading Ease = 206.835 − 1.015(words/sentence) − 84.6(syllables/word); Flesch-Kincaid inverts it into a US grade.
 Gunning Fog counts polysyllables. SMOG counts them in three 10-sentence samples.
 Dale-Chall alone consults a word list — tokens outside a 3,000-word familiar list — so it alone measures familiarity, not length (<https://arxiv.org/abs/2301.02975>; https://arxiv.org/abs/2301.02975).
- **The scores partly measure the topic.** Under a topic model, Flesch scores converge almost surely to functions of the document's topic distribution (Ehara, https://arxiv.org/abs/2608.23327). A topic vector from one half predicts the other half's grade level at r = 0.779 (Brown) and 0.884 (written BNC). It adds only R² = 0.002, CI spanning zero. ⚠️ Single study, unreplicated; the author declines to read it as a claim about human readability.
- **Issuers reject their own instrument.** CDC: "Readability formulas are inadequate to assess communication effectiveness. These formulas are a mechanical 'count' of syllables and sentences; they don't consider audience, purpose, or the majority of communication characteristics that contribute to clarity and comprehension" (https://www.cdc.gov/ccindex/tool/index-different.html).
- **Validity hierarchy** (<https://blog.iclr.cc/2025/11/19>): Flesch/Fog/SMOG valid as relative surface complexity inside one corpus, invalid for comprehension or cross-topic comparison. Dale-Chall valid against its school list, invalid for experts. Readability-machine-learning reached 0.631 Spearman with human ratings — on code, not prose. Linters (Vale, alex, textlint) are valid because they publish the rule they enforce.
- **Target ranges, rules of thumb** (⚠️ conventions, not measured optima): general public grade level ≤8, ease ≥60; educated generalists grade ~10–12; expert peers keep their terms, sentences 15–25 words.

## Decision rules

1. Use a score only inside one corpus and one audience. Never compare scores across topics.
2. A high score never means the text is understood. Reader testing decides comprehension.
3. Machine optimisation of a grade level can destroy accuracy. Verify with readers after any automated cut.
4. Never use an authorship detector as evidence of anything (F1 from <0.55 to 0.80 across domains).

## Procedure

1. Baseline the current text. Record the instrument, its version, the audience and the topic.
2. Revise for the audience, not for the number (subskills/plain-language.md).
3. Re-score. A change of 2–3 points is noise; 10 points means vocabulary or sentences moved.
4. Run the reader test: 5–8 readers from the actual audience, one task each, comprehension questions, no help.
5. Record what readers could not find, answer, or did wrong. That list drives the next revision.
6. Record both results in the document record: the score and the test outcome.

## Anti-patterns

- Optimising the score and shipping the text.
- Comparing a legal text's score against a marketing page's score.
- Treating a detector output as proof of authorship.
- Skipping reader testing because the score improved.

## Done checklist

- [ ] Baseline recorded with instrument, audience and topic.
- [ ] Score change interpreted inside one corpus.
- [ ] Reader test run with 5–8 actual readers.
- [ ] Failure list recorded and acted on.
- [ ] No authorship detector used as evidence.
- [ ] Automation limited to named, checkable rules.

## Sources

- <https://arxiv.org/abs/2301.02975>
- <https://arxiv.org/abs/2301.02975>
- https://arxiv.org/abs/2608.23327 · https://www.cdc.gov/ccindex/tool/index-different.html · https://www.ahrq.gov/talkingquality/resources/writing/tip6.html
