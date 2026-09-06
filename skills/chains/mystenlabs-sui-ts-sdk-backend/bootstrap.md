# Keypair, Faucet, and Client Setup

> Source: [sdk.mystenlabs.com](https://sdk.mystenlabs.com/sui/cryptography/keypairs)

This file covers the complete bootstrap sequence for an agent or backend service: create a keypair, fund it, and connect to Sui — all without CLI.

---

## Install

```bash
npm install @mysten/sui
```

---

## Step 1: Create a keypair

### Supported key types

| Scheme | Class | Import |
|--------|-------|--------|
| Ed25519 | `Ed25519Keypair` | `@mysten/sui/keypairs/ed25519` |
| ECDSA Secp256k1 | `Secp256k1Keypair` | `@mysten/sui/keypairs/secp256k1` |
| ECDSA Secp256r1 | `Secp256r1Keypair` | `@mysten/sui/keypairs/secp256r1` |

Ed25519 is the default and most common choice.

### Generate a random keypair

```typescript
import { Ed25519Keypair } from '@mysten/sui/keypairs/ed25519';

const keypair = new Ed25519Keypair();
const address = keypair.toSuiAddress();
console.log('Address:', address);
```

### Derive from a mnemonic

```typescript
const keypair = Ed25519Keypair.deriveKeypair(
  'result crisp session latin must fruit genuine question ...'
);
```

### Import from a Bech32 secret key

Sui private keys use the `suiprivkey` Bech32 prefix. This is the standard format for storing and exchanging keys.

```typescript
const keypair = Ed25519Keypair.fromSecretKey(
  'suiprivkey1qzse89atw7d3zum8ujep76d2cxmgduyuast0y9fu23xcl0mpafgkktllhyc'
);
```

### Import from raw hex bytes

```typescript
import { fromHex } from '@mysten/sui/utils';

const keypair = Ed25519Keypair.fromSecretKey(fromHex('0xabcdef...'));
```

### Export a keypair

```typescript
const secretKey = keypair.getSecretKey(); // Returns Bech32 'suiprivkey...' string
```

### Detect key scheme from encoded key

When loading a key from storage and you don't know the scheme:

```typescript
import { decodeSuiPrivateKey } from '@mysten/sui/cryptography';

const { scheme, secretKey } = decodeSuiPrivateKey(encodedKey);
// scheme is 'ED25519', 'Secp256k1', or 'Secp256r1'
// Use the appropriate Keypair class based on scheme
```

### Get public key and address

```typescript
const publicKey = keypair.getPublicKey();
const address = keypair.toSuiAddress();
```

---

## Step 2: Fund the address (testnet/devnet)

### Programmatic faucet request

```typescript
import { requestSuiFromFaucetV2, getFaucetHost } from '@mysten/sui/faucet';

await requestSuiFromFaucetV2({
  host: getFaucetHost('testnet'),
  recipient: keypair.toSuiAddress(),
});
```

Available networks for `getFaucetHost`: `'testnet'`, `'devnet'`, `'localnet'`.

There is no faucet for Mainnet. For Mainnet, acquire SUI through an exchange or transfer from another address.

### Local faucet (when running localnet)

```typescript
await requestSuiFromFaucetV2({
  host: getFaucetHost('localnet'), // http://127.0.0.1:9123/v2/gas
  recipient: keypair.toSuiAddress(),
});
```

---

## Step 3: Connect to a network

### SuiGrpcClient (default — use this)

```typescript
import { SuiGrpcClient } from '@mysten/sui/grpc';

// Testnet
const client = new SuiGrpcClient({ network: 'testnet' });

// Mainnet
const client = new SuiGrpcClient({ network: 'mainnet' });

// Devnet
const client = new SuiGrpcClient({ network: 'devnet' });

// Localnet
const client = new SuiGrpcClient({ network: 'localnet' });

// Custom endpoint
const client = new SuiGrpcClient({
  network: 'mainnet',
  baseUrl: 'https://your-custom-fullnode.example.com:443',
});
```

`SuiGrpcClient` reads from a full node and is the only client with real-time streaming subscriptions.

### SuiGraphQLClient (for flexible queries)

```typescript
import { SuiGraphQLClient } from '@mysten/sui/graphql';

const client = new SuiGraphQLClient({
  network: 'mainnet',
  url: 'https://graphql.mainnet.sui.io/graphql',
});
```

`SuiGraphQLClient` reads from the indexer. Use it when you need relational queries or multi-entity joins.

### Both clients share the same API

Top-level methods and `client.core.*` methods work identically on both clients. Switching between them is mostly a constructor change.

### Client extensions

Extend a client with first-party SDK modules:

```typescript
import { deepbook } from '@mysten/deepbook-v3';
import { walrus } from '@mysten/walrus';
import { seal } from '@mysten/seal';

const client = new SuiGrpcClient({ network: 'mainnet' })
  .$extend(deepbook({ address: '0x...' }))
  .$extend(walrus())
  .$extend(seal());
```

---

## Complete bootstrap example

End-to-end: create a keypair, fund it on testnet, connect, and verify the balance.

```typescript
import { Ed25519Keypair } from '@mysten/sui/keypairs/ed25519';
import { SuiGrpcClient } from '@mysten/sui/grpc';
import { requestSuiFromFaucetV2, getFaucetHost } from '@mysten/sui/faucet';

// 1. Create keypair
const keypair = new Ed25519Keypair();
const address = keypair.toSuiAddress();
console.log('Address:', address);

// 2. Fund from faucet
await requestSuiFromFaucetV2({
  host: getFaucetHost('testnet'),
  recipient: address,
});

// 3. Connect
const client = new SuiGrpcClient({ network: 'testnet' });

// 4. Verify balance
const { balance } = await client.getBalance({ owner: address });
console.log('Balance:', balance);
```

---

## Loading a keypair from environment (production pattern)

For production services, load keys from environment variables or a secrets manager:

```typescript
import { Ed25519Keypair } from '@mysten/sui/keypairs/ed25519';

const keypair = Ed25519Keypair.fromSecretKey(process.env.SUI_PRIVATE_KEY!);
```

For higher security, use AWS KMS or GCP KMS signers instead of raw keys. See the `signing.md` reference file.
