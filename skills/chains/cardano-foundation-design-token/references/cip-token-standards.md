# Cardano Token Standards: CIP-25, CIP-68, CIP-113

Comparison of Cardano Improvement Proposals for native token metadata.

## Quick Comparison

| Feature | CIP-25 | CIP-68 | CIP-113 (draft) |
|---------|--------|--------|---------|
| Metadata location | Transaction metadata (label 721) | Datum on reference UTxO | Orthogonal — standard native-asset naming; can pair with CIP-68 metadata |
| Updatable | No | Yes | n/a (metadata is a separate concern) |
| On-chain behavior | No | No | Yes (validation on every transfer/mint/burn) |
| Complexity | Low | Medium | High |
| Wallet support | Universal | Growing | Early (needs stake-credential-aware integration) |
| Fee / script cost | Lowest (no script) | Higher (Plutus on update) | Highest (validators run on every movement) |
| Token types | NFT only | NFT, FT, RFT | Programmable native assets |

---

## CIP-25: Media Token Metadata Standard

**Purpose:** Define a standard way to attach metadata to NFTs at mint time.

**How it works:**
- Metadata is included in the minting transaction under label `721`
- Metadata is permanently recorded in the transaction, immutable
- No on-chain UTxO is created for metadata -- it lives in tx metadata only
- Wallets and marketplaces read label 721 from the minting transaction

**When to use:**
- Simple NFTs or NFT collections
- Metadata will never need updating
- Want maximum wallet/marketplace compatibility
- Want simplest possible implementation

**Label convention:**
- Transaction metadata label: `721`

**Metadata structure:**
```json
{
  "721": {
    "<policy_id>": {
      "<asset_name_utf8>": {
        "name": "SpaceBud #1234",
        "image": "ipfs://QmXyz...",
        "mediaType": "image/png",
        "description": "A unique SpaceBud",
        "files": [
          {
            "name": "SpaceBud1234_hires.png",
            "mediaType": "image/png",
            "src": "ipfs://QmAbc..."
          }
        ],
        "<custom_field>": "<custom_value>"
      }
    }
  }
}
```

**Required fields:** `name`, `image`
**Optional fields:** `mediaType`, `description`, `files`, any custom fields

**Update mechanism:** None. Metadata is immutable once the minting transaction
is confirmed. To "update," you must burn and re-mint (new token).

---

## CIP-68: Datum Metadata Standard

**Purpose:** Enable updatable, on-chain metadata for NFTs, fungible tokens,
and rich fungible tokens using reference tokens.

**How it works:**
- Two tokens are minted simultaneously under the same policy:
  1. **Reference token** (label 100): held at a script address with metadata in its datum
  2. **User token** (label 222/333/444): held by the owner, represents the asset
- Metadata lives in the datum of the reference token's UTxO
- To update metadata: spend the reference UTxO and recreate it with new datum
- Wallets read the reference token's datum to display metadata

**When to use:**
- NFTs that need updatable metadata (e.g., game items, evolving art)
- Fungible tokens that need rich on-chain metadata
- Projects that want on-chain verifiable metadata
- Dynamic NFTs that change based on external events

**Label conventions:**

| Label | Hex Prefix | Token Type | Purpose |
|-------|-----------|------------|---------|
| 100 | `000643b0` | Reference | Holds metadata datum |
| 222 | `000de140` | NFT | User-facing NFT token |
| 333 | `0014df10` | FT | User-facing fungible token |
| 444 | `001bc280` | RFT | User-facing rich fungible token |

The asset name is constructed as: `<hex_prefix><token_name_bytes>`

Both the reference token (100) and user token (222/333/444) share the same
`<token_name_bytes>` suffix, linking them together.

**Datum structure (CBOR):**
```
121_0([ ; Constr 0
  { ; metadata map
    h'6E616D65': h'<utf8_name>',           ; "name"
    h'696D616765': h'<utf8_image_uri>',    ; "image"
    h'6D6564696154797065': h'<utf8_mime>', ; "mediaType"
    h'6465736372697074696F6E': h'<utf8>'   ; "description"
  },
  1,           ; version (integer)
  121_0([])    ; extra data (application-specific)
])
```

**Update mechanism:**
1. Spend the UTxO holding the reference token
2. Create a new UTxO at the same script address with the reference token
   and an updated datum
