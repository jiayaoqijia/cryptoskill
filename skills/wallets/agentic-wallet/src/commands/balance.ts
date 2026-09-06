import chalk from 'chalk';
import ora from 'ora';
import inquirer from 'inquirer';
import { execSync } from 'child_process';
import { listAllWallets, listCrossmintWallets, CHAIN_CONFIG } from '../utils/storage.js';
import { createPublicClient, http, formatUnits } from 'viem';
import { base, mainnet, arbitrum, optimism, polygon } from 'viem/chains';
import { isJsonMode, jsonOut, jsonError, ExitCode } from '../utils/output.js';

interface BalanceOptions {
  all?: boolean;
  provider?: string;
  json?: boolean;
  fields?: string;
}

interface WalletBalance {
  provider: string;
  name: string;
  address: string;
  chain: string;
  chainId: number;
  balanceUSDC: string;
  balanceETH: string;
  status: 'ok' | 'error';
  error?: string;
}

const USDC_ADDRESSES: Record<number, `0x${string}`> = {
  8453: '0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913',   // Base
  1: '0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48',      // Ethereum
  42161: '0xaf88d065e77c8cC2239327C5EDb3A432268e5831',  // Arbitrum
  10: '0x0b2C639c533813f4Aa9D7837CAf62653d097Ff85',     // Optimism
  137: '0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359',    // Polygon
};

const CHAINS: Record<number, typeof base | typeof mainnet | typeof arbitrum | typeof optimism | typeof polygon> = {
  8453: base,
  1: mainnet,
  42161: arbitrum,
  10: optimism,
  137: polygon,
};

export async function balanceCommand(options: BalanceOptions): Promise<void> {
  const useJson = isJsonMode(options);
  const { all, fields } = options;
  let { provider } = options;

  const results: WalletBalance[] = [];

  // If --all flag or JSON mode without provider, check all
  if (all || (useJson && !provider)) {
    if (!useJson) {
      console.log();
      console.log(chalk.bold('Unified Balance Check — All Providers'));
      console.log(chalk.gray('═'.repeat(60)));
    }

    const coinbaseResult = await checkCoinbaseBalance(useJson);
    if (coinbaseResult) results.push(coinbaseResult);

    const tempoResult = await checkTempoBalance(useJson);
    if (tempoResult) results.push(tempoResult);

    const openwalletResults = await checkOpenWalletBalances(useJson);
    results.push(...openwalletResults);

    const crossmintResult = await checkCrossmintBalance(useJson);
    if (crossmintResult) results.push(crossmintResult);

    if (useJson) {
      jsonOut(results, fields);
    } else {
      printBalanceSummary(results);
    }
    return;
  }

  // Single provider check
  if (!provider) {
    if (useJson) {
      jsonError(ExitCode.INVALID_INPUT, 'Provider required. Use --provider or --all');
    }
    const answers = await inquirer.prompt([
      {
        type: 'list',
        name: 'provider',
        message: 'Which wallet provider to check balance?',
        choices: [
          { name: 'All providers', value: 'all' },
          { name: 'Coinbase Agentic Wallet (Coinbase)', value: 'coinbase' },
          { name: 'Tempo Wallet (Stripe)', value: 'tempo' },
          { name: 'OpenWallet Standard (Moonpay)', value: 'openwallet' },
          { name: 'Crossmint Wallet (Crossmint)', value: 'crossmint' }
        ]
      }
    ]);
    provider = answers.provider;

    if (provider === 'all') {
      return balanceCommand({ all: true, json: options.json, fields });
    }
  }

  if (!useJson) {
    console.log();
    console.log(chalk.bold(`Balance Check — ${provider}`));
    console.log(chalk.gray('═'.repeat(60)));
  }

  switch (provider) {
    case 'coinbase': {
      const result = await checkCoinbaseBalance(useJson);
      if (result) results.push(result);
      break;
    }
    case 'tempo': {
      const result = await checkTempoBalance(useJson);
      if (result) results.push(result);
      break;
    }
    case 'openwallet': {
      const openwalletResults = await checkOpenWalletBalances(useJson);
      results.push(...openwalletResults);
      break;
    }
    case 'crossmint': {
      const result = await checkCrossmintBalance(useJson);
      if (result) results.push(result);
      break;
    }
  }

  if (useJson) {
    jsonOut(results, fields);
  } else {
    printBalanceSummary(results);
  }
}

