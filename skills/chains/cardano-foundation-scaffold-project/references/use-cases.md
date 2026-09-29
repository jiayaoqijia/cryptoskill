# Use-case Menu

When scaffolding a new Cardano project, picking the use case up front is more useful than picking only a stack. The use case decides the datum shape, the redeemer shape, what the validator checks, and what the off-chain code has to do. The stack decision (Mesh / Evolution / PyCardano / cardano-client-lib) sits on top of that and is mostly about which language the team writes.

This file lists the reference use cases derived from `../../docs/sources/cardano-use-case-templates/`. They come from the research paper "Smart Contract Languages: A Comparative Analysis" (Bartoletti et al., 2024) and are implemented for Cardano by the Cardano Foundation.

## Curated vs agent-generated

Not every use case is equally polished. We split them into two tiers:

- **Curated (5).** End-to-end implementations have been hand-reviewed across Aiken on-chain plus all four off-chain stacks (Mesh, Evolution, cardano-client-lib, PyCardano). The skill points you at the source files; the on-chain code, off-chain code, and (for vesting) a walkthrough are in the repo.
- **Agent-generated (16).** The Aiken on-chain implementation exists upstream, but off-chain coverage is patchy or non-existent. For these the workflow is: read the Aiken validator as the spec, run `aiken build` to emit the CIP-57 `plutus.json`, then write off-chain code on the fly. The agent uses bundled SDK docs at `../../docs/sources/<sdk-slug>/` and the corresponding upstream off-chain implementation (where present) as a model.

For curated use cases the deliverable is a working starting point. For agent-generated use cases the deliverable is a structured plan plus the on-chain code, and the off-chain code is written in-session by the agent.

## How to pick

Ask the developer one question: "What does the contract do at the highest level?" Then map onto the closest entry below. If nothing matches, encourage the developer to describe their case in their own words and treat it as a custom use case (read the closest upstream Aiken validator, generalise, build).

## Curated use cases (5)

| # | Name | One-liner |
|---|---|---|
| 1 | simple-transfer | Plain spend validator that only releases funds to a designated recipient. |
| 2 | vesting | Time-locked funds with an owner clawback and a beneficiary withdrawal path past the deadline. |
| 3 | escrow | Funds locked by a buyer, released by mutual agreement or arbitration. |
| 4 | token-transfer | Native-token movement under a spend validator (not bare ADA). |
| 5 | htlc | Hashed Time-Locked Contract: redeem-with-preimage or refund-after-deadline. |

For each: source code at `../../docs/sources/cardano-use-case-templates/<name>/`. Vesting has its own end-to-end walkthrough; see `references/vesting-walkthrough.md`.

## Agent-generated use cases (16)

| # | Name | One-liner | On-chain frameworks | Off-chain notes |
|---|---|---|---|---|
| 6 | bet | Two parties stake funds; oracle or timer settles. | aiken | Build off-chain from `../../docs/sources/cardano-use-case-templates/bet/onchain/aiken/`. |
| 7 | auction | English auction; highest bidder wins after a deadline. | aiken, scalus | Read the Aiken validator first; CF has partial off-chain coverage. |
| 8 | crowdfund | Goal-based fundraising; refund or release on deadline. | aiken | Refund logic is the subtle bit; read the validator carefully. |
| 9 | vault | Holds funds under a single beneficiary key with an optional admin override. | aiken | Read the validator. |
| 10 | storage | On-chain key-value storage with simple ownership rules. | aiken | Blaze is the recommended off-chain extra for storage-style flows where many small UTxOs need indexing; otherwise use any of the four stacks. |
| 11 | simple-wallet | Multi-signature wallet pattern under a single script. | aiken | Datum encodes the signer set. |
| 12 | pricebet | Bet against an oracle-reported price. | aiken | Requires an oracle UTxO; combine with `query-chain` skill for the oracle read path. |
| 13 | payment-splitter | Distributes incoming payments across multiple recipients by share. | aiken, scalus | Useful pattern when one address receives funds destined for several parties. |
| 14 | lottery | Pick a winner from a pot via a verifiable mechanism (commit-reveal or oracle randomness). | aiken | Randomness on-chain is the tricky part; treat the upstream impl as a starting point only. |
| 15 | constant-product-amm | x*y=k AMM pool (README only upstream, no full implementation). | aiken | Treat as a learning target; implementing safely is a multi-skill exercise. |
| 16 | upgradable-proxy | A proxy validator that delegates to a swappable implementation. | aiken | Approach with care; review the security implications via `review-contract` skill. |
| 17 | factory | One validator mints many child instances. | aiken | Common for spawning per-user vaults; combine with `design-token` for the minting policy side. |
| 18 | decentralized-identity | DID-style identity records anchored on-chain. | aiken | Read the validator; off-chain wraps DID resolution. |
| 19 | editable-nft | CIP-68-style mutable NFT metadata (README only upstream). | aiken | Combine with `design-token` skill for the CIP-68 token-pair design. |
| 20 | anonymous-data | Commit-reveal pattern for private data publication. | aiken | Useful primitive; agent generates off-chain wrappers. |
| 21 | atomic-transaction | Multi-step swap that commits or aborts atomically. | aiken | Off-chain orchestration is the bulk of the work. |

## Where to look during a session

When the agent and developer pick an agent-generated use case, the workflow is:

1. Read the Aiken validator at `../../docs/sources/cardano-use-case-templates/<name>/onchain/aiken/validators/<name>.ak`. This is the spec.
2. Run `aiken build` after copying the validator into the scaffolded project. The CIP-57 `plutus.json` produced is the contract between on-chain and off-chain code.
3. Open bundled SDK docs at `../../docs/sources/<sdk-slug>/` to look up current API shapes. SDKs change quickly; the bundled docs are the source of truth.
4. Read the closest curated off-chain implementation as a structural model (e.g. for any new use case, vesting's off-chain code shows the load-blueprint, build-tx, submit pattern).
5. Write the off-chain code in the scaffolded project. Don't paste from the bundled docs verbatim — adapt to your stack and the validator's exact datum/redeemer shapes.

## Caveats

- Yaci Store's Blockfrost-compatible API is `http://localhost:8080/api/v1`, the same URL the upstream scenarios use. Port 10000 is the DevKit admin API, not a chain-query endpoint.
- Upstream off-chain code uses a single shared mnemonic (`"test test test ... sauce"`) for convenience. The scaffold replaces this with a `.env`-driven dev mnemonic generated per project. Do not commit the upstream literal as a project secret.
- Plutus time is POSIX milliseconds. Slot-to-time conversion is era-dependent. The upstream vesting code aligns the slot config manually for Yaci DevKit's compressed eras; copy that pattern when working with time-locked validators.
