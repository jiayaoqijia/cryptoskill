import { getConfig, getTokenContractAddress } from '../core/config.js';
import { callSend, callView } from '../core/chain-client.js';
import { fail, ok, requireField } from '../core/errors.js';
import type {
  ChainId,
  JsonObject,
  SendOptions,
  ToolResult,
} from '../core/types.js';

export interface TokenAllowanceViewInput {
  chainId?: ChainId;
  symbol: string;
  owner: string;
  spender: string;
}

export interface TokenBalanceViewInput {
  chainId?: ChainId;
  symbol: string;
  owner: string;
}

export interface TokenApproveArgsInput {
  spender: string;
  symbol: string;
  amount: number;
}

export interface TokenApproveInput extends SendOptions {
  chainId?: ChainId;
  args: TokenApproveArgsInput;
}

function tokenChain(chainId?: ChainId): ChainId {
  return chainId || getConfig().defaultDaoChain;
}

export async function tokenAllowanceView(
  params: TokenAllowanceViewInput,
): Promise<ToolResult<JsonObject>> {
  try {
    requireField(params.symbol, 'symbol');
    requireField(params.owner, 'owner');
    requireField(params.spender, 'spender');
    const chainId = tokenChain(params.chainId);
    const data = await callView({
      chainId,
      contractAddress: getTokenContractAddress(chainId),
      methodName: 'GetAllowance',
      args: {
        symbol: params.symbol,
        owner: params.owner,
        spender: params.spender,
      },
    });
    return ok((data || {}) as JsonObject);
  } catch (err) {
    return fail(err);
  }
}

export async function tokenBalanceView(
  params: TokenBalanceViewInput,
): Promise<ToolResult<JsonObject>> {
  try {
    requireField(params.symbol, 'symbol');
    requireField(params.owner, 'owner');
    const chainId = tokenChain(params.chainId);
    const data = await callView({
      chainId,
      contractAddress: getTokenContractAddress(chainId),
      methodName: 'GetBalance',
      args: {
        symbol: params.symbol,
        owner: params.owner,
      },
    });
    return ok((data || {}) as JsonObject);
  } catch (err) {
    return fail(err);
  }
}

export async function tokenApprove(
  input: TokenApproveInput,
): Promise<ToolResult<unknown>> {
  try {
    requireField(input.args, 'args');
    requireField(input.args.spender, 'args.spender');
    requireField(input.args.symbol, 'args.symbol');
    requireField(input.args.amount, 'args.amount');
    const chainId = tokenChain(input.chainId);
    const result = await callSend(
      {
        chainId,
        contractAddress: getTokenContractAddress(chainId),
        methodName: 'Approve',
        args: {
          spender: input.args.spender,
          symbol: input.args.symbol,
          amount: input.args.amount,
        },
      },
      input,
    );
    return ok(result.result, { tx: result.tx });
  } catch (err) {
    return fail(err);
  }
}
