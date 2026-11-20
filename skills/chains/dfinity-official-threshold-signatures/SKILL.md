---
name: threshold-signatures
description: "Sign from a canister with ICP threshold (chain-key) keys: Ed25519 and BIP340 Schnorr through sign_with_schnorr, and ECDSA on secp256k1 or secp256r1 (P-256) through sign_with_ecdsa. Explains how to pick the scheme the verifier needs and why Ed25519 is the default when the choice is free. Also covers key names and fees, the budget of about 10 signatures per second, derivation paths, public keys and offline derivation, and the formats that Bitcoin, Ethereum, Solana and JWTs expect, with Rust and Motoko code. Use when a canister must hold a key, derive an address or sign transactions, tokens or attestations, or when ecdsa_public_key, schnorr_public_key, sign_with_ecdsa or sign_with_schnorr fails. Do NOT use for BLS signatures or encryption (vetkeys), ckBTC/ckETH/ckSOL deposits and withdrawals (ckbtc, cketh, cksol) or EVM RPC calls (evm-rpc)."
license: Apache-2.0
compatibility: "icp-cli >= 0.2.2. Rust: ic-cdk 0.20 with ic-cdk-management-canister >= 0.3 (secp256r1 needs 0.3). Motoko: the ic mops package >= 5.0.0 (secp256r1 needs 5.0.0)."
metadata:
  title: Threshold Signatures (ECDSA, Schnorr, Ed25519)
  category: Security
  summary: "Produce Ed25519, Schnorr and ECDSA signatures from a canister for transactions, tokens and attestations."
  keywords: "tECDSA, tSchnorr, chain-key signatures, sign_with_ecdsa, sign_with_schnorr, EdDSA, secp256k1, secp256r1, P-256, ES256, BIP340, Taproot, Bitcoin address, Ethereum address, Solana address, canister wallet, JWT, derivation path, chain fusion"
---

# Threshold Signatures (Ed25519, Schnorr, ECDSA)

## What This Is

A canister must never keep a private key in its state (node operators can read canister memory). It asks the management canister (`aaaaa-aa`) to sign instead: a signing subnet holds a **master key** in shares, and its nodes compute the signature together without any node seeing the key. Each canister gets its own key tree, derived from the master key and its **canister ID**; `derivation_path` selects any number of child keys. Only that canister can sign with its keys.

| Scheme | Methods | `key_id` | `*_public_key` returns | You pass | Signature |
|---|---|---|---|---|---|
| Ed25519 (EdDSA, RFC 8032) | `schnorr_public_key`, `sign_with_schnorr` | `record { algorithm = variant { ed25519 }; name }` | 32 bytes | `message`, the raw message | 64 bytes `R‖S` |
| Schnorr BIP340 (secp256k1) | same | `algorithm = variant { bip340secp256k1 }` | 33-byte SEC1 compressed; drop byte 0 for the 32-byte x-only key | `message`; optional `aux` for Taproot (BIP341) | 64 bytes BIP340 |
| ECDSA secp256k1 | `ecdsa_public_key`, `sign_with_ecdsa` | `record { curve = variant { secp256k1 }; name }` | 33-byte SEC1 compressed | `message_hash`, **exactly 32 bytes** | 64 bytes `r‖s`, low-s normalized, no recovery id |
| ECDSA secp256r1 (NIST P-256) | same | `curve = variant { secp256r1 }` | 33-byte SEC1 compressed | `message_hash`, exactly 32 bytes | 64 bytes `r‖s`, low-s normalized |

Only canisters can call these methods, from update contexts. `*_public_key` accepts `canister_id = opt <other>` to read another canister's keys. Signatures are randomized, Ed25519 included. BLS: see `vetkeys`.

## Choosing the Scheme

**Rule 1: the verifier decides.** Use the scheme the standard, chain or library checking the signature requires. **Rule 2: if free to choose, use Ed25519**: it has the best threshold-signing throughput on ICP and is the simplest (no pre-hashing, 32-byte keys).

