import { describe, expect, test } from 'bun:test';
import AElf from 'aelf-sdk';

// ---------------------------------------------------------------------------
// chainIdToNum — validate base58 chain ID conversion matches aelf-sdk
// ---------------------------------------------------------------------------

const { base58ToChainId } = AElf.utils.chainIdConvertor;

describe('chainIdToNum (base58 chain ID conversion)', () => {
  test('AELF → 9992731', () => {
    expect(base58ToChainId('AELF')).toBe(9992731);
  });

  test('tDVV → 1866392', () => {
    expect(base58ToChainId('tDVV')).toBe(1866392);
  });

  test('roundtrip: chainIdToBase58(base58ToChainId(x)) === x', () => {
    const { chainIdToBase58 } = AElf.utils.chainIdConvertor;
    for (const id of ['AELF', 'tDVV']) {
      expect(chainIdToBase58(base58ToChainId(id))).toBe(id);
    }
  });
});
