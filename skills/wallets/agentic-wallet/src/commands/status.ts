import chalk from 'chalk';
import ora from 'ora';
import inquirer from 'inquirer';
import { execSync } from 'child_process';
import { listAllWallets, listCrossmintWallets, CHAIN_CONFIG } from '../utils/storage.js';
import { isJsonMode, jsonOut, info } from '../utils/output.js';

interface StatusOptions {
  provider?: string;
  json?: boolean;
}

interface ProviderStatus {
  provider: string;
  name: string;
  status: 'authenticated' | 'not_authenticated' | 'not_installed';
  address?: string;
  balance?: string;
  wallets?: Array<{ name: string; address: string; chain: string; chainId: number; encrypted: boolean }>;
}

export async function statusWallet(options: StatusOptions): Promise<void> {
  const useJson = isJsonMode(options);
  let { provider } = options;

  // If no provider specified and interactive, prompt; otherwise default to all
  if (!provider) {
    if (useJson) {
      provider = 'all';
    } else {
      const { checkAll } = await inquirer.prompt([
        {
          type: 'list',
          name: 'checkAll',
          message: 'Which wallet provider to check?',
          choices: [
            { name: 'All providers', value: 'all' },
            { name: 'Coinbase Agentic Wallet (Coinbase)', value: 'coinbase' },
            { name: 'Tempo Wallet (Stripe)', value: 'tempo' },
            { name: 'OpenWallet Standard (Moonpay)', value: 'openwallet' },
            { name: 'Crossmint Wallet (Crossmint)', value: 'crossmint' }
          ]
        }
      ]);
      provider = checkAll;
    }
  }

  const results: ProviderStatus[] = [];

  if (provider === 'all' || provider === 'coinbase') {
    results.push(await getCoinbaseStatus(useJson));
  }
  if (provider === 'all' || provider === 'tempo') {
    results.push(await getTempoStatus(useJson));
  }
  if (provider === 'all' || provider === 'openwallet') {
    results.push(await getOpenWalletStatus(useJson));
  }
  if (provider === 'all' || provider === 'crossmint') {
    results.push(await getCrossmintStatus(useJson));
  }

  if (useJson) {
    jsonOut({ ok: true, providers: results });
    return;
  }

  // Human output
  console.log();
  console.log(chalk.bold('Wallet Status'));
  console.log(chalk.gray('═'.repeat(60)));

  for (const r of results) {
    console.log();
    console.log(chalk.cyan.bold(r.name));
    console.log(chalk.gray('─'.repeat(40)));

    if (r.status === 'not_installed') {
      console.log(`  Status:  ${chalk.gray('○ Not installed')}`);
    } else if (r.status === 'not_authenticated') {
      console.log(`  Status:  ${chalk.yellow('○ Not authenticated')}`);
    } else {
      console.log(`  Status:  ${chalk.green('✓ Authenticated')}`);
      if (r.address) console.log(`  Address: ${r.address}`);
      if (r.balance) console.log(`  Balance: ${r.balance}`);
    }

    if (r.wallets && r.wallets.length > 0) {
      console.log(`  Status:  ${chalk.green(`✓ ${r.wallets.length} wallet(s) found`)}`);
      console.log();
      for (const w of r.wallets) {
        const encrypted = w.encrypted ? chalk.green('🔒') : chalk.yellow('🔓');
        console.log(`  ${encrypted} ${chalk.white(w.name)}`);
        console.log(`     Address: ${w.address}`);
        console.log(`     Chain:   ${w.chain} (${w.chainId})`);
      }
      console.log();
      console.log(chalk.gray('  Storage: ~/.agent-arena/wallets/'));
    }
  }

  console.log(chalk.gray('═'.repeat(60)));
  console.log();
  console.log(chalk.gray('Note: Agent Arena does NOT have access to any of these wallets.'));
  console.log(chalk.gray('All data is stored locally or with your chosen provider.'));
}