| Verifier / standard | Scheme |
|---|---|
| Bitcoin P2PKH, P2WPKH, P2SH; Dogecoin; Ethereum and EVM chains; Cosmos SDK chains | ECDSA secp256k1 |
| Bitcoin Taproot (P2TR), Ordinals/Runes; Nostr events (NIP-01) | Schnorr BIP340 |
| Solana, Stellar, TON, NEAR, Aptos, Sui, Cardano, Polkadot (ed25519 accounts); JWT `alg: EdDSA`; SSH; your own verifier | Ed25519 |
| JWT/JWS/COSE `ES256`, X.509 certificates and CSRs, mdoc/EUDI-style credentials, any NIST/FIPS-only verifier | ECDSA secp256r1 |

You may not need a threshold signature at all:

- **Only ICP canisters verify it:** inter-canister calls already authenticate the caller, and certified data (`certified-variables`) has no fee or throughput limit.
- **Unique or BLS signatures, encryption, end-user keys:** `vetkeys` skill.
- **Per-user Bitcoin/Ethereum keys for a web app without a backend:** the Chain Fusion Signer canister `grghe-syaaa-aaaar-qabyq-cai`, paid in cycles via ICRC-2.

## Keys, Environments and Cost

| Key name | Where | Use | Fee per `sign_with_*` |
|---|---|---|---|
| `key_1` | mainnet (34-node fiduciary subnet `pzp6e`), local | production | 26_153_846_153 cycles (~$0.036) |
| `test_key_1` | mainnet (13-node subnet `fuqsr`), local | development; never for anything of value | 10_000_000_000 cycles (~$0.014) |
| `dfx_test_key` | local / PocketIC only | legacy tests | n/a on mainnet |

- Both names exist for all four schemes. `*_public_key` calls are **free**; rejected signing requests are refunded.
- The signing subnet sets the fee. Let the helpers attach it (Rust `ic-cdk-management-canister`, Motoko `mo:ic/Call`; both use `ic0.cost_sign_with_ecdsa` / `ic0.cost_sign_with_schnorr`). Too few cycles: `sign_with_ecdsa request sent with N cycles, but M cycles are required.`
- The icp-cli local network always provides `key_1`, `test_key_1` and `dfx_test_key` for all four schemes, but **its master keys are not mainnet's**: every local public key and address differs from mainnet.
- The key name is **permanent configuration**: another name means other keys and addresses, stranding funds at the old ones. Read it from one place (below: the `THRESHOLD_KEY_NAME` canister environment variable, default `key_1`) and never change it for a deployed canister.

## Throughput and Latency: Design for Them

- **Plan for about 10 signatures per second per key**, shared by every canister on ICP using that key. Short bursts somewhat above it are served from pre-computed pre-signatures; sustained excess fills the key's queue and new requests are **rejected immediately**: `sign_with_schnorr request failed: request queue for key <key> is full.` (reject code `CANISTER_REJECT` = 4, cycles refunded). Ed25519 has the highest throughput.
- **A signature takes seconds** (a round trip to the signing subnet plus consensus there).
- Design accordingly:
  1. **Sign less.** Sign one hash over a batch (a Merkle root) instead of every item; reuse long-lived signatures (JWTs, certificates) until they expire.
  2. **Queue in your canister.** Store requests, drain them from a timer with a bounded number of in-flight `sign_with_*` calls, and retry rejections with exponential backoff.
  3. **Rate-limit and authenticate callers** of anything that signs; this also protects your cycles (about 26B per `key_1` signature).
  4. **Keep signing off latency-critical paths**: return a job ID and let the client poll.

## Derivation Paths

- A key is fully determined by `(scheme, key name, canister ID, derivation_path)`.
- `derivation_path : vec blob`, at most **254** elements (the replica prepends the canister ID), each of any length, including empty. `[]` is the canister's root key.
- **Never take the path from the caller.** Build it from `msg_caller` and your own constants, for example `["user-v1", caller principal bytes]`. A caller-chosen path lets anyone sign with anyone's key.
- Use separate elements, not concatenated strings, so parts cannot run into each other, and version the scheme (`"user-v1"`) so later paths never collide.
- Derivation is public: anyone who knows the canister ID and path can compute the public key offline.
- secp256k1, BIP340 and secp256r1 derivation is BIP-32 / SLIP-10 compatible only if every element is a 4-byte big-endian integer below 2^31; this matters only for outside HD-wallet tooling. Ed25519 uses an IC-specific scheme.
- Keys are bound to the **canister ID**: upgrades and reinstalls keep them; a new canister (another ID) has entirely different keys. Never delete a canister that controls funds.

