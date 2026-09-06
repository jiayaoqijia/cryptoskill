import { z } from 'zod';
import type { ToolResult } from '../../lib/types.js';
import {
  getAccounts,
  getAddressDetail,
  getAddressNftAssets,
  getAddressTokens,
  getAddressTransfers,
  getContractEvents,
  getContractHistory,
  getContracts,
  getContractSource,
} from '../core/address.js';
import {
  getAddressDictionary,
  getBlockDetail,
  getBlockchainOverview,
  getBlocks,
  getLatestBlocks,
  getLatestTransactions,
  getLogEvents,
  getTransactionDataChart,
  getTransactionDetail,
  getTransactions,
} from '../core/blockchain.js';
import {
  getNftCollectionDetail,
  getNftCollections,
  getNftHolders,
  getNftInventory,
  getNftItemActivity,
  getNftItemDetail,
  getNftItemHolders,
  getNftTransfers,
} from '../core/nft.js';
import { getSearchFilters, search } from '../core/search.js';
import {
  getAvgBlockDuration,
  getBlockProduceRate,
  getCurrencyPrice,
  getCycleCount,
  getDailyActiveAddresses,
  getDailyActivityAddress,
  getDailyAvgBlockSize,
  getDailyAvgTransactionFee,
  getDailyBlockReward,
  getDailyContractCall,
  getDailyDeployContract,
  getDailyElfPrice,
  getDailyHolder,
  getDailyMarketCap,
  getDailyStaked,
  getDailySupplyGrowth,
  getDailyTotalBurnt,
  getDailyTransactionInfo,
  getDailyTransactions,
  getDailyTvl,
  getDailyTxFee,
  getElfSupply,
  getMonthlyActiveAddresses,
  getNodeBlockProduce,
  getNodeCurrentProduceInfo,
  getStatisticsByMetric,
  STATISTICS_METRICS,
  getTopContractCall,
  getUniqueAddresses,
} from '../core/statistics.js';
import { getTokenDetail, getTokenHolders, getTokens, getTokenTransfers } from '../core/token.js';

export type ToolOutputPolicy = 'normal' | 'summary';
export type ToolAdapter = 'sdk' | 'cli' | 'mcp' | 'openclaw';

const DEFAULT_ADAPTERS = ['sdk', 'cli', 'mcp', 'openclaw'] as const;
const DETAILED_STATISTICS_ADAPTERS = ['sdk', 'cli', 'openclaw'] as const;

export interface ToolDescriptor {
  key: string;
  domain: string;
  action: string;
  mcpName: string;
  description: string;
  inputSchema: z.ZodRawShape;
  parser: z.ZodObject<z.ZodRawShape>;
  parse: (input: unknown) => Record<string, unknown>;
  handler: (input: Record<string, unknown>) => Promise<ToolResult<unknown>>;
  outputPolicy: ToolOutputPolicy;
  adapters: ReadonlyArray<ToolAdapter>;
}

function defineTool<S extends z.ZodRawShape, O = unknown>(config: {
  key: string;
  domain: string;
  action: string;
  mcpName: string;
  description: string;
  inputSchema: S;
  handler: (input: z.infer<z.ZodObject<S>>) => Promise<ToolResult<O>>;
  outputPolicy?: ToolOutputPolicy;
  adapters?: ReadonlyArray<ToolAdapter>;
}): ToolDescriptor {
  const parser = z.object(config.inputSchema).passthrough();

  return {
    key: config.key,
    domain: config.domain,
    action: config.action,
    mcpName: config.mcpName,
    description: config.description,
    inputSchema: config.inputSchema,
    parser: parser as z.ZodObject<z.ZodRawShape>,
    parse: (input: unknown) => parser.parse(input) as Record<string, unknown>,
    handler: (input: Record<string, unknown>) => config.handler(input as z.infer<z.ZodObject<S>>) as Promise<ToolResult<unknown>>,
    outputPolicy: config.outputPolicy ?? 'normal',
    adapters: config.adapters ?? DEFAULT_ADAPTERS,
  };
}

