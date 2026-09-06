# zkLogin Integration Guide

> **Source:** All content sourced from [docs.sui.io/concepts/cryptography/zklogin](https://docs.sui.io/concepts/cryptography/zklogin).

## Supported OpenID Providers

### All Networks (Mainnet, Testnet, Devnet)
- Facebook
- Google
- Twitch
- Apple
- AWS (Tenant)
- Karrier One
- Credenza3

### Devnet and Testnet Only (Not Mainnet)
- Slack
- Kakao
- Microsoft

### Under Review
- RedBull
- Amazon
- WeChat
- Auth0
- Okta

---

## Implementation Steps

Integrating zkLogin into a Sui application follows the 10-step protocol flow. At a high level:

### 1. Generate Ephemeral Key Pair
Create a short-lived key pair `(eph_sk, eph_pk)` for the session. Choose a `max_epoch` to define when the session expires and generate randomness.

### 2. Construct the OAuth Nonce
Embed the ephemeral public key, `max_epoch`, and randomness into the OAuth nonce. The nonce links the OAuth session to the ephemeral key.

### 3. Initiate OAuth Login
Redirect the user to the chosen OpenID provider (e.g., Google) with the constructed nonce. The user authenticates and the provider returns a JWT.

### 4. Retrieve the Salt
Send the JWT to your salt service. The salt service returns a consistent `user_salt` derived from the JWT's `iss`, `aud`, and `sub` fields.

### 5. Generate the ZK Proof
Send the JWT, salt, ephemeral public key, randomness, and key claim name to the proving service. The proving service returns a Groth16 zkSNARK proof.

### 6. Compute the Sui Address
Derive the user's Sui address from `iss`, `aud`, `sub` (key claim value), and `user_salt` using the address derivation formula (see `architecture.md`).

### 7. Sign and Submit Transactions
Sign transactions with the ephemeral private key (`eph_sk`). Submit to validators with the signature, ZK proof, and auxiliary inputs.

---

## Offchain Signature Verification

There are four methods to verify zkLogin signatures offchain:

### 1. Sui TypeScript SDK
Use the SDK's built-in verification functions.

### 2. GraphQL Endpoint
Query the Sui GraphQL endpoint:
```
https://sui-[network].mystenlabs.com/graphql
```
Replace `[network]` with `mainnet`, `testnet`, or `devnet`.

### 3. Sui Keytool CLI
```bash
sui keytool zk-login-sig-verify \
  --sig $ZKLOGIN_SIG \
  --bytes $BYTES \
  --intent-scope 3 \
  --network devnet \
  --curr-epoch 3
```

### 4. Self-hosted Verifier
Deploy the zklogin-verifier from the official repository for self-hosted verification.

---

## Security Considerations

### JWT Security
- A leaked JWT can compromise privacy but **cannot** steal funds.
- Fund theft requires the ephemeral private key in addition to the JWT.
- The JWT is not published onchain. However, `iss`, `aud`, and `kid` are revealed onchain.

### Salt Security
- A leaked salt allows linking the OAuth `sub` to the Sui address, compromising privacy.
- A leaked salt alone **cannot** enable fund theft.
- **Losing the salt means permanent loss of access** to the associated Sui address.
- Consider using a multisig wallet with a backup signer for recovery in case of salt loss.

### Ephemeral Private Key Security
- If the ephemeral private key is lost, generate a new key pair (log in again).
- If the ephemeral private key is compromised, the attacker also needs the salt and a valid ZK proof to create transactions.

### ZK Proof Security
- A ZK proof alone cannot create a valid transaction; the ephemeral signature is also required.
- Proofs are bound to a specific ephemeral key and max epoch.
- Proofs can be cached and reused within a session but not across sessions.

### Privacy Properties
- By default, there is no link between the OAuth `sub` and the Sui address (this is the purpose of the salt).
- The JWT is not published onchain.
- The following fields **are** revealed onchain: `iss`, `aud`, `kid`.

### Two-Factor Security Model
zkLogin is effectively a two-factor system:
- Factor 1: OAuth credential (JWT from the provider)
- Factor 2: Salt (from the salt service)

An OAuth provider compromise alone cannot result in fund theft because the attacker would still need the salt.

---

## FAQ

### Does zkLogin support mobile?
Yes. zkLogin is a protocol-level primitive and works on mobile.

### Can I reuse a ZK proof across sessions?
No. A proof is valid only until the ephemeral key expires (defined by `max_epoch`). However, you can cache and reuse the proof within a single session.

### Can I convert a traditional wallet to a zkLogin address?
No. Traditional wallets and zkLogin addresses use different address derivation schemes. They are not interchangeable.

### What happens if the OAuth provider is compromised?
Fund theft is not possible through OAuth compromise alone. zkLogin is a two-factor system: the attacker would also need the user's salt to derive the correct address and create valid transactions.

### What happens if I lose access to my OAuth account?
You must be able to produce a current JWT from the OAuth provider. If you lose OAuth access entirely, you lose the ability to generate new proofs and sign transactions. To mitigate this risk, use a multisig wallet with a backup signer for recovery.