## Public Keys: Cache or Derive

The `*_public_key` calls are free but slow (cross-subnet): cache results per path, or derive. Code for all three options is in [references/public-keys.md](references/public-keys.md).

- **In a canister:** fetch the root once (`derivation_path = []`), keep `public_key` **and** `chain_code`, derive with `ic-secp256k1` / `ic-secp256r1` / `ic-ed25519` `derive_subkey_with_chain_code`. **Not `derive_subkey`** (zero chain code: wrong key).
- **Offline in TypeScript:** `@dfinity/ic-pub-key@^1.0.2` (1.0.1 has a broken entry point) for secp256k1, BIP340 and Ed25519 (not secp256r1); the first path element is the canister ID. `forMainnetKey("key_1")` on mainnet, `forPocketIcKey("key_1")` locally.
- **Offline in Rust:** `ic-pub-key = "0.4"` (all four schemes): `derive_ecdsa_key` / `derive_schnorr_key` take the management canister argument types with `canister_id: Some(id)`. Local key names are `pocketic_key_1`, `pocketic_test_key_1`, `dfx_test_key`.

## Implementation: Rust

```toml
# backend/Cargo.toml (package "backend", crate-type cdylib)
[dependencies]
candid = "0.10"
ic-cdk = "0.20"
ic-cdk-management-canister = "0.3"
serde = "1"
sha2 = "0.10"
```

```yaml
# icp.yaml
canisters:
  - name: backend
    recipe:
      type: "@dfinity/rust@v3.4.0"
    settings:
      environment_variables:
        THRESHOLD_KEY_NAME: "key_1"
```

