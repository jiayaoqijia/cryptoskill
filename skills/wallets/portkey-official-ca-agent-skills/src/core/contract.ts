import type {
  PortkeyConfig,
  ChainId,
  ViewMethodParams,
  ManagerForwardCallParams,
  ManagerSyncCheckResult,
  TransactionFeePreview,
  TransactionResult,
} from '../../lib/types.js';
import {
  callViewMethod as aelfCallViewMethod,
  calculateTransactionFee as aelfCalculateTransactionFee,
  callSendMethod,
  encodeManagerForwardCallParams,
  getWalletByPrivateKey,
  type AElfWallet,
} from '../../lib/aelf-client.js';
import { getChainInfoByChainId } from './account.js';
import {
  normalizeTransferGuardiansApproved,
  toContractApprovedGuardians,
} from './guardian-approval.js';
import { checkManagerSyncState, formatManagerSyncError } from './manager-sync.js';

// ============================================================================
// callViewMethod — generic read-only contract call
// ============================================================================

/**
 * Call a read-only (view) method on any contract.
 *
 * Can be used with explicit rpcUrl + contractAddress, or with chainId
 * (which will auto-resolve the chain's RPC endpoint).
 */
export async function callContractViewMethod<T = unknown>(
  config: PortkeyConfig,
  params: ViewMethodParams,
): Promise<T> {
  if (!params.rpcUrl) throw new Error('rpcUrl is required');
  if (!params.contractAddress) throw new Error('contractAddress is required');
  if (!params.methodName) throw new Error('methodName is required');

  return aelfCallViewMethod<T>(
    params.rpcUrl,
    params.contractAddress,
    params.methodName,
    params.params,
  );
}

/**
 * Convenience: call a view method by chainId (auto-resolves RPC and CA contract).
 */
export async function callCaViewMethod<T = unknown>(
  config: PortkeyConfig,
  chainId: ChainId,
  methodName: string,
  params?: Record<string, unknown>,
): Promise<T> {
  const chainInfo = await getChainInfoByChainId(config, chainId);
  return aelfCallViewMethod<T>(
    chainInfo.endPoint,
    chainInfo.caContractAddress,
    methodName,
    params,
  );
}

// ============================================================================
// managerForwardCall — generic write call through CA contract
// ============================================================================

/**
 * Execute a ManagerForwardCall on the CA contract.
 *
 * This is the core mechanism for all write operations through a Portkey CA wallet.
 * The manager's private key signs the transaction, and the CA contract forwards
 * the call to the target contract on behalf of the CA address.
 *
 * Flow:
 * 1. Get chain info (RPC, CA contract address)
 * 2. Encode target method's args using protobuf
 * 3. Call CA contract's ManagerForwardCall
 * 4. Wait for TX result
 */
export async function managerForwardCall(
  config: PortkeyConfig,
  wallet: AElfWallet,
  params: ManagerForwardCallParams,
): Promise<{
  transactionId: string;
  data: TransactionResult;
  feePreview: TransactionFeePreview | null;
  caAddress: string;
}> {
  if (!params.caHash) throw new Error('caHash is required');
  if (!params.contractAddress) throw new Error('contractAddress is required');
  if (!params.methodName) throw new Error('methodName is required');
  if (!params.chainId) throw new Error('chainId is required');

  const chainInfo = await getChainInfoByChainId(config, params.chainId);
  const managerSync: ManagerSyncCheckResult = params.managerSync ?? await checkManagerSyncState(config, {
    caHash: params.caHash,
    chainId: params.chainId,
    managerAddress: wallet.address,
  });
  if (!managerSync.isManagerSynced) {
    throw new Error(formatManagerSyncError(managerSync));
  }

  // Encode the inner method's args using protobuf
  const encodedParams = await encodeManagerForwardCallParams(chainInfo.endPoint, {
    caHash: params.caHash,
    contractAddress: params.contractAddress,
    methodName: params.methodName,
    args: params.args,
  });
  const guardiansApproved = toContractApprovedGuardians(
    normalizeTransferGuardiansApproved(params.guardiansApproved),
  );
  const payload = guardiansApproved ? { ...encodedParams, guardiansApproved } : encodedParams;

  let feePreview: TransactionFeePreview | null = null;
  try {
    feePreview = await aelfCalculateTransactionFee(
      chainInfo.endPoint,
      chainInfo.caContractAddress,
      wallet,
      'ManagerForwardCall',
      payload,
    );
  } catch {
    feePreview = null;
  }

  // Call ManagerForwardCall on the CA contract
  const txResult = await callSendMethod(
    chainInfo.endPoint,
    chainInfo.caContractAddress,
    wallet,
    'ManagerForwardCall',
    payload,
  );
  return {
    ...txResult,
    feePreview,
    caAddress: managerSync.caAddress,
  };
}

/**
 * Convenience: create a wallet from private key and call managerForwardCall.
 */
export async function managerForwardCallWithKey(
  config: PortkeyConfig,
  privateKey: string,
  params: ManagerForwardCallParams,
): Promise<{
  transactionId: string;
  data: TransactionResult;
  feePreview: TransactionFeePreview | null;
  caAddress: string;
}> {
  const wallet = getWalletByPrivateKey(privateKey);
  return managerForwardCall(config, wallet, params);
}
