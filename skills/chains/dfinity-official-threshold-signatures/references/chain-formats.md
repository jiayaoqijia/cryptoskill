# Chain-Specific Formats for Threshold Signatures

The management canister returns a bare 64-byte signature and a compressed public key. Every consumer wants its own encoding. The Rust helpers below compile for `wasm32-unknown-unknown` with ic-cdk 0.20 and `ic-cdk-management-canister` 0.3.

## Extra dependencies

```toml
[dependencies]
ic-secp256k1 = "0.3"    # secp256k1 + BIP340: SEC1 (de)compression, recovery, derivation
ic-secp256r1 = "0.3"    # P-256: SEC1 (de)compression, derivation
ic-sha3 = "1"           # Keccak-256
base64 = "0.22"
serde_json = "1"
# ic-secp256k1 / ic-secp256r1 pull in getrandom 0.2, which needs this for wasm32-unknown-unknown:
getrandom = { version = "0.2", features = ["custom"] }
```

```rust
// lib.rs: the helpers below never need randomness, so a failing source is enough.
getrandom::register_custom_getrandom!(always_fail);
fn always_fail(_buf: &mut [u8]) -> Result<(), getrandom::Error> {
    Err(getrandom::Error::UNSUPPORTED)
}
```

## Ethereum and EVM chains (ECDSA secp256k1)

- `message_hash` is Keccak-256 of what the chain signs: `keccak256(0x02 || rlp([...]))` for an EIP-1559 transaction, `keccak256("\x19Ethereum Signed Message:\n" + len + msg)` for `personal_sign`, the EIP-712 digest for typed data.
- The IC returns `r‖s` without a recovery id: recover `y_parity` by trial recovery. Typed transactions use `y_parity` (0/1); `personal_sign` uses `v = 27 + y_parity`; legacy EIP-155 transactions use `v = chain_id * 2 + 35 + y_parity`.
- Build and send transactions with the EVM RPC canister (`evm-rpc` skill). Full working canister: `rust/basic_ethereum` in github.com/dfinity/examples.

```rust
use ic_secp256k1::PublicKey;

/// Ethereum address of a SEC1-encoded secp256k1 public key from `ecdsa_public_key`.
pub fn ethereum_address(sec1_public_key: &[u8]) -> Result<[u8; 20], String> {
    let pk = PublicKey::deserialize_sec1(sec1_public_key).map_err(|e| format!("{e:?}"))?;
    let uncompressed = pk.serialize_sec1(false); // 0x04 || x || y
    let hash = ic_sha3::Keccak256::hash(&uncompressed[1..]);
    let mut address = [0u8; 20];
    address.copy_from_slice(&hash[12..]);
    Ok(address)
}

/// Turn the 64-byte `sign_with_ecdsa` signature into Ethereum's (r, s, y_parity).
pub fn ethereum_signature(
    sec1_public_key: &[u8],
    digest: &[u8; 32], // Keccak-256 of the RLP/EIP-712 payload you passed as message_hash
    signature: &[u8],
) -> Result<([u8; 64], bool), String> {
    let pk = PublicKey::deserialize_sec1(sec1_public_key).map_err(|e| format!("{e:?}"))?;
    let recovery_id = pk
        .try_recovery_from_digest(digest, signature)
        .map_err(|e| format!("{e:?}"))?;
    let sig: [u8; 64] = signature.try_into().map_err(|_| "signature is not 64 bytes")?;
    Ok((sig, recovery_id.is_y_odd()))
}
```

To compute addresses for many users without a management canister call each, derive the keys locally: see [public-keys.md](public-keys.md).

## Bitcoin legacy and SegWit (ECDSA secp256k1)

