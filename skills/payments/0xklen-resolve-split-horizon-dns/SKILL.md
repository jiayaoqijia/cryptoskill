---
name: resolve-split-horizon-dns
description: Use when a name resolves differently inside versus outside your network — an internal service that must not be public, or a record that works on one network and fails on another. Reconcile the internal and external views deliberately and test both.
---

# Resolve split-horizon DNS

Split-horizon (split-view) DNS answers the same name with different records depending on who asks. It
is intentional — internal clients hit private IPs, the public sees an edge IP — but it breaks whenever
the two views drift out of sync or a resolver is misclassified.

## Procedure

1. Determine which view a given client gets by querying both resolvers:
   ```bash
   dig @10.0.0.53 internal.example.com A +short     # internal resolver
   dig @1.1.1.1 internal.example.com A +short       # public resolver
   ```
   The internal name should resolve only on the internal resolver; the public one returning `NXDOMAIN`
   is correct for a truly private service.
2. Confirm the internal view returns RFC 1918 or private ranges, never public IPs:
   ```bash
   dig @10.0.0.53 app.example.com A +short | grep -E '^(10\.|172\.(1[6-9]|2[0-9]|3[01])\.|192\.168\.)'
   ```
3. Check the edge view point at the public hostname, which must never expose the private IP:
   ```bash
   dig @1.1.1.1 app.example.com A +short
   ```
4. Test the failure mode directly — resolve from a VPN-connected host and from an off-network host:
   ```bash
   # on VPN
   dig app.example.com A +short        # expect internal IP
   # off network
   dig app.example.com A +short        # expect edge IP or NXDOMAIN
   ```
5. Verify the reverse zone matches, or logging and access controls break:
   ```bash
   dig -x 10.0.1.5 +short              # expect the internal hostname
   ```
6. Confirm the internal resolver is *only* reachable internally (a public DNS server must not answer
   your private records):
   ```bash
   dig @<public-ip-of-your-resolver> internal.example.com   # must time out / refuse
   ```
7. Keep both zone files under version control and deploy them together so a record edit lands in both
   views at once.

## Pitfalls

- Publishing private A records on a globally reachable resolver leaks your internal topology (RFC 1918 leakage).
- A VPN that sets a search domain but not the internal resolver sends queries to the public resolver, breaking internal names.
- Forgetting the reverse zone makes internal IPs resolve to nothing, breaking logs and monitoring.
- An internal view that duplicates the public edge IP defeats the split and adds a useless hop.
- A CNAME added to one view only causes differing behaviour that looks like flaky DNS.
- Caching resolvers in the middle may have cached the internal answer and serve it to an external client during the TTL.
- Testing only from the VPN hides the off-network path that real users take.

## Verification

    dig @10.0.0.53 app.example.com A +short   # private IP
    dig @1.1.1.1  app.example.com A +short    # edge IP or NXDOMAIN
    dig @<public-resolver> internal.example.com   # must refuse/time out

Pass means each client class gets its intended view and private records are unreachable from outside.
Report both dig outputs and the resolver-refusal result.
