import chalk from 'chalk';
import ora from 'ora';
import inquirer from 'inquirer';
import { readFileSync, existsSync } from 'fs';
import { createDecipheriv, scryptSync } from 'crypto';
import { mnemonicToAccount } from 'viem/accounts';
import { v4 as uuidv4 } from 'uuid';
import {
  walletExists,
  saveWalletExclusive,
  encryptPrivateKey,
  validateWalletName,
  safePasswordEqual,
  CHAIN_CONFIG,
  type StoredWallet
} from '../utils/storage.js';
import { isJsonMode, jsonOut, jsonError, ExitCode } from '../utils/output.js';

interface RecoverOptions {
  from?: string;
  seedPhrase?: boolean;
  name?: string;
  passwordFile?: string;
  json?: boolean;
}

interface BackupFile {
  version: number;
  type: string;
  wallet: {
    id: string;
    name: string;
    address: string;
    chainId: number;
    chain: string;
    createdAt: string;
  };
  encryptedPrivateKey: string;
  iv: string;
  salt: string;
}

export async function recoverWallet(options: RecoverOptions): Promise<void> {
  const useJson = isJsonMode(options);
  const { from, seedPhrase, name = 'recovered', passwordFile } = options;

  if (!useJson) {
    console.log();
    console.log(chalk.bold('OpenWallet Recovery'));
    console.log(chalk.gray('─'.repeat(50)));
    console.log();
    console.log(chalk.white('Agent Arena does NOT have access to your recovery data.'));
    console.log(chalk.white('All recovery happens locally on your machine.'));
    console.log();
  }

  if (!from && !seedPhrase) {
    if (useJson) jsonError(ExitCode.INVALID_INPUT, 'Specify --from <backup-file> or --seed-phrase');

    console.log(chalk.yellow('Choose recovery method:'));
    const { method } = await inquirer.prompt([
      {
        type: 'list',
        name: 'method',
        message: 'How do you want to recover?',
        choices: [
          { name: 'From backup file', value: 'backup' },
          { name: 'From 12-word seed phrase', value: 'seed' }
        ]
      }
    ]);

    if (method === 'backup') {
      const { backupPath } = await inquirer.prompt([
        {
          type: 'input',
          name: 'backupPath',
          message: 'Enter path to backup file:',
          validate: (input: string) => existsSync(input) || 'File not found'
        }
      ]);
      return recoverFromBackup(backupPath, name, useJson, passwordFile);
    } else {
      return recoverFromSeed(name, useJson, passwordFile);
    }
  }

  if (from) {
    return recoverFromBackup(from, name, useJson, passwordFile);
  }

  if (seedPhrase) {
    return recoverFromSeed(name, useJson, passwordFile);
  }
}

