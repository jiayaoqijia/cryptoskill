# zkLogin Architecture and Protocol Flow

> **Source:** All content sourced from [docs.sui.io/concepts/cryptography/zklogin](https://docs.sui.io/concepts/cryptography/zklogin).

## Three Key Entities

The zkLogin system involves three distinct components:

### 1. Application Frontend
- Stores the ephemeral private key
- Manages the OAuth login flow
- Creates and signs transactions with the ephemeral key
- Computes the user's Sui address from the JWT claims and salt

### 2. Salt Service
- Backend service returning a consistent, unique salt per user
- Salt is derived from the JWT's `iss`, `aud`, and `sub` fields
- The salt unlinks the OAuth identifier from the onchain address
- Losing the salt means permanent loss of access to the address

### 3. Proving Service
- Generates zero-knowledge proofs (Groth16 zkSNARK)
- Inputs: JWT, randomness, salt, max epoch
- The proof validates:
  - Nonce was derived correctly from the ephemeral public key, max epoch, and randomness
  - Key claim value matches the JWT
  - RSA signature on the JWT is valid
  - Address is consistent with the key claim and salt

---

## Technical Terminology

### OpenID Connect Entities
- **OpenID Provider (OP):** OAuth 2.0 authorization server, identified by the `iss` field in the JWT
- **Relying Party (RP):** OAuth client application, identified by the `aud` field
- **Subject Identifier (sub):** Locally unique end-user identifier within the issuer
- **JSON Web Key (JWK):** JSON structure representing the OP's public keys
- **JSON Web Token (JWT):** Token containing header, payload, and signature

### JWT Header Fields
| Field | Value | Description |
|-------|-------|-------------|
| `alg` | RS256 | RSA + SHA-256 (required) |
| `kid` | varies | Identifies the JWK used for verification |
| `typ` | JWT | Token type (required) |

### JWT Payload Fields
| Field | Example | Description |
|-------|---------|-------------|
| `iss` | `https://accounts.google.com` | OAuth provider identifier |
| `aud` | (client ID) | Relying party identifier |
| `nonce` | (hash) | Hash of ephemeral public key, expiry, and randomness |
| `sub` | (user ID) | Unique user identifier within the provider |

---

## Key Notations

| Symbol | Definition |
|--------|-----------|
| `(eph_sk, eph_pk)` | Ephemeral key pair; short-lived, scoped to one session |
| `nonce` | `ToBase64URL(Poseidon_BN254([...]).to_bytes()[len - 20..])` |
| `ext_eph_pk` | Byte representation: `flag \|\| eph_pk` |
| `user_salt` | Unlinks OAuth identifier from onchain address |
| `max_epoch` | Epoch when ephemeral key expires (u64) |
| `kc_name` | Key claim name (e.g., `sub`) |
| `kc_value` | Key claim value (e.g., user ID) |

---

## Protocol Flow (10 Steps)

### Phase 1: Setup (Steps 0-3)

**Step 0:** A one-time decentralized Groth16 zkSNARK ceremony was performed before zkLogin was enabled on Sui. This ceremony generated the Common Reference String (CRS) and the verifying key is pinned in the Sui protocol. This is not a user action.

**Step 1:** Application creates an ephemeral key pair `(eph_sk, eph_pk)`.

**Step 2:** The ephemeral public key, expiry (`max_epoch`), and randomness are embedded in the OAuth nonce.

**Step 3:** User completes the OAuth login flow with the chosen OpenID provider.

### Phase 2: Salt Retrieval (Steps 4-5)

**Step 4:** Application sends the JWT to the salt service.

**Step 5:** Salt service returns a unique `user_salt` based on `iss`, `aud`, and `sub`.

### Phase 3: Proof Generation (Steps 6-7)

**Step 6:** Application sends the JWT, salt, ephemeral public key, randomness, and key claim name to the proving service.

**Step 7:** Proving service generates a ZK proof that validates:
- Nonce was derived correctly from the ephemeral public key, max epoch, and randomness
- Key claim value matches the JWT
- RSA signature on the JWT is valid
- Address is consistent with the key claim and salt

### Phase 4: Transaction Submission (Steps 8-10)

**Step 8:** Application computes the Sui address from `iss`, `aud`, `sub`, and `user_salt`.

**Step 9:** Transaction is signed with the ephemeral private key (`eph_sk`).

**Step 10:** Transaction is submitted to validators with the signature, ZK proof, and auxiliary inputs. Validators verify both the proof and the ephemeral signature.

---

## Address Derivation

The zkLogin address is computed deterministically from the following inputs:

### Computation Steps

1. `zk_login_flag = 0x05` (domain separator for zkLogin)
2. `kc_name_F = hashBytesToField(kc_name, maxKCNameLen)`
3. `kc_value_F = hashBytesToField(kc_value, maxKCValueLen)`
4. `aud_F = hashBytesToField(aud, maxAudValueLen)`
5. `iss`: Provider identifier (e.g., `https://accounts.google.com`)
6. `user_salt`: User-specific salt from the salt service

### Final Address Formula

```
addr_seed = Poseidon_BN254(kc_name_F, kc_value_F, aud_F, Poseidon_BN254(user_salt))
zk_login_address = Blake2b_256(zk_login_flag, iss_L, iss, addr_seed)
```

> **TODO:** The `Poseidon_BN254` hash function used in address derivation will change as part of the zkLogin v2 migration. Update this section once the migration is complete.

### Address Properties

- **Permanent:** The address does not change unless `sub`, `iss`, `aud`, or `user_salt` changes.
- **Provider-specific:** Different OAuth providers produce different addresses for the same user.
- **Application-specific:** Different applications (different `aud` values) produce different addresses for the same user and provider.
- **Not convertible:** A zkLogin address cannot be converted to or from a traditional wallet address. They use different derivation schemes.

---

## Session Lifetime

The ephemeral key pair and `max_epoch` together control the session duration:

1. The ephemeral key pair `(eph_sk, eph_pk)` is generated at login time.
2. `max_epoch` defines when the ephemeral key expires (as a Sui epoch number, u64).
3. The ZK proof is bound to this ephemeral key and max epoch.
4. When the current epoch passes `max_epoch`, the session expires.
5. To continue, the user logs in again, generating a new ephemeral key pair and a new ZK proof.
6. The user's Sui address remains the same across sessions.

The ZK proof can be cached and reused within a session (until the ephemeral key expires), but cannot be reused across sessions.

---

## Groth16 zkSNARK Ceremony

The protocol uses a Groth16 zkSNARK proving system. The ceremony (Step 0) generates the Common Reference String (CRS), which is a one-time setup that produces the proving and verification keys used by all participants. The CRS is generated through a multi-party computation ceremony to ensure security.
