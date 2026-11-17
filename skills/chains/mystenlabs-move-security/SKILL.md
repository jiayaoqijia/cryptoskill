---
name: move-security
description: >
  Audits and hardens Move smart contracts on Sui: access control, capability
  objects, randomness, upgrade governance, emergency controls, and key custody.
  Use when the user asks to review or audit Move code for security issues or
  vulnerabilities, mentions AdminCap, MinterCap, UpgradeCap, capability
  revocation or rotation, tx_context::sender authorization, shared object
  access, onchain randomness or RandomGenerator, oracle or offchain data
  validation, emergency pause or rate limiting, multisig and private key
  custody, or frontend transaction signing safety.

  Related skills: `sui-move` (language), `object-model` (ownership),
  `sui-publish` (upgrades).
---

# Move Smart Contract Security

Source of truth: [docs.sui.io/develop/security/best-practices](https://docs.sui.io/develop/security/best-practices) only. If the Sui docs MCP server (`https://sui.mcp.kapa.ai`) is available, use it to verify details.

## Quick start

- **Authorizing a privileged function?** Take a capability object as the second parameter. Never rely on `tx_context::sender()` alone.
- **Consuming randomness?** The function must be private `entry`, and `RandomGenerator` must be created inside it, never passed in.
- **Holding an admin capability?** Multisig or dedicated custody, plus a revocation mechanism designed before publishing.

Reference files: `access-control.md` (capabilities, allowlists, revocation, shared object authorization) and `best-practices.md` (package auditing, upgrades, dependencies, invariants, events, randomness, oracles, emergency controls, frontend signing, key management). Load one when you need detail beyond the sections below.

---

## Task: review a Move module for security issues

Walk this checklist, then report findings in severity order with the fix for each.

1. **Authorization mechanism.** Does each privileged function take a capability, or does it compare `ctx.sender()` to a stored address? Sender-only checks tie the function to a single signer and break composability — another contract cannot call it on behalf of a user. Recommend a capability object.
2. **Shared state.** Anyone can submit a transaction referencing a shared object, so access is never restricted by sharing alone; every function touching shared state must check authorization internally.
3. **Capability–object relationship.** Assert the capability belongs to the object being modified (store and compare the object ID).
4. **Events.** Every privileged action — admin change, allowlist update, mint/burn, denylist, config change, oracle update, pause — must emit an event so offchain monitoring can detect misuse.
5. **Revocation.** Is there a way to invalidate a leaked capability? Packages are immutable, so this must exist before publishing.
6. **Randomness.** See the randomness section below.
7. **Invariants and external data.** Assert invariants after state changes; validate oracle/offchain data for staleness, bounds, and source.
8. **Emergency controls.** Value-moving paths should have a pause or rate limit.
9. **Package identity.** `Move.toml` names are arbitrary strings, not unique. Verify the onchain package ID; an upgrade publishes a new package at a new address.

### Example finding and fix

A shared `Vault` storing `admin: address` and checking `ctx.sender() == vault.admin`:

> **High — sender-only authorization.** `withdraw` and `change_admin` authorize by comparing `ctx.sender()` to a stored address. This binds the function to a single signer and breaks composability; no other contract can act for the admin. The `Vault` is shared, so anyone can reference it — the internal check is the only barrier.
> **Medium — no events.** Neither `withdraw` nor `change_admin` emits an event, leaving privileged actions invisible to offchain monitoring.
> **Medium — no revocation path.** If the admin key is compromised, nothing invalidates it for the life of the immutable package.

Fix:

```move
public struct AdminCap has key, store { id: UID, vault_id: ID }

public struct Withdrawn has copy, drop { vault: ID, amount: u64 }

public fun withdraw(
    vault: &mut Vault,          // object first
    cap: &AdminCap,             // capability second: keeps method associativity
    amount: u64,
    ctx: &mut TxContext,
): Coin<SUI> {
    assert!(cap.vault_id == object::id(vault), ENotAuthorized);
    event::emit(Withdrawn { vault: object::id(vault), amount });
    coin::take(&mut vault.balance, amount, ctx)
}
```

---

## Task: capability object vs address allowlist

**Default: the capability object.** Capabilities compose — another protocol can hold a `MinterCap` on behalf of a user, which an allowlist keyed on `tx_context::sender()` cannot support. Require the capability as a parameter, placed **second** (after the object acted on) so method associativity still works.

**Escape hatch — allowlist:** if the authorized set must be mutable from a single admin action, store it in a well-defined object, restrict who may update it, and emit an event on every change. Even then, authorization still needs an explicit check inside each function, because the holding object is shared.

Design the revocation mechanism before publishing either way (next section).

---

## Task: protect, revoke, and rotate an admin capability

**Custody.** Hold `AdminCap`/`UpgradeCap` in a multisig address, hardware wallet, or dedicated custody — never a single hot wallet. Treat `UpgradeCap` as seriously as an admin capability: its holder can change package behavior. Each transfer grants full privileges, so do not transfer casually. Separate deploy, admin, and operations keys.

**If a capability leaks and no revocation exists, it remains valid for the life of the package** — the package is immutable and cannot be patched to ignore it.

Revocation options, chosen before publishing:

| Mechanism | How it works | Needs holder cooperation? |
|---|---|---|
| Onchain registry of valid capability IDs | Each privileged function checks the capability ID against the registry; admins remove compromised IDs | No |
| Version / epoch field | Capability carries a version; functions reject versions below the current one, so bumping invalidates older capabilities | No |
| Destruction function | Holder calls a function that deletes the capability | Yes |

Pair any of these with a documented rotation path: mint the replacement capability, move it to the new custody, then invalidate the old ID or bump the version.

---

## Task: audit randomness usage

Checklist for any function consuming `Random`:

- [ ] The function is **private `entry`** — not `public`. The Move compiler lints against `public` functions that take `Random` or `RandomGenerator`.
- [ ] Private entry is what prevents other modules from composing randomness calls into larger attacks (e.g. aborting on an unfavorable draw).
- [ ] `RandomGenerator` is **never a parameter**. Create it inside the entry function with `r.new_generator(ctx)` and pass it only to `public(package)` or private helpers.
- [ ] Gas paths are balanced: the favorable outcome consumes equal or more gas than the unfavorable one, so a caller cannot force an abort on bad draws.
- [ ] For high-stakes applications, consider commit-reveal instead of a single-transaction draw.

So `public fun draw_winner(lottery: &mut Lottery, rng: &mut RandomGenerator, ...)` is unsafe on two counts — it is `public`, and it accepts the generator. Correct shape:

```move
entry fun draw_winner(lottery: &mut Lottery, r: &Random, ctx: &mut TxContext) {
    let mut gen = r.new_generator(ctx);
    // use gen here, or pass to public(package)/private helpers
}
```

---

## Other checks

- **Upgrades:** restrict or burn `UpgradeCap` per the intended policy; verify dependency package IDs onchain, not by name.
- **Oracles/offchain data:** validate staleness, bounds, and source before acting on it.
- **Emergency controls:** pause flags and rate limits on value-moving paths, each emitting an event.
- **Frontend signing:** verify the package ID the transaction targets and show users what they are signing.

Details for all four are in `best-practices.md`.
