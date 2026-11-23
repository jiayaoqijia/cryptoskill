---
name: agent-marketplace-selling
description: Use when selling services or skills on an agent marketplace.
version: 1.0.0
author: Hermes Agent
license: MIT
triggers:
  - termix
  - agent.family
  - jual jasa agent
  - agent marketplace
  - listing jasa AI agent
metadata:
  hermes:
    tags: [crypto, agent-marketplace, termix, income, listing]
    related_skills: [agentic-wallet-ops, external-skill-adoption, hermes-cron-automation]
---

# Selling services as an agent

Covers any agent-to-agent job marketplace: vetting it, installing its bundle safely, activating an identity,
publishing a listing, and keeping the delivery clock. Termix / agent.family is the worked example.

## When to Use

Do asks to vet, join, or sell on an AI-agent marketplace ("coba cek legit ga buat dicoba", "gas daftar"),
asks to fix a listing, an order flow, or a marketplace watcher, or wants a repository turned into a
sellable skill listing on a marketplace that ships `SKILL.md` packages (Agensi and similar). Also when a
tweet promotes a marketplace skill for agents.

Not for mint/drop screening → `agentic-wallet-ops`. Not for installing an arbitrary GitHub skill →
`external-skill-adoption`. Not for what to trade → `crypto-portfolio-advisory`.

## Step 0 — What the marketplace sells decides the packaging

Two shapes exist and they are not interchangeable. A **service marketplace** (Termix / agent.family) sells
jobs delivered by this agent, so the listing is a profile plus an order watcher. A **skill marketplace**
(Agensi) sells a ZIP of text files that the buyer's own agent executes, so the deliverable is a
self-contained script and instructions, and there is no delivery clock to watch.

Before promising anything, settle which shape you are in and read the marketplace's packaging rules. On a
skill marketplace the hard constraints are structural, not stylistic: the script runs alone from a temp
file, no dependencies, text output only, `SKILL.md` at the zip root. A repository that only runs against
the author's sealed data or a vendored challenge kit is not listable until it is rebuilt — see
`references/agensi-skill-marketplace.md` for the audit order, the rebuild shape, the 70/30 economics and
the clean-room test.

## Step 1 — Vet the marketplace before installing anything

1. **Pull the protocol's own stats endpoint, not the landing page.** Marketing pages render `--` placeholders
   while the API answers real numbers; the API is the only thing you can quote. Termix:
   `GET https://platform-backend.prod.termix.live/api/v1/stats/network` (volume, jobs, providers, clients,
   open offers, avg new jobs/day, latest block).
2. **Cross-check the vanity number against what top earners actually take home.** A "N verified agents" counter
   that dwarfs the job count is inflated; the leaderboard and featured-provider endpoints give the real
   ceiling. State that ceiling in dollars per week before he asks, because it is the actual decision input.
3. **Check stake-lock fields before repeating any "stake backs the risk" claim.** A protocol-wide
   `vaultLockedUsd` of a few dollars means the stake story is marketing, not protection.
4. **Look for backing and an audit report** (investor name in the footer, third-party audit PDF). Then decide:
   sell as a provider = zero capital, or skip.

## Step 2 — Inspect the vendor bundle before it touches the agent

Never install a marketplace skill straight from a tweet. Download, unpack, read:

```bash
curl -sSL "<bundle-url>" -o pkg.bin && file pkg.bin && unzip -o -q pkg.bin -d x
find x -type f | head -40
grep -rIn -E "private.?key|mnemonic|seed phrase|curl .*\| *(ba)?sh|base64 -d|eval\(|\.env|approve\(" x | head -20
grep -rhoE "https?://[a-z0-9.-]+" x | sort | uniq -c | sort -rn | head
```

The four answers that matter: where keys come from, which hosts it talks to, whether it approves or transfers
anything, and whether a keyless path exists. If the bundle supports keyless auth (browser wallet sign-in, or
the Binance Agentic Wallet via `baw`), that is the only mode to use — say so explicitly, and never switch on a
`WALLET_KEY` / key mode "to make it work".

Install under the skills tree and prove it with ONE read-only command (`GET` a public stats route) before any
account step.

## Step 3 — Identity: reuse what the wallet already holds

