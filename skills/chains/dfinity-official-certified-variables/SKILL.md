---
name: certified-variables
description: "Serve cryptographically verified responses from query calls using Merkle trees and subnet BLS signatures. Covers the certified data API, RbTree/CertTree construction, witness generation, HTTP response certification for custom http_request canisters (ic-http-certification), and frontend certificate validation (@dfinity/certificate-verification). Use when query responses need verification, certified data, or response authenticity proofs. For static frontends served by the certified-assets canister, use the static-site skill instead: certification is automatic there."
license: Apache-2.0
compatibility: "icp-cli >= 0.2.2"
metadata:
  title: Certified Variables
  category: Security
---

# Certified Variables

A query call is answered by a single replica, without consensus, so a faulty or malicious replica can return fabricated data. Certification closes that gap: during update calls the canister stores a 32-byte hash (usually the root of a Merkle tree over its data) in the subnet's certified state, and query responses carry a certificate signed by the subnet's threshold BLS key. Clients verify the certificate and a Merkle witness, and get a fast query response that is as trustworthy as an update call.

## Who Verifies What

Decide this first. Certification only helps if something checks it.

| Response | Verified by | Client code needed |
|----------|-------------|--------------------|
| HTTP from a frontend canister or `http_request`, via `<id>.icp.net` or a custom domain | the HTTP gateway | none |
| The same, via `<id>.raw.icp.net` or your own HTTP client | nobody | `@dfinity/response-verification` (`verifyRequestResponsePair`) |
| Update call through an actor (`agent.update`) | consensus; the agent checks the response certificate | none |
| Candid **query** call through an actor | only the answering node's signature | **certified data + `@dfinity/certificate-verification`** (this skill) |

