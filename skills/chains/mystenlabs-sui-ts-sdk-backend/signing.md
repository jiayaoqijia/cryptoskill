# Cloud KMS and Multisig

> Source: [sdk.mystenlabs.com/sui/cryptography/signers](https://sdk.mystenlabs.com/sui/cryptography/signers)

Production backends should use cloud KMS signers instead of storing raw private keys. For shared custody, use multisig.

---

## The Signer interface

All signers — keypairs, KMS, multisig — implement the same `Signer` interface:

```typescript
signer.getPublicKey()           // Returns PublicKey
signer.toSuiAddress()           // Returns Sui address string
signer.signPersonalMessage(msg) // Returns { signature }
signer.signTransaction(bytes)   // Returns { signature }
signer.signAndExecuteTransaction({ transaction, client }) // Build, sign, execute
```

Because every signer extends the same base class, they are interchangeable. Code that works with a keypair works identically with a KMS signer or multisig signer.

---

## AWS KMS Signer

### Install

```bash
npm install @mysten/aws-kms-signer
```

### Supported key types

- Ed25519
- Secp256k1 (`ECC_SECG_P256K1`)
- Secp256r1 (`ECC_NIST_P256`)

### Setup

```typescript
import { AwsKmsSigner } from '@mysten/aws-kms-signer';

const signer = await AwsKmsSigner.fromKeyId(AWS_KMS_KEY_ID, {
  region: AWS_REGION,
  accessKeyId: AWS_ACCESS_KEY_ID,
  secretAccessKey: AWS_SECRET_ACCESS_KEY,
});

const address = signer.getPublicKey().toSuiAddress();
```

### Sign and execute

```typescript
const result = await client.signAndExecuteTransaction({
  transaction: tx,
  signer,
});
```

The signer is passed to the client method. All signers work interchangeably with this pattern.

---

## GCP KMS Signer

### Install

```bash
npm install @mysten/gcp-kms-signer
```

### Supported key types

- Secp256k1 (`EC_SIGN_SECP256K1_SHA256`)
- Secp256r1 (`EC_SIGN_P256_SHA256`)

### Setup

```typescript
import { GcpKmsSigner } from '@mysten/gcp-kms-signer';

const signer = await GcpKmsSigner.fromOptions({
  projectId: 'your-google-project-id',
  location: 'your-google-location',
  keyRing: 'your-google-keyring',
  cryptoKey: 'your-google-key-name',
  cryptoKeyVersion: 'your-google-key-version',
});

const address = signer.getPublicKey().toSuiAddress();
```

### Sign and execute

```typescript
const result = await client.signAndExecuteTransaction({
  transaction: tx,
  signer,
});
```

---

## When to use KMS vs keypair

| | Raw Keypair | AWS/GCP KMS |
|--|------------|-------------|
| Key storage | In-memory / env var | Cloud HSM |
| Key extraction | Private key is accessible | Private key never leaves KMS |
| Signing speed | Fastest | Network round-trip per sign |
| Audit trail | None | Cloud audit logs |
| Use case | Development, testing | Production backends |

---

## Multisig

Multisig allows multiple signers to collectively authorize transactions when their combined signature weight meets a threshold.

### Install

Multisig is built into `@mysten/sui`:

```typescript
import { MultiSigPublicKey } from '@mysten/sui/multisig';
```

### Setup: define threshold and weights

```typescript
import { Ed25519Keypair } from '@mysten/sui/keypairs/ed25519';
import { MultiSigPublicKey } from '@mysten/sui/multisig';

const kp1 = new Ed25519Keypair();
const kp2 = new Ed25519Keypair();
const kp3 = new Ed25519Keypair();

const multiSigPublicKey = MultiSigPublicKey.fromPublicKeys({
  threshold: 2,
  publicKeys: [
    { publicKey: kp1.getPublicKey(), weight: 1 },
    { publicKey: kp2.getPublicKey(), weight: 1 },
    { publicKey: kp3.getPublicKey(), weight: 2 },
  ],
});

const multisigAddress = multiSigPublicKey.toSuiAddress();
```

In this configuration:
- `kp1` alone (weight 1) cannot sign — below threshold of 2
- `kp1 + kp2` (weight 1+1=2) can sign — meets threshold
- `kp3` alone (weight 2) can sign — meets threshold

Maximum 10 accounts per multisig configuration.

### Option A: Manual signature combination

Collect individual signatures from each participant, then combine:

```typescript
// Each participant signs independently
const { signature: sig1 } = await kp1.signTransaction(txBytes);
const { signature: sig2 } = await kp2.signTransaction(txBytes);

// Combine (only need enough weight to meet threshold)
const combinedSignature = multiSigPublicKey.combinePartialSignatures([
  sig1,
  sig2,
]);

// Execute
const result = await client.executeTransaction({
  transaction: txBytes,
  signatures: [combinedSignature],
});
```

### Option B: MultiSigSigner (recommended)

Wraps a subset of keypairs into a single signer that handles combination automatically:

```typescript
// Create a signer from one keypair (if its weight alone meets threshold)
const signer = multiSigPublicKey.getSigner(kp3); // weight 2 meets threshold 2

// Or provide multiple keypairs whose combined weight meets threshold
// getSigner takes rest params (...signers)
const signer2 = multiSigPublicKey.getSigner(kp1, kp2); // weight 1+1=2 meets threshold
// Use like any other signer
const result = await signer.signAndExecuteTransaction({
  transaction: tx,
  client,
});
```

You can provide any subset of signers, as long as their combined weight meets the threshold.

### Hybrid multisig: keypairs + zkLogin

Combine traditional keypairs with zkLogin public identifiers for recovery:

```typescript
import { toZkLoginPublicIdentifier, genAddressSeed, decodeJwt } from '@mysten/sui/zklogin';

const kp1 = new Ed25519Keypair();
const decodedJwt = decodeJwt(jwtToken);
const userSalt = BigInt('123');
const addressSeed = genAddressSeed(
  userSalt,
  'sub',
  decodedJwt.sub!,
  decodedJwt.aud as string,
).toString();

const pkZklogin = toZkLoginPublicIdentifier(addressSeed, decodedJwt.iss!);

const multiSigPublicKey = MultiSigPublicKey.fromPublicKeys({
  threshold: 1,
  publicKeys: [
    { publicKey: kp1.getPublicKey(), weight: 1 },
    { publicKey: pkZklogin, weight: 1 },
  ],
});
```

This provides backup access to a zkLogin account through a traditional private key.

### Hybrid multisig: keypairs + passkeys

```typescript
import { PasskeyKeypair, BrowserPasskeyProvider } from '@mysten/sui/keypairs/passkey';

const passkeyKeypair = await PasskeyKeypair.getPasskeyInstance(
  new BrowserPasskeyProvider('My App', { /* options */ }),
);

const multiSigPublicKey = MultiSigPublicKey.fromPublicKeys({
  threshold: 1,
  publicKeys: [
    { publicKey: kp1.getPublicKey(), weight: 1 },
    { publicKey: passkeyKeypair.getPublicKey(), weight: 1 },
  ],
});
```

### Multisig with KMS signers

KMS signers implement the same `Signer` interface, so they work with `MultiSigSigner`:

```typescript
const kmsSigner = await AwsKmsSigner.fromKeyId('arn:aws:kms:...');
const localKeypair = new Ed25519Keypair();

const multiSigPublicKey = MultiSigPublicKey.fromPublicKeys({
  threshold: 2,
  publicKeys: [
    { publicKey: kmsSigner.getPublicKey(), weight: 1 },
    { publicKey: localKeypair.getPublicKey(), weight: 1 },
  ],
});

// Both sign
const { signature: kmsSig } = await kmsSigner.signTransaction(txBytes);
const { signature: localSig } = await localKeypair.signTransaction(txBytes);

const combined = multiSigPublicKey.combinePartialSignatures([kmsSig, localSig]);
```
