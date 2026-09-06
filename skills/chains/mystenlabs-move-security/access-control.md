# Access Control Patterns

> Source: [docs.sui.io/develop/security/best-practices](https://docs.sui.io/develop/security/best-practices)

---

## Capability objects vs address allowlists

- Prefer capability objects (structs with `key` ability) over address allowlists as the default authorization mechanism.
- Capability objects compose well since other protocols can hold them on behalf of users.
- Avoid maintaining onchain address lists when possible.

## Address allowlist management

When address allowlists are necessary:

- Store allowlists in well-defined objects with restricted update access.
- Emit events whenever entries change for auditability.
- Consider time-locks on updates to give observers time to react.

## Avoid `tx_context::sender()` alone

- Using only `tx_context::sender()` as an authorization check ties functions to single signers and breaks composability.
- On Sui, other contracts cannot call functions on behalf of another address — each transaction has a single sender. This means `tx_context::sender()` checks prevent any contract-to-contract delegation.
- Reserve `tx_context::sender()` for cases where the signer is genuinely the only valid actor.

## Explicit capability requirements

- Require relevant capabilities as parameters for all privileged functions (`AdminCap`, `TreasuryCap`, `DenyCapV2`).
- Place the capability as the second parameter to maintain method associativity.
- Move's type system enforces capability requirements at compile time — a function requiring `AdminCap` cannot be called without one, and the transaction will fail if the caller does not own or have access to the required capability object.

## Admin capability protection

- Treat admin capabilities as high-value assets.
- Hold in multisig address or dedicated custody rather than single hot wallets.
- Do not transfer casually as each transfer grants full privileges.
- Plan a rotation path before publishing.

## Capability revocation mechanisms

Design revocation before publishing the package. Options include:

- **Onchain registry of valid capability IDs:** Check the registry inside privileged functions. Works without holder cooperation.
- **Version or epoch fields:** Advance a version counter to invalidate older capabilities. Works without holder cooperation.
- **Destruction functions:** Allow the capability holder to destroy the capability. Requires holder cooperation.

Without a revocation mechanism, a leaked capability remains valid for the life of the package.

Registry or version checks work without holder cooperation. Destruction requires cooperation from the holder.

## Capability-object relationship validation

- When a capability governs a specific object, store the object ID in the capability (or vice versa).
- Check that IDs match inside the function to prevent using valid capabilities on wrong objects.

## Shared object authorization

- Anyone can submit a transaction that references a shared object.
- Never assume shared object access is restricted.
- Require capabilities, validate sender, or check ownership inside every privileged function touching shared state.
