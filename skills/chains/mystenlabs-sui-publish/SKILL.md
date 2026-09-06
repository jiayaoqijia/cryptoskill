---
name: sui-publish
description: >
  Publishing, upgrading, and deploying Sui Move packages. Use this skill when the
  user needs to publish a package, upgrade a published package, deploy to multiple
  networks, serialize transactions for multisig signing, run a local Sui network
  (localnet), prepare for Mainnet launch, monitor production deployments, or debug
  dry run failures. Also use when the user asks about sui client publish, sui client
  upgrade, UpgradeCap, upgrade policies, Published.toml, --serialize-output, localnet,
  mainnet launch checklist, gas estimation, multisig publishing, production monitoring,
  rollback, incident response, devInspectTransactionBlock, or --dry-run.
---

# Publishing, Deploying & Local Network

> **MCP tool:** When available in your environment, also query the Sui documentation MCP server (`https://sui.mcp.kapa.ai`) for up-to-date answers. Use it for verification and for details not covered by these reference files.

> **Source constraint:** All information sourced exclusively from [docs.sui.io](https://docs.sui.io) and [MystenLabs/sui-stack-hello-world](https://github.com/MystenLabs/sui-stack-hello-world).

## Publishing a package

### Canonical hello-world publish flow

For the full-stack starter, publish the existing hello-world package only:

```bash
cd sui-stack-hello-world/move/hello-world
sui move build
sui client publish
```

Use the package ID from the publish output to update `sui-stack-hello-world/ui/src/constants.ts` (`TESTNET_HELLO_WORLD_PACKAGE_ID`). Do not publish a separate counter package, and do not create a second project directory.

### Pre-publish checklist

1. Verify your active environment: `sui client active-env`
2. Verify you have SUI tokens: `sui client balance`
3. Build successfully: `sui move build`

### Publish

```bash
sui client publish
```

This deploys the package to the active network and returns:

- A unique **package ID** (use this for all future interactions)
- An **UpgradeCap** object (sent to your address, controls future upgrades)
- Object IDs for anything created during `init` functions

### Test publishing (ephemeral networks)

Use `sui client test-publish` to publish a package to an ephemeral environment for testing without persisting state to a real network:

```bash
sui client test-publish
```

This publishes the package, runs `init` functions, and returns the same output as `sui client publish` (package ID, UpgradeCap, created objects), but the deployment is not permanent. Use it to:

- Verify that `init` functions execute correctly before committing to a real publish
- Test publish + upgrade flows in CI without consuming Testnet/Devnet resources
- Validate gas costs and object creation before a Mainnet deploy

`test-publish` respects `--build-env` for multi-environment packages:

```bash
sui client test-publish --build-env testnet
```

### After publishing

The publish transaction output lists the package ID under the **created objects** section (alongside the `UpgradeCap` and any objects created by `init` functions). The `published-at` field is also automatically added to your `Published.toml`. To interact with the published package:

```bash
# Call a function
sui client call --package <PACKAGE_ID> --module greeting --function new

# Query an object
sui client object <OBJECT_ID>
```

### "Your package is already published" error

If you see this error when running `sui client publish`, it means `Published.toml` already has an entry for your active environment. This happens when iterating on a package during development.

- To **publish to a different network**, switch environments with `sui client switch --env <ENV>` and run `sui client publish` again. The toolchain tracks published addresses per environment in `Published.toml` automatically — do not delete `Published.toml`.
- To **upgrade** the existing package on the same network, use `sui client upgrade` (see below).

### Upgrading a published package

Published packages are immutable, but you can upgrade by publishing a new version linked to the original. The `UpgradeCap` object controls upgrade authority. **Important:** you can restrict the `UpgradeCap` in the same PTB as the `publish` command — for example, publishing and immediately calling `sui::package::only_additive_upgrades` in one atomic transaction. You can also destroy it entirely to make the package permanently immutable (see upgrade policies below).

```bash
sui client upgrade --upgrade-capability <CAP_ID>
```

#### Finding your UpgradeCap

The `UpgradeCap` object ID is needed for every upgrade. There are several ways to find it:

1. **Published.toml** (preferred): After publishing, the toolchain records the cap ID in `Published.toml` under the `upgrade-capability` field for each environment.
2. **Query owned objects**: List all `UpgradeCap` objects owned by the publish address:
   ```bash
   sui client objects --type 0x2::package::UpgradeCap
   ```
3. **Publish transaction output**: The original `sui client publish` output includes the `UpgradeCap` object ID in the created objects list.
4. **Explorer**: Search for your address on SuiVision (`suivision.xyz`) or Suiscan (`suiscan.xyz`) and filter owned objects by type `0x2::package::UpgradeCap`.

#### Upgrade policies

Upgrade policies restrict what can change:

- **Compatible** (default): The most permissive policy. See detailed rules below.
- **Additive:** New modules can be added, but existing modules cannot change at all.
- **Dependency-only:** Only dependency versions can be updated. No code changes.

**Restricting the UpgradeCap in the same PTB as publish:** You can restrict the `UpgradeCap` in the same programmable transaction block as the `publish` command itself — for example, calling `sui::package::only_additive_upgrades` on the `UpgradeCap` immediately after publishing, all within a single atomic transaction. This is the recommended approach for locking down upgrade policy from the start. Once restricted, you cannot widen the policy.

**Other UpgradeCap options:**
- **Transfer to a multisig address** for shared upgrade governance.
- **Destroy the UpgradeCap** to make the package permanently immutable. Call `sui::package::make_immutable`, which consumes and destroys the `UpgradeCap` object. Once the cap is destroyed, no one can ever upgrade the package again — this is irreversible.

#### Compatible upgrade rules (detailed)

Under the **compatible** policy, these changes are **allowed**:

- Add new functions (public or private)
- Add new modules
- Change function implementations (body)
- Add new struct types
- Change private/friend function signatures

These changes **break compatibility** and will be rejected:

- Remove or rename an existing module
- Remove or rename a public function
- Change a public function's signature (parameters, return types, type parameters)
- Remove, rename, or reorder struct fields
- Change the type of a struct field
- Add or remove struct abilities (`key`, `store`, `copy`, `drop`)
- Remove a struct type entirely
- Change a struct's type parameters

Before upgrading, review your diff against these rules. The `sui client upgrade` command will reject incompatible changes at build time with a descriptive error.

### Type anchoring after upgrades

**Struct types are permanently anchored to the original package ID where they were first published.** After an upgrade, the new package gets a new ID, but all objects created by the upgraded code still have their type rooted in the original package ID.

This has critical implications:
- **Querying objects by type** (e.g., `listOwnedObjects` with a `type` filter) must use the **original** package ID.
- **Calling functions** via `moveCall` must use the **upgraded** (latest) package ID.
- **Frontend apps** should maintain both IDs: `ORIGINAL_PACKAGE_ID` for type queries and `PACKAGE_ID` for function calls.

```ts
// Original publish → package ID 0x1234...
// After upgrade  → package ID 0x5678...

// Query: use ORIGINAL package ID
client.core.listOwnedObjects({
  owner: addr,
  type: '0x1234...::module::MyObject',  // ✅ original ID
});

// Call: use UPGRADED package ID
tx.moveCall({
  target: '0x5678...::module::my_function',  // ✅ upgraded ID
});
```

### Publishing to multiple networks

To publish to a different network (for example, from Testnet to Devnet), switch environments and publish again. Each network gives the package a different ID. The `Published.toml` file tracks published addresses per environment.

Before publishing to a new network, ensure you have tokens for that network:

- **Testnet:** Free tokens through the web faucet at `faucet.sui.io`, Discord (`!faucet <ADDRESS>` in `#testnet-faucet`), or the TypeScript SDK (`requestSuiFromFaucetV2()`). **`sui client faucet` does not work on Testnet.**
- **Devnet:** Free tokens via `sui client faucet`, the web faucet at `faucet.sui.io`, Discord (`!faucet <ADDRESS>` in `#devnet-faucet`), or the TypeScript SDK.
- **Localnet:** Free tokens via `sui client faucet` or the local faucet at `127.0.0.1:5003/gas` or `127.0.0.1:9123/gas` (started with `sui start --with-faucet --force-regenesis`).
- **Mainnet:** SUI tokens with real monetary value. Acquire through exchanges or transfers. No faucet available.

### Serializing for external signing

To generate transaction bytes for signing by another party (for example, a multisig):

```bash
sui client publish --serialize-output
```

This outputs base64 transaction bytes instead of executing.

## Local network (localnet)

Localnet runs a full Sui network on your machine for offline development and rapid iteration. Start it with:

```bash
sui start --with-faucet --force-regenesis
```

The `--force-regenesis` flag resets all on-chain state each time the network starts, giving you a clean environment on every restart. The `--with-faucet` flag starts a local faucet so you can fund addresses.

To connect the CLI to your localnet:

```bash
sui client switch --env localnet
```

Get local tokens via `sui client faucet` or by hitting the local faucet endpoint directly at `127.0.0.1:5003/gas` or `127.0.0.1:9123/gas`.

Localnet is useful for:
- Offline development without depending on Testnet/Devnet availability
- Rapid iteration on publish and upgrade flows (reset state with each restart)
- Testing `init` functions and object creation before deploying to a shared network

## Mainnet launch checklist

Use this checklist when preparing a package for Mainnet publishing. Every item should be verified before executing the publish transaction.

### 1. Tests and coverage

Run the full test suite and confirm all tests pass:

```bash
sui move test
```

For coverage reporting (if your project requires a threshold):

```bash
sui move test --coverage
sui move coverage summary
```

Fix any failing tests before proceeding. Do not publish untested code to Mainnet.

### 2. Dependencies and addresses

- Verify `Move.toml` uses `edition = "2024"` and has no legacy `[addresses]` section or git-based Sui framework dependency.
- Confirm `[environments]` includes a `mainnet` entry with the correct chain ID.
- If using MVR dependencies (`{ r.mvr = "@org/package" }`), verify they resolve on Mainnet.
- Run `sui move build` to confirm clean compilation with no warnings.

### 3. Upgrade policy decision

Decide your upgrade policy **before** publishing — you cannot widen it later:

| Policy | What you can change | When to use |
|---|---|---|
| **Compatible** (default) | Add functions, add modules, update implementations. Cannot remove functions or change struct layouts. | Most packages — gives flexibility for bug fixes while preserving type safety. |
| **Additive** | Add new modules only. Existing modules are frozen. | Packages where you want to extend functionality but guarantee existing code never changes. |
| **Dependency-only** | Only update dependency versions. | Nearly-finalized packages that should only track framework updates. |
| **Immutable** | Nothing. Package is permanently frozen. | Fully audited packages where immutability is a trust guarantee (e.g., token contracts). |

To restrict the policy in the same transaction as publish, include a `moveCall` to `sui::package::only_additive_upgrades`, `only_dep_upgrades`, or `make_immutable` on the `UpgradeCap` in your publish PTB.

### 4. Gas estimation

Mainnet SUI has real monetary value. Estimate gas before publishing:

```bash
sui client publish --dry-run
```

The dry-run output includes `computationCost`, `storageCost`, and `storageRebate`. The total gas required is `computationCost + storageCost - storageRebate`. Ensure your address holds enough SUI to cover this amount plus a margin.

### 5. Signer and custody plan

Decide who controls the publish address and the `UpgradeCap`:

- **Single signer:** Simplest. One key publishes and holds the `UpgradeCap`. Suitable for personal projects or early-stage development.
- **Multisig:** For teams or high-value packages. Create a multisig address, publish using `--serialize-output`, and have the required signers sign offline. Transfer the `UpgradeCap` to the multisig address in the same PTB as publish.
- **Immutable on publish:** If no upgrades will ever be needed, destroy the `UpgradeCap` in the publish PTB (`sui::package::make_immutable`). This removes custody concerns entirely.

For multisig publishing:

```bash
# Generate unsigned transaction bytes
sui client publish --serialize-output

# Each signer signs the bytes, then combine and execute
```

### 6. Final pre-publish verification

Before executing the publish transaction on Mainnet:

- [ ] `sui client active-env` returns `mainnet`
- [ ] `sui client balance` shows sufficient SUI for gas (check dry-run estimate)
- [ ] `sui move build` succeeds with no warnings
- [ ] `sui move test` passes with all tests green
- [ ] `Move.toml` has correct `edition`, no legacy format
- [ ] Upgrade policy is decided and restriction call is included in the PTB (if applicable)
- [ ] Signer key or multisig is ready
- [ ] You have verified the package on Testnet first — same code, same tests, same publish flow

## Dry runs and transaction debugging

A dry run simulates a transaction without submitting it to the network. Use dry runs to:

- Estimate gas costs before execution.
- Verify that a transaction succeeds before asking a user to sign.
- Debug failing transactions by inspecting the error before spending gas.

Wallets (like Slush) automatically perform dry runs before presenting a transaction for signing. If a dry run fails, the wallet shows an error instead of prompting.

From the TypeScript SDK, use `devInspectTransactionBlock` to dry-run a transaction programmatically. From the CLI, the `--dry-run` flag simulates execution.

When debugging a dry run failure: check that all object IDs are correct, the object versions are current, the sender has sufficient gas, the function arguments match the expected types, and the active environment (`sui client active-env`) matches the network where the package is published.

## Production monitoring

Sui packages are immutable once published, so monitoring is critical — you cannot hotfix a live contract, only publish an upgrade.

### What to monitor

| Signal | How | Why |
|---|---|---|
| Failed transactions involving your package | Subscribe to transaction effects via gRPC streaming, filter by package ID | Detects Move aborts, gas failures, or unexpected reverts in production |
| Gas spend | Track `gasUsed` from transaction effects | Catch unexpectedly expensive operations or gas drain attacks |
| Event emission | Subscribe to events by type (`{packageId}::module::EventName`) via gRPC streaming | Core business telemetry — mints, transfers, admin actions, deny list changes |
| Object creation/deletion rates | Query or subscribe to object changes filtered by your types | Detect abnormal activity (mass minting, object spam) |
| Admin/cap usage | Filter events for capability-gated actions | Detect unauthorized or unexpected admin operations |
| Shared object contention | Monitor transaction latency for shared-object transactions | High contention degrades UX; may need object sharding |

### Implementation

Use gRPC streaming subscriptions for real-time monitoring:

```ts
for await (const event of client.subscriptionService.subscribeEvents({
  filter: { MoveEventModule: { package: PACKAGE_ID, module: 'my_module' } },
})) {
  // Forward to your monitoring stack (Grafana, Datadog, PagerDuty, etc.)
}
```

For historical analysis, run a custom indexer (`sui-indexer-alt`) that writes relevant events and transaction effects to your own database. See the `accessing-data` skill's `indexers.md`.

Emit events for every security-critical action in your Move code — admin changes, configuration updates, deny list modifications, object deletions. Events are the only way offchain systems can observe these actions.

## Rollback and incident response

**Sui packages cannot be rolled back.** Published bytecode is immutable. There is no `revert` or `rollback` command. Recovery means publishing a forward-fix upgrade.

### If a bad upgrade is published

1. **Assess scope.** Determine which functions are affected. Existing objects created by prior versions are still valid — their types are anchored to the original package ID.
2. **Publish a fix upgrade immediately.** Write the corrected code, run tests, dry-run on Testnet, then `sui client upgrade` on Mainnet. The new package ID replaces the old one for all future calls.
3. **Update frontends.** Point `PACKAGE_IDS` to the new (fixed) package ID. Type queries still use `ORIGINAL_PACKAGE_IDS`.
4. **Communicate.** If the bug affected user-facing behavior, notify users through your app's channels.

### If the UpgradeCap is compromised

An attacker with the `UpgradeCap` can publish arbitrary code under your package. Mitigation:

- **If you still hold the cap:** Immediately restrict it (`only_dep_upgrades` or `make_immutable`) to prevent further malicious upgrades.
- **If the attacker holds the cap:** You cannot recover upgrade authority. Publish a new package, migrate users, and communicate the migration. This is why multisig custody of the `UpgradeCap` matters for production packages.

### If a shared object is corrupted

A buggy function may write invalid state to a shared object. Since shared objects are mutable by any transaction:

- **If you can upgrade:** Publish an upgrade with a repair function that fixes the corrupted state. Gate it behind an `AdminCap`.
- **If the package is immutable:** The only option is to deploy a new package with a migration function that reads the old object's data (if accessible) and creates corrected objects.

### Prevention checklist

- [ ] `UpgradeCap` held by multisig or restricted to `additive` / `dep_only`
- [ ] All upgrades tested on Testnet with the same code, same publish flow
- [ ] Admin actions emit events for monitoring
- [ ] Critical shared objects have repair functions gated behind capabilities
- [ ] Frontend can switch package IDs without a redeploy (environment config, not hardcoded)
