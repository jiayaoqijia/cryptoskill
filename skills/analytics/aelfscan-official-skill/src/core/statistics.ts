import type {
  DailyActivityAddressResponse,
  DailyTransactionInfoResponse,
  DailyTransactionsResponse,
  ElfSupplyResponse,
  NodeCurrentProduceInfoResponse,
  StatisticsListResponse,
} from '../../lib/api-types.js';
import { requireField } from '../../lib/errors.js';
import { request } from '../../lib/http-client.js';
import type {
  StatisticsDateRangeInput,
  StatisticsMetric,
  StatisticsMetricInput,
  StatisticsQueryInput,
  ToolResult,
} from '../../lib/types.js';
import { executeTool, resolveChainId } from './common.js';

function withChainId(input: StatisticsQueryInput): Record<string, unknown> {
  return {
    ...input,
    chainId: resolveChainId(input.chainId),
  };
}

async function getStatistics<T>(
  path: string,
  input: StatisticsQueryInput = {},
  fallbackCode: string,
): Promise<ToolResult<T>> {
  return executeTool(async (traceId) => {
    const result = await request<T>({
      traceId,
      path,
      query: withChainId(input),
    });

    return result;
  }, fallbackCode);
}

async function getDateRangeStatistics<T>(
  path: string,
  input: StatisticsDateRangeInput,
  fallbackCode: string,
): Promise<ToolResult<T>> {
  return executeTool(async (traceId) => {
    requireField(input.startDate, 'startDate');
    requireField(input.endDate, 'endDate');

    const result = await request<T>({
      traceId,
      path,
      query: withChainId(input),
    });

    return result;
  }, fallbackCode);
}

export async function getDailyTransactions(input: StatisticsQueryInput = {}): Promise<ToolResult<DailyTransactionsResponse>> {
  return getStatistics('/api/app/statistics/dailyTransactions', input, 'GET_DAILY_TRANSACTIONS_FAILED');
}

export async function getUniqueAddresses(input: StatisticsQueryInput = {}): Promise<ToolResult<StatisticsListResponse>> {
  return getStatistics('/api/app/statistics/uniqueAddresses', input, 'GET_UNIQUE_ADDRESSES_FAILED');
}

export async function getDailyActiveAddresses(input: StatisticsQueryInput = {}): Promise<ToolResult<StatisticsListResponse>> {
  return getStatistics('/api/app/statistics/dailyActiveAddresses', input, 'GET_DAILY_ACTIVE_ADDRESSES_FAILED');
}

export async function getMonthlyActiveAddresses(
  input: StatisticsQueryInput = {},
): Promise<ToolResult<StatisticsListResponse>> {
  return getStatistics('/api/app/statistics/monthlyActiveAddresses', input, 'GET_MONTHLY_ACTIVE_ADDRESSES_FAILED');
}

export async function getBlockProduceRate(input: StatisticsQueryInput = {}): Promise<ToolResult<StatisticsListResponse>> {
  return getStatistics('/api/app/statistics/blockProduceRate', input, 'GET_BLOCK_PRODUCE_RATE_FAILED');
}

export async function getAvgBlockDuration(input: StatisticsQueryInput = {}): Promise<ToolResult<StatisticsListResponse>> {
  return getStatistics('/api/app/statistics/avgBlockDuration', input, 'GET_AVG_BLOCK_DURATION_FAILED');
}

export async function getCycleCount(input: StatisticsQueryInput = {}): Promise<ToolResult<StatisticsListResponse>> {
  return getStatistics('/api/app/statistics/cycleCount', input, 'GET_CYCLE_COUNT_FAILED');
}

export async function getNodeBlockProduce(input: StatisticsQueryInput = {}): Promise<ToolResult<StatisticsListResponse>> {
  return getStatistics('/api/app/statistics/nodeBlockProduce', input, 'GET_NODE_BLOCK_PRODUCE_FAILED');
}

export async function getDailyAvgTransactionFee(
  input: StatisticsQueryInput = {},
): Promise<ToolResult<StatisticsListResponse>> {
  return getStatistics('/api/app/statistics/dailyAvgTransactionFee', input, 'GET_DAILY_AVG_TRANSACTION_FEE_FAILED');
}

