---
name: priors
description: Give an AI agent a credit history on Priors — register an ERC-8004 identity, get a line (a $5 treasury invite, a $25 Ethos lane line, a line its owner's own $PRIORS stake opens, a backer, or a stock line against the agent's own stock tokens), borrow, repay, and earn a public trust score on Robinhood Chain. Use when the user wants to give their agent credit, reputation, a trust score, an ERC-8004 identity, wants to borrow, repay, pay x402 APIs on credit, or look up an agent's record on Priors (priors.trade).
---

# Priors: give your agent a credit history

Reviews are cheap to fake. Repaid debt isn't. Priors lends unsecured stablecoin ($5 to $500) to agents
registered on [ERC-8004](https://eips.ethereum.org/EIPS/eip-8004). Every line is backed, dollar for dollar, by
someone who put money behind that agent, and every repayment and every default is a public event. From those
events comes a score anyone can query before trusting an agent.

Your job in this skill is to take an agent from nothing to a real, on-chain, repaid loan.

**Priors v2 is live on Robinhood Chain mainnet (chain 4663).** The v1 pool is paused. Know which one you are
talking to:

| Situation | What works |
|---|---|
| Robinhood Chain, v2 (`npx priors-v2`, `deployments/4663.v2.json`) | Everything, at real speed, with real USDG. **This is the one to use.** |
| Robinhood Chain, v1 (`npx priors`, `deployments/4663.json`) | Reading history only (`score`, `report`, `loans`). The pool is paused: new lines and loans revert. |
| Local dev chain (31337, from `npm run devnet`) | The v1 flow, instantly, with mock USDG and warped time. Good for a demo; nothing there is real. |
| A chain with no deployment record | Nothing on-chain. Say so — do not pretend otherwise. |

⛔ **Never invent a pool address, never send an agent to the paused v1 pool, and never tell a user their agent is
registered or has a line when it does not.** The tools resolve addresses from the deployment records and refuse to
guess; when they refuse, say it plainly.

## Step 0: a key, and a funded wallet

```bash
npm install
cp .env.example .env     # set PRIORS_KEY=0x... (the key that owns, or will own, the agent's identity)
npx priors-v2 status
```

Run every `npx priors…` command from inside this repository's clone: there it runs the repository's own CLI. Outside
it, `npx priors` is an unrelated npm package and `priors-v2` on npm is only a placeholder that prints these
instructions, so never run them with the key set anywhere else.

⛔ **The key goes in the environment or `.env`, never on the command line.** The CLI refuses a key passed as an
argument (it would land in shell history) and never prints it.

The wallet needs a little native gas, 5 USDG for the bond if you take a self-service invite (step 2), and, for
step 3, enough USDG to pay the fee (about $0.023 on $5 for 14 days).
`RPC_URL` defaults to Robinhood Chain's official endpoint; it takes a comma-separated failover list.

## Step 1: identity

```bash
npx priors-v2 join
#  -> registered agent #6301 for 0x…
```

`join` registers an ERC-8004 identity for this key if it owns none, and prints its id. **Already have an
identity?** If it was minted before the v2 deploy (for example a v1 agent), or transferred to this key, set
`PRIORS_AGENT_ID=<id>`; v1 records were imported, so its history is already there. Only an identity minted to the key
that never left it is picked up on its own: one someone else sent it, or one that came back to it, may carry their open
loan, and `repay` leaves a loan the agent's owner now did not take.

**No clone?** `@priors/mcp` 0.12.1, started with `PRIORS_JOIN=on`, offers a `join` tool that does the same for its
wallet (one transaction, its gas in the wallet's ETH) and answers the id and the routes to a first line.

⛔ **Use the id this command printed, not the one in these examples.** One identity, one record, forever.

## Step 2: a line

Five ways, and every one needs the agent owner's signature (the pool consent), which `join`, the SDK or Go mode signs
for you. Seats are not a way in: the growth seat vault (SeatVaultV4) takes no new seats since 2026-10-09, and the
seats already open run until they close.

```bash
npx priors-v2 join --invite priors-invite:<id>:<expiry>:<signature>   # treasury v4: $5
```

- **Invite.** Ask at [priors.trade/invite](https://priors.trade/invite) for an invite **for the id from step 1**.
  An invite names one agent id, expires, and seats that agent once. The self-service invite needs a 5 USDG bond in
  `InviteBond` from the wallet that owns the agent, and proof of ownership to the invite bot (that wallet signs the
  bot's message on the same page, or on Telegram); the bond comes back
  once the agent closes its treasury line with no loan open (since 2026-10-12), or after 4 days if the agent never
  gets a line, and goes to the Safe on a default. Otherwise an admin approves the invite.
- **Ethos lane.** A new agent (no Priors record yet) whose owner proves a wallet with an Ethos score of 1400 or more
  gets a $25 line from the lane's root, with no bond and no invite. The owner takes it on Go mode's Start page
  ([go.priors.trade/start](https://go.priors.trade/start)), signed in with the account that owns the agent; the lane
  checks the score and its room for the day before anything is spent.
- **The owner's $PRIORS (SeatVaultV5).** The agent's owner, and only its owner, stakes its own $PRIORS behind the
  agent as collateral, in Go mode's Back agents ([go.priors.trade/account](https://go.priors.trade/account), the Seats
  tab), signed in with the account that owns the agent. The stake opens the line; the line itself is 100% USDG from
  SeatVaultV5's root, $25 to $50 to start, and it grows by steps up to $500. Loans on it last at most 10 days. V5 opens
  no line while a loan is open, and the agent's current line ends as it opens. On a default, 75% of the stake burns.
  There is no CLI subcommand: Go mode shows the exact line before the owner confirms.
- **Backer.** A root backer can vouch any size, with your signed consent (`signConsent` in the SDK).
- **Stock line.** Deposit one of the 35 accepted Robinhood stock tokens and the stock vault vouches 25-70% of its
  value by token (plus up to 15 points for a record of repaid treasury credit), at most $500. New loans follow the
  collateral's value now, and a default seizes what is owed plus a 20% buffer and gives the rest back. There is no CLI subcommand: use the SDK
  (`stockAssets()`, `openStockLine(agentId, token, amount)`, `closeStockLine(agentId)`); see the README's
  "Stock lines".

Ways it legitimately fails, and what they mean:

- **`EpochCapReached`** — treasury v4 has spent its $100 of new lines for this 7-day epoch. Wait, or take another
  way above (the Ethos lane, the owner's $PRIORS, a backer or a stock line). Do not retry in a loop.
- **`NotInvited` / `InviteExpired` / `InviteUsed`** — the code is wrong, stale, or spent. Ask for a new one. There
  is no path around the invite; that is the gate working.

## Step 3: borrow, hold, repay

```bash
npx priors-v2 borrow 5 --days 14   # -> loan #N, $5 lands in the wallet, due date printed (14 days is the default)
#  ... the agent does its work ...
npx priors-v2 repay --all          # principal + fee; approves USDG for exactly what is due
```

The CLI records every transaction it signs (one private file each, synced to disk) **before** sending it, sends it as
one request that is never retried, and holds a lock per key, so a second command of the same key waits its turn (exit
3) and a killed command leaves its record. One killed before it sent anything is recorded as unsent: `npx priors-v2
tx` drops it (it never sends an unsent one).
If `borrow` exits with **code 4**, or was killed, the borrow may have opened a loan or may still be pending, so
`status` showing no loan proves nothing yet. The CLI refuses `borrow`, `join`, `raise` and `move` until the record is
settled; `repay` still runs. Do not run `borrow` again: run `npx priors-v2 tx` (no argument: it reads what the CLI
recorded) until it says final (exit 0; exit 3 means not final yet, check again in a few minutes). Its verdicts:
- **mined**: it ran. This includes a fee-bumped copy (a speed-up: the same call at the same nonce with another hash)
  that succeeded. Never borrow again for it; `npx priors-v2 status` lists the loan: repay it before its due date.
- **reverted** or **replaced** (a different call used its nonce): it did not run; borrow again once it is final.

A verdict is final only once its block is finalized and still canonical; until then `tx` says "waiting for finality"
and keeps the record. A hash the node does not know is never final: `npx priors-v2 tx --resend` sends the same signed
transaction again, which cannot make a second one. The public node keeps only minutes of history, so `tx` remembers
what it saw and asks the explorer for a pointer (checked on the RPC, never trusted alone). If neither can say which
transaction used the nonce, `npx priors-v2 tx --forget` drops the record once that nonce is in finalized history: it
prints the open loans and explorer links first, because whether the borrow ran is then unknown; check them before
borrowing again. It refuses while the nonce is free. Exit code 1 means the step that failed did nothing (refused,
reverted or cancelled); a revert or cancel that mined stays recorded until `tx` shows it final.

**Hold it for real time, then repay at or before the due date.** The score is dollar-days: how much you borrowed
times how long you held it, capped at the term you contracted for. A loan shorter than **7 days** repays fine but
does not count as a qualified loan. Take 14 days: hold it a week, then repay any time before its due date. A 7-day
loan counts only when repaid at or after its due time, the moment Score v2 starts counting a repayment as late (from
weights 2.0.3, on 2026-11-02, only after 24 hours more); `borrow` says so before it borrows for 7 days or less.
Churning one-day loans gets you nowhere; that is deliberate. On a line the owner's $PRIORS opens (SeatVaultV5), a loan
lasts at most 10 days (`BorrowBlockedByBacker` above that): `borrow` takes 10 there by default and refuses a longer
`--days` before sending anything. Borrow for 8 to 10 days and hold it a week or more; that is also what V5 counts
toward its next step.

⛔ **Repay before the due date.** Three days past due and *anyone* can mark the loan defaulted. The record is
defaulted forever, the identity can never borrow again, the owner's address is marked, and the sponsor pays (its
shares burnt, or 75% of the owner's $PRIORS on a SeatVaultV5 line). There is no appeal. If the user cannot repay
on time, tell them to borrow less, not to borrow later.

## Step 4: grow

The raise is on treasury v5 since 2026-10-14 (treasury v4 raises nothing): it tops a treasury line up to $25 once the
record has 3 qualified loans, 14 days, a score of at least 100 and no default.

```bash
npx priors-v2 move     # an agent on a treasury v4 line: moves it to treasury v5, then raises it
npx priors-v2 raise    # an agent already on treasury v5's line
```

`move` leaves the v4 line, takes the InviteBond back, posts the owner's 5 USDG `InviteBondV2` bond (it stays as long
as the agent holds a line) and moves the agent, sending only the steps not done yet: after a failure, run it again.
It refuses, with nothing sent, while a loan is open, before the record qualifies, or until the v1 bond is 4 days old.
Beyond that, v2 has no unbacked "earned" credit: a bigger line comes from a backer, a stock line or the owner's
$PRIORS (whose line grows by steps).

## Paying x402 APIs on credit

`sdk/float.mjs` pays a `402 Payment Required` in USDG from the agent's balance and borrows only the shortfall from
its line. Always set `maxBorrow` to what the agent can repay within the term, and never call `pay()` again for a
purchase whose result (or error) carries a `paymentHeader` without `paid` (pending, a dropped connection, a timeout):
the merchant can still cash it until `validBefore`. Send that same payment with `priors.resend(url, paymentHeader)`.
See `docs/FLOAT.md`.

## Reading any agent's record

```bash
npx priors-v2 status               # this key's agent: line, loans, record
npx priors report <agentId>        # v1 history (paused pool)
```

On v2, `score(uint256)` and `creditReport(uint256)` are on `CreditLensV2` (address in
`deployments/4663.v2.json`). From JavaScript:

```js
import { resolveV2 } from "priors/env";
const { priors } = await resolveV2();
await priors.status(agentId);
```

## Doing it from code instead of the CLI

`sdk/priors-v2.mjs` is the v2 client on ethers v6 — `register`, `signConsent`, `redeemInvite`,
`quoteFee`, `borrow`, `repay`, `openLoans`, `status`, plus `pay`/`settleLoans` for x402 and `stockAssets`,
`stockPosition`, `openStockLine`, `addCollateral`, `closeStockLine` for a stock line. `sdk/env.mjs`'s
`resolveV2()` resolves chain, deployment and signer the same way the CLI does. Every write is simulated first and
a revert is decoded to the contract's own error. Prefer these over hand-rolling calls.

## What not to claim

- **Do not call this audited.** v2 had internal adversarial reviews and no third-party audit. Every known finding,
  its fix and what remains is in `docs/SECURITY-v2.md`.
- v1 shipped with a lender-loss defect that randomized invariants did not catch; it was found, fixed and migrated.
  v2's design (every line fully backed, a default burns the backer's shares) is why no path to lender principal
  was found — that is still not a proof.
- Do not tell a lender they cannot lose money, and do not tell a backer or staker their stake is safe: backers and
  stakers carry the credit risk by design.
- The owner's $PRIORS behind a SeatVaultV5 line is collateral the owner posts, never a return, and only the agent's
  owner can stake behind it: do not say anyone else can.
