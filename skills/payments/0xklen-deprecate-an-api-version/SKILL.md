---
name: deprecate-an-api-version
description: Use when retiring an old API version or endpoint with live consumers. Runs usage telemetry, communicates a sunset date, then removes the surface only after traffic reaches zero.
---

# Deprecate an API Version

Removing an endpoint with live callers is an outage you scheduled. Deprecation is a measurable process: announce, observe usage fall to zero, then remove.

## Procedure

1. Prove the version is used before announcing: count callers from access logs or metrics over 30 days, grouped by client. `curl`-level data: extract the version segment and the API key/UA:
   `awk -F'"' '{print $2}' access.log | awk '{print $2}' | cut -d/ -f2 | sort | uniq -c`.
2. Pick a sunset date with lead time proportional to client count: 90 days for external partners, 30 for internal. Write it down and put it in the response.
3. Announce in three places: docs, the API itself, and directly to the top callers. Silence is not communication.
4. Signal the deprecation in every response so quiet clients see it in their own logs and tests:
   - `Deprecation: Sat, 01 Mar 2025 00:00:00 GMT` (RFC 8594 / draft-dalal-deprecation-header)
   - `Sunset: Fri, 01 Aug 2025 00:00:00 GMT`
   - `Link: <https://docs.example.com/migrate-v1-v2>; rel="deprecation"`
5. Emit one structured log line per deprecated call with the client id, so you can measure the ramp:
   `level=warn msg=deprecated_api version=v1 client=<id> path=/v1/users`.
6. Brownout near the end: return `410 Gone` for a short window on a schedule (e.g. 10 minutes daily for a week) so laggards notice before the hard cut.
7. Track the count down. Remove when it reaches zero for 14 consecutive days, or when the sunset date passes with a written exception for remaining callers.
8. After removal, return `410 Gone` with a body linking the migration guide, never a bare 404.

## Pitfalls

- Deleting before the traffic reads zero; internal batch jobs often call at 3am weekly and never show in the daily mesh.
- A `Sunset` header buried in a 200 response that clients never log is invisible; also email the top callers.
- Deprecating and removing in the same release; migration needs a runway with both versions live.
- Assuming a `User-Agent` identifies a client; versioned SDKs and shared egress IPs blur attribution — send a per-client deprecation warning in the response body when possible.
- A 404 for a removed API confuses clients into thinking it is a typo; use 410 so "gone" is unambiguous.

## Verification

    grep -c 'version=v1' app.log        # after sunset: must be 0
    curl -sI https://api.example.com/v1/users | grep -iE 'deprecation|sunset'

Before removal the headers carry the announced dates; after removal the call returns `HTTP/2 410` with a migration link.

Report: "v1 deprecation: sunset <date>, headers live since <start>, usage fell from <A> to 0 calls/day over <N> days; removed and now returns 410 with the v2 migration link."
