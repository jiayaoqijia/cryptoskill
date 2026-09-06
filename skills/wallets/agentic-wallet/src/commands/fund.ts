import chalk from 'chalk';
import inquirer from 'inquirer';
import { execSync } from 'child_process';
import { listAllWallets, listCrossmintWallets, CHAIN_CONFIG } from '../utils/storage.js';
import { isJsonMode, jsonOut, jsonError, ExitCode } from '../utils/output.js';

interface FundOptions {
  provider?: string;
  json?: boolean;
}

export async function fundWallet(options: FundOptions): Promise<void> {
  const useJson = isJsonMode(options);
  let { provider } = options;

  // Provider selection if not specified
  if (!provider) {
    if (useJson) jsonError(ExitCode.INVALID_INPUT, '--provider is required in JSON/piped mode', { validProviders: ['coinbase', 'tempo', 'openwallet', 'crossmint'] });
    const answers = await inquirer.prompt([
      {
        type: 'list',
        name: 'provider',
        message: 'Which wallet do you want to fund?',
        choices: [
          { name: 'Coinbase Agentic Wallet (Coinbase)', value: 'coinbase' },
          { name: 'Tempo Wallet (Stripe)', value: 'tempo' },
          { name: 'OpenWallet Standard (Moonpay)', value: 'openwallet' },
          { name: 'Crossmint Wallet (Crossmint)', value: 'crossmint' }
        ]
      }
    ]);
    provider = answers.provider;
  }

  if (!useJson) console.log();

  switch (provider) {
    case 'coinbase':
      await fundCoinbase(useJson);
      break;
    case 'tempo':
      await fundTempo(useJson);
      break;
    case 'openwallet':
      await fundOpenWallet(useJson);
      break;
    case 'crossmint':
      await fundCrossmint(useJson);
      break;
    default:
      if (useJson) jsonError(ExitCode.INVALID_INPUT, `Unknown provider: ${provider}`);
      console.error(chalk.red(`Unknown provider: ${provider}`));
      process.exit(ExitCode.INVALID_INPUT);
  }
}

async function fundCoinbase(useJson: boolean): Promise<void> {
  if (!useJson) {
    console.log(chalk.bold('Fund Coinbase Agentic Wallet'));
    console.log(chalk.gray('─'.repeat(50)));
    console.log();
  }

  let address = '';
  try {
    address = execSync('npx awal address 2>/dev/null', {
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'pipe']
    }).trim();
  } catch {
    if (useJson) jsonError(ExitCode.NOT_AUTHENTICATED, 'Coinbase wallet not authenticated', { setupCommand: 'npx agentic-wallet setup --provider coinbase' });
    console.log(chalk.yellow('⚠ Coinbase wallet not authenticated.'));
    console.log(chalk.gray('Run: npx agentic-wallet setup --provider coinbase'));
    process.exit(ExitCode.NOT_AUTHENTICATED);
    return;
  }

  if (!address || !address.startsWith('0x')) {
    if (useJson) jsonError(ExitCode.NOT_AUTHENTICATED, 'Could not get wallet address');
    console.log(chalk.yellow('⚠ Could not get wallet address.'));
    process.exit(ExitCode.NOT_AUTHENTICATED);
    return;
  }

  if (useJson) {
    jsonOut({
      ok: true,
      provider: 'coinbase',
      address,
      chain: 'Base',
      chainId: 8453,
      usdcContract: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',
      fundingMethods: [
        { method: 'direct_transfer', description: 'Send USDC to this address on Base mainnet' },
        { method: 'coinbase_onramp', description: 'Use Coinbase onramp (if available)' },
        { method: 'bridge', services: ['https://app.squidrouter.com/', 'https://relay.link/'] }
      ]
    });
    return;
  }

  console.log(chalk.cyan('Your Coinbase Wallet Address:'));
  console.log(chalk.white(`  ${address}`));
  console.log();
  console.log(chalk.bold('Funding Options:'));
  console.log();
  console.log('  1. ' + chalk.white('Send USDC to this address on Base mainnet'));
  console.log('     USDC Contract: 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913');
  console.log();
  console.log('  2. ' + chalk.white('Use Coinbase onramp (if available in your region)'));
  console.log();
  console.log('  3. ' + chalk.white('Bridge from another chain'));
  console.log('     - Squid: https://app.squidrouter.com/');
  console.log('     - Relay: https://relay.link/');
  console.log();
  console.log(chalk.gray('Check balance: npx awal balance'));
}

