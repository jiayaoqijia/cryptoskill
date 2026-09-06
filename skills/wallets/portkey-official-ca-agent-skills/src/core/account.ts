import type {
  PortkeyConfig,
  ChainId,
  ChainInfo,
  GuardianItem,
  VerifierItem,
  HolderInfo,
  NetworkType,
} from '../../lib/types.js';
import { createHttpClient, HttpError } from '../../lib/http.js';
import { callViewMethod } from '../../lib/aelf-client.js';
import { SkillError } from './errors.js';
import {
  getWalletProfileByLoginEmail,
  type WalletProfileSummary,
} from './keystore.js';

const ACCOUNT_NOT_FOUND_ERROR_CODE = '3002';

// ============================================================================
// checkAccount
// ============================================================================

export interface CheckAccountParams {
  /** Email address to check */
  email: string;
}

export interface CheckAccountResult {
  /** Whether the account is already registered */
  isRegistered: boolean;
  /** Origin chain ID where the account was first created */
  originChainId: ChainId | null;
}

/**
 * Check if an email account is already registered in Portkey.
 * Returns the originChainId if registered.
 *
 * API: GET /api/app/wallet/getRegisterInfo
 */
export async function checkAccount(
  config: PortkeyConfig,
  params: CheckAccountParams,
): Promise<CheckAccountResult> {
  if (!params.email) throw new SkillError('INVALID_PARAMS', 'email is required');

  const http = createHttpClient(config);

  try {
    const result = await http.get<{ originChainId: ChainId }>('/api/app/account/registerInfo', {
      params: { loginGuardianIdentifier: params.email },
    });
    // Defensive: API should always return originChainId for registered accounts,
    // but guard against unexpected null/undefined responses.
    if (!result || !result.originChainId) {
      return { isRegistered: false, originChainId: null };
    }
    return {
      isRegistered: true,
      originChainId: result.originChainId,
    };
  } catch (err: unknown) {
    // Account not found: prefer structured HttpError matching, fallback to message
    if (err instanceof HttpError) {
      if (err.statusCode === 404 || err.errorCode === ACCOUNT_NOT_FOUND_ERROR_CODE) {
        return { isRegistered: false, originChainId: null };
      }
    } else if (
      err instanceof Error &&
      (
        err.message.includes(ACCOUNT_NOT_FOUND_ERROR_CODE) ||
        /not exist|guardian not exist/i.test(err.message)
      )
    ) {
      // Legacy fallback for non-HttpError paths
      return { isRegistered: false, originChainId: null };
    }
    throw err;
  }
}

// ============================================================================
// getGuardianList
// ============================================================================

export interface GetGuardianListParams {
  /** Guardian identifier (email, phone, or social ID) */
  identifier: string;
  /** Chain ID to query guardians from */
  chainId: ChainId;
}

export interface GuardianListItem {
  guardianIdentifier: string;
  identifierHash: string;
  isLoginGuardian: boolean;
  salt: string;
  /** Guardian type as string label (e.g. "Email", "Phone", "Google") */
  type: string;
  verifierId: string;
  /** Optional fields returned by API */
  thirdPartyEmail?: string | null;
  isPrivate?: boolean | null;
  firstName?: string | null;
  lastName?: string | null;
}

export interface GetGuardianListResult {
  guardians: GuardianListItem[];
  /** CA hash (returned when account is found) */
  caHash?: string;
  /** CA address (returned when account is found) */
  caAddress?: string;
  /** Chain where the CA was created */
  createChainId?: ChainId;
}

export interface PrepareAuthFlowParams {
  email: string;
  network: NetworkType;
  chainId?: ChainId;
}

export interface PrepareAuthFlowResult {
  email: string;
  isRegistered: boolean;
  recommendedFlow: 'register' | 'recovery';
  originChainId: ChainId | null;
  resolvedChainId: ChainId;
  caHash?: string;
  caAddress?: string;
  guardians?: GuardianListItem[];
  matchedLocalProfile?: WalletProfileSummary | null;
}

/**
 * Get all guardians associated with an account.
 *
 * API: GET /api/app/account/guardianIdentifiers
 */
