# Client Initialization and BalanceManager Lifecycle

## Installation

```bash
npm install @mysten/deepbook-v3 @mysten/sui
```

## Client construction

The `deepbook` function extends a `SuiGrpcClient` via `$extend` to add DeepBook transaction builders under a `deepbook` namespace:

```typescript
import { SuiGrpcClient } from "@mysten/sui/grpc";
import { deepbook } from "@mysten/deepbook-v3";
import { Ed25519Keypair } from "@mysten/sui/keypairs/ed25519";

const suiClient = new SuiGrpcClient({ network: "testnet" });
const keypair = new Ed25519Keypair(); // or load from existing key

const client = suiClient.$extend(
  deepbook({
    address: keypair.toSuiAddress(),
    balanceManagers: {
      MANAGER_1: {
        address: "0x...", // existing BalanceManager object ID
        tradeCap: undefined,
      },
    },
  })
);
```

The client references pools and coins by SDK keys (e.g., `"DEEP_SUI"`, `"SUI"`) rather than raw on-chain addresses. Default coin and pool maps are included for testnet and mainnet. Custom `PoolMap` and `CoinMap` can override defaults.

### Three-tier setup pattern

The sandbox examples demonstrate three setup levels with increasing complexity:

1. **Read-only client** — No keypair, no BalanceManager. Sufficient for querying order book depth, prices, and pool state.

2. **Basic setup** — Fresh keypair + faucet funding. Sufficient for swaps (which operate directly on wallet coins without a BalanceManager).

3. **Full setup** — Keypair + BalanceManager creation + fund deposits. Required for placing limit and market orders.

### Localnet/sandbox configuration

For localnet (sandbox), the client loads pool/coin configuration from a deployment manifest:

```typescript
import manifest from "../../sandbox/deployments/localnet.json";

const suiClient = new SuiGrpcClient({ network: "custom", baseUrl: "http://localhost:9000" });

const client = suiClient.$extend(
  deepbook({
    address: keypair.toSuiAddress(),
    pools: manifest.pools,
    coins: manifest.coins,
    packageIds: {
      deepbook: manifest.packages.deepbook,
    },
  })
);
```

## BalanceManager lifecycle

### Creating a BalanceManager

A BalanceManager is a shared on-chain object. Create it in a transaction, then extract the object ID from the transaction result:

```typescript
import { Transaction } from "@mysten/sui/transactions";

const tx = new Transaction();
client.deepbook.balanceManager.createAndShareBalanceManager()(tx);

const result = await suiClient.signAndExecuteTransaction({
  transaction: tx,
  signer: keypair,
});

// Extract the BalanceManager ID from changed objects in effects
const managerObj = result.Transaction?.effects?.changedObjects?.find(
  ([_id, change]) => change.objectType?.includes("BalanceManager")
);
const managerId = managerObj?.[0];
```

After creation, reinitialize the client with the BalanceManager address:

```typescript
const client = suiClient.$extend(
  deepbook({
    address: keypair.toSuiAddress(),
    balanceManagers: {
      MANAGER_1: { address: managerId, tradeCap: undefined },
    },
  })
);
```

### Reusing a BalanceManager

Persist the BalanceManager ID (e.g., in a config file or database) and pass it to the client on subsequent runs. Do not create a new BalanceManager per session — this wastes gas and creates orphaned shared objects.

Discover existing BalanceManagers via the DeepBook indexer or by persisting the ID at creation time.

## Deposits and withdrawals

### Depositing funds

```typescript
const tx = new Transaction();
client.deepbook.balanceManager.depositIntoManager("MANAGER_1", "SUI", 10)(tx);
await signAndExecute(tx);
```

The SDK automatically scales amounts to coin decimals. Size deposits to your wallet balance — the SDK validates at build time and throws `Insufficient balance` if the wallet cannot cover the deposit.

### Withdrawing funds

```typescript
const tx = new Transaction();
client.deepbook.balanceManager.withdrawAllFromManager("MANAGER_1", "SUI", recipientAddress)(tx);
await signAndExecute(tx);
```

Withdrawals move settled balances back to the wallet. Funds locked in resting orders cannot be withdrawn until those orders are canceled.

### Checking balances

```typescript
const balance = await client.deepbook.balanceManager.checkManagerBalance("MANAGER_1", "SUI");
```

## SDK API overview

### Read-only operations (no BalanceManager required)

- `client.deepbook.balanceManager.checkManagerBalance(managerKey, coinKey)` — query BalanceManager balances
- `client.deepbook.getLevel2TicksFromMid(poolKey, depth)` — retrieve order book data around the mid price (returns `{ bid_prices, bid_quantities, ask_prices, ask_quantities }`)

### BalanceManager operations

- `client.deepbook.balanceManager.depositIntoManager(managerKey, coinKey, amount)` — deposit funds
- `client.deepbook.balanceManager.withdrawAllFromManager(managerKey, coinKey, recipient)` — withdraw all settled funds
- `client.deepbook.balanceManager.createAndShareBalanceManager()` — create a new BalanceManager

### Trading operations

See the `trading.md` reference file for order placement, swaps, and order management.

### Referral operations

- `mintReferral(poolKey, multiplier)` — create a referral (multiplier: 0.1–2.0, multiples of 0.1)
- `updatePoolReferralMultiplier(poolKey, id, multiplier)` — adjust fee allocation
- `claimPoolReferralRewards(poolKey, id)` — collect accumulated rewards
- `setBalanceManagerReferral(managerKey, referralId, tradeCap)` — link referral to manager
- `unsetBalanceManagerReferral(managerKey, poolKey, tradeCap)` — unlink referral
