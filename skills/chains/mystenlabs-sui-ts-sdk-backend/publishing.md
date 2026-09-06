# Programmatic Package Publish and Upgrade

> Source: [sdk.mystenlabs.com/sui/transactions/reference](https://sdk.mystenlabs.com/sui/transactions/reference)

Publishing and upgrading Move packages from TypeScript without CLI.

---

## Prerequisites

Publishing requires compiled Move bytecode (the `modules` bytes and `dependencies` list). There are two ways to get these:

1. **Build locally with CLI, publish from SDK:** Run `sui move build` to produce bytecode in `build/`, then load the bytes in TypeScript and construct the Publish PTB.
2. **Use a build service or pre-compiled bytes:** If an agent cannot run CLI at all, it needs pre-compiled module bytes provided by another service or stored as artifacts.

The TypeScript SDK does not include a Move compiler. The `sui move build` step must happen somewhere — either locally, in CI, or via a build service.

---

## Publishing a package

### Step 1: Load compiled modules and dependencies

After `sui move build`, the compiled modules are in `build/<package_name>/bytecode_modules/`. Dependencies are package ID strings (e.g., `'0x1'`, `'0x2'`), not filesystem paths.

```typescript
import { readFileSync, readdirSync } from 'fs';
import { Transaction } from '@mysten/sui/transactions';

// Load compiled module bytes
const modulesDir = './build/my_package/bytecode_modules';
const modules = readdirSync(modulesDir)
  .filter(f => f.endsWith('.mv'))
  .map(f => Array.from(readFileSync(`${modulesDir}/${f}`)));

// Dependencies: array of package IDs this package depends on
// At minimum, include the Sui framework: '0x1' and '0x2'
const dependencies = ['0x1', '0x2'];
```

### Step 2: Construct and execute the Publish transaction

```typescript
const tx = new Transaction();

const [upgradeCap] = tx.publish({ modules, dependencies });

// Transfer the UpgradeCap to the publisher
tx.transferObjects([upgradeCap], keypair.toSuiAddress());

const result = await keypair.signAndExecuteTransaction({
  transaction: tx,
  client,
});
```

### Step 3: Extract the package ID from results

```typescript
if (result.$kind === 'FailedTransaction') {
  throw new Error(result.FailedTransaction.status.error?.message);
}

// The package ID is in the created objects
const createdObjects = result.Transaction.effects.created;
const publishedPackage = createdObjects?.find(
  obj => obj.owner?.$kind === 'Immutable'
);
const packageId = publishedPackage?.reference.objectId;
console.log('Published package:', packageId);
```

---

## Upgrading a package

### Step 1: Fetch the UpgradeCap

```typescript
const upgradeCapId = '0x...'; // The UpgradeCap object ID from the original publish

const upgradeCapObject = await client.getObject({
  id: upgradeCapId,
  options: { showContent: true },
});
```

### Step 2: Construct the Upgrade transaction

```typescript
const tx = new Transaction();

// Load new compiled modules
const newModules = readdirSync(newModulesDir)
  .filter(f => f.endsWith('.mv'))
  .map(f => Array.from(readFileSync(`${newModulesDir}/${f}`)));

const ticket = tx.moveCall({
  target: '0x2::package::authorize_upgrade',
  arguments: [
    tx.object(upgradeCapId),
    tx.pure.u8(0), // upgrade policy: 0 = Compatible
    tx.pure('vector<u8>', [/* digest bytes */]),
  ],
});

const receipt = tx.upgrade({
  modules: newModules,
  dependencies: ['0x1', '0x2'],
  package: originalPackageId,
  ticket,
});

tx.moveCall({
  target: '0x2::package::commit_upgrade',
  arguments: [tx.object(upgradeCapId), receipt],
});

const result = await keypair.signAndExecuteTransaction({
  transaction: tx,
  client,
});
```

### Upgrade policies

| Policy | Value | Effect |
|--------|-------|--------|
| Compatible | 0 | Can add functions, change implementations. Cannot remove public functions or change signatures. |
| Additive | 128 | Can only add new modules/functions. Cannot modify existing code. |
| Dependency-only | 192 | Can only change dependencies. |
| Immutable | — | Call `0x2::package::make_immutable` on UpgradeCap to prevent all future upgrades. |

---

## Dry-run before publishing

Use `simulateTransaction` to simulate a transaction without executing it:

```typescript
tx.setSender(keypair.toSuiAddress());
const dryRunResult = await client.simulateTransaction({
  transaction: tx,
  include: { effects: true },
});

if (dryRunResult.$kind === 'FailedTransaction') {
  console.error('Dry run failed:', dryRunResult.FailedTransaction.status.error?.message);
}
```

---

## Multi-network deployment pattern

For deploying the same package to multiple networks:

```typescript
const networks = ['devnet', 'testnet'] as const;

for (const network of networks) {
  const client = new SuiGrpcClient({ network });
  const tx = new Transaction();
  const [upgradeCap] = tx.publish({ modules, dependencies });
  tx.transferObjects([upgradeCap], keypair.toSuiAddress());

  const result = await keypair.signAndExecuteTransaction({
    transaction: tx,
    client,
  });

  await client.waitForTransaction({ result });
  console.log(`Published on ${network}:`, result.Transaction?.digest);
}
```
