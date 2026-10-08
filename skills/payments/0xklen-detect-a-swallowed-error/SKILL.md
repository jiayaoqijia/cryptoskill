---
name: detect-a-swallowed-error
description: Use when something fails silently — a job reports success but did nothing. Hunts the best-effort catch, ignored return value, or log-and-continue path that consumed the error.
---

# Detect a Swallowed Error

Silent failures are the opposite of crashes: the process is green and the work is missing. The bug is a place that caught or ignored an error and kept going. Find it by making the missing failure loud.

## Procedure

1. State the observable: "report_job exited 0 but zero rows were written." Pair it with a measurement — table count before and after.
2. Search for the swallowing constructs: `grep -rnE 'except.*:\s*pass|catch\s*\(\s*\)|\.catch\(\s*\)\s*;|_ = ' src/` and `grep -rn 'errors="ignore"\|ignore_errors=True' src/`.
3. Look for log-and-continue: a `logger.warning(...)` right before a `continue`/`return None` that the caller never inspects.
4. Check the return value chain: does the caller check the boolean/None the callee returns? `grep -rn 'if .*result()' ` and read whether failure is distinguishable from empty.
5. Make the swallow loud temporarily: replace `pass` with `raise` and re-run the failing case; the traceback names the exact swallowed failure.
6. Inspect the exit code path: a shell script missing `set -e`, a pipeline without `pipefail`, or a subshell whose failure is never propagated.
7. Check `try/except Exception` blocks that also catch `KeyboardInterrupt`/`SystemExit` (should be `BaseException`-scoped), masking real aborts.
8. Fix by making the error propagate or by checking and acting on the return value; keep the loud path.

## Pitfalls

- A bare `except: pass` that is intentional but hides a regression when the swallowed branch changes.
- `errors="ignore"` in a decode path corrupting data where a strict decode would have surfaced the bad byte.
- Fire-and-forget async tasks: an unawaited promise whose rejection is never handled.
- A supervisor that restarts the failing job, so "success" is the restart loop, not the work.
- Metrics that count attempts, not completions, so failure looks like throughput.
- Fixing the visible data gap by rerunning, without proving why the first run went quiet.

## Verification

    grep -rnE 'except[^:]*:\s*$|except[^:]*:\s*pass' src/ | head
    # lists candidate silence sites; each is a place to raise or log-and-fail

    BEFORE=$(psql -tAc 'select count(*) from out'); ./report_job.sh; echo "job exit=$?"
    AFTER=$(psql -tAc 'select count(*) from out'); echo "rows $BEFORE -> $AFTER"
    # passes when the job exits non-zero on failure OR rows actually increased

Report to the user: the construct that swallowed the error (file:line), the hidden exception, and the exit code the job had been reporting.
