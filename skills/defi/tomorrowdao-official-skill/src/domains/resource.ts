import { CONTRACTS, getConfig } from '../core/config.js';
import { callSend } from '../core/chain-client.js';
import { fail, ok, requireField, SkillError } from '../core/errors.js';
import { apiGet } from '../core/http.js';
import type {
  ChainId,
  ExecutionMode,
  JsonObject,
  PagedResponse,
  SignerContextInput,
  ToolResult,
} from '../core/types.js';

type SignerAware = {
  signer?: SignerContextInput;
  signerContext?: SignerContextInput;
};

function resourceChain(chainId?: ChainId): ChainId {
  return chainId || getConfig().defaultNetworkChain;
}

function ensureAelf(chainId: ChainId): ChainId {
  if (chainId !== 'AELF') throw new SkillError('UNSUPPORTED_CHAIN', `resource domain only supports AELF, got ${chainId}`);
  return chainId;
}

function validateTradeInput(symbol: string, amount: number): void {
  requireField(symbol, 'symbol');
  if (!Number.isFinite(amount) || amount <= 0) {
    throw new SkillError('INVALID_INPUT', 'amount must be a positive number');
  }
}

function sendOptions(input: SignerAware & { mode?: ExecutionMode }) {
  return {
    mode: input.mode || 'simulate',
    signer: input.signer,
    signerContext: input.signerContext,
  };
}

export async function resourceBuy(input: {
  chainId?: ChainId;
  symbol: string;
  amount: number;
  mode?: ExecutionMode;
} & SignerAware): Promise<ToolResult<JsonObject>> {
  try {
    validateTradeInput(input.symbol, input.amount);
    const chainId = ensureAelf(resourceChain(input.chainId));
    const result = await callSend(
      {
        chainId,
        contractAddress: CONTRACTS.network.AELF.tokenConverter,
        methodName: 'Buy',
        args: {
          symbol: input.symbol,
          amount: input.amount,
        },
      },
      sendOptions(input),
    );
    return ok((result.result || {}) as JsonObject, { tx: result.tx });
  } catch (err) {
    return fail(err);
  }
}

export async function resourceSell(input: {
  chainId?: ChainId;
  symbol: string;
  amount: number;
  mode?: ExecutionMode;
} & SignerAware): Promise<ToolResult<JsonObject>> {
  try {
    validateTradeInput(input.symbol, input.amount);
    const chainId = ensureAelf(resourceChain(input.chainId));
    const result = await callSend(
      {
        chainId,
        contractAddress: CONTRACTS.network.AELF.tokenConverter,
        methodName: 'Sell',
        args: {
          symbol: input.symbol,
          amount: input.amount,
        },
      },
      sendOptions(input),
    );
    return ok((result.result || {}) as JsonObject, { tx: result.tx });
  } catch (err) {
    return fail(err);
  }
}

export async function resourceRealtimeRecords(input: {
  chainId?: ChainId;
  maxResultCount?: number;
  skipCount?: number;
}): Promise<ToolResult<PagedResponse>> {
  try {
    const data = await apiGet<PagedResponse>('/resource/realtime-records', {
      chainId: resourceChain(input.chainId),
      skipCount: input.skipCount || 0,
      maxResultCount: input.maxResultCount || 20,
    });
    return ok(data);
  } catch (err) {
    return fail(err);
  }
}

export async function resourceTurnover(input: {
  chainId?: ChainId;
  symbol?: string;
}): Promise<ToolResult<JsonObject>> {
  try {
    const data = await apiGet<JsonObject>('/resource/turnover', {
      chainId: resourceChain(input.chainId),
      symbol: input.symbol,
    });
    return ok(data);
  } catch (err) {
    return fail(err);
  }
}

export async function resourceRecords(input: {
  chainId?: ChainId;
  maxResultCount?: number;
  skipCount?: number;
  symbol?: string;
}): Promise<ToolResult<PagedResponse>> {
  try {
    const data = await apiGet<PagedResponse>('/resource/records', {
      chainId: resourceChain(input.chainId),
      skipCount: input.skipCount || 0,
      maxResultCount: input.maxResultCount || 20,
      symbol: input.symbol,
    });
    return ok(data);
  } catch (err) {
    return fail(err);
  }
}