async function recoverFromBackup(backupPath: string, walletName: string, useJson: boolean, passwordFile?: string): Promise<void> {
  if (!useJson) {
    console.log(chalk.cyan('Recovering from backup file...'));
    console.log(`  File: ${backupPath}`);
    console.log();
  }

  // Validate wallet name
  try {
    validateWalletName(walletName);
  } catch (err: any) {
    if (useJson) jsonError(ExitCode.INVALID_INPUT, err.message);
    console.error(chalk.red(`✗ ${err.message}`));
    process.exit(ExitCode.INVALID_INPUT);
  }

  if (!existsSync(backupPath)) {
    if (useJson) jsonError(ExitCode.WALLET_NOT_FOUND, `Backup file not found: ${backupPath}`);
    console.error(chalk.red(`✗ Backup file not found: ${backupPath}`));
    process.exit(ExitCode.WALLET_NOT_FOUND);
  }

  if (walletExists(walletName)) {
    if (useJson) jsonError(ExitCode.ALREADY_EXISTS, `Wallet "${walletName}" already exists`);
    console.error(chalk.red(`✗ Wallet "${walletName}" already exists`));
    console.log(chalk.gray('Use --name <different-name> to specify a different name'));
    process.exit(ExitCode.ALREADY_EXISTS);
  }

  let backup: BackupFile;
  try {
    const content = readFileSync(backupPath, 'utf8');
    backup = JSON.parse(content);
  } catch {
    if (useJson) jsonError(ExitCode.INVALID_INPUT, 'Failed to read backup file');
    console.error(chalk.red('✗ Failed to read backup file'));
    process.exit(ExitCode.INVALID_INPUT);
  }

  if (backup!.type !== 'openwallet-backup') {
    if (useJson) jsonError(ExitCode.INVALID_INPUT, 'Invalid backup file format');
    console.error(chalk.red('✗ Invalid backup file format'));
    process.exit(ExitCode.INVALID_INPUT);
  }

  if (!useJson) {
    console.log(chalk.cyan('Backup contains:'));
    console.log(`  Original name: ${backup!.wallet.name}`);
    console.log(`  Address:       ${backup!.wallet.address}`);
    console.log(`  Chain:         ${backup!.wallet.chain}`);
    console.log();
  }

  // Get backup password
  let backupPassword: string;
  if (passwordFile) {
    if (!existsSync(passwordFile)) {
      if (useJson) jsonError(ExitCode.INVALID_INPUT, `Password file not found: ${passwordFile}`);
      console.error(chalk.red(`✗ Password file not found: ${passwordFile}`));
      process.exit(ExitCode.INVALID_INPUT);
    }
    backupPassword = readFileSync(passwordFile, 'utf8').trim();
  } else {
    const answers = await inquirer.prompt([
      {
        type: 'password',
        name: 'backupPassword',
        message: 'Enter backup decryption password:',
        mask: '*'
      }
    ]);
    backupPassword = answers.backupPassword;
  }

  // Decrypt private key
  const spinner = useJson ? null : ora('Decrypting backup...').start();
  let privateKey: string;

  try {
    const key = scryptSync(backupPassword, Buffer.from(backup!.salt, 'hex'), 32);
    const ivBuffer = Buffer.from(backup!.iv, 'hex');

    const authTag = Buffer.from(backup!.encryptedPrivateKey.slice(-32), 'hex');
    const encryptedData = backup!.encryptedPrivateKey.slice(0, -32);

    const decipher = createDecipheriv('aes-256-gcm', key, ivBuffer);
    decipher.setAuthTag(authTag);

    privateKey = decipher.update(encryptedData, 'hex', 'utf8');
    privateKey += decipher.final('utf8');

    spinner?.succeed('Backup decrypted');
  } catch {
    spinner?.fail(chalk.red('Failed to decrypt backup. Wrong password?'));
    if (useJson) jsonError(ExitCode.ENCRYPTION_ERROR, 'Failed to decrypt backup. Wrong password?');
    process.exit(ExitCode.ENCRYPTION_ERROR);
  }

  // Get new wallet password
  let newPassword: string;
  if (passwordFile) {
    newPassword = backupPassword;
  } else {
    if (!useJson) {
      console.log();
      console.log(chalk.yellow('Set a password for the recovered wallet.'));
    }
    const answers = await inquirer.prompt([
      {
        type: 'password',
        name: 'newPassword',
        message: 'Enter new wallet password (min 8 chars):',
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

    if (!safePasswordEqual(answers.newPassword, answers.confirmPassword)) {
      if (useJson) jsonError(ExitCode.INVALID_INPUT, 'Passwords do not match');
      console.error(chalk.red('✗ Passwords do not match'));
      process.exit(ExitCode.INVALID_INPUT);
    }
    newPassword = answers.newPassword;
  }

  // Create new wallet with recovered key
  const saveSpinner = useJson ? null : ora('Saving recovered wallet...').start();

  try {
    const { encrypted, iv, salt, authTag } = encryptPrivateKey(privateKey!, newPassword);

    const wallet: StoredWallet = {
      id: uuidv4(),
      name: walletName,
      address: backup!.wallet.address,
      chainId: backup!.wallet.chainId,
      chain: backup!.wallet.chain,
      createdAt: new Date().toISOString(),
      encrypted: true,
      encryptedPrivateKey: encrypted,
      iv,
      salt,
      authTag
    };

    const saved = saveWalletExclusive(wallet);
    if (!saved) {
      saveSpinner?.fail(chalk.red('Wallet already exists'));
      if (useJson) jsonError(ExitCode.ALREADY_EXISTS, `Wallet "${walletName}" already exists`);
      process.exit(ExitCode.ALREADY_EXISTS);
    }

    saveSpinner?.succeed(chalk.green('Wallet recovered successfully!'));

    if (useJson) {
      jsonOut({
        ok: true,
        name: walletName,
        address: backup!.wallet.address,
        chain: backup!.wallet.chain,
        chainId: backup!.wallet.chainId
      });
    } else {
      console.log();
      console.log(chalk.bold('Recovered Wallet:'));
      console.log(chalk.gray('─'.repeat(50)));
      console.log(`  Name:    ${walletName}`);
      console.log(`  Address: ${backup!.wallet.address}`);
      console.log(`  Chain:   ${backup!.wallet.chain}`);
      console.log(chalk.gray('─'.repeat(50)));
      console.log();
      console.log(chalk.green('✓ Your wallet is ready to use'));
    }

  } catch (error) {
    saveSpinner?.fail(chalk.red('Failed to save wallet'));
    if (useJson) jsonError(ExitCode.GENERAL_ERROR, 'Failed to save wallet');
    console.error(error);
    process.exit(ExitCode.GENERAL_ERROR);
  }
}

async function recoverFromSeed(walletName: string, useJson: boolean, passwordFile?: string): Promise<void> {
  if (!useJson) {
    console.log(chalk.cyan('Recovering from seed phrase...'));
    console.log();
    console.log(chalk.yellow('⚠ SECURITY WARNING:'));
    console.log(chalk.white('  Your seed phrase gives full access to your wallet.'));
    console.log(chalk.white('  Make sure no one is watching your screen.'));
    console.log(chalk.white('  Agent Arena does NOT see or store your seed phrase.'));
    console.log();
  }

  // Validate wallet name
  try {
    validateWalletName(walletName);
  } catch (err: any) {
    if (useJson) jsonError(ExitCode.INVALID_INPUT, err.message);
    console.error(chalk.red(`✗ ${err.message}`));
    process.exit(ExitCode.INVALID_INPUT);
  }

  if (walletExists(walletName)) {
    if (useJson) jsonError(ExitCode.ALREADY_EXISTS, `Wallet "${walletName}" already exists`);
    console.error(chalk.red(`✗ Wallet "${walletName}" already exists`));
    console.log(chalk.gray('Use --name <different-name> to specify a different name'));
    process.exit(ExitCode.ALREADY_EXISTS);
  }

  // Get seed phrase
  const { seedPhrase } = await inquirer.prompt([
    {
      type: 'password',
      name: 'seedPhrase',
      message: 'Enter your 12-word seed phrase:',
      mask: '*',
      validate: (input: string) => {
        const words = input.trim().split(/\s+/);
        return words.length === 12 || 'Seed phrase must be exactly 12 words';
      }
    }
  ]);

  // Get chain
  const { chain } = await inquirer.prompt([
    {
      type: 'list',
      name: 'chain',
      message: 'Select target chain:',
      choices: Object.keys(CHAIN_CONFIG).map(k => ({
        name: `${CHAIN_CONFIG[k].name} (${CHAIN_CONFIG[k].chainId})`,
        value: k
      })),
      default: 'base'
    }
  ]);

  // Get wallet password
  let password: string;
  if (passwordFile) {
    if (!existsSync(passwordFile)) {
      if (useJson) jsonError(ExitCode.INVALID_INPUT, `Password file not found: ${passwordFile}`);
      console.error(chalk.red(`✗ Password file not found: ${passwordFile}`));
      process.exit(ExitCode.INVALID_INPUT);
    }
    password = readFileSync(passwordFile, 'utf8').trim();
  } else {
    const answers = await inquirer.prompt([
      {
        type: 'password',
        name: 'password',
        message: 'Enter wallet encryption password (min 8 chars):',
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

  const spinner = useJson ? null : ora('Recovering wallet from seed...').start();

  try {
    const account = mnemonicToAccount(seedPhrase.trim());
    const privateKey = account.getHdKey().privateKey;

    if (!privateKey) {
      throw new Error('Failed to derive private key');
    }

    const privateKeyHex = `0x${Buffer.from(privateKey).toString('hex')}`;
    const chainConfig = CHAIN_CONFIG[chain];

    const { encrypted, iv, salt, authTag } = encryptPrivateKey(privateKeyHex, password);

    const wallet: StoredWallet = {
      id: uuidv4(),
      name: walletName,
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

    const saved = saveWalletExclusive(wallet);
    if (!saved) {
      spinner?.fail(chalk.red('Wallet already exists'));
      if (useJson) jsonError(ExitCode.ALREADY_EXISTS, `Wallet "${walletName}" already exists`);
      process.exit(ExitCode.ALREADY_EXISTS);
    }

    spinner?.succeed(chalk.green('Wallet recovered successfully!'));

    if (useJson) {
      jsonOut({
        ok: true,
        name: walletName,
        address: account.address,
        chain: chainConfig.name,
        chainId: chainConfig.chainId
      });
    } else {
      console.log();
      console.log(chalk.bold('Recovered Wallet:'));
      console.log(chalk.gray('─'.repeat(50)));
      console.log(`  Name:    ${walletName}`);
      console.log(`  Address: ${account.address}`);
      console.log(`  Chain:   ${chainConfig.name} (${chainConfig.chainId})`);
      console.log(chalk.gray('─'.repeat(50)));
      console.log();
      console.log(chalk.green('✓ Your wallet is ready to use'));
    }

  } catch (error) {
    spinner?.fail(chalk.red('Failed to recover wallet'));
    if (useJson) jsonError(ExitCode.GENERAL_ERROR, 'Failed to recover wallet');
    console.error(error);
    process.exit(ExitCode.GENERAL_ERROR);
  }
}