async function checkCoinbaseBalance(useJson: boolean): Promise<WalletBalance | null> {
  const spinner = useJson ? null : ora('Checking Coinbase wallet...').start();

  try {
    const address = execSync('npx awal address 2>/dev/null', {
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'pipe']
    }).trim();

    if (!address || !address.startsWith('0x')) {
      spinner?.info('Coinbase: Not authenticated');
      return null;
    }

    let balanceUSDC = '0';
    try {
      const balanceOutput = execSync('npx awal balance 2>/dev/null', {
        encoding: 'utf8',
        stdio: ['pipe', 'pipe', 'pipe']
      }).trim();
      const match = balanceOutput.match(/[\d.]+/);
      if (match) balanceUSDC = match[0];
    } catch {
      // Balance command failed
    }

    spinner?.succeed(`Coinbase: ${address.slice(0, 10)}...${address.slice(-8)}`);

    return {
      provider: 'coinbase',
      name: 'Coinbase Agentic Wallet',
      address,
      chain: 'Base',
      chainId: 8453,
      balanceUSDC,
      balanceETH: 'N/A',
      status: 'ok'
    };
  } catch {
    spinner?.info('Coinbase: Not installed or not authenticated');
    return null;
  }
}

async function checkTempoBalance(useJson: boolean): Promise<WalletBalance | null> {
  const spinner = useJson ? null : ora('Checking Tempo wallet...').start();

  let tempoCmd = '';
  try {
    execSync('which tempo', { stdio: 'pipe' });
    tempoCmd = 'tempo';
  } catch {
    try {
      execSync('test -f "$HOME/.tempo/bin/tempo"', { stdio: 'pipe' });
      tempoCmd = '$HOME/.tempo/bin/tempo';
    } catch {
      spinner?.info('Tempo: Not installed');
      return null;
    }
  }

  try {
    const whoami = execSync(`${tempoCmd} wallet -t whoami 2>/dev/null`, {
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'pipe']
    });

    const addressMatch = whoami.match(/0x[a-fA-F0-9]{40}/);
    const balanceMatch = whoami.match(/balance[:\s]+(\d+\.?\d*)/i);

    if (!addressMatch) {
      spinner?.info('Tempo: Not authenticated');
      return null;
    }

    const address = addressMatch[0];
    const balanceUSDC = balanceMatch ? balanceMatch[1] : '0';

    spinner?.succeed(`Tempo: ${address.slice(0, 10)}...${address.slice(-8)}`);

    return {
      provider: 'tempo',
      name: 'Tempo Wallet (Stripe)',
      address,
      chain: 'Tempo',
      chainId: 0,
      balanceUSDC,
      balanceETH: 'N/A',
      status: 'ok'
    };
  } catch {
    spinner?.info('Tempo: Not authenticated');
    return null;
  }
}

async function checkOpenWalletBalances(useJson: boolean): Promise<WalletBalance[]> {
  const results: WalletBalance[] = [];
  const wallets = listAllWallets();

  if (wallets.length === 0) {
    if (!useJson) console.log(chalk.gray('  OpenWallet: No wallets found'));
    return results;
  }

  for (const wallet of wallets) {
    const spinner = useJson ? null : ora(`Checking OpenWallet: ${wallet.name}...`).start();

    try {
      const chain = CHAINS[wallet.chainId];
      if (!chain) {
        spinner?.warn(`OpenWallet ${wallet.name}: Unsupported chain ${wallet.chainId}`);
        results.push({
          provider: 'openwallet',
          name: wallet.name,
          address: wallet.address,
          chain: wallet.chain,
          chainId: wallet.chainId,
          balanceUSDC: 'N/A',
          balanceETH: 'N/A',
          status: 'error',
          error: 'Unsupported chain'
        });
        continue;
      }

      const client = createPublicClient({
        chain,
        transport: http()
      });

      const ethBalance = await client.getBalance({ address: wallet.address as `0x${string}` });
      const ethFormatted = formatUnits(ethBalance, 18);

      let usdcFormatted = '0';
      const usdcAddress = USDC_ADDRESSES[wallet.chainId];
      if (usdcAddress) {
        try {
          const usdcBalance = await client.readContract({
            address: usdcAddress,
            abi: [{
              name: 'balanceOf',
              type: 'function',
              stateMutability: 'view',
              inputs: [{ name: 'account', type: 'address' }],
              outputs: [{ name: '', type: 'uint256' }]
            }],
            functionName: 'balanceOf',
            args: [wallet.address as `0x${string}`]
          });
          usdcFormatted = formatUnits(usdcBalance as bigint, 6);
        } catch {
          // USDC contract call failed
        }
      }

      spinner?.succeed(`OpenWallet ${wallet.name}: ${wallet.address.slice(0, 10)}...${wallet.address.slice(-8)}`);

      results.push({
        provider: 'openwallet',
        name: wallet.name,
        address: wallet.address,
        chain: wallet.chain,
        chainId: wallet.chainId,
        balanceUSDC: usdcFormatted,
        balanceETH: ethFormatted,
        status: 'ok'
      });
    } catch (error) {
      spinner?.fail(`OpenWallet ${wallet.name}: Failed to fetch balance`);
      results.push({
        provider: 'openwallet',
        name: wallet.name,
        address: wallet.address,
        chain: wallet.chain,
        chainId: wallet.chainId,
        balanceUSDC: 'N/A',
        balanceETH: 'N/A',
        status: 'error',
        error: String(error)
      });
    }
  }

  return results;
}

