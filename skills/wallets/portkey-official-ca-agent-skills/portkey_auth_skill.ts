#!/usr/bin/env bun
import { Command } from 'commander';
import packageJson from './package.json';
import { getConfig } from './lib/config.js';
import { outputSuccess, outputError, safeJsonParse } from './cli-helpers.js';
import { createWallet } from './lib/aelf-client.js';
import {
  saveKeystore,
  unlockWallet,
  lockWallet,
  getWalletStatus,
  listWalletProfiles,
} from './src/core/keystore.js';
import {
  getVerifierServer,
  sendVerificationCode,
  verifyCode,
  registerWallet,
  recoverWallet,
  checkRegisterOrRecoveryStatus,
} from './src/core/auth.js';
import { recoverAndSaveWallet } from './src/core/auth-session.js';
import { OperationType } from './lib/types.js';

const program = new Command();
program.name('portkey-auth').version(packageJson.version).description('Portkey wallet registration & login tools')
  .option('--network <network>', 'Portkey network (mainnet only)', 'mainnet');

function parseOperationType(operation: string): OperationType {
  const normalized = String(operation || '').toLowerCase().trim();
  if (normalized === 'register') return OperationType.CreateCAHolder;
  if (normalized === 'recovery') return OperationType.SocialRecovery;
  if (normalized === 'transferapprove' || normalized === 'guardianapprovetransfer') {
    return OperationType.GuardianApproveTransfer;
  }
  outputError(`Invalid --operation "${operation}". Expected "register", "recovery", or "transferApprove".`);
  return OperationType.Unknown; // unreachable
}

program.command('get-verifier')
  .description('Get an assigned verifier server')
  .requiredOption('--chain-id <chainId>', 'Resolved chain ID. Call portkey_query_skill.ts prepare-auth-flow first.')
  .action(async (opts) => {
    try {
      const config = getConfig({ network: program.opts().network });
      outputSuccess(await getVerifierServer(config, { chainId: opts.chainId }));
    } catch (err: any) { outputError(err.message); }
  });

program.command('send-code')
  .description('Send verification code to email')
  .requiredOption('--email <email>', 'Email address')
  .requiredOption('--verifier-id <id>', 'Verifier service ID')
  .requiredOption('--operation <type>', 'Operation type: register|recovery|transferApprove')
  .requiredOption('--chain-id <chainId>', 'Resolved chain ID. Call portkey_query_skill.ts prepare-auth-flow first.')
  .action(async (opts) => {
    try {
      const config = getConfig({ network: program.opts().network });
      outputSuccess(await sendVerificationCode(config, {
        email: opts.email, verifierId: opts.verifierId,
        chainId: opts.chainId, operationType: parseOperationType(opts.operation),
      }));
    } catch (err: any) { outputError(err.message); }
  });

program.command('verify-code')
  .description('Verify a 6-digit code')
  .requiredOption('--email <email>', 'Email address')
  .requiredOption('--code <code>', '6-digit verification code')
  .requiredOption('--verifier-id <id>', 'Verifier service ID')
  .requiredOption('--session-id <id>', 'Verifier session ID')
  .requiredOption('--operation <type>', 'Operation type: register|recovery|transferApprove')
  .requiredOption('--chain-id <chainId>', 'Resolved chain ID. Call portkey_query_skill.ts prepare-auth-flow first.')
  .action(async (opts) => {
    try {
      const config = getConfig({ network: program.opts().network });
      outputSuccess(await verifyCode(config, {
        email: opts.email, verificationCode: opts.code,
        verifierId: opts.verifierId, verifierSessionId: opts.sessionId,
        chainId: opts.chainId, operationType: parseOperationType(opts.operation),
      }));
    } catch (err: any) { outputError(err.message); }
  });

program.command('create-wallet')
  .description('Create a new manager wallet')
  .action(() => {
    try {
      outputSuccess(createWallet());
    } catch (err: any) { outputError(err.message); }
  });

program.command('register')
  .description('Register a new CA wallet')
  .requiredOption('--email <email>', 'Email address')
  .requiredOption('--manager <addr>', 'Manager wallet address')
  .requiredOption('--verifier-id <id>', 'Verifier service ID')
  .requiredOption('--verification-doc <doc>', 'Verification document')
  .requiredOption('--signature <sig>', 'Verifier signature')
  .requiredOption('--chain-id <chainId>', 'Resolved chain ID. Call portkey_query_skill.ts prepare-auth-flow first.')
  .action(async (opts) => {
    try {
      const config = getConfig({ network: program.opts().network });
      outputSuccess(await registerWallet(config, {
        email: opts.email, manager: opts.manager,
        verifierId: opts.verifierId, verificationDoc: opts.verificationDoc,
        signature: opts.signature, chainId: opts.chainId,
      }));
    } catch (err: any) { outputError(err.message); }
  });

