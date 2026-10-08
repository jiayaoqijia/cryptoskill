---
name: scrub-pii-from-structured-logs
description: Use when application logs, request lines, or debug output may carry emails, ids, or tokens. Redact at the emit site and verify with a canary through the real sink.
---

# Scrub PII from structured logs

Logs are the most common uncontrolled copy of personal data. This skill keeps them useful while removing identifiers at the emit site, before anything is stored.

## Procedure

1. Enumerate every sink: stdout, files, syslog, the aggregator (Loki/Elastic), and any error forwarder. Each sink is an independent copy.

2. Define an allowlist of loggable fields per event, not a denylist. Unknown fields are dropped, never passed through.

3. Redact at emit, not in the pipeline: once the line reaches a transport it is already stored and replicated.

4. Mask rather than drop where operators need to correlate: `u***@domain.com`, card as `************4242`, keeping only the last four.

5. Use a keyed hash as a join key: `user_ref = sha256(user_id + pepper)[:16]` so the same user correlates across lines without the raw id appearing.

6. Install the filter at the logger:
   ```python
   class PIIFilter(logging.Filter):
       PAT = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
       def filter(self, record):
           record.msg = self.PAT.sub("[email]", str(record.msg)); return True
   ```

7. Scrub exception args and traceback locals, not just the message; request bodies appear inside tracebacks.

8. Set and enforce a retention window on the log store, 30 days typical, and confirm the store actually expires lines.

9. Ship a canary: log a synthetic email in a test environment and grep the index to confirm it is absent.

## Pitfalls

- URLs carry PII in query strings (`?email=`); scrub the request line and query before logging it.
- `repr()` of a dataclass dumps every field; log selected fields explicitly one at a time.
- Debug logging left on in production bypasses the filter; assert the effective level at startup.
- Multi-line stack traces evade single-line regexes; scrub each rendered line individually.
- Third-party log shippers with auto-capture may attach the request body; disable auto-capture explicitly.

## Verification

    grep -cE "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}" /var/log/app/*.log   # expect 0

Report the sinks covered, the retention set, and the canary scan result through the real aggregator.