async function fundTempo(useJson: boolean): Promise<void> {
  let tempoCmd = '';
  try {
    execSync('which tempo', { stdio: 'pipe' });
    tempoCmd = 'tempo';
  } catch {
    try {
      execSync('test -f "$HOME/.tempo/bin/tempo"', { stdio: 'pipe' });
      tempoCmd = '$HOME/.tempo/bin/tempo';
    } catch {
      if (useJson) jsonError(ExitCode.PROVIDER_NOT_INSTALLED, 'Tempo CLI not installed', { setupCommand: 'npx agentic-wallet setup --provider tempo' });
      console.log(chalk.yellow('⚠ Tempo CLI not installed.'));
      console.log(chalk.gray('Run: npx agentic-wallet setup --provider tempo'));
      process.exit(ExitCode.PROVIDER_NOT_INSTALLED);
      return;
    }
  }

  if (useJson) {
    jsonOut({
      ok: true,
      provider: 'tempo',
      fundingMethods: [
        { method: 'cli', command: 'tempo wallet fund', description: 'Fund via Tempo CLI (recommended)' },
        { method: 'web', url: 'https://wallet.tempo.xyz', description: 'Web wallet — click Add funds' },
        { method: 'bridge', services: [
          { name: 'LayerZero (Stargate)', url: 'https://stargate.finance/' },
          { name: 'Squid', url: 'https://app.squidrouter.com/' },
          { name: 'Relay', url: 'https://relay.link/' },
          { name: 'Across', url: 'https://app.across.to/' }
        ]}
      ]
    });
    return;
  }

  console.log(chalk.bold('Fund Tempo Wallet'));
  console.log(chalk.gray('─'.repeat(50)));
  console.log();
  console.log(chalk.cyan('Tempo Funding Options:'));
  console.log();
  console.log('  1. ' + chalk.bold('CLI (recommended):'));
  console.log(chalk.white('     tempo wallet fund'));
  console.log();
  console.log('  2. ' + chalk.bold('Web Wallet:'));
  console.log('     https://wallet.tempo.xyz');
  console.log('     Click "Add funds" after logging in');
  console.log();
  console.log('  3. ' + chalk.bold('Bridge USDC from other chains:'));
  console.log('     - LayerZero (Stargate): https://stargate.finance/');
  console.log('     - Squid: https://app.squidrouter.com/');
  console.log('     - Relay: https://relay.link/');
  console.log('     - Across: https://app.across.to/');
  console.log();
  console.log(chalk.gray('Check balance: tempo wallet -t whoami'));
}

async function fundOpenWallet(useJson: boolean): Promise<void> {
  const wallets = listAllWallets();

  if (wallets.length === 0) {
    if (useJson) jsonError(ExitCode.WALLET_NOT_FOUND, 'No OpenWallet wallets found', { setupCommand: 'npx agentic-wallet setup --provider openwallet' });
    console.log(chalk.bold('Fund OpenWallet (Moonpay)'));
    console.log(chalk.gray('─'.repeat(50)));
    console.log();
    console.log(chalk.yellow('⚠ No OpenWallet wallets found.'));
    console.log(chalk.gray('Run: npx agentic-wallet setup --provider openwallet'));
    process.exit(ExitCode.WALLET_NOT_FOUND);
    return;
  }

  // For JSON mode, return all wallets with funding info
  if (useJson) {
    jsonOut({
      ok: true,
      provider: 'openwallet',
      wallets: wallets.map(w => ({
        name: w.name,
        address: w.address,
        chain: w.chain,
        chainId: w.chainId,
        usdcContract: w.chainId === 8453 ? '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913' : undefined
      })),
      fundingMethods: [
        { method: 'direct_transfer', description: 'Send USDC to wallet address on correct chain' },
        { method: 'bridge', services: [
          { name: 'Squid', url: 'https://app.squidrouter.com/' },
          { name: 'Relay', url: 'https://relay.link/' },
          { name: 'Across', url: 'https://app.across.to/' }
        ]}
      ]
    });
    return;
  }

  console.log(chalk.bold('Fund OpenWallet (Moonpay)'));
  console.log(chalk.gray('─'.repeat(50)));
  console.log();

  // Let user select wallet if multiple
  let selectedWallet = wallets[0];
  if (wallets.length > 1) {
    const { walletName } = await inquirer.prompt([
      {
        type: 'list',
        name: 'walletName',
        message: 'Select wallet to fund:',
        choices: wallets.map(w => ({
          name: `${w.name} (${w.address.slice(0, 10)}...${w.address.slice(-8)})`,
          value: w.name
        }))
      }
    ]);
    selectedWallet = wallets.find(w => w.name === walletName)!;
  }

  console.log(chalk.cyan('Wallet to Fund:'));
  console.log(`  Name:    ${selectedWallet.name}`);
  console.log(`  Address: ${selectedWallet.address}`);
  console.log(`  Chain:   ${selectedWallet.chain} (${selectedWallet.chainId})`);
  console.log();

  console.log(chalk.bold('Funding Options:'));
  console.log();
  console.log('  1. ' + chalk.white('Send USDC to this address'));
  console.log(`     Chain: ${selectedWallet.chain}`);
  if (selectedWallet.chainId === 8453) {
    console.log('     USDC Contract: 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913');
  }
  console.log();
  console.log('  2. ' + chalk.white('Bridge from another chain'));
  console.log('     - Squid: https://app.squidrouter.com/');
  console.log('     - Relay: https://relay.link/');
  console.log('     - Across: https://app.across.to/');
  console.log();
  console.log(chalk.yellow('⚠ Important:'));
  console.log(chalk.white('  Make sure to send to the correct chain!'));
  console.log(chalk.white(`  Your wallet is on: ${selectedWallet.chain}`));
}

