# Auditing a web tool / agent front-end (read-only)

When the candidate is a **tool, dashboard, LP bot or agent UI** (not a protocol), the site's own
JavaScript is the cheapest ground truth. Everything below is keyless GET-only — no login, no wallet,
no money at risk. Worked case: `metina.id` vs Meteora (Sep 2026).

## 1. Who runs it, without login

```bash
curl -s "https://api.fxtwitter.com/<screen_name>"          # keyless JSON: id, followers, tweets, description, media_count
```

- `description` usually names the dev + handle + Discord (e.g. "Managed by @0xyanman, @dojigato & @lifeatfarrel 🇮🇩").
- Account age from the numeric `id` (Twitter snowflake):
  `datetime.utcfromtimestamp(((id >> 22) + 1288834974657) / 1000)` → e.g. `2025-09-25`. A 1-year-old
  account with a few hundred followers is a different risk class than a 5-year-old project.
- Mirror/aggregator sites behind Cloudflare (403 "Just a moment") and the syndication timeline
  endpoint (429) are unreliable here; try `api.fxtwitter.com` first, and search-result snippets of
  mirror pages (`twstalker`) for quoted tweets/testimonials if needed.

## 2. Enumerate every route (including unlisted ones)

```bash
curl -s https://<host>/ -o home.html
grep -oE '"buildId":"[^"]+"' home.html                      # buildId
curl -s https://<host>/_next/static/<buildId>/_buildManifest.js   # -> {"/(route)":[...chunks]}
```

The build manifest lists routes that appear nowhere in the nav — in the worked case
`/monitor`, `/pnl-card`, `/token-safety`, `/treasury`, `/wrapper`, `/admin/evm-calendar`.
Those hidden routes are exactly where a tool reveals what it really does (and a publicly shipped
`/admin/*` route is a hygiene finding).

## 3. Where does the data come from? (data provenance)

```bash
grep -ohE '/_next/static/chunks/[a-zA-Z0-9./_-]+\.js' home.html | sort -u > chunklist.txt
while read -r c; do curl -s "https://<host>$c" -o "ch/$(echo $c | md5sum | cut -c1-8).js"; done < chunklist.txt
cat ch/*.js | grep -oE 'https?://[a-zA-Z0-9._-]+' | sort | uniq -c | sort -rn   # upstream hosts
grep -oE '"(/api/[a-zA-Z0-9_/-]+)"' ch/*.js | sort -u                          # its own endpoints
```

Reading the result:
- Upstream = incumbent protocol's public API (`dlmm.datapi.meteora.ag`, `damm-v2.datapi.meteora.ag`)
  + `rugcheck.xyz` + exchange price feeds → the tool **owns no data**; it is a UI layer. Say so:
  "bukan platform LP, cuma kaca spion" — there is nothing to migrate to.
- Upstream = its own backend (`POST /api/meteora/launch` with `{mint, solAmount:0.1}`) → that feature
  spends *their* wallet, server-side; it is a demo/unauthenticated surface, not a service.
- Note exact host spellings: `dlmm-api.meteora.ag` 404s where `dlmm.datapi.meteora.ag` works.

## 4. Probe its own endpoints — GET only

| Endpoint | Read it for |
|---|---|
| `/api/online-users` | live concurrent users = the real traction number (worked case: **3**) |
| `/api/donations`, `/api/donate` | funding evidence — check the *shape*, not the totals |

A donations endpoint that takes free-text `amount`, `walletAddress` and `transactionSignature` is
**not** verified on-chain revenue. Worked case returned `fake_signature_12345`, `"Hacker Donator"`,
`<script>alert(1)</script>`, `<img src=x onerror=alert(1)>` and invented addresses (`aaaaa`,
`Sir_...ell_`). Conclusion to write: *no verified revenue* + a security finding (stored XSS payloads,
no signature check) — never quote the leaderboard total as funding.

**Hard rule: never fire a state-changing endpoint.** A `POST` that opens a position or moves funds
spends the third party's money. State it in the report: "the client chunk sends no credentials, so it
looks unauthenticated — I did not test-fire it because it touches their funds."

## 5. Independent PnL for any Solana LP wallet (Meteora, keyless)

```bash
curl -s "https://dlmm.datapi.meteora.ag/portfolio/total?user=<WALLET>"
#  -> {"totalPnlUsd":"50.18","totalPnlSol":"0.5216","totalClosedPositions":17}
curl -s "https://dlmm.datapi.meteora.ag/portfolio?user=<WALLET>&page=1"
#  -> {pools:[{tokenX,tokenY,binStep,totalDeposit,totalWithdrawal,totalFee,pnlUsd,lastClosedAt,...}], hasNext, totalPositions}
```

This is the same source the tool's own `/portfolio` page calls, so it doubles as (a) proof the tool
works, (b) a **third-party check on our own book**. Worked case: local engine DB recorded 7 live
closed positions (+$43.12) while the protocol API reported **17 closed positions / +$50.18 / +0.5216
SOL** — i.e. the DB under-counts history (post-wipe) and the chain wallet was still below the
return-of-capital line. Report all three numbers (book, protocol API, chain) instead of one.
Pools with `totalDeposit: 0` are ghost/failed position accounts — useful evidence of failed opens.

## 6. Interpretation crib

| Finding | What to write |
|---|---|
| Tool calls only the incumbent's public APIs | Not a competitor; a UI layer. "Pindah ke <tool>" doesn't exist. |
| Concurrent users in single digits | Real traction is tiny; say the number, no adjectives. |
| Unverified free-text donation/leaderboard API | No verified revenue + security finding. |
| Hidden `/admin/*` route in build manifest | Hygiene/ops finding, low severity. |
| Contract interactions in chunks (`sendTransaction`) | Check *whose* key signs: bundled `@solana/web3.js` in client chunk ≠ the user's wallet is at risk. |
| No repo / no audit / no TOS | Weight it as risk, not disqualification — but say it plainly. |

## 7. Hygiene for this class of task

- Read-only end to end; never connect a wallet to an unevaluated tool, never paste API keys it asks
  for (a treasury feature asking for a Helius key means that key reaches their backend — privacy note).
- Save the write-up to the vault (`~/obsidian-vault/Ide Project - <Name> ... .md`) with the raw
  numbers, the commands' outputs, and the rating; the user wants the note as part of the deliverable.
