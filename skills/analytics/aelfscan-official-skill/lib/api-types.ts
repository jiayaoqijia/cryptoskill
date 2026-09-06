export interface ApiValidationError {
  memberNames?: string[];
  errorMessage?: string;
}

export interface ApiSuccessEnvelope<T> {
  code: string;
  message?: string;
  data: T;
}

export interface ApiErrorEnvelope {
  code: string;
  message?: string;
  data?: unknown;
  validationErrors?: ApiValidationError[];
}

export interface ApiPagedList<TItem> {
  total?: number;
  list?: TItem[];
  items?: TItem[];
  [key: string]: unknown;
}

export interface SearchFilterOption {
  filterType?: number;
  filterInfo?: string;
  searchType?: number;
  searchInfo?: string;
  [key: string]: unknown;
}

export interface SearchFiltersResponse {
  filterTypes?: SearchFilterOption[];
  searchTypes?: SearchFilterOption[];
  [key: string]: unknown;
}

export interface BlockSummary {
  blockHeight?: number;
  blockHash?: string;
  chainId?: string;
  blockTime?: string;
  txns?: number;
  [key: string]: unknown;
}

export interface TransactionSummary {
  transactionId?: string;
  blockHeight?: number;
  blockHash?: string;
  from?: string;
  to?: string;
  methodName?: string;
  status?: string;
  blockTime?: string;
  [key: string]: unknown;
}

export interface LogEvent {
  name?: string;
  indexed?: unknown[];
  nonIndexed?: unknown[];
  [key: string]: unknown;
}

export interface SearchEntity {
  symbol?: string;
  address?: string;
  blockHeight?: number;
  transactionId?: string;
  [key: string]: unknown;
}

export interface SearchResponse {
  tokens?: SearchEntity[];
  nfts?: SearchEntity[];
  accounts?: SearchEntity[];
  contracts?: SearchEntity[];
  blocks?: BlockSummary[];
  block?: BlockSummary;
  transaction?: TransactionSummary | null;
  [key: string]: unknown;
}

export interface BlockListResponse extends ApiPagedList<BlockSummary> {
  blocks?: BlockSummary[];
}

export interface BlockDetailResponse extends BlockSummary {
  transactions?: TransactionSummary[];
  [key: string]: unknown;
}

export interface TransactionListResponse extends ApiPagedList<TransactionSummary> {
  transactions?: TransactionSummary[];
}

export interface TransactionDetailResponse extends TransactionSummary {
  logEvents?: LogEvent[] | null;
  [key: string]: unknown;
}

export interface BlockchainOverviewResponse {
  transactions?: number;
  tokenPriceInUsd?: number;
  tokenDailyPriceInUsd?: number;
  tokenPriceRate24h?: number;
  [key: string]: unknown;
}

export interface TransactionChartPoint {
  start?: number;
  end?: number;
  count?: number;
  [key: string]: unknown;
}

export interface TransactionDataChartResponse {
  all?: TransactionChartPoint[];
  mainChain?: TransactionChartPoint[];
  sideChain?: TransactionChartPoint[];
  [key: string]: unknown;
}

export interface AddressDictionaryResponse {
  name?: string;
  addresses?: string[];
  [key: string]: unknown;
}

export interface LogEventsResponse {
  total?: number;
  logEvents?: LogEvent[] | null;
  [key: string]: unknown;
}

export interface AccountSummary {
  address?: string;
  balance?: number;
  txns?: number;
  [key: string]: unknown;
}

export interface ContractSummary {
  address?: string;
  contractName?: string;
  type?: string;
  txns?: number;
  [key: string]: unknown;
}

export interface AddressDetailResponse {
  address?: string;
  balance?: number;
  accountType?: string;
  [key: string]: unknown;
}

export interface AddressAssetItem {
  symbol?: string;
  balance?: number;
  amount?: string | number;
  [key: string]: unknown;
}

export interface AddressTransferItem {
  transactionId?: string;
  symbol?: string;
  from?: string;
  to?: string;
  amount?: string | number;
  [key: string]: unknown;
}

export interface ContractHistoryItem {
  transactionId?: string;
  blockHeight?: number;
  updateTime?: string;
  [key: string]: unknown;
}

export interface ContractEventItem {
  blockHeight?: number;
  transactionId?: string;
  eventName?: string;
  [key: string]: unknown;
}

export interface ContractSourceResponse {
  address?: string;
  codeHash?: string;
  version?: string;
  [key: string]: unknown;
}

export interface TokenSummary {
  symbol?: string;
  tokenName?: string;
  decimals?: number;
  supply?: string | number;
  [key: string]: unknown;
}

export interface TokenDetailResponse extends TokenSummary {
  holders?: number;
  transfers?: number;
  [key: string]: unknown;
}

export interface TokenTransferItem {
  transactionId?: string;
  from?: string;
  to?: string;
  amount?: string | number;
  [key: string]: unknown;
}

export interface TokenHolderItem {
  address?: string;
  amount?: string | number;
  percentage?: string | number;
  [key: string]: unknown;
}

export interface NftCollectionSummary {
  collectionSymbol?: string;
  collectionName?: string;
  items?: number;
  holders?: number;
  [key: string]: unknown;
}

export interface NftCollectionDetailResponse extends NftCollectionSummary {
  description?: string;
  [key: string]: unknown;
}

export interface NftTransferItem {
  transactionId?: string;
  symbol?: string;
  from?: string;
  to?: string;
  [key: string]: unknown;
}

export interface NftHolderItem {
  address?: string;
  amount?: string | number;
  [key: string]: unknown;
}

export interface NftInventoryItem {
  symbol?: string;
  owner?: string;
  [key: string]: unknown;
}

export interface NftItemDetailResponse {
  symbol?: string;
  collectionSymbol?: string;
  owner?: string;
  [key: string]: unknown;
}

export interface StatisticsSeriesPoint {
  date?: number;
  dateStr?: string;
  value?: number | string;
  [key: string]: unknown;
}

export interface StatisticsListResponse extends ApiPagedList<StatisticsSeriesPoint> {
  list?: StatisticsSeriesPoint[];
}

export interface DailyTransactionsPoint extends StatisticsSeriesPoint {
  transactionCount?: number;
  blockCount?: number;
  mergeTransactionCount?: number;
}

export interface DailyTransactionsResponse extends StatisticsListResponse {
  list?: DailyTransactionsPoint[];
}

export interface DailyTransactionInfoChain {
  transactionAvgByAllType?: number;
  transactionAvgByExcludeSystem?: number;
  [key: string]: unknown;
}

export interface DailyTransactionInfoResponse {
  mainChain?: DailyTransactionInfoChain;
  sideChain?: DailyTransactionInfoChain;
  [key: string]: unknown;
}

export interface DailyActivityAddressChain {
  max?: number;
  min?: number;
  avg?: number;
  [key: string]: unknown;
}

export interface DailyActivityAddressResponse {
  mainChain?: DailyActivityAddressChain;
  sideChain?: DailyActivityAddressChain;
  [key: string]: unknown;
}

export interface NodeCurrentProduceInfoItem {
  nodeAddress?: string;
  producedBlockCount?: number;
  expectedBlockCount?: number;
  [key: string]: unknown;
}

export interface NodeCurrentProduceInfoResponse {
  roundNumber?: number;
  list?: NodeCurrentProduceInfoItem[];
  [key: string]: unknown;
}

export interface ElfSupplyResponse {
  maxSupply?: number;
  burn?: number;
  totalSupply?: number;
  circulatingSupply?: number;
  [key: string]: unknown;
}
