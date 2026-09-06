import { describe, expect, test } from 'bun:test';
import { normalizeAddress, normalizeChainId } from '../../lib/normalize.js';

describe('normalize', () => {
  test('normalizes chain id', () => {
    expect(normalizeChainId('multiChain')).toBe('');
    expect(normalizeChainId('   ')).toBe('');
    expect(normalizeChainId('AELF')).toBe('AELF');
    expect(normalizeChainId('')).toBe('');
    expect(normalizeChainId(undefined)).toBe('');
  });

  test('normalizes address formats', () => {
    const raw = 'JRmBduh4nXWi1aXgdUsj5gJrzeZb2LxmrAbf7W99faZSvoAaE';
    const withNewLine = 'abc\ndef';
    expect(normalizeAddress(raw)).toBe(raw);
    expect(normalizeAddress(`ELF_${raw}_AELF`)).toBe(raw);
    expect(normalizeAddress(`ELF_${raw}_tDVV`)).toBe(raw);
    expect(normalizeAddress(withNewLine)).toBe(withNewLine);
    expect(normalizeAddress('   ')).toBe('');
    expect(normalizeAddress(undefined)).toBe('');
  });
});
