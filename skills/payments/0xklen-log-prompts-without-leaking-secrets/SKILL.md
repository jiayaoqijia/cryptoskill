---
name: log-prompts-without-leaking-secrets
description: Use when capturing prompts and responses for debugging. Redact secrets and personal data before they hit logs or a tracing backend, and keep the redaction working on joined log lines.
---

# Log prompts without leaking secrets

Prompt logs are the most common place credentials and user data leak. Capture enough to debug; redact the rest at the edge, before the log line exists.

## Procedure

1. Decide what is loggable: structure and metadata (model, tokens, latency, schema pass/fail) always; content only redacted, and only when needed.

2. Run a redactor on prompt and response text before it is serialised: API keys, bearer tokens, emails, phone numbers, card-like digit runs, and any known secret patterns.

```python
import re, functools
PATTERNS = [r'(?i)bearer\s+[a-z0-9._-]+', r'\b\d{13,19}\b',
            r'[\w.+-]+@[\w-]+\.[\w.]+', r'sk-[A-Za-z0-9]{20,}']
def redact(s):
    return functools.reduce(lambda t, p: re.sub(p, '[REDACTED]', t), PATTERNS, s)
```

3. Redact on the client, before the value reaches the tracer or logger. Backend-side redaction misses whatever was already shipped.

4. Match keys by name, case-insensitively — `authorization`, `api_key`, `password`, `token` — in both JSON and query-string forms.

5. Hash or drop identifiers you must correlate: log `user_id_sha256` (or a tenant-scoped pseudo-id), not the raw id, if policy forbids it.

6. Test the redactor with real-looking samples and run a leak scan over the log sink, not just a unit test on the regex.

7. Treat the tracing backend as a second data store with its own access controls and retention — scope who can read it.

## Pitfalls

- Redacting after the value is joined into a larger string, so a key prints because the pattern expected it at the start.
- Missing an encoded secret: base64 blobs and URL-encoded query strings pass the plain patterns.
- Logging the full request on error "just this once" — the exception path is the leak path.
- A regex so greedy it eats the whole message, destroying the debug value you logged for.
- Allowing secrets into prompt text via tool output in the first place — sanitise upstream too.

## Verification

    python3 redact.py < sample_requests.jsonl | grep -icE 'sk-|bearer [a-z0-9]|@'   # must be 0 matches in the redacted output

Report: "redactor applied at the client edge; scanned 10k logged prompts, 0 secret or email matches; log lines keep model, tokens, latency, and schema status with content redacted."