- Sign the input's sighash: `SighashCache::p2wpkh_signature_hash(...)` (BIP143) for P2WPKH, `legacy_signature_hash` for P2PKH. That 32-byte value is `message_hash`.
- Witness/scriptSig need DER plus the sighash-type byte: `bitcoin::ecdsa::Signature { signature: bitcoin::secp256k1::ecdsa::Signature::from_compact(&sig)?, sighash_type: EcdsaSighashType::All }.to_vec()`. IC signatures are already low-s, so no normalization is needed.
- The public key for P2WPKH/P2PKH is the 33-byte compressed key as returned.
- The `bitcoin` crate builds `secp256k1-sys` C code: building for wasm32 needs a clang with the WebAssembly backend (on macOS: Homebrew `llvm`).
- One signature per input: consolidate UTXOs rather than spending many small ones, because each input costs a signature and a share of the ~10/s budget.
- Full working canister (P2PKH, P2WPKH, P2TR key and script path): `rust/basic_bitcoin` in github.com/dfinity/examples.

## Bitcoin Taproot (Schnorr BIP340)

- Internal key = `schnorr_public_key(path).public_key[1..]` (32-byte x-only).
- **Key-path spend:** pass `aux = Some(SchnorrAux::Bip341(Bip341 { merkle_root_hash }))` with an **empty** `merkle_root_hash` if the output has no script tree, or the 32-byte tree root if it has one. The IC then applies the BIP341 TapTweak and signs for the output key. Without `aux` the signature is for the untweaked internal key and the spend is invalid.
- **Script-path spend:** the leaf script's key signs with `aux = None`.
- The message is the 32-byte BIP341 sighash (`taproot_key_spend_signature_hash` / `taproot_script_spend_signature_hash`).

```rust
use ic_cdk_management_canister::{
    Bip341, SchnorrAlgorithm, SchnorrAux, SchnorrKeyId, SignWithSchnorrArgs, sign_with_schnorr,
};

/// Key-path spend of a P2TR output whose internal key is `schnorr_public_key(path)[1..]`.
pub async fn sign_taproot_key_spend(
    key_name: String,
    path: Vec<Vec<u8>>,
    sighash: [u8; 32],           // BIP341 sighash of the input
    merkle_root: Option<[u8; 32]>, // Some(root) if the output also commits to a script tree
) -> Result<Vec<u8>, String> {
    let merkle_root_hash = merkle_root.map(|r| r.to_vec()).unwrap_or_default(); // empty = no scripts
    let res = sign_with_schnorr(&SignWithSchnorrArgs {
        message: sighash.to_vec(),
        derivation_path: path,
        key_id: SchnorrKeyId { algorithm: SchnorrAlgorithm::Bip340secp256k1, name: key_name },
        aux: Some(SchnorrAux::Bip341(Bip341 { merkle_root_hash })),
    })
    .await
    .map_err(|e| e.to_string())?;
    Ok(res.signature) // 64 bytes; append the sighash type byte unless SIGHASH_DEFAULT
}
```

## Nostr (Schnorr BIP340)

The event `id` is SHA-256 of the serialized `[0, pubkey, created_at, kind, tags, content]`; sign the 32-byte `id` with `bip340secp256k1` and `aux = None`. The Nostr `pubkey` is the hex of the 32-byte x-only key (drop byte 0 of the returned key).

## Solana and other Ed25519 chains

- Sign the serialized transaction **message** bytes with `sign_with_schnorr` (`ed25519`, `aux = None`); place the 64-byte signature in the transaction's signature list.
- The Solana address is the base58 encoding of the 32-byte public key.
- Solana transactions reference a recent blockhash that expires in about a minute; signing latency counts against that window, so use durable nonces for anything that may queue.
- Full working canister: `examples/basic_solana` in github.com/dfinity/sol-rpc-canister (SOL RPC canister for fetching blockhashes and sending).

## JWT and other ES256 / EdDSA tokens

ES256 (P-256) JWS signatures are exactly the 64-byte `r‖s` the IC returns. For EdDSA JWTs (`alg: EdDSA`) sign the same signing input with Ed25519 and no hashing. Mind the throughput budget: reuse tokens until they expire.

