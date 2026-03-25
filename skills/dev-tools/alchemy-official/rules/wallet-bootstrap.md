# Wallet Setup

Use this rule when the agent does not yet have access to an Ethereum wallet for signing.

## Determine Wallet Source

Ask the user:

> Do you have an existing Ethereum wallet you'd like to use, or should I create a new one?

Based on the answer, follow one of the three paths below.

---

## Path A: Use an Existing Connected Wallet

If the user already has a wallet available (e.g. a private key in an environment variable or config file), derive the account from it and proceed directly to [Fund the Wallet](#fund-the-wallet).

---

## Path B: Import an Existing Wallet

The user provides their private key.

### 1. Derive the account

```typescript
import { privateKeyToAccount } from "viem/accounts";

const account = privateKeyToAccount("0x<user_private_key>" as `0x${string}`);

const wallet = {
  address: account.address,
  privateKey: "0x<user_private_key>",
};
```

### 2. Save to `wallet.json`

Write the wallet object to `wallet.json`:

```typescript
import { writeFileSync } from "node:fs";

writeFileSync("wallet.json", JSON.stringify(wallet, null, 2));
```

### 3. Add `wallet.json` to `.gitignore`

```bash
echo "wallet.json" >> .gitignore
```

Proceed to [Fund the Wallet](#fund-the-wallet).

---

## Path C: Create a New Wallet

### 1. Generate a private key and derive the account

```typescript
import { generatePrivateKey, privateKeyToAccount } from "viem/accounts";

const privateKey = generatePrivateKey();
const account = privateKeyToAccount(privateKey);

const wallet = {
  address: account.address,
  privateKey: privateKey,
};

console.log(JSON.stringify(wallet, null, 2));
```

This outputs wallet JSON to stdout:

```json
{
  "address": "0xYourChecksummedAddress",
  "privateKey": "0x..."
}
```

Save the output to `wallet.json`:

```bash
npx tsx create-wallet.ts > wallet.json
```

### 2. Add `wallet.json` to `.gitignore`

```bash
echo "wallet.json" >> .gitignore
```

Proceed to [Fund the Wallet](#fund-the-wallet).

---

## Fund the Wallet

### Testnet (Base Sepolia)

1. Go to the [Circle USDC faucet](https://faucet.circle.com/)
2. Select **Base Sepolia**
3. Paste your wallet address
4. Request testnet USDC

The USDC will arrive at your address on Base Sepolia (`0x036CbD53842c5426634e7929541eC2318f3dCF7e`).

### Mainnet

Transfer USDC to your wallet address on Base Mainnet.

## Load the Wallet in Code

```typescript
import { readFileSync } from "node:fs";
import { privateKeyToAccount } from "viem/accounts";

const wallet = JSON.parse(readFileSync("wallet.json", "utf-8")) as {
  address: string;
  privateKey: `0x${string}`;
};

const account = privateKeyToAccount(wallet.privateKey);
```

Use this `account` for SIWE token generation (see [authentication](authentication.md)) and payment signing (see [making-requests](making-requests.md)).
