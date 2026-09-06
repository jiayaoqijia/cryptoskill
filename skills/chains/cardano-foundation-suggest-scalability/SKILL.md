---
name: suggest-scalability
description: >-
  Decide whether a Cardano project needs Layer 2 / scaling at all, and if so which approach and topology fits — then route to the bundled implementation docs. Covers the L1-first sufficiency check (including the Leios throughput horizon), Hydra Head (the only mainnet-ready L2) vs Mithril vs in-development rollups (Midgard, Gummiworm), and Hydra topology selection (basic 2-party, delegated head, managed, star-shaped). Triggers: "do I need Layer 2", "which L2", "scale my dApp", "Hydra vs rollup", "Midgard", "Gummiworm", "state channel", "payment channel", "sidechain", "increase throughput", "sub-second finality", "which Hydra topology", "off-chain scaling", "reduce fees at scale".
allowed-tools: Read Grep Glob
disallowed-tools: Bash Edit Write WebFetch WebSearch
---

<!-- Documentation lookup path: ${CLAUDE_SKILL_DIR}/../../docs/sources/ -->

# Suggest a Cardano Scalability Approach

Help a developer decide whether their project needs Layer 2 / scaling, choose the right approach if it does, and — for Hydra — pick a topology, then hand off to the bundled implementation docs. This skill is the *decision layer*: Its job is to stop unnecessary L2 adoption and to route real requirements to the right shape.

## When to use

- Developer asks "do I need Layer 2 / a sidechain / a rollup for this?"
- Comparing scaling approaches (Hydra Head vs Mithril vs emerging rollups)
- A project has a *specific* throughput, fee, or sub-second-finality requirement and wants to know if L1 can meet it
- Choosing a Hydra topology (2-party channel, delegated head, managed, star-shaped)
- Someone is about to reach for Hydra by default and needs a reality check first
- Planning where a workload should live before committing to an architecture

## When NOT to use

- Choosing SDKs, on-chain languages, or general infrastructure — use `suggest-tooling`
- The scaling decision is already made and the developer needs to build — read the bundled Hydra docs directly (`${CLAUDE_SKILL_DIR}/../../docs/sources/hydra/`).
- Setting up a local devnet for testing — use `setup-devnet`
- Explaining the eUTxO model or L1 concurrency patterns (batching, UTxO indexing) — that is often the *real* fix instead of L2; cover it with `explain-eutxo` and `cardano-context`
- General "how does Hydra work" explanation — the bundled Hydra docs answer that better than a skill

## Key principles

1. **L1-first. Most projects do not need L2.** Cardano L1 handles the large majority of dApp workloads. Recommending L2 speculatively adds real operational burden (every participant runs and funds a node) for no benefit. The default answer is "stay on L1."
2. **Demand a real, confirmed requirement.** Only pursue L2 against a *specific, measured* throughput or latency need L1 cannot meet. "It might get big someday" is not a requirement.
3. **Rule out cheaper fixes first.** Many "throughput" problems are eUTxO contention, solved on L1 by batching, UTxO indexing, or multiple validator UTxOs — not by L2. Check this before scaling.
4. **Isomorphism is the payoff.** Hydra transactions use the same format, validators, and ledger rules as L1, so on-chain code ported into a head behaves identically. This is why Hydra beats a foreign execution environment when it fits.
5. **Never recommend frontier tech for production.** Emerging rollup-style L2s are "watch this space," not production choices. Say so plainly and verify their status upstream.
6. **Route, don't reimplement.** Once the shape is chosen, point at the bundled docs for the lifecycle, APIs, and config. Read them rather than answering node/tx details from memory.

## Workflow

### Step 1: Establish whether scaling is even needed

Interview only what you can't infer:

