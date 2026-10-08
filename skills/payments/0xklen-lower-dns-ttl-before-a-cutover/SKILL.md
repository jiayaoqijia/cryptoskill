---
name: lower-dns-ttl-before-a-cutover
description: Use when moving a service to a new IP, load balancer, or provider. Drop the record TTL at least one old-TTL in advance so cached answers expire by the time you flip, then raise it back after the change settles.
---

# Lower DNS TTL before a cutover

Cutovers fail because resolvers still hold the old address. You cannot recall a cached record, so
you shorten its lifetime *before* the change and let the long-lived copies age out.

## Procedure

1. Read the current TTL and record the number — this is your waiting period:
   ```bash
   dig example.com A +noall +answer | awk '{print $2, $4, $5}'
   ```
   A TTL of 86400 means you need up to a full day before clients stop caching the old value.
2. At least one old-TTL ahead of the change, publish the *same* records with a low TTL:
   ```bash
   # zone file: lead with the new short TTL on every record for the name
   example.com.   60   IN  A  93.184.216.34
   www.example.com. 60 IN  CNAME  example.com.
   ```
   ```bash
   named-checkzone example.com /etc/bind/db.example.com
   rndc reload example.com
   ```
3. Confirm the short TTL is live from an authoritative server, not your cache:
   ```bash
   dig @ns1.example.com example.com A +noall +answer
   ```
4. Wait the full old TTL. Track it explicitly rather than guessing:
   ```bash
   date -u -v+86400S   # macOS; on GNU: date -u -d '+86400 seconds'
   ```
5. Flip the address at the cutover, still at TTL 60:
   ```bash
   dig @ns1.example.com example.com A +short    # expect the NEW ip
   ```
6. Drain and watch for a settle window (old TTL + traffic skew, often 1 h). Raise TTL back only
   after error rates and 5xx counts are flat.
7. If you use a CDN or managed DNS, set the low TTL through the provider API; the zone file edit
   may not reach their edge.

## Pitfalls

- Setting the low TTL *and* flipping the IP in the same change means clients still hold the old record.
- A shortened TTL does not force an early expiry — it only bounds how long new lookups cache.
- An old `CNAME` chain keeps its own TTL; shorten every link, not just the A record.
- Some resolvers floor TTLs at 30–60 s, so a TTL of 5 does not resolve instantly.
- Forgetting to restore the TTL leaves you paying per-query on a cheap-DNS bill and adds resolver load.
- A cutover during a low-traffic window can look "settled" while a large client population is simply offline.

## Verification

    dig @ns1.example.com example.com A +noall +answer   # before flip: short TTL, old IP
    dig @ns1.example.com example.com A +noall +answer   # after flip:  short TTL, new IP

Report: "TTL lowered from 86400 to 60 at 14:00 UTC, flip executed >24 h later, TTL restored to 3600
after 1 h of flat 5xx." Include both dig outputs.
