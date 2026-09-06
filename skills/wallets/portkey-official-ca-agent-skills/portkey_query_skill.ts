#!/usr/bin/env bun
import { Command } from 'commander';
import packageJson from './package.json';
import { getConfig } from './lib/config.js';
import { outputSuccess, outputError, safeJsonParse } from './cli-helpers.js';
import {
  checkAccount,
  getGuardianList,
  getHolderInfo,
  getChainInfo,
  prepareAuthFlow,
} from './src/core/account.js';
import { getTokenBalance, getTokenList, getNftCollections, getNftItems, getTokenPrice } from './src/core/assets.js';
import { callContractViewMethod } from './src/core/contract.js';
import { getTransactionResult } from './src/core/transfer.js';
import { checkManagerSyncState } from './src/core/manager-sync.js';
import { transferPreflight } from './src/core/security.js';
import { validateRpcUrl } from './lib/http.js';
import type { CaAddressInfo, TokenListStrategy } from './lib/types.js';

const program = new Command();
program.name('portkey-query').version(packageJson.version).description('Portkey wallet query tools')
  .option('--network <network>', 'Portkey network (mainnet only)', 'mainnet');

// --- Account ---

program.command('check-account')
  .description('Check if an email is registered')
  .requiredOption('--email <email>', 'Email address')
  .action(async (opts) => {
    try {
      const config = getConfig({ network: program.opts().network });
      outputSuccess(await checkAccount(config, { email: opts.email }));
    } catch (err: any) { outputError(err.message); }
  });

program.command('guardian-list')
  .description('Get guardian list for an account')
  .requiredOption('--identifier <id>', 'Guardian identifier')
  .requiredOption('--chain-id <chainId>', 'Explicit chain ID. Prefer prepare-auth-flow for account-aware routing.')
  .action(async (opts) => {
    try {
      const config = getConfig({ network: program.opts().network });
      outputSuccess(await getGuardianList(config, { identifier: opts.identifier, chainId: opts.chainId }));
    } catch (err: any) { outputError(err.message); }
  });

program.command('prepare-auth-flow')
  .description('Prepare register/recovery flow for an email account and resolve the chain to use')
  .requiredOption('--email <email>', 'Email address')
  .option('--chain-id <chainId>', 'Optional registration chain override for new accounts')
  .action(async (opts) => {
    try {
      const config = getConfig({ network: program.opts().network });
      outputSuccess(await prepareAuthFlow(config, {
        email: opts.email,
        chainId: opts.chainId,
        network: config.network,
      }));
    } catch (err: any) { outputError(err.message); }
  });

program.command('holder-info')
  .description('Get CA holder info from blockchain')
  .requiredOption('--ca-hash <hash>', 'CA hash')
  .requiredOption('--chain-id <chainId>', 'Chain ID')
  .action(async (opts) => {
    try {
      const config = getConfig({ network: program.opts().network });
      outputSuccess(await getHolderInfo(config, { caHash: opts.caHash, chainId: opts.chainId }));
    } catch (err: any) { outputError(err.message); }
  });

program.command('manager-sync-status')
  .description('Check whether a manager address has synced to the CA holder on the target chain. Use managerAddress from recover-and-save or the currently selected signer.')
  .requiredOption('--ca-hash <hash>', 'CA hash')
  .requiredOption('--chain-id <chainId>', 'Target chain ID')
  .requiredOption('--manager-address <addr>', 'Manager wallet address')
  .action(async (opts) => {
    try {
      const config = getConfig({ network: program.opts().network });
      outputSuccess(await checkManagerSyncState(config, {
        caHash: opts.caHash,
        chainId: opts.chainId,
        managerAddress: opts.managerAddress,
      }));
    } catch (err: any) { outputError(err.message); }
  });

program.command('chain-info')
  .description('Get chain configuration info')
  .action(async () => {
    try {
      const config = getConfig({ network: program.opts().network });
      outputSuccess(await getChainInfo(config));
    } catch (err: any) { outputError(err.message); }
  });

// --- Assets ---

program.command('balance')
  .description('Get token balance')
  .requiredOption('--ca-address <addr>', 'CA address')
  .requiredOption('--chain-id <chainId>', 'Chain ID')
  .requiredOption('--symbol <symbol>', 'Token symbol')
  .action(async (opts) => {
    try {
      const config = getConfig({ network: program.opts().network });
      outputSuccess(await getTokenBalance(config, {
        caAddress: opts.caAddress, chainId: opts.chainId, symbol: opts.symbol,
      }));
    } catch (err: any) { outputError(err.message); }
  });