```rust
use candid::{CandidType, Deserialize, Principal};
use ic_cdk::api::{env_var_name_exists, env_var_value, msg_caller};
use ic_cdk::call::{CallFailed, RejectCode};
use ic_cdk::update;
use ic_cdk_management_canister::{
    self as mgmt, EcdsaCurve, EcdsaKeyId, EcdsaPublicKeyArgs, SchnorrAlgorithm, SchnorrKeyId,
    SchnorrPublicKeyArgs, SignCallError, SignWithEcdsaArgs, SignWithSchnorrArgs,
};
use sha2::{Digest, Sha256};

#[derive(CandidType, Deserialize, Clone, Copy)]
enum Scheme {
    #[serde(rename = "ed25519")]
    Ed25519,
    #[serde(rename = "bip340secp256k1")]
    Bip340Secp256k1,
    #[serde(rename = "ecdsaSecp256k1")]
    EcdsaSecp256k1,
    #[serde(rename = "ecdsaSecp256r1")]
    EcdsaSecp256r1,
}

enum Api {
    Schnorr(SchnorrAlgorithm),
    Ecdsa(EcdsaCurve),
}

fn api(scheme: Scheme) -> Api {
    match scheme {
        Scheme::Ed25519 => Api::Schnorr(SchnorrAlgorithm::Ed25519),
        Scheme::Bip340Secp256k1 => Api::Schnorr(SchnorrAlgorithm::Bip340secp256k1),
        Scheme::EcdsaSecp256k1 => Api::Ecdsa(EcdsaCurve::Secp256k1),
        Scheme::EcdsaSecp256r1 => Api::Ecdsa(EcdsaCurve::Secp256r1),
    }
}

/// Permanent configuration: another key name means other keys and addresses.
fn key_name() -> String {
    const VAR: &str = "THRESHOLD_KEY_NAME";
    if env_var_name_exists(VAR) { env_var_value(VAR) } else { "key_1".to_string() }
}

/// Versioned, per-user derivation path. Never let callers choose the path.
fn user_path(user: &Principal) -> Vec<Vec<u8>> {
    vec![b"user-v1".to_vec(), user.as_slice().to_vec()]
}

fn authenticated_caller() -> Result<Principal, String> {
    let caller = msg_caller();
    if caller == Principal::anonymous() {
        return Err("anonymous caller".to_string());
    }
    Ok(caller)
}

/// The caller's public key. Free, but a cross-subnet call: cache the result.
#[update]
async fn public_key(scheme: Scheme) -> Result<Vec<u8>, String> {
    let derivation_path = user_path(&authenticated_caller()?);
    let name = key_name();
    let result = match api(scheme) {
        Api::Schnorr(algorithm) => mgmt::schnorr_public_key(&SchnorrPublicKeyArgs {
            canister_id: None,
            derivation_path,
            key_id: SchnorrKeyId { algorithm, name },
        })
        .await
        .map(|r| r.public_key),
        Api::Ecdsa(curve) => mgmt::ecdsa_public_key(&EcdsaPublicKeyArgs {
            canister_id: None,
            derivation_path,
            key_id: EcdsaKeyId { curve, name },
        })
        .await
        .map(|r| r.public_key),
    };
    result.map_err(|e| format!("public key call failed: {e}"))
}

/// Signs with the caller's own key ("wallet" pattern). Each call costs the
/// canister ~26B cycles on key_1: rate-limit or charge callers.
#[update]
async fn sign(scheme: Scheme, message: Vec<u8>) -> Result<Vec<u8>, String> {
    let derivation_path = user_path(&authenticated_caller()?);
    let name = key_name();
    let result = match api(scheme) {
        // Schnorr and Ed25519 sign the message itself, not a hash of it.
        Api::Schnorr(algorithm) => mgmt::sign_with_schnorr(&SignWithSchnorrArgs {
            message,
            derivation_path,
            key_id: SchnorrKeyId { algorithm, name },
            aux: None,
        })
        .await
        .map(|r| r.signature),
        // ECDSA signs a 32-byte hash: SHA-256 here (ES256, generic use);
        // Keccak-256 for Ethereum, the transaction sighash for Bitcoin.
        Api::Ecdsa(curve) => mgmt::sign_with_ecdsa(&SignWithEcdsaArgs {
            message_hash: Sha256::digest(&message).to_vec(),
            derivation_path,
            key_id: EcdsaKeyId { curve, name },
        })
        .await
        .map(|r| r.signature),
    };
    result.map_err(describe_sign_error) // Ok: 64 bytes for every scheme
}

fn describe_sign_error(e: SignCallError) -> String {
    match &e {
        SignCallError::CallFailed(CallFailed::CallRejected(r)) => match r.reject_code() {
            // Queue full, cycles, unknown key, bad argument: nothing was signed.
            Ok(RejectCode::CanisterReject) => format!("signing rejected: {}", r.reject_message()),
            // Outcome unknown: the signature may exist.
            Ok(RejectCode::SysUnknown) | Ok(RejectCode::CanisterError) => {
                format!("signing outcome unknown: {}", r.reject_message())
            }
            _ => format!("signing failed: {}", r.reject_message()),
        },
        _ => format!("signing failed: {e}"),
    }
}

ic_cdk::export_candid!();
```

`sign_with_*` are unbounded-wait calls with the fee attached; `*_public_key` are bounded-wait. Crate versions 0.1/0.2 lack `Secp256r1`. Before ic-cdk 0.20 these lived in `ic_cdk::management_canister`.

## Implementation: Motoko

Same canister in Motoko (identical Candid variant names, so the commands in "Verify It Works" apply): see [references/motoko.md](references/motoko.md). Essentials:

- `mops add ic && mops add sha2`. Public keys via `ic.ecdsa_public_key` / `ic.schnorr_public_key` (`mo:ic`); sign via `Call.signWithEcdsa` / `Call.signWithSchnorr` (`mo:ic/Call`), which attach the exact fee. `#secp256r1` needs `ic` >= 5.0.0; `ic` 6.x needs `moc` >= 2.1.0.
- ECDSA hash: `Sha256.fromBlob(#sha256, message)` (`mo:sha2/Sha256`). Older Motoko examples hardcode `10_000_000_000` cycles, enough only for `test_key_1`.

## Chain-Specific Formats

The IC returns bare signatures; [references/chain-formats.md](references/chain-formats.md) has compiled Rust helpers and off-chain verification code for each consumer:

- **Ethereum/EVM:** sign Keccak-256 of the RLP/EIP-712 payload; recover `y_parity`/`v` by trial recovery; address = `keccak256(uncompressed key)[12..]`.
- **Bitcoin legacy/SegWit:** sign the sighash; DER-encode and append the sighash-type byte (already low-s).
- **Bitcoin Taproot key-path spend:** `aux = opt variant { bip341 = record { merkle_root_hash = blob "" } }` (or the 32-byte script-tree root). Script-path leaves use `aux = null`.
- **Solana:** sign the serialized message; the address is base58 of the 32-byte key. **JWT ES256:** sign SHA-256 of `header.payload` with secp256r1; the JWS signature is the 64-byte `r‖s` as is.