```rust
use base64::{Engine, engine::general_purpose::URL_SAFE_NO_PAD as B64};
use ic_cdk_management_canister::{EcdsaCurve, EcdsaKeyId, SignWithEcdsaArgs, sign_with_ecdsa};
use sha2::{Digest, Sha256};

/// Issue an ES256 JWT signed by the canister's P-256 key at `path`.
pub async fn issue_es256_jwt(
    key_name: String,
    path: Vec<Vec<u8>>,
    kid: &str,
    claims: &serde_json::Value,
) -> Result<String, String> {
    let header = serde_json::json!({ "alg": "ES256", "typ": "JWT", "kid": kid });
    let signing_input = format!(
        "{}.{}",
        B64.encode(header.to_string()),
        B64.encode(claims.to_string())
    );
    let sig = sign_with_ecdsa(&SignWithEcdsaArgs {
        message_hash: Sha256::digest(signing_input.as_bytes()).to_vec(),
        derivation_path: path,
        key_id: EcdsaKeyId { curve: EcdsaCurve::Secp256r1, name: key_name },
    })
    .await
    .map_err(|e| e.to_string())?
    .signature;
    // JOSE ES256 signatures are the raw 64-byte r || s, exactly what the IC returns.
    Ok(format!("{signing_input}.{}", B64.encode(sig)))
}

/// Public JWK for verifiers, from the 33-byte SEC1 key returned by `ecdsa_public_key`.
pub fn es256_jwk(sec1_public_key: &[u8], kid: &str) -> Result<serde_json::Value, String> {
    let pk = ic_secp256r1::PublicKey::deserialize_sec1(sec1_public_key)
        .map_err(|e| format!("{e:?}"))?;
    let uncompressed = pk.serialize_sec1(false); // 0x04 || x (32) || y (32)
    Ok(serde_json::json!({
        "kty": "EC", "crv": "P-256", "alg": "ES256", "use": "sig", "kid": kid,
        "x": B64.encode(&uncompressed[1..33]),
        "y": B64.encode(&uncompressed[33..65]),
    }))
}
```

Encodings differ by format: JWS and COSE (`ES256`, RFC 9053) use the fixed-width 64-byte `r‖s` exactly as returned, while X.509 certificates and CSRs need it converted to DER, an ASN.1 `SEQUENCE { INTEGER r, INTEGER s }`.

## Verifying off-chain (TypeScript)

`npm i @noble/curves@^2 @noble/hashes@^2`. `scheme` is the Candid variant label the canisters in SKILL.md and motoko.md take (`ed25519`, `bip340secp256k1`, `ecdsaSecp256k1`, `ecdsaSecp256r1`); the other inputs are the bytes they return. For ECDSA those canisters signed `sha256(message)`.

```typescript
import { ed25519 } from "@noble/curves/ed25519.js";
import { schnorr, secp256k1 } from "@noble/curves/secp256k1.js";
import { p256 } from "@noble/curves/nist.js";
import { sha256 } from "@noble/hashes/sha2.js";

// publicKey / signature: bytes returned by the canister; message: the bytes it signed.
export function verify(scheme, publicKey, message, signature) {
  switch (scheme) {
    case "ed25519": // 32-byte key, message signed as-is
      return ed25519.verify(signature, message, publicKey);
    case "bip340secp256k1": // BIP340 uses the 32-byte x-only key: drop the SEC1 prefix byte
      return schnorr.verify(signature, message, publicKey.slice(1));
    case "ecdsaSecp256k1": // the canister signed sha256(message); noble v2 would hash again by default
      return secp256k1.verify(signature, sha256(message), publicKey, { prehash: false });
    case "ecdsaSecp256r1":
      return p256.verify(signature, sha256(message), publicKey, { prehash: false });
  }
  throw new Error(`unknown scheme ${scheme}`);
}
```

In Rust, `ic_ed25519::PublicKey::verify_signature`, `ic_secp256k1::PublicKey::verify_bip340_signature` (x-only semantics), `ic_secp256k1::PublicKey::verify_ecdsa_signature_prehashed` and `ic_secp256r1::PublicKey::verify_signature_prehashed` verify the same signatures inside a canister.
