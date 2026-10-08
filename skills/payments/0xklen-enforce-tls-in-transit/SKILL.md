---
name: enforce-tls-in-transit
description: Use when data crosses a network hop and plaintext is still permitted, or you must prove TLS is enforced everywhere. Probe each hop and pin a minimum protocol version.
---

# Enforce TLS in transit

A connection that permits plaintext will eventually be plaintext. This skill forces TLS on every hop and proves it with a live probe rather than a config glance.

## Procedure

1. Enumerate the hops: user to edge, edge to app, app to DB, app to cache, app to vendors, and service to service internally.

2. For public endpoints, test the redirect and the handshake:
   `curl -sI http://host/` must return `301` or `308` to https, and `curl -sI https://host/` must succeed.

3. Check the negotiated protocol and cipher:
   `openssl s_client -connect host:443 -servername host </dev/null | grep -E "Protocol|Cipher"` requiring TLS 1.2 minimum, preferring 1.3.

4. Add HSTS only after serving works, starting short to avoid lockout: `Strict-Transport-Security: max-age=604800; includeSubDomains`, raised later to a year with `preload`.

5. Force TLS at the database: set `hostssl` in `pg_hba.conf` and `sslmode=verify-full` in the client DSN with a pinned CA.

6. Use mutual TLS or a service mesh for internal hops; a plaintext east-west connection is disclosure after a lateral move.

7. Disable weak protocols and ciphers at the terminator (TLS 1.0/1.1 off, RC4 and 3DES off) and re-scan with `testssl.sh host`.

8. Verify chain and certificate validity: `openssl s_client -connect host:443 -verify_return_error` must end with `Verify return code: 0 (ok)`.

9. Automate the probe in CI so a downgrade regression fails the build.

## Pitfalls

- `verify=False` or `ssl_verify=False` in client code silently accepts any certificate; grep for it and fail the review.
- Self-signed certificates with a widely shared bundled CA are not trust; they are shared secrecy.
- Proxies and load balancers can terminate TLS and re-originate plaintext to the app on the private network; check that hop too.
- Certificate expiry is a hard outage; monitor with a 30-day alert and auto-renew.
- HSTS preload is painful to undo; only submit once every subdomain serves HTTPS.

## Verification

    for h in $HOSTS; do printf "%s " "$h"; openssl s_client -connect "$h:443" -servername "$h" </dev/null 2>/dev/null | grep -m1 Protocol; done

Every host must report TLSv1.2 or TLSv1.3; report any host negotiating lower or failing the chain check.
