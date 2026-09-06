import chalk from 'chalk';
import ora from 'ora';
import inquirer from 'inquirer';
import { execSync, spawn } from 'child_process';
import { readFileSync, existsSync } from 'fs';
import { generatePrivateKey, privateKeyToAccount } from 'viem/accounts';
import { v4 as uuidv4 } from 'uuid';
import {
  walletExists,
  saveWalletExclusive,
  encryptPrivateKey,
  validateWalletName,
  safePasswordEqual,
  CHAIN_CONFIG,
  saveCrossmintWallet,
  crossmintWalletExists,
  CROSSMINT_CHAIN_TYPES,
  type StoredWallet,
  type CrossmintWalletRecord,
  type CrossmintChainType
} from '../utils/storage.js';
import { isJsonMode, jsonOut, jsonError, ExitCode } from '../utils/output.js';

interface SetupOptions {
  provider?: string;
  chain?: string;
  name?: string;
  passwordFile?: string;
  apiKeyFile?: string;
  chainType?: string;
  walletType?: string;
  nonInteractive?: boolean;
  json?: boolean;
}

const PROVIDERS = ['coinbase', 'tempo', 'openwallet', 'crossmint'] as const;
type Provider = typeof PROVIDERS[number];

export async function setupWallet(options: SetupOptions): Promise<void> {
  const useJson = isJsonMode(options);
  let { provider, chain = 'base', name = 'default', passwordFile, nonInteractive } = options;

  if (!useJson) {
    console.log();
    console.log(chalk.bold('🔐 Agent Wallet Setup'));
    console.log(chalk.gray('─'.repeat(50)));
    console.log();
    console.log(chalk.white('Agent Arena does NOT store your keys.'));
    console.log(chalk.white('All wallet data stays on YOUR machine or with YOUR provider.'));
    console.log();
  }

  // Non-interactive mode validation
  if (nonInteractive) {
    if (!provider) {
      if (useJson) jsonError(ExitCode.INVALID_INPUT, '--provider is required in non-interactive mode');
      console.error(chalk.red('✗ --provider is required in non-interactive mode'));
      process.exit(ExitCode.INVALID_INPUT);
    }
    if (provider === 'openwallet' && !passwordFile) {
      if (useJson) jsonError(ExitCode.INVALID_INPUT, '--password-file is required for openwallet in non-interactive mode');
      console.error(chalk.red('✗ --password-file is required for openwallet in non-interactive mode'));
      process.exit(ExitCode.INVALID_INPUT);
    }
    if (provider === 'crossmint' && !options.apiKeyFile) {
      if (useJson) jsonError(ExitCode.INVALID_INPUT, '--api-key-file is required for crossmint in non-interactive mode');
      console.error(chalk.red('✗ --api-key-file is required for crossmint in non-interactive mode'));
      process.exit(ExitCode.INVALID_INPUT);
    }
  }

  // Provider selection if not specified
  if (!provider) {
    if (useJson) jsonError(ExitCode.INVALID_INPUT, '--provider is required in JSON/piped mode');
    const answers = await inquirer.prompt([
      {
        type: 'list',
        name: 'provider',
        message: 'Select wallet provider:',
        choices: [
          {
            name: 'Coinbase Agentic Wallet (Coinbase) — Managed, compliant, x402 native',
            value: 'coinbase'
          },
          {
            name: 'Tempo Wallet (Stripe) — Fast payments, service discovery, passkey auth',
            value: 'tempo'
          },
          {
            name: 'OpenWallet Standard (Moonpay) — Self-custody, policy-gated signing',
            value: 'openwallet'
          },
          {
            name: 'Crossmint Wallet (Crossmint) — API-first, 50+ chains, custodial or non-custodial',
            value: 'crossmint'
          }
        ]
      }
    ]);
    provider = answers.provider;
  }

  // Validate provider
  if (!PROVIDERS.includes(provider as Provider)) {
    if (useJson) jsonError(ExitCode.INVALID_INPUT, `Unknown provider: ${provider}`, { validProviders: [...PROVIDERS] });
    console.error(chalk.red(`✗ Unknown provider: ${provider}`));
    console.log(chalk.gray(`Valid providers: ${PROVIDERS.join(', ')}`));
    process.exit(ExitCode.INVALID_INPUT);
  }

  if (!useJson) {
    console.log();
    console.log(chalk.cyan(`Setting up ${provider} wallet...`));
    console.log();
  }

  switch (provider) {
    case 'coinbase':
      await setupCoinbase(useJson);
      break;
    case 'tempo':
      await setupTempo(useJson);
      break;
    case 'openwallet':
      await setupOpenWallet(name, chain, useJson, passwordFile, nonInteractive);
      break;
    case 'crossmint':
      await setupCrossmint(name, useJson, options.apiKeyFile, options.chainType, options.walletType, nonInteractive);
      break;
  }
}

