---
name: shrink-a-fuzz-crash-to-a-minimal-repro
description: Use when a fuzzer or property test found a crashing input — shrink it to the smallest reproducing case and freeze that as a regression test before writing the fix.
---

# Shrink a fuzz crash to a minimal repro

A fuzzer hands you a pile of bytes and a stack trace. Minimize the input to the smallest case that still fails, freeze it as a test, then fix — so the fix is provably about the bug, not the noise.

## Procedure

1. Save the raw crashing input before touching anything:
```
cp /tmp/fuzz-crash-abc123 /tmp/crash.raw
```
2. Shrink with the fuzzer's minimizer. libFuzzer: `./fuzz_target -minimize_crash=1 /tmp/crash.raw`. AFL++: `afl-tmin -i /tmp/crash.raw -o /tmp/crash.min -- ./target @@`. Go writes an already-minimized case under `testdata/fuzz/FuzzParse/<hash>`.
3. Verify the minimized input still crashes and read the failure type (assert, segfault, timeout, OOM). A shrunk input that fails for a different reason means the minimizer drifted — discard it.
4. Reduce further by hand if the minimizer stalls: delete byte blocks and re-run. Keep the input valid enough to reach the parser, so you are not just testing the reject path.
5. Convert the input into a self-contained regression test — inline bytes, not a path into the fuzzer corpus:
```python
def test_rejects_truncated_ndjson():
    with pytest.raises(ValueError):
        parse_ndjson(b'{"a":1}\n{"a":')       # minimized 16-byte input
```
6. Confirm it fails before the fix: run it against the unfixed commit and see red.
7. Commit the corpus directory (`testdata/fuzz/`, `corpus/`) so CI re-runs every discovered crash each build.

## Pitfalls

- Minimizing against a build that differs from the crashing one can lose the bug. Rebuild the same commit and flags.
- A timeout crash shrunk into a hang: cap wall clock (`timeout 5s`) so the regression test cannot stall CI.
- Committing the raw multi-megabyte fuzz input bloats the repo. Commit only the minimized case.
- Fixing before freezing the repro lets the fix silently over-fit. Freeze the test and watch it go green.

## Verification

```
git stash && pytest -q tests/test_rejects_truncated_ndjson.py; git stash pop && pytest -q tests/test_rejects_truncated_ndjson.py
```
Passes = red on the unfixed tree, green after the fix, same test. Report: "shrunk a 4 KB crash to 16 bytes, froze as test_rejects_truncated_ndjson (red before fix, green after), corpus committed."
