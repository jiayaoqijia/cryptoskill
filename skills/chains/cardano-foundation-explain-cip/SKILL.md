---
name: explain-cip
description: >-
  Explain Cardano Improvement Proposals (CIPs) to developers. Trigger phrases:
  "explain CIP", "what is CIP-30", "CIP-68 metadata", "what CIP covers",
  "which CIP for wallets", "governance CIP", "token metadata standard".
allowed-tools: Read Grep Glob
disallowed-tools: Bash Edit Write WebFetch WebSearch
---

<!-- Documentation lookup path: ${CLAUDE_SKILL_DIR}/../../docs/sources/ -->

# Explain CIP

Help developers understand Cardano Improvement Proposals — what they standardize, how they
affect development, and how to implement them.

## When to use

- A developer asks about a specific CIP by number ("What is CIP-30?")
- A developer asks which standard covers a topic ("How do I do NFT metadata?")
- A developer wants to understand the motivation behind a standard
- Questions about CIP status, adoption, or SDK support
- Comparing CIPs that address similar concerns (e.g., CIP-25 vs CIP-68 for metadata)

## When NOT to use

- The developer wants to **implement** wallet connectivity — use `connect-wallet` (which
  covers CIP-30 implementation)
- The developer needs to **write a validator** or **build a transaction** — redirect to
  the relevant skill
- The developer asks about eUTxO concepts — use `explain-eutxo`
- The question is about Cardano governance participation — use the governance skill

## Key Principles

### 1. CIPs are standards, not implementations

A CIP defines a specification or convention. It does not provide a library or runtime. SDKs
and tools choose to implement CIPs. When explaining a CIP, distinguish between what the
standard defines and how specific tools implement it.

### 2. Always check CIP status

CIPs go through lifecycle stages: Draft, Proposed, Active, Inactive. A Draft CIP may change
significantly. An Active CIP is stable and widely adopted. Always note the status when
explaining a CIP, because developers should not build on unstable drafts without
understanding the risk.

### 3. Focus on developer impact

Developers care about: What does this CIP let me do? What do I need to implement? Which
SDKs support it? What are the constraints? Lead with practical impact, not governance
process.

### 4. CIPs build on each other

Many CIPs reference or extend others. CIP-68 builds on CIP-25 concepts. CIP-95 extends
CIP-30. When explaining a CIP, note its dependencies and related CIPs so the developer
understands the full picture.

## Workflow

### Step 1: Identify the CIP

Determine the CIP number from the developer's question. If they describe a feature without
naming a CIP, map it:
- "NFT metadata" -> CIP-25, CIP-68
- "Wallet connection" -> CIP-30
- "Governance wallet" -> CIP-95
- "Token metadata on-chain" -> CIP-68
- "Validator blueprint" -> CIP-57
- "Programmable tokens" -> CIP-113
- "On-chain governance" -> CIP-1694

### Step 2: Search Bundled Documentation

Search the bundled documentation for relevant content:
- `${CLAUDE_SKILL_DIR}/../../docs/sources/cips/` - CIP specifications and proposals

Use Grep and Glob to find relevant files. CIP content may appear in reference docs,
registry entries, or skill files.

### Step 3: Explain the CIP

Structure your explanation with these components:

**Summary:** One-paragraph description of what the CIP standardizes.

**Motivation:** Why was this CIP created? What problem does it solve? What existed before?

**Developer impact:** What does this mean for a developer building on Cardano?
- What can they build with it?
- What do they need to implement?
- What constraints does it impose?

**Implementation status:** Is this CIP Active, Draft, or Proposed? Which SDKs support it?
Are there known limitations or upcoming changes?

**SDK support:** Which Cardano SDKs and tools implement this CIP, and how?

### Step 4: Provide practical guidance

Give the developer actionable next steps:
- Point to the relevant skill if they need to implement something
- Note which SDK methods or tools to use
- Highlight common pitfalls or misunderstandings

## Key CIPs for Developers

### CIP-25: Media Token Metadata Standard

**Status:** Active

**Summary:** Defines a standard for attaching metadata to media tokens/NFTs using
transaction metadata (label 721). Metadata is included in the minting transaction and
indexed by off-chain services. (For fungible-token metadata — ticker, decimals, logo —
the standard path is CIP-26, the off-chain token registry, not CIP-25.)

