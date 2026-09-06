// ============================================================
// Awaken OpenClaw Skills - aelf SDK Client
// ============================================================
// Wraps aelf-sdk for both view (read) and send (write) contract calls.
// Supports both EOA and CA wallets via @portkey/aelf-signer.

import AElf from 'aelf-sdk';
import BigNumber from 'bignumber.js';
import type { AelfSigner } from '@portkey/aelf-signer';
import type { NetworkConfig, TxResult } from './types';

// ---- Caches ----
const aelfInstances: Record<string, any> = {};
const viewContracts: Record<string, any> = {};

// ---- AElf Instance ----

export function getAElfInstance(rpcUrl: string) {
  if (!aelfInstances[rpcUrl]) {
    aelfInstances[rpcUrl] = new AElf(new AElf.providers.HttpProvider(rpcUrl));
  }
  return aelfInstances[rpcUrl];
}

// ---- Wallets ----

let _viewWallet: any = null;
export function getViewWallet() {
  if (!_viewWallet) _viewWallet = AElf.wallet.createNewWallet();
  return _viewWallet;
}

export function getWalletByPrivateKey(privateKey?: string) {
  const pk = privateKey || process.env.AELF_PRIVATE_KEY;
  if (!pk) {
    throw new Error('[ERROR] AELF_PRIVATE_KEY environment variable is required for send transactions.');
  }
  return AElf.wallet.getWalletByPrivateKey(pk);
}

// ---- View Contract ----

export async function getViewContract(rpcUrl: string, contractAddress: string) {
  const key = `${rpcUrl}:${contractAddress}`;
  if (!viewContracts[key]) {
    const aelf = getAElfInstance(rpcUrl);
    const wallet = getViewWallet();
    viewContracts[key] = await aelf.chain.contractAt(contractAddress, wallet);
  }
  return viewContracts[key];
}

export async function callViewMethod(
  rpcUrl: string,
  contractAddress: string,
  methodName: string,
  args?: any,
): Promise<any> {
  const contract = await getViewContract(rpcUrl, contractAddress);
  return contract[methodName].call(args);
}

// ---- Send Contract ----

export async function callSendMethod(
  rpcUrl: string,
  contractAddress: string,
  methodName: string,
  wallet: any,
  args?: any,
): Promise<any> {
  const aelf = getAElfInstance(rpcUrl);
  const contract = await aelf.chain.contractAt(contractAddress, wallet);
  return contract[methodName](args);
}

// ---- TX Result Polling ----

export async function getTxResult(
  rpcUrl: string,
  transactionId: string,
  maxRetries = 30,
): Promise<TxResult> {
  const aelf = getAElfInstance(rpcUrl);

  for (let i = 0; i < maxRetries; i++) {
    try {
      const result = await aelf.chain.getTxResult(transactionId);
      const status = (result?.Status || result?.result?.Status || '').toLowerCase();

      if (status === 'mined') {
        return { transactionId, status: 'mined' };
      }
      if (status === 'failed' || status === 'nodevalidationfailed') {
        const error = result?.Error || result?.result?.Error || 'Transaction failed';
        throw new Error(`[ERROR] TX ${transactionId} failed: ${error}`);
      }
      // pending / notexisted - keep waiting
    } catch (err: any) {
      if (err.message?.startsWith('[ERROR]')) throw err;
      // network error, retry
    }
    await sleep(1000);
  }
  throw new Error(`[ERROR] TX ${transactionId} did not confirm after ${maxRetries}s`);
}

// ---- Balance & Allowance ----

export async function getBalance(
  rpcUrl: string,
  tokenContract: string,
  symbol: string,
  owner: string,
): Promise<string> {
  const result = await callViewMethod(rpcUrl, tokenContract, 'GetBalance', { symbol, owner });
  return result?.balance ?? result?.amount ?? '0';
}

export async function getAllowance(
  rpcUrl: string,
  tokenContract: string,
  symbol: string,
  owner: string,
  spender: string,
): Promise<string> {
  const result = await callViewMethod(rpcUrl, tokenContract, 'GetAllowance', { symbol, owner, spender });
  return result?.allowance ?? '0';
}

export async function getTokenInfo(
  rpcUrl: string,
  tokenContract: string,
  symbol: string,
): Promise<{ symbol: string; decimals: number }> {
  const result = await callViewMethod(rpcUrl, tokenContract, 'GetTokenInfo', { symbol });
  return {
    symbol: result?.symbol ?? symbol,
    decimals: result?.decimals ?? 8,
  };
}

// ---- Approve ----

/**
 * Approve a contract to spend tokens.
 * Accepts AelfSigner (EOA or CA) — signing is handled transparently.
 */
export async function approveToken(
  config: NetworkConfig,
  signer: AelfSigner,
  symbol: string,
  spender: string,
  amount: string,
): Promise<TxResult> {
  const result = await signer.sendContractCall(config.rpcUrl, config.tokenContract, 'Approve', {
    symbol,
    spender,
    amount,
  });
  return {
    transactionId: result.transactionId,
    status: (result.txResult.Status || 'mined').toLowerCase(),
  };
}

// ---- Utility ----

export function timesDecimals(value: string | number, decimals: number): BigNumber {
  return new BigNumber(value).times(new BigNumber(10).pow(decimals));
}

export function divDecimals(value: string | number, decimals: number): BigNumber {
  return new BigNumber(value).div(new BigNumber(10).pow(decimals));
}

function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

// Note: outputSuccess/outputError moved to cli-helpers.ts (CLI adapter layer only)
