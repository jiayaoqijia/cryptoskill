# Trading terminals / wallet trackers — comparison recipe + worked case (27 Sep 2026)

Question asked: *"deepdive wallet tracker: Axiom Trade, Fomo, atau GMGN — mana yang bagus buat gw pakai?"*
Same job as platform DD, different scorecard: the axes that decide money are **what you can track
(arbitrary address vs platform users), alerts + latency, copy-trade / automation, official API for
your own agent, chains, fees, custody, and the incident record**.

## The three findings that decided it

1. **Fomo is not a wallet tracker.** You cannot paste an on-chain address to watch — "following"
   means following *app users* inside their feed/leaderboard, the follow count is capped by your own
   app activity, spot price alerts don't exist (perps only), and the vendor's own help centre states
   *"fomo does not have a copy trading feature"* (loop = follow → notification → DYOR → trade
   yourself). The same page also documents Apple/Google-only signup. ⇒ eliminate it from a
   tracker shortlist; it competes on mobile onboarding + social feed, not tracking.
2. **Axiom: great tracker, but the automation layer and API are not documented by the vendor.** Its
   own docs (`docs.axiom.trade`) list Wallet Tracking (add wallet → live alerts on charts, BullX
   import), Trader Scan, Tweet Monitor, Pulse, perps — and, checked by grepping
   `docs.axiom.trade/llms-full.txt`, have **no** "copy trade", no webhook and no public API.
   Third-party sites claiming "Axiom copy trading" are affiliate/SEO pages — one of those domains
   (`axiompro.app`) was flagged as a phishing site by PhishDestroy (Oct 2025). Its Feb 2026 incident
   (ZachXBT: staff used an internal "god mode" dashboard to read users' wallets **and their tracked
   -wallet lists** for ~10 months) is directly relevant when the product's job is holding your
   watchlist: funds were never at risk (Turnkey, non-custodial), but the watchlist was.
3. **GMGN wins on tracking + automation.** Tracking/following/alerts are free (1% only when you
   trade — vendor blog, Jun 2026), wallet detail carries PnL 7D/30D, win rate, avg hold time and
   anti-phishing metrics (blacklist hits, "sold > bought", buy/sell within 10s = bot), plus Wallet
   Radar (scan up to 10 tokens → earliest / most-profitable / shared-holding wallets → import to
   tracklist or copy trade), 0-Delay Telegram bot push, copy trade with TP/SL + safety filters,
   ~10 chains, and an **official Agent API / MCP + skills** — the only one of the three you can wire
   into your own agent. Caveats: 1% flat (no cashback), non-extension signup uses a
   GMGN-managed hot wallet with private keys not exportable per its TG-wallet docs, 2FA + whitelist
   + 3h wait on first withdrawal, thin team disclosure, and heavy phishing-clone surface (Oct 2025:
   BNB anti-MEV failure 729 txns + a phishing attack ~107 users, both reimbursed).

## Verify a terminal's feature claim (do this, don't recall it)

```bash
curl -s https://docs.<product>/llms.txt          # index; then append .md per page
curl -s https://docs.<product>/llms-full.txt -o /tmp/d.txt
grep -o -i -n "copy.trade[a-z ]*" /tmp/d.txt | head     # vendor-documented, or absent?
grep -o -i -n "webhook[a-z ]*"  /tmp/d.txt | head
```
Absent from the vendor's own index ⇒ write "not documented by the vendor", never "the product has
it". Then check the domain you found the claim on (phishing flags) before repeating it.

## Wiring GMGN into an agent (verification harness)

```bash
npm install -g gmgn-cli          # npm prefix is user-local here → no sudo; v1.6.6 current
gmgn-cli config --check          # exit 0 = API key present and usable
gmgn-cli track smartmoney --chain sol --limit 3 --raw   # live smoke test (exist auth = API key only)
```
- Credentials live in `~/.config/gmgn/.env` (`GMGN_API_KEY`; add `GMGN_PRIVATE_KEY` from
  `~/.config/gmgn/keypair.pem` only when a **signed-auth** route is needed).
- **Auth split:** `track follow-tokens` / `kol` / `smartmoney` need the API key only;
  `track follow-wallet` (the wallets the user personally follows on GMGN) needs the private key too.
- If a key looks right but calls 401/403, check IPv6 first (`curl -s https://ipv6.icanhazip.com`) —
  GMGN's API is IPv4-only.
- The vendor's own skill docs (shipped with the CLI) list per-route rate-limit weights and the
  upgrade URL for paid tiers; respect them instead of retry-spamming.

## Verdict pattern that worked

Recommend the tracker that is **automatable with what the user already runs**, then keep a second
terminal for execution only. State plainly which claims were verified against the vendor's docs vs
which came from affiliate pages, and warn about clone domains (`gmgn.ai`, official bots
`@GMGN_vip_Bot` / `@GMGN_sol_bot*`; `axiom.trade`, not lookalikes).