async function setupCoinbase(useJson: boolean): Promise<void> {
  if (!useJson) {
    console.log(chalk.bold('Coinbase Agentic Wallet Setup'));
    console.log(chalk.gray('─'.repeat(50)));
    console.log();
    console.log('This will use the Coinbase awal CLI to create your wallet.');
    console.log('Your keys are stored in Coinbase infrastructure — never on Agent Arena servers.');
    console.log();
  }

  // Check if awal is available
  const spinner = useJson ? null : ora('Checking for Coinbase awal CLI...').start();

  try {
    execSync('npx awal --version', { stdio: 'pipe' });
    spinner?.succeed('Coinbase awal CLI available');
  } catch {
    spinner?.info('Installing Coinbase awal skills...');
    if (useJson) {
      jsonError(ExitCode.PROVIDER_NOT_INSTALLED, 'Coinbase awal CLI not installed', {
        installCommand: 'npx skills add coinbase/agentic-wallet-skills'
      });
    }
    console.log();
    console.log(chalk.yellow('Run the following command to install:'));
    console.log();
    console.log(chalk.white('  npx skills add coinbase/agentic-wallet-skills'));
    console.log();
    console.log(chalk.gray('After installation, authenticate with:'));
    console.log(chalk.white('  npx awal auth login your-email@example.com'));
    console.log();
    process.exit(ExitCode.PROVIDER_NOT_INSTALLED);
    return;
  }

  // Prompt for email
  const { email } = await inquirer.prompt([
    {
      type: 'input',
      name: 'email',
      message: 'Enter your email for Coinbase authentication:',
      validate: (input: string) => {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(input) || 'Please enter a valid email';
      }
    }
  ]);

  if (!useJson) {
    console.log();
    console.log(chalk.cyan('Starting Coinbase authentication...'));
    console.log(chalk.gray('You will receive a 6-digit OTP via email.'));
    console.log();
  }

  // Run awal auth login
  try {
    const child = spawn('npx', ['awal', 'auth', 'login', email], {
      stdio: 'inherit',
      shell: true
    });

    child.on('close', (code) => {
      if (code === 0) {
        if (useJson) {
          jsonOut({ ok: true, provider: 'coinbase', email, message: 'OTP sent. Run: npx awal auth verify <flowId> <otp>' });
        } else {
          console.log();
          console.log(chalk.green('✓ Coinbase wallet setup initiated!'));
          console.log();
          console.log(chalk.bold('Next steps:'));
          console.log('  1. Check your email for the OTP');
          console.log('  2. Run: npx awal auth verify <flowId> <otp>');
          console.log('  3. Check status: npx awal status');
          console.log('  4. Get address: npx awal address');
        }
      }
    });
  } catch (error) {
    if (useJson) jsonError(ExitCode.GENERAL_ERROR, 'Failed to start Coinbase authentication');
    console.error(chalk.red('Failed to start Coinbase authentication'));
    console.error(error);
  }
}

async function setupTempo(useJson: boolean): Promise<void> {
  if (!useJson) {
    console.log(chalk.bold('Tempo Wallet Setup'));
    console.log(chalk.gray('─'.repeat(50)));
    console.log();
    console.log('This will use the Tempo CLI to create your wallet.');
    console.log('Your keys are stored locally with passkey authentication.');
    console.log();
  }

  const spinner = useJson ? null : ora('Checking for Tempo CLI...').start();

  // Check if tempo is installed
  let tempoPath = '';
  try {
    execSync('which tempo', { stdio: 'pipe' });
    tempoPath = 'tempo';
    spinner?.succeed('Tempo CLI found');
  } catch {
    try {
      execSync('test -f "$HOME/.tempo/bin/tempo"', { stdio: 'pipe' });
      tempoPath = '"$HOME/.tempo/bin/tempo"';
      spinner?.succeed('Tempo CLI found at ~/.tempo/bin/tempo');
    } catch {
      spinner?.info('Tempo CLI not found. Installing...');
      if (useJson) {
        jsonError(ExitCode.PROVIDER_NOT_INSTALLED, 'Tempo CLI not installed', {
          installCommand: 'curl -fsSL https://tempo.xyz/install | bash'
        });
      }
      console.log();
      console.log(chalk.yellow('Run the following command to install Tempo:'));
      console.log();
      console.log(chalk.white('  curl -fsSL https://tempo.xyz/install | bash'));
      console.log();
      process.exit(ExitCode.PROVIDER_NOT_INSTALLED);
      return;
    }
  }

  if (!useJson) {
    console.log();
    console.log(chalk.cyan('Starting Tempo wallet login...'));
    console.log(chalk.yellow('⚠ This will open a browser for passkey authentication.'));
    console.log(chalk.gray('  (This may take up to 16 minutes for agent workflows)'));
    console.log();
  }

  const { proceed } = await inquirer.prompt([
    {
      type: 'confirm',
      name: 'proceed',
      message: 'Ready to open browser for authentication?',
      default: true
    }
  ]);

  if (!proceed) {
    if (useJson) jsonOut({ ok: false, provider: 'tempo', message: 'Setup cancelled by user' });
    else console.log(chalk.gray('Setup cancelled.'));
    return;
  }

  try {
    const child = spawn(tempoPath, ['wallet', 'login'], {
      stdio: 'inherit',
      shell: true
    });

    child.on('close', (code) => {
      if (code === 0) {
        if (useJson) {
          jsonOut({ ok: true, provider: 'tempo', message: 'Tempo wallet setup complete' });
        } else {
          console.log();
          console.log(chalk.green('✓ Tempo wallet setup complete!'));
          console.log();
          console.log(chalk.bold('Next steps:'));
          console.log('  1. Check status: tempo wallet -t whoami');
          console.log('  2. Fund wallet: tempo wallet fund');
          console.log('  3. Discover services: tempo wallet -t services --search ai');
        }
      }
    });
  } catch (error) {
    if (useJson) jsonError(ExitCode.GENERAL_ERROR, 'Failed to start Tempo authentication');
    console.error(chalk.red('Failed to start Tempo authentication'));
    console.error(error);
  }
}