3. The minting policy or a separate governance script controls who can update

**Example -- minting a CIP-68 NFT pair:**
- Mint `000643b04d794e4654` (reference token: label 100 + "MyNFT")
- Mint `000de1404d794e4654` (user NFT token: label 222 + "MyNFT")
- Send reference token to script address with metadata datum
- Send user token to the buyer/owner

---

## CIP-113: Programmable Tokens

**Status:** "Proposed" per the draft's own header, but the CIP is an unmerged
PR ([cardano-foundation/CIPs#444](https://github.com/cardano-foundation/CIPs/pull/444))
— not yet in the official CIPs repo. The Cardano Foundation reference
implementation has not been professionally audited, has only been briefly
tested on the Preview testnet, and is not production-ready.

**Purpose:** Native tokens whose transfers, mints, and burns must satisfy
on-chain validation logic — freeze/seize, allowlists, KYC gating, and other
compliance rules an issuer must enforce after issuance.

**How it works (shared-custody architecture):**
- All programmable tokens are locked at a **shared spending validator**
  (`programmableLogicBase`) — they never sit free in user wallets, so every
  movement is a script spend and the validation logic always runs
- **Ownership is tracked by stake credential**: a user's "smart wallet" is the
  set of UTxOs at the shared script whose stake credential identifies them;
  standard wallets keep a normal send/receive experience
- An **on-chain registry** (a sorted linked list of UTxOs with NFT markers)
  records each programmable token and points to its transfer, third-party, and
  issuance logic scripts
- Validation uses the **withdraw-zero pattern**: the base validator delegates to
  a global stake validator that runs once per transaction and requires the
  token-specific transfer-logic script to run alongside it
- **Substandards** (e.g. freeze-and-seize, KYC) plug custom rules into the
  shared framework instead of re-implementing the plumbing

**Relationship to CIP-68 — it is NOT an extension:**
- CIP-113 builds on native-asset infrastructure (its registry design descends
  from CIP-143, now folded into it) and uses standard native-asset naming
- A CIP-113 token can still carry CIP-68-style metadata, but the enforcement
  model (shared custody + registry + stake validators) is orthogonal to CIP-68's
  reference/user token pairing

**When to use:**
- Regulated/security tokens and stablecoins requiring freeze, seize, or
  allowlist controls
- Real-world assets with compliance obligations (sanctions screening, KYC/AML)
- Any asset whose issuer must enforce rules after issuance, not just at mint

**Trade-off:** every movement runs scripts — higher fees, and wallets, DEXes,
and explorers need stake-credential-aware integration to support these tokens.
If control at mint/burn is enough, a plain minting policy is the right tool.

**Source of truth:** search `docs/sources/cip-113-programmable-tokens/` (core
framework), `docs/sources/cip-113-programmable-tokens-platform/` (substandards),
and `docs/sources/cip-113-sdk-typescript/` (off-chain SDK) — do not rely on
memory for this standard; it is still evolving.

---

## Migration Paths

**CIP-25 to CIP-68:**
- Cannot update existing CIP-25 tokens (metadata is immutable)
- Burn old tokens and re-mint as CIP-68 pair
- Or maintain both standards and let users swap

**CIP-68 to CIP-113:**
- Not an in-place upgrade: CIP-113 is a different custody model, not a CIP-68
  extension. Tokens must be re-issued through the CIP-113 issuance flow and
  registered in the on-chain registry (new policy ID = new token)
- Existing CIP-68 metadata practices can be reused for the new token's metadata
- If compliance rules are likely, design for CIP-113 from the start — and note
  it is still a draft standard (unmerged PR #444)

## Choosing the Right Standard

```
Do you need updatable metadata?
  No  --> CIP-25
  Yes --> Do you need on-chain transfer rules?
            No  --> CIP-68
            Yes --> CIP-113
```

For fungible tokens: register static metadata (ticker, decimals, logo) with
**CIP-26** (the off-chain Cardano token registry) — free, widely supported, and
the default path. Use CIP-68 (label 333 or 444) when metadata must live
on-chain or be updatable by script. CIP-25 was designed for media tokens/NFTs,
not FTs.

For maximum compatibility today: CIP-25 has the widest wallet and
marketplace support. CIP-68 support is growing rapidly. CIP-113 is
still early-stage.
