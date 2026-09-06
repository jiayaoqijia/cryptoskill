#!/usr/bin/env bun
import { Command } from 'commander';
import packageJson from './package.json';
import { getConfig } from './lib/config.js';
import { outputSuccess, outputError, safeJsonParse } from './cli-helpers.js';
import { getWalletByPrivateKey, type AElfWallet } from './lib/aelf-client.js';
import { sameChainTransfer, crossChainTransfer, recoverStuckTransfer } from './src/core/transfer.js';
import { addGuardian, removeGuardian } from './src/core/guardian.js';
import { managerForwardCallWithKey } from './src/core/contract.js';
import { resolveManagerWallet } from './src/core/keystore.js';
import type { ApprovedGuardian, GuardianToAdd, GuardianToRemove } from './lib/types.js';

const program = new Command();
program.name('portkey-tx').version(packageJson.version).description('Portkey wallet transaction & guardian tools')
  .option('--network <network>', 'Portkey network (mainnet only)', 'mainnet');

function requireWallet(input: {
  network: string;
  loginEmail?: string;
  password?: string;
  keystoreFile?: string;
}): AElfWallet {
  try {
    return resolveManagerWallet(input).wallet;
  } catch (error) {
    if (error instanceof Error) outputError(error.message);
    outputError(String(error));
  }
  throw new Error('Wallet resolution unexpectedly returned without exiting');
}

function withWalletOptions(command: Command): Command {
  return command
    .option('--login-email <email>', 'Use a saved CA keystore profile by login email')
    .option('--password <pwd>', 'Keystore password for this command (avoids relying on prior unlock)')
    .option('--keystore-file <path>', 'Explicit CA keystore file path');
}

withWalletOptions(program.command('transfer'))
  .description('Transfer tokens on the same chain')
  .requiredOption('--ca-hash <hash>', 'CA hash')
  .requiredOption('--token-contract <addr>', 'Token contract address')
  .requiredOption('--symbol <symbol>', 'Token symbol')
  .requiredOption('--to <addr>', 'Recipient address')
  .requiredOption('--amount <amount>', 'Amount in smallest unit')
  .option('--memo <memo>', 'Transfer memo')
  .option('--guardians-approved <json>', 'Optional JSON array of one-time approved guardians')
  .requiredOption('--chain-id <chainId>', 'Chain ID')
  .action(async (opts) => {
    try {
      const wallet = requireWallet({
        network: program.opts().network,
        loginEmail: opts.loginEmail,
        password: opts.password,
        keystoreFile: opts.keystoreFile,
      });
      const config = getConfig({ network: program.opts().network });
      outputSuccess(await sameChainTransfer(config, wallet, {
        caHash: opts.caHash, tokenContractAddress: opts.tokenContract,
        symbol: opts.symbol, to: opts.to, amount: opts.amount,
        memo: opts.memo, chainId: opts.chainId,
        guardiansApproved: opts.guardiansApproved
          ? safeJsonParse(opts.guardiansApproved, 'guardians-approved') as ApprovedGuardian[]
          : undefined,
      }));
    } catch (err: any) { outputError(err.message); }
  });

withWalletOptions(program.command('cross-chain-transfer'))
  .description('Transfer tokens cross-chain')
  .requiredOption('--ca-hash <hash>', 'CA hash')
  .requiredOption('--token-contract <addr>', 'Token contract address')
  .requiredOption('--symbol <symbol>', 'Token symbol')
  .requiredOption('--to <addr>', 'Recipient address')
  .requiredOption('--amount <amount>', 'Amount in smallest unit')
  .option('--guardians-approved <json>', 'Optional JSON array of one-time approved guardians')
  .requiredOption('--chain-id <chainId>', 'Source chain ID')
  .requiredOption('--to-chain-id <chainId>', 'Target chain ID')
  .action(async (opts) => {
    try {
      const wallet = requireWallet({
        network: program.opts().network,
        loginEmail: opts.loginEmail,
        password: opts.password,
        keystoreFile: opts.keystoreFile,
      });
      const config = getConfig({ network: program.opts().network });
      outputSuccess(await crossChainTransfer(config, wallet, {
        caHash: opts.caHash, tokenContractAddress: opts.tokenContract,
        symbol: opts.symbol, to: opts.to, amount: opts.amount,
        chainId: opts.chainId, toChainId: opts.toChainId,
        guardiansApproved: opts.guardiansApproved
          ? safeJsonParse(opts.guardiansApproved, 'guardians-approved') as ApprovedGuardian[]
          : undefined,
      }));
    } catch (err: any) { outputError(err.message); }
  });

