import chalk from 'chalk';
import ora from 'ora';
import inquirer from 'inquirer';
import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import { join } from 'path';
import { homedir } from 'os';
import { createCipheriv, randomBytes, scryptSync } from 'crypto';
import { loadWallet, decryptPrivateKey, validateWalletName, safePasswordEqual } from '../utils/storage.js';
import { isJsonMode, jsonOut, jsonError, ExitCode } from '../utils/output.js';

interface BackupOptions {
  name?: string;
  output?: string;
  passwordFile?: string;
  json?: boolean;
}

export async function backupWallet(options: BackupOptions): Promise<void> {
  const useJson = isJsonMode(options);
  const { name = 'default', output, passwordFile } = options;

  if (!useJson) {
    console.log();
    console.log(chalk.bold('OpenWallet Backup'));
    console.log(chalk.gray('─'.repeat(50)));
    console.log();
  }

  // Load wallet
  const wallet = loadWallet(name);
  if (!wallet) {
    if (useJson) jsonError(ExitCode.WALLET_NOT_FOUND, `Wallet "${name}" not found`);
    console.error(chalk.red(`✗ Wallet "${name}" not found`));
    console.log(chalk.gray('List wallets: npx agentic-wallet status --provider openwallet'));
    process.exit(ExitCode.WALLET_NOT_FOUND);
  }

  if (!useJson) {
    console.log(chalk.cyan('Wallet to backup:'));
    console.log(`  Name:    ${wallet.name}`);
    console.log(`  Address: ${wallet.address}`);
    console.log(`  Chain:   ${wallet.chain}`);
    console.log();
  }

  // Get decryption password for the wallet
  let walletPassword: string;
  if (passwordFile) {
    if (!existsSync(passwordFile)) {
      if (useJson) jsonError(ExitCode.INVALID_INPUT, `Password file not found: ${passwordFile}`);
      console.error(chalk.red(`✗ Password file not found: ${passwordFile}`));
      process.exit(ExitCode.INVALID_INPUT);
    }
    walletPassword = readFileSync(passwordFile, 'utf8').trim();
  } else {
    const answers = await inquirer.prompt([
      {
        type: 'password',
        name: 'walletPassword',
        message: 'Enter wallet decryption password:',
        mask: '*'
      }
    ]);
    walletPassword = answers.walletPassword;
  }

  // Decrypt private key to verify password is correct
  let privateKey: string;
  try {
    if (!wallet.encrypted || !wallet.encryptedPrivateKey) {
      throw new Error('Wallet is not encrypted — cannot backup unencrypted wallets');
    }
    privateKey = decryptPrivateKey(
      wallet.encryptedPrivateKey,
      wallet.iv!,
      wallet.salt!,
      walletPassword,
      wallet.authTag
    );
  } catch {
    if (useJson) jsonError(ExitCode.ENCRYPTION_ERROR, 'Failed to decrypt wallet. Wrong password?');
    console.error(chalk.red('✗ Failed to decrypt wallet. Wrong password?'));
    process.exit(ExitCode.ENCRYPTION_ERROR);
  }

  // Get backup password (can be different from wallet password)
  let backupPassword: string;
  if (passwordFile) {
    backupPassword = walletPassword;
  } else {
    if (!useJson) {
      console.log(chalk.yellow('Choose a password for the backup file.'));
      console.log(chalk.gray('This can be different from your wallet password.'));
    }
    const answers = await inquirer.prompt([
      {
        type: 'password',
        name: 'backupPassword',
        message: 'Enter backup encryption password (min 8 chars):',
        mask: '*',
        validate: (input: string) => input.length >= 8 || 'Password must be at least 8 characters'
      },
      {
        type: 'password',
        name: 'confirmPassword',
        message: 'Confirm backup password:',
        mask: '*'
      }
    ]);

    if (!safePasswordEqual(answers.backupPassword, answers.confirmPassword)) {
      if (useJson) jsonError(ExitCode.INVALID_INPUT, 'Passwords do not match');
      console.error(chalk.red('✗ Passwords do not match'));
      process.exit(ExitCode.INVALID_INPUT);
    }
    backupPassword = answers.backupPassword;
  }

  const spinner = useJson ? null : ora('Creating encrypted backup...').start();

  try {
    const backupData = {
      version: 1,
      type: 'openwallet-backup',
      createdAt: new Date().toISOString(),
      wallet: {
        id: wallet.id,
        name: wallet.name,
        address: wallet.address,
        chainId: wallet.chainId,
        chain: wallet.chain,
        createdAt: wallet.createdAt
      },
    };

    // Encrypt private key with backup password
    const salt = randomBytes(16);
    const key = scryptSync(backupPassword, salt, 32);
    const iv = randomBytes(16);
    const cipher = createCipheriv('aes-256-gcm', key, iv);

    let encryptedKey = cipher.update(privateKey!, 'utf8', 'hex');
    encryptedKey += cipher.final('hex');
    const authTag = cipher.getAuthTag();

    const fullBackup = {
      ...backupData,
      encryptedPrivateKey: encryptedKey + authTag.toString('hex'),
      iv: iv.toString('hex'),
      salt: salt.toString('hex')
    };

    // Determine output path
    const timestamp = new Date().toISOString().split('T')[0];
    const filename = `${wallet.name}-backup-${timestamp}.json`;
    let outputPath: string;

    if (output) {
      if (!existsSync(output)) {
        mkdirSync(output, { recursive: true });
      }
      outputPath = join(output, filename);
    } else {
      const defaultDir = join(homedir(), '.agent-arena', 'backups');
      if (!existsSync(defaultDir)) {
        mkdirSync(defaultDir, { recursive: true });
      }
      outputPath = join(defaultDir, filename);
    }

    writeFileSync(outputPath, JSON.stringify(fullBackup, null, 2), 'utf8');

    spinner?.succeed(chalk.green('Backup created successfully!'));

    if (useJson) {
      jsonOut({
        ok: true,
        file: outputPath,
        wallet: wallet.name,
        address: wallet.address,
        chain: wallet.chain,
        createdAt: backupData.createdAt,
        recoverCommand: `npx agentic-wallet recover --from "${outputPath}"`
      });
    } else {
      console.log();
      console.log(chalk.bold('Backup Details:'));
      console.log(chalk.gray('─'.repeat(50)));
      console.log(`  File:     ${outputPath}`);
      console.log(`  Wallet:   ${wallet.name}`);
      console.log(`  Address:  ${wallet.address}`);
      console.log(`  Created:  ${backupData.createdAt}`);
      console.log(chalk.gray('─'.repeat(50)));
      console.log();
      console.log(chalk.bold('Recovery Command:'));
      console.log(chalk.white(`  npx agentic-wallet recover --from "${outputPath}"`));
      console.log();
      console.log(chalk.yellow('⚠ IMPORTANT:'));
      console.log(chalk.white('  • Store this backup file in a secure location'));
      console.log(chalk.white('  • The backup is encrypted but should not be shared'));
      console.log(chalk.white('  • Remember your backup password - it cannot be recovered'));
      console.log(chalk.white('  • Agent Arena does NOT have access to this backup'));
    }

  } catch (error) {
    spinner?.fail(chalk.red('Failed to create backup'));
    if (useJson) jsonError(ExitCode.GENERAL_ERROR, 'Failed to create backup');
    console.error(error);
    process.exit(ExitCode.GENERAL_ERROR);
  }
}
