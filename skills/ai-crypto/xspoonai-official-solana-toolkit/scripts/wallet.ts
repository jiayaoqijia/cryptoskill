/**
 * Wallet management for solana-skill
 * 
 * Usage:
 *   npx tsx scripts/wallet.ts create [name]
 *   npx tsx scripts/wallet.ts list
 *   npx tsx scripts/wallet.ts balance [name]
 *   npx tsx scripts/wallet.ts export [name] (shows public key only)
 */

import { Keypair, Connection, PublicKey, LAMPORTS_PER_SOL } from '@solana/web3.js';
import { readFileSync, writeFileSync, readdirSync, existsSync } from 'fs';
import { join } from 'path';
import { createCipheriv, createDecipheriv, randomBytes, scryptSync, createHash } from 'crypto';
import bs58 from 'bs58';
import { loadConfig, getRpcUrl, getWalletsDir } from './config.js';

const ALGORITHM = 'aes-256-gcm';

// Encryption helpers
function deriveKey(password: string, salt: Buffer): Buffer {
  return scryptSync(password, salt, 32);
}

interface EncryptedWallet {
  name: string;
  publicKey: string;
  encrypted: string;
  salt: string;
  iv: string;
  authTag: string;
  createdAt: string;
}

function encryptPrivateKey(privateKey: Uint8Array, password: string): Omit<EncryptedWallet, 'name' | 'publicKey' | 'createdAt'> {
  const salt = randomBytes(16);
  const iv = randomBytes(16);
  const key = deriveKey(password, salt);
  
  const cipher = createCipheriv(ALGORITHM, key, iv);
  const encrypted = Buffer.concat([
    cipher.update(Buffer.from(privateKey)),
    cipher.final()
  ]);
  
  return {
    encrypted: encrypted.toString('base64'),
    salt: salt.toString('base64'),
    iv: iv.toString('base64'),
    authTag: cipher.getAuthTag().toString('base64')
  };
}

function decryptPrivateKey(wallet: EncryptedWallet, password: string): Uint8Array {
  const key = deriveKey(password, Buffer.from(wallet.salt, 'base64'));
  const decipher = createDecipheriv(
    ALGORITHM,
    key,
    Buffer.from(wallet.iv, 'base64')
  );
  decipher.setAuthTag(Buffer.from(wallet.authTag, 'base64'));
  
  const decrypted = Buffer.concat([
    decipher.update(Buffer.from(wallet.encrypted, 'base64')),
    decipher.final()
  ]);
  
  return new Uint8Array(decrypted);
}

// Derive password from machine-specific data (simple protection)
function getDefaultPassword(): string {
  const machineId = process.env.USER + process.env.HOME;
  return createHash('sha256').update(machineId).digest('hex');
}

// Wallet operations
export function createWallet(name: string): { publicKey: string; walletPath: string } {
  const walletsDir = getWalletsDir();
  const walletPath = join(walletsDir, `${name}.json`);
  
  if (existsSync(walletPath)) {
    throw new Error(`Wallet "${name}" already exists`);
  }
  
  const keypair = Keypair.generate();
  const password = getDefaultPassword();
  const encryptedData = encryptPrivateKey(keypair.secretKey, password);
  
  const wallet: EncryptedWallet = {
    name,
    publicKey: keypair.publicKey.toBase58(),
    ...encryptedData,
    createdAt: new Date().toISOString()
  };
  
  writeFileSync(walletPath, JSON.stringify(wallet, null, 2), { mode: 0o600 });
  
  return {
    publicKey: wallet.publicKey,
    walletPath
  };
}

export function loadWallet(name: string): Keypair {
  const walletsDir = getWalletsDir();
  const walletPath = join(walletsDir, `${name}.json`);
  
  if (!existsSync(walletPath)) {
    throw new Error(`Wallet "${name}" not found`);
  }
  
  const wallet: EncryptedWallet = JSON.parse(readFileSync(walletPath, 'utf-8'));
  const password = getDefaultPassword();
  const secretKey = decryptPrivateKey(wallet, password);
  
  return Keypair.fromSecretKey(secretKey);
}

export function listWallets(): Array<{ name: string; publicKey: string; createdAt: string }> {
  const walletsDir = getWalletsDir();
  
  if (!existsSync(walletsDir)) {
    return [];
  }
  
  const files = readdirSync(walletsDir).filter(f => f.endsWith('.json'));
  
  return files.map(file => {
    const wallet: EncryptedWallet = JSON.parse(
      readFileSync(join(walletsDir, file), 'utf-8')
    );
    return {
      name: wallet.name,
      publicKey: wallet.publicKey,
      createdAt: wallet.createdAt
    };
  });
}

