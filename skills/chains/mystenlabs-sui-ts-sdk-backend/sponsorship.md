# Sponsored Transactions

> Source: [sdk.mystenlabs.com/sponsor](https://sdk.mystenlabs.com/sponsor/basic-usage)

Sponsored transactions let a backend pay gas on behalf of users. The `@mysten-incubation/sponsor` package provides the recommended flow.

---

## Install

```bash
npm install @mysten-incubation/sponsor @mysten/sui
```

---

## Recommended flow: client-builds, backend co-signs

The recommended pattern is that the **client builds the full transaction bytes** and the **backend validates, co-signs, and executes**.

### Why client-builds is preferred

The sponsor sees the exact bytes it is co-signing before committing. This prevents the sponsor from unknowingly signing malicious transactions.

> "Prefer services that expect already-built bytes plus the user's signature."

### Flow

```
1. Client fetches sponsor address from backend /config endpoint
2. Client builds transaction with sponsor as gas owner (empty gas payment)
3. User signs the transaction bytes
4. Client sends bytes + user signature to backend
5. Backend validates, co-signs, and executes
6. Backend returns result to client
```

---

## Address-balance sponsorship (simpler)

The sender can sign before the sponsor, enabling simpler async flows.

### Client side

```typescript
import { Transaction } from '@mysten/sui/transactions';

const tx = new Transaction();
tx.moveCall({ target: '0x...::module::function', arguments: [...] });

// Set empty gas payment to signal address-balance sponsorship
tx.setGasPayment([]);
tx.setSender(userAddress);
tx.setGasOwner(sponsorAddress); // from /config endpoint

const bytes = await tx.build({ client });
const { signature: userSignature } = await userKeypair.signTransaction(bytes);

// Send bytes + userSignature to backend
```

### Backend side

```typescript
import { Ed25519Keypair } from '@mysten/sui/keypairs/ed25519';
import { createSponsor, defaults, gasBudget } from '@mysten-incubation/sponsor';

const sponsorKeypair = Ed25519Keypair.fromSecretKey(process.env.SPONSOR_KEY!);

const sponsor = createSponsor({
  signer: sponsorKeypair,
  client,
  validate: [
    defaults(),
    gasBudget({ max: 50_000_000n }),
    allowedFunctions(['0xYourPkg::module::allowed_fn']),
    // Add application-specific validators as needed
  ],
});

// Validate, co-sign, and execute in one call
const result = await sponsor.signAndExecuteTransaction({
  transaction: bytes,
  userSignature,
});
```

---

## Sponsor security: validation is not optional

`defaults()` and `gasBudget()` alone still permit arbitrary Move calls — an attacker could drain sponsor funds through gas. **Always layer application-specific validators:**

- **Authentication:** Verify the user's identity before co-signing (JWT, session token, API key).
- **Rate limits / quotas:** Cap transactions per user per time window.
- **Function allowlists:** Use `allowedFunctions([...])` to restrict which Move functions the sponsor will co-sign. Only allow your application's entry points.
- **Recipient allowlists:** Restrict `TransferObjects` targets to known addresses.
- **Amount caps:** Limit the value that can be transferred per transaction.

```typescript
import { createSponsor, defaults, gasBudget, allowedFunctions } from '@mysten-incubation/sponsor';

const sponsor = createSponsor({
  signer: sponsorKeypair,
  client,
  validate: [
    defaults(),
    gasBudget({ max: 50_000_000n }),
    allowedFunctions([
      '0xYourPkg::game::play',
      '0xYourPkg::game::claim_reward',
    ]),
    // Custom validator for authentication + rate limiting
    async (tx) => {
      // Verify user identity and enforce quotas here
      // Return { ok: false, issues: [...] } to reject
    },
  ],
});
```

Without application-specific validation, your sponsor is an open gas faucet.

---

## Coin-based sponsorship

When address balances are not used, the sponsor provides specific coin objects for gas:

### Flow

```
1. User builds transaction kind bytes (no gas info)
2. Sponsor wraps with gas coin objects and gas owner address
3. Both parties sign the full transaction bytes
4. Either party executes with both signatures
```

```typescript
// User side: build kind-only
const tx = new Transaction();
tx.moveCall({ target: '0x...::module::function', arguments: [...] });

const kindBytes = await tx.build({ client, onlyTransactionKind: true });

// Send kindBytes to sponsor
```

```typescript
// Sponsor side: wrap with gas info
const sponsoredTx = Transaction.fromKind(kindBytes);
sponsoredTx.setSender(userAddress);
sponsoredTx.setGasOwner(sponsorKeypair.toSuiAddress());
sponsoredTx.setGasPayment([gasCoinsFromSponsor]);
sponsoredTx.setGasBudget(50_000_000n);
sponsoredTx.setGasPrice(1000n);

const fullBytes = await sponsoredTx.build({ client });
const { signature: sponsorSig } = await sponsorKeypair.signTransaction(fullBytes);

// Return fullBytes + sponsorSig to user for their signature
```

---

## Gas coin ownership in sponsored transactions

When `setGasPayment([])` is used, the protocol materializes a synthetic GasCoin from the **gas owner's** (sponsor's) address balance. `tx.gas` references this synthetic coin — it belongs to the sponsor, not the sender.

