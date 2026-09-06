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
import { getSearchFilters, search } from '../../src/core/search.js';
import { getTokenDetail, getTokenHolders, getTokens, getTokenTransfers } from '../../src/core/token.js';
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
  STATISTICS_METRICS,
  getCurrencyPrice,
  getDailyActivityAddress,
  getDailyTransactionInfo,
  getDailyTransactions,
  getStatisticsByMetric,
  getUniqueAddresses,
} from '../../src/core/statistics.js';

const originalFetch = globalThis.fetch;
const seenRequests: Array<{ url: string; method: string; body?: string | null }> = [];

function okData(url: string) {
  return {
    code: '20000',
    message: '',
    data: {
      items: [],
      totalCount: 0,
      marker: url,
      result: 'ok',
    },
  };
}

function installFetchMock() {
  globalThis.fetch = (async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = String(input);
    const method = init?.method || 'GET';
    const body = typeof init?.body === 'string' ? init.body : null;
    seenRequests.push({ url, method, body });

    return new Response(JSON.stringify(okData(url)), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  }) as unknown as typeof fetch;
}

afterEach(() => {
  seenRequests.length = 0;
  globalThis.fetch = originalFetch;
});

describe('aelfscan core api coverage', () => {
  test('search + blockchain happy path', async () => {
    installFetchMock();

    const filters = await getSearchFilters({ chainId: 'AELF' });
    const searchResult = await search({ chainId: 'AELF', keyword: 'ELF', filterType: 0, searchType: 0 });
    const blocks = await getBlocks({ chainId: 'AELF', skipCount: 0, maxResultCount: 2 });
    const latestBlocks = await getLatestBlocks({ chainId: 'AELF', maxResultCount: 3 });
    const blockDetail = await getBlockDetail({ chainId: 'AELF', blockHeight: 123 });
    const txs = await getTransactions({ chainId: 'AELF', skipCount: 0, maxResultCount: 2, address: 'ELF_addr' });
    const latestTxs = await getLatestTransactions({ chainId: 'AELF', maxResultCount: 2 });
    const txDetail = await getTransactionDetail({ chainId: 'AELF', transactionId: '0xabc' });
    const overview = await getBlockchainOverview({ chainId: 'AELF', blockTime: '1D' as any });
    const chart = await getTransactionDataChart({ chainId: 'AELF' });
    const dict = await getAddressDictionary({
      chainId: 'AELF',
      name: 'test-dict',
      addresses: ['ELF_123_AELF', 'ELF_456_AELF'],
    });
    const events = await getLogEvents({
      chainId: 'AELF',
      contractAddress: '2mABCDEF1234567890',
      skipCount: 0,
      maxResultCount: 1,
    });

    for (const result of [
      filters,
      searchResult,
      blocks,
      latestBlocks,
      blockDetail,
      txs,
      latestTxs,
      txDetail,
      overview,
      chart,
      dict,
      events,
    ]) {
      expect(result.success).toBe(true);
    }

    expect(seenRequests.length).toBeGreaterThanOrEqual(12);
    expect(seenRequests.some((entry) => entry.url.includes('/api/app/blockchain/blocks'))).toBe(true);
    expect(seenRequests.some((entry) => entry.url.includes('/api/app/blockchain/search'))).toBe(true);
    expect(seenRequests.some((entry) => entry.method === 'POST')).toBe(true);
  });

  test('address + token + nft happy path', async () => {
    installFetchMock();

    const accounts = await getAccounts({ chainId: 'AELF', skipCount: 0, maxResultCount: 2 });
    const contracts = await getContracts({ chainId: 'AELF', skipCount: 0, maxResultCount: 2 });
    const detail = await getAddressDetail({ chainId: 'AELF', address: 'ELF_abc_AELF' });
    const tokens = await getAddressTokens({ chainId: 'AELF', address: 'ELF_abc_AELF', skipCount: 0, maxResultCount: 2 });
    const nftAssets = await getAddressNftAssets({ chainId: 'AELF', address: 'ELF_abc_AELF', skipCount: 0, maxResultCount: 2 });
    const transfers = await getAddressTransfers({ chainId: 'AELF', address: 'ELF_abc_AELF', skipCount: 0, maxResultCount: 2 });
    const history = await getContractHistory({ chainId: 'AELF', address: 'ELF_abc_AELF' });
    const contractEvents = await getContractEvents({ chainId: 'AELF', contractAddress: 'ELF_contract_AELF', skipCount: 0, maxResultCount: 2 });
    const source = await getContractSource({ chainId: 'AELF', address: 'ELF_contract_AELF' });

    const tokenList = await getTokens({ chainId: 'AELF', skipCount: 0, maxResultCount: 2, symbols: ['ELF'] });
    const tokenDetail = await getTokenDetail({ chainId: 'AELF', symbol: 'ELF' });
    const tokenTransfers = await getTokenTransfers({ chainId: 'AELF', symbol: 'ELF', skipCount: 0, maxResultCount: 2 });
    const holders = await getTokenHolders({ chainId: 'AELF', symbol: 'ELF', skipCount: 0, maxResultCount: 2 });

    const collections = await getNftCollections({ chainId: 'AELF', skipCount: 0, maxResultCount: 2 });
    const collectionDetail = await getNftCollectionDetail({ chainId: 'AELF', collectionSymbol: 'COOL' });
    const nftTransfers = await getNftTransfers({ chainId: 'AELF', collectionSymbol: 'COOL', skipCount: 0, maxResultCount: 2 });
    const nftHolders = await getNftHolders({ chainId: 'AELF', collectionSymbol: 'COOL', skipCount: 0, maxResultCount: 2 });
    const inventory = await getNftInventory({ chainId: 'AELF', collectionSymbol: 'COOL', skipCount: 0, maxResultCount: 2 });
    const itemDetail = await getNftItemDetail({ chainId: 'AELF', symbol: 'COOL-1' });
    const itemHolders = await getNftItemHolders({ chainId: 'AELF', symbol: 'COOL-1', skipCount: 0, maxResultCount: 2 });
    const itemActivity = await getNftItemActivity({ chainId: 'AELF', symbol: 'COOL-1', skipCount: 0, maxResultCount: 2 });

    for (const result of [
      accounts,
      contracts,
      detail,
      tokens,
      nftAssets,
      transfers,
      history,
      contractEvents,
      source,
      tokenList,
      tokenDetail,
      tokenTransfers,
      holders,
      collections,
      collectionDetail,
      nftTransfers,
      nftHolders,
      inventory,
      itemDetail,
      itemHolders,
      itemActivity,
    ]) {
      expect(result.success).toBe(true);
    }

    expect(seenRequests.some((entry) => entry.url.includes('/api/app/address/detail'))).toBe(true);
    expect(seenRequests.some((entry) => entry.url.includes('/api/app/token/detail'))).toBe(true);
    expect(seenRequests.some((entry) => entry.url.includes('/api/app/token/nft/item-activity'))).toBe(true);
  });

  test('statistics happy path + metric router', async () => {
    installFetchMock();

    const daily = await getDailyTransactions({ chainId: 'AELF' });
    const unique = await getUniqueAddresses({ chainId: 'AELF' });
    const txInfo = await getDailyTransactionInfo({ chainId: 'AELF', startDate: '2026-02-01', endDate: '2026-02-27' });
    const active = await getDailyActivityAddress({ chainId: 'AELF', startDate: '2026-02-01', endDate: '2026-02-27' });
    const currency = await getCurrencyPrice({ chainId: 'AELF' });

    expect(daily.success).toBe(true);
    expect(unique.success).toBe(true);
    expect(txInfo.success).toBe(true);
    expect(active.success).toBe(true);
    expect(currency.success).toBe(true);

    for (const metric of STATISTICS_METRICS) {
      const payload =
        metric === 'dailyTransactionInfo' || metric === 'dailyActivityAddress'
          ? { metric, chainId: 'AELF', startDate: '2026-02-01', endDate: '2026-02-27' }
          : { metric, chainId: 'AELF' };
      const result = await getStatisticsByMetric(payload as any);
      expect(result.success).toBe(true);
    }

    expect(seenRequests.some((entry) => entry.url.includes('/api/app/statistics/dailyTransactions'))).toBe(true);
    expect(seenRequests.some((entry) => entry.url.includes('/api/app/statistics/currencyPrice'))).toBe(true);
  });

  test('required input guards return failure envelope', async () => {
    installFetchMock();

    const missingKeyword = await search({ chainId: 'AELF', keyword: '' as any });
    const missingBlockHeight = await getBlockDetail({ chainId: 'AELF' } as any);
    const missingAddress = await getAddressDetail({ chainId: 'AELF', address: '' } as any);
    const missingSymbol = await getTokenDetail({ chainId: 'AELF', symbol: '' } as any);
    const missingCollection = await getNftCollectionDetail({ chainId: 'AELF', collectionSymbol: '' } as any);
    const missingDateRange = await getDailyTransactionInfo({ chainId: 'AELF', startDate: '' as any, endDate: '2026-02-27' });

    for (const result of [
      missingKeyword,
      missingBlockHeight,
      missingAddress,
      missingSymbol,
      missingCollection,
      missingDateRange,
    ]) {
      expect(result.success).toBe(false);
      expect(result.error?.code).toBe('INVALID_INPUT');
    }
  });
});
