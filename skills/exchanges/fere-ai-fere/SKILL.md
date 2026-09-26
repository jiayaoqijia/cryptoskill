---
name: fere
description: Move real money on-chain through FereAI with a single wallet — yours, or one agent's. Swap and bridge on 7 chains with server-side take-profit/stop-loss, trade Hyperliquid perps and spot, bet on Polymarket, park USDC in a yield vault, all behind one key or the MCP connector. Use when the user says "fere", "my wallet", "agent wallet", "gasless swap", "buy this token", "swap", "bridge", "stop loss", "take profit", "limit order", "perp", "Hyperliquid", "Polymarket", "onchain yield", "check my holdings", "custodial vs non-custodial", or wants to trade with real money from code or chat. For giving every end user of a product their own wallet, use the fere-multitenant skill instead.
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/fere.py *) Bash(${CLAUDE_SKILL_DIR}/scripts/test_fere.py *) Bash(mkdir *) Bash(ls *) Read Write Edit
---

# Fere — the money layer for one agent

FereAI is a **wallet + execution API behind one bearer token**: register an Ed25519
keypair, get an EVM address and a Solana address, and swap, bridge, arm stop-losses,
open perps, buy prediction-market shares or earn yield through the same auth. No
email, no KYC, no dashboard, no gas token, no signing code.

> **One wallet, or one per end user?** This skill is the single-wallet path — your own
> money, or one agent's. Building a product where every user gets their own wallet (and
> their own HL account and Polymarket Safe)? That is **`/fere-multitenant`**.

The user's request is: **$ARGUMENTS**

If `$ARGUMENTS` is empty, ask what they want to set up or trade. Otherwise: pick the
lane below, read the one reference file it names, then act.

> **Real money.** Everything here except `quote`/`dryrun` moves funds that cannot be
> withdrawn to an outside address. Before the first live call in a session, say what
> will move, from which wallet, and how much — and get a yes.

---

## 1. Which door: MCP or REST?

| | **MCP connector** (`fere_*` tools) | **key-auth REST** (`scripts/fere.py`) |
|---|---|---|
| Who | *you*, in Claude/Cursor/ChatGPT — research, one-off trades on **the human's own account** | *code* — a script, a bot, CI; also the substrate `/fere-multitenant` builds on |
| Auth | Clerk OAuth, or an `agt_*` bearer for headless use, against `https://api.fereai.xyz/mcp` | Ed25519 → `agt_*` bearer, 1 h |
| Wallets | exactly one pair — the account's | one pair per agent; more wallets = more agents |
| Polymarket | ✅ 12 tools, incl. discovery + live prices (but `fere_polymarket_setup` posts `/setup/v2`, which fails on a fresh agent — let `fere_polymarket_account` run setup) | ✅ **own Safe per agent** via the `/polymarket/*` routes; no discovery/price tools |
| Hyperliquid | ✅ perps + spot on that one account | ✅ **own HL account per agent** (`min_fund_usd` 50 — **fund first; fund runs setup itself**; setup on an empty account fails `HYPERLIQUID_NOT_FUNDED`) |
| Task polling | ❌ no task tool → **confirm every fill by holdings diff** | ✅ `GET /v1/tasks/{id}` (still diff holdings; **poll with a deadline** — an id that was never issued is `200 PENDING` forever) |

**If both are available, prefer MCP for the user's own money and the CLI for anything
multi-wallet.** They are the same backend; a wallet made by one is invisible to the
other unless you hold its key.

## 2. Minutes to a funded wallet

Run these from this skill's directory. Paths are `scripts/…` next to this file.

```bash
python3 scripts/test_fere.py                  # 22 checks, ~6 s, no money — run this first
python3 scripts/fere.py new alice             # register → prints the EVM + Solana address
python3 scripts/fere.py ls                    # every wallet you own
python3 scripts/fere.py holdings alice        # balances across all chains AND venues
python3 scripts/fere.py poly setup alice      # alice's own Polymarket Safe (~5 s)
python3 scripts/fere.py perp status alice     # alice's own Hyperliquid account (setup needs $50 in it FIRST)
```

Send funds to the printed addresses (**any liquid token, no gas coin needed**), then:

