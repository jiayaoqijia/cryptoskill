---
name: redact-secrets-from-model-context
description: Use when files, logs, or tool output you are about to send to a model may contain credentials. Scan and replace secrets with placeholders before they enter context, then verify nothing sensitive remains.
---

# Redact secrets from model context

Once a credential is in a prompt it is out of your control — it may be logged, cached, or echoed back. This skill scans candidate content for secret shapes and swaps them for placeholders before the content is ever sent.

## Procedure

1. Scan content before it enters context, not after. Run a pattern pass over every file you intend to include.

       grep -rEn '(AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36}|sk-[A-Za-z0-9]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY-----|xox[baprs]-[A-Za-z0-9-]+)' incoming/

2. Broaden to assignment shapes, which catch keys you have no pattern for:

       grep -rEn '(api[_-]?key|secret|token|password|passwd|bearer)[":= ]+[A-Za-z0-9._-]{12,}' incoming/ -i

3. Replace each hit with a stable placeholder that preserves structure for reasoning, e.g. `sk-REDACTED-4f2a`, and keep the real value only in a local vault outside the prompt.

4. Redact by parsing, not by regex alone, for structured files: load `.env`/YAML as key-value and mask the values of sensitive keys; regex misses multi-line PEM blobs.

5. Handle encoded secrets too: decode base64/JWT segments and re-scan, and redact the `authorization` header in captured HTTP.

       printf '%s' "$B64" | base64 -d 2>/dev/null | grep -En '(key|token|secret)' && echo "encoded secret"

6. Verify the redacted payload is clean before sending: re-grep the post-redaction text and confirm zero hits.

7. If a secret was already sent, treat it as disclosed: rotate it, and record which context received it.

## Pitfalls

- `echo`ing the variable to check it prints the secret into the log you were trying to protect; use `${VAR:+set}` instead.
- Redacting only obvious fields misses secrets in free-text notes, commit messages, and stack traces.
- Placeholders that leak length or prefix still help an attacker; truncate consistently.
- A redaction step that fails silently leaves the raw value; assert the operation ran and reduced the match count.

## Verification

    grep -rEn '(AKIA[0-9A-Z]{16}|ghp_[A-Za-z0-9]{36}|sk-[A-Za-z0-9]{20,}|PRIVATE KEY)' redacted/ | wc -l   # must be 0

Report: "scanned <files>; secrets found n, redacted n, encoded m; post-redaction scan clean; disclosed-and-rotated <list or none>."