async function getCoinbaseStatus(useJson: boolean): Promise<ProviderStatus> {
  const result: ProviderStatus = { provider: 'coinbase', name: 'Coinbase Agentic Wallet', status: 'not_installed' };

  try {
    const status = execSync('npx awal status 2>/dev/null', {
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'pipe']
    });

    const isAuthenticated = !status.includes('Not authenticated') &&
                           (status.includes('✓') || status.includes('Authenticated'));

    if (isAuthenticated) {
      result.status = 'authenticated';
      try {
        const address = execSync('npx awal address 2>/dev/null', {
          encoding: 'utf8',
          stdio: ['pipe', 'pipe', 'pipe']
        }).trim();
        if (address && address.startsWith('0x')) result.address = address;
      } catch { /* no address */ }

      try {
        const balance = execSync('npx awal balance 2>/dev/null', {
          encoding: 'utf8',
          stdio: ['pipe', 'pipe', 'pipe']
        }).trim();
        if (balance) result.balance = balance;
      } catch { /* no balance */ }
    } else {
      result.status = 'not_authenticated';
    }
  } catch {
    result.status = 'not_installed';
  }

  return result;
}

async function getTempoStatus(useJson: boolean): Promise<ProviderStatus> {
  const result: ProviderStatus = { provider: 'tempo', name: 'Tempo Wallet (Stripe)', status: 'not_installed' };

  let tempoCmd = '';
  try {
    execSync('which tempo', { stdio: 'pipe' });
    tempoCmd = 'tempo';
  } catch {
    try {
      execSync('test -f "$HOME/.tempo/bin/tempo"', { stdio: 'pipe' });
      tempoCmd = '$HOME/.tempo/bin/tempo';
    } catch {
      return result;
    }
  }

  try {
    const whoami = execSync(`${tempoCmd} wallet -t whoami 2>/dev/null`, {
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'pipe']
    });

    if (whoami.includes('0x')) {
      result.status = 'authenticated';
      const addressMatch = whoami.match(/0x[a-fA-F0-9]{40}/);
      if (addressMatch) result.address = addressMatch[0];
      const balanceMatch = whoami.match(/balance[:\s]+(\d+\.?\d*)/i);
      if (balanceMatch) result.balance = balanceMatch[1] + ' USDC';
    } else {
      result.status = 'not_authenticated';
    }
  } catch {
    result.status = 'not_authenticated';
  }

  return result;
}

async function getOpenWalletStatus(useJson: boolean): Promise<ProviderStatus> {
  const result: ProviderStatus = { provider: 'openwallet', name: 'OpenWallet Standard (Moonpay)', status: 'authenticated' };

  const wallets = listAllWallets();

  if (wallets.length === 0) {
    result.status = 'not_authenticated';
    return result;
  }

  result.wallets = wallets.map(w => ({
    name: w.name,
    address: w.address,
    chain: w.chain,
    chainId: w.chainId,
    encrypted: w.encrypted
  }));

  return result;
}

async function getCrossmintStatus(useJson: boolean): Promise<ProviderStatus> {
  const result: ProviderStatus = { provider: 'crossmint', name: 'Crossmint Wallet', status: 'not_authenticated' };

  // Check for locally stored Crossmint wallets first
  const wallets = listCrossmintWallets();

  if (wallets.length > 0) {
    result.status = 'authenticated';
    result.wallets = wallets.map(w => ({
      name: w.name,
      address: w.address,
      chain: `${w.chainType} (${w.walletType})`,
      chainId: 0,
      encrypted: false
    }));
    return result;
  }

  // No local wallets — check if Crossmint CLI is installed and authenticated
  try {
    execSync('crossmint --version', { stdio: 'pipe' });
  } catch {
    result.status = 'not_installed';
    return result;
  }

  try {
    const whoami = execSync('crossmint whoami 2>/dev/null', {
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'pipe']
    });

    if (whoami && !whoami.includes('not logged in') && !whoami.includes('Not logged in')) {
      result.status = 'authenticated';
      const emailMatch = whoami.match(/[\w.-]+@[\w.-]+\.\w+/);
      if (emailMatch) result.address = emailMatch[0];
    } else {
      result.status = 'not_authenticated';
    }
  } catch {
    result.status = 'not_authenticated';
  }

  return result;
}