- **What is the bottleneck, concretely?** Throughput (tx/s), per-tx fee, confirmation latency, or node bootstrap/sync time? Each points to a different answer (and some to *no* L2).
- **Is the requirement measured or assumed?** Ask for the actual number. If there isn't one, the answer is almost certainly "stay on L1 and measure first."
- **Is the real problem eUTxO contention?** If the pain is "users collide on the same UTxO," the fix is usually an L1 design pattern (batching, UTxO indexing, multiple script UTxOs), not L2. Hand to `explain-eutxo` / `cardano-context`.
- **Who transacts, and with whom?** A *small and fixed* set of counterparties transacting among themselves is the signal for a state channel. A *large and variable* set of counterparties is the signal against one, or for a different scaling solution.

**The Leios horizon (context, not a dependency).** Ouroboros Leios is L1 throughput scaling (input-endorser pipelining) that raises Cardano's own tx/s ceiling substantially. It is protocol research, **not** something a dApp integrates, but it matters to this decision: a throughput requirement that L1 can't meet *today* may be met by L1 itself before a bespoke L2 pays off. For status and scope, read `${CLAUDE_SKILL_DIR}/../../docs/sources/ouroboros-leios/` (start with the latest `status-report-*.md` and `technical-report-*.md`). Treat it as a reason to be *more* conservative about adopting L2, never as a shippable component.

### Step 2: Search the bundled documentation

Ground scaling claims in the bundled sources rather than memory:

- `${CLAUDE_SKILL_DIR}/../../docs/sources/hydra/` — Hydra Head protocol (start with `docs/protocol-overview.md`, then `topologies/` and `use-cases/`)
- `${CLAUDE_SKILL_DIR}/../../docs/sources/ouroboros-leios/` — Leios L1-throughput research

Mithril and emerging rollups are **not** bundled as sources — verify their status upstream and flag them as such.

### Step 3: Choose an approach

| Approach | Type | Status | Reach for it when… |
|---|---|---|---|
| **Stay on L1 (+ design patterns)** | — | Production | The default. Requirement is unmeasured, low-frequency, or is really eUTxO contention solvable by batching/indexing. |
| **Hydra Head** | Isomorphic state channel (L2) | Production | A *known, fixed set of parties* transacts frequently among themselves, each can run a node and stay online. |
| **Mithril** | Snapshot certificates | Production | You need fast node bootstrap or light-client sync — **not** tx throughput. Often complements L1, not a scaling layer for dApp txs. |
| **Emerging L2** | Midgard / Gummiworm | Experimental | Not yet — none is mainnet-ready. See the breakout below. |


**Hydra fits when all of these hold:**
- The participant set is **small and fixed** (two payment counterparties, a fixed group of players, a set of auction delegates). A head is not a public network — parties are enrolled when the head opens.
- Those parties transact **with each other at high frequency** and want near-instant, zero-fee L2 confirmation.
- **Every participant can run a `hydra-node` and stay online** — the head only makes progress while participants are responsive (unanimous signing).
- Funds can be **committed** into the head and settled back to L1 on close (incremental commit/decommit move UTxOs in and out of a running head without closing it).

**Hydra does NOT fit when:**
- You need to serve **arbitrary, unknown users** (an open public dApp backend) — parties must be enrolled up front.
- Participants are **frequently offline** — the head stalls without all of them.
- The workload is **low-frequency** — L1 finality is simpler and sufficient.

**Decision-time gotchas** (factor these in *before* recommending Hydra):
- **Contestation period** (default 12h on mainnet, and mainnet should be ≥ 12h) governs dispute/close timing — it sets a floor on worst-case settlement latency, not the fast L2 path.
- **A node per participant**, each funded to pay L1 fees for protocol transactions — real ops cost.
- **All parties must configure identical** peers, contestation-period, deposit-period, and ledger params, or the head won't form or open. This is the #1 setup failure; the bundled `docs/configuration.md` documents it.

**Emerging L2 (in development — not bundled sources).** These target the case Hydra cannot serve: L2 *without* a known, bounded, always-online participant set. All are pre-mainnet; their designs and status move fast, so verify upstream (none is in `docs/sources/`) and never recommend one for a production build.

| Emerging L2 | Type | Status |
|---|---|---|
| **Midgard** | Optimistic rollup | In development |
| **Gummiworm** | Validium-style (off-chain data availability) | In development |