### When the sender needs to transfer their own tokens

Use `balance::send_funds` with `useGasCoin: false` to source from the sender's balance and deposit into the recipient's address balance:

```typescript
tx.moveCall({
  target: '0x2::balance::send_funds',
  typeArguments: ['0x2::sui::SUI'],
  arguments: [
    tx.balance({ balance: 1_000_000_000n, useGasCoin: false }),
    tx.pure.address(recipient),
  ],
});
```

### When the sponsor is paying for everything

If the sponsor is both paying gas and funding the transfer (e.g., an airdrop), `tx.splitCoins(tx.gas, ...)` works at the protocol level because `tx.gas` belongs to the sponsor. However, the `defaults()` validator includes `gasCoinNotUsed()`, which **rejects** transactions that consume the gas coin. To allow this pattern, use a custom policy without `gasCoinNotUsed()`:

```typescript
import { createSponsor, gasBudget, allowedFunctions } from '@mysten-incubation/sponsor';

// Custom policy that permits gas coin usage (for sponsor-funded airdrops)
const sponsor = createSponsor({
  signer: sponsorKeypair,
  client,
  validate: [
    gasBudget({ max: 50_000_000n }),
    allowedFunctions(['0xYourPkg::airdrop::claim']),
    // Omit defaults() — it includes gasCoinNotUsed() which would reject this
  ],
});
```

```typescript
// Transaction that sends from sponsor's gas coin via balance transfer
tx.moveCall({
  target: '0x2::balance::send_funds',
  typeArguments: ['0x2::sui::SUI'],
  arguments: [tx.balance({ balance: 1_000_000_000n }), tx.pure.address(recipient)],
});
```

### Rule of thumb

- `tx.balance()` / `tx.coin()` (default `useGasCoin: true`) — sources from the gas owner's (sponsor's) funds. Rejected by `defaults()` unless you build a custom policy that omits `gasCoinNotUsed()`.
- `tx.balance({ useGasCoin: false })` / `tx.coin({ useGasCoin: false })` — sources from the sender's funds. Works with `defaults()`.
- For transfers, prefer `balance::send_funds` over `transferObjects` — it deposits into the recipient's address balance.

---

## Config endpoint pattern

Backends should expose a `/config` endpoint returning the current sponsor address. This allows dynamic sponsor address rotation without client redeployment:

```typescript
// Backend
app.get('/config', (req, res) => {
  res.json({ sponsorAddress: sponsorKeypair.toSuiAddress() });
});
```

---

## Result handling

Backend receives one of three outcomes:

| Result | Meaning | Action |
|--------|---------|--------|
| `Rejected` | Policy validation failed; transaction was never executed or signed | Return error to user |
| `FailedTransaction` | Executed on-chain but Move call aborted; sponsor still pays gas | Log failure, return error |
| `Transaction` | Successful execution | Return digest to user |

Always check using `$kind`:

```typescript
switch (result.$kind) {
  case 'Rejected':
    // Never executed on-chain
    throw new Error(result.issues.map((i) => i.message).join('; '));
  case 'FailedTransaction':
    // Executed but aborted — sponsor still paid gas
    throw new Error(`Aborted: ${result.FailedTransaction.digest}`);
  case 'Transaction':
    // Success
    console.log('Digest:', result.Transaction.digest);
}
```