```bash
python3 scripts/fere.py quote alice --chain base --in USDC --out 0x<token> --usd 10   # dryrun
python3 scripts/fere.py buy   alice --chain base --in USDC --out 0x<token> --usd 10 \
        --tp 1.0:0.5 --sl 0.3:1.0 --i-understand-this-moves-real-money
```

That last call arms a server-side +100 % take-profit on half and a −30 % stop on the
rest, then **confirms the fill by diffing holdings** and exits non-zero if it can't.
The keyring lives at `$FERE_HOME` (default `~/.fere/agents.json`, 0600) — **that file
is the login**; back it up, never commit it, never print it.

> **Provenance.** Live fills have gone through both the MCP connector and the key-auth REST path. `fere.py buy` itself has not carried a live fill in our hands yet. Run one funded $10 round trip through your own path before it touches money you care about.

## 3. The six rules that cost real money to learn

1. **A fill is a holdings delta. Nothing else.** `status` lies both ways and
   `message` is a hardcoded constant (`"Swap task queued successfully"` sits next to
   `status:"failure"`). Snapshot → swap → poll task → **re-read holdings 3× over 15 s**
   and diff. `FAILURE` + delta > 0 means filled; `SUCCESS` + delta == 0 means
   *unconfirmed* — show pending, never auto-retry. **Every read in that diff must be
   `GET /v1/holdings?event=wallet-refresh`**: a plain read can be Fere's saved answer,
   and an empty wallet's answer is kept up to **45 min** and never re-checked
   (`reference/spot.md` § Holdings). `fere.py` always refreshes.
2. **Only `"Balance validation failed"` and a 4xx are definitive failures** (Fere
   validates balance before routing, so nothing ran). Everything else can fill late.
   Two corollaries from the sweep: **every venue write returns HTTP 200 with a
   `task_id` even when it cannot succeed** (perp with no collateral, HL spot with no
   setup, a Polymarket order with no cash) — the task is the verdict, the status code
   is not; and a task whose error names a precondition (`Hyperliquid setup not
   complete`, `Minimum … withdraw is $6.00`, `Insufficient Polymarket cash balance`,
   `BELOW_MINIMUM`) is definitive too. **Always poll with a deadline**: `GET
   /v1/tasks/{id}` answers `200 PENDING` forever for an id that was never issued, so
   "poll until terminal" never terminates on a typo.
3. **A timed-out write is UNKNOWN — read, never re-send.** `idempotency_key` is accepted but **not enforced**: one key produced three filled swaps because the client re-sent on a read timeout. A ConnectError is safe to retry (nothing was sent); a ReadTimeout is not.
4. **One on-chain action in flight per wallet, ≥3 s gap.** Parallel sends produce
   mempool nonce errors. `fere.py` takes a per-wallet lock and queues; keep that.
5. **Hooks re-base on Fere's price at registration, not your entry, and they decay.**
   Arm them inline at buy, then reconcile `holdings[].outstanding_orders` on every
   poll against your own expected-exits table and re-arm what vanished.
6. **Fere is execution + balances. Prices come from your own feed.** The one
   exception is `fere_polymarket_prices`, which reads the live book.

Min notional **$5** (HL: $10 per order, **$6 to withdraw** from HL; Earn **$100** to
deposit *and* to withdraw) — `fere.py` enforces the $5 on `--usd`, but a raw `--amount`
in smallest units is passed through unchecked, so size that path yourself. Default `slippage_bps` 300, 500 on thin books.
All-in cost same-chain runs **57–70 bps per leg**; budget 60–100. Bridging into Robinhood Chain tolled
**2–8 %, variably** — deposit per chain instead of bridging on the buy path.

## 4. Pick the lane

