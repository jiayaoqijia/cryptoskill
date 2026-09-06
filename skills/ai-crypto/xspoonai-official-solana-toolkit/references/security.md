# Wallet Security Best Practices

Critical security guidelines for managing Solana wallets.

## Key Storage

### Encryption at Rest

Always encrypt private keys before storing:

```typescript
import {
  createCipheriv,
  createDecipheriv,
  randomBytes,
  scryptSync,
} from "crypto";

const ALGORITHM = "aes-256-gcm";

function deriveKey(password: string, salt: Buffer): Buffer {
  return scryptSync(password, salt, 32);
}

export function encryptPrivateKey(
  privateKey: Uint8Array,
  password: string,
): {
  encrypted: string;
  salt: string;
  iv: string;
  authTag: string;
} {
  const salt = randomBytes(16);
  const iv = randomBytes(16);
  const key = deriveKey(password, salt);

  const cipher = createCipheriv(ALGORITHM, key, iv);
  const encrypted = Buffer.concat([
    cipher.update(Buffer.from(privateKey)),
    cipher.final(),
  ]);

  return {
    encrypted: encrypted.toString("base64"),
    salt: salt.toString("base64"),
    iv: iv.toString("base64"),
    authTag: cipher.getAuthTag().toString("base64"),
  };
}

export function decryptPrivateKey(
  encryptedData: {
    encrypted: string;
    salt: string;
    iv: string;
    authTag: string;
  },
  password: string,
): Uint8Array {
  const key = deriveKey(password, Buffer.from(encryptedData.salt, "base64"));
  const decipher = createDecipheriv(
    ALGORITHM,
    key,
    Buffer.from(encryptedData.iv, "base64"),
  );
  decipher.setAuthTag(Buffer.from(encryptedData.authTag, "base64"));

  const decrypted = Buffer.concat([
    decipher.update(Buffer.from(encryptedData.encrypted, "base64")),
    decipher.final(),
  ]);

  return new Uint8Array(decrypted);
}
```

### File Permissions

```bash
# Wallet storage directory
chmod 700 ~/.config/solana-skill/wallets/

# Individual wallet files
chmod 600 ~/.config/solana-skill/wallets/*.json
```

### Never Store

- Plain text private keys
- Keys in environment variables (prefer encrypted files)
- Keys in version control
- Keys in logs or console output

## Address Validation

Always validate addresses before transactions:

```typescript
import { PublicKey } from "@solana/web3.js";

function isValidSolanaAddress(address: string): boolean {
  try {
    const pubkey = new PublicKey(address);
    return PublicKey.isOnCurve(pubkey.toBytes());
  } catch {
    return false;
  }
}

function validateAddressOrThrow(address: string, label: string): PublicKey {
  if (!isValidSolanaAddress(address)) {
    throw new Error(`Invalid ${label} address: ${address}`);
  }
  return new PublicKey(address);
}
```

## Transaction Safety

### Confirmation Levels

```typescript
// For high-value transactions, wait for finalized
const sig = await connection.sendTransaction(tx, [signer]);
await connection.confirmTransaction(sig, "finalized");

// For regular transactions, confirmed is sufficient
await connection.confirmTransaction(sig, "confirmed");
```

### Slippage Protection

```typescript
// Default: 1% slippage
const SLIPPAGE_BPS = 100; // 1% = 100 basis points

// For stablecoins: 0.1%
const STABLE_SLIPPAGE_BPS = 10;

// For volatile tokens: up to 5%
const VOLATILE_SLIPPAGE_BPS = 500;
```

### Amount Validation

```typescript
function validateTransferAmount(
  amount: number,
  balance: number,
  reserveForFees: number = 0.01, // SOL
): void {
  if (amount <= 0) {
    throw new Error("Amount must be positive");
  }
  if (amount > balance - reserveForFees) {
    throw new Error(
      `Insufficient balance. Have: ${balance}, Need: ${amount + reserveForFees}`,
    );
  }
}
```

## User Confirmation

For transactions above thresholds, require explicit confirmation:

```typescript
const CONFIRM_THRESHOLD_SOL = 1; // Confirm for >1 SOL
const CONFIRM_THRESHOLD_USD = 100; // Confirm for >$100

async function requireConfirmation(
  amount: number,
  token: string,
  recipient: string,
): Promise<boolean> {
  // In agent context, send message and wait for response
  const message =
    `⚠️ Confirm transaction:\n` +
    `Amount: ${amount} ${token}\n` +
    `To: ${recipient}\n` +
    `Reply YES to confirm`;

  // Implementation depends on messaging context
  return await waitForUserConfirmation(message);
}
```

## Audit Trail

Log all transactions (without sensitive data):

```typescript
interface TransactionLog {
  timestamp: string;
  type: "send" | "swap" | "receive";
  signature: string;
  from: string;
  to: string;
  amount: string;
  token: string;
  status: "pending" | "confirmed" | "failed";
  fee?: number;
}

function logTransaction(tx: TransactionLog): void {
  const logPath = `~/.config/solana-skill/logs/${tx.from}.jsonl`;
  appendFileSync(logPath, JSON.stringify(tx) + "\n");
}
```

## Common Attack Vectors

### 1. Address Poisoning

Attackers send tiny amounts from similar-looking addresses.
**Defense:** Always verify full address, not just first/last characters.

### 2. Approval Exploits

Malicious dApps request unlimited token approvals.
**Defense:** Only approve exact amounts needed.

### 3. Phishing Transactions

Transactions that look legitimate but drain wallets.
**Defense:** Simulate transactions before signing, verify all instructions.

### 4. Clipboard Hijacking

Malware replaces copied addresses.
**Defense:** Double-check pasted addresses against source.

## Emergency Procedures

### Key Compromise

1. Immediately create new wallet
2. Transfer all assets to new wallet
3. Revoke all token approvals from compromised wallet
4. Document incident

### Suspicious Transaction

1. Do NOT sign
2. Check transaction simulation
3. Verify all instruction accounts
4. When in doubt, reject
