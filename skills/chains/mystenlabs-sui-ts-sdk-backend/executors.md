# Running Transactions at Scale

> Source: [sdk.mystenlabs.com/sui/executors](https://sdk.mystenlabs.com/sui/executors)

The SDK provides two executor classes for efficiently managing multiple transactions from a single address without manual gas management.

---

## SerialTransactionExecutor

For sequential execution from a single address (wallets, backend services with ordered operations).

### How it works

1. Selects all of the sender's SUI coins for the first transaction, which merges them into a single coin.
2. That single coin is reused as gas payment for all subsequent transactions.
3. Maintains an internal object version cache to speed execution when reusing objects.
4. Queues transactions internally — no need to await previous transactions before submitting the next.

### Setup

```typescript
import { SerialTransactionExecutor } from '@mysten/sui/transactions';
import { SuiGrpcClient } from '@mysten/sui/grpc';
import { Ed25519Keypair } from '@mysten/sui/keypairs/ed25519';

const client = new SuiGrpcClient({ network: 'testnet' });
const keypair = Ed25519Keypair.fromSecretKey('suiprivkey1...');

const executor = new SerialTransactionExecutor({
  client,
  signer: keypair,
  defaultGasBudget: 50_000_000n, // default
});
```

### Execute transactions

```typescript
import { Transaction } from '@mysten/sui/transactions';

const tx = new Transaction();
tx.moveCall({ target: '0x...::module::function', arguments: [...] });

const result = await executor.executeTransaction(tx);
```

Queue multiple transactions without awaiting each one:

```typescript
const results = await Promise.all([
  executor.executeTransaction(tx1),
  executor.executeTransaction(tx2),
  executor.executeTransaction(tx3),
]);
```

The executor queues them internally and executes them in order.

### Configuration

| Option | Default | Description |
|--------|---------|-------------|
| `client` | required | `SuiGrpcClient` or `SuiGraphQLClient` |
| `signer` | required | Keypair or any Signer |
| `defaultGasBudget` | `50_000_000n` | Gas budget per transaction |

---

## ParallelTransactionExecutor (experimental)

For concurrent execution from a single address (high-throughput pipelines, batch operations).

### How it works

1. Automatically maintains and refills a pool of gas coins.
2. Detects which objects each transaction uses and schedules transactions to avoid conflicts between transactions using the same object IDs.
3. Transactions that touch different objects execute in parallel.

### Setup

```typescript
import { ParallelTransactionExecutor } from '@mysten/sui/transactions';

const executor = new ParallelTransactionExecutor({
  client,
  signer: keypair,
  coinBatchSize: 20,        // Gas coins to create per batch
  initialCoinBalance: 200_000_000n,  // Starting balance per gas coin
  minimumCoinBalance: 50_000_000n,   // Refill threshold
  maxPoolSize: 50,           // Maximum gas coins in pool
});
```

### Execute transactions

```typescript
const result = await executor.executeTransaction(tx);
```

The executor handles gas coin selection, conflict detection, and scheduling automatically.

### Configuration

| Option | Default | Description |
|--------|---------|-------------|
| `client` | required | `SuiGrpcClient` or `SuiGraphQLClient` |
| `signer` | required | Keypair or any Signer |
| `coinBatchSize` | `20` | Number of gas coins created per batch |
| `initialCoinBalance` | `200_000_000n` | Balance for each new gas coin |
| `minimumCoinBalance` | `50_000_000n` | When a coin drops below this, it's refilled |
| `maxPoolSize` | `50` | Maximum number of gas coins maintained |
| `gasMode` | `'coins'` | `'coins'` or `'addressBalance'`. Use `'addressBalance'` to pay gas from the address balance instead of coin objects — pairs well with address-balance sponsorship. |

### Limitations

- **Single executor per address.** Do not run multiple `ParallelTransactionExecutor` instances on the same address — they will conflict over gas coins.
- **No external transactions.** While the executor is active, do not execute transactions from the same address outside the executor.
- **Experimental.** The API may change in future releases.

---

## Best practices for both executors

### Use unresolved object IDs

Pass object IDs as strings rather than fully-specified `{ objectId, version, digest }` refs. This lets the executor use its internal object cache for the latest version and digest:

```typescript
// Good — executor resolves the latest version
tx.object('0xABC...');

// Avoid — pins to a specific version that may be stale
tx.objectRef({ objectId: '0xABC...', version: '5', digest: '...' });
```

### Choose the right executor

| Scenario | Executor |
|----------|----------|
| Wallet or single-user backend | `SerialTransactionExecutor` |
| Batch processing (airdrops, migrations) | `ParallelTransactionExecutor` |
| Multiple concurrent users from one hot wallet | `ParallelTransactionExecutor` |
| Transactions that must execute in strict order | `SerialTransactionExecutor` |
