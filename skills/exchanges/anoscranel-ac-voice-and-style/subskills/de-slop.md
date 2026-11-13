---
name: de-slop
domain: writing/de-slop
trigger: "\"this sounds like AI\", \"de-slop this\", \"make it sound human\"."
anti_trigger: "Building a positive brand voice (subskills/voice.md); AI-use policy and disclosure."
scope: "Spotting and removing AI tells; restoring specificity and stance"
status: "seedling"
---

# De-slop

## Standard

- **The "AI tell" is a per-model fingerprint, not a word list.** In a matched-corpus study *tapestry* hit 19.8% of GPT-4o documents against 0.10% of human ones. But only 1.5% of Llama 3 70B documents used it. A list calibrated on one model misses another (https://naturalmelo.com/research/ai-vocabulary-gap ⚠️ single study).
- **The measured profile is two statistical features, not vocabulary:** mean entropy "a full standard deviation higher" than human text, lexical diversity "two standard deviations above" (https://arxiv.org/html/2608.27855). Uniform, low-surprisal prose is the tell.
- **The failure mode is broken reasoning between locally plausible parts.** SciSlop defines slop as text where "each part… looks plausible while the scientific reasoning that connects the parts breaks down" (https://arxiv.org/abs/2610.00531).
- **Repair is evidence-bound, never style-bound.** From that source: "standard revisions leave residual slop", and "direct slop-aware prompting triggers reward hacking". The fix that works guides revision "only where the experiment records support the change".
- **Detection is not an enforcement instrument.** Seven detectors misclassified 61.3% of non-native TOEFL essays on average (https://pmc.ncbi.nlm.nih.gov/articles/PMC10382961). Across 135,389 paired human manuscripts, 13 detectors produced false-positive rates of 0.0%–100% (https://arxiv.org/abs/2608.26710). A court expunged a finding built on a "100% AI" score (*In re the Application of Newby* ⚠️ one jurisdiction).

## Decision rules

1. Judge the text, not the pipeline: uniformity, missing specifics, and stance-free hedging need no tool.
2. Repair against the evidence record. A style instruction alone leaves residual slop and invites reward hacking.
3. Specificity is the test: numbers, names, dates, decisions. "De-slopped" text with the same generic content is not fixed.
4. Restore stance: hedge claims you might be wrong about, assert the rest, delete the whataboutism pair.
5. A detector score never gates publication — it points to text needing a human read.
6. Never fabricate a reference, quotation, number or case while rewriting. That failure is checkable and punished.

## Procedure

1. List the tells: uniform sentence rhythm and paragraph length; em-dash chains; filler openers ("It's important to note"); "not only… but also" stacks; both-sides hedging; generic transitions (*Furthermore*, *In conclusion*); the marked lexicon (*delve*, *tapestry*, *underscore*, *landscape*, *robust*, *leverage*).
2. Extract the claims. For each, find its supporting record — note, data, or source span.
3. Rewrite claim by claim against the record: who did what, when, with what result. Cut what the record does not support.
4. Take a stance: one position per contested claim, the strongest objection, the answer.
5. Vary sentence length. Read three paragraphs aloud; identical cadence failed.
6. Tell the human the probability, never a verdict: "probably machine-generated — three tells present, unverified".

## Anti-patterns

- Swapping *utilize* for *use* and calling it de-slop.
- A verdict ("100% AI") from a tool or your own read.
- A slop-aware prompt ("remove AI tells") as the whole fix — measured to trigger reward hacking.

## Done checklist

- [ ] Tell list matched against the text.
- [ ] Every changed claim traces to a record.
- [ ] Stance restored; hedging matches accuracy.
- [ ] Sentence rhythm varies; marked lexicon gone.
- [ ] Human warned with probability plus the tell list, not a verdict.
- [ ] No fabrication introduced.
## Sources

- <https://arxiv.org/html/2608.27855>
- <https://arxiv.org/abs/2210.15067>
- <https://gptzero.me/news/ai-accuracy-benchmarking>
- https://arxiv.org/abs/2610.00531 · https://arxiv.org/html/2608.27855 · https://arxiv.org/abs/2608.26710
- https://pmc.ncbi.nlm.nih.gov/articles/PMC10382961 · https://naturalmelo.com/research/ai-vocabulary-gap
