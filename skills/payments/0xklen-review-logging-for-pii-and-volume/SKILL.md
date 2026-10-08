---
name: review-logging-for-pii-and-volume
description: Use when a diff adds or changes logging. Checks each new log line for personal data, secrets, and per-request volume that would flood the sink or leak user data.
---

# Review logging for PII and volume

Logs are the widest data surface a system has: shipped to a third party, retained for months, and readable by everyone on call. A log line is a data export.

## Procedure

1. List new log statements: `gh pr diff 482 | grep -nE '^\+.*(log\.|logger\.|console\.log|print\(|fmt\.Print|Log\.)'`.
2. For each, check the interpolated values for personal data: email, phone, full name, address, government id, IP, full card number, auth token, session cookie, password even hashed.
3. Require redaction at the point of logging, not downstream: log `email_hash(masked) = ab***@example.com` or the user id, not the raw address.
4. Scrub by construction: never `log.info("req", req)` with a whole request object — that carries headers (Authorization), body (password), and cookies.
5. Check the level matches the volume. A `debug`/`trace` line inside a hot loop is fine; an `info` line per request at 5k rps is not. Estimate: requests-per-second × log size must fit the sink's budget.
6. Confirm structured fields, not string concatenation, so the sink can index and redact by field: `logger.info("login", user_id=uid, result="fail")`.
7. Verify the retention and access policy of the sink covers anything you let through — if logs go to a vendor without a DPA, no PII may pass.

## Pitfalls

- Logging the full JWT to debug an auth issue; the token is live until expiry.
- A stack trace that includes a connection string with a password in the error message.
- Logging the request body for a payment endpoint, capturing the PAN and CVC.
- An info-level line in a per-row loop, producing gigabytes an hour and hiding real errors.

## Verification

    gh pr diff 482 | grep -nE '^\+.*(log|logger)\.' | grep -iE 'email|phone|token|password|authorization|cookie|card'
    # Then grep for whole-object logging:
    gh pr diff 482 | grep -nE '^\+.*log\.(info|debug)\([^)]*\b(req|request|event|body)\b'

Zero PII hits and no whole-object logging is the pass. Report the redaction used and the estimated lines-per-second for any new hot-path log.

## Worked example

Added line:
    logger.info("login", email=email, password=password)
Two findings: the raw email is PII, and the password has just reached the log sink. The fix:
    logger.info("login", user_id=uid, email_domain=email.split("@")[-1], ok=ok)
The domain is enough to debug deliverability; the local part and the password never leave the process.