export async function getBalance(publicKey: string | PublicKey): Promise<{
  sol: number;
  lamports: number;
}> {
  const config = loadConfig();
  const connection = new Connection(getRpcUrl(config));
  
  const pubkey = typeof publicKey === 'string' ? new PublicKey(publicKey) : publicKey;
  const lamports = await connection.getBalance(pubkey);
  
  return {
    sol: lamports / LAMPORTS_PER_SOL,
    lamports
  };
}

export async function getFullBalance(publicKey: string): Promise<{
  sol: number;
  tokens: Array<{
    mint: string;
    symbol?: string;
    amount: number;
    decimals: number;
    uiAmount: number;
  }>;
}> {
  const config = loadConfig();
  const rpcUrl = getRpcUrl(config);
  
  // Use Helius DAS API for comprehensive balance
  const response = await fetch(rpcUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      jsonrpc: '2.0',
      id: 'balance-1',
      method: 'getAssetsByOwner',
      params: {
        ownerAddress: publicKey,
        page: 1,
        limit: 1000,
        displayOptions: {
          showFungible: true,
          showNativeBalance: true
        }
      }
    })
  });
  
  const data = await response.json();
  
  if (data.error) {
    throw new Error(data.error.message);
  }
  
  const result = data.result;
  const sol = (result.nativeBalance?.lamports || 0) / LAMPORTS_PER_SOL;
  
  const tokens = result.items
    ?.filter((item: any) => item.interface === 'FungibleToken' || item.interface === 'FungibleAsset')
    .map((item: any) => ({
      mint: item.id,
      symbol: item.content?.metadata?.symbol,
      amount: parseInt(item.token_info?.balance || '0'),
      decimals: item.token_info?.decimals || 0,
      uiAmount: parseInt(item.token_info?.balance || '0') / Math.pow(10, item.token_info?.decimals || 0)
    })) || [];
  
  return { sol, tokens };
}

// CLI handler
async function main() {
  const [,, command, ...args] = process.argv;
  
  switch (command) {
    case 'create': {
      const name = args[0] || `wallet-${Date.now()}`;
      const { publicKey, walletPath } = createWallet(name);
      console.log(`✅ Created wallet "${name}"`);
      console.log(`   Public Key: ${publicKey}`);
      console.log(`   Saved to: ${walletPath}`);
      break;
    }
    
    case 'list': {
      const wallets = listWallets();
      if (wallets.length === 0) {
        console.log('No wallets found. Create one with: npx tsx scripts/wallet.ts create [name]');
      } else {
        console.log('Wallets:\n');
        for (const w of wallets) {
          console.log(`  ${w.name}`);
          console.log(`    ${w.publicKey}`);
          console.log(`    Created: ${w.createdAt}\n`);
        }
      }
      break;
    }
    
    case 'balance': {
      const name = args[0];
      if (!name) {
        console.error('Usage: npx tsx scripts/wallet.ts balance <name>');
        process.exit(1);
      }
      
      const wallets = listWallets();
      const wallet = wallets.find(w => w.name === name);
      
      if (!wallet) {
        console.error(`Wallet "${name}" not found`);
        process.exit(1);
      }
      
      console.log(`Fetching balance for ${name}...`);
      const balance = await getFullBalance(wallet.publicKey);
      
      console.log(`\n💰 ${name} (${wallet.publicKey})`);
      console.log(`   SOL: ${balance.sol.toFixed(6)}`);
      
      if (balance.tokens.length > 0) {
        console.log('\n   Tokens:');
        for (const token of balance.tokens) {
          console.log(`   - ${token.symbol || token.mint.slice(0, 8)}: ${token.uiAmount}`);
        }
      }
      break;
    }
    
    case 'export': {
      const name = args[0];
      if (!name) {
        console.error('Usage: npx tsx scripts/wallet.ts export <name>');
        process.exit(1);
      }
      
      const wallets = listWallets();
      const wallet = wallets.find(w => w.name === name);
      
      if (!wallet) {
        console.error(`Wallet "${name}" not found`);
        process.exit(1);
      }
      
      console.log(`Public Key: ${wallet.publicKey}`);
      console.log('\n⚠️  Private key export disabled for security.');
      console.log('   To use this wallet programmatically, use loadWallet() from this module.');
      break;
    }
    
    default:
      console.log(`
Solana Wallet Manager

Commands:
  create [name]   Create a new wallet
  list            List all wallets
  balance <name>  Check wallet balance
  export <name>   Show public key

Examples:
  npx tsx scripts/wallet.ts create main
  npx tsx scripts/wallet.ts balance main
`);
  }
}

main().catch(console.error);
