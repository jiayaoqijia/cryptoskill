export type SortDirection = 'Asc' | 'Desc';

export interface OrderInfo {
  orderBy: string;
  sort: SortDirection;
}

export interface PaginationInput {
  chainId?: string;
  skipCount?: number;
  maxResultCount?: number;
  orderBy?: string;
  sort?: SortDirection;
  orderInfos?: OrderInfo[];
  searchAfter?: string[];
}

export interface ToolError {
  code: string;
  message: string;
  details?: unknown;
  httpStatus?: number;
}

export interface ToolResult<T> {
  success: boolean;
  data?: T;
  error?: ToolError;
  traceId: string;
  raw?: unknown;
}

export interface AelfscanEnvelope<T> {
  code?: string;
  message?: string;
  data?: T;
}

export interface HttpClientResult<T> {
  data: T;
  raw: unknown;
}

export interface AelfscanConfig {
  apiBaseUrl: string;
  defaultChainId: string;
  timeoutMs: number;
  retry: number;
  retryBaseMs: number;
  retryMaxMs: number;
  maxConcurrentRequests: number;
  cacheTtlMs: number;
  cacheMaxEntries: number;
  maxResultCount: number;
  mcpMaxItems: number;
  mcpMaxChars: number;
  mcpIncludeRaw: boolean;
}

export interface SearchInput {
  chainId?: string;
  keyword: string;
  filterType?: number;
  searchType?: number;
}

export interface SearchFiltersInput {
  chainId?: string;
}

export interface BlocksInput extends PaginationInput {
  isLastPage?: boolean;
}

export interface BlockDetailInput {
  chainId?: string;
  blockHeight: number;
}

export interface TransactionsInput extends PaginationInput {
  transactionId?: string;
  blockHeight?: number;
  address?: string;
  startTime?: number;
  endTime?: number;
}

export interface TransactionDetailInput {
  chainId?: string;
  transactionId: string;
  blockHeight?: number;
}

export interface BlockchainOverviewInput {
  chainId?: string;
  [key: string]: unknown;
}

export interface TransactionDataChartInput {
  chainId?: string;
  [key: string]: unknown;
}

export interface AddressDictionaryInput {
  chainId?: string;
  name: string;
  addresses: string[];
  [key: string]: unknown;
}

export interface LogEventsInput extends PaginationInput {
  chainId?: string;
  contractAddress: string;
  address?: string;
  eventName?: string;
  transactionId?: string;
  blockHeight?: number;
  startBlockHeight?: number;
  endBlockHeight?: number;
  [key: string]: unknown;
}

export interface AccountsInput extends PaginationInput {}

export interface ContractsInput extends PaginationInput {}

export interface AddressDetailInput {
  chainId?: string;
  address: string;
}

export interface AddressTokensInput extends PaginationInput {
  address: string;
  fuzzySearch?: string;
}

export interface AddressNftAssetsInput extends PaginationInput {
  address: string;
  fuzzySearch?: string;
}

export interface AddressTransfersInput extends PaginationInput {
  address: string;
  symbol?: string;
  tokenType?: number;
}

export interface ContractHistoryInput {
  chainId?: string;
  address: string;
}

export interface ContractEventsInput extends PaginationInput {
  chainId?: string;
  contractAddress: string;
  blockHeight?: number;
}

export interface ContractSourceInput {
  chainId?: string;
  address: string;
}

export interface TokenListInput extends PaginationInput {
  types?: number[];
  symbols?: string[];
  collectionSymbols?: string[];
  search?: string;
  exactSearch?: string;
  fuzzySearch?: string;
  beginBlockTime?: string | number;
}

export interface TokenDetailInput {
  chainId?: string;
  symbol: string;
}

export interface TokenTransfersInput extends PaginationInput {
  symbol: string;
  search?: string;
  collectionSymbol?: string;
  address?: string;
  types?: number[];
  fuzzySearch?: string;
  beginBlockTime?: string | number;
}

export interface TokenHoldersInput extends PaginationInput {
  symbol?: string;
  collectionSymbol?: string;
  address?: string;
  partialSymbol?: string;
  search?: string;
  types?: number[];
  symbols?: string[];
  addressList?: string[];
  searchSymbols?: string[];
  fuzzySearch?: string;
  amountGreaterThanZero?: boolean;
}

export interface NftCollectionsInput extends TokenListInput {}

export interface NftCollectionDetailInput {
  chainId?: string;
  collectionSymbol: string;
}

export interface NftTransfersInput extends PaginationInput {
  chainId?: string;
  collectionSymbol: string;
  search?: string;
  address?: string;
}

export interface NftHoldersInput extends PaginationInput {
  chainId?: string;
  collectionSymbol: string;
  search?: string;
}

export interface NftInventoryInput extends PaginationInput {
  chainId?: string;
  collectionSymbol: string;
  search?: string;
}

export interface NftItemDetailInput {
  chainId?: string;
  symbol: string;
}

export interface NftItemHoldersInput extends PaginationInput {
  chainId?: string;
  symbol: string;
  types?: number[];
}

export interface NftItemActivityInput extends PaginationInput {
  chainId?: string;
  symbol: string;
}

export interface StatisticsQueryInput {
  chainId?: string;
  startDate?: string;
  endDate?: string;
  [key: string]: unknown;
}

export interface StatisticsDateRangeInput extends StatisticsQueryInput {
  startDate: string;
  endDate: string;
}

export type StatisticsMetric =
  | 'dailyTransactions'
  | 'uniqueAddresses'
  | 'dailyActiveAddresses'
  | 'monthlyActiveAddresses'
  | 'blockProduceRate'
  | 'avgBlockDuration'
  | 'cycleCount'
  | 'nodeBlockProduce'
  | 'dailyAvgTransactionFee'
  | 'dailyTxFee'
  | 'dailyTotalBurnt'
  | 'dailyElfPrice'
  | 'dailyDeployContract'
  | 'dailyBlockReward'
  | 'dailyAvgBlockSize'
  | 'topContractCall'
  | 'dailyContractCall'
  | 'dailySupplyGrowth'
  | 'dailyMarketCap'
  | 'dailyStaked'
  | 'dailyHolder'
  | 'dailyTvl'
  | 'nodeCurrentProduceInfo'
  | 'elfSupply'
  | 'dailyTransactionInfo'
  | 'dailyActivityAddress'
  | 'currencyPrice';

export interface StatisticsMetricInput extends StatisticsQueryInput {
  metric: StatisticsMetric;
}
