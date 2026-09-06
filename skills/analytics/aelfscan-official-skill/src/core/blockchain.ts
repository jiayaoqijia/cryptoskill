import { request } from '../../lib/http-client.js';
import { requireField, SkillError } from '../../lib/errors.js';
import type {
  AddressDictionaryResponse,
  BlockDetailResponse,
  BlockchainOverviewResponse,
  BlockListResponse,
  LogEventsResponse,
  TransactionDataChartResponse,
  TransactionDetailResponse,
  TransactionListResponse,
} from '../../lib/api-types.js';
import type {
  AddressDictionaryInput,
  BlockchainOverviewInput,
  BlockDetailInput,
  BlocksInput,
  LogEventsInput,
  ToolResult,
  TransactionDataChartInput,
  TransactionDetailInput,
  TransactionsInput,
} from '../../lib/types.js';
import { executeTool, resolveChainId, toPaginationQuery } from './common.js';

export async function getBlocks(input: BlocksInput = {}): Promise<ToolResult<BlockListResponse>> {
  return executeTool(async (traceId) => {
    const result = await request<BlockListResponse>({
      traceId,
      path: '/api/app/blockchain/blocks',
      query: {
        chainId: resolveChainId(input.chainId),
        ...toPaginationQuery(input),
        isLastPage: input.isLastPage,
      },
    });

    return result;
  }, 'GET_BLOCKS_FAILED');
}

export async function getLatestBlocks(input: Omit<BlocksInput, 'skipCount'> = {}): Promise<ToolResult<BlockListResponse>> {
  return getBlocks({
    ...input,
    skipCount: 0,
    maxResultCount: input.maxResultCount ?? 6,
  });
}

export async function getBlockDetail(input: BlockDetailInput): Promise<ToolResult<BlockDetailResponse>> {
  return executeTool(async (traceId) => {
    requireField(input.blockHeight, 'blockHeight');

    const result = await request<BlockDetailResponse>({
      traceId,
      path: '/api/app/blockchain/blockDetail',
      query: {
        chainId: resolveChainId(input.chainId),
        blockHeight: input.blockHeight,
      },
    });

    return result;
  }, 'GET_BLOCK_DETAIL_FAILED');
}

export async function getTransactions(input: TransactionsInput = {}): Promise<ToolResult<TransactionListResponse>> {
  return executeTool(async (traceId) => {
    const result = await request<TransactionListResponse>({
      traceId,
      path: '/api/app/blockchain/transactions',
      query: {
        chainId: resolveChainId(input.chainId),
        ...toPaginationQuery(input),
        transactionId: input.transactionId,
        blockHeight: input.blockHeight,
        address: input.address,
        startTime: input.startTime,
        endTime: input.endTime,
      },
    });

    return result;
  }, 'GET_TRANSACTIONS_FAILED');
}

export async function getLatestTransactions(
  input: Omit<TransactionsInput, 'skipCount'> = {},
): Promise<ToolResult<TransactionListResponse>> {
  return getTransactions({
    ...input,
    skipCount: 0,
    maxResultCount: input.maxResultCount ?? 6,
  });
}

export async function getTransactionDetail(input: TransactionDetailInput): Promise<ToolResult<TransactionDetailResponse>> {
  return executeTool(async (traceId) => {
    requireField(input.transactionId, 'transactionId');

    const result = await request<TransactionDetailResponse>({
      traceId,
      path: '/api/app/blockchain/transactionDetail',
      query: {
        chainId: resolveChainId(input.chainId),
        transactionId: input.transactionId,
        blockHeight: input.blockHeight,
      },
    });

    return result;
  }, 'GET_TRANSACTION_DETAIL_FAILED');
}

export async function getBlockchainOverview(
  input: BlockchainOverviewInput = {},
): Promise<ToolResult<BlockchainOverviewResponse>> {
  return executeTool(async (traceId) => {
    const result = await request<BlockchainOverviewResponse>({
      traceId,
      method: 'POST',
      path: '/api/app/blockchain/blockchainOverview',
      body: {
        ...input,
        chainId: resolveChainId(input.chainId),
      },
    });

    return result;
  }, 'GET_BLOCKCHAIN_OVERVIEW_FAILED');
}

export async function getTransactionDataChart(
  input: TransactionDataChartInput = {},
): Promise<ToolResult<TransactionDataChartResponse>> {
  return executeTool(async (traceId) => {
    const result = await request<TransactionDataChartResponse>({
      traceId,
      method: 'POST',
      path: '/api/app/blockchain/transactionDataChart',
      body: {
        ...input,
        chainId: resolveChainId(input.chainId),
      },
    });

    return result;
  }, 'GET_TRANSACTION_DATA_CHART_FAILED');
}

export async function getAddressDictionary(input: AddressDictionaryInput): Promise<ToolResult<AddressDictionaryResponse>> {
  return executeTool(async (traceId) => {
    requireField(input.name, 'name');
    const addresses = requireField(input.addresses, 'addresses');
    if (!Array.isArray(addresses) || addresses.length === 0) {
      throw new SkillError('INVALID_INPUT', 'addresses must be a non-empty array');
    }

    const result = await request<AddressDictionaryResponse>({
      traceId,
      method: 'POST',
      path: '/api/app/blockchain/addressDictionary',
      body: {
        ...input,
        chainId: resolveChainId(input.chainId),
      },
    });

    return result;
  }, 'GET_ADDRESS_DICTIONARY_FAILED');
}

export async function getLogEvents(input: LogEventsInput): Promise<ToolResult<LogEventsResponse>> {
  return executeTool(async (traceId) => {
    requireField(input.contractAddress, 'contractAddress');

    const result = await request<LogEventsResponse>({
      traceId,
      method: 'POST',
      path: '/api/app/blockchain/logEvents',
      body: {
        ...input,
        chainId: resolveChainId(input.chainId),
        contractAddress: input.contractAddress,
        ...toPaginationQuery(input),
      },
    });

    return result;
  }, 'GET_LOG_EVENTS_FAILED');
}