**Developer impact:**
- Metadata is stored in the transaction, not on the UTxO itself
- Metadata is only in the minting transaction — it cannot be updated after minting
- Off-chain indexers (Blockfrost, Koios, etc.) parse and serve CIP-25 metadata
- Simple to implement: add a metadata entry to the minting transaction

**Limitations:**
- Immutable after minting (no metadata updates)
- Stored off-chain relative to the UTxO (only in the transaction)
- Led to the creation of CIP-68 to address mutability and on-chain storage

**Structure:**
```json
{
  "721": {
    "<policy_id>": {
      "<asset_name>": {
        "name": "Token Name",
        "image": "ipfs://<hash>",
        "description": "Token description",
        "mediaType": "image/png",
        "<additional_properties>": "..."
      }
    }
  }
}
```

### CIP-30: Cardano dApp-Wallet Web Bridge

**Status:** Active

**Summary:** Defines a JavaScript API that wallets inject into web pages, enabling dApps to
request wallet information, build transactions, and request signing. This is the primary
standard for dApp-wallet interaction in browsers.

**Developer impact:**
- `window.cardano.<walletName>` exposes the wallet API
- `enable()` returns an API object with methods for address, UTxO, and signing operations
- All data is CBOR-encoded — SDKs handle serialization
- Wallets: Begin, Eternl, Flint, GeroWallet, Lace, Nami, NuFi, RayWallet, Yoroi all implement CIP-30

**Key API methods:**
- `getNetworkId()` — returns 0 (testnet) or 1 (mainnet)
- `getUtxos()` — returns available UTxOs for transaction building
- `getBalance()` — returns wallet balance
- `getUsedAddresses()` / `getUnusedAddresses()` — address management
- `signTx(tx, partialSign)` — request transaction signing
- `signData(addr, payload)` — sign arbitrary data (CIP-8)
- `submitTx(tx)` — submit a signed transaction

**Common pitfalls:**
- Always check `window.cardano` exists before accessing wallet properties
- Handle the case where the user rejects the `enable()` prompt
- CBOR encoding/decoding — use an SDK (Mesh, Evolution SDK) rather than raw CIP-30

### CIP-57: Plutus Contract Blueprint (CIP-0057)

**Status:** Active

**Summary:** Defines a JSON schema (blueprint) for Plutus validators, describing their
parameters, datum, and redeemer types. Aiken generates CIP-57 blueprints automatically.
SDKs use blueprints to create type-safe interfaces for validator interaction.

**Developer impact:**
- Aiken produces `plutus.json` after compilation — this is the CIP-57 blueprint
- SDKs (Mesh, Evolution SDK) can read the blueprint to generate typed transaction
  builders
- Blueprints enable code generation and type safety across the on-chain/off-chain boundary
- Includes validator hashes, parameter schemas, and datum/redeemer definitions

**Structure highlights:**
- `validators[]` — list of validators with their hashes and compiled code
- `definitions` — shared type definitions (datum, redeemer schemas)
- Each validator entry includes `datum.schema`, `redeemer.schema`, and `compiledCode`

### CIP-68: Datum Metadata Standard

**Status:** Active

**Summary:** Defines a pattern for storing token metadata as a datum on a reference UTxO,
making metadata on-chain, updatable, and queryable via reference inputs. Replaces CIP-25
for use cases requiring mutable or on-chain metadata.

**Developer impact:**
- Each token has a paired reference NFT holding metadata in its datum
- Token labels: `(222)` for NFTs, `(333)` for FTs, `(444)` for RFTs
- The reference NFT sits at a script address; the user token is in the user's wallet
- Metadata can be updated by consuming and recreating the reference UTxO
- Requires a more complex minting policy than CIP-25

**Architecture:**
- **User token:** `<policy_id>.<label><name>` — held by the owner, represents ownership
- **Reference token:** `<policy_id>.(100)<name>` — held at a script address, carries
  metadata in its datum (label 100, hex prefix `000643b0`)
- The minting policy enforces that both tokens are minted together