List the identities the wallet can already claim before minting anything. On Termix an existing Binance Agent
ID is **activated free, with no transaction and no gas**, and that ID *is* the agent — orders, stake and payouts
resolve through it. Minting a fresh `.agent` identity costs gas and buys nothing extra. Check first
(`GET /api/v1/me/agent-ids`, or the skill's `next` command), then activate.

## Step 4 — The profile is one-shot: draft, show, then write

Activation writes `displayName`, `description`, `category`, `tags` **once**; re-activating an active ID returns
`activated: false` and changes nothing. Order: draft the profile → show it → activate.

- `category` is a strict enum (Termix: `Code & Smart Contracts`, `Security & Verification`, `Data & Research`,
  `Design & Brand`, `Writing & Content`, `Automation & Ops`, `Market & Protocol Research`,
  `Model & Dataset Ops`). Anything else is a 400.
- Write only what he can actually deliver, phrased as the deliverable. No invented clients, volumes or results.

## Step 4.5 — Decide WHAT to sell from live demand, not from imagination

The obvious listing is the one everyone posts and nobody buys. Measure both sides before writing a word:

1. **Sample the supply and price it out.** `GET /api/v1/listings?page=1..3&pageSize=100 --auth none` (auth none
   works; query params are strict). Count listings per category and take the price quartiles. If the intended
   category is 30+ listings deep with a median near the platform average and a floor of $1–5 filler, a generic
   version of the same offer is invisible — that is the finding, say it before he asks.
2. **Read the actual paid requests.** `GET /api/v1/prepayment-orders/discover --auth session` (paginate; `?limit=`
   is a 400). Read titles *and* budgets. What buyers pay for on these marketplaces is **verifiable execution**
   — boot this repo, match this contract source, supply liquidity and confirm the position, check a role via
   bot — not opinions, not market commentary. A research-brief listing competes with $1–5 noise; an
   execution-with-proof listing competes with almost nobody.
3. **Pick the category the buyer browses for the outcome**, not the one closest to what you studied. A
   verification deliverable belongs in `Security & Verification` even if the work started as research.
4. **Put the differentiator in the title**, not only in the description: "verified state + re-runnable evidence"
   beats "research brief" because it answers the trust question the buyer already has.
5. **Size the demand honestly.** Open requests can number in the low tens; the money is in being found and
   trusted (instant buy, samples, badge), not in racing a queue of requests. Never imply an order backlog.

Price only after the offer is chosen (next step). What each offer should promise, and how to physically deliver
evidence instead of prose: `references/proof-pack-deliverable.md`.

## Step 5 — Publish the listing

1. **Cover image is a hard prerequisite.** Get a presigned URL, PUT the file, then confirm the returned
   `publicUrl` answers HTTP 200 with the right byte count before creating the draft — a listing without a real
   cover is rejected with 400.
2. **Build the cover yourself when there is no asset**: dark background, accent bar, headline, three chips, a
   stylised candle card; then look at it with vision before upload. Fix text/collision/clipping at thumbnail
   size — a chart card running into the pill row reads as accidental.
3. **The schema is strict**: unknown keys are a 400 (`Unrecognized key(s) in object`). Write the body to a file
   and pass `--body "$(cat body.json)"` instead of fighting shell quoting.
4. **Publishing is off-chain and free.** `instantBuyable: true` lets a buyer start the delivery clock with no
   conversation — enable it only when the Step 7 watcher runs.
5. **Price as a ladder, never as one number.** `packages[]` gives 1–6 tiers on one listing; use three: an entry
tier, the real offer, and a multi-scope tier. Put the entry tier in the **teens of dollars** — its job is to buy the
first completed order and review, not margin — and state plainly that it gets repriced once the first rating lands.
6. **The card label comes from `basePrice`, not from the cheapest package.** A ladder of 15/45/95 with
`basePrice:45` still advertises "from $45" and hides the hook behind a click; PATCH `basePrice` down to the entry
tier and re-read `priceLabel` to confirm the shop-window number.
7. **Justify the price with comparable settled work, not the category median.** A category median mixes $1–5 filler
listings and makes any real offer look expensive; what matters is what comparable work actually got funded at
(match this contract source, supply liquidity and confirm the position). Quote those figures, then place the offer
under them. Never drop to the $1–5 tier to compete — that is a different market and it signals unseriousness.

## Step 6 — Prove it is live

A marketplace app is a SPA, so `curl` returns a shell with no text. Verify in two layers:

```bash
curl -sS -o /dev/null -w "%{http_code}\n" "<public agent url>"     # routing exists
```

then render with the browser and read `document.body.innerText`: agent name, `Available now`, the service row
and `from $X` must actually appear. A JSON response is not a live listing.

The **API read is the authoritative assertion** (status, `priceLabel`, `packages[]`, samples) because the page is
just a view over it; use the render for presentation only. The SPA hydrates a second or two after load, so read
the DOM after a wait and re-read rather than concluding from the first snapshot.

The public app host is often **not** the marketing domain — probe the marketing site's `href`s to find it
(Termix: `termix.ai` 404s every agent path; the app is `agent.family/agents/<agentId>`).

## Step 7 — Never miss the delivery clock

A listing with `instantBuyable` is a promise measured in hours. The vendor skill's `wait` command long-polls and
returns the moment there is work, at zero token cost while blocked. Run it as a **persistent Hermes background
process with notify patterns on the event names** (`order.funded`, `chat.message`, `offer.received`),
`persist_on_release: true`:

```
export PATH=/home/ubuntu/.nvm/versions/node/v22.23.2/bin:$PATH
cd <skill-dir> && node scripts/aacp-watch.mjs wait --agent <agentId>
```

Do not wrap it in cron: a cron tick wakes a fresh agent that re-reads the skill whether or not there is work
(~40k tokens for nothing), while the poller is free. Vendor docs insist on a foreground blocking call; that
shape is impossible from a chat turn, so use the persistent background process and re-check it is alive when Do
asks about orders.

Accepting an order on-chain is a transaction: preview it, show the fields, wait for the explicit go.

## Pitfalls

- **Never probe an undocumented schema by inventing a shape once and giving up.** Send a minimal body, read the
  validation error, add exactly the key it names, repeat — the error chain (`packages.0.name: Required` →
  `packages.0.scope: Required` → `packages.0.delivery: Expected string, received number`) writes the schema for you
  in a handful of calls. Read the *type* half of the message: on Termix every price and duration is a string.
- **A probe failure inside a data-collection run must not abort the run.** ERC-721 contracts have no
  `decimals()` and every `eth_call` for it reverts; wrap each read and degrade that field (ERC-721 `balanceOf`
  counts NFTs, decimals 0) instead of letting one revert kill the whole evidence bundle. Same for a contract
  without `paused()`/`owner()`. An aborted run leaves a half-built bundle and no deliverable.
- **`samples[]` takes images only.** To show a PDF deliverable as a listing sample, render its first page to PNG
  (`pymupdf`, `dpi≈110`) and upload that with `purpose:"sample"`; a buyer never opens a PDF from a gallery.
- **`--help` is not safe on these CLIs.** Their parsers switch on known verbs and ignore unknown flags, so
  `a2a-runtime.mjs login --help` actually **logged in** and cached a session. Never pass an unsupported flag to
  a command that can sign or authenticate; read `docs/` for usage instead of probing with `--help`.
- **Verify the bundle's hosts.** A package calling `platform-backend.prod.<vendor>.live` while the site is
  `<vendor>.ai` is normal vendor infra — check the hosts resolve to the vendor, then say so, instead of calling
  it phishing and stalling.
- **Activation success is not verification.** The public profile can still read `Unverified`; that is a separate
  badge, not a failed activation. Say which one is missing instead of implying the account is broken.
- **Quote economics honestly and unprompted.** Top-provider weekly net, average job value, number of competing
  providers, and the fact that this is pocket money — before he starts imagining an income stream. Never
  restate marketplace marketing numbers as achievements.
- **Draft-then-publish is the safe split.** Creating a draft is reversible; publishing starts the SLA. Draft,
  show the deliverable text and the price, publish on his go.

Termix-specific commands, endpoints, field limits and error codes: `references/termix-aacp.md`.
Agensi/SKILL.md packaging, repo-to-skill audit, pricing anchors: `references/agensi-skill-marketplace.md`.
