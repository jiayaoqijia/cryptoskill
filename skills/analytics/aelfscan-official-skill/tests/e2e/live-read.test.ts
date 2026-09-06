import { describe, expect, test } from 'bun:test';
import {
  getAddressDetail,
  getBlockDetail,
  getBlocks,
  getSearchFilters,
  getTokenDetail,
  getTransactionDetail,
  search,
} from '../../index.js';

const shouldRunLive = process.env.RUN_LIVE_TESTS === '1';
const maybe = shouldRunLive ? describe : describe.skip;

maybe('live read smoke', () => {
  test('search filters', async () => {
    const result = await getSearchFilters({ chainId: 'AELF' });
    expect(result.success).toBe(true);
  });

  test('blocks and block detail', async () => {
    const blocks = await getBlocks({ chainId: 'AELF', maxResultCount: 1, skipCount: 0 });
    expect(blocks.success).toBe(true);

    const first = (blocks.data as any)?.blocks?.[0];
    if (first?.blockHeight !== undefined) {
      const detail = await getBlockDetail({ chainId: 'AELF', blockHeight: Number(first.blockHeight) });
      expect(detail.success).toBe(true);
    }
  });

  test('search and transaction detail', async () => {
    const result = await search({ chainId: 'AELF', keyword: 'ELF', filterType: 0, searchType: 0 });
    expect(result.success).toBe(true);

    const tx = (result.data as any)?.transaction;
    if (tx?.transactionId) {
      const detail = await getTransactionDetail({ chainId: 'AELF', transactionId: tx.transactionId });
      expect(detail.success).toBe(true);
    }
  });

  test('token detail and address detail', async () => {
    const token = await getTokenDetail({ chainId: 'AELF', symbol: 'ELF' });
    expect(token.success).toBe(true);

    const address = await getAddressDetail({
      chainId: 'AELF',
      address: 'JRmBduh4nXWi1aXgdUsj5gJrzeZb2LxmrAbf7W99faZSvoAaE',
    });
    expect(address.success).toBe(true);
  });
});