program.command('recover')
  .description('Recover (login) an existing CA wallet')
  .requiredOption('--email <email>', 'Email address')
  .requiredOption('--manager <addr>', 'New manager wallet address')
  .requiredOption('--guardians-approved <json>', 'JSON array of approved guardians')
  .requiredOption('--chain-id <chainId>', 'Resolved chain ID. Call portkey_query_skill.ts prepare-auth-flow first.')
  .action(async (opts) => {
    try {
      const config = getConfig({ network: program.opts().network });
      outputSuccess(await recoverWallet(config, {
        email: opts.email, manager: opts.manager,
        guardiansApproved: safeJsonParse(opts.guardiansApproved, 'guardians-approved') as any, chainId: opts.chainId,
      }));
    } catch (err: any) { outputError(err.message); }
  });

program.command('recover-and-save')
  .description('Recover an existing CA wallet, wait for pass status, and immediately save the new manager to a keystore')
  .requiredOption('--email <email>', 'Email address')
  .requiredOption('--guardians-approved <json>', 'JSON array of approved guardians')
  .requiredOption('--chain-id <chainId>', 'Resolved chain ID. Call portkey_query_skill.ts prepare-auth-flow first.')
  .requiredOption('--password <pwd>', 'Password to encrypt the saved keystore')
  .option('--login-email <email>', 'Login email associated with this CA account (defaults to --email)')
  .option('--max-status-checks <n>', 'Max status polling attempts before failing')
  .option('--status-check-delay-ms <ms>', 'Delay between status polling attempts in milliseconds')
  .action(async (opts) => {
    try {
      const config = getConfig({ network: program.opts().network });
      outputSuccess(await recoverAndSaveWallet(config, {
        email: opts.email,
        guardiansApproved: safeJsonParse(opts.guardiansApproved, 'guardians-approved') as any,
        chainId: opts.chainId,
        password: opts.password,
        loginEmail: opts.loginEmail,
        network: config.network,
        maxStatusChecks: opts.maxStatusChecks ? Number(opts.maxStatusChecks) : undefined,
        statusCheckDelayMs: opts.statusCheckDelayMs ? Number(opts.statusCheckDelayMs) : undefined,
      }));
    } catch (err: any) { outputError(err.message); }
  });

program.command('check-status')
  .description('Check registration or recovery status')
  .requiredOption('--session-id <id>', 'Session ID')
  .requiredOption('--type <type>', 'register or recovery')
  .action(async (opts) => {
    try {
      const config = getConfig({ network: program.opts().network });
      outputSuccess(await checkRegisterOrRecoveryStatus(config, {
        sessionId: opts.sessionId, type: opts.type,
      }));
    } catch (err: any) { outputError(err.message); }
  });

program.command('save-keystore')
  .description('Encrypt and save Manager wallet to keystore file')
  .requiredOption('--password <pwd>', 'Password to encrypt')
  .requiredOption('--private-key <key>', 'Manager private key (hex)')
  .requiredOption('--mnemonic <words>', 'Manager mnemonic')
  .requiredOption('--ca-hash <hash>', 'CA hash')
  .requiredOption('--ca-address <addr>', 'CA address')
  .option('--login-email <email>', 'Login email associated with this CA account')
  .requiredOption('--origin-chain-id <chainId>', 'Resolved origin chain ID. Call portkey_query_skill.ts prepare-auth-flow first.')
  .action(async (opts) => {
    try {
      const network = getConfig({ network: program.opts().network }).network;
      outputSuccess(saveKeystore({
        password: opts.password, privateKey: opts.privateKey, mnemonic: opts.mnemonic,
        caHash: opts.caHash, caAddress: opts.caAddress,
        loginEmail: opts.loginEmail,
        originChainId: opts.originChainId, network,
      }));
    } catch (err: any) { outputError(err.message); }
  });

program.command('unlock')
  .description('Unlock the encrypted keystore with a password. If the password was forgotten, use recover-and-save to re-login / recover with fresh guardian verification codes.')
  .requiredOption('--password <pwd>', 'Keystore password')
  .option('--login-email <email>', 'Login email associated with this CA account')
  .option('--keystore-file <path>', 'Explicit CA keystore file path')
  .action(async (opts) => {
    try {
      const network = getConfig({ network: program.opts().network }).network;
      outputSuccess(unlockWallet(
        opts.password,
        network,
        opts.loginEmail,
        opts.keystoreFile,
      ));
    } catch (err: any) { outputError(err.message); }
  });

program.command('lock')
  .description('Lock the wallet (clear private key from memory)')
  .action(async () => {
    try {
      outputSuccess(lockWallet());
    } catch (err: any) { outputError(err.message); }
  });

program.command('wallet-status')
  .description('Check wallet status (keystore exists, unlocked, CA info, recommended next step, and wrong-profile / forgotten-password guidance)')
  .option('--login-email <email>', 'Login email associated with this CA account')
  .action(async (opts) => {
    try {
      const network = getConfig({ network: program.opts().network }).network;
      outputSuccess(getWalletStatus(
        network,
        opts.loginEmail,
      ));
    } catch (err: any) { outputError(err.message); }
  });

program.command('list-wallet-profiles')
  .description('List locally saved CA keystore profiles')
  .action(async () => {
    try {
      const optionSource = program.getOptionValueSource('network');
      const network = optionSource === 'default'
        ? undefined
        : getConfig({ network: program.opts().network }).network;
      outputSuccess({ profiles: listWalletProfiles(network) });
    } catch (err: any) { outputError(err.message); }
  });

program.parse();
