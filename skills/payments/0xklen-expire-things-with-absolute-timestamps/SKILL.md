---
name: expire-things-with-absolute-timestamps
description: Use when caching, tokens, sessions or leases have a lifetime — store an absolute expiry instant and compare clocks, instead of a countdown that drifts across restarts and zones.
---

# Expire things with absolute timestamps

A TTL is a policy; an expiry is an instant. Storing "expires_in: 3600" and restarting the process or reading it in another zone loses the anchor. Store the absolute expiry and let every reader compare instants.

## Procedure

1. Compute the expiry once, at the point of creation, in UTC:
```python
from datetime import datetime, timedelta, timezone
exp = datetime.now(timezone.utc) + timedelta(hours=1)
```
2. Persist the instant, not the remaining seconds:
```
redis-cli SETEX session:abc 3600 '{"uid":42,"exp":"2026-03-01T15:00:00Z"}'
psql -c "INSERT INTO tokens(token,expires_at) VALUES ('...','2026-03-01T15:00:00Z');"
```
3. Compare on the same clock at read time; treat a missing or unparseable expiry as *already expired* (fail closed):
```python
if exp is None or datetime.now(timezone.utc) >= exp:
    raise Expired
```
4. For JWTs, set `exp` explicitly in UTC seconds and validate with a small clock-skew tolerance (leeway), not by trusting `iat`:
```
exp = int(datetime.now(timezone.utc).timestamp()) + 3600   # exp claim
# verify with leeway=60 to absorb host skew
```
5. Push expiry into the store when it has native TTL (Redis `EXPIRE`, DynamoDB `TTL`, Redis `PXAT` absolute) so eviction is the store's job, not scan-based:
```
redis-cli PEXPIREAT session:abc 1798700400000   # absolute ms epoch
```
6. Use absolute expiry for leases and locks too; a countdown lease renews wrongly after a pause or GC stall.
7. Sweep by range, never by scanning: `DELETE FROM tokens WHERE expires_at < now();` with an index on `expires_at`.

## Pitfalls

- Storing only `issued_at` and computing `expires = issued + ttl` at each read means a TTL change is applied retroactively to already-issued tokens — pin the expiry at issue time.
- A TTL of "1 day" interpreted as 86400s is wrong across a DST day if the caller meant "same time tomorrow local"; decide policy explicitly.
- Comparing a naive expiry to an aware `now` raises or silently misbehaves depending on the language; keep both sides aware UTC.
- Redis `EXPIRE` set from a replica restarts the clock; use `PEXPIREAT` with an absolute epoch for idempotent renewals.
- No leeway on `exp` fails valid tokens around a one-second NTP correction; too much leeway extends every token's life.
- Clock skew between signer and verifier turns expiry into a random variable — bound it (see `handle-clock-skew-between-hosts`).

## Verification

```
python3 -c "from datetime import datetime,timezone,timedelta; e=datetime.now(timezone.utc)+timedelta(hours=1); print(e.isoformat(), 'expired' if datetime.now(timezone.utc)>=e else 'valid')"
```
An absolute ISO instant is stored and the comparison is aware UTC on both sides = expiry is anchored. Report: "tokens/sessions carry `expires_at` in UTC; reads fail closed; Redis uses PEXPIREAT; 60s leeway on JWT `exp`."