function defineDetailedStatisticsTool<S extends z.ZodRawShape, O = unknown>(config: {
  key: string;
  domain: string;
  action: string;
  mcpName: string;
  description: string;
  inputSchema: S;
  handler: (input: z.infer<z.ZodObject<S>>) => Promise<ToolResult<O>>;
  outputPolicy?: ToolOutputPolicy;
}): ToolDescriptor {
  return defineTool({
    ...config,
    adapters: DETAILED_STATISTICS_ADAPTERS,
  });
}

const sortDirectionSchema = z.enum(['Asc', 'Desc']);

const orderInfoSchema = z.object({
  orderBy: z.string().describe('Sort field name, e.g. BlockTime'),
  sort: sortDirectionSchema.describe('Sort direction Asc or Desc'),
});

const paginationSchema = {
  chainId: z.string().optional().describe('Chain id, e.g. AELF/tDVV; empty for multi-chain'),
  skipCount: z.number().int().optional().describe('Offset for pagination'),
  maxResultCount: z.number().int().optional().describe('Page size'),
  orderBy: z.string().optional().describe('Simple sort field'),
  sort: sortDirectionSchema.optional().describe('Simple sort direction'),
  orderInfos: z.array(orderInfoSchema).optional().describe('Advanced sorting list'),
  searchAfter: z.array(z.string()).optional().describe('search_after cursor values'),
} satisfies z.ZodRawShape;

const statisticsSchema = {
  chainId: z.string().optional().describe('Chain id, e.g. AELF/tDVV; empty for multi-chain'),
  startDate: z.string().optional().describe('Start date (YYYY-MM-DD)'),
  endDate: z.string().optional().describe('End date (YYYY-MM-DD)'),
} satisfies z.ZodRawShape;

const statisticsDateRangeSchema = {
  chainId: z.string().optional().describe('Chain id, e.g. AELF/tDVV; empty for multi-chain'),
  startDate: z.string().describe('Start date (YYYY-MM-DD)'),
  endDate: z.string().describe('End date (YYYY-MM-DD)'),
} satisfies z.ZodRawShape;

const statisticsMetricSchema = {
  metric: z.enum(STATISTICS_METRICS),
  chainId: z.string().optional().describe('Chain id, e.g. AELF/tDVV; empty for multi-chain'),
  startDate: z.string().optional().describe('Start date (YYYY-MM-DD)'),
  endDate: z.string().optional().describe('End date (YYYY-MM-DD)'),
} satisfies z.ZodRawShape;

