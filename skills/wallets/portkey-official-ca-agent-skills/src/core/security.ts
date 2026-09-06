import type {
  PortkeyConfig,
  TransferSecurityCheckParams,
  TransferSecurityCheckResult,
  TransferLimitCheckParams,
  TransferLimitCheckResult,
  TransferPreflightParams,
  TransferPreflightResult,
} from '../../lib/types.js';
import { createHttpClient } from '../../lib/http.js';
import { callViewMethod } from '../../lib/aelf-client.js';
import { getChainInfoByChainId } from './account.js';
import { getTokenBalance } from './assets.js';

const MAX_TRANSACTION_FEE = '0.1';

type RawTransferLimit = {
  dailyLimit?: string | number;
  singleLimit?: string | number;
  dailyTransferredAmount?: string | number;
};

type RawDefaultTransferLimit = {
  transferLimit?: {
    dayLimit?: string | number;
    singleLimit?: string | number;
  };
};

/**
 * Query wallet security state for a transfer target chain.
 *
 * API: GET /api/app/user/security/balanceCheck
 */
export async function checkTransferSecurity(
  config: PortkeyConfig,
  params: TransferSecurityCheckParams,
): Promise<TransferSecurityCheckResult> {
  if (!params.caHash) throw new Error('caHash is required');
  if (!params.chainId) throw new Error('chainId is required');

  const http = createHttpClient(config);

  const result = await http.get<TransferSecurityCheckResult>('/api/app/user/security/balanceCheck', {
    params: {
      caHash: params.caHash,
      checkTransferSafeChainId: params.chainId,
    },
  });

  return {
    isTransferSafe: !!result?.isTransferSafe,
    isSynchronizing: !!result?.isSynchronizing,
    isOriginChainSafe: !!result?.isOriginChainSafe,
    accelerateGuardians: Array.isArray(result?.accelerateGuardians) ? result.accelerateGuardians : [],
  };
}

/**
 * Query chain transfer limits and decide whether one-time approval is available.
 *
 * Uses on-chain reads:
 * - CA.GetTransferLimit
 * - CA.GetDefaultTokenTransferLimit
 * - Token.GetBalance / Token.GetTokenInfo
 */
export async function checkTransferLimit(
  config: PortkeyConfig,
  params: TransferLimitCheckParams,
): Promise<TransferLimitCheckResult> {
  if (!params.caHash) throw new Error('caHash is required');
  if (!params.caAddress) throw new Error('caAddress is required');
  if (!params.symbol) throw new Error('symbol is required');
  if (!params.amount) throw new Error('amount is required');
  if (!params.chainId) throw new Error('chainId is required');

  const chainInfo = await getChainInfoByChainId(config, params.chainId);
  const feeSymbol = chainInfo.defaultToken.symbol;
  const [tokenBalance, feeTokenBalance] = await Promise.all([
    getTokenBalance(config, {
      caAddress: params.caAddress,
      chainId: params.chainId,
      symbol: params.symbol,
    }),
    params.symbol === feeSymbol
      ? Promise.resolve(null)
      : getTokenBalance(config, {
        caAddress: params.caAddress,
        chainId: params.chainId,
        symbol: feeSymbol,
      }),
  ]);
  const resolvedFeeTokenBalance = feeTokenBalance ?? tokenBalance;

  const [limitInfo, defaultLimitInfo] = await Promise.all([
    callViewMethod<RawTransferLimit>(
      chainInfo.endPoint,
      chainInfo.caContractAddress,
      'GetTransferLimit',
      {
        caHash: params.caHash,
        symbol: params.symbol,
      },
    ),
    callViewMethod<RawDefaultTransferLimit>(
      chainInfo.endPoint,
      chainInfo.caContractAddress,
      'GetDefaultTokenTransferLimit',
      {
        caHash: params.caHash,
        symbol: params.symbol,
      },
    ).catch(() => ({})),
  ]);
  const defaultTransferLimit =
    defaultLimitInfo && typeof defaultLimitInfo === 'object' && 'transferLimit' in defaultLimitInfo
      ? defaultLimitInfo.transferLimit
      : undefined;

  const amount = toBigIntStrict(params.amount, 'amount');
  const transferBalance = toBigIntStrict(tokenBalance.balance, 'balance');
  const feeBalance = toBigIntStrict(resolvedFeeTokenBalance.balance, 'feeBalance');
  const dailyLimit = parseOptionalBigInt(limitInfo?.dailyLimit);
  const dailyTransferredAmount = parseOptionalBigInt(limitInfo?.dailyTransferredAmount) ?? 0n;
  const singleLimit = parseOptionalBigInt(limitInfo?.singleLimit);
  const defaultDailyLimit = parseOptionalBigInt(defaultTransferLimit?.dayLimit);
  const defaultSingleLimit = parseOptionalBigInt(defaultTransferLimit?.singleLimit);

  if (dailyLimit === null || singleLimit === null) {
    throw new Error(`Failed to fetch transfer limit for ${params.symbol} on ${params.chainId}`);
  }

  const dailyBalance = dailyLimit === -1n ? -1n : dailyLimit - dailyTransferredAmount;
  const feeBuffer = scaleDecimalString(MAX_TRANSACTION_FEE, resolvedFeeTokenBalance.decimals);
  const isDailyLimited = dailyLimit !== -1n && amount > dailyBalance;
  const isSingleLimited = singleLimit !== -1n && amount > singleLimit;
  const canApprove = params.symbol === feeSymbol
    ? amount + feeBuffer <= transferBalance
    : amount <= transferBalance && feeBuffer <= feeBalance;

  return {
    symbol: params.symbol,
    chainId: params.chainId,
    amount: params.amount,
    balance: tokenBalance.balance,
    decimals: tokenBalance.decimals,
    tokenContractAddress: tokenBalance.tokenContractAddress,
    feeSymbol,
    feeBalance: resolvedFeeTokenBalance.balance,
    feeDecimals: resolvedFeeTokenBalance.decimals,
    feeTokenContractAddress: resolvedFeeTokenBalance.tokenContractAddress,
    dailyLimit: dailyLimit.toString(),
    dailyBalance: dailyBalance.toString(),
    singleLimit: singleLimit.toString(),
    defaultDailyLimit: defaultDailyLimit?.toString() ?? null,
    defaultSingleLimit: defaultSingleLimit?.toString() ?? null,
    isDailyLimited,
    isSingleLimited,
    canApprove,
    feeBuffer: feeBuffer.toString(),
  };
}

