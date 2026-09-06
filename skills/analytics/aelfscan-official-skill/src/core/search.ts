import { request } from '../../lib/http-client.js';
import { requireField } from '../../lib/errors.js';
import type { SearchFiltersResponse, SearchResponse } from '../../lib/api-types.js';
import type { SearchFiltersInput, SearchInput, ToolResult } from '../../lib/types.js';
import { executeTool, resolveAddress, resolveChainId } from './common.js';

export async function getSearchFilters(input: SearchFiltersInput = {}): Promise<ToolResult<SearchFiltersResponse>> {
  return executeTool(async (traceId) => {
    const result = await request<SearchFiltersResponse>({
      traceId,
      path: '/api/app/blockchain/filters',
      query: {
        chainId: resolveChainId(input.chainId),
      },
    });

    return result;
  }, 'SEARCH_FILTERS_FAILED');
}

export async function search(input: SearchInput): Promise<ToolResult<SearchResponse>> {
  return executeTool(async (traceId) => {
    requireField(input.keyword, 'keyword');

    const result = await request<SearchResponse>({
      traceId,
      path: '/api/app/blockchain/search',
      query: {
        chainId: resolveChainId(input.chainId),
        keyword: resolveAddress(input.keyword.trim()),
        filterType: input.filterType ?? 0,
        searchType: input.searchType ?? 0,
      },
    });

    return result;
  }, 'SEARCH_FAILED');
}
