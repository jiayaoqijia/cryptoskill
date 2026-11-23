# Prefixless exchange credentials: which half am I holding?

Provider is unidentifiable from the string: Binance API Keys and Secret Keys are **both 64
alphanumeric characters with no prefix**. Every account endpoint needs *both* (HMAC-SHA256 signature
over the query string), so a lone pasted string is a to-do, not a connection.

Runnable probe: `scripts/binance_key_probe.py <candidate>` (read-only, masked output, persists nothing).

## Differential probe (verified 5 Okt 2026)

Binance validates in this order: **API key exists → source IP allowed → signature valid**. So sending
the candidate as `X-MBX-APIKEY` on a *read* endpoint with a deliberately wrong signature separates the
two cases, with a known-fake 64-char key as the control:

```
GET https://api.binance.com/api/v3/account?timestamp=<ms>&recvWindow=5000&signature=<hmac of dummy secret>
X-MBX-APIKEY: <candidate>
```

| response | meaning |
|---|---|
| `-1022 Signature for this request is not valid`, **HTTP 400** | key RECOGNISED → candidate **is a live API Key** |
| `-2015 Invalid API-key, IP, or permissions`, **HTTP 401**, identical to control | not an API key (usually the Secret Key) — or this host is outside the key's IP whitelist |
| `-2014 API-key format invalid` | invisible characters: strip whitespace/zero-width, re-measure length |

Observed values: user's real API key → `HTTP 400 code=-1022`; fake control → `HTTP 401 code=-2015`.
**Don't read the 400 as "malformed"** — the informative part is the body code, and a valid key
legitimately answers 400 on a bad signature.

Side effects: none (auth fails before any data is returned). Never "test" a credential against a
state-mutating endpoint.

## What a `-1022` also tells you

The request got past the IP check, so this host's public IP is allowed — either the key's whitelist
matches it (`curl -s https://api.ipify.org`, e.g. `43.173.12.165`) or no whitelist is set. Say which
in the report; a whitelisted key is the stronger setup, and the whitelist silently breaks if the VPS
IP changes (symptom: the good key suddenly returns `-2015`).

## Connecting a read-only portfolio monitor: order of operations

1. Prove the service is reachable from this host **before** asking for credentials —
   `api/v3/ping`, `/api/v3/time`, and a public price call; a sandbox/geo block should surface first.
2. Ask for BOTH halves, plus the permission boxes and the IP field. Exact wording that works:
   - tick **Enable Reading** only
   - leave **OFF**: Spot & Margin Trading, Futures, Withdrawals, Internal Transfer,
     Permit Universal Transfer
   - **Restrict access to trusted IPs only** → the **server's** IP, not the user's
3. Probe the first half that arrives (table above) and answer which half it is.
4. With both halves, read the permission flags and refuse to store if any write scope is on.
   Binance's endpoint for this is `/sapi/v1/account/apiRestrictions` (signed GET) — confirm the path
   against the live docs the first time you call it; it has not been exercised in this environment yet.
5. Store both halves in `~/.hermes/.env` (mode 600) **in one write**, never in notes, repo or commit.
6. `rm` the probe script copy if the key was inlined in it.
7. First live run = pull balances, price them, and send the resulting card as proof of connection.
8. If the credential was pasted into a chat, offer rotation at the exchange's API-management page
   once setup is done.

## Notes for the monitor itself

- Balances may be split across Spot, Funding, and Simple/Earn wallets — enumerate them; a spot-only
  read under-reports the portfolio.
- Signed GETs need `timestamp` (ms) + `recvWindow`; clock drift causes `-1021`.
- Alert on **deltas** (allocation shift, asset in/out, cap breach), not on every poll — this user
  rejects periodic "no change" messages.
