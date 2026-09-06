# Building, Coins, and Execution

> Source: [sdk.mystenlabs.com/sui/transactions](https://sdk.mystenlabs.com/sui/transactions/basics)

---

## Coin access: `tx.coin()` and `tx.balance()`

These are the **recommended** way to access funds in a transaction. They automatically resolve from both address balances and coin objects, preferring address balances to avoid versioned object dependencies.

### `tx.coin()` — produces a `Coin<T>`

Use for transfers, Move functions that accept `Coin<T>`, and standard coin operations.

```typescript
import { Transaction } from '@mysten/sui/transactions';

const tx = new Transaction();

// SUI transfer — deposits into recipient's address balance
tx.moveCall({
  target: '0x2::balance::send_funds',
  typeArguments: ['0x2::sui::SUI'],
  arguments: [tx.balance({ balance: 1_000_000_000n }), tx.pure.address('0xRecipient')],
});

// Non-SUI transfer
tx.moveCall({
  target: '0x2::balance::send_funds',
  typeArguments: ['0x...::usdc::USDC'],
  arguments: [
    tx.balance({ balance: 1_000_000n, type: '0x...::usdc::USDC' }),
    tx.pure.address('0xRecipient'),
  ],
});

// Get a Coin<T> for Move call arguments
const coin = tx.coin({ balance: 1_000_000_000n });
tx.moveCall({ target: '0x...::module::use_coin', arguments: [coin] });

// Non-SUI coin for Move call arguments
const usdcCoin = tx.coin({
  balance: 1_000_000n,
  type: '0x...::usdc::USDC',
});
```

For transfers, prefer `balance::send_funds` over `transferObjects` — it deposits directly into the recipient's address balance, avoiding versioned coin objects on the receiving side.

### `tx.balance()` — produces a `Balance<T>`

Use for Move functions that accept `Balance<T>` directly. Specify `type` for non-SUI tokens — omitting it defaults to `Balance<SUI>`.

```typescript
const bal = tx.balance({
  balance: 500_000_000n,
  type: '0x...::usdc::USDC',
});
tx.moveCall({
  target: '0x...::my_module::deposit',
  arguments: [someObject, bal],
  typeArguments: ['0x...::usdc::USDC'],
});
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `balance` | `bigint \| number` | required | Amount in base units |
| `type` | `string` | `'0x2::sui::SUI'` | Coin type |
| `useGasCoin` | `boolean` | `true` | Whether to include the gas coin as a source. Set `false` in sponsored transactions where the gas coin belongs to the sponsor. |

### How resolution works at build time

1. If the address balance alone is sufficient, the SDK uses a direct withdrawal (no versioned object inputs needed).
2. Otherwise, it fetches coin objects and address balance in parallel, then merges and splits as needed.
3. A zero-balance request resolves to `balance::zero` with no network lookups.

### The gas coin (`tx.gas`) — low-level

Every transaction has a gas coin referenced via `tx.gas`. With address-balance gas (`setGasPayment([])`), the protocol materializes a synthetic GasCoin from the sender's or sponsor's address balance. `tx.gas` can be borrowed by reference and consumed by value only through permitted commands (`TransferObjects`, `coin::send_funds`).

In most cases, prefer `tx.coin()` / `tx.balance()` over `tx.splitCoins(tx.gas, ...)`. The higher-level methods handle balance resolution automatically and work correctly across all gas modes.

---

## Address balances vs coin objects

Sui has two ways of holding fungible tokens:

| | Coin Objects | Address Balances |
|--|-------------|-----------------|
| Structure | Individual on-chain objects with unique ID, version, and balance | Accumulator per address per coin type |
| Concurrency | Each coin is a versioned object — using it requires the exact version | No versions — concurrent transactions from the same address work |
| Management | Must manually split/merge | Deposits automatically merge |

An address's total balance = sum of coin object balances + address balance.

### Query balance

```typescript
const { balance } = await client.getBalance({ owner: address });
// balance contains: balance (total), coinBalance, addressBalance (as strings)
const total = BigInt(balance.balance);
```

### List individual coin objects

```typescript
const { objects } = await client.listCoins({
  owner: address,
});
```

---

## Manual coin operations

When you need explicit control over coin objects:

### Split coins

```typescript
const [coin1, coin2] = tx.splitCoins('0xMyCoinId', [1_000_000n, 2_000_000n]);
```

### Merge coins

```typescript
tx.mergeCoins('0xCoin1', ['0xCoin2', '0xCoin3']);
```

### Deposit into address balance

```typescript
tx.moveCall({
  target: '0x2::coin::send_funds',
  arguments: [tx.object('0xMyCoinObjectId'), tx.pure.address('0xRecipientAddress')],
  typeArguments: ['0x2::sui::SUI'],
});
```

### Withdraw from address balance

Use `tx.withdrawal()` to create a withdrawal input, then redeem via Move:

```typescript
const withdrawal = tx.withdrawal({ amount: 1_000_000_000n });
tx.moveCall({
  target: '0x2::coin::redeem_funds',
  arguments: [withdrawal],
  typeArguments: ['0x2::sui::SUI'],
});
```

---

## Signing and executing from a backend

### Direct sign and execute (simplest)

```typescript
import { Ed25519Keypair } from '@mysten/sui/keypairs/ed25519';
import { SuiGrpcClient } from '@mysten/sui/grpc';
import { Transaction } from '@mysten/sui/transactions';

const keypair = Ed25519Keypair.fromSecretKey('suiprivkey1...');
const client = new SuiGrpcClient({ network: 'testnet' });

const tx = new Transaction();
tx.moveCall({
  target: '0x2::balance::send_funds',
  typeArguments: ['0x2::sui::SUI'],
  arguments: [tx.balance({ balance: 1_000_000_000n }), tx.pure.address('0xRecipient')],
});

const result = await keypair.signAndExecuteTransaction({
  transaction: tx,
  client,
});
```

This automatically sets the sender to the keypair's address, builds the transaction, signs it, and executes it. Results include transaction data and effects by default.

### Separate sign then execute

Use when you need to inspect bytes before execution, or for multi-party signing:

```typescript
tx.setSender(keypair.toSuiAddress());
const bytes = await tx.build({ client });
const { signature } = await keypair.signTransaction(bytes);

// Execute later
const result = await client.executeTransaction({
  transaction: bytes,
  signatures: [signature],
});
```

---

## Result handling

Transaction results are discriminated unions. Always check the outcome:

```typescript
if (result.$kind === 'FailedTransaction') {
  // Executed on-chain but Move call aborted. Gas was still consumed.
  console.error('Failed:', result.FailedTransaction.status.error?.message);
} else {
  // Success
  console.log('Digest:', result.Transaction.digest);
}
```

Always check for `FailedTransaction` — a successful execution does not mean the Move call succeeded.

---

## Waiting for indexing

After a transaction executes, read APIs may not immediately reflect the effects. Always wait before dependent reads:

```typescript
await client.waitForTransaction({ result });

// Now safe to read updated state
const { balance } = await client.getBalance({ owner: address });
```

---

## Gasless stablecoin transfers

Qualified stablecoin transfers can execute with zero gas using `0x2::balance::send_funds`:

```typescript
const tx = new Transaction();
tx.moveCall({
  target: '0x2::balance::send_funds',
  arguments: [tx.balance({ balance: 1_000_000n, type: USDC_TYPE }), tx.pure.address(recipient)],
  typeArguments: [USDC_TYPE],
});

// gRPC/GraphQL transports automatically detect eligible transactions
// and set gas price/budget to 0
const result = await keypair.signAndExecuteTransaction({ transaction: tx, client });
```

The gRPC and GraphQL transports automatically detect and configure eligible gasless transactions. The sender does not need any SUI balance.