async function setupOpenWallet(name: string, chain: string, useJson: boolean, passwordFile?: string, nonInteractive?: boolean): Promise<void> {
  if (!useJson) {
    console.log(chalk.bold('OpenWallet Standard Setup (by Moonpay)'));
    console.log(chalk.gray('─'.repeat(50)));
    console.log();
    console.log('This creates an encrypted MoonPay local wallet stored on YOUR local filesystem.');
    console.log('Agent Arena has NO access to your keys — they never leave your machine.');
    console.log();
    console.log(chalk.gray(`Storage location: ~/.agent-arena/wallets/${name}.json`));
    console.log();
  }

  // Validate wallet name (path traversal prevention)
  try {
    validateWalletName(name);
  } catch (err: any) {
    if (useJson) jsonError(ExitCode.INVALID_INPUT, err.message);
    console.error(chalk.red(`✗ ${err.message}`));
    process.exit(ExitCode.INVALID_INPUT);
  }

  // Validate chain
  if (!CHAIN_CONFIG[chain]) {
    if (useJson) jsonError(ExitCode.INVALID_INPUT, `Unknown chain: ${chain}`, { supportedChains: Object.keys(CHAIN_CONFIG) });
    console.error(chalk.red(`✗ Unknown chain: ${chain}`));
    console.log(chalk.gray(`Supported chains: ${Object.keys(CHAIN_CONFIG).join(', ')}`));
    process.exit(ExitCode.INVALID_INPUT);
  }

  // Check if wallet exists
  if (walletExists(name)) {
    if (useJson) jsonError(ExitCode.ALREADY_EXISTS, `Wallet "${name}" already exists`);
    console.error(chalk.red(`✗ Wallet "${name}" already exists`));
    console.log(chalk.gray('Use a different name or delete the existing wallet first'));
    process.exit(ExitCode.ALREADY_EXISTS);
  }

  let password: string;

  // Get password from file or prompt
  if (passwordFile) {
    if (!existsSync(passwordFile)) {
      if (useJson) jsonError(ExitCode.INVALID_INPUT, `Password file not found: ${passwordFile}`);
      console.error(chalk.red(`✗ Password file not found: ${passwordFile}`));
      process.exit(ExitCode.INVALID_INPUT);
    }
    password = readFileSync(passwordFile, 'utf8').trim();
    if (password.length < 8) {
      if (useJson) jsonError(ExitCode.INVALID_INPUT, 'Password in file must be at least 8 characters');
      console.error(chalk.red('✗ Password in file must be at least 8 characters'));
      process.exit(ExitCode.INVALID_INPUT);
    }
    if (!useJson) console.log(chalk.gray('Using password from file (not displayed for security)'));
  } else if (nonInteractive) {
    if (useJson) jsonError(ExitCode.INVALID_INPUT, '--password-file is required in non-interactive mode');
    console.error(chalk.red('✗ --password-file is required in non-interactive mode'));
    process.exit(ExitCode.INVALID_INPUT);
  } else {
    // Interactive: prompt for password
    const answers = await inquirer.prompt([
      {
        type: 'password',
        name: 'password',
        message: 'Enter encryption password (min 8 chars):',
        mask: '*',
        validate: (input: string) => input.length >= 8 || 'Password must be at least 8 characters'
      },
      {
        type: 'password',
        name: 'confirmPassword',
        message: 'Confirm password:',
        mask: '*'
      }
    ]);

    if (!safePasswordEqual(answers.password, answers.confirmPassword)) {
      if (useJson) jsonError(ExitCode.INVALID_INPUT, 'Passwords do not match');
      console.error(chalk.red('✗ Passwords do not match'));
      process.exit(ExitCode.INVALID_INPUT);
    }
    password = answers.password;
  }

  const spinner = useJson ? null : ora('Generating wallet...').start();

  try {
    // Generate new wallet
    const privateKey = generatePrivateKey();
    const account = privateKeyToAccount(privateKey);
    const chainConfig = CHAIN_CONFIG[chain];

    // Encrypt private key
    const { encrypted, iv, salt, authTag } = encryptPrivateKey(privateKey, password);

    const wallet: StoredWallet = {
      id: uuidv4(),
      name,
      address: account.address,
      chainId: chainConfig.chainId,
      chain: chainConfig.name,
      createdAt: new Date().toISOString(),
      encrypted: true,
      encryptedPrivateKey: encrypted,
      iv,
      salt,
      authTag
    };

    // Save wallet atomically (prevents TOCTOU race condition)
    const saved = saveWalletExclusive(wallet);
    if (!saved) {
      spinner?.fail(chalk.red('Wallet already exists (race condition)'));
      if (useJson) jsonError(ExitCode.ALREADY_EXISTS, `Wallet "${name}" already exists`);
      process.exit(ExitCode.ALREADY_EXISTS);
    }

    spinner?.succeed(chalk.green('Wallet created successfully!'));

    if (useJson) {
      jsonOut({
        ok: true,
        provider: 'openwallet',
        name,
        address: account.address,
        chain: chainConfig.name,
        chainId: chainConfig.chainId,
        accountId: `eip155:${chainConfig.chainId}:${account.address}`,
        storagePath: `~/.agent-arena/wallets/${name}.json`
      });
    } else {
      console.log();
      console.log(chalk.bold('Wallet Details:'));
      console.log(chalk.gray('─'.repeat(50)));
      console.log(`  ${chalk.cyan('Name:')}      ${name}`);
      console.log(`  ${chalk.cyan('Address:')}   ${account.address}`);
      console.log(`  ${chalk.cyan('Chain:')}     ${chainConfig.name} (${chainConfig.chainId})`);
      console.log(`  ${chalk.cyan('Encrypted:')} ${chalk.green('Yes')}`);
      console.log(chalk.gray('─'.repeat(50)));
      console.log();
      console.log(chalk.bold('CAIP-10 Account ID:'));
      console.log(`  eip155:${chainConfig.chainId}:${account.address}`);
      console.log();
      console.log(chalk.bold('Security:'));
      console.log(chalk.white('  ✓ Private key encrypted with AES-256-GCM'));
      console.log(chalk.white('  ✓ Stored ONLY at: ~/.agent-arena/wallets/' + name + '.json'));
      console.log(chalk.white('  ✓ Agent Arena has ZERO access to your keys'));
      console.log();
      console.log(chalk.bold('Next steps:'));
      console.log(`  1. Fund your wallet with USDC on ${chainConfig.name}`);
      console.log('  2. Register with Agent Arena: POST /api/register');
      console.log('  3. Use for x402 payments');
    }

  } catch (error) {
    spinner?.fail(chalk.red('Failed to create wallet'));
    if (useJson) jsonError(ExitCode.GENERAL_ERROR, 'Failed to create wallet');
    console.error(error);
    process.exit(ExitCode.GENERAL_ERROR);
  }
}