For anything shipping to mainnet today, the realistic answer is **Hydra** (if the participant shape fits) or **stay on L1**. Point at these only as the direction the space is heading.

### Step 4: If Hydra — pick a topology

Route the confirmed Hydra case to a topology using four questions, then map to the bundled docs.

- **How many parties per head?** 2, a small fixed group, or many transient clients?
- **Custody / trust:** must every party hold its own keys and be able to close unilaterally, or is a trusted always-on operator acceptable?
- **Online assumptions:** can all parties come online to make progress, or do you need an operator that is always up on their behalf?
- **On-chain logic:** pure payments, or Plutus validators / escrow / HTLCs running *inside* the head?

| Use-case shape | Topology | Bundled reference |
|---|---|---|
| 2 parties; micropayments, pay-per-use, inter-wallet transfer | **Basic** (2-party channel) | `topologies/basic/`, `use-cases/payments/{pay-per-use-api,inter-wallet-payments}/` |
| Small fixed group; in-head Plutus rules (game, escrow, order matching) | **Basic / managed** | `topologies/basic/`, `topologies/managed/`, `use-cases/other/poker-game/` |
| Many transient clients served by ≥1 always-on operator | **Delegated head** | `topologies/delegated-head/`, `use-cases/auctions/always-on-service-*/` |
| Delegated bidding; L1 escrow + L2 process | **Delegated head / star-shaped** | `topologies/star-shaped/`, `use-cases/auctions/delegated-voucher-*/` |

Read the matched `topologies/*/index.{md,mdx}` and `use-cases/*/index.md` before proposing a design —
they carry the trade-offs and the operator/trust assumptions each shape implies.

### Step 5: Hand off to implementation

Once the approach and topology are chosen, this skill's job is done — route to the bundled Hydra docs rather than restating them. A useful reading order:

1. **Understand** — `docs/protocol-overview.md`, then the chosen `topologies/` and `use-cases/` page.
2. **Set up nodes** — `docs/getting-started.md`, `docs/configuration.md` (backend, keys, zero-fee ledger params, the cross-party consistency rules), `docs/how-to/operating-hydra.md`.
3. **Drive the head** — `docs/how-to/submit-transaction.md` (L2 `NewTx`), `docs/how-to/deposit-with-javascript-sdk.md` (deposit via `@hydra-sdk`), `docs/how-to/incremental-commit.md`, `docs/how-to/incremental-decommit.md`, `docs/how-to/selective-fanout.md`, and `docs/api-behavior.md` (history replay, filtering).
4. **Build securely** — `docs/how-to/best-practise-dapp.md` for commit/deposit validator checks.

Note the API is under active change (ADR-33, `adr/2026-03-10_033-directly-open-head.md`): the head opens **empty** and funds enter via deposits. Pin the node version and re-check output tags after upgrades — the bundled docs currently show some inconsistency between `Commit*` and `Deposit*` naming, so trust the shipped `api-behavior.md` / API reference for the version you run.

### Step 6: State the trade-offs plainly

Whatever you recommend, close with the honest cost:

- **Staying on L1:** simplest, no new ops. If contention is the issue, name the L1 pattern that fixes it.
- **Hydra:** zero-fee, sub-second L2 among enrolled parties — but a node per participant, all-online liveness, and contestation-period settlement latency on close. Worth it only for the right participant shape at real frequency.
- **Emerging rollups:** promising direction, not production. Revisit later; don't build on them now.

## References

- Bundled Hydra docs: `${CLAUDE_SKILL_DIR}/../../docs/sources/hydra/` (topologies, use-cases, how-tos, ADRs)
- Bundled Leios research: `${CLAUDE_SKILL_DIR}/../../docs/sources/ouroboros-leios/`
- Hand-off: `suggest-tooling` (SDKs/infra), `explain-eutxo` (L1 contention patterns), `setup-devnet` (local testing)
- Hydra project site: https://hydra.family/head-protocol
