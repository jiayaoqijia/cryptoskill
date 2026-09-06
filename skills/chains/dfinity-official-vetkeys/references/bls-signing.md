# Threshold BLS Signatures

vetKeys can produce **canister-authenticated BLS signatures**: the subnet's threshold infrastructure signs a message on the canister's behalf, and anyone with the canister's BLS public key can verify it — no encryption involved. This uses the **unencrypted** vetKey; the library helper (`sign_with_bls` / `signWithBls`) handles that for you.

The `context` typically embeds a domain separator **and** the signer, so signatures are scoped per user. `context` and the message must be identical between signing and verification.

## Backend — sign a message + expose the verification key

### Rust

`sign_with_bls` comes from the `ic-vetkeys` crate; the public key is fetched via the ic-cdk management binding.

```rust
use ic_cdk::update;
use ic_cdk_management_canister::{VetKDCurve, VetKDKeyId, VetKDPublicKeyArgs};
use candid::Principal;

fn key_id() -> VetKDKeyId {
    VetKDKeyId { curve: VetKDCurve::Bls12_381_G2, name: "test_key_1".to_string() }
}

// Domain separator (length-prefixed) + signer principal.
fn context(signer: &Principal) -> Vec<u8> {
    const DS: &[u8] = b"basic_bls_signing_app";
    [DS.len() as u8].into_iter().chain(DS.iter().copied()).chain(signer.as_slice().iter().copied()).collect()
}

#[update]
async fn sign_message(message: Vec<u8>) -> Vec<u8> {
    let signer = ic_cdk::api::msg_caller();
    ic_vetkeys::management_canister::sign_with_bls(message, context(&signer), key_id())
        .await
        .expect("sign_with_bls failed")
}

#[update]
async fn get_my_verification_key() -> Vec<u8> {
    let res = ic_cdk_management_canister::vetkd_public_key(&VetKDPublicKeyArgs {
        canister_id: None,
        context: context(&ic_cdk::api::msg_caller()),
        key_id: key_id(),
    })
    .await
    .expect("vetkd_public_key failed");
    res.public_key
}
```

### Motoko

Both `signWithBls` and `blsPublicKey` come from `mo:ic-vetkeys/ManagementCanister`.

```motoko
import VetKeys "mo:ic-vetkeys";
import Principal "mo:core/Principal";
import Text "mo:core/Text";
import Blob "mo:core/Blob";
import Array "mo:core/Array";
import Nat "mo:core/Nat";
import Runtime "mo:core/Runtime";

persistent actor {
  // Captured at first install and fixed for the canister's derived keys (immutable after install).
  let keyName = Runtime.envVar<system>("VETKD_KEY_NAME") ?? "test_key_1";
  let keyId : VetKeys.ManagementCanister.VetKdKeyid = { curve = #bls12_381_g2; name = keyName };

  // Length-prefixed domain separator + signer principal. The dot-notation calls
  // (.toArray/.concat/.toBlob/.toNat8) resolve against the imported Blob/Array/Nat modules.
  func context(signer : Principal) : Blob {
    let ds : [Nat8] = Text.encodeUtf8("basic_bls_signing_app").toArray();
    let dsLen : [Nat8] = [ds.size().toNat8()];
    let signerArray : [Nat8] = Principal.toBlob(signer).toArray();
    dsLen.concat(ds).concat(signerArray).toBlob();
  };

  public shared ({ caller }) func signMessage(message : Text) : async Blob {
    await VetKeys.ManagementCanister.signWithBls(Text.encodeUtf8(message), context(caller), keyId);
  };

  public shared ({ caller }) func getMyVerificationKey() : async Blob {
    await VetKeys.ManagementCanister.blsPublicKey(null, context(caller), keyId);
  };
};
```

## Verify a signature (TypeScript)

```typescript
import { verifyBlsSignature, DerivedPublicKey } from "@icp-sdk/vetkeys";

// Encode once and use the SAME bytes for signing and verifying. The Motoko backend's
// signMessage(Text) signs Text.encodeUtf8(message), so verify against those bytes.
const messageBytes = new TextEncoder().encode("hello");
const signature = new Uint8Array(await backend.signMessage("hello"));
// First arg is a DerivedPublicKey object, not raw bytes — deserialize first.
const publicKey = DerivedPublicKey.deserialize(new Uint8Array(await backend.getMyVerificationKey()));
const ok = verifyBlsSignature(publicKey, messageBytes, signature); // true if valid
```

## Pitfalls

- BLS uses the **unencrypted** vetKey — there is no transport key or `decryptAndVerify` step. Use the `sign_with_bls` / `signWithBls` helper; never construct a BLS signature from an `EncryptedVetKey`.
- Keep `context` (domain separator + signer) and the message byte-identical between signing and verification, or verification fails.
- Do not reuse the same `context` / `input` across BLS and IBE — derive distinct keys for distinct purposes.

## Additional References

- Core concepts, key names, cycles, and pitfalls: the main `vetkeys` SKILL.md
- Canonical examples: `motoko/vetkeys/basic_bls_signing`, `rust/vetkeys/basic_bls_signing` in [dfinity/examples](https://github.com/dfinity/examples/tree/master/rust/vetkeys)
