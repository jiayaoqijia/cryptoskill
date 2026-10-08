---
name: forward-client-ip-through-a-proxy
description: Use when an app behind a proxy, load balancer, or CDN logs the wrong client IP or rate-limits everyone as one address. Forward the real IP through the trusted-proxy chain and parse the correct header, rejecting spoofed values from untrusted hops.
---

# Forward client IP through a proxy

Behind a proxy the TCP peer is the proxy, so the app sees one IP for all users. The real client
address arrives in a header — and that header is client-controllable unless you strip and re-add it at
the edge.

## Procedure

1. Confirm what your reverse proxy sets. Nginx with `real_ip`:
   ```nginx
   set_real_ip_from 10.0.0.0/8;          # only your LB range
   real_ip_header X-Forwarded-For;
   real_ip_recursive on;
   ```
2. Strip inbound trust headers at the edge so a client cannot smuggle a fake IP:
   ```nginx
   proxy_set_header X-Forwarded-For $remote_addr;   # overwrite, do not append
   proxy_set_header X-Real-IP       $remote_addr;
   ```
   Appending (`$proxy_add_x_forwarded_for`) preserves client-supplied values — only do that when
   every upstream hop re-strips.
3. In the app, enable proxy trust for exactly the known hops, not `*`:
   ```python
   from werkzeug.middleware.proxy_fix import ProxyFix
   app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)   # trust ONE hop
   ```
   `x_for=1` reads the last ingress-appended value, which is the closest trusted proxy's view.
4. Set the framework's trusted-proxy CIDR list (Django `SECURE_PROXY_SSL_HEADER` + `USE_X_FORWARDED_HOST`, Express `app.set('trust proxy', '10.0.0.0/8')`).
5. Verify the app now sees the client, not the proxy:
   ```bash
   curl -s http://api.example.com/whoami -H 'X-Real-IP: 203.0.113.9'
   ```
   Against a properly-stripping edge, a spoofed `X-Real-IP` should be ignored and the response should
   show your real source address.
6. Check the access log format records the resolved client field, not `$remote_addr`.

## Pitfalls

- `trust proxy: true` / `x_for=*` trusts any hop, so anyone can spoof IPs and defeat rate limits and geo rules.
- Appending to an existing `X-Forwarded-For` lets a client control the leftmost value; count hops from the right.
- Two chained proxies without re-stripping leave two entries and the app reads the wrong one.
- Cloudflare/CloudFront add their own header (`CF-Connecting-IP`, `CloudFront-Viewer-Address`); prefer it at the edge, then re-emit a single canonical header.
- Rate limiting on the raw socket IP throttles the proxy, not the abuser — everyone shares one bucket.
- IPv6 addresses with ports (`[2001:db8::1]:443`) break naive string splitting and produce garbage keys.
- Trusting a header for authz decisions ("internal IP = admin") turns spoofing into privilege escalation.

## Verification

    curl -s https://api.example.com/ip -H 'X-Forwarded-For: 1.2.3.4'
    # response must show YOUR real IP, not 1.2.3.4

Pass means injected client headers are ignored and the app logs the true source. Report: "edge
rewrites XFF, ProxyFix x_for=1, spoofed XFF rejected; logs now show real client IP."