export async function getDailyTxFee(input: StatisticsQueryInput = {}): Promise<ToolResult<StatisticsListResponse>> {
  return getStatistics('/api/app/statistics/dailyTxFee', input, 'GET_DAILY_TX_FEE_FAILED');
}

export async function getDailyTotalBurnt(input: StatisticsQueryInput = {}): Promise<ToolResult<StatisticsListResponse>> {
  return getStatistics('/api/app/statistics/dailyTotalBurnt', input, 'GET_DAILY_TOTAL_BURNT_FAILED');
}

export async function getDailyElfPrice(input: StatisticsQueryInput = {}): Promise<ToolResult<StatisticsListResponse>> {
  return getStatistics('/api/app/statistics/dailyElfPrice', input, 'GET_DAILY_ELF_PRICE_FAILED');
}

export async function getDailyDeployContract(
  input: StatisticsQueryInput = {},
): Promise<ToolResult<StatisticsListResponse>> {
  return getStatistics('/api/app/statistics/dailyDeployContract', input, 'GET_DAILY_DEPLOY_CONTRACT_FAILED');
}

export async function getDailyBlockReward(input: StatisticsQueryInput = {}): Promise<ToolResult<StatisticsListResponse>> {
  return getStatistics('/api/app/statistics/dailyBlockReward', input, 'GET_DAILY_BLOCK_REWARD_FAILED');
}

export async function getDailyAvgBlockSize(input: StatisticsQueryInput = {}): Promise<ToolResult<StatisticsListResponse>> {
  return getStatistics('/api/app/statistics/dailyAvgBlockSize', input, 'GET_DAILY_AVG_BLOCK_SIZE_FAILED');
}

export async function getTopContractCall(input: StatisticsQueryInput = {}): Promise<ToolResult<StatisticsListResponse>> {
  return getStatistics('/api/app/statistics/topContractCall', input, 'GET_TOP_CONTRACT_CALL_FAILED');
}

export async function getDailyContractCall(input: StatisticsQueryInput = {}): Promise<ToolResult<StatisticsListResponse>> {
  return getStatistics('/api/app/statistics/dailyContractCall', input, 'GET_DAILY_CONTRACT_CALL_FAILED');
}

export async function getDailySupplyGrowth(input: StatisticsQueryInput = {}): Promise<ToolResult<StatisticsListResponse>> {
  return getStatistics('/api/app/statistics/dailySupplyGrowth', input, 'GET_DAILY_SUPPLY_GROWTH_FAILED');
}

export async function getDailyMarketCap(input: StatisticsQueryInput = {}): Promise<ToolResult<StatisticsListResponse>> {
  return getStatistics('/api/app/statistics/dailyMarketCap', input, 'GET_DAILY_MARKET_CAP_FAILED');
}

export async function getDailyStaked(input: StatisticsQueryInput = {}): Promise<ToolResult<StatisticsListResponse>> {
  return getStatistics('/api/app/statistics/dailyStaked', input, 'GET_DAILY_STAKED_FAILED');
}

export async function getDailyHolder(input: StatisticsQueryInput = {}): Promise<ToolResult<StatisticsListResponse>> {
  return getStatistics('/api/app/statistics/dailyHolder', input, 'GET_DAILY_HOLDER_FAILED');
}

export async function getDailyTvl(input: StatisticsQueryInput = {}): Promise<ToolResult<StatisticsListResponse>> {
  return getStatistics('/api/app/statistics/dailyTvl', input, 'GET_DAILY_TVL_FAILED');
}

export async function getNodeCurrentProduceInfo(
  input: StatisticsQueryInput = {},
): Promise<ToolResult<NodeCurrentProduceInfoResponse>> {
  return getStatistics('/api/app/statistics/nodeCurrentProduceInfo', input, 'GET_NODE_CURRENT_PRODUCE_INFO_FAILED');
}

export async function getElfSupply(input: StatisticsQueryInput = {}): Promise<ToolResult<ElfSupplyResponse>> {
  return getStatistics('/api/app/statistics/elfSupply', input, 'GET_ELF_SUPPLY_FAILED');
}

