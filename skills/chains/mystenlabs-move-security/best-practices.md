# Security Best Practices

> Source: [docs.sui.io/develop/security/best-practices](https://docs.sui.io/develop/security/best-practices)

---

## Package auditing and immutability

- Sui packages are immutable once published. During a package upgrade, a new package with a new address is published. Verify package IDs directly onchain rather than relying on names or frontend constants.
- Audit both current packages and their upgrade policies before trusting them.
- The `UpgradeCap` controls all future versions and should be treated as security-critical.

## Upgrade governance

- Protect `UpgradeCap` with the same rigor as admin capabilities since holders can modify package behavior.
- Apply custom upgrade policies, multisig, or timelocks to prevent unilateral upgrades.
- Call `make_immutable` on `UpgradeCap` to prevent package upgrades permanently. This is an irreversible action.

## Package versioning

- Version every published package and assert on the current version in every `public` function. This is essential for safe upgrades.
- Store the version in a shared configuration object and check it at the start of each entry point.
- When upgrading, increment the version and migrate state in the same transaction to prevent calls against stale logic.

## Emergency pause mechanism

- Implement a pause or "stop" capability as a red button for quick response to security incidents.
- Gate the pause behind a dedicated capability (e.g., `PauseCap`) held in multisig custody.
- When paused, all public functions should abort early. Emit an event on pause and unpause for auditability.

## Dependency verification

- Verify exact onchain package IDs and dependency IDs, not just names.
- Upgradeable dependencies can change after your audit completes. Re-verify when dependencies update.

## Move language guarantees

- Move's type system, resource model, bytecode verifier, and checked arithmetic prevent whole classes of bugs but do not replace business-logic review.
- Unexpected aborts from checked arithmetic can still cause denial of service. Check zero and overflow edge cases despite checked arithmetic.

## Invariant and relationship validation

- Many Sui bugs exploit valid objects in wrong relationships.
- Within privileged functions, validate:
  - Amounts
  - Object IDs
  - Dynamic field keys
  - Ownership
  - Inter-object relationships
- Validate that capabilities match the specific objects they govern.

## Event emission for privileged actions

Emit events for all privileged actions to enable offchain monitoring of unexpected behavior:

- Admin changes
- Allowlist updates
- Mint/burn operations
- Denylist actions
- Configuration changes
- Oracle updates
- Emergency pauses

## Onchain randomness security

### Post-random command restrictions

- Sui restricts which commands can follow a `MoveCall` that consumes `Random` in the same PTB.
- Only allowed object transfers and coin merges can follow random calls.
- This prevents test-and-abort attacks where attackers abort unfavorable outcomes.

### Function declaration requirements

- Mark randomness-consuming functions as private `entry` only.
- The Move compiler lints against `public` functions that take `Random` or `RandomGenerator`.
- Private entry prevents other modules from composing randomness calls into larger attacks.

### RandomGenerator parameter restriction

- Never accept `RandomGenerator` as a `public` function parameter. Passing it to `public(package)` or private functions is acceptable for testing and in-package logic.
- Always create the generator within the entry function via `r.new_generator(ctx)` and pass it only to internal helpers.

### Gas path balance

- Design functions so favorable outcomes consume equal or more gas than unfavorable ones.
- This prevents attackers from setting gas budgets that cover only desired outcomes.

### Commit-reveal pattern

- Consider a two-transaction commit-reveal pattern for high-stakes applications to further reduce caller influence over outcomes.

## Oracle and offchain data security

- Validate offchain data before using it (price feeds, etc.).
- Check data freshness and confirm source.
- Verify signatures and apply replay protection.
- Define explicit failure behavior for missing, stale, or invalid data.

## Emergency controls

- Consider pause mechanisms, kill-switches, or rate-limits for high-value applications.
- Document who can trigger controls and how to prevent abuse.
- Gate emergency controls with capabilities and emit events on usage.

## Frontend and transaction signing

### Human-readable intent display

- Show users human-readable descriptions of what transactions do before signing.
- Avoid blind signing of opaque bytes.
- Dry-run or simulate transactions so expected effects are visible first.

### Package ID verification

- Verify exact package IDs your frontend calls at runtime.
- Do not trust packages based only on names or compiled constants.
- Pin audited IDs and check them during execution.

## Key management

### Private key protection

- Keep private signature keys private.

### Privileged key custody

- Hold admin keys in multisig addresses, hardware wallets, or dedicated custody.
- Avoid single hot wallets for privileged keys.

### Key role and network separation

- Use separate keys for deployer, admin, and routine operations.
- Prevent compromise of one role from affecting others.
- Keep Testnet and Mainnet keys separate.

### Recovery and rotation documentation

- Document procedures before launch to enable quick response to lost or compromised keys.