## Mistakes That Break Your Build

1. **Passing a message to `sign_with_ecdsa`.** `message_hash` must be exactly 32 bytes, hashed with the verifier's hash (SHA-256, Keccak-256, a Bitcoin sighash). Conversely, **don't add a hash for Schnorr or Ed25519**: pass exactly the bytes the protocol signs (a raw message, or Taproot's sighash or Nostr's event id).
2. **Exposing a signing oracle.** An endpoint that signs caller-supplied bytes with a **shared** key (treasury, bridge, issuer) lets anyone sign a transaction or token in your name. Build the message inside the canister from validated inputs, with a domain prefix (`"myapp:attest:v1"`). Arbitrary-message signing is acceptable only with a key derived from the caller's own principal, as above.
3. **Letting the caller choose `derivation_path`.** Derive it from `msg_caller()` and constants.
4. **Hardcoding the fee or the key name.** `10_000_000_000` cycles covers only `test_key_1`. `dfx_test_key` does not exist on mainnet. Shipping `test_key_1` to production, or switching keys after launch, changes every address.
5. **Assuming local keys equal mainnet keys.** Use `forPocketIcKey` / `pocketic_key_1` offline for the local network, or just call `*_public_key`.
6. **Deriving children with `derive_subkey`** (zero chain code) instead of `derive_subkey_with_chain_code` with the parent's `chain_code`.
7. **BIP340 and Taproot details.** Use the 32-byte x-only key (drop byte 0). A key-path spend without `bip341` aux signs for the untweaked key; a non-empty `merkle_root_hash` must be 32 bytes; Ed25519 rejects any `aux`.
8. **Double hashing when verifying.** `@noble/curves` v2 ECDSA `verify` hashes its input by default: pass the original message, or the 32-byte hash with `{ prehash: false }`.
9. **Treating signatures as unique.** All four schemes are randomized; never use a signature as an ID, dedup key or randomness.
10. **Assuming a failed call signed nothing.** On `SYS_UNKNOWN` (bounded-wait timeout) or `CANISTER_ERROR` the signature may exist. Make a lost signature harmless (nonces, expiry) and never sign a conflicting replacement until the first is provably dead (Bitcoin: same inputs; Ethereum: same nonce).
11. **Mutating state after `await` without a guard.** Reserve the nonce, UTXOs or balance before awaiting `sign_with_*` (see `canister-security`).
12. **Retrying in a loop on `request queue ... is full`.** It is a capacity signal: back off with a timer and sign less.
13. **Calling the APIs from a query or a frontend.** Only canisters can; frontends derive public keys offline or call your canister.
14. **Deleting or recreating a canister that holds funds.** Keys depend on the canister ID. Controllers can make the canister sign anything by upgrading it: decentralize control (SNS, blackholing) if users must trust the keys.
15. **Calling `aaaaa-aa` directly from a CloudEngine subnet.** Route threshold calls through the engine's proxy (see `cloud-engine-canisters`).

## Verify It Works

```bash
icp network start -d
icp deploy backend
icp canister call backend public_key '(variant { ed25519 })'
# Expected: (variant { Ok = blob "..." }), 32 bytes (Motoko: variant { ok = ... })
icp canister call backend sign '(variant { ed25519 }, blob "hello")'
# Expected: (variant { Ok = blob "..." }), 64 bytes, different on every call
icp canister call backend sign '(variant { ecdsaSecp256r1 }, blob "hello")'
# Mainnet: add -e ic; each key_1 signature burns ~26B cycles (icp canister status backend -e ic)
```

Verify signatures off-chain with the TypeScript function in [references/chain-formats.md](references/chain-formats.md). If verification fails, check that the public key comes from the same environment (local master keys differ from mainnet's) and the same derivation path as the signature.

## Related Skills

- `vetkeys` (BLS, encryption); `evm-rpc`, `ckbtc`, `cketh`, `cksol` (sending transactions, chain-key tokens); `canister-security` (state around `await`); `cloud-engine-canisters` (signing from engines).
