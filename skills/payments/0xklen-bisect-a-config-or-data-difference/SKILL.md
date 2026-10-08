---
name: bisect-a-config-or-data-difference
description: Use when two runs of the same code disagree and the difference is in configuration, feature flags, or input rows. Binary-searches the config keys or data records to the one that flips the outcome.
---

# Bisect a Config or Data Difference

Code unchanged, results different: the variable is data. Treat the config map or the input rows like a commit range and halve it until one key or row is responsible.

## Procedure

1. Dump both sides to files so they can be diffed and replayed: failing `curl localhost:8080/config > cfg-bad.json`, working baseline `> cfg-good.json`.
2. Filter to keys that actually differ: `jq -S . cfg-good.json > a && jq -S . cfg-bad.json > b && diff a b`.
3. If the diff is small (under ~5 keys), test each directly. Otherwise bisect: apply the first half of bad's values onto good's config, run, note pass/fail.
4. Halve again on the half that flipped the outcome, using `git diff`-style apply of the candidate keys. Each run must change only the keys under test, nothing else.
5. When one key flips it, test plausible values of that key rather than just the two: `for v in 0 1 100 true false; do ...`.
6. For data rows, sort deterministically, then bisect the row set: `head -n <half>` plus `tail -n <rest>`. Keep the failing subset, discard the clean half.
7. For feature flags, check the *interaction*: two flags that are individually safe may combine. If no single key flips, test pairs.
8. Record the deciding key and its offending value in the bug note; write a test that pins it.

## Pitfalls

- Diffing raw JSON without sorting keys, so every line looks different and the real delta is buried.
- Applying a whole "bad" config at once and concluding "the config", never naming the key.
- Overlooking nested or inherited defaults: the key is absent in one config and defaulted silently.
- Assuming the config file is the effective config — env vars, CLI flags, or a remote config service may override it (see `capture-effective-runtime-config`).
- Bisecting data that is not deterministically ordered, so the split is different each run.
- Chasing a whitespace or type difference (`"false"` vs `false`) as if it were semantic without checking how it is parsed.

## Verification

    jq -S . cfg-good.json > a; jq -S . cfg-bad.json > b; diff a b
    # names the differing keys; the deciding one is candidate

    ./run.sh --config <good+the-one-key>; echo "exit=$?"
    # passes when injecting just that key into the good config reproduces the failure

Report to the user: the single key or row that decides the outcome, its two values, and the value of every override source for that key.
