---
name: localize-a-fault-by-bisecting-layers
description: Use when a request fails somewhere across client, proxy, network, app, and database. Probing each boundary in turn, binary-searching the layers to the one that first diverges.
---

# Localize a Fault by Bisecting Layers

A 502 could be the client, the TLS terminator, the app, or the database. Probe the pipeline at each boundary; the layer where the good signal stops is the layer that owns the bug.

## Procedure

1. Draw the path end to end: browser -> DNS -> CDN -> LB -> proxy -> app -> cache -> DB -> upstream. Name each hop with a host and port.
2. Probe the closest hop to you and walk outward, so each failure is attributable: `curl -sv https://api.example.com/health` first.
3. At each boundary test *two* things: reachability (`curl --connect-timeout 2 -so /dev/null -w '%{http_code}' <hop>`) and correct payload (does the body contain what the next layer expects?).
4. Binary-search the hops rather than probing all: test the middle hop. Green there means the fault is downstream; red means upstream.
5. On divergence, capture the evidence at the seam: full response headers (`curl -D -`), status, body, and timestamp, from both sides of the boundary.
6. Check the layer's own logs at that instant (correlate by request id) before moving inward or outward.
7. For TLS/DNS hops, use the dedicated tools: `dig +trace api.example.com`, `openssl s_client -connect host:443 -servername api.example.com`.
8. State the owning layer explicitly, then only that team/instrument is relevant; stop probing the others.

## Pitfalls

- Probing only from the outermost client, so every intermediate failure looks like "the API is down".
- Testing `/health`, which returns 200 while the actual route is broken — probe the failing path, not the health endpoint.
- A local proxy or VPN intercepting the request, so your probe never reaches the real hop.
- Ignoring request-id correlation and reading logs at the wrong second, concluding a false failure.
- Treating a cached 5xx from the CDN as the origin's response.
- Moving inward without capturing the seam evidence, then being unable to prove which side broke.

## Verification

    for hop in https://cdn.example.com https://api.example.com http://127.0.0.1:8080; do
      printf '%s -> ' "$hop"; curl -so /dev/null -w '%{http_code}\n' --connect-timeout 3 "$hop/health"; done
    # the first hop that diverges from 200 localizes the fault to that boundary's downstream

    curl -sD - https://api.example.com/v1/cart -H "X-Request-Id: t1" | head -20
    # headers + body + X-Request-Id to correlate the same second in every layer's logs

Report to the user: the path diagram, the first divergent hop, and the evidence captured at that seam.