withWalletOptions(program.command('recover-stuck-transfer'))
  .description('Recover tokens stuck on Manager after failed cross-chain transfer')
  .requiredOption('--token-contract <addr>', 'Token contract address')
  .requiredOption('--symbol <symbol>', 'Token symbol')
  .requiredOption('--amount <amount>', 'Amount in smallest unit')
  .requiredOption('--ca-address <addr>', 'CA address to recover tokens to')
  .requiredOption('--chain-id <chainId>', 'Chain ID')
  .option('--memo <memo>', 'Optional memo')
  .action(async (opts) => {
    try {
      const wallet = requireWallet({
        network: program.opts().network,
        loginEmail: opts.loginEmail,
        password: opts.password,
        keystoreFile: opts.keystoreFile,
      });
      const config = getConfig({ network: program.opts().network });
      outputSuccess(await recoverStuckTransfer(config, wallet, {
        tokenContractAddress: opts.tokenContract, symbol: opts.symbol,
        amount: opts.amount, caAddress: opts.caAddress, chainId: opts.chainId,
        memo: opts.memo,
      }));
    } catch (err: any) { outputError(err.message); }
  });

withWalletOptions(program.command('add-guardian'))
  .description('Add a guardian to a CA wallet')
  .requiredOption('--ca-hash <hash>', 'CA hash')
  .requiredOption('--guardian-to-add <json>', 'JSON guardian to add')
  .requiredOption('--guardians-approved <json>', 'JSON array of approved guardians')
  .requiredOption('--chain-id <chainId>', 'Chain ID')
  .action(async (opts) => {
    try {
      const wallet = requireWallet({
        network: program.opts().network,
        loginEmail: opts.loginEmail,
        password: opts.password,
        keystoreFile: opts.keystoreFile,
      });
      const config = getConfig({ network: program.opts().network });
      outputSuccess(await addGuardian(config, wallet, {
        caHash: opts.caHash,
        guardianToAdd: safeJsonParse(opts.guardianToAdd, 'guardian-to-add') as GuardianToAdd,
        guardiansApproved: safeJsonParse(opts.guardiansApproved, 'guardians-approved') as ApprovedGuardian[],
        chainId: opts.chainId,
      }));
    } catch (err: any) { outputError(err.message); }
  });

withWalletOptions(program.command('remove-guardian'))
  .description('Remove a guardian from a CA wallet')
  .requiredOption('--ca-hash <hash>', 'CA hash')
  .requiredOption('--guardian-to-remove <json>', 'JSON guardian to remove')
  .requiredOption('--guardians-approved <json>', 'JSON array of approved guardians')
  .requiredOption('--chain-id <chainId>', 'Chain ID')
  .action(async (opts) => {
    try {
      const wallet = requireWallet({
        network: program.opts().network,
        loginEmail: opts.loginEmail,
        password: opts.password,
        keystoreFile: opts.keystoreFile,
      });
      const config = getConfig({ network: program.opts().network });
      outputSuccess(await removeGuardian(config, wallet, {
        caHash: opts.caHash,
        guardianToRemove: safeJsonParse(opts.guardianToRemove, 'guardian-to-remove') as GuardianToRemove,
        guardiansApproved: safeJsonParse(opts.guardiansApproved, 'guardians-approved') as ApprovedGuardian[],
        chainId: opts.chainId,
      }));
    } catch (err: any) { outputError(err.message); }
  });

withWalletOptions(program.command('forward-call'))
  .description('Generic ManagerForwardCall to any contract (blocks early if the current manager is not yet synced on the target chain)')
  .requiredOption('--ca-hash <hash>', 'CA hash')
  .requiredOption('--contract-address <addr>', 'Target contract address')
  .requiredOption('--method-name <name>', 'Target method name')
  .requiredOption('--args <json>', 'JSON method arguments')
  .option('--guardians-approved <json>', 'Optional JSON array of approved guardians for transfer-related calls')
  .requiredOption('--chain-id <chainId>', 'Chain ID')
  .action(async (opts) => {
    try {
      const wallet = requireWallet({
        network: program.opts().network,
        loginEmail: opts.loginEmail,
        password: opts.password,
        keystoreFile: opts.keystoreFile,
      });
      const config = getConfig({ network: program.opts().network });
      outputSuccess(await managerForwardCallWithKey(config, wallet.privateKey, {
        caHash: opts.caHash, contractAddress: opts.contractAddress,
        methodName: opts.methodName,
        args: safeJsonParse(opts.args, 'args') as Record<string, unknown>,
        chainId: opts.chainId,
        guardiansApproved: opts.guardiansApproved
          ? safeJsonParse(opts.guardiansApproved, 'guardians-approved') as ApprovedGuardian[]
          : undefined,
      }));
    } catch (err: any) { outputError(err.message); }
  });

program.parse();