export async function getGuardianList(
  config: PortkeyConfig,
  params: GetGuardianListParams,
): Promise<GetGuardianListResult> {
  if (!params.identifier) throw new Error('identifier is required');
  if (!params.chainId) throw new Error('chainId is required');

  const http = createHttpClient(config);

  const result = await http.get<{
    guardianList?: { guardians: GuardianListItem[] };
    guardianAccounts?: GuardianListItem[];
    caHash?: string;
    caAddress?: string;
    createChainId?: ChainId;
  }>('/api/app/account/guardianIdentifiers', {
    params: {
      guardianIdentifier: params.identifier,
      chainId: params.chainId,
    },
  });

  // Normalize response - API may return in different formats
  const guardians =
    result.guardianList?.guardians || result.guardianAccounts || [];

  return {
    guardians,
    caHash: result.caHash,
    caAddress: result.caAddress,
    createChainId: result.createChainId,
  };
}

export async function prepareAuthFlow(
  config: PortkeyConfig,
  params: PrepareAuthFlowParams,
): Promise<PrepareAuthFlowResult> {
  if (!params.email) throw new SkillError('INVALID_PARAMS', 'email is required');
  if (!params.network) throw new SkillError('INVALID_PARAMS', 'network is required');

  const matchedLocalProfile = getWalletProfileByLoginEmail(
    params.network,
    params.email,
  );
  const account = await checkAccount(config, { email: params.email });
  const resolvedChainId = account.isRegistered
    ? account.originChainId!
    : (params.chainId || 'tDVV');

  if (!account.isRegistered) {
    return {
      email: params.email,
      isRegistered: false,
      recommendedFlow: 'register',
      originChainId: account.originChainId,
      resolvedChainId,
      matchedLocalProfile,
    };
  }

  const guardianList = await getGuardianList(config, {
    identifier: params.email,
    chainId: resolvedChainId,
  });

  return {
    email: params.email,
    isRegistered: true,
    recommendedFlow: 'recovery',
    originChainId: guardianList.createChainId || account.originChainId,
    resolvedChainId,
    caHash: guardianList.caHash,
    caAddress: guardianList.caAddress,
    guardians: guardianList.guardians,
    matchedLocalProfile,
  };
}

// ============================================================================
// getHolderInfo
// ============================================================================

export interface GetHolderInfoParams {
  /** CA hash */
  caHash: string;
  /** Chain ID */
  chainId: ChainId;
}

/**
 * Get CA holder info directly from the blockchain (on-chain view call).
 * Returns guardian list, manager list, CA address, etc.
 *
 * Contract: GetHolderInfo (view method on CA contract)
 */
export async function getHolderInfo(
  config: PortkeyConfig,
  params: GetHolderInfoParams,
): Promise<HolderInfo> {
  if (!params.caHash) throw new Error('caHash is required');
  if (!params.chainId) throw new Error('chainId is required');

  // First get chain info to find the CA contract address and RPC endpoint
  const chainInfo = await getChainInfoByChainId(config, params.chainId);

  const result = await callViewMethod<HolderInfo>(
    chainInfo.endPoint,
    chainInfo.caContractAddress,
    'GetHolderInfo',
    { caHash: params.caHash },
  );

  if (!result || !result.caHash) {
    throw new Error(`Holder not found for caHash: ${params.caHash}`);
  }

  return result;
}

// ============================================================================
// getChainInfo
// ============================================================================

// Process-level cache — ChainInfo is static config (endpoints, contract addresses),
// does NOT contain block height. Safe to cache for the entire process lifetime.
const chainInfoCache = new Map<string, ChainInfo[]>();

/**
 * Get chain info for all available chains (RPC endpoints, contract addresses).
 * Results are cached per apiUrl for the process lifetime.
 *
 * API: GET /api/app/search/chainsinfoindex
 */
export async function getChainInfo(
  config: PortkeyConfig,
): Promise<ChainInfo[]> {
  const key = config.apiUrl;
  const cached = chainInfoCache.get(key);
  if (cached) return cached;

  const http = createHttpClient(config);
  const result = await http.get<{ items: ChainInfo[] }>('/api/app/search/chainsinfoindex');
  const data = result.items || [];
  chainInfoCache.set(key, data);
  return data;
}

/** Clear chain info cache (e.g. after config/network change). */
export function clearChainInfoCache(): void {
  chainInfoCache.clear();
}

/**
 * Get chain info for a specific chain ID.
 */
export async function getChainInfoByChainId(
  config: PortkeyConfig,
  chainId: ChainId,
): Promise<ChainInfo> {
  const chains = await getChainInfo(config);
  const chain = chains.find((c) => c.chainId === chainId);
  if (!chain) {
    throw new Error(`Chain "${chainId}" not found. Available: ${chains.map((c) => c.chainId).join(', ')}`);
  }
  return chain;
}