/**
 * Perform the same high-level transfer decisioning as the CA app:
 * 1. wallet security gate
 * 2. transfer-limit gate
 */
export async function transferPreflight(
  config: PortkeyConfig,
  params: TransferPreflightParams,
): Promise<TransferPreflightResult> {
  const walletSecurity = await checkTransferSecurity(config, {
    caHash: params.caHash,
    chainId: params.chainId,
  });

  if (!walletSecurity.isTransferSafe) {
    if (walletSecurity.isSynchronizing && walletSecurity.isOriginChainSafe) {
      return {
        decision: 'needs_security_sync',
        reason: 'Wallet security upgrade is still synchronizing to the target chain.',
        walletSecurity,
      };
    }

    return {
      decision: 'needs_add_guardian',
      reason: 'Wallet security level is too low for this transfer.',
      walletSecurity,
    };
  }

  const transferLimit = await checkTransferLimit(config, params);
  if (transferLimit.isDailyLimited || transferLimit.isSingleLimited) {
    return {
      decision: transferLimit.canApprove
        ? 'needs_one_time_approval'
        : 'needs_limit_modification',
      reason: transferLimit.canApprove
        ? 'Transfer limit exceeded; one-time guardian approval is available.'
        : 'Transfer limit exceeded and balance is insufficient to cover amount plus fee buffer.',
      walletSecurity,
      transferLimit,
    };
  }

  return {
    decision: 'direct_transfer',
    reason: 'Wallet security and transfer limits both allow direct transfer.',
    walletSecurity,
    transferLimit,
  };
}

function parseOptionalBigInt(value: unknown): bigint | null {
  if (value === null || value === undefined || value === '') return null;
  try {
    return BigInt(String(value));
  } catch {
    return null;
  }
}

function toBigIntStrict(value: string, field: string): bigint {
  try {
    return BigInt(String(value));
  } catch {
    throw new Error(`${field} must be an integer string in smallest unit`);
  }
}

function scaleDecimalString(value: string, decimals: number): bigint {
  const text = String(value || '').trim();
  if (!/^\d+(\.\d+)?$/.test(text)) {
    throw new Error(`Invalid decimal amount: ${value}`);
  }

  const [whole, fraction = ''] = text.split('.');
  const paddedFraction = `${fraction}${'0'.repeat(decimals)}`.slice(0, decimals);
  return BigInt(`${whole}${paddedFraction}`.replace(/^0+(?=\d)/, '') || '0');
}
