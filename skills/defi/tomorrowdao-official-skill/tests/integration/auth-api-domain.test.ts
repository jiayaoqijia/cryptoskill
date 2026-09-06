import { afterEach, beforeEach, describe, expect, test } from 'bun:test';
import { clearTokenCache } from '../../src/core/auth.js';
import { resetConfigCache } from '../../src/core/config.js';
import { bpTeamDescAdd } from '../../src/domains/bp.js';
import { discussionComment } from '../../src/domains/dao.js';
import { networkContractNameAdd } from '../../src/domains/network.js';
import { restoreTestEnv, resetTestEnv } from '../helpers/env.js';
import { installFetchMock, jsonResponse } from '../helpers/mock-fetch.js';

describe('integration auth + api + domain', () => {
  let restoreFetch: (() => void) | undefined;

  beforeEach(() => {
    resetTestEnv({
      TMRW_PRIVATE_KEY: '1'.repeat(64),
      TMRW_API_BASE: 'https://api.tmrwdao.com',
      TMRW_AUTH_BASE: 'https://api.tmrwdao.com',
    });
    clearTokenCache();
    resetConfigCache();
  });

  afterEach(() => {
    if (restoreFetch) restoreFetch();
    clearTokenCache();
    resetConfigCache();
    restoreTestEnv();
  });

  test('reuses auth token across multiple domain auth endpoints', async () => {
    const authHeaders: string[] = [];

    const mocked = installFetchMock((url, init) => {
      if (url.endsWith('/connect/token')) {
        return jsonResponse({
          access_token: 'integration-token',
          token_type: 'Bearer',
          expires_in: 120,
        });
      }

      const headers = (init?.headers || {}) as Record<string, string>;
      authHeaders.push(headers.Authorization || '');

      if (url.includes('/discussion/new-comment')) {
        return jsonResponse({ code: '20000', data: { id: 'comment-1' } });
      }
      if (url.includes('/networkdao/contract/add')) {
        return jsonResponse({ code: '20000', data: { id: 'contract-1' } });
      }
      if (url.includes('/networkdao/vote/addTeamDesc')) {
        return jsonResponse({ code: '20000', data: { id: 'team-1' } });
      }

      return jsonResponse({ code: '20000', data: {} });
    });
    restoreFetch = mocked.restore;

    const comment = await discussionComment({
      chainId: 'tDVV',
      proposalId: 'p-1',
      comment: 'integration test',
    });

    const contract = await networkContractNameAdd({
      chainId: 'AELF',
      operateChainId: 'AELF',
      contractName: 'DemoContract',
      txId: 'tx-1',
      action: 1,
      address: 'address-1',
    });

    const team = await bpTeamDescAdd({
      chainId: 'AELF',
      publicKey: 'pubkey-1',
      address: 'address-1',
      name: 'team',
    });

    expect(comment.success).toBeTrue();
    expect(contract.success).toBeTrue();
    expect(team.success).toBeTrue();
    expect(mocked.calls.filter((x) => x.url.endsWith('/connect/token')).length).toBe(1);
    expect(authHeaders.every((header) => header === 'Bearer integration-token')).toBeTrue();
  });
});