| The ask | Read | Surface |
|---|---|---|
| Wallets, keys, recovery, custody, no-CORS, gasless | `reference/wallets.md` | `fere.py new/ls/key/import/recover` |
| **Putting this in a consumer product** — the passthrough allowlist, CSP for a key-holding page, `prepare`/sizing, the fill rule, the funding journey | `reference/consumer-app.md` | your own `/api/fere/{path}` |
| A wallet per end user; replacing Privy/Turnkey/CDP | the **`/fere-multitenant`** skill | same CLI, keyring of N agents |
| Buy/sell a token, bridge, TP/SL, limit orders, honeypot check | `reference/spot.md` | `POST /v1/swap` · `fere_swap` |
| Perps, leverage, funding, HL spot | `reference/hyperliquid.md` | `fere_perp_*` · `fere_spot_hl_*` |
| Prediction markets, event odds, redeem | `reference/polymarket.md` | `fere_polymarket_*` · `/polymarket/*` (discovery + prices **MCP only**) |
| Park idle USDC | `reference/earn.md` | `fere_earn_*` · `/v1/earn/*` |
| Migrating off Privy / Turnkey / CDP, or deciding whether to | `/fere-multitenant` → its `reference/vs-privy.md` | — |

## 5. What Fere cannot do — design around these

- **No withdrawal or transfer to an arbitrary address.** Money leaves only by swapping
  or by exporting the key in the web app (no API export for key-registered agents). **Size
  every deposit as capital you are committing.** A stolen key or bearer can't *transfer*
  funds out either — but it can swap them into anything, including a token the thief
  controls, so treat a leak as a loss, not a contained incident.
- **No end-user auth.** There is no email/passkey/social login and no consent screen.
  Your product owns identity; Fere only knows keys. (See Custody in
  `reference/wallets.md`, and `/fere-multitenant`'s `reference/vs-privy.md`.)
- **No CORS.** A browser cannot call `api.fereai.xyz` directly; put a stateless
  method+path-allowlisted passthrough in front and keep `/v1/chat` denied (the one
  endpoint known to burn credits, 15 per query).
- **No sub-accounts.** One wallet pair per agent. More wallets = more agents.
- **No Polymarket discovery or live prices outside MCP.** Every *trading* route works per
  agent, but `markets`, `prices` and `whale_data` are MCP-only conveniences — read
  `gamma-api.polymarket.com` / `clob.polymarket.com` directly instead (fresher anyway).
- **No published fee schedule**, no per-agent spend policy, and registration rate
  limits are unknown — don't promise "unlimited wallets" to anyone.

## 6. Cost

Reads, dryruns, hook and limit-order registration, security checks, Polymarket setup
and every *failed* venue write burn **0 credits**. A fresh
agent gets **200 credits that expire in 14 days**; packs are $5→300, $10→650,
$20→1,400, and `GET /credits/packs` + `GET /credits/recharge-chains` answer an `agt_`
bearer, so an API agent can at least *see* the recharge path (`POST
/credits/onchain-recharge` is the buy — untested). Live swaps, perps and CLOB fills
also burned **zero** credits. Still open: whether an agent whose
200 free credits expired at day 14 can still trade. Read `GET /v1/credits` around your own and
write the number down.

## 7. Portability

This folder is self-contained: it lives at `skills/fere/` and is installed with the
plugin in this repo. `scripts/fere.py` needs only `httpx` plus `cryptography` (or
`pynacl`), reads proxies from the environment, and keeps its keyring outside the repo.
Nothing here imports anything else from this repository. Run `scripts/fere.py` from
this directory.

`allowed-tools` grants `Bash(${CLAUDE_SKILL_DIR}/scripts/fere.py *)`, which Claude Code
expands to this folder wherever the plugin is installed. The `fere_*` MCP tools come
from a connector, not this folder — add it with

```json
{"mcpServers": {"FereAI": {"type": "http", "url": "https://api.fereai.xyz/mcp"}}}
```

which authenticates by Clerk OAuth in the client. The same endpoint also accepts an
`Authorization: Bearer agt_…` header, which points MCP at a wallet you made with the
CLI (headless mode in the README).

## 8. If something looks broken

`python3 scripts/test_fere.py` from this directory first — it separates a Fere outage
from your bug in under six seconds. A `holdings` 502 blanks the *whole* response from
one bad upstream: retry 3× with backoff, keep the last-good snapshot for **display
only**, and never trade off a stale one.

**A deposit confirmed on-chain but missing from holdings** is Fere's saved answer, not
lost money: read once with `?event=wallet-refresh`. Funding and swaps validate against
the chain, not that list, so they already work (a $100 USDC deposit on Base once stayed invisible
for ~40 min to plain polls while `perp/fund` moved it first try — Fere's RCA).
