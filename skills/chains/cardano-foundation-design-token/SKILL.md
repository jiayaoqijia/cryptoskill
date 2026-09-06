---
name: design-token
description: >-
  Design Cardano native token, NFT, NFT collection, fungible token, CIP-25
  metadata, CIP-68 reference tokens, CIP-113 programmable tokens, minting
  policy, token architecture.
allowed-tools: Read Grep Glob
disallowed-tools: Bash Edit Write WebFetch WebSearch
---

<!-- Documentation lookup path: ${CLAUDE_SKILL_DIR}/../../docs/sources/ -->

# Design Cardano Native Token

Guide the user through designing a Cardano native token: choosing the right
CIP standard, designing the minting policy, structuring metadata, and planning
for ecosystem compatibility.

## When to Use

- User wants to create an NFT or NFT collection
- User wants to create a fungible token
- User asks about CIP-25, CIP-68, or CIP-113 standards
- User wants to design token metadata
- User needs help choosing between token standards
- User asks about updatable metadata or programmable tokens
- User wants to understand reference tokens (label 100/222/333/444)

## When NOT to Use

- User wants to write the minting policy validator code -- use `write-validator`
- User wants to build the actual minting transaction -- use `build-transaction`
- User has a failing mint transaction -- use `debug-transaction`
- User wants a security review of an existing minting policy -- use `review-contract`

## Key Principles

1. **Pick the right CIP standard first.** CIP-25 is simple but immutable.
   CIP-68 enables updatable metadata via reference tokens. CIP-113 (still a
   draft) makes tokens programmable via shared-custody validation. The choice
   affects the entire architecture.

2. **Design the minting policy before the metadata.** The policy determines
   who can mint, when, and how many. It is the foundation of token security.

3. **Plan for ecosystem compatibility.** Wallets, marketplaces, and explorers
   rely on CIP standards to display tokens correctly. Non-conformant metadata
   will appear broken in most tools.

4. **Minimize on-chain data.** Store large assets (images, documents) off-chain
   via IPFS or Arweave. On-chain metadata should contain references (IPFS CID),
   not raw data.

5. **Consider the full token lifecycle.** Can it be burned? Can metadata be
   updated? Can supply change? These decisions must be made at design time.

## Workflow

### Step 1: Identify the Token Type

Ask the user what they are building:

| Token Type | Description | Recommended Standard |
|------------|-------------|---------------------|
| Simple NFT | One-off unique token, immutable | CIP-25 |
| NFT Collection | Series of unique tokens, immutable | CIP-25 or CIP-68 |
| Updatable NFT | NFT with mutable metadata | CIP-68 (label 222) |
| Fungible Token | Divisible, tradeable token | CIP-68 (label 333) |
| Rich Fungible Token | Fungible with detailed on-chain metadata | CIP-68 (label 444) |
| Programmable Token | Token with on-chain behavior rules | CIP-113 |

### Step 2: Search Bundled Documentation