async function setupCrossmint(
  name: string,
  useJson: boolean,
  apiKeyFile?: string,
  chainType?: string,
  walletType?: string,
  nonInteractive?: boolean
): Promise<void> {
  if (!useJson) {
    console.log(chalk.bold('Crossmint Wallet Setup'));
    console.log(chalk.gray('─'.repeat(50)));
    console.log();
    console.log('Crossmint supports custodial and non-custodial wallets on 50+ chains.');
    console.log();
  }

  // Validate wallet name
  try {
    validateWalletName(name);
  } catch (err: any) {
    if (useJson) jsonError(ExitCode.INVALID_INPUT, err.message);
    console.error(chalk.red(`✗ ${err.message}`));
    process.exit(ExitCode.INVALID_INPUT);
  }

  // Check if this wallet name already exists locally
  if (crossmintWalletExists(name)) {
    if (useJson) jsonError(ExitCode.ALREADY_EXISTS, `Crossmint wallet "${name}" already exists locally`);
    console.error(chalk.red(`✗ Crossmint wallet "${name}" already exists locally`));
    process.exit(ExitCode.ALREADY_EXISTS);
  }

  // --- Determine mode: non-interactive (API key) vs interactive (browser login) ---

  if (nonInteractive || apiKeyFile) {
    // ═══════════════════════════════════════════════════
    // NON-INTERACTIVE MODE — API key from file, no browser
    // Creates a custodial wallet via Crossmint REST API
    // ═══════════════════════════════════════════════════
    await setupCrossmintNonInteractive(name, useJson, apiKeyFile, chainType, walletType);
  } else {
    // ═══════════════════════════════════════════════════
    // INTERACTIVE MODE — browser login + prompted wallet creation
    // Supports both custodial and non-custodial
    // ═══════════════════════════════════════════════════
    await setupCrossmintInteractive(name, useJson, chainType, walletType);
  }
}

