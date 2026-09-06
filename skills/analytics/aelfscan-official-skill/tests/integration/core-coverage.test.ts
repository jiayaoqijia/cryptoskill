import { afterEach, describe, expect, test } from 'bun:test';
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
} from '../../src/core/blockchain.js';
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
} from '../../src/core/address.js';
import {
  getNftCollectionDetail,
  getNftCollections,
  getNftHolders,
  getNftInventory,
  getNftItemActivity,
  getNftItemDetail,
  getNftItemHolders,
  getNftTransfers,
} from '../../src/core/nft.js';
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
  getTopContractCall,
  getUniqueAddresses,
} from '../../src/core/statistics.js';
import { getSearchFilters } from '../../src/core/search.js';
import { getTokenDetail, getTokenHolders, getTokens, getTokenTransfers } from '../../src/core/token.js';

const originalFetch = globalThis.fetch;

afterEach(() => {
  globalThis.fetch = originalFetch;
});

function mockEnvelopeFetch() {
  const calls: Array<{ url: string; method: string; body?: string }> = [];

  globalThis.fetch = (async (input: RequestInfo | URL, init?: RequestInit) => {
    calls.push({
      url: String(input),
      method: String(init?.method || 'GET'),
      body: typeof init?.body === 'string' ? init.body : undefined,
    });

    return new Response(
      JSON.stringify({
        code: '20000',
        data: { ok: true },
        message: '',
      }),
      { status: 200, headers: { 'Content-Type': 'application/json' } },
    );
  }) as typeof fetch;

  return calls;
}

function expectPathCalled(calls: Array<{ url: string }>, path: string): void {
  expect(calls.some((call) => call.url.includes(path))).toBe(true);
}

