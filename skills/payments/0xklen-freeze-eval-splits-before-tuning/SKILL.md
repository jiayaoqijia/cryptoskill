---
name: freeze-eval-splits-before-tuning
description: Use when an eval set is also used to choose prompts, thresholds, or hyperparameters. Locks a held-out split and its hash so tuning cannot leak into the reported number.
---

# Freeze Eval Splits Before Tuning

The moment you tune on the set you report on, the number stops being an estimate. Make the split immutable and its hash public before the first experiment.

## Procedure

1. Split once: dev for iterating, test for the final number. Allocate by a fixed rule (hash of item id mod 10), not by eye.
2. Hash the test file and store the digest; any change to the test set invalidates every prior comparison.
   ```bash
   shasum -a 256 tests/heldout.jsonl | tee tests/heldout.sha256
   ```
3. Load the test set behind a read guard so tuning jobs cannot open it:
   ```python
   def load_test(path):
       assert os.environ.get("EVAL_ALLOW_TEST") == "1", "test set is frozen"
       return read_jsonl(path)
   ```
4. Version the split with the code: commit the dev/test manifest, not just the files.
5. Log every tuning run's score on dev. If the report quotes a dev number, label it dev.
6. When you must re-split (the corpus changed), re-freeze and re-run the baseline on the new test set before comparing anything.
7. Keep a small hidden set nobody looks at until ship day, to guard against the team overfitting the visible test set.

```bash
git log --oneline -- tests/heldout.sha256   # digest changes only on a deliberate re-freeze
```

## Pitfalls

- "Just one quick look" at the test set, repeated, is tuning — the number inflates by several points.
- Copying the test set into a notebook directory puts it back in the tuning path.
- A test split sharing near-duplicate items with dev is effectively the dev set; dedup before splitting.
- Re-freezing after each model change turns the test set back into a dev set.
- Reporting the best of many test runs is a max statistic, not an estimate.

## Verification

    shasum -a 256 -c tests/heldout.sha256   # must print OK; digest unchanged since freeze

Report: "Held-out test frozen at sha256 3f9c…, 512 items, untouched across 23 dev iterations; the final number was reported once on the frozen set."
