# Identity-Based Encryption (IBE) & Timelock

IBE lets a sender encrypt to an **identity** (e.g. a principal) using only the canister's derived public key — the recipient need not be online or have registered a key. The recipient later authenticates, obtains their vetKey for that identity via `vetkd_derive_key`, and decrypts locally.

The IBE cryptography (`IbeCiphertext`, `IbeIdentity`, `IbeSeed`, `EncryptedVetKey`, `VetKey`) lives in **`@icp-sdk/vetkeys`** (frontend) and the **`ic-vetkeys` Rust crate** — **not** in the Motoko library. A Motoko backend only derives and returns the *encrypted* vetKey; the frontend does the IBE math.

## Backend — expose the IBE public key + the caller's encrypted key

The two endpoints are the same shape as any vetKD derivation: `context` is the app's domain separator, `input` is the recipient identity (their principal).

### Rust

```rust
use ic_cdk::update;
use ic_cdk_management_canister::{VetKDCurve, VetKDDeriveKeyArgs, VetKDKeyId, VetKDPublicKeyArgs};

const DOMAIN_SEPARATOR: &[u8] = b"basic_ibe_example_dapp";

fn key_id() -> VetKDKeyId {
    VetKDKeyId { curve: VetKDCurve::Bls12_381_G2, name: "test_key_1".to_string() }
}

#[update]
async fn get_ibe_public_key() -> Vec<u8> {
    let res = ic_cdk_management_canister::vetkd_public_key(&VetKDPublicKeyArgs {
        canister_id: None,
        context: DOMAIN_SEPARATOR.to_vec(),
        key_id: key_id(),
    })
    .await
    .expect("vetkd_public_key failed");
    res.public_key
}

#[update]
async fn get_my_encrypted_ibe_key(transport_public_key: Vec<u8>) -> Vec<u8> {
    let caller = ic_cdk::api::msg_caller();
    let res = ic_cdk_management_canister::vetkd_derive_key(&VetKDDeriveKeyArgs {
        input: caller.as_slice().to_vec(), // identity = caller principal
        context: DOMAIN_SEPARATOR.to_vec(),
        transport_public_key,
        key_id: key_id(),
    })
    .await
    .expect("vetkd_derive_key failed");
    res.encrypted_key
}
```

### Motoko

```motoko
import ManagementCanister "mo:ic-vetkeys/ManagementCanister";
import Principal "mo:core/Principal";
import Text "mo:core/Text";
import Runtime "mo:core/Runtime";

persistent actor {
  // Captured at first install and fixed for the canister's derived keys (immutable after install).
  let keyName = Runtime.envVar<system>("VETKD_KEY_NAME") ?? "test_key_1";
  let keyId : ManagementCanister.VetKdKeyid = { curve = #bls12_381_g2; name = keyName };

  public shared func getIbePublicKey() : async Blob {
    await ManagementCanister.vetKdPublicKey(null, Text.encodeUtf8("basic_ibe_example_dapp"), keyId);
  };

  public shared ({ caller }) func getMyEncryptedIbeKey(transportPublicKey : Blob) : async Blob {
    await ManagementCanister.vetKdDeriveKey(
      Principal.toBlob(caller), Text.encodeUtf8("basic_ibe_example_dapp"), keyId, transportPublicKey);
  };
};
```

## Frontend — encrypt to a principal, then decrypt (TypeScript)