async function checkCrossmintBalance(useJson: boolean): Promise<WalletBalance | null> {
  const wallets = listCrossmintWallets();

  if (wallets.length === 0) {
    if (!useJson) console.log(chalk.gray('  Crossmint: No wallets found'));
    return null;
  }

  // Return first wallet's info — for multi-wallet support, this could be expanded
  // similar to how OpenWallet returns an array
  const wallet = wallets[0];
  const spinner = useJson ? null : ora(`Checking Crossmint: ${wallet.name}...`).start();

  // For EVM custodial wallets with a valid address, try on-chain balance check
  if (wallet.chainType === 'evm' && wallet.address && wallet.address.startsWith('0x')) {
    try {
      const client = createPublicClient({
        chain: base,
        transport: http()
      });

      const ethBalance = await client.getBalance({ address: wallet.address as `0x${string}` });
      const ethFormatted = formatUnits(ethBalance, 18);

      let usdcFormatted = '0';
      const usdcAddress = USDC_ADDRESSES[8453]; // Base USDC
      if (usdcAddress) {
        try {
          const usdcBalance = await client.readContract({
            address: usdcAddress,
            abi: [{
              name: 'balanceOf',
              type: 'function',
              stateMutability: 'view',
              inputs: [{ name: 'account', type: 'address' }],
              outputs: [{ name: '', type: 'uint256' }]
            }],
            functionName: 'balanceOf',
            args: [wallet.address as `0x${string}`]
          });
          usdcFormatted = formatUnits(usdcBalance as bigint, 6);
        } catch {
          // USDC contract call failed
        }
      }

      spinner?.succeed(`Crossmint ${wallet.name}: ${wallet.address.slice(0, 10)}...${wallet.address.slice(-8)}`);

      return {
        provider: 'crossmint',
        name: wallet.name,
        address: wallet.address,
        chain: `Crossmint ${wallet.chainType}`,
        chainId: 8453,
        balanceUSDC: usdcFormatted,
        balanceETH: ethFormatted,
        status: 'ok'
      };
    } catch (error) {
      spinner?.warn(`Crossmint ${wallet.name}: On-chain balance check failed, showing wallet info`);
    }
  }

  // For non-EVM or if on-chain check failed, return basic info
  spinner?.succeed(`Crossmint ${wallet.name}: ${wallet.address ? wallet.address.slice(0, 10) + '...' + wallet.address.slice(-8) : 'address pending'}`);

  return {
    provider: 'crossmint',
    name: wallet.name,
    address: wallet.address || 'See Crossmint dashboard',
    chain: `Crossmint ${wallet.chainType}`,
    chainId: 0,
    balanceUSDC: 'Use Crossmint API for balance',
    balanceETH: 'N/A',
    status: 'ok'
  };
}

function printBalanceSummary(results: WalletBalance[]): void {
  console.log();
  console.log(chalk.bold('Balance Summary'));
  console.log(chalk.gray('─'.repeat(60)));
  console.log();

  if (results.length === 0) {
    console.log(chalk.yellow('No wallets found across any provider.'));
    console.log(chalk.gray('Setup a wallet: npx agentic-wallet setup'));
    return;
  }

  let totalUSDC = 0;

  for (const wallet of results) {
    const statusIcon = wallet.status === 'ok' ? chalk.green('✓') : chalk.red('✗');
    console.log(`${statusIcon} ${chalk.cyan(wallet.provider.toUpperCase())} — ${wallet.name}`);
    console.log(`   Address: ${wallet.address}`);
    console.log(`   Chain:   ${wallet.chain} (${wallet.chainId})`);

    if (wallet.status === 'ok') {
      const usdcNum = parseFloat(wallet.balanceUSDC) || 0;
      totalUSDC += usdcNum;
      console.log(`   USDC:    ${chalk.green(wallet.balanceUSDC)}`);
      if (wallet.balanceETH !== 'N/A') {
        console.log(`   ETH:     ${wallet.balanceETH}`);
      }
    } else {
      console.log(`   Error:   ${chalk.red(wallet.error)}`);
    }
    console.log();
  }

  console.log(chalk.gray('─'.repeat(60)));
  console.log(chalk.bold(`Total USDC across all wallets: ${chalk.green(totalUSDC.toFixed(2))}`));
  console.log();
}