export async function getDailyTransactionInfo(
  input: StatisticsDateRangeInput,
): Promise<ToolResult<DailyTransactionInfoResponse>> {
  return getDateRangeStatistics('/api/app/statistics/dailyTransactionInfo', input, 'GET_DAILY_TRANSACTION_INFO_FAILED');
}

export async function getDailyActivityAddress(
  input: StatisticsDateRangeInput,
): Promise<ToolResult<DailyActivityAddressResponse>> {
  return getDateRangeStatistics('/api/app/statistics/dailyActivityAddress', input, 'GET_DAILY_ACTIVITY_ADDRESS_FAILED');
}

export async function getCurrencyPrice(input: StatisticsQueryInput = {}): Promise<ToolResult<StatisticsListResponse>> {
  return getStatistics('/api/app/statistics/currencyPrice', input, 'GET_CURRENCY_PRICE_FAILED');
}

export const STATISTICS_METRICS = [
  'dailyTransactions',
  'uniqueAddresses',
  'dailyActiveAddresses',
  'monthlyActiveAddresses',
  'blockProduceRate',
  'avgBlockDuration',
  'cycleCount',
  'nodeBlockProduce',
  'dailyAvgTransactionFee',
  'dailyTxFee',
  'dailyTotalBurnt',
  'dailyElfPrice',
  'dailyDeployContract',
  'dailyBlockReward',
  'dailyAvgBlockSize',
  'topContractCall',
  'dailyContractCall',
  'dailySupplyGrowth',
  'dailyMarketCap',
  'dailyStaked',
  'dailyHolder',
  'dailyTvl',
  'nodeCurrentProduceInfo',
  'elfSupply',
  'dailyTransactionInfo',
  'dailyActivityAddress',
  'currencyPrice',
] as const satisfies ReadonlyArray<StatisticsMetric>;

type StatisticsMetricPayload = Omit<StatisticsMetricInput, 'metric'>;
type StatisticsMetricHandler = (input: StatisticsMetricPayload) => Promise<ToolResult<unknown>>;

const STATISTICS_METRIC_HANDLER_MAP: Record<StatisticsMetric, StatisticsMetricHandler> = {
  dailyTransactions: getDailyTransactions,
  uniqueAddresses: getUniqueAddresses,
  dailyActiveAddresses: getDailyActiveAddresses,
  monthlyActiveAddresses: getMonthlyActiveAddresses,
  blockProduceRate: getBlockProduceRate,
  avgBlockDuration: getAvgBlockDuration,
  cycleCount: getCycleCount,
  nodeBlockProduce: getNodeBlockProduce,
  dailyAvgTransactionFee: getDailyAvgTransactionFee,
  dailyTxFee: getDailyTxFee,
  dailyTotalBurnt: getDailyTotalBurnt,
  dailyElfPrice: getDailyElfPrice,
  dailyDeployContract: getDailyDeployContract,
  dailyBlockReward: getDailyBlockReward,
  dailyAvgBlockSize: getDailyAvgBlockSize,
  topContractCall: getTopContractCall,
  dailyContractCall: getDailyContractCall,
  dailySupplyGrowth: getDailySupplyGrowth,
  dailyMarketCap: getDailyMarketCap,
  dailyStaked: getDailyStaked,
  dailyHolder: getDailyHolder,
  dailyTvl: getDailyTvl,
  nodeCurrentProduceInfo: getNodeCurrentProduceInfo,
  elfSupply: getElfSupply,
  dailyTransactionInfo: input => getDailyTransactionInfo(input as StatisticsDateRangeInput),
  dailyActivityAddress: input => getDailyActivityAddress(input as StatisticsDateRangeInput),
  currencyPrice: getCurrencyPrice,
};

export async function getStatisticsByMetric(input: StatisticsMetricInput): Promise<ToolResult<unknown>> {
  const { metric, ...payload } = input;
  const handler = STATISTICS_METRIC_HANDLER_MAP[metric];
  return handler(payload);
}