export const TOOL_DESCRIPTORS = [
  defineTool({
    key: 'search.filters',
    domain: 'search',
    action: 'filters',
    mcpName: 'aelfscan_search_filters',
    description: 'Get search filter metadata used by explorer search UI.',
    inputSchema: {
      chainId: z.string().optional(),
    },
    handler: getSearchFilters,
    outputPolicy: 'summary',
  }),
  defineTool({
    key: 'search.query',
    domain: 'search',
    action: 'query',
    mcpName: 'aelfscan_search',
    description: 'Search tokens/accounts/contracts/NFTs/blocks/transactions on AelfScan explorer.',
    inputSchema: {
      chainId: z.string().optional(),
      keyword: z.string().describe('Search keyword'),
      filterType: z.number().int().optional().describe('0:all,1:tokens,2:accounts,3:contracts,4:nfts'),
      searchType: z.number().int().optional().describe('0:fuzzy,1:exact'),
    },
    handler: search,
    outputPolicy: 'summary',
  }),

  defineTool({
    key: 'blockchain.blocks',
    domain: 'blockchain',
    action: 'blocks',
    mcpName: 'aelfscan_blocks',
    description: 'List blocks with pagination.',
    inputSchema: {
      ...paginationSchema,
      isLastPage: z.boolean().optional(),
    },
    handler: getBlocks,
    outputPolicy: 'summary',
  }),
  defineTool({
    key: 'blockchain.blocks-latest',
    domain: 'blockchain',
    action: 'blocks-latest',
    mcpName: 'aelfscan_blocks_latest',
    description: 'Get latest blocks (uses blocks API with skipCount=0).',
    inputSchema: {
      chainId: z.string().optional(),
      maxResultCount: z.number().int().optional(),
      orderBy: z.string().optional(),
      sort: sortDirectionSchema.optional(),
      orderInfos: z.array(orderInfoSchema).optional(),
      searchAfter: z.array(z.string()).optional(),
      isLastPage: z.boolean().optional(),
    },
    handler: getLatestBlocks,
    outputPolicy: 'summary',
  }),
  defineTool({
    key: 'blockchain.block-detail',
    domain: 'blockchain',
    action: 'block-detail',
    mcpName: 'aelfscan_block_detail',
    description: 'Get block detail by block height.',
    inputSchema: {
      chainId: z.string().optional(),
      blockHeight: z.number().int().describe('Block height'),
    },
    handler: getBlockDetail,
  }),
  defineTool({
    key: 'blockchain.transactions',
    domain: 'blockchain',
    action: 'transactions',
    mcpName: 'aelfscan_transactions',
    description: 'List transactions with optional filters.',
    inputSchema: {
      ...paginationSchema,
      transactionId: z.string().optional(),
      blockHeight: z.number().int().optional(),
      address: z.string().optional(),
      startTime: z.number().int().optional(),
      endTime: z.number().int().optional(),
    },
    handler: getTransactions,
    outputPolicy: 'summary',
  }),
  defineTool({
    key: 'blockchain.transactions-latest',
    domain: 'blockchain',
    action: 'transactions-latest',
    mcpName: 'aelfscan_transactions_latest',
    description: 'Get latest transactions (uses transactions API with skipCount=0).',
    inputSchema: {
      chainId: z.string().optional(),
      maxResultCount: z.number().int().optional(),
      orderBy: z.string().optional(),
      sort: sortDirectionSchema.optional(),
      orderInfos: z.array(orderInfoSchema).optional(),
      searchAfter: z.array(z.string()).optional(),
      transactionId: z.string().optional(),
      blockHeight: z.number().int().optional(),
      address: z.string().optional(),
      startTime: z.number().int().optional(),
      endTime: z.number().int().optional(),
    },
    handler: getLatestTransactions,
    outputPolicy: 'summary',
  }),
  defineTool({
    key: 'blockchain.transaction-detail',
    domain: 'blockchain',
    action: 'transaction-detail',
    mcpName: 'aelfscan_transaction_detail',
    description: 'Get transaction detail by transaction id.',
    inputSchema: {
      chainId: z.string().optional(),
      transactionId: z.string().describe('Transaction id'),
      blockHeight: z.number().int().optional(),
    },
    handler: getTransactionDetail,
  }),
  defineTool({
    key: 'blockchain.overview',
    domain: 'blockchain',
    action: 'overview',
    mcpName: 'aelfscan_blockchain_overview',
    description: 'Get blockchain overview metrics and aggregate stats.',
    inputSchema: {
      chainId: z.string().optional(),
    },
    handler: getBlockchainOverview,
    outputPolicy: 'summary',
  }),
  defineTool({
    key: 'blockchain.transaction-data-chart',
    domain: 'blockchain',
    action: 'transaction-data-chart',
    mcpName: 'aelfscan_transaction_data_chart',
    description: 'Get transaction data chart series.',
    inputSchema: {
      chainId: z.string().optional(),
    },
    handler: getTransactionDataChart,
    outputPolicy: 'summary',
  }),
  defineTool({
    key: 'blockchain.address-dictionary',
    domain: 'blockchain',
    action: 'address-dictionary',
    mcpName: 'aelfscan_address_dictionary',
    description: 'Resolve or query address dictionary metadata.',
    inputSchema: {
      chainId: z.string().optional(),
      name: z.string().describe('Dictionary name'),
      addresses: z.array(z.string()).min(1).describe('Address list'),
    },
    handler: getAddressDictionary,
  }),
  defineTool({
    key: 'blockchain.log-events',
    domain: 'blockchain',
    action: 'log-events',
    mcpName: 'aelfscan_log_events',
    description: 'Get contract log events by contract address.',
    inputSchema: {
      ...paginationSchema,
      contractAddress: z.string().describe('Contract address'),
      address: z.string().optional(),
      eventName: z.string().optional(),
      transactionId: z.string().optional(),
      blockHeight: z.number().int().optional(),
      startBlockHeight: z.number().int().optional(),
      endBlockHeight: z.number().int().optional(),
    },
    handler: getLogEvents,
    outputPolicy: 'summary',
  }),

  defineTool({
    key: 'address.accounts',
    domain: 'address',
    action: 'accounts',
    mcpName: 'aelfscan_accounts',
    description: 'List top accounts.',
    inputSchema: {
      ...paginationSchema,
    },
    handler: getAccounts,
    outputPolicy: 'summary',
  }),
  defineTool({
    key: 'address.contracts',
    domain: 'address',
    action: 'contracts',
    mcpName: 'aelfscan_contracts',
    description: 'List contracts.',
    inputSchema: {
      ...paginationSchema,
    },
    handler: getContracts,
    outputPolicy: 'summary',
  }),
  defineTool({
    key: 'address.detail',
    domain: 'address',
    action: 'detail',
    mcpName: 'aelfscan_address_detail',
    description: 'Get address detail (EOA/contract profile and portfolio).',
    inputSchema: {
      chainId: z.string().optional(),
      address: z.string().describe('Address, supports ELF_xxx_chain format'),
    },
    handler: getAddressDetail,
  }),
  defineTool({
    key: 'address.tokens',
    domain: 'address',
    action: 'tokens',
    mcpName: 'aelfscan_address_tokens',
    description: 'Get token holdings for an address.',
    inputSchema: {
      ...paginationSchema,
      address: z.string().describe('Address'),
      fuzzySearch: z.string().optional(),
    },
    handler: getAddressTokens,
    outputPolicy: 'summary',
  }),
  defineTool({
    key: 'address.nft-assets',
    domain: 'address',
    action: 'nft-assets',
    mcpName: 'aelfscan_address_nft_assets',
    description: 'Get NFT holdings for an address.',
    inputSchema: {
      ...paginationSchema,
      address: z.string().describe('Address'),
      fuzzySearch: z.string().optional(),
    },
    handler: getAddressNftAssets,
    outputPolicy: 'summary',
  }),
  defineTool({
    key: 'address.transfers',
    domain: 'address',
    action: 'transfers',
    mcpName: 'aelfscan_address_transfers',
    description: 'Get transfer history for an address.',
    inputSchema: {
      ...paginationSchema,
      address: z.string().describe('Address'),
      symbol: z.string().optional(),
      tokenType: z.number().int().optional().describe('0:token,1:nft'),
    },
    handler: getAddressTransfers,
    outputPolicy: 'summary',
  }),
  defineTool({
    key: 'address.contract-history',
    domain: 'address',
    action: 'contract-history',
    mcpName: 'aelfscan_contract_history',
    description: 'Get contract deploy/update history.',
    inputSchema: {
      chainId: z.string().optional(),
      address: z.string().describe('Contract address'),
    },
    handler: getContractHistory,
    outputPolicy: 'summary',
  }),
  defineTool({
    key: 'address.contract-events',
    domain: 'address',
    action: 'contract-events',
    mcpName: 'aelfscan_contract_events',
    description: 'Get contract events list.',
    inputSchema: {
      ...paginationSchema,
      chainId: z.string().optional(),
      contractAddress: z.string().describe('Contract address'),
      blockHeight: z.number().int().optional(),
    },
    handler: getContractEvents,
    outputPolicy: 'summary',
  }),
  defineTool({
    key: 'address.contract-source',
    domain: 'address',
    action: 'contract-source',
    mcpName: 'aelfscan_contract_source',
    description: 'Get verified contract source metadata.',
    inputSchema: {
      chainId: z.string().optional(),
      address: z.string().describe('Contract address'),
    },
    handler: getContractSource,
  }),

  defineTool({
    key: 'token.list',
    domain: 'token',
    action: 'list',
    mcpName: 'aelfscan_tokens',
    description: 'List tokens.',
    inputSchema: {
      ...paginationSchema,
      types: z.array(z.number().int()).optional(),
      symbols: z.array(z.string()).optional(),
      collectionSymbols: z.array(z.string()).optional(),
      search: z.string().optional(),
      exactSearch: z.string().optional(),
      fuzzySearch: z.string().optional(),
      beginBlockTime: z.union([z.string(), z.number()]).optional(),
    },
    handler: getTokens,
    outputPolicy: 'summary',
  }),
  defineTool({
    key: 'token.detail',
    domain: 'token',
    action: 'detail',
    mcpName: 'aelfscan_token_detail',
    description: 'Get token detail by symbol.',
    inputSchema: {
      chainId: z.string().optional(),
      symbol: z.string().describe('Token symbol'),
    },
    handler: getTokenDetail,
  }),
  defineTool({
    key: 'token.transfers',
    domain: 'token',
    action: 'transfers',
    mcpName: 'aelfscan_token_transfers',
    description: 'Get token transfer list by symbol.',
    inputSchema: {
      ...paginationSchema,
      symbol: z.string().describe('Token symbol'),
      search: z.string().optional(),
      collectionSymbol: z.string().optional(),
      address: z.string().optional(),
      types: z.array(z.number().int()).optional(),
      fuzzySearch: z.string().optional(),
      beginBlockTime: z.union([z.string(), z.number()]).optional(),
    },
    handler: getTokenTransfers,
    outputPolicy: 'summary',
  }),
  defineTool({
    key: 'token.holders',
    domain: 'token',
    action: 'holders',
    mcpName: 'aelfscan_token_holders',
    description: 'Get token holders.',
    inputSchema: {
      ...paginationSchema,
      symbol: z.string().optional(),
      collectionSymbol: z.string().optional(),
      address: z.string().optional(),
      partialSymbol: z.string().optional(),
      search: z.string().optional(),
      types: z.array(z.number().int()).optional(),
      symbols: z.array(z.string()).optional(),
      addressList: z.array(z.string()).optional(),
      searchSymbols: z.array(z.string()).optional(),
      fuzzySearch: z.string().optional(),
      amountGreaterThanZero: z.boolean().optional(),
    },
    handler: getTokenHolders,
    outputPolicy: 'summary',
  }),

  defineTool({
    key: 'nft.collections',
    domain: 'nft',
    action: 'collections',
    mcpName: 'aelfscan_nft_collections',
    description: 'List NFT collections.',
    inputSchema: {
      ...paginationSchema,
      types: z.array(z.number().int()).optional(),
      symbols: z.array(z.string()).optional(),
      collectionSymbols: z.array(z.string()).optional(),
      search: z.string().optional(),
      exactSearch: z.string().optional(),
      fuzzySearch: z.string().optional(),
      beginBlockTime: z.union([z.string(), z.number()]).optional(),
    },
    handler: getNftCollections,
    outputPolicy: 'summary',
  }),
  defineTool({
    key: 'nft.collection-detail',
    domain: 'nft',
    action: 'collection-detail',
    mcpName: 'aelfscan_nft_collection_detail',
    description: 'Get NFT collection detail.',
    inputSchema: {
      chainId: z.string().optional(),
      collectionSymbol: z.string().describe('NFT collection symbol'),
    },
    handler: getNftCollectionDetail,
  }),
  defineTool({
    key: 'nft.transfers',
    domain: 'nft',
    action: 'transfers',
    mcpName: 'aelfscan_nft_transfers',
    description: 'Get NFT transfers by collection symbol.',
    inputSchema: {
      ...paginationSchema,
      chainId: z.string().optional(),
      collectionSymbol: z.string().describe('NFT collection symbol'),
      search: z.string().optional(),
      address: z.string().optional(),
    },
    handler: getNftTransfers,
    outputPolicy: 'summary',
  }),
  defineTool({
    key: 'nft.holders',
    domain: 'nft',
    action: 'holders',
    mcpName: 'aelfscan_nft_holders',
    description: 'Get NFT holders by collection symbol.',
    inputSchema: {
      ...paginationSchema,
      chainId: z.string().optional(),
      collectionSymbol: z.string().describe('NFT collection symbol'),
      search: z.string().optional(),
    },
    handler: getNftHolders,
    outputPolicy: 'summary',
  }),
  defineTool({
    key: 'nft.inventory',
    domain: 'nft',
    action: 'inventory',
    mcpName: 'aelfscan_nft_inventory',
    description: 'Get NFT inventory by collection symbol.',
    inputSchema: {
      ...paginationSchema,
      chainId: z.string().optional(),
      collectionSymbol: z.string().describe('NFT collection symbol'),
      search: z.string().optional(),
    },
    handler: getNftInventory,
    outputPolicy: 'summary',
  }),
  defineTool({
    key: 'nft.item-detail',
    domain: 'nft',
    action: 'item-detail',
    mcpName: 'aelfscan_nft_item_detail',
    description: 'Get NFT item detail by symbol.',
    inputSchema: {
      chainId: z.string().optional(),
      symbol: z.string().describe('NFT item symbol'),
    },
    handler: getNftItemDetail,
  }),
  defineTool({
    key: 'nft.item-holders',
    domain: 'nft',
    action: 'item-holders',
    mcpName: 'aelfscan_nft_item_holders',
    description: 'Get holders of a specific NFT item.',
    inputSchema: {
      ...paginationSchema,
      chainId: z.string().optional(),
      symbol: z.string().describe('NFT item symbol'),
      types: z.array(z.number().int()).optional(),
    },
    handler: getNftItemHolders,
    outputPolicy: 'summary',
  }),
  defineTool({
    key: 'nft.item-activity',
    domain: 'nft',
    action: 'item-activity',
    mcpName: 'aelfscan_nft_item_activity',
    description: 'Get activity list of a specific NFT item.',
    inputSchema: {
      ...paginationSchema,
      chainId: z.string().optional(),
      symbol: z.string().describe('NFT item symbol'),
    },
    handler: getNftItemActivity,
    outputPolicy: 'summary',
  }),

  defineTool({
    key: 'statistics.metric',
    domain: 'statistics',
    action: 'metric',
    mcpName: 'aelfscan_statistics',
    description: 'Get statistics by metric enum, supports all existing statistics endpoints.',
    inputSchema: statisticsMetricSchema,
    handler: getStatisticsByMetric,
    outputPolicy: 'summary',
  }),

  defineDetailedStatisticsTool({
    key: 'statistics.daily-transactions',
    domain: 'statistics',
    action: 'daily-transactions',
    mcpName: 'aelfscan_statistics_daily_transactions',
    description: 'Get daily transactions statistics.',
    inputSchema: statisticsSchema,
    handler: getDailyTransactions,
    outputPolicy: 'summary',
  }),
  defineDetailedStatisticsTool({
    key: 'statistics.unique-addresses',
    domain: 'statistics',
    action: 'unique-addresses',
    mcpName: 'aelfscan_statistics_unique_addresses',
    description: 'Get unique addresses statistics.',
    inputSchema: statisticsSchema,
    handler: getUniqueAddresses,
    outputPolicy: 'summary',
  }),
  defineDetailedStatisticsTool({
    key: 'statistics.daily-active-addresses',
    domain: 'statistics',
    action: 'daily-active-addresses',
    mcpName: 'aelfscan_statistics_daily_active_addresses',
    description: 'Get daily active addresses statistics.',
    inputSchema: statisticsSchema,
    handler: getDailyActiveAddresses,
    outputPolicy: 'summary',
  }),
  defineDetailedStatisticsTool({
    key: 'statistics.monthly-active-addresses',
    domain: 'statistics',
    action: 'monthly-active-addresses',
    mcpName: 'aelfscan_statistics_monthly_active_addresses',
    description: 'Get monthly active addresses statistics.',
    inputSchema: statisticsSchema,
    handler: getMonthlyActiveAddresses,
    outputPolicy: 'summary',
  }),
  defineDetailedStatisticsTool({
    key: 'statistics.block-produce-rate',
    domain: 'statistics',
    action: 'block-produce-rate',
    mcpName: 'aelfscan_statistics_block_produce_rate',
    description: 'Get block produce rate statistics.',
    inputSchema: statisticsSchema,
    handler: getBlockProduceRate,
    outputPolicy: 'summary',
  }),
  defineDetailedStatisticsTool({
    key: 'statistics.avg-block-duration',
    domain: 'statistics',
    action: 'avg-block-duration',
    mcpName: 'aelfscan_statistics_avg_block_duration',
    description: 'Get average block duration statistics.',
    inputSchema: statisticsSchema,
    handler: getAvgBlockDuration,
    outputPolicy: 'summary',
  }),
  defineDetailedStatisticsTool({
    key: 'statistics.cycle-count',
    domain: 'statistics',
    action: 'cycle-count',
    mcpName: 'aelfscan_statistics_cycle_count',
    description: 'Get cycle count statistics.',
    inputSchema: statisticsSchema,
    handler: getCycleCount,
    outputPolicy: 'summary',
  }),
  defineDetailedStatisticsTool({
    key: 'statistics.node-block-produce',
    domain: 'statistics',
    action: 'node-block-produce',
    mcpName: 'aelfscan_statistics_node_block_produce',
    description: 'Get node block produce statistics.',
    inputSchema: statisticsSchema,
    handler: getNodeBlockProduce,
    outputPolicy: 'summary',
  }),
  defineDetailedStatisticsTool({
    key: 'statistics.daily-avg-transaction-fee',
    domain: 'statistics',
    action: 'daily-avg-transaction-fee',
    mcpName: 'aelfscan_statistics_daily_avg_transaction_fee',
    description: 'Get daily average transaction fee statistics.',
    inputSchema: statisticsSchema,
    handler: getDailyAvgTransactionFee,
    outputPolicy: 'summary',
  }),
  defineDetailedStatisticsTool({
    key: 'statistics.daily-tx-fee',
    domain: 'statistics',
    action: 'daily-tx-fee',
    mcpName: 'aelfscan_statistics_daily_tx_fee',
    description: 'Get daily transaction fee statistics.',
    inputSchema: statisticsSchema,
    handler: getDailyTxFee,
    outputPolicy: 'summary',
  }),
  defineDetailedStatisticsTool({
    key: 'statistics.daily-total-burnt',
    domain: 'statistics',
    action: 'daily-total-burnt',
    mcpName: 'aelfscan_statistics_daily_total_burnt',
    description: 'Get daily total burnt statistics.',
    inputSchema: statisticsSchema,
    handler: getDailyTotalBurnt,
    outputPolicy: 'summary',
  }),
  defineDetailedStatisticsTool({
    key: 'statistics.daily-elf-price',
    domain: 'statistics',
    action: 'daily-elf-price',
    mcpName: 'aelfscan_statistics_daily_elf_price',
    description: 'Get daily ELF price statistics.',
    inputSchema: statisticsSchema,
    handler: getDailyElfPrice,
    outputPolicy: 'summary',
  }),
  defineDetailedStatisticsTool({
    key: 'statistics.daily-deploy-contract',
    domain: 'statistics',
    action: 'daily-deploy-contract',
    mcpName: 'aelfscan_statistics_daily_deploy_contract',
    description: 'Get daily deploy contract statistics.',
    inputSchema: statisticsSchema,
    handler: getDailyDeployContract,
    outputPolicy: 'summary',
  }),
  defineDetailedStatisticsTool({
    key: 'statistics.daily-block-reward',
    domain: 'statistics',
    action: 'daily-block-reward',
    mcpName: 'aelfscan_statistics_daily_block_reward',
    description: 'Get daily block reward statistics.',
    inputSchema: statisticsSchema,
    handler: getDailyBlockReward,
    outputPolicy: 'summary',
  }),
  defineDetailedStatisticsTool({
    key: 'statistics.daily-avg-block-size',
    domain: 'statistics',
    action: 'daily-avg-block-size',
    mcpName: 'aelfscan_statistics_daily_avg_block_size',
    description: 'Get daily average block size statistics.',
    inputSchema: statisticsSchema,
    handler: getDailyAvgBlockSize,
    outputPolicy: 'summary',
  }),
  defineDetailedStatisticsTool({
    key: 'statistics.top-contract-call',
    domain: 'statistics',
    action: 'top-contract-call',
    mcpName: 'aelfscan_statistics_top_contract_call',
    description: 'Get top contract call statistics.',
    inputSchema: statisticsSchema,
    handler: getTopContractCall,
    outputPolicy: 'summary',
  }),
  defineDetailedStatisticsTool({
    key: 'statistics.daily-contract-call',
    domain: 'statistics',
    action: 'daily-contract-call',
    mcpName: 'aelfscan_statistics_daily_contract_call',
    description: 'Get daily contract call statistics.',
    inputSchema: statisticsSchema,
    handler: getDailyContractCall,
    outputPolicy: 'summary',
  }),
  defineDetailedStatisticsTool({
    key: 'statistics.daily-supply-growth',
    domain: 'statistics',
    action: 'daily-supply-growth',
    mcpName: 'aelfscan_statistics_daily_supply_growth',
    description: 'Get daily supply growth statistics.',
    inputSchema: statisticsSchema,
    handler: getDailySupplyGrowth,
    outputPolicy: 'summary',
  }),
  defineDetailedStatisticsTool({
    key: 'statistics.daily-market-cap',
    domain: 'statistics',
    action: 'daily-market-cap',
    mcpName: 'aelfscan_statistics_daily_market_cap',
    description: 'Get daily market cap statistics.',
    inputSchema: statisticsSchema,
    handler: getDailyMarketCap,
    outputPolicy: 'summary',
  }),
  defineDetailedStatisticsTool({
    key: 'statistics.daily-staked',
    domain: 'statistics',
    action: 'daily-staked',
    mcpName: 'aelfscan_statistics_daily_staked',
    description: 'Get daily staked statistics.',
    inputSchema: statisticsSchema,
    handler: getDailyStaked,
    outputPolicy: 'summary',
  }),
  defineDetailedStatisticsTool({
    key: 'statistics.daily-holder',
    domain: 'statistics',
    action: 'daily-holder',
    mcpName: 'aelfscan_statistics_daily_holder',
    description: 'Get daily holder statistics.',
    inputSchema: statisticsSchema,
    handler: getDailyHolder,
    outputPolicy: 'summary',
  }),
  defineDetailedStatisticsTool({
    key: 'statistics.daily-tvl',
    domain: 'statistics',
    action: 'daily-tvl',
    mcpName: 'aelfscan_statistics_daily_tvl',
    description: 'Get daily TVL statistics.',
    inputSchema: statisticsSchema,
    handler: getDailyTvl,
    outputPolicy: 'summary',
  }),
  defineDetailedStatisticsTool({
    key: 'statistics.node-current-produce-info',
    domain: 'statistics',
    action: 'node-current-produce-info',
    mcpName: 'aelfscan_statistics_node_current_produce_info',
    description: 'Get current node produce information.',
    inputSchema: statisticsSchema,
    handler: getNodeCurrentProduceInfo,
    outputPolicy: 'summary',
  }),
  defineDetailedStatisticsTool({
    key: 'statistics.elf-supply',
    domain: 'statistics',
    action: 'elf-supply',
    mcpName: 'aelfscan_statistics_elf_supply',
    description: 'Get ELF supply statistics.',
    inputSchema: statisticsSchema,
    handler: getElfSupply,
    outputPolicy: 'summary',
  }),
  defineDetailedStatisticsTool({
    key: 'statistics.daily-transaction-info',
    domain: 'statistics',
    action: 'daily-transaction-info',
    mcpName: 'aelfscan_statistics_daily_transaction_info',
    description: 'Get daily transaction summary for a date range.',
    inputSchema: statisticsDateRangeSchema,
    handler: getDailyTransactionInfo,
    outputPolicy: 'summary',
  }),
  defineDetailedStatisticsTool({
    key: 'statistics.daily-activity-address',
    domain: 'statistics',
    action: 'daily-activity-address',
    mcpName: 'aelfscan_statistics_daily_activity_address',
    description: 'Get daily activity address summary for a date range.',
    inputSchema: statisticsDateRangeSchema,
    handler: getDailyActivityAddress,
    outputPolicy: 'summary',
  }),
  defineDetailedStatisticsTool({
    key: 'statistics.currency-price',
    domain: 'statistics',
    action: 'currency-price',
    mcpName: 'aelfscan_statistics_currency_price',
    description: 'Get currency price statistics.',
    inputSchema: statisticsSchema,
    handler: getCurrencyPrice,
    outputPolicy: 'summary',
  }),
] as const;

export const TOOL_DESCRIPTOR_BY_KEY = new Map(TOOL_DESCRIPTORS.map(tool => [tool.key, tool]));

export const MCP_TOOL_DESCRIPTORS = TOOL_DESCRIPTORS.filter(tool => tool.adapters.includes('mcp'));
export const CLI_TOOL_DESCRIPTORS = TOOL_DESCRIPTORS.filter(tool => tool.adapters.includes('cli'));
export const OPENCLAW_TOOL_DESCRIPTORS = TOOL_DESCRIPTORS.filter(tool => tool.adapters.includes('openclaw'));

export const CLI_TOOL_DESCRIPTOR_BY_KEY = new Map(CLI_TOOL_DESCRIPTORS.map(tool => [tool.key, tool]));
export const TOOL_DESCRIPTOR_BY_MCP_NAME = new Map(MCP_TOOL_DESCRIPTORS.map(tool => [tool.mcpName, tool]));
