---
name: shrink-a-repro-by-delta-debugging
description: Use when a failing input, request log, or config is too large to reason about. Reduces it automatically to the smallest subset that still triggers the failure.
---

# Shrink a Repro by Delta Debugging

A 5,000-line log that fails is a haystack, not a repro. Delta debugging removes pieces and keeps the runs that still fail, converging on one minimal cause you can read.

## Procedure

1. Write a predicate that returns True when the bug is present, taking the candidate data as its only input: `test(candidate) -> bool`.
2. Confirm the predicate is currently True on the full input and *fast* — the algorithm may call it hundreds of times. Cache setup.
3. Confirm the predicate is False on empty input. If empty already fails, the bug is in the harness, not the payload.
4. Run ddmin (or `hypothesis.extra.ghostwriter` style shrinkers for structured data; `creduce`/`cvise` for C and similar).
5. Save the shrunk artefact plus the exact predicate under `repro/` so the reduction is reproducible.
6. Re-read the minimal case by eye; the goal is a cause small enough to inspect, not merely small.
7. Re-run the predicate on the minimal case three times to confirm determinism.

## Pitfalls

- A predicate with side effects (writes a file, advances a cursor) that corrupts state between calls, so reduction reports a false minimum.
- Shrinking past meaning: removing the field that is the actual cause because the predicate happened to still pass for the wrong reason.
- Not caching expensive setup, so a 2-hour ddmin becomes a 2-day ddmin.
- Reducing the log but not the input — a minimal log with a 10 MB request body still does not fit in your head.
- Accepting the first "smaller" result without confirming the reduced case fails for the *same* exception text.

## Verification

    python3 repro/ddmin.py repro/input.json
    # prints the minimal case; confirm the byte count dropped and exit code is still non-zero

    diff <(python3 -c "print(open('repro/input.json').read())") /dev/null >/dev/null
    sha256sum repro/minimal.json && wc -c repro/minimal.json

Report to the user: original size, minimal size, the predicate command, and the single line in the minimal case that carries the cause.

```

Shrinker to adapt:

```python
def ddmin(data, test):
    n = 2
    while len(data) >= 2:
        chunks = [data[i::n] for i in range(n)]
        for c in chunks:                      # try each chunk alone
            if test(list(c)):
                data, n = list(c), max(n - 1, 2)
                break
        else:
            for c in chunks[:-1]:             # try dropping each chunk
                rest = [x for x in data if x not in set(c)]
                if test(rest):
                    data, n = rest, max(n - 1, 2)
                    break
            else:
                if n >= len(data):
                    break
                n = min(len(data), 2 * n)
    return data
```
