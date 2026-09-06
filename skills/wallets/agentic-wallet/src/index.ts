#!/usr/bin/env node

import { Command } from 'commander';
import { setupWallet } from './commands/setup.js';
import { statusWallet } from './commands/status.js';
import { fundWallet } from './commands/fund.js';
import { providers } from './commands/providers.js';
import { balanceCommand } from './commands/balance.js';
import { backupWallet } from './commands/backup.js';
import { recoverWallet } from './commands/recover.js';
import { schemaCommand } from './commands/schema.js';
import {
  cardStatus, cardCreate, cardLinkWallet, cardUnlinkWallet,
  cardFreeze, cardUnfreeze, cardTransactions,
  cardOnboardingStart, cardOnboardingCheck, cardOnboardingFinish
} from './commands/card.js';
import { isJsonMode } from './utils/output.js';

const program = new Command();

program
  .name('agent-wallet')
  .description('CLI for agents to create and manage wallets via Coinbase, Tempo (Stripe), OpenWallet (Moonpay), or Crossmint providers. Agent Arena NEVER stores your keys.')
  .version('1.1.0');

program
  .command('setup')
  .description('Set up a new wallet with your chosen provider')
  .option('-p, --provider <provider>', 'Wallet provider: coinbase, tempo, openwallet, or crossmint')
  .option('-c, --chain <chain>', 'Target chain: base, ethereum, arbitrum, optimism, polygon (default: base)')
  .option('-n, --name <name>', 'Wallet name for openwallet provider (default: "default")')
  .option('--password-file <path>', 'Path to file containing encryption password (for non-interactive openwallet)')
  .option('--api-key-file <path>', 'Path to file containing Crossmint API key (for non-interactive crossmint)')
  .option('--chain-type <type>', 'Crossmint chain type: evm, solana, aptos, sui, stellar (default: evm)')
  .option('--wallet-type <type>', 'Crossmint wallet type: smart or mpc (default: smart)')
  .option('--non-interactive', 'Run without prompts (requires --password-file for openwallet, --api-key-file for crossmint)')
  .option('--json', 'Output as JSON for programmatic use')
  .action(setupWallet);

program
  .command('balance')
  .description('Check wallet balances across all providers')
  .option('-a, --all', 'Check all providers at once')
  .option('-p, --provider <provider>', 'Check specific provider: coinbase, tempo, openwallet, or crossmint')
  .option('--json', 'Output as JSON for programmatic use')
  .option('--fields <fields>', 'Comma-separated fields to include (e.g. address,balanceUSDC)')
  .action(balanceCommand);

program
  .command('status')
  .description('Check wallet authentication status')
  .option('-p, --provider <provider>', 'Wallet provider to check')
  .option('--json', 'Output as JSON for programmatic use')
  .action(statusWallet);

program
  .command('fund')
  .description('Get instructions to fund your wallet')
  .option('-p, --provider <provider>', 'Wallet provider')
  .option('--json', 'Output as JSON for programmatic use')
  .action(fundWallet);

program
  .command('backup')
  .description('Backup an OpenWallet to encrypted file')
  .option('-n, --name <name>', 'Wallet name to backup (default: "default")')
  .option('-o, --output <path>', 'Output directory for backup file')
  .option('--password-file <path>', 'Path to file containing encryption password')
  .option('--json', 'Output as JSON for programmatic use')
  .action(backupWallet);

program
  .command('recover')
  .description('Recover an OpenWallet from backup or seed phrase')
  .option('--from <path>', 'Path to backup file')
  .option('--seed-phrase', 'Recover from 12-word seed phrase')
  .option('-n, --name <name>', 'Name for recovered wallet (default: "recovered")')
  .option('--password-file <path>', 'Path to file containing encryption password')
  .option('--json', 'Output as JSON for programmatic use')
  .action(recoverWallet);

program
  .command('providers')
  .description('List available wallet providers and their features')
  .option('--json', 'Output as JSON for programmatic use')
  .action(providers);

program
  .command('schema')
  .description('Show machine-readable schema for a command')
  .argument('[command]', 'Command to show schema for (omit for all)')
  .action(schemaCommand);

// --- MoonAgents Card commands (MoonPay) ---
const card = program
  .command('card')
  .description('MoonAgents Card — virtual Mastercard debit card for AI agents (powered by MoonPay + Monavate)');

card
  .command('status')
  .description('Check MoonAgents Card status')
  .option('--json', 'Output as JSON for programmatic use')
  .action(cardStatus);

card
  .command('create')
  .description('Issue a new MoonAgents virtual Mastercard (requires KYC)')
  .option('--json', 'Output as JSON for programmatic use')
  .action(cardCreate);

card
  .command('link-wallet')
  .description('Link an onchain wallet to your card with a spending cap')
  .option('-w, --wallet <name>', 'Wallet name to link')
  .option('-c, --currency <currency>', 'Stablecoin currency (default: usdc)')
  .option('-a, --amount <amount>', 'Spending cap in the chosen currency')
  .option('--json', 'Output as JSON for programmatic use')
  .action(cardLinkWallet);

card
  .command('unlink-wallet')
  .description('Revoke card access to a wallet (stops spending immediately)')
  .option('-w, --wallet <name>', 'Wallet name to unlink')
  .option('--json', 'Output as JSON for programmatic use')
  .action(cardUnlinkWallet);

card
  .command('freeze')
  .description('Freeze card — pause all transactions instantly')
  .option('--json', 'Output as JSON for programmatic use')
  .action(cardFreeze);

card
  .command('unfreeze')
  .description('Unfreeze card — re-enable transactions')
  .option('--json', 'Output as JSON for programmatic use')
  .action(cardUnfreeze);

card
  .command('transactions')
  .description('List card transactions')
  .option('--json', 'Output as JSON for programmatic use')
  .action(cardTransactions);

card
  .command('onboarding-start')
  .description('Start KYC identity verification (required before card issuance)')
  .option('--first-name <name>', 'First name')
  .option('--last-name <name>', 'Last name')
  .option('--country-of-residence <code>', 'ISO 3166-1 alpha-3 country code (e.g. GBR)')
  .option('--country-of-nationality <code>', 'ISO 3166-1 alpha-3 country code')
  .option('--phone-country-code <code>', 'Phone country code (e.g. +44)')
  .option('--phone-number <number>', 'Phone number (digits only)')
  .option('--date-of-birth <date>', 'Date of birth (YYYY-MM-DD)')
  .option('--json', 'Output as JSON for programmatic use')
  .action(cardOnboardingStart);

card
  .command('onboarding-check')
  .description('Check KYC verification status')
  .option('--json', 'Output as JSON for programmatic use')
  .action(cardOnboardingCheck);

card
  .command('onboarding-finish')
  .description('Complete KYC by submitting address and accepting terms')
  .option('--address-line1 <address>', 'Street address')
  .option('--city <city>', 'City')
  .option('--zip <zip>', 'ZIP or postal code')
  .option('--accept-terms', 'Accept MoonAgents Card terms and conditions')
  .option('--json', 'Output as JSON for programmatic use')
  .action(cardOnboardingFinish);

program.parse();