**When to use CIP-68 vs CIP-25:**
| Requirement | CIP-25 | CIP-68 |
|---|---|---|
| Simple, immutable NFT | Good fit | Overkill |
| Updatable metadata | Not possible | Designed for this |
| On-chain metadata access | Not available | Via reference input |
| Implementation complexity | Low | Medium |
| Transaction cost | Lower (metadata only) | Higher (reference UTxO + datum) |

### CIP-95: Governance Wallet Extensions

**Status:** Active (Conway era)

**Summary:** Extends CIP-30 with governance-specific wallet methods for the Conway
governance era (Voltaire). Enables dApps to interact with DRep registration, voting, and
governance actions.

**Developer impact:**
- Adds `cip95` methods accessible after `enable({ extensions: [{ cip: 95 }] })`
- `getPubDRepKey()` — get the wallet's DRep public key
- `getRegisteredPubStakeKeys()` — get registered stake keys
- `getUnregisteredPubStakeKeys()` — get unregistered stake keys
- Required for governance dApps (GovTool, DRep platforms)

**Prerequisite:** CIP-30 wallet connection must be established first.

### CIP-113: Programmable Tokens

**Status:** Proposed per the draft's own header — but the CIP is an **unmerged PR**
([cardano-foundation/CIPs#444](https://github.com/cardano-foundation/CIPs/pull/444)),
so it is not yet in the official CIPs repo or the bundled `cips/` mirror — though an
adapted reference implementation is bundled under `docs/sources/cip-113-programmable-tokens/`.

**Summary:** Defines a standard for tokens with programmable validation logic — rules
enforced on every transfer, mint, and burn. Tokens are held at a shared script address
with ownership tracked by stake credential; an on-chain registry links each token to its
transfer/issuance logic, and substandards (freeze-and-seize, KYC) plug into the shared
framework.

**Developer impact:**
- Enables "smart tokens" with enforced transfer rules (regulated assets, stablecoins)
- Shared-custody model: wallets/DEXes need stake-credential-aware integration
- Relevant for compliance-bound assets; plain minting policies remain right for most tokens

**Note:** The specification may still change, and the Cardano Foundation reference
implementation is not professionally audited, has only been briefly tested on the
Preview testnet, and is not production-ready. Check the PR and
`docs/sources/cip-113-programmable-tokens/` for current state.

### CIP-1694: Conway Era Governance (Voltaire)

**Status:** Active

**Summary:** Defines Cardano's on-chain governance system introduced in the Conway era.
Establishes the governance framework with DReps (Delegated Representatives), a
Constitutional Committee, and SPO governance roles. All holders can participate in governance
through delegation or direct voting.

**Developer impact:**
- Governance actions are on-chain transactions (parameter changes, treasury withdrawals,
  hard forks, constitutional committee updates, motions of no confidence)
- DRep registration and voting use specific transaction certificate types
- SDKs need Conway-era transaction support for governance features
- dApps can integrate governance features using CIP-95 wallet extensions

**Key concepts:**
- **DRep:** A delegated representative who votes on governance actions
- **Constitutional Committee:** A group that checks governance actions against the constitution
- **Governance action:** A proposal submitted on-chain with a deposit
- **Ratification:** The process by which DReps, SPOs, and the Constitutional Committee
  approve or reject actions

## Mapping Topics to CIPs

When a developer describes a feature, map it to the relevant CIP:

| Developer asks about... | Relevant CIP(s) |
|---|---|
| NFT metadata | CIP-25 (immutable), CIP-68 (updatable) |
| Wallet connection | CIP-30 |
| Wallet governance | CIP-95 (extends CIP-30) |
| Message signing | CIP-8 (via CIP-30's `signData`) |
| Token metadata on-chain | CIP-68 |
| Validator interface / types | CIP-57 (blueprint) |
| Programmable tokens | CIP-113 |
| Governance / voting | CIP-1694 |
| Reference inputs | CIP-31 |
| Inline datums | CIP-32 |
| Reference scripts | CIP-33 |
| Collateral outputs | CIP-40 |
| Multi-asset structure | CIP-14 (asset fingerprint) |

## References

- CIP repository: `github.com/cardano-foundation/CIPs`
- Shared principles: `../shared/PRINCIPLES.md`