/**
 * Non-interactive Crossmint setup.
 * Reads API key from file, creates a custodial wallet via REST API.
 * No browser or user interaction required — ideal for autonomous agents.
 */
async function setupCrossmintNonInteractive(
  name: string,
  useJson: boolean,
  apiKeyFile?: string,
  chainType?: string,
  walletType?: string
): Promise<void> {
  // Read API key from file
  if (!apiKeyFile) {
    if (useJson) jsonError(ExitCode.INVALID_INPUT, '--api-key-file is required for non-interactive Crossmint setup');
    console.error(chalk.red('✗ --api-key-file is required for non-interactive Crossmint setup'));
    process.exit(ExitCode.INVALID_INPUT);
  }

  if (!existsSync(apiKeyFile)) {
    if (useJson) jsonError(ExitCode.INVALID_INPUT, `API key file not found: ${apiKeyFile}`);
    console.error(chalk.red(`✗ API key file not found: ${apiKeyFile}`));
    process.exit(ExitCode.INVALID_INPUT);
  }

  const apiKey = readFileSync(apiKeyFile, 'utf8').trim();
  if (!apiKey || apiKey.length < 10) {
    if (useJson) jsonError(ExitCode.INVALID_INPUT, 'API key file appears to be empty or invalid');
    console.error(chalk.red('✗ API key file appears to be empty or invalid'));
    process.exit(ExitCode.INVALID_INPUT);
  }

  // Default to EVM smart wallet if not specified
  const selectedChainType = chainType || 'evm';
  const selectedWalletType = walletType || 'smart';

  // Validate chain type
  if (!CROSSMINT_CHAIN_TYPES.includes(selectedChainType as any)) {
    if (useJson) jsonError(ExitCode.INVALID_INPUT, `Invalid chain type: ${selectedChainType}`, { validChainTypes: [...CROSSMINT_CHAIN_TYPES] });
    console.error(chalk.red(`✗ Invalid chain type: ${selectedChainType}`));
    console.log(chalk.gray(`Valid chain types: ${CROSSMINT_CHAIN_TYPES.join(', ')}`));
    process.exit(ExitCode.INVALID_INPUT);
  }

  const spinner = useJson ? null : ora('Creating Crossmint wallet via API...').start();

  try {
    // Build request body — custodial wallet with API key as admin signer
    const requestBody: Record<string, any> = {
      chainType: selectedChainType,
      type: selectedWalletType,
      config: {
        adminSigner: {
          type: 'api-key'
        }
      }
    };

    // Use production API
    const apiUrl = 'https://www.crossmint.com/api/2025-06-09/wallets';

    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'X-API-KEY': apiKey,
        'Content-Type': 'application/json',
        'x-idempotency-key': `agentic-wallet-${name}-${Date.now()}`
      },
      body: JSON.stringify(requestBody)
    });

    if (!response.ok) {
      const errorBody = await response.text();
      let errorMsg = `Crossmint API error (${response.status})`;
      try {
        const parsed = JSON.parse(errorBody);
        errorMsg = parsed.message || parsed.error || errorMsg;
      } catch {
        errorMsg = errorBody || errorMsg;
      }
      spinner?.fail(chalk.red('Failed to create Crossmint wallet'));
      if (useJson) jsonError(ExitCode.GENERAL_ERROR, errorMsg, { statusCode: response.status });
      console.error(chalk.red(`✗ ${errorMsg}`));
      process.exit(ExitCode.GENERAL_ERROR);
    }

    const walletData = await response.json() as Record<string, any>;

    // Normalize createdAt — API may return Unix timestamp (number) or ISO string
    let createdAt: string;
    if (typeof walletData.createdAt === 'number') {
      createdAt = new Date(walletData.createdAt).toISOString();
    } else {
      createdAt = walletData.createdAt || new Date().toISOString();
    }

    // Save wallet record locally
    const walletRecord: CrossmintWalletRecord = {
      id: walletData.address || uuidv4(),
      name,
      address: walletData.address,
      chainType: walletData.chainType || selectedChainType,
      walletType: walletData.type || selectedWalletType,
      custodyModel: 'custodial',
      createdAt,
      crossmintLocator: walletData.owner
    };

    const saved = saveCrossmintWallet(walletRecord);
    if (!saved) {
      spinner?.fail(chalk.red('Wallet already exists locally (race condition)'));
      if (useJson) jsonError(ExitCode.ALREADY_EXISTS, `Wallet "${name}" already exists locally`);
      process.exit(ExitCode.ALREADY_EXISTS);
    }

    spinner?.succeed(chalk.green('Crossmint wallet created successfully!'));

    if (useJson) {
      jsonOut({
        ok: true,
        provider: 'crossmint',
        name,
        address: walletRecord.address,
        chainType: walletRecord.chainType,
        walletType: walletRecord.walletType,
        custodyModel: walletRecord.custodyModel,
        createdAt: walletRecord.createdAt,
        storagePath: `~/.agent-arena/crossmint-wallets/${name}.json`
      });
    } else {
      console.log();
      console.log(chalk.bold('Wallet Details:'));
      console.log(chalk.gray('─'.repeat(50)));
      console.log(`  ${chalk.cyan('Name:')}          ${name}`);
      console.log(`  ${chalk.cyan('Address:')}       ${walletRecord.address}`);
      console.log(`  ${chalk.cyan('Chain Type:')}    ${walletRecord.chainType}`);
      console.log(`  ${chalk.cyan('Wallet Type:')}   ${walletRecord.walletType}`);
      console.log(`  ${chalk.cyan('Custody:')}       ${chalk.green('Custodial (API-key signer)')}`);
      console.log(chalk.gray('─'.repeat(50)));
      console.log();
      console.log(chalk.bold('Security:'));
      console.log(chalk.white('  ✓ Keys managed by Crossmint infrastructure'));
      console.log(chalk.white('  ✓ API key controls wallet operations'));
      console.log(chalk.white('  ✓ Wallet record stored at: ~/.agent-arena/crossmint-wallets/' + name + '.json'));
      console.log(chalk.white('  ✓ Agent Arena has ZERO access to your keys'));
      console.log();
      console.log(chalk.bold('Next steps:'));
      console.log('  1. Fund wallet: npx agentic-wallet fund --provider crossmint');
      console.log('  2. Check balance: npx agentic-wallet balance --provider crossmint');
      console.log();
      console.log(chalk.gray('Docs: https://docs.crossmint.com/introduction/platform-overview'));
    }

  } catch (error: any) {
    spinner?.fail(chalk.red('Failed to create Crossmint wallet'));
    const errorMsg = error.cause?.code === 'ENOTFOUND'
      ? 'Network error: cannot reach Crossmint API'
      : error.message || String(error);
    if (useJson) jsonError(ExitCode.GENERAL_ERROR, errorMsg);
    console.error(chalk.red(`✗ ${errorMsg}`));
    process.exit(ExitCode.GENERAL_ERROR);
  }
}

