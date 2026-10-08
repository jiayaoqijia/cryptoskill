---
name: break-down-request-timing-with-curl
description: Use when a request is slow and you cannot tell whether DNS, TCP connect, TLS, or the server's first byte is the culprit. Split the total with curl's -w timing variables and read where the milliseconds actually go.
---

# Break down request timing with curl

"Slow request" is four different problems wearing one label. curl can time each phase separately, so
you attribute the latency to DNS, connect, TLS, or time-to-first-byte before you touch any code.

## Procedure

1. Request the URL with a phase-by-phase timing template:
   ```bash
   curl -sS -o /dev/null -w '\
   dns=%{time_namelookup} connect=%{time_connect} tls=%{time_appconnect} \
   ttfb=%{time_starttransfer} total=%{time_total} size=%{size_download}\n' \
     https://api.example.com/v1/health
   ```
2. Read the deltas, which is where the meaning is:
   - `connect - namelookup` = TCP handshake cost (network RTT).
   - `appconnect - connect` = TLS handshake cost.
   - `starttransfer - appconnect` = server processing + TTFB (your code/DB).
   - `total - starttransfer` = body transfer.
3. Run it 10 times and look at the spread — a p99 far above the mean points to intermittent server GC
   or a shared-path issue:
   ```bash
   for i in $(seq 1 10); do
     curl -sS -o /dev/null -w '%{time_namelookup} %{time_connect} %{time_appconnect} %{time_starttransfer} %{time_total}\n' \
       https://api.example.com/v1/health
   done
   ```
4. Separate connection reuse from fresh connects — a warm pool should show near-zero connect:
   ```bash
   curl -sS -o /dev/null -w 'reused=%{time_connect}\n' \
     https://api.example.com/a https://api.example.com/b   # second connection is reused
   ```
5. If TTFB dominates, the network is fine and the server is the problem. If connect dominates, check
   path/latency with `trace-a-network-path-with-mtr`.
6. Isolate DNS from the rest by resolving first:
   ```bash
   curl -sS --resolve api.example.com:443:93.184.216.34 -o /dev/null \
     -w 'connect=%{time_connect} ttfb=%{time_starttransfer}\n' https://api.example.com/
   ```
   A `--resolve` call that is fast while the normal one is slow means DNS, not the server.

## Pitfalls

- `time_total` alone hides which phase is slow; always break it down.
- A single run measures one moment; capture a spread before concluding.
- `time_appconnect` is 0 when the URL is HTTP, so the TLS delta is meaningless — check the scheme.
- Connection reuse makes the second identical request look "fast"; the first cold request is the real cost.
- HTTP redirects are not followed unless `-L` is set, so you time only the 301, not the real page.
- A proxy in the environment (`http_proxy`) silently routes curl through a different path than the app takes.
- Measuring from a laptop adds last-mile latency the production server never sees — test from a comparable host.

## Verification

    curl -sS -o /dev/null -w 'connect=%{time_connect} tls=%{time_appconnect} ttfb=%{time_starttransfer} total=%{time_total}\n' \
      https://api.example.com/v1/health

Pass means the phase that dominates matches your hypothesis (e.g. TTFB >> connect ⇒ server-side).
Report: "dns 2 ms, connect 18 ms, tls 24 ms, ttfb 640 ms — server processing, not network."
