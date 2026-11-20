# Public Keys: Caching, Local Derivation and Offline Derivation

`ecdsa_public_key` and `schnorr_public_key` are free but cross-subnet calls, so they take seconds. Derivation is deterministic and uses only public data (master public key, canister ID, path), so you can avoid repeated calls. All results below were checked against each other: deriving locally from the root gives the same bytes as the management canister call with the full path.

## In a canister: fetch the root once, derive children locally

Call `ecdsa_public_key` / `schnorr_public_key` once with `derivation_path: vec![]` (the canister's root key), store both `public_key` and `chain_code` (stable memory if you want them across upgrades), then derive:

```toml
ic-secp256k1 = "0.3"   # secp256k1 ECDSA and BIP340
ic-secp256r1 = "0.3"   # P-256
ic-ed25519 = "0.6"     # Ed25519
# ic-secp256k1 / ic-secp256r1 need getrandom's "custom" feature on wasm32: see chain-formats.md
```

```rust
/// Equals `ecdsa_public_key(path).public_key` (secp256k1). For BIP340 use the same
/// function on the `bip340secp256k1` root; for P-256 use `ic_secp256r1` the same way.
pub fn derive_child(
    root_public_key: &[u8],
    root_chain_code: &[u8],
    path: &[Vec<u8>],
) -> Result<Vec<u8>, String> {
    use ic_secp256k1::{DerivationIndex, DerivationPath, PublicKey};
    let root = PublicKey::deserialize_sec1(root_public_key).map_err(|e| format!("{e:?}"))?;
    let chain_code: [u8; 32] = root_chain_code.try_into().map_err(|_| "chain code is not 32 bytes")?;
    let path = DerivationPath::new(path.iter().cloned().map(DerivationIndex).collect());
    // Must pass the returned chain code: `derive_subkey` assumes a zero chain code
    // and yields a different (wrong) key for anything but the master key.
    let (child, _child_chain_code) = root.derive_subkey_with_chain_code(&path, &chain_code);
    Ok(child.serialize_sec1(true))
}

/// Equals `schnorr_public_key(path).public_key` for `ed25519`.
pub fn derive_child_ed25519(
    root_public_key: &[u8],
    root_chain_code: &[u8],
    path: &[Vec<u8>],
) -> Result<[u8; 32], String> {
    use ic_ed25519::{DerivationIndex, DerivationPath, PublicKey};
    let root = PublicKey::deserialize_raw(root_public_key).map_err(|e| format!("{e:?}"))?;
    let chain_code: [u8; 32] = root_chain_code.try_into().map_err(|_| "chain code is not 32 bytes")?;
    let path = DerivationPath::new(path.iter().cloned().map(DerivationIndex).collect());
    let (child, _child_chain_code) = root.derive_subkey_with_chain_code(&path, &chain_code);
    Ok(child.serialize_raw())
}
```

Fetching the root from the management canister (rather than hardcoding a master key) keeps the code correct on both the local network and mainnet.

## Offline in TypeScript (frontends, scripts, explorers)

```bash
npm i @dfinity/ic-pub-key@^1.0.2 @icp-sdk/core@^6   # 1.0.1 ships a broken package entry point
```

```typescript
import { ecdsa, schnorr } from "@dfinity/ic-pub-key";
import { Principal } from "@icp-sdk/core/principal";

const canister = Principal.fromText("<backend canister id>");
// Must match the canister's derivation_path, without the canister ID:
const path = [new TextEncoder().encode("user-v1"), user.toUint8Array()];
const full = (p: Uint8Array[]) => [canister.toUint8Array(), ...p]; // the IC prepends the canister ID

// Mainnet: forMainnetKey("key_1") or ("test_key_1"). Local network: forPocketIcKey("key_1").
const ed = schnorr.ed25519.PublicKeyWithChainCode.forMainnetKey("key_1")
  .deriveSubkeyWithChainCode(new schnorr.ed25519.DerivationPath(full(path)));
ed.public_key.toHex(); // 32-byte Ed25519 key (base58 of it = Solana address)

const k1 = ecdsa.secp256k1.PublicKeyWithChainCode.forMainnetKey("key_1")
  .deriveSubkeyWithChainCode(new ecdsa.secp256k1.DerivationPath(full(path)));
k1.public_key.toHex(); // 33-byte SEC1 compressed

const bip340 = schnorr.bip340secp256k1.PublicKeyWithChainCode.forMainnetKey("key_1")
  .deriveSubkeyWithChainCode(new schnorr.bip340secp256k1.DerivationPath(full(path)));
bip340.public_key.toHex(); // 33-byte SEC1; drop the first byte for the x-only key
```

`DerivationPath.withCanisterPrefix(canister, path)` does the same prepending. The library has no secp256r1 support: derive P-256 keys in Rust or ask the canister. The same package has a CLI: `npx @dfinity/ic-pub-key derive schnorr ed25519 --derivationpath <candid-blob-path>`.

## Offline in Rust (all four schemes)

```toml
ic-pub-key = { version = "0.4", default-features = false, features = ["secp256k1", "secp256r1", "ed25519"] }
ic-management-canister-types = "0.11"
candid = "0.10"
```

```rust
use candid::Principal;
use ic_management_canister_types::{
    EcdsaCurve, EcdsaKeyId, EcdsaPublicKeyArgs, SchnorrAlgorithm, SchnorrKeyId, SchnorrPublicKeyArgs,
};

/// Same bytes that `schnorr_public_key` returns for `canister_id` on mainnet.
pub fn ed25519_public_key(canister_id: &str, path: Vec<Vec<u8>>) -> Result<Vec<u8>, String> {
    let canister_id = Principal::from_text(canister_id).map_err(|e| e.to_string())?;
    let res = ic_pub_key::derive_schnorr_key(&SchnorrPublicKeyArgs {
        canister_id: Some(canister_id), // required offline
        derivation_path: path,
        key_id: SchnorrKeyId { algorithm: SchnorrAlgorithm::Ed25519, name: "key_1".to_string() },
    })
    .map_err(|e| format!("{e:?}"))?;
    Ok(res.public_key) // 32 bytes
}

/// P-256 (not covered by the TypeScript library). Use "pocketic_key_1" for the local network.
pub fn p256_public_key(canister_id: &str, path: Vec<Vec<u8>>) -> Result<Vec<u8>, String> {
    let canister_id = Principal::from_text(canister_id).map_err(|e| e.to_string())?;
    let res = ic_pub_key::derive_ecdsa_key(&EcdsaPublicKeyArgs {
        canister_id: Some(canister_id),
        derivation_path: path,
        key_id: EcdsaKeyId { curve: EcdsaCurve::Secp256r1, name: "key_1".to_string() },
    })
    .map_err(|e| format!("{e:?}"))?;
    Ok(res.public_key) // 33-byte SEC1 compressed
}
```

Key names accepted offline: `key_1`, `test_key_1` (mainnet master keys) and `pocketic_key_1`, `pocketic_test_key_1`, `dfx_test_key` (the local network and PocketIC, which answer to `key_1`, `test_key_1`, `dfx_test_key` in canister calls).
