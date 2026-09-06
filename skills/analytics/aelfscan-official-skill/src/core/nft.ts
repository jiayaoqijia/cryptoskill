import { request } from '../../lib/http-client.js';
import { requireField } from '../../lib/errors.js';
import type {
  ApiPagedList,
  NftCollectionDetailResponse,
  NftCollectionSummary,
  NftHolderItem,
  NftInventoryItem,
  NftItemDetailResponse,
  NftTransferItem,
} from '../../lib/api-types.js';
import type {
  NftCollectionDetailInput,
  NftCollectionsInput,
  NftHoldersInput,
  NftInventoryInput,
  NftItemActivityInput,
  NftItemDetailInput,
  NftItemHoldersInput,
  NftTransfersInput,
  ToolResult,
} from '../../lib/types.js';
import { executeTool, resolveAddress, resolveChainId, toPaginationQuery } from './common.js';

export async function getNftCollections(
  input: NftCollectionsInput = {},
): Promise<ToolResult<ApiPagedList<NftCollectionSummary>>> {
  return executeTool(async (traceId) => {
    return request<ApiPagedList<NftCollectionSummary>>({
      traceId,
      path: '/api/app/token/nft/collection-list',
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
  }, 'GET_NFT_COLLECTIONS_FAILED');
}

export async function getNftCollectionDetail(
  input: NftCollectionDetailInput,
): Promise<ToolResult<NftCollectionDetailResponse>> {
  return executeTool(async (traceId) => {
    requireField(input.collectionSymbol, 'collectionSymbol');

    return request<NftCollectionDetailResponse>({
      traceId,
      path: '/api/app/token/nft/collection-detail',
      query: {
        chainId: resolveChainId(input.chainId),
        collectionSymbol: input.collectionSymbol,
      },
    });
  }, 'GET_NFT_COLLECTION_DETAIL_FAILED');
}

export async function getNftTransfers(input: NftTransfersInput): Promise<ToolResult<ApiPagedList<NftTransferItem>>> {
  return executeTool(async (traceId) => {
    requireField(input.collectionSymbol, 'collectionSymbol');

    return request<ApiPagedList<NftTransferItem>>({
      traceId,
      path: '/api/app/token/nft/transfers',
      query: {
        chainId: resolveChainId(input.chainId),
        collectionSymbol: input.collectionSymbol,
        search: resolveAddress(input.search),
        address: resolveAddress(input.address),
        ...toPaginationQuery(input),
      },
    });
  }, 'GET_NFT_TRANSFERS_FAILED');
}

export async function getNftHolders(input: NftHoldersInput): Promise<ToolResult<ApiPagedList<NftHolderItem>>> {
  return executeTool(async (traceId) => {
    requireField(input.collectionSymbol, 'collectionSymbol');

    return request<ApiPagedList<NftHolderItem>>({
      traceId,
      path: '/api/app/token/nft/holders',
      query: {
        chainId: resolveChainId(input.chainId),
        collectionSymbol: input.collectionSymbol,
        search: resolveAddress(input.search),
        ...toPaginationQuery(input),
      },
    });
  }, 'GET_NFT_HOLDERS_FAILED');
}

export async function getNftInventory(input: NftInventoryInput): Promise<ToolResult<ApiPagedList<NftInventoryItem>>> {
  return executeTool(async (traceId) => {
    requireField(input.collectionSymbol, 'collectionSymbol');

    return request<ApiPagedList<NftInventoryItem>>({
      traceId,
      path: '/api/app/token/nft/inventory',
      query: {
        chainId: resolveChainId(input.chainId),
        collectionSymbol: input.collectionSymbol,
        search: resolveAddress(input.search),
        ...toPaginationQuery(input),
      },
    });
  }, 'GET_NFT_INVENTORY_FAILED');
}

export async function getNftItemDetail(input: NftItemDetailInput): Promise<ToolResult<NftItemDetailResponse>> {
  return executeTool(async (traceId) => {
    requireField(input.symbol, 'symbol');

    return request<NftItemDetailResponse>({
      traceId,
      path: '/api/app/token/nft/item-detail',
      query: {
        chainId: resolveChainId(input.chainId),
        symbol: input.symbol,
      },
    });
  }, 'GET_NFT_ITEM_DETAIL_FAILED');
}

export async function getNftItemHolders(
  input: NftItemHoldersInput,
): Promise<ToolResult<ApiPagedList<NftHolderItem>>> {
  return executeTool(async (traceId) => {
    requireField(input.symbol, 'symbol');

    return request<ApiPagedList<NftHolderItem>>({
      traceId,
      path: '/api/app/token/nft/item-holders',
      query: {
        chainId: resolveChainId(input.chainId),
        symbol: input.symbol,
        types: input.types,
        ...toPaginationQuery(input),
      },
    });
  }, 'GET_NFT_ITEM_HOLDERS_FAILED');
}

export async function getNftItemActivity(
  input: NftItemActivityInput,
): Promise<ToolResult<ApiPagedList<NftTransferItem>>> {
  return executeTool(async (traceId) => {
    requireField(input.symbol, 'symbol');

    return request<ApiPagedList<NftTransferItem>>({
      traceId,
      path: '/api/app/token/nft/item-activity',
      query: {
        chainId: resolveChainId(input.chainId),
        symbol: input.symbol,
        ...toPaginationQuery(input),
      },
    });
  }, 'GET_NFT_ITEM_ACTIVITY_FAILED');
}