Search the bundled documentation for relevant content:
- `${CLAUDE_SKILL_DIR}/../../docs/sources/cips/` - CIP specifications (CIP-25, CIP-68, CIP-113)
- `${CLAUDE_SKILL_DIR}/../../docs/sources/mesh-sdk/` - Mesh SDK docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/evolution-sdk/` - Evolution SDK docs
- `${CLAUDE_SKILL_DIR}/../../docs/sources/aiken/` - Aiken language docs

### Step 3: Choose the CIP Standard

Search `${CLAUDE_SKILL_DIR}/../../docs/sources/` for detailed CIP comparisons.

**CIP-25 (Simple Metadata)**
- Metadata stored in transaction metadata (label 721)
- Immutable after minting -- cannot update
- Simplest to implement
- Universally supported by wallets and marketplaces
- Best for: simple NFTs and collections that never need updates

**CIP-68 (Reference Tokens)**
- Metadata stored in a datum at a reference token UTxO
- Updatable by spending and recreating the reference UTxO
- Uses label pairs: 100 (reference) + 222 (NFT) / 333 (FT) / 444 (RFT)
- More complex to implement but far more flexible
- Best for: projects needing updatable metadata, rich fungible tokens,
  or dynamic NFTs

**CIP-113 (Programmable Tokens — draft, unmerged PR #444)**
- Tokens are held at a shared script address; ownership is tracked by stake
  credential, and validation logic runs on every transfer, mint, and burn
- An on-chain registry links each token to its transfer/issuance logic;
  substandards (freeze-and-seize, KYC) plug into the shared framework
- Most complex; reference implementation is unaudited and not production-ready
- Best for: regulated tokens, stablecoins, and compliance-bound assets

See `references/cip-token-standards.md` for a detailed comparison.

### Step 4: Design the Minting Policy

The minting policy is a Cardano script that authorizes token creation.

**Native Script Policies (no Plutus needed):**

- **Time-locked:** Minting allowed only before a specific slot.
  After the deadline, no more tokens can ever be minted. Good for
  fixed-supply collections.

  ```json
  {
    "type": "all",
    "scripts": [
      { "type": "sig", "keyHash": "<policy_key_hash>" },
      { "type": "before", "slot": 98765432 }
    ]
  }
  ```

- **Multi-sig:** Require multiple signatures to mint.

**Plutus Script Policies (for complex logic):**

- **One-shot (NFT guarantee):** Consume a specific UTxO to ensure
  the policy ID is unique and can only mint once.
- **Collection minting:** Allow minting multiple tokens under the
  same policy with rules (e.g., max supply, whitelist).
- **CIP-68 minting:** Must mint the reference token (label 100)
  alongside the user token (label 222/333/444) in the same transaction.

### Step 5: Design the Metadata Structure

#### CIP-25 Metadata

Attached to the minting transaction under label 721:

```json
{
  "721": {
    "<policy_id>": {
      "<asset_name>": {
        "name": "My NFT #1",
        "image": "ipfs://QmXyz...",
        "mediaType": "image/png",
        "description": "Description of the NFT",
        "attributes": {
          "trait1": "value1",
          "trait2": "value2"
        }
      }
    }
  }
}
```

Required fields: `name`, `image`
Optional but recommended: `mediaType`, `description`

#### CIP-68 Datum Metadata

Stored as a datum on the reference token UTxO:

```
Constr(0, [
  // metadata map
  Map([
    (Bytes("name"), Bytes("My NFT #1")),
    (Bytes("image"), Bytes("ipfs://QmXyz...")),
    (Bytes("mediaType"), Bytes("image/png")),
    (Bytes("description"), Bytes("Description")),
  ]),
  // version
  Int(1),
  // extra (application-specific)
  Constr(0, [])
])
```

The datum structure is: `Constr 0 [metadata_map, version, extra]`

- `metadata_map`: key-value pairs where keys are byte strings
- `version`: integer version number
- `extra`: application-specific data (use `Constr 0 []` for none)

### Step 6: Plan the Asset Name Encoding

Token asset names are byte strings (max 32 bytes). Conventions:

- **CIP-25 NFTs:** Use human-readable names, hex-encoded
  (e.g., `"MyNFT001"` becomes `4d794e4654303031`)
- **CIP-68 tokens:** Prefix with the label in hex:
  - Reference token: `000643b0` + name bytes (label 100)
  - NFT user token: `000de140` + name bytes (label 222)
  - FT user token: `0014df10` + name bytes (label 333)
  - RFT user token: `001bc280` + name bytes (label 444)

### Step 7: Architecture Decisions

Guide the user through these design choices:

- **Supply model:** Fixed supply (time-lock policy) vs. ongoing minting
  (Plutus policy with admin key)
- **Burnability:** Should tokens be burnable? Most policies allow it
  by default. Time-locked policies make burning impossible after the deadline.
- **Metadata storage:** IPFS (decentralized, persistent) vs. HTTP URLs
  (centralized, mutable). Prefer IPFS with CID pinning.
- **Royalties:** CIP-27 defines on-chain royalty info. Marketplaces may
  or may not enforce it. CIP-113 can enforce royalties at the protocol level.
- **Collection grouping:** All tokens under one policy ID form a
  "collection." Use one policy per logical collection.

### Step 8: Ecosystem Compatibility Checklist

Verify the design works with:

- [ ] Wallets: display name, image, and metadata correctly
- [ ] Marketplaces: JPG Store, CNFT.io recognize the token standard
- [ ] Explorers: CardanoScan, Cexplorer show metadata
- [ ] Token registries: Cardano Token Registry for fungible tokens
- [ ] IPFS: images and files are pinned and accessible
- [ ] Metadata standard: conforms to chosen CIP exactly

## Common Mistakes

- **Wrong label for CIP-68:** Using 721 (CIP-25) metadata label with
  CIP-68 tokens. CIP-68 uses datums, not transaction metadata.
- **Exceeding 32-byte asset name limit:** Including the CIP-68 prefix
  in the 32-byte calculation. The prefix IS part of the 32 bytes.
- **Not minting the reference token:** CIP-68 requires both the reference
  token (100) and user token (222/333/444) to be minted together.
- **Forgetting mediaType:** Without `mediaType`, wallets may not render
  the asset correctly.
- **Using HTTP URLs instead of IPFS:** HTTP URLs are mutable and can break.
  Always prefer `ipfs://` URIs for permanence.

## References

- `references/cip-token-standards.md` -- detailed CIP-25 vs CIP-68 vs CIP-113 comparison
- CIP-25: https://cips.cardano.org/cip/CIP-25
- CIP-68: https://cips.cardano.org/cip/CIP-68
- CIP-113: https://cips.cardano.org/cip/CIP-113
- CIP-27 (Royalties): https://cips.cardano.org/cip/CIP-27
- Search `${CLAUDE_SKILL_DIR}/../../docs/sources/` for minting policy patterns and examples