async function fundCrossmint(useJson: boolean): Promise<void> {
  const wallets = listCrossmintWallets();

  if (wallets.length === 0) {
    if (useJson) jsonError(ExitCode.WALLET_NOT_FOUND, 'No Crossmint wallets found', { setupCommand: 'npx agentic-wallet setup --provider crossmint' });
    console.log(chalk.bold('Fund Crossmint Wallet'));
    console.log(chalk.gray('─'.repeat(50)));
    console.log();
    console.log(chalk.yellow('⚠ No Crossmint wallets found.'));
    console.log(chalk.gray('Run: npx agentic-wallet setup --provider crossmint'));
    process.exit(ExitCode.WALLET_NOT_FOUND);
    return;
  }

  // Select wallet if multiple
  let selectedWallet = wallets[0];
  if (wallets.length > 1 && !useJson) {
    const { walletName } = await inquirer.prompt([
      {
        type: 'list',
        name: 'walletName',
        message: 'Select Crossmint wallet to fund:',
        choices: wallets.map(w => ({
          name: `${w.name} (${w.address ? w.address.slice(0, 10) + '...' + w.address.slice(-8) : 'no address'}) — ${w.chainType} ${w.custodyModel}`,
          value: w.name
        }))
      }
    ]);
    selectedWallet = wallets.find(w => w.name === walletName)!;
  }

  if (useJson) {
    jsonOut({
      ok: true,
      provider: 'crossmint',
      wallet: {
        name: selectedWallet.name,
        address: selectedWallet.address,
        chainType: selectedWallet.chainType,
        walletType: selectedWallet.walletType,
        custodyModel: selectedWallet.custodyModel
      },
      fundingMethods: [
        { method: 'direct_transfer', description: `Send crypto to ${selectedWallet.address} on a supported ${selectedWallet.chainType} chain` },
        { method: 'dashboard', url: 'https://www.crossmint.com/console', description: 'Fund via Crossmint Console dashboard' },
        { method: 'bridge', services: [
          { name: 'Squid', url: 'https://app.squidrouter.com/' },
          { name: 'Relay', url: 'https://relay.link/' },
          { name: 'Across', url: 'https://app.across.to/' }
        ]}
      ]
    });
    return;
  }

  console.log(chalk.bold('Fund Crossmint Wallet'));
  console.log(chalk.gray('─'.repeat(50)));
  console.log();
  console.log(chalk.cyan('Wallet to Fund:'));
  console.log(`  Name:     ${selectedWallet.name}`);
  console.log(`  Address:  ${selectedWallet.address || 'Not available'}`);
  console.log(`  Chain:    ${selectedWallet.chainType} (${selectedWallet.walletType})`);
  console.log(`  Custody:  ${selectedWallet.custodyModel}`);
  console.log();
  console.log(chalk.bold('Funding Options:'));
  console.log();
  if (selectedWallet.address) {
    console.log('  1. ' + chalk.bold('Direct transfer:'));
    console.log(`     Send crypto to ${chalk.white(selectedWallet.address)}`);
    console.log(`     Chain type: ${selectedWallet.chainType}`);
    console.log();
  }
  console.log('  2. ' + chalk.bold('Crossmint Console Dashboard:'));
  console.log('     https://www.crossmint.com/console');
  console.log('     Log in and manage wallet balances directly');
  console.log();
  console.log('  3. ' + chalk.bold('Bridge from another chain:'));
  console.log('     - Squid: https://app.squidrouter.com/');
  console.log('     - Relay: https://relay.link/');
  console.log('     - Across: https://app.across.to/');
  console.log();
  console.log(chalk.gray('Docs: https://docs.crossmint.com/introduction/platform-overview'));
}
