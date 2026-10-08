---
name: audit-analytics-events-for-pii
description: Use when product analytics or a CDP receives event payloads that may carry personal data. Find PII in the emit sites and strip it, then set vendor-side controls and a CI guard.
---

# Audit analytics events for PII

Product analytics is a shadow copy of personal data with its own retention and vendors. This skill finds PII in event payloads and removes it at the source.

## Procedure

1. Export the event schema from the tracking plan or by sampling:
   `curl -s "$ANALYTICS_API/events/schema" | jq '.events[].properties[].name' | sort -u`

2. Sample real payloads, not just the schema; properties are often free-form:
   `jq -c '.properties' events.ndjson | head -1000`

3. Scan values for PII patterns (emails, phones, addresses, raw ids) and for suspicious keys: `email`, `phone`, `name`, `address`, `ip`, `lat`, `lng`.

4. For each offending property find the call site: `rg -n "track\('[a-z_]+'" src/` and read the payload construction.

5. Remove the property at the emit site. Do not rely on a downstream scrub, which the vendor can change or disable.

6. Replace identity with a coarse property: send `plan_tier` not `email`, `region` not raw `lat`/`lng`.

7. Set the vendor's own controls: disable IP geolocation, enable IP anonymisation, set the shortest workable retention, and turn off cross-site ad sharing.

8. Add a deletion path at the vendor and include it in the erasure checklist.

9. Add a CI lint that fails when a `track` payload contains a denylisted key or a value matching an email regex.

## Pitfalls

- Custom dimensions and URL query strings capture PII even without a named property.
- Auto-capture features (session replay, tap maps) record everything on screen, including user data; disable or mask fields.
- Server-side events sent by the backend carry the raw user id and email unless they are stripped first.
- The vendor may share data with ad partners by default; set sharing off explicitly.
- Schema docs lag reality; always sample the actual payloads before declaring the audit done.

## Verification

    rg -nE "\"(email|phone|name|ip|lat|lng)\"\s*:" src/events/ || echo "no PII keys in event payloads"

Report the events with PII removed, the vendor controls set, the retention configured, and the CI lint status.
