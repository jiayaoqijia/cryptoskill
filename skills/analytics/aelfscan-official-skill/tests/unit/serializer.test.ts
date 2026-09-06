import { describe, expect, test } from 'bun:test';
import { serializeQuery } from '../../lib/serializer.js';

describe('serializeQuery', () => {
  test('returns empty query for undefined or empty input', () => {
    expect(serializeQuery(undefined)).toBe('');
    expect(serializeQuery({})).toBe('');
  });

  test('serializes primitive values', () => {
    const query = serializeQuery({ chainId: 'AELF', maxResultCount: 10, skipCount: 0 });
    expect(query).toContain('chainId=AELF');
    expect(query).toContain('maxResultCount=10');
    expect(query).toContain('skipCount=0');
  });

  test('serializes orderInfos in aelfscan style', () => {
    const query = serializeQuery({
      orderInfos: [
        { orderBy: 'BlockTime', sort: 'Desc' },
        { orderBy: 'TransactionId', sort: 'Desc' },
      ],
    });

    expect(query).toContain('orderInfos[0].orderBy=BlockTime');
    expect(query).toContain('orderInfos[0].sort=Desc');
    expect(query).toContain('orderInfos[1].orderBy=TransactionId');
    expect(query).toContain('orderInfos[1].sort=Desc');
  });

  test('supports nested object and array values', () => {
    const query = serializeQuery({
      test: {
        inner: 'abc',
      },
      list: [1, 2],
    });

    expect(query).toContain('test[inner]=abc');
    expect(query).toContain('list[0]=1');
    expect(query).toContain('list[1]=2');
  });

  test('skips undefined/null and keeps empty string in arrays', () => {
    const query = serializeQuery({
      values: [undefined, null, ''],
    });

    expect(query).not.toContain('values[0]');
    expect(query).not.toContain('values[1]');
    expect(query).toContain('values[2]=');
  });

  test('returns empty when keys exist but all values are filtered out', () => {
    const query = serializeQuery({
      foo: undefined,
      bar: null,
      baz: Number.NaN,
    });

    expect(query).toBe('');
  });
});
