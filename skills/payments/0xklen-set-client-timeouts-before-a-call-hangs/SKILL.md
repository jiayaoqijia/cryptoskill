---
name: set-client-timeouts-before-a-call-hangs
description: Use when making outbound HTTP calls. Set explicit connect, read, and total timeouts on every client so a hung peer cannot pin a worker forever.
---

# Set client timeouts before a call hangs

Most HTTP clients default to "wait forever". One hung peer then pins a worker and, as pool slots
fill, cascades into a full stall. Set timeouts explicitly on every client.

## Procedure

1. Set timeouts at construction, not on the happy path:
   ```python
   import httpx
   client = httpx.Client(timeout=httpx.Timeout(connect=3.0, read=10.0, write=10.0, pool=3.0))
   ```
2. Use separate connect (short, ~3 s) and read (bounded by expected latency) values; one number is a compromise.
3. For long transfers use a read timeout larger than a single chunk, not a total timeout that kills a healthy transfer.
4. Wrap the retry loop in a total deadline so retries cannot sum past the budget.
5. In shell scripts use the curl equivalents:
   ```bash
   curl -s --connect-timeout 3 --max-time 30 "$API/v1/me" | jq .
   ```
6. Distinguish a timeout (retryable) from refused/DNS (usually config) in the error path.
7. Test the timeout path with a deliberately slow endpoint or a proxy that stalls.

## Pitfalls

- A per-response `read=10` is not a total limit when the server trickles bytes; it resets per read.
- No timeout on a `requests`/`httpx` default means the worker hangs until the OS TCP timeout (minutes).
- Timeouts shorter than the API's real p99 cause spurious failures and pointless retries.
- A too-long timeout holds pool slots and cascades into pool exhaustion.
- Retrying with no total deadline multiplies the timeout by the attempt count.

## Verification

    curl -s -o /dev/null -w 'connect=%{time_connect} total=%{time_total}\n' --max-time 30 "$API/v1/me"

Report: "Client connect=3s read=10s total-deadline=45s; slow-endpoint test fails fast at 3s."
