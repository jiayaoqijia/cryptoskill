---
name: sanitise-exception-payloads-for-error-trackers
description: Use when an error tracker or crash reporter captures request context, cookies, or locals. Disable auto-capture, scrub in before_send, and prove it with a canary error.
---

# Sanitise exception payloads for error trackers

Error trackers capture request context, cookies, and locals by default. This skill strips personal data before an exception ever leaves the process.

## Procedure

1. Audit current capture in the SDK. For Sentry check `send_default_pii`, `max_request_body_size`, and whether `before_send` is set.

2. Turn off automatic PII capture at init:
   `Sentry.init(dsn=dsn, send_default_pii=False, max_request_body_size="never")`

3. Add a `before_send` hook that strips cookies, headers, and query strings:
   ```python
   def before_send(event, hint):
       req = event.get("request", {})
       req.pop("cookies", None); req.pop("headers", None)
       req["query_string"] = ""
       return event
   ```

4. Scrub `extra` and `contexts` by allowlist; drop every key not on the safe list rather than trusting a denylist.

5. Scrub breadcrumbs. Network breadcrumbs record URLs with query params; filter or disable them entirely.

6. Reduce the user object to an opaque id: `event["user"] = {"id": hash_id(user_id)}` and nothing else.

7. For frameworks (Rails, Django, Express) disable parameter capture in the tracker middleware explicitly, not just the SDK flag.

8. Test with a synthetic exception carrying a canary email in a header, a query string, and the body, then confirm the tracker event contains none of them.

9. Set server-side scrubbing rules in the tracker as a second layer, in case an older client still ships an unsanitised payload.

## Pitfalls

- Upgrading the SDK can re-enable default capture; pin the version and re-run the canary after upgrades.
- Source-context capture sends surrounding source lines that may hold fixtures with real data.
- Attachments (screenshots, log files) bypass `before_send`; disable attachment capture or scrub it separately.
- Breadcrumbs survive on some SDKs even when `send_default_pii` is off; verify empirically.
- Sampling config may apply scrubbing only to sampled events; always scrub before sampling runs.

## Verification

    # post a synthetic error carrying CANARY-PII, then
    curl -s -H "Authorization: Bearer $TRACKER_TOKEN" "$TRACKER_API/issues/$ID/events/latest" | grep -c "CANARY"   # expect 0

Report which capture paths were disabled and the canary scan result for header, query, and body.