The gateway never verifies Candid API calls (`/api/...`), even when the page came from a verifying host: on `ic0.app`, `icp0.io` or local origins the agent sends them through the page origin, and the gateway only proxies them. Certify a query when a client acts on its result: balances, permissions, prices, anything security-relevant. The alternative is to call the method as an update and accept consensus latency. Ledgers implementing ICRC-3 already certify their tip: `icrc3_get_tip_certificate` returns `opt { certificate; hash_tree }`, which verifies with `verifyCertification` like any witness below (labels `last_block_index`, a LEB128 number, and `last_block_hash`, so decode them instead of the helper's UTF-8 compare).

Static frontends served by the certified-assets canister (`@dfinity/static-site` recipe) are certified automatically: load the `static-site` skill for those.

## Versions

| Side | Package | Version | Used for |
|------|---------|---------|----------|
| Rust | `ic-cdk` | 0.20 | `certified_data_set` / `data_certificate` |
| Rust | `ic-certification` (feature `serde`) | 4 | `RbTree` Merkle map with witnesses |
| Rust | `ic-http-certification` | 4 | certifying `http_request` responses |
| Motoko | `core` | 2.6 | `mo:core/CertifiedData` |
| Motoko | `ic-certification` (mops) | 1.1 | `CertTree` Merkle tree with witnesses |
| Motoko | `sha2` (mops) | 0.2 | hashing a single certified value |
| Frontend | `@icp-sdk/core` | ^6 | agent, `Certificate`, `lookup_path` |
| Frontend | `@dfinity/certificate-verification` | ^4 | witness verification (peers `@icp-sdk/core` ^6, takes `Uint8Array`) |

`ic-certified-map` 0.4 exposes the same `RbTree`/`AsHashTree` API and still works, but `ic-certification` is maintained alongside `ic-http-certification` and is what the official examples use.

## Root Key

Client-side verification needs the root key of the network the canister runs on:
- **Browser:** `safeGetCanisterEnv()?.IC_ROOT_KEY` from the `ic_env` cookie (`@icp-sdk/core/agent/canister-env`), set by the frontend canister on local networks and mainnet alike. It is the key of the network serving the page; to verify a canister on another network (e.g. mainnet data from a local dev server), use that network's key. It is only as trustworthy as the page: on a verifying hostname the gateway verifies the cookie along with the page, but a page from a `raw` hostname can carry a forged key, so a client verifying `raw` responses needs an independently obtained key.
- **Node scripts and tests:** `root_key` from `icp network status --json`, hex-decoded to bytes.
- **Mainnet:** the agent's built-in default (`agent.rootKey` on an agent created without `rootKey`): `308182301d060d2b0601040182dc7c0503010201060c2b0601040182dc7c05030201036100814c0e6ec71fab583b08bd81373c255c3c371b2e84863c98a4f1e08b74235d14fb5d9c0cd546d9685f913a0c0b2cc5341583bf4b4392e467db96d65b9bb4cb717112f8472e0d5a4d14505ffd7484b01291091c5f87b98883463f98091a0baaae`

Never call `fetchRootKey()` in shipped code: it trusts whatever key the replica sends (see the `canister-security` skill).

## Pitfalls

1. **Certifying more than 32 bytes.** `certified_data_set` / `CertifiedData.set` accept at most 32 bytes. Build a Merkle tree over the data and certify its root hash; the tree provides per-key proofs.

2. **Setting certified data in a query, or not at install and after every change.** `certified_data_set` can be called from `canister_init`, `canister_post_upgrade`, `canister_pre_upgrade`, update methods, reply/reject callbacks, and system tasks (heartbeat, global timer, low-Wasm-memory hook); it traps anywhere else, including any query (even one called as an update) and cleanup callbacks. Certified data starts empty on install, so certify the initial state in `init` (Rust) or the actor body (Motoko), or queries fail verification until the first write. Forgetting to set it after a mutation leaves a stale hash with the same result. Batch writes need only one `certified_data_set` after the last insert.

3. **Expecting a certificate from a call that is not a query call.** `data_certificate()` / `CertifiedData.getCertificate()` return `None`/`null` in update calls, and a query method invoked as an update call counts as one. **`icp canister call` sends an update call unless you pass `--query`**: without it, the Rust example below traps on its `expect`, and the Motoko examples return `certificate = null`. Frontend code calling a `query` method through an actor sends a query call automatically.

4. **Losing the tree on upgrade, not the certified data.** The certified data itself survives upgrades (install and reinstall start it empty). What does not survive is a Merkle tree kept on the heap: the Rust `RbTree` below is wiped on upgrade while the old hash stays set, so `#[post_upgrade]` must rebuild the tree (from stable storage in a real app, see the `stable-memory` skill) and call `certified_data_set` again. A Motoko `CertTree.Store` persists with the actor, so nothing needs re-setting after an upgrade.

5. **Building the witness for the wrong key.** The witness must reveal the exact path being queried; a witness for `users/alice` proves nothing about `users/bob`.

6. **Treating every non-`Found` lookup as "absent".** `lookup_path` returns a status: `Found` (value proven), `Absent` (absence proven), or `Unknown`/`Error` (the witness does not cover the path). Only `Absent` proves a key does not exist. Collapsing `Unknown` into "not found" (for example with `lookupResultToBuffer`, which returns `undefined` for all three) lets a replica send a witness for a different key and make a real value look missing.

7. **Skipping the freshness check.** The certificate's `/time` is when the subnet signed it; without a bound, a stale certificate with outdated data can be replayed. `verifyCertification` enforces `maxCertificateTimeOffsetMs` (5 minutes is a sensible value); `Certificate.create` enforces ±5 minutes by default (`maxAgeInMinutes`).

8. **Declaring the Motoko `CertTree.Ops` object as stable.** In a persistent actor, `let ct = CertTree.Ops(certStore)` fails with `M0131` (`variable ct is declared stable but has non-stable type`). Declare it `transient let ct = CertTree.Ops(certStore);`; only the `CertTree.Store` is stable.

9. **Certifying an HTTP response without its `IC-CertificateExpression` header.** With `ic-http-certification`, the header carrying the CEL expression must be part of the response you certify; `HttpCertification::response_only`/`full` return `CertificateExpressionHeaderMissing` otherwise. Serve exactly that response, plus the `IC-Certificate` header from `add_v2_certificate_header`, or the HTTP gateway rejects it with `backend_response_verification`.

## Canister

### Rust

```toml
[package]
name = "certified_vars_backend"
version = "0.1.0"
edition = "2021"

[lib]
crate-type = ["cdylib"]

[dependencies]
candid = "0.10"
ic-cdk = "0.20"
ic-certification = { version = "4", features = ["serde"] }
serde = { version = "1", features = ["derive"] }
serde_bytes = "0.11"
ciborium = "0.2"
```

```rust
use candid::{CandidType, Deserialize};
use ic_cdk::{init, post_upgrade, query, update};
use ic_certification::{AsHashTree, RbTree};
use serde_bytes::ByteBuf;
use std::cell::RefCell;

thread_local! {
    // RbTree is a Merkle-tree-backed map: keys and values are byte slices
    static TREE: RefCell<RbTree<Vec<u8>, Vec<u8>>> = RefCell::new(RbTree::new());
}

// Update the certified data hash after any modification
fn update_certified_data() {
    TREE.with(|tree| {
        let tree = tree.borrow();
        // root_hash() returns a 32-byte SHA-256 hash of the entire tree
        ic_cdk::api::certified_data_set(&tree.root_hash());
    });
}

#[init]
fn init() {
    update_certified_data();
}

#[post_upgrade]
fn post_upgrade() {
    // This example keeps TREE on the heap only: it is empty after an upgrade, while the
    // old certified hash is kept. A real canister reinserts its entries from stable storage
    // here first; this one re-certifies the empty tree so the hash matches it again.
    update_certified_data();
}

#[update]
fn set(key: String, value: String) {
    TREE.with(|tree| {
        let mut tree = tree.borrow_mut();
        tree.insert(key.as_bytes().to_vec(), value.as_bytes().to_vec());
    });
    // Must update certified hash after every data change
    update_certified_data();
}

#[update]
fn delete(key: String) {
    TREE.with(|tree| {
        let mut tree = tree.borrow_mut();
        tree.delete(key.as_bytes());
    });
    update_certified_data();
}

#[derive(CandidType, Deserialize)]
struct CertifiedResponse {
    value: Option<String>,
    certificate: ByteBuf,      // subnet BLS signature
    witness: ByteBuf,          // Merkle proof for this key
}

#[query]
fn get(key: String) -> CertifiedResponse {
    // data_certificate() is only available in query calls (icp canister call --query)
    let certificate = ic_cdk::api::data_certificate()
        .expect("data_certificate only available in query calls");

    TREE.with(|tree| {
        let tree = tree.borrow();

        // Look up the value
        let value = tree.get(key.as_bytes())
            .map(|v| String::from_utf8(v.clone()).unwrap());

        // Build a witness (Merkle proof) for this specific key
        let witness = tree.witness(key.as_bytes());

        // Serialize the witness as CBOR
        let mut witness_buf = vec![];
        ciborium::into_writer(&witness, &mut witness_buf)
            .expect("Failed to serialize witness as CBOR");

        CertifiedResponse {
            value,
            certificate: ByteBuf::from(certificate),
            witness: ByteBuf::from(witness_buf),
        }
    })
}

// Required by the icp-cli Rust recipe, which extracts the Candid interface from the wasm
ic_cdk::export_candid!();
```

### Motoko: single value

A single value needs no Merkle tree: certify its hash, and the client compares `sha256(value)` with the certificate's `certified_data` (see "Single value without a witness").

```motoko
import CertifiedData "mo:core/CertifiedData";
import Text "mo:core/Text";
// Requires: mops add sha2
import Sha256 "mo:sha2/Sha256";

persistent actor {

  // Simple certified single-value example:
  var certifiedValue : Text = "";

  // Certify the hash of the current value (max 32 bytes; traps in a query call)
  func certify() {
    CertifiedData.set(Sha256.fromBlob(#sha256, Text.encodeUtf8(certifiedValue)));
  };

  // Certify the initial value at install: certified data starts empty, not as sha256("")
  certify();

  // Set a certified value (update call only)
  public func setCertifiedValue(value : Text) : async () {
    certifiedValue := value;
    certify();
  };

  // Get the certified value with its certificate (query call)
  public query func getCertifiedValue() : async {
    value : Text;
    certificate : ?Blob;
  } {
    {
      value = certifiedValue;
      certificate = CertifiedData.getCertificate();
    }
  };
};
```

### Motoko: key-value store with witnesses

`CertTree` from the `ic-certification` mops package (`mops add ic-certification`) is a Merkle tree that produces per-key witnesses:

```motoko
import CertifiedData "mo:core/CertifiedData";
import Blob "mo:core/Blob";
import Text "mo:core/Text";
// Requires: mops add ic-certification
import CertTree "mo:ic-certification/CertTree";

persistent actor {

  // CertTree.Store is stable -- the tree persists across upgrades, and so does the certified data
  let certStore : CertTree.Store = CertTree.newStore();
  // Ops is an object with functions, not stable data: it must be transient
  transient let ct = CertTree.Ops(certStore);

  // Set certified data on init
  ct.setCertifiedData();

  // Set a key-value pair and update certification
  public func set(key : Text, value : Text) : async () {
    ct.put([Text.encodeUtf8(key)], Text.encodeUtf8(value));
    // CRITICAL: call after every mutation to update the subnet-certified root hash
    ct.setCertifiedData();
  };

  // Delete a key and update certification
  public func delete(key : Text) : async () {
    ct.delete([Text.encodeUtf8(key)]);
    ct.setCertifiedData();
  };

  // Query with certificate and Merkle witness for the requested key
  public query func get(key : Text) : async {
    value : ?Blob;
    certificate : ?Blob;
    witness : Blob;
  } {
    let path = [Text.encodeUtf8(key)];
    // reveal() generates a Merkle proof for this specific path
    let witness = ct.reveal(path);
    {
      value = ct.lookup(path);
      certificate = CertifiedData.getCertificate();
      witness = ct.encodeWitness(witness);
    }
  };
};
```

### Custom `http_request` canisters

Canisters that serve HTTP from their own `http_request` must certify each response with `ic-http-certification` so the HTTP gateway can verify it. Read `references/http-certification.md` before writing one: it has a complete, minimal canister (certify in `init`/`post_upgrade`, attach the witness in `http_request`, and a certified 404 for every other path) and the header rules from pitfall 9. Every path the gateway can request needs a certified response: an uncertified error or 404 is rejected with `backend_response_verification`.

## Client Verification (TypeScript)

`@icp-sdk/core` ships every primitive (`Certificate.create`, `Cbor`, `reconstruct`, `lookup_path`); `@dfinity/certificate-verification` wraps them for the witness case: it verifies the certificate signature, checks `/time`, decodes the witness, and checks that its root hash equals the certificate's `certified_data`. Candid `blob` fields arrive as `Uint8Array` in `@icp-sdk/bindgen` bindings. bindgen turns `opt` record fields into optional properties that are `undefined` when empty. The helpers take the getters' responses as returned: a Motoko `?Blob` value or certificate is `Uint8Array | undefined`, and the witness helper decodes a `Uint8Array` value as UTF-8. Take the root key from "Root Key".

### With a witness

```typescript
import { verifyCertification } from "@dfinity/certificate-verification";
import { lookup_path, LookupPathStatus } from "@icp-sdk/core/agent";
import { Principal } from "@icp-sdk/core/principal";

const MAX_CERT_TIME_OFFSET_MS = 5 * 60 * 1000; // 5 minutes

export async function getVerifiedValue(
  rootKey: Uint8Array,
  canisterId: string,
  key: string,
  // value is opt text (Rust) or ?blob (Motoko); certificate is a blob (Rust) or ?blob (Motoko)
  response: {
    value?: string | Uint8Array | null;
    certificate?: Uint8Array | null;
    witness: Uint8Array;
  },
): Promise<string | null> {
  if (!response.certificate) throw new Error("no certificate: call the getter as a query");
  const value =
    response.value instanceof Uint8Array
      ? new TextDecoder().decode(response.value)
      : (response.value ?? null);
  // Checks signature, time and root hash; throws CertificateTimeError or CertificateVerificationError.
  const tree = await verifyCertification({
    canisterId: Principal.fromText(canisterId),
    encodedCertificate: response.certificate,
    encodedTree: response.witness,
    rootKey,
    maxCertificateTimeOffsetMs: MAX_CERT_TIME_OFFSET_MS,
  });

  // The path must match how the canister inserted the key (here: UTF-8 bytes).
  const result = lookup_path([new TextEncoder().encode(key)], tree);
  switch (result.status) {
    case LookupPathStatus.Found: {
      const verified = new TextDecoder().decode(result.value);
      if (value !== verified) throw new Error("value does not match witness");
      return verified;
    }
    case LookupPathStatus.Absent:
      if (value !== null) throw new Error("witness proves the key is absent");
      return null;
    default:
      // Unknown/Error: the witness does not cover this key, so it proves nothing
      throw new Error(`witness does not cover key (${result.status})`);
  }
}
```

### Single value without a witness

`verifyCertification` needs a witness tree, so verify the Motoko single-value example with `Certificate.create` directly. It checks the signature and the ±5 minute freshness window:

```typescript
import { Certificate, lookupResultToBuffer, uint8Equals } from "@icp-sdk/core/agent";
import { Principal } from "@icp-sdk/core/principal";

export async function verifySingleValue(
  rootKey: Uint8Array,
  canisterId: string,
  // certificate is ?blob in the Motoko getter; empty means it did not run as a query call
  response: { value: string; certificate?: Uint8Array | null },
): Promise<string> {
  if (!response.certificate) throw new Error("no certificate: call the getter as a query");
  const principal = Principal.fromText(canisterId);
  const cert = await Certificate.create({
    certificate: response.certificate,
    rootKey,
    principal: { canisterId: principal },
  });
  const certifiedData = lookupResultToBuffer(
    cert.lookup_path(["canister", principal.toUint8Array(), "certified_data"]),
  );
  // Recompute what the canister certified: sha256 of the UTF-8 value
  const hash = new Uint8Array(
    await crypto.subtle.digest("SHA-256", new TextEncoder().encode(response.value)),
  );
  if (!certifiedData || !uint8Equals(certifiedData, hash)) {
    throw new Error("value does not match certified data");
  }
  return response.value;
}
```

A runnable single-value example with a browser frontend that verifies with `Certificate.create` is [dfinity/examples `motoko/cert-var`](https://github.com/dfinity/examples/tree/master/motoko/cert-var). It certifies the raw 4-byte `Nat32` instead of a hash.

## Checking It Works

```bash
icp canister call backend set '("greeting", "hello world")'
icp canister call --query backend get '("greeting")'
# Expected: certificate = blob "..." (Rust) / opt blob "..." (Motoko); null or a trap means the call was not a query
```

Then run the client function against a response: it must return the value, and must throw once `response.value` is changed.