/**
 * Interactive Crossmint setup.
 * Authenticates via browser (Crossmint CLI), then prompts for wallet config
 * and creates the wallet via API. Supports custodial + non-custodial.
 */
async function setupCrossmintInteractive(
  name: string,
  useJson: boolean,
  chainType?: string,
  walletType?: string
): Promise<void> {
  // Step 1: Check if Crossmint CLI is installed (needed for login)
  const spinner = useJson ? null : ora('Checking for Crossmint CLI...').start();

  let crossmintInstalled = false;
  try {
    execSync('crossmint --version', { stdio: 'pipe' });
    crossmintInstalled = true;
    spinner?.succeed('Crossmint CLI available');
  } catch {
    spinner?.info('Crossmint CLI not found');
  }

  if (!crossmintInstalled) {
    if (useJson) {
      jsonError(ExitCode.PROVIDER_NOT_INSTALLED, 'Crossmint CLI not installed', {
        installCommand: 'npm install -g @crossmint/cli'
      });
    }
    console.log();
    console.log(chalk.yellow('The Crossmint CLI is needed for interactive login.'));
    console.log(chalk.yellow('Install it with one of these commands:'));
    console.log();
    console.log(chalk.white('  npm install -g @crossmint/cli'));
    console.log(chalk.white('  brew tap crossmint/tap && brew install crossmint'));
    console.log();
    console.log(chalk.gray('Alternatively, use non-interactive mode with an API key:'));
    console.log(chalk.white('  npx agentic-wallet setup --provider crossmint --api-key-file <path> --non-interactive'));
    console.log();
    process.exit(ExitCode.PROVIDER_NOT_INSTALLED);
    return;
  }

  // Step 2: Check if already logged in
  let alreadyLoggedIn = false;
  try {
    const whoami = execSync('crossmint whoami 2>/dev/null', {
      encoding: 'utf8',
      stdio: ['pipe', 'pipe', 'pipe']
    });
    if (whoami && !whoami.includes('not logged in') && !whoami.includes('Not logged in')) {
      alreadyLoggedIn = true;
      if (!useJson) {
        console.log();
        console.log(chalk.green('✓ Already authenticated with Crossmint'));
        console.log(chalk.gray(whoami.trim()));
      }
    }
  } catch {
    // Not logged in
  }

  // Step 3: Login if needed
  if (!alreadyLoggedIn) {
    if (!useJson) {
      console.log();
      console.log(chalk.cyan('Starting Crossmint authentication...'));
      console.log(chalk.yellow('⚠ This will open a browser for device authorization.'));
      console.log();
    }

    const { proceed } = await inquirer.prompt([
      {
        type: 'confirm',
        name: 'proceed',
        message: 'Ready to open browser for Crossmint authentication?',
        default: true
      }
    ]);

    if (!proceed) {
      if (useJson) jsonOut({ ok: false, provider: 'crossmint', message: 'Setup cancelled by user' });
      else console.log(chalk.gray('Setup cancelled.'));
      return;
    }

    // Wait for login to complete
    try {
      await new Promise<void>((resolve, reject) => {
        const child = spawn('crossmint', ['login', '--env', 'production'], {
          stdio: 'inherit',
          shell: true
        });
        child.on('close', (code) => {
          if (code === 0) resolve();
          else reject(new Error('Crossmint authentication failed'));
        });
        child.on('error', reject);
      });
    } catch (error) {
      if (useJson) jsonError(ExitCode.GENERAL_ERROR, 'Crossmint authentication failed');
      console.error(chalk.red('✗ Crossmint authentication failed'));
      process.exit(ExitCode.GENERAL_ERROR);
    }

    console.log();
    console.log(chalk.green('✓ Crossmint authentication complete!'));
  }

  // Step 4: Prompt for wallet configuration
  console.log();

  let selectedChainType = chainType;
  let selectedWalletType = walletType;
  let custodyModel: 'custodial' | 'non-custodial' = 'custodial';

  if (!selectedChainType) {
    const { chain } = await inquirer.prompt([
      {
        type: 'list',
        name: 'chain',
        message: 'Select chain type:',
        choices: [
          { name: 'EVM (Ethereum, Base, Polygon, Arbitrum, Optimism, etc.)', value: 'evm' },
          { name: 'Solana', value: 'solana' },
          { name: 'Aptos', value: 'aptos' },
          { name: 'Sui', value: 'sui' },
          { name: 'Stellar', value: 'stellar' }
        ]
      }
    ]);
    selectedChainType = chain;
  }

  if (!selectedWalletType) {
    const { wtype } = await inquirer.prompt([
      {
        type: 'list',
        name: 'wtype',
        message: 'Select wallet type:',
        choices: [
          { name: 'Smart Wallet (recommended — default for most chains)', value: 'smart' },
          { name: 'MPC Wallet (multi-party computation)', value: 'mpc' }
        ]
      }
    ]);
    selectedWalletType = wtype;
  }

  const { custody } = await inquirer.prompt([
    {
      type: 'list',
      name: 'custody',
      message: 'Select custody model:',
      choices: [
        { name: 'Custodial (API-key signer — Crossmint manages keys, ideal for agents)', value: 'custodial' },
        { name: 'Non-custodial (email signer — you retain key control)', value: 'non-custodial' }
      ]
    }
  ]);
  custodyModel = custody;

  // Step 5: Get API key
  console.log();
  console.log(chalk.cyan('An API key is needed to create the wallet.'));
  console.log(chalk.gray('Get one from https://www.crossmint.com/console → API Keys'));
  console.log();

  const { apiKey } = await inquirer.prompt([
    {
      type: 'password',
      name: 'apiKey',
      message: 'Enter your Crossmint API key (server-side key with wallets.create scope):',
      mask: '*',
      validate: (input: string) => input.length >= 10 || 'API key appears too short'
    }
  ]);

  // Step 6: Build request and create wallet
  const createSpinner = useJson ? null : ora('Creating Crossmint wallet...').start();

  try {
    const requestBody: Record<string, any> = {
      chainType: selectedChainType,
      type: selectedWalletType,
      config: {
        adminSigner: custodyModel === 'custodial'
          ? { type: 'api-key' }
          : { type: 'email', email: '' }  // Will be set below
      }
    };

    // For non-custodial, prompt for email
    if (custodyModel === 'non-custodial') {
      const { email } = await inquirer.prompt([
        {
          type: 'input',
          name: 'email',
          message: 'Enter the email for wallet ownership:',
          validate: (input: string) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(input) || 'Please enter a valid email'
        }
      ]);
      requestBody.config.adminSigner.email = email;
      requestBody.owner = `email:${email}`;
    }

    const apiUrl = 'https://www.crossmint.com/api/2025-06-09/wallets';

    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'X-API-KEY': apiKey,
        'Content-Type': 'application/json',
        'x-idempotency-key': `agentic-wallet-${name}-${Date.now()}`
      },
      body: JSON.stringify(requestBody)
    });

    if (!response.ok) {
      const errorBody = await response.text();
      let errorMsg = `Crossmint API error (${response.status})`;
      try {
        const parsed = JSON.parse(errorBody);
        errorMsg = parsed.message || parsed.error || errorMsg;
      } catch {
        errorMsg = errorBody || errorMsg;
      }
      createSpinner?.fail(chalk.red('Failed to create wallet'));
      if (useJson) jsonError(ExitCode.GENERAL_ERROR, errorMsg, { statusCode: response.status });
      console.error(chalk.red(`✗ ${errorMsg}`));
      process.exit(ExitCode.GENERAL_ERROR);
    }

    const walletData = await response.json() as Record<string, any>;

    // Normalize createdAt — API may return Unix timestamp (number) or ISO string
    let createdAtStr: string;
    if (typeof walletData.createdAt === 'number') {
      createdAtStr = new Date(walletData.createdAt).toISOString();
    } else {
      createdAtStr = walletData.createdAt || new Date().toISOString();
    }

    // Save wallet record locally
    const walletRecord: CrossmintWalletRecord = {
      id: walletData.address || uuidv4(),
      name,
      address: walletData.address,
      chainType: walletData.chainType || selectedChainType || 'evm',
      walletType: walletData.type || selectedWalletType || 'smart',
      custodyModel,
      createdAt: createdAtStr,
      crossmintLocator: walletData.owner
    };

    const saved = saveCrossmintWallet(walletRecord);
    if (!saved) {
      createSpinner?.fail(chalk.red('Wallet already exists locally (race condition)'));
      if (useJson) jsonError(ExitCode.ALREADY_EXISTS, `Wallet "${name}" already exists locally`);
      process.exit(ExitCode.ALREADY_EXISTS);
    }

    createSpinner?.succeed(chalk.green('Crossmint wallet created successfully!'));

    if (useJson) {
      jsonOut({
        ok: true,
        provider: 'crossmint',
        name,
        address: walletRecord.address,
        chainType: walletRecord.chainType,
        walletType: walletRecord.walletType,
        custodyModel: walletRecord.custodyModel,
        createdAt: walletRecord.createdAt,
        storagePath: `~/.agent-arena/crossmint-wallets/${name}.json`
      });
    } else {
      console.log();
      console.log(chalk.bold('Wallet Details:'));
      console.log(chalk.gray('─'.repeat(50)));
      console.log(`  ${chalk.cyan('Name:')}          ${name}`);
      console.log(`  ${chalk.cyan('Address:')}       ${walletRecord.address}`);
      console.log(`  ${chalk.cyan('Chain Type:')}    ${walletRecord.chainType}`);
      console.log(`  ${chalk.cyan('Wallet Type:')}   ${walletRecord.walletType}`);
      console.log(`  ${chalk.cyan('Custody:')}       ${custodyModel === 'custodial' ? chalk.green('Custodial (API-key signer)') : chalk.yellow('Non-custodial (email signer)')}`);
      console.log(chalk.gray('─'.repeat(50)));
      console.log();
      console.log(chalk.bold('Security:'));
      if (custodyModel === 'custodial') {
        console.log(chalk.white('  ✓ Keys managed by Crossmint infrastructure'));
        console.log(chalk.white('  ✓ API key controls wallet operations'));
      } else {
        console.log(chalk.white('  ✓ Keys controlled by your email signer'));
        console.log(chalk.white('  ✓ Crossmint cannot access your funds without your approval'));
      }
      console.log(chalk.white('  ✓ Wallet record stored at: ~/.agent-arena/crossmint-wallets/' + name + '.json'));
      console.log(chalk.white('  ✓ Agent Arena has ZERO access to your keys'));
      console.log();
      console.log(chalk.bold('Next steps:'));
      console.log('  1. Fund wallet: npx agentic-wallet fund --provider crossmint');
      console.log('  2. Check balance: npx agentic-wallet balance --provider crossmint');
      console.log();
      console.log(chalk.gray('Docs: https://docs.crossmint.com/introduction/platform-overview'));
    }

  } catch (error: any) {
    createSpinner?.fail(chalk.red('Failed to create wallet'));
    const errorMsg = error.cause?.code === 'ENOTFOUND'
      ? 'Network error: cannot reach Crossmint API'
      : error.message || String(error);
    if (useJson) jsonError(ExitCode.GENERAL_ERROR, errorMsg);
    console.error(chalk.red(`✗ ${errorMsg}`));
    process.exit(ExitCode.GENERAL_ERROR);
  }
}
