import { describe, expect, test } from 'bun:test';
import { networkProposalsList } from '../../src/domains/network.js';
import { resourceRealtimeRecords } from '../../src/domains/resource.js';

const runE2E = process.env.RUN_TMRW_E2E === '1';

describe('e2e read-only smoke', () => {
  test('network proposals list', async () => {
    if (!runE2E) return;
    const res = await networkProposalsList({ chainId: 'AELF', maxResultCount: 5 });
    expect(res.success).toBeTrue();
  });

  test('resource realtime records', async () => {
    if (!runE2E) return;
    const res = await resourceRealtimeRecords({ chainId: 'AELF', maxResultCount: 5 });
    expect(res.success).toBeTrue();
  });

  test('e2e marker', () => {
    expect(runE2E === false || runE2E === true).toBeTrue();
  });
});
