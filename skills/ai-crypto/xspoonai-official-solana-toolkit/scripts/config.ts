/**
 * Configuration management for solana-skill
 */

import { readFileSync, existsSync, mkdirSync, writeFileSync } from 'fs';
import { homedir } from 'os';
import { join } from 'path';

export interface Config {
  heliusApiKey: string;
  network: 'mainnet-beta' | 'devnet';
  rpcUrl?: string;
}

const CONFIG_DIR = join(homedir(), '.config', 'solana-skill');
const CONFIG_FILE = join(CONFIG_DIR, 'config.json');
const WALLETS_DIR = join(CONFIG_DIR, 'wallets');

export function ensureConfigDir(): void {
  if (!existsSync(CONFIG_DIR)) {
    mkdirSync(CONFIG_DIR, { recursive: true, mode: 0o700 });
  }
  if (!existsSync(WALLETS_DIR)) {
    mkdirSync(WALLETS_DIR, { mode: 0o700 });
  }
}

export function loadConfig(): Config {
  ensureConfigDir();
  
  if (!existsSync(CONFIG_FILE)) {
    throw new Error(
      `Config not found. Create ${CONFIG_FILE} with:\n` +
      JSON.stringify({
        heliusApiKey: 'your-api-key',
        network: 'mainnet-beta'
      }, null, 2)
    );
  }
  
  const config = JSON.parse(readFileSync(CONFIG_FILE, 'utf-8')) as Config;
  
  if (!config.heliusApiKey) {
    throw new Error('heliusApiKey required in config');
  }
  
  return config;
}

export function getRpcUrl(config: Config): string {
  if (config.rpcUrl) return config.rpcUrl;
  
  const network = config.network || 'mainnet-beta';
  return `https://${network}.helius-rpc.com/?api-key=${config.heliusApiKey}`;
}

export function getWalletsDir(): string {
  ensureConfigDir();
  return WALLETS_DIR;
}

export function saveConfig(config: Config): void {
  ensureConfigDir();
  writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2), { mode: 0o600 });
}
