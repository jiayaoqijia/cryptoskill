import { request } from '../../lib/http-client.js';
import { requireField } from '../../lib/errors.js';
import type { ApiPagedList, TokenDetailResponse, TokenHolderItem, TokenSummary, TokenTransferItem } from '../../lib/api-types.js';
import type { TokenDetailInput, TokenHoldersInput, TokenListInput, TokenTransfersInput, ToolResult } from '../../lib/types.js';
import { executeTool, resolveAddress, resolveChainId, toPaginationQuery } from './common.js';

export async function getTokens(input: TokenListInput = {}): Promise<ToolResult<ApiPagedList<TokenSummary>>> {
  return executeTool(async (traceId) => {
    return request<ApiPagedList<TokenSummary>>({
      traceId,
      path: '/api/app/token/list',
      query: {
        chainId: resolveChainId(input.chainId),
        ...toPaginationQuery(input),
        types: input.types,
        symbols: input.symbols,
        collectionSymbols: input.collectionSymbols,
        search: input.search,
        exactSearch: input.exactSearch,
        fuzzySearch: input.fuzzySearch,
        beginBlockTime: input.beginBlockTime,
      },
    });
  }, 'GET_TOKENS_FAILED');
}

export async function getTokenDetail(input: TokenDetailInput): Promise<ToolResult<TokenDetailResponse>> {
  return executeTool(async (traceId) => {
    requireField(input.symbol, 'symbol');

    return request<TokenDetailResponse>({
      traceId,
      path: '/api/app/token/detail',
      query: {
        chainId: resolveChainId(input.chainId),
        symbol: input.symbol,
      },
    });
  }, 'GET_TOKEN_DETAIL_FAILED');
}

export async function getTokenTransfers(input: TokenTransfersInput): Promise<ToolResult<ApiPagedList<TokenTransferItem>>> {
  return executeTool(async (traceId) => {
    requireField(input.symbol, 'symbol');

    return request<ApiPagedList<TokenTransferItem>>({
      traceId,
      path: '/api/app/token/transfers',
      query: {
        chainId: resolveChainId(input.chainId),
        symbol: input.symbol,
        search: resolveAddress(input.search),
        collectionSymbol: input.collectionSymbol,
        address: resolveAddress(input.address),
        types: input.types,
        fuzzySearch: input.fuzzySearch,
        beginBlockTime: input.beginBlockTime,
        ...toPaginationQuery(input),
      },
    });
  }, 'GET_TOKEN_TRANSFERS_FAILED');
}

export async function getTokenHolders(input: TokenHoldersInput): Promise<ToolResult<ApiPagedList<TokenHolderItem>>> {
  return executeTool(async (traceId) => {
    return request<ApiPagedList<TokenHolderItem>>({
      traceId,
      path: '/api/app/token/holders',
      query: {
        chainId: resolveChainId(input.chainId),
        symbol: input.symbol,
        collectionSymbol: input.collectionSymbol,
        address: resolveAddress(input.address),
        partialSymbol: input.partialSymbol,
        search: resolveAddress(input.search),
        types: input.types,
        symbols: input.symbols,
        addressList: input.addressList,
        searchSymbols: input.searchSymbols,
        fuzzySearch: input.fuzzySearch,
        amountGreaterThanZero: input.amountGreaterThanZero,
        ...toPaginationQuery(input),
      },
    });
  }, 'GET_TOKEN_HOLDERS_FAILED');
}
