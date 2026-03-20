import { KeyPair } from 'near-api-js';
import * as fs from 'fs';
import * as path from 'path';
import * as bs58 from 'bs58';
import * as nacl from 'tweetnacl';

// Generate a new key pair
const keyPair = KeyPair.fromRandom('ed25519');
const publicKeyStr = keyPair.toString();

// For implicit accounts, we need to create a key pair from scratch to get the secret key
const secretKeyUint8 = nacl.sign.keyPair().secretKey;
const publicKeyUint8 = nacl.sign.keyPair().publicKey;

// Encode in base58
const secretKeyBase58 = bs58.encode(secretKeyUint8);
const publicKeyBase58 = bs58.encode(publicKeyUint8);

// The account ID is the public key in base58 (implicit account)
const accountId = publicKeyBase58;
const privateKey = `ed25519:${secretKeyBase58}`;
const publicKey = `ed25519:${publicKeyBase58}`;

console.log('=== Generated NEAR Account ===');
console.log('Account ID (Implicit):', accountId);
console.log('Public Key:', publicKey);
console.log('Private Key:', privateKey);
console.log('');
console.log('IMPORTANT:');
console.log('1. Save this private key securely - it gives full access to the account');
console.log('2. Fund the account at:', accountId);
console.log('3. Once funded, you can use this account for NEAR Intents operations');

// Save to a file for reference
const output = {
  accountId: accountId,
  publicKey: publicKey,
  privateKey: privateKey,
  generatedAt: new Date().toISOString()
};

const outputPath = path.join(__dirname, '..', '.env.example');
fs.writeFileSync(outputPath, `# NEAR Account Configuration for NEAR Intents Skill\nNEAR_ACCOUNT_ID=${accountId}\nNEAR_PRIVATE_KEY=${privateKey}\nNEAR_RPC_URL=https://rpc.mainnet.fastnear.com\nNEAR_NETWORK_ID=mainnet\n`);

console.log('');
console.log(`Configuration saved to: ${outputPath}`);
