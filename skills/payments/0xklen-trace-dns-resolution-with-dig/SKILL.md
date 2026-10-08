---
name: trace-dns-resolution-with-dig
description: Use when a hostname resolves to the wrong IP, times out, or behaves differently on one machine than another. Walk the delegation chain with dig and read the authority, TTL, and flags at each hop instead of trusting one cached answer.
---

# Trace DNS resolution with dig

A resolver returning `SERVFAIL`, a stale A record, or an `NXDOMAIN` that only one machine sees is a
path problem, not a single-answer problem. Resolve the name hop by hop and confirm which server
actually returned the answer.

## Procedure

1. Start with the default resolver and note the flags:
   ```bash
   dig +noall +answer +comments example.com A
   ```
   `flags: qr aa` on a recursive answer means the upstream is authoritative, not necessarily correct.
2. Query a public resolver directly to separate your local cache from upstream truth:
   ```bash
   dig @1.1.1.1 example.com A +short
   dig @8.8.8.8 example.com A +short
   ```
   Different answers mean split-horizon or propagation lag (see `resolve-split-horizon-dns`).
3. Walk the delegation from the root — this shows the exact nameservers for each zone:
   ```bash
   dig +trace example.com
   ```
4. Ask the authoritative server that `+trace` reported, and read the TTL it returns:
   ```bash
   dig @ns1.example.com example.com A
   ```
5. Check every record type the name carries; the bug is often a stale `AAAA` or `CNAME`:
   ```bash
   dig example.com A AAAA CNAME MX TXT +noall +answer
   ```
6. For DNSSEC failures, confirm the chain explicitly:
   ```bash
   dig +dnssec +cd example.com A    # bypass validation
   dig +dnssec example.com A        # validation on
   ```
   `+cd` succeeding while validation fails points at a missing or expired DS/RRSIG.
7. Compare from a second network (a container or jump host) to rule out local `/etc/hosts`
   overrides: `getent hosts example.com`.

## Pitfalls

- A single `dig` hits your cache; the answer may be minutes from expiring. Re-query the authority.
- `dig` ignores `/etc/hosts` but browsers and `getent` honour it — a "DNS" bug is often a hosts file.
- `+short` hides the `SERVFAIL`/`NXDOMAIN` status and the responsible server; use `+comments`.
- TTL `0` in an answer means "do not cache", not "instant propagation" — resolvers still hold it briefly.
- A `CNAME` to a name that does not exist returns `NXDOMAIN` for the whole lookup, masking the A record.
- Trailing-dot differences (`example.com` vs `example.com.`) change the search-domain path and can add a suffix.

## Verification

    dig +trace example.com | grep -A1 'example.com.  *IN *NS'
    dig @ns1.example.com example.com A +short

Pass means the authoritative server returns the intended IP(s) and no hop reports `SERVFAIL`. Report:
"trace ends at ns1.example.com returning 93.184.216.34; public resolvers agree, local resolver
cached a stale 1.2.3.4 with TTL 300."
