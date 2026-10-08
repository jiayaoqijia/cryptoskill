---
name: review-swallowed-exceptions
description: Use when a diff adds error handling that discards the error. Flags bare catches, empty error blocks, and log-and-continue paths that turn a failure into silence.
---

# Review swallowed exceptions

An exception that is caught and dropped converts a loud failure into a quiet one. The bug still happens; now nothing reports it, and the data is half-written.

## Procedure

1. Sweep the added lines for the pattern: `gh pr diff 482 | grep -nE '^\+.*(except\s*:|catch\s*\(e\)\s*\{\s*\}|catch\s*\(_|_\s*=\s*err|\.catch\(\)|if err != nil \{\s*\})'`.
2. Classify each catch by what it does with the error:
   - re-raise or wrap with context — good,
   - return a default and log at warn/error — acceptable if the default is documented,
   - `pass` / `{}` / `return nil` with no log — blocking.
3. For a `pass`, require one of: re-raise, a logged `error` with the operation and key, or a comment explaining why the error is provably impossible.
4. Check the logger, if present, records enough to debug: the operation, the identifier, and the error value. `log.warn("failed")` without the cause is nearly as bad as silence.
5. Look for a swallowed error inside a loop or transaction where partial success leaves inconsistent state — those need an explicit rollback or a dead-letter record.
6. Distinguish a genuinely expected condition (a `FileNotFoundError` guarding an optional config) from an unexpected one; only the first may be silently handled, and it must be narrow, not a bare `except`.
7. Confirm at least one test forces the error path, so the swallow is behaviour someone chose.

## Pitfalls

- `except Exception: pass` around a network call, so timeouts look like empty results.
- Catching to keep a batch job running but losing the failed record with no retry queue.
- Logging at `debug`, which is off in production, so the error is invisible exactly when it matters.
- Swallowing the error in cleanup code, hiding a failure that corrupts the next run.

## Verification

    gh pr diff 482 | grep -nE '^\+.*(except\s*:|catch\s*\(e\)\s*\{|\.catch\(\)|_\s*=\s*err)'
    # Every match must re-raise, log with context, or carry a why-impossible comment.

Report each swallowed-error site, what it does instead of propagating, and whether a test exercises that path.

## Worked example

Added code:
    try:
        resp = client.post(url)
    except Exception:
        pass
A timeout now looks like "no result", and the caller persists a zero row. The fix catches the specific `httpx.TimeoutException`, logs the url and elapsed time at `error`, and returns a 503 so the caller does not write a fake success.