```typescript
import { Principal } from "@icp-sdk/core/principal";
import {
  TransportSecretKey, DerivedPublicKey, EncryptedVetKey, VetKey,
  IbeCiphertext, IbeIdentity, IbeSeed,
} from "@icp-sdk/vetkeys";

// --- Encrypt (sender; no canister call needed if the public key is known/derived offline) ---
async function encrypt(cleartext: Uint8Array, receiver: Principal): Promise<Uint8Array> {
  const publicKey = DerivedPublicKey.deserialize(new Uint8Array(await backend.get_ibe_public_key()));
  const ciphertext = IbeCiphertext.encrypt(
    publicKey,
    IbeIdentity.fromPrincipal(receiver),
    cleartext,
    IbeSeed.random(),
  );
  return ciphertext.serialize(); // store or transmit
}

// --- Get my IBE private key (a VetKey) ---
async function getMyIbePrivateKey(myPrincipal: Principal): Promise<VetKey> {
  const tsk = TransportSecretKey.random();
  const encryptedKey = Uint8Array.from(await backend.get_my_encrypted_ibe_key(tsk.publicKeyBytes()));
  const publicKey = DerivedPublicKey.deserialize(new Uint8Array(await backend.get_ibe_public_key()));
  return EncryptedVetKey.deserialize(encryptedKey).decryptAndVerify(
    tsk,
    publicKey,
    myPrincipal.toUint8Array(), // identity bytes = the backend `input`
  );
}

// --- Decrypt a received message ---
async function decryptMessage(encrypted: Uint8Array, myPrincipal: Principal): Promise<string> {
  const ibeKey = await getMyIbePrivateKey(myPrincipal);
  const plaintext = IbeCiphertext.deserialize(encrypted).decrypt(ibeKey);
  return new TextDecoder().decode(plaintext);
}
```

Exact API: `IbeCiphertext.encrypt(derivedPublicKey, IbeIdentity.fromPrincipal(p), cleartext, IbeSeed.random())` (static); `TransportSecretKey.random()` / `.publicKeyBytes()`; `EncryptedVetKey.deserialize(bytes).decryptAndVerify(tsk, derivedPublicKey, identityBytes)` → `VetKey`; `IbeCiphertext.deserialize(bytes).decrypt(vetKey)`.

## Timelock encryption (reveal after a deadline)

Timelock is IBE where the identity is an **event/lot ID** and the **canister itself** derives the key and decrypts once a deadline passes (e.g. a sealed-bid auction). This requires in-canister decryption, so the low-level primitives are needed — **Rust only** (Motoko has no IBE primitives). Encrypt with `IbeCiphertext.encrypt(...)` (frontend, identity = lot ID); the canister runs a timer and decrypts after the deadline.

```rust
use ic_vetkeys::{DerivedPublicKey, EncryptedVetKey, IbeCiphertext, TransportSecretKey};
use ic_cdk_management_canister::VetKDDeriveKeyArgs;

const DOMAIN_SEPARATOR: &[u8] = b"basic_timelock_ibe_example_dapp";

// Called from an ic_cdk_timers job once the lot's deadline has passed.
async fn decrypt_after_deadline(identity: Vec<u8>, encrypted_values: Vec<Vec<u8>>) -> Vec<Vec<u8>> {
    // The canister decrypts for itself, so a deterministic dummy transport key is fine.
    let tsk = TransportSecretKey::from_seed(vec![0; 32]).expect("tsk");

    let res = ic_cdk_management_canister::vetkd_derive_key(&VetKDDeriveKeyArgs {
        input: identity.clone(),
        context: DOMAIN_SEPARATOR.to_vec(),
        transport_public_key: tsk.public_key().to_vec(),
        key_id: key_id(),
    })
    .await
    .expect("vetkd_derive_key failed");

    let ibe_public_key = DerivedPublicKey::deserialize(&get_ibe_public_key().await).unwrap();
    let ibe_key = EncryptedVetKey::deserialize(&res.encrypted_key)
        .unwrap()
        .decrypt_and_verify(&tsk, &ibe_public_key, &identity)
        .expect("decrypt vetkey");

    encrypted_values
        .iter()
        .map(|v| IbeCiphertext::deserialize(v).unwrap().decrypt(&ibe_key).unwrap())
        .collect()
}
```

The timer is set with `ic_cdk_timers::set_timer_interval(..)` from `#[init]` **and** `#[post_upgrade]` (timers do not survive upgrades). See the `basic_timelock_ibe` example for the full auction.

## Additional References

- Core concepts, key names, cycles, and pitfalls: the main `vetkeys` SKILL.md
- Canonical examples: `motoko/vetkeys/basic_ibe`, `rust/vetkeys/basic_ibe`, `rust/vetkeys/basic_timelock_ibe` in [dfinity/examples](https://github.com/dfinity/examples/tree/master/rust/vetkeys)