program.command('token-list')
  .description('Get all tokens with balances')
  .requiredOption('--ca-address-infos <json>', 'JSON array of { chainId, caAddress }')
  .option('--strategy <strategy>', 'Strategy: aa | auto | eoa', 'auto')
  .action(async (opts) => {
    try {
      const config = getConfig({ network: program.opts().network });
      outputSuccess(await getTokenList(config, {
        caAddressInfos: safeJsonParse(opts.caAddressInfos, 'ca-address-infos') as CaAddressInfo[],
        strategy: String(opts.strategy || 'auto').toLowerCase() as TokenListStrategy,
      }));
    } catch (err: any) { outputError(err.message); }
  });

program.command('nft-collections')
  .description('Get NFT collections')
  .requiredOption('--ca-address-infos <json>', 'JSON array of { chainId, caAddress }')
  .action(async (opts) => {
    try {
      const config = getConfig({ network: program.opts().network });
      outputSuccess(await getNftCollections(config, {
        caAddressInfos: safeJsonParse(opts.caAddressInfos, 'ca-address-infos') as CaAddressInfo[],
      }));
    } catch (err: any) { outputError(err.message); }
  });

program.command('nft-items')
  .description('Get NFT items in a collection')
  .requiredOption('--ca-address-infos <json>', 'JSON array of { chainId, caAddress }')
  .requiredOption('--symbol <symbol>', 'Collection symbol')
  .action(async (opts) => {
    try {
      const config = getConfig({ network: program.opts().network });
      outputSuccess(await getNftItems(config, {
        caAddressInfos: safeJsonParse(opts.caAddressInfos, 'ca-address-infos') as CaAddressInfo[],
        symbol: opts.symbol,
      }));
    } catch (err: any) { outputError(err.message); }
  });

program.command('token-price')
  .description('Get token prices')
  .requiredOption('--symbols <symbols>', 'Comma-separated token symbols')
  .action(async (opts) => {
    try {
      const config = getConfig({ network: program.opts().network });
      outputSuccess(await getTokenPrice(config, { symbols: opts.symbols.split(',') }));
    } catch (err: any) { outputError(err.message); }
  });

// --- Contract ---

program.command('view-call')
  .description('Call a read-only contract method')
  .requiredOption('--rpc-url <url>', 'RPC endpoint URL')
  .requiredOption('--contract-address <addr>', 'Contract address')
  .requiredOption('--method-name <name>', 'Method name')
  .option('--params <json>', 'JSON parameters')
  .action(async (opts) => {
    try {
      validateRpcUrl(opts.rpcUrl);
      const config = getConfig({ network: program.opts().network });
      outputSuccess(await callContractViewMethod(config, {
        rpcUrl: opts.rpcUrl, contractAddress: opts.contractAddress,
        methodName: opts.methodName,
        params: opts.params ? safeJsonParse(opts.params, 'params') as Record<string, unknown> : undefined,
      }));
    } catch (err: any) { outputError(err.message); }
  });

program.command('tx-result')
  .description('Get transaction result')
  .requiredOption('--tx-id <id>', 'Transaction ID')
  .requiredOption('--chain-id <chainId>', 'Chain ID')
  .action(async (opts) => {
    try {
      const config = getConfig({ network: program.opts().network });
      outputSuccess(await getTransactionResult(config, { txId: opts.txId, chainId: opts.chainId }));
    } catch (err: any) { outputError(err.message); }
  });

program.command('transfer-preflight')
  .description('Check whether a transfer can proceed directly, needs one-time approval, or is blocked by wallet security')
  .requiredOption('--ca-hash <hash>', 'CA hash')
  .requiredOption('--ca-address <addr>', 'CA address on the source chain')
  .requiredOption('--chain-id <chainId>', 'Chain ID')
  .requiredOption('--symbol <symbol>', 'Token symbol')
  .requiredOption('--amount <amount>', 'Amount in smallest unit')
  .action(async (opts) => {
    try {
      const config = getConfig({ network: program.opts().network });
      outputSuccess(await transferPreflight(config, {
        caHash: opts.caHash,
        caAddress: opts.caAddress,
        chainId: opts.chainId,
        symbol: opts.symbol,
        amount: opts.amount,
      }));
    } catch (err: any) { outputError(err.message); }
  });

program.parse();
