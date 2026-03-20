/**
 * Sui Agent Wallet - Key Management with Keychain Support
 * 
 * Seed phrase is stored securely in macOS Keychain.
 * Only non-sensitive data (accounts, network) stored in wallet.json.
 */

import { Ed25519Keypair } from '@mysten/sui/keypairs/ed25519';
import { SuiClient } from '@mysten/sui/client';
import { toBase64, fromBase64 } from '@mysten/sui/utils';
import { existsSync, mkdirSync, readFileSync, writeFileSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';

import { generateMnemonic, validateMnemonic } from './bip39';
import { storeMnemonic, retrieveMnemonic, hasMnemonic } from './keychain';

const WALLET_DIR = join(homedir(), '.sui-agent-wallet');
const WALLET_FILE = join(WALLET_DIR, 'wallet.json');

export type NetworkType = 'mainnet' | 'testnet' | 'devnet' | 'localnet';

const NETWORK_URLS: Record<NetworkType, string> = {
  mainnet: 'https://fullnode.mainnet.sui.io:443',
  testnet: 'https://fullnode.testnet.sui.io:443',
  devnet: 'https://fullnode.devnet.sui.io:443',
  localnet: 'http://127.0.0.1:9000'
};

// Non-sensitive wallet data (stored in JSON file)
interface WalletData {
  accounts: {
    index: number;
    address: string;
    publicKey: string;
  }[];
  activeAccountIndex: number;
  network: NetworkType;
}

export class AgentWallet {
  private mnemonic: string;
  private accounts: Map<number, Ed25519Keypair> = new Map();
  private activeAccountIndex: number = 0;
  private network: NetworkType = 'devnet';
  private client: SuiClient;

  constructor() {
    this.mnemonic = this.loadOrCreateMnemonic();
    const data = this.loadWalletData();
    
    this.network = data.network;
    this.activeAccountIndex = data.activeAccountIndex;
    
    // Restore accounts from saved data
    for (const acc of data.accounts) {
      const keypair = this.deriveKeypair(acc.index);
      this.accounts.set(acc.index, keypair);
    }
    
    // Ensure at least one account exists
    if (this.accounts.size === 0) {
      this.createAccount(0);
    }
    
    this.client = new SuiClient({ url: NETWORK_URLS[this.network] });
  }

  private loadOrCreateMnemonic(): string {
    // Try to load from Keychain first
    const stored = retrieveMnemonic();
    if (stored && validateMnemonic(stored)) {
      console.log('🔐 Loaded seed phrase from macOS Keychain');
      return stored;
    }

    // Generate new mnemonic
    const mnemonic = generateMnemonic();
    
    // Store in Keychain
    if (storeMnemonic(mnemonic)) {
      console.log('');
      console.log('═══════════════════════════════════════════════════════════');
      console.log('  🔐 NEW WALLET CREATED');
      console.log('═══════════════════════════════════════════════════════════');
      console.log('');
      console.log('  Seed phrase stored securely in macOS Keychain.');
      console.log('');
      console.log('  To view your seed phrase for backup:');
      console.log('    curl http://localhost:3847/mnemonic');
      console.log('');
      console.log('  Or use macOS Keychain Access app:');
      console.log('    Service: sui-agent-wallet');
      console.log('    Account: mnemonic');
      console.log('');
      console.log('═══════════════════════════════════════════════════════════');
      console.log('');
    } else {
      // Fallback: print to console if Keychain fails
      console.log('');
      console.log('⚠️  Failed to store in Keychain. SAVE THIS SEED PHRASE:');
      console.log('');
      console.log(`  ${mnemonic}`);
      console.log('');
    }
    
    return mnemonic;
  }

  private loadWalletData(): WalletData {
    if (!existsSync(WALLET_DIR)) {
      mkdirSync(WALLET_DIR, { recursive: true });
    }

    if (existsSync(WALLET_FILE)) {
      try {
        const data = JSON.parse(readFileSync(WALLET_FILE, 'utf-8')) as WalletData;
        // Migration: remove mnemonic if it exists in old file
        if ((data as any).mnemonic) {
          delete (data as any).mnemonic;
          this.saveWalletData(data);
          console.log('📦 Migrated wallet data (removed mnemonic from file)');
        }
        return data;
      } catch (e) {
        console.error('Failed to load wallet data');
      }
    }

    // Default data
    return {
      accounts: [],
      activeAccountIndex: 0,
      network: 'devnet'
    };
  }

  private deriveKeypair(accountIndex: number): Ed25519Keypair {
    // Derive using BIP44 path: m/44'/784'/accountIndex'/0'/0'
    const path = `m/44'/784'/${accountIndex}'/0'/0'`;
    return Ed25519Keypair.deriveKeypair(this.mnemonic, path);
  }

  private saveWalletData(data?: WalletData) {
    const walletData: WalletData = data || {
      accounts: Array.from(this.accounts.entries()).map(([index, kp]) => ({
        index,
        address: kp.toSuiAddress(),
        publicKey: toBase64(kp.getPublicKey().toRawBytes())
      })),
      activeAccountIndex: this.activeAccountIndex,
      network: this.network
    };
    writeFileSync(WALLET_FILE, JSON.stringify(walletData, null, 2));
  }

  // === Account Management ===

  createAccount(index?: number): { address: string; index: number } {
    const accountIndex = index ?? this.accounts.size;
    
    if (this.accounts.has(accountIndex)) {
      const existing = this.accounts.get(accountIndex)!;
      return { address: existing.toSuiAddress(), index: accountIndex };
    }
    
    const keypair = this.deriveKeypair(accountIndex);
    this.accounts.set(accountIndex, keypair);
    this.saveWalletData();
    
    console.log(`Created account #${accountIndex}: ${keypair.toSuiAddress()}`);
    return { address: keypair.toSuiAddress(), index: accountIndex };
  }

  switchAccount(index: number): { address: string; index: number } {
    if (!this.accounts.has(index)) {
      this.createAccount(index);
    }
    
    this.activeAccountIndex = index;
    this.saveWalletData();
    
    const keypair = this.accounts.get(index)!;
    console.log(`Switched to account #${index}: ${keypair.toSuiAddress()}`);
    return { address: keypair.toSuiAddress(), index };
  }

  getAccounts(): { address: string; index: number; active: boolean }[] {
    return Array.from(this.accounts.entries()).map(([index, kp]) => ({
      index,
      address: kp.toSuiAddress(),
      active: index === this.activeAccountIndex
    }));
  }

  getActiveKeypair(): Ed25519Keypair {
    return this.accounts.get(this.activeAccountIndex)!;
  }

  // === Network Management ===

  getNetwork(): NetworkType {
    return this.network;
  }

  switchNetwork(network: NetworkType): { network: NetworkType; rpcUrl: string } {
    this.network = network;
    this.client = new SuiClient({ url: NETWORK_URLS[network] });
    this.saveWalletData();
    
    console.log(`Switched to network: ${network}`);
    return { network, rpcUrl: NETWORK_URLS[network] };
  }

  getClient(): SuiClient {
    return this.client;
  }

  // === Address & Keys ===

  getAddress(): string {
    return this.getActiveKeypair().toSuiAddress();
  }

  getPublicKey(): Uint8Array {
    return this.getActiveKeypair().getPublicKey().toRawBytes();
  }

  getMnemonic(): string {
    return this.mnemonic;
  }

  // === Signing ===

  async signTransaction(txBytes: Uint8Array): Promise<{ bytes: string; signature: string }> {
    const keypair = this.getActiveKeypair();
    const signature = await keypair.signTransaction(txBytes);
    return {
      bytes: toBase64(txBytes),
      signature: signature.signature
    };
  }

  async signAndExecuteTransaction(
    txBytes: Uint8Array,
    options?: { showEffects?: boolean; showEvents?: boolean; showObjectChanges?: boolean }
  ) {
    const keypair = this.getActiveKeypair();
    const signature = await keypair.signTransaction(txBytes);
    
    const result = await this.client.executeTransactionBlock({
      transactionBlock: toBase64(txBytes),
      signature: signature.signature,
      options: {
        showEffects: options?.showEffects ?? true,
        showEvents: options?.showEvents ?? true,
        showObjectChanges: options?.showObjectChanges ?? true
      }
    });
    
    return result;
  }

  async signPersonalMessage(message: Uint8Array): Promise<{ bytes: string; signature: string }> {
    const keypair = this.getActiveKeypair();
    const signature = await keypair.signPersonalMessage(message);
    return {
      bytes: toBase64(message),
      signature: signature.signature
    };
  }

  // === Balance ===

  async getBalance(address?: string): Promise<string> {
    const balance = await this.client.getBalance({
      owner: address || this.getAddress()
    });
    return balance.totalBalance;
  }

  // === Import/Export ===

  importMnemonic(mnemonic: string): { address: string } {
    if (!validateMnemonic(mnemonic)) {
      throw new Error('Invalid mnemonic phrase');
    }
    
    // Store new mnemonic in Keychain
    if (!storeMnemonic(mnemonic)) {
      throw new Error('Failed to store mnemonic in Keychain');
    }
    
    this.mnemonic = mnemonic;
    this.accounts.clear();
    this.activeAccountIndex = 0;
    
    // Create first account
    this.createAccount(0);
    
    console.log('Imported wallet from mnemonic');
    return { address: this.getAddress() };
  }

  exportMnemonic(): string {
    return this.mnemonic;
  }
}
