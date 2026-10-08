---
name: detect-eval-set-contamination
description: Use when an eval or benchmark score looks too good, or a test set predates a model's training cutoff. Measures prompt and answer overlap with the training corpus.
---

# Detect Eval-Set Contamination

A model that has seen the test items scores on memory, not ability. Contamination is the default state for any public eval older than the training cutoff, so measure it rather than assume it away.

## Procedure

1. Pin the eval's release date and the model's training cutoff. Any public split published before the cutoff is presumed contaminated until shown otherwise.
2. Measure n-gram containment: for each item, compute the longest shared word run with the nearest corpus document. A 13-gram match is the standard memorisation signal.
   ```python
   def has_match(item, docs, n=13):
       words = item.split()
       grams = set(tuple(words[i:i+n]) for i in range(len(words)-n+1))
       return any(grams & set(tuple(d.split()[i:i+n]) for i in range(len(d.split())-n+1)) for d in docs)
   ```
3. Do it on answers, not just questions. Multiple-choice items contaminate through the option text and label order, not only the stem.
4. Check paraphrase leakage: a model may not recall the exact string but a close variant. Use MinHash near-duplicate detection with a Jaccard threshold of 0.8.
5. Run the canary test: prepend a random GUID to each item, ask the model to complete the prefix, and see whether it reproduces the gold answer.
6. Compare contaminated vs clean subsets when you can segment them (e.g. by publication date). The gap is the contamination effect size.
7. Report contamination as a number — percent of items with a >=13-gram match — not a yes/no.

```bash
python3 tools/contaminate.py --eval mmlu.jsonl --corpus pile/*.txt --ngram 13 > contam.tsv
```

## Pitfalls

- Checking only the question stem misses answer-side and option-order leakage.
- A web-crawled corpus changes under you; record the corpus snapshot hash next to the score.
- Substring search is not enough — tokenisation differences (whitespace, unicode) hide exact matches.
- A held-out set you authored after the model's release is clean only if it was never published or used in any fine-tune.
- Assuming a "private" eval is clean misses a downstream fine-tune; check the training data card.

## Verification

    wc -l contam.tsv   # count flagged items; divide by total items for the contamination rate

Report: "12% of the eval set has a >=13-gram match with the pretraining corpus; the model's 94% drops to 79% on the uncontaminated subset — treat the headline as inflated."