describe('core wrapper coverage', () => {
  test('covers address/token/nft/search endpoints', async () => {
    const calls = mockEnvelopeFetch();
    const address = 'ELF_2QfxpszFfG2jxhw72iHY4dM6Z1ZZCYxvKf1MsA3bejnBws9RMG_AELF';

    const results = await Promise.all([
      getSearchFilters({ chainId: 'AELF' }),

      getAccounts({ chainId: 'AELF', skipCount: 0, maxResultCount: 1 }),
      getContracts({ chainId: 'AELF', skipCount: 0, maxResultCount: 1 }),
      getAddressDetail({ chainId: 'AELF', address }),
      getAddressTokens({ chainId: 'AELF', address, skipCount: 0, maxResultCount: 1 }),
      getAddressNftAssets({ chainId: 'AELF', address, skipCount: 0, maxResultCount: 1 }),
      getAddressTransfers({ chainId: 'AELF', address, skipCount: 0, maxResultCount: 1 }),
      getContractHistory({ chainId: 'AELF', address }),
      getContractEvents({ chainId: 'AELF', contractAddress: address, skipCount: 0, maxResultCount: 1 }),
      getContractSource({ chainId: 'AELF', address }),

      getTokens({ chainId: 'AELF', skipCount: 0, maxResultCount: 1 }),
      getTokenDetail({ chainId: 'AELF', symbol: 'ELF' }),
      getTokenTransfers({ chainId: 'AELF', symbol: 'ELF', address, skipCount: 0, maxResultCount: 1 }),
      getTokenHolders({ chainId: 'AELF', symbol: 'ELF', skipCount: 0, maxResultCount: 1 }),

      getNftCollections({ chainId: 'AELF', skipCount: 0, maxResultCount: 1 }),
      getNftCollectionDetail({ chainId: 'AELF', collectionSymbol: 'ABC' }),
      getNftTransfers({ chainId: 'AELF', collectionSymbol: 'ABC', address, skipCount: 0, maxResultCount: 1 }),
      getNftHolders({ chainId: 'AELF', collectionSymbol: 'ABC', skipCount: 0, maxResultCount: 1 }),
      getNftInventory({ chainId: 'AELF', collectionSymbol: 'ABC', skipCount: 0, maxResultCount: 1 }),
      getNftItemDetail({ chainId: 'AELF', symbol: 'ABC-1' }),
      getNftItemHolders({ chainId: 'AELF', symbol: 'ABC-1', skipCount: 0, maxResultCount: 1 }),
      getNftItemActivity({ chainId: 'AELF', symbol: 'ABC-1', skipCount: 0, maxResultCount: 1 }),
    ]);

    results.forEach((result) => {
      expect(result.success).toBe(true);
    });

    expectPathCalled(calls, '/api/app/blockchain/filters');

    expectPathCalled(calls, '/api/app/address/accounts');
    expectPathCalled(calls, '/api/app/address/contracts');
    expectPathCalled(calls, '/api/app/address/detail');
    expectPathCalled(calls, '/api/app/address/tokens');
    expectPathCalled(calls, '/api/app/address/nft-assets');
    expectPathCalled(calls, '/api/app/address/transfers');
    expectPathCalled(calls, '/api/app/address/contract/history');
    expectPathCalled(calls, '/api/app/address/contract/events');
    expectPathCalled(calls, '/api/app/address/contract/file');

    expectPathCalled(calls, '/api/app/token/list');
    expectPathCalled(calls, '/api/app/token/detail');
    expectPathCalled(calls, '/api/app/token/transfers');
    expectPathCalled(calls, '/api/app/token/holders');

    expectPathCalled(calls, '/api/app/token/nft/collection-list');
    expectPathCalled(calls, '/api/app/token/nft/collection-detail');
    expectPathCalled(calls, '/api/app/token/nft/transfers');
    expectPathCalled(calls, '/api/app/token/nft/holders');
    expectPathCalled(calls, '/api/app/token/nft/inventory');
    expectPathCalled(calls, '/api/app/token/nft/item-detail');
    expectPathCalled(calls, '/api/app/token/nft/item-holders');
    expectPathCalled(calls, '/api/app/token/nft/item-activity');

    const detailCall = calls.find((call) => call.url.includes('/api/app/address/detail'));
    expect(detailCall?.url.includes('address=2QfxpszFfG2jxhw72iHY4dM6Z1ZZCYxvKf1MsA3bejnBws9RMG')).toBe(true);
  });

  test('covers blockchain and statistics endpoints', async () => {
    const calls = mockEnvelopeFetch();
    const address = '2QfxpszFfG2jxhw72iHY4dM6Z1ZZCYxvKf1MsA3bejnBws9RMG';

    const blockchainResults = await Promise.all([
      getBlocks({ chainId: 'AELF', skipCount: 0, maxResultCount: 1 }),
      getLatestBlocks({ chainId: 'AELF', maxResultCount: 1 }),
      getBlockDetail({ chainId: 'AELF', blockHeight: 100 }),
      getTransactions({ chainId: 'AELF', skipCount: 0, maxResultCount: 1 }),
      getLatestTransactions({ chainId: 'AELF', maxResultCount: 1 }),
      getTransactionDetail({ chainId: 'AELF', transactionId: '0xabc' }),
      getBlockchainOverview({ chainId: 'AELF' }),
      getTransactionDataChart({ chainId: 'AELF' }),
      getAddressDictionary({ chainId: 'AELF', name: 'test', addresses: [address] }),
      getLogEvents({ chainId: 'AELF', contractAddress: address, skipCount: 0, maxResultCount: 1 }),
    ]);

    const statisticsResults = await Promise.all([
      getDailyTransactions({ chainId: 'AELF' }),
      getUniqueAddresses({ chainId: 'AELF' }),
      getDailyActiveAddresses({ chainId: 'AELF' }),
      getMonthlyActiveAddresses({ chainId: 'AELF' }),
      getBlockProduceRate({ chainId: 'AELF' }),
      getAvgBlockDuration({ chainId: 'AELF' }),
      getCycleCount({ chainId: 'AELF' }),
      getNodeBlockProduce({ chainId: 'AELF' }),
      getDailyAvgTransactionFee({ chainId: 'AELF' }),
      getDailyTxFee({ chainId: 'AELF' }),
      getDailyTotalBurnt({ chainId: 'AELF' }),
      getDailyElfPrice({ chainId: 'AELF' }),
      getDailyDeployContract({ chainId: 'AELF' }),
      getDailyBlockReward({ chainId: 'AELF' }),
      getDailyAvgBlockSize({ chainId: 'AELF' }),
      getTopContractCall({ chainId: 'AELF' }),
      getDailyContractCall({ chainId: 'AELF' }),
      getDailySupplyGrowth({ chainId: 'AELF' }),
      getDailyMarketCap({ chainId: 'AELF' }),
      getDailyStaked({ chainId: 'AELF' }),
      getDailyHolder({ chainId: 'AELF' }),
      getDailyTvl({ chainId: 'AELF' }),
      getNodeCurrentProduceInfo({ chainId: 'AELF' }),
      getElfSupply({ chainId: 'AELF' }),
      getDailyTransactionInfo({ chainId: 'AELF', startDate: '2026-02-20', endDate: '2026-02-26' }),
      getDailyActivityAddress({ chainId: 'AELF', startDate: '2026-02-20', endDate: '2026-02-26' }),
      getCurrencyPrice({ chainId: 'AELF' }),
    ]);

    [...blockchainResults, ...statisticsResults].forEach((result) => {
      expect(result.success).toBe(true);
    });

    expectPathCalled(calls, '/api/app/blockchain/blocks');
    expectPathCalled(calls, '/api/app/blockchain/blockDetail');
    expectPathCalled(calls, '/api/app/blockchain/transactions');
    expectPathCalled(calls, '/api/app/blockchain/transactionDetail');
    expectPathCalled(calls, '/api/app/blockchain/blockchainOverview');
    expectPathCalled(calls, '/api/app/blockchain/transactionDataChart');
    expectPathCalled(calls, '/api/app/blockchain/addressDictionary');
    expectPathCalled(calls, '/api/app/blockchain/logEvents');

    expectPathCalled(calls, '/api/app/statistics/dailyTransactions');
    expectPathCalled(calls, '/api/app/statistics/uniqueAddresses');
    expectPathCalled(calls, '/api/app/statistics/dailyActiveAddresses');
    expectPathCalled(calls, '/api/app/statistics/monthlyActiveAddresses');
    expectPathCalled(calls, '/api/app/statistics/blockProduceRate');
    expectPathCalled(calls, '/api/app/statistics/avgBlockDuration');
    expectPathCalled(calls, '/api/app/statistics/cycleCount');
    expectPathCalled(calls, '/api/app/statistics/nodeBlockProduce');
    expectPathCalled(calls, '/api/app/statistics/dailyAvgTransactionFee');
    expectPathCalled(calls, '/api/app/statistics/dailyTxFee');
    expectPathCalled(calls, '/api/app/statistics/dailyTotalBurnt');
    expectPathCalled(calls, '/api/app/statistics/dailyElfPrice');
    expectPathCalled(calls, '/api/app/statistics/dailyDeployContract');
    expectPathCalled(calls, '/api/app/statistics/dailyBlockReward');
    expectPathCalled(calls, '/api/app/statistics/dailyAvgBlockSize');
    expectPathCalled(calls, '/api/app/statistics/topContractCall');
    expectPathCalled(calls, '/api/app/statistics/dailyContractCall');
    expectPathCalled(calls, '/api/app/statistics/dailySupplyGrowth');
    expectPathCalled(calls, '/api/app/statistics/dailyMarketCap');
    expectPathCalled(calls, '/api/app/statistics/dailyStaked');
    expectPathCalled(calls, '/api/app/statistics/dailyHolder');
    expectPathCalled(calls, '/api/app/statistics/dailyTvl');
    expectPathCalled(calls, '/api/app/statistics/nodeCurrentProduceInfo');
    expectPathCalled(calls, '/api/app/statistics/elfSupply');
    expectPathCalled(calls, '/api/app/statistics/dailyTransactionInfo');
    expectPathCalled(calls, '/api/app/statistics/dailyActivityAddress');
    expectPathCalled(calls, '/api/app/statistics/currencyPrice');

    const overviewCall = calls.find((call) => call.url.includes('/api/app/blockchain/blockchainOverview'));
    const chartCall = calls.find((call) => call.url.includes('/api/app/blockchain/transactionDataChart'));
    const dictionaryCall = calls.find((call) => call.url.includes('/api/app/blockchain/addressDictionary'));
    const logEventsCall = calls.find((call) => call.url.includes('/api/app/blockchain/logEvents'));

    expect(overviewCall?.method).toBe('POST');
    expect(chartCall?.method).toBe('POST');
    expect(dictionaryCall?.method).toBe('POST');
    expect(logEventsCall?.method).toBe('POST');
    expect(dictionaryCall?.body?.includes('"addresses":["2QfxpszFfG2jxhw72iHY4dM6Z1ZZCYxvKf1MsA3bejnBws9RMG"]')).toBe(true);
  });

  test('returns invalid input for required fields', async () => {
    const results = await Promise.all([
      getAddressDetail({ chainId: 'AELF', address: '' }),
      getTokenDetail({ chainId: 'AELF', symbol: '' }),
      getNftCollectionDetail({ chainId: 'AELF', collectionSymbol: '' }),
      getBlockDetail({ chainId: 'AELF', blockHeight: undefined as unknown as number }),
      getTransactionDetail({ chainId: 'AELF', transactionId: '' }),
      getLogEvents({ chainId: 'AELF', contractAddress: '' }),
      getAddressDictionary({ chainId: 'AELF', name: 'x', addresses: [] }),
      getDailyTransactionInfo({ chainId: 'AELF', startDate: '', endDate: '' }),
      getDailyActivityAddress({ chainId: 'AELF', startDate: '', endDate: '' }),
    ]);

    results.forEach((result) => {
      expect(result.success).toBe(false);
      expect(result.error?.code).toBe('INVALID_INPUT');
    });
  });
});
