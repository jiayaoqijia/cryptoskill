# Signing and executing transactions in dApps

Source: https://sdk.mystenlabs.com/dapp-kit/getting-started/react

## Full pattern

```tsx
import { useDAppKit, useCurrentClient, useCurrentAccount } from '@mysten/dapp-kit-react';
import { useQueryClient } from '@tanstack/react-query';
import { Transaction } from '@mysten/sui/transactions';
import { useState } from 'react';

function ActionButton() {
  const dAppKit = useDAppKit();
  const client = useCurrentClient();
  const account = useCurrentAccount();
  const queryClient = useQueryClient();

  const [isPending, setIsPending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handle() {
    if (!account) return;
    setIsPending(true);
    setError(null);

    try {
      // Build the PTB — see sui-sdks / ptbs skills for patterns
      // Note: for simple transfers, tx.coin() is now the preferred approach:
      //   tx.transferObjects([tx.coin({ balance: 1_000_000n })], tx.pure.address('0xrecipient'));
      // The splitCoins + transferObjects pattern below still works:
      const tx = new Transaction();
      const [coin] = tx.splitCoins(tx.gas, [tx.pure.u64(1_000_000n)]);
      tx.transferObjects([coin], tx.pure.address('0xrecipient'));

      // Hand the Transaction to the wallet — DO NOT call tx.build() first
      const result = await dAppKit.signAndExecuteTransaction({ transaction: tx });

      // Check failure
      if (result.$kind === 'FailedTransaction') {
        throw new Error(result.FailedTransaction.status.error?.message ?? 'Transaction failed');
      }

      // Wait for indexing, then invalidate caches
      // Note: useCurrentClient() returns ClientWithCoreApi — use client.core for methods
      const digest = result.Transaction.digest;
      await client.core.waitForTransaction({ digest });
      await queryClient.invalidateQueries({ queryKey: ['balance', account.address] });
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Unknown error');
    } finally {
      setIsPending(false);
    }
  }

  return (
    <>
      <button onClick={handle} disabled={!account || isPending}>
        {isPending ? 'Waiting for wallet…' : 'Submit'}
      </button>
      {error && <p style={{ color: 'red' }}>{error}</p>}
    </>
  );
}
```

## Result shape

`signAndExecuteTransaction` returns a discriminated union keyed on `$kind`:

```ts
type Result =
  | { $kind: 'Transaction'; Transaction: { digest: string; /* ... */ } }
  | { $kind: 'FailedTransaction'; FailedTransaction: { status: { error?: { message: string } } } };
```

Access patterns:

```ts
if (result.$kind === 'FailedTransaction') {
  // result.FailedTransaction is populated
  console.error(result.FailedTransaction.status.error?.message);
  return;
}
// result.Transaction is populated
const digest = result.Transaction.digest;
```

Do **not** use v1's `result.effects?.status?.status === 'success'` — that shape is gone.

## Using package IDs in transactions

Import `PACKAGE_IDS` and `ORIGINAL_PACKAGE_IDS` from your setup file (see `setup.md`) and use them with the current network:

```tsx
import { useCurrentNetwork } from '@mysten/dapp-kit-react';
import { PACKAGE_IDS, ORIGINAL_PACKAGE_IDS } from './dapp-kit';

function MintButton() {
  const dAppKit = useDAppKit();
  const network = useCurrentNetwork();

  async function handleMint() {
    const packageId = PACKAGE_IDS[network];
    const tx = new Transaction();
    tx.moveCall({
      target: `${packageId}::nft::mint`,
      arguments: [tx.pure.string('My NFT')],
    });
    await dAppKit.signAndExecuteTransaction({ transaction: tx });
  }
  // ...
}
```

For type-filtered queries after a package upgrade, use `ORIGINAL_PACKAGE_IDS`:

```ts
const originalId = ORIGINAL_PACKAGE_IDS[network];
const objects = await client.core.listOwnedObjects({
  owner: account.address,
  type: `${originalId}::nft::NFT`,
});
```

See `sui-publish` skill → "Type anchoring after upgrades" for why the original ID is needed for type queries.

## Handing PTBs to the wallet

**Pass the `Transaction` instance directly.** dApp Kit serializes it and forwards to the wallet, which selects gas coins and sets budget via dry-run.

```tsx
// ✅
await dAppKit.signAndExecuteTransaction({ transaction: tx });

// ❌ Do NOT build bytes in app code — wallet can't do gas selection
const bytes = await tx.build({ client });
await dAppKit.signAndExecuteTransaction({ transaction: bytes });
```

The one exception is sponsored transactions — see below.

## Signing without executing (sponsored flow)

When your backend pays for gas, the wallet signs but the app submits via your sponsor service:

```tsx
async function handleSponsored() {
  const tx = new Transaction();
  // ... build PTB ...

  // Wallet signs but does not execute
  const { bytes, signature } = await dAppKit.signTransaction({ transaction: tx });

  // Hand off to your sponsor backend
  const res = await fetch('/api/sponsor', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ bytes, signature }),
  });
  const { digest } = await res.json();

  await client.waitForTransaction({ digest });
}
```

For the backend side of the sponsored flow (setting gas owner, attaching sponsor signature, executing with both signatures), see the `ptbs` skill — the sponsor pattern with `tx.build({ onlyTransactionKind: true })` and `Transaction.fromKind`.

## Signing without a wallet (testnet / development)

For scripts, tests, or local development where no browser wallet is available, sign directly with an `Ed25519Keypair`:

```ts
import { Ed25519Keypair } from '@mysten/sui/keypairs/ed25519';
import { SuiGrpcClient } from '@mysten/sui/grpc';
import { Transaction } from '@mysten/sui/transactions';

// From a private key or generate a new one
const keypair = Ed25519Keypair.fromSecretKey(privateKeyBytes);
// or: const keypair = new Ed25519Keypair();

const client = new SuiGrpcClient({ baseUrl: 'https://fullnode.testnet.sui.io:443', network: 'testnet' });

const tx = new Transaction();
// ... build PTB ...

const result = await keypair.signAndExecuteTransaction({
  transaction: tx,
  client,
});
```

**Never embed private keys in production frontend apps.** This pattern is for testnet automation, integration tests, and backend services only.

## Personal message signing

Use for wallet-based authentication (Sign-In-with-Sui / off-chain login):

```tsx
import { useDAppKit, useCurrentAccount } from '@mysten/dapp-kit-react';

async function handleAuth() {
  const dAppKit = useDAppKit();
  const account = useCurrentAccount();
  if (!account) return;

  // Fetch a single-use nonce from your backend
  const { nonce } = await fetch('/api/auth/nonce').then((r) => r.json());
  const message = new TextEncoder().encode(`Sign in to MyApp: nonce=${nonce}`);

  const { bytes, signature } = await dAppKit.signPersonalMessage({ message });

  // Verify server-side, invalidate the nonce
  await fetch('/api/auth/verify', {
    method: 'POST',
    body: JSON.stringify({ address: account.address, bytes, signature }),
  });
}
```

- **Message must be `Uint8Array`** — use `TextEncoder` on strings.
- **Display the message clearly** — users see it in the wallet.
- **Use a server-issued, single-use nonce** — client-side nonces are replayable.

## The `waitForTransaction` + invalidate sequence

This is the single most commonly missed pattern:

```
tx signed → wallet returns digest → fullnode finalizes (fast)
                                          ↓
                                  fullnode indexes (async, a few hundred ms)
                                          ↓
                              waitForTransaction resolves
                                          ↓
                           NOW safe to invalidate / refetch
```

```ts
// ❌ Refetch fires before indexer has caught up — stale data
await dAppKit.signAndExecuteTransaction(...);
await queryClient.invalidateQueries(...);  // BAD

// ✅ Wait first (use client.core — that's what useCurrentClient returns)
const result = await dAppKit.signAndExecuteTransaction(...);
if (result.$kind === 'FailedTransaction') throw new Error(...);
await client.core.waitForTransaction({ digest: result.Transaction.digest });
await queryClient.invalidateQueries(...);  // GOOD
```

## Error handling — common wallet failures

| Symptom | Cause | Fix |
|---|---|---|
| User rejects in wallet | normal | Catch and show a "cancelled" state — not an error |
| "Insufficient gas" | wallet has too little SUI for gas budget | UX: surface the address and amount, suggest faucet (testnet) or exchange (mainnet) |
| `InsufficientCoinBalance` (command 0) | `splitCoins` from gas requests more than the gas coin can cover after reserving for gas budget — the gas coin must cover payment + gas | Reduce price, merge coins first, or tell the user how much SUI they need (price + ~0.01 SUI for gas) |
| "Nothing to execute" | PTB has no effective commands | Check you actually added commands to `tx` before signing |
| Tx executes but fails Move assertion | Move code aborted | Catch `result.FailedTransaction`, surface the error message verbatim |
| Tx succeeds but UI doesn't update | missing `waitForTransaction` / `invalidateQueries` | Add both, in that order |
| "Wallet not available" in dev | SSR rendered before hydration | `'use client'` in Next.js; guard render until wallet detected |

## Don't fetch gas info before sending

Leave gas budget / price / payment to the wallet. If you hardcode `setGasBudget` or `setGasPayment` in the app, the wallet can't adjust for fluctuating gas prices or replace gas coins. The one exception is sponsored flows, where a sponsor service fills gas data before the wallet signs.

## Multi-moveCall chaining

When a PTB calls multiple Move functions, use the destructured return value from one `moveCall` as an argument to the next:

```ts
const tx = new Transaction();

// First call returns a value — destructure it
const [payload] = tx.moveCall({
  target: `${pkg}::payloads::new_audit_report`,
  arguments: [tx.pure.string(url), tx.pure.string(auditor)],
});

// Second call consumes it
tx.moveCall({
  target: `${pkg}::registry::attest`,
  typeArguments: [`${pkg}::payloads::AuditReport`],
  arguments: [tx.object(registryId), payload],
});
```

The `const [payload] = tx.moveCall(...)` destructuring extracts the first return value as a `TransactionResult` that can be passed directly to subsequent commands. For functions with multiple return values, destructure more: `const [a, b] = tx.moveCall(...)`.

## Compound types in `tx.pure`

Typed helpers like `tx.pure.u64()`, `tx.pure.string()`, and `tx.pure.address()` only cover scalar types. For vectors and other compound types, use the generic `tx.pure(type, value)` overload:

```ts
// Vector of strings
tx.pure("vector<string>", ["a", "b", "c"]);

// Vector of bytes (e.g., for BCS-encoded data)
tx.pure("vector<u8>", [1, 2, 3]);

// Vector of addresses
tx.pure("vector<address>", ["0xabc...", "0xdef..."]);
```

## PTB construction

See the `ptbs` skill for command-by-command semantics and the `sui-sdks` skill (`typescript.md`) for the `Transaction` class API. This skill covers the *dApp-side* of the flow; building the PTB itself is the same in dApp, backend, or CLI code.
