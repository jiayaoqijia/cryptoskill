import { afterEach, beforeEach, describe, expect, test } from 'bun:test';
import { clearTokenCache } from '../../src/core/auth.js';
import { resetConfigCache } from '../../src/core/config.js';
import {
  bpApply,
  bpChangeVote,
  bpClaimProfits,
  bpQuit,
  bpTeamDescAdd,
  bpTeamDescGet,
  bpTeamDescList,
  bpVote,
  bpVoteReclaim,
  bpVotesList,
  bpWithdraw,
} from '../../src/domains/bp.js';
import { restoreTestEnv, resetTestEnv } from '../helpers/env.js';
import { installFetchMock, jsonResponse } from '../helpers/mock-fetch.js';

describe('bp domain', () => {
  let restoreFetch: (() => void) | undefined;

  beforeEach(() => {
    resetTestEnv({
      TMRW_PRIVATE_KEY: '1'.repeat(64),
      TMRW_API_BASE: 'https://api.tmrwdao.com',
      TMRW_AUTH_BASE: 'https://api.tmrwdao.com',
      TMRW_CHAIN_DEFAULT_NETWORK: 'AELF',
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

  test('supports simulate election operations', async () => {
    const apply = await bpApply({ chainId: 'AELF', args: { value: 1 }, mode: 'simulate' });
    const quit = await bpQuit({ chainId: 'AELF', args: { value: 1 }, mode: 'simulate' });
    const vote = await bpVote({ chainId: 'AELF', args: { value: 1 }, mode: 'simulate' });
    const withdraw = await bpWithdraw({ chainId: 'AELF', args: { value: 1 }, mode: 'simulate' });
    const changeVote = await bpChangeVote({ chainId: 'AELF', args: { value: 1 }, mode: 'simulate' });
    const claim = await bpClaimProfits({ chainId: 'AELF', args: { value: 1 }, mode: 'simulate' });

    expect(apply.success).toBeTrue();
    expect(quit.success).toBeTrue();
    expect(vote.success).toBeTrue();
    expect(withdraw.success).toBeTrue();
    expect(changeVote.success).toBeTrue();
    expect(claim.success).toBeTrue();
  });

  test('supports read-only and auth APIs', async () => {
    const mocked = installFetchMock((url) => {
      if (url.endsWith('/connect/token')) {
        return jsonResponse({
          access_token: 'bp-token',
          token_type: 'Bearer',
          expires_in: 120,
        });
      }
      if (url.includes('/networkdao/votes')) {
        return jsonResponse({ code: '20000', data: { items: [] } });
      }
      if (url.includes('/networkdao/vote/getTeamDesc')) {
        return jsonResponse({ code: '20000', data: { publicKey: 'pk-1' } });
      }
      if (url.includes('/networkdao/vote/getAllTeamDesc')) {
        return jsonResponse({ code: '20000', data: { items: [] } });
      }
      if (url.includes('/networkdao/vote/addTeamDesc')) {
        return jsonResponse({ code: '20000', data: { id: 'desc-1' } });
      }
      if (url.includes('/networkdao/vote/reclaim')) {
        return jsonResponse({ code: '20000', data: { id: 'reclaim-1' } });
      }
      return jsonResponse({ code: '20000', data: {} });
    });
    restoreFetch = mocked.restore;

    const votes = await bpVotesList({ chainId: 'AELF', maxResultCount: 5 });
    const get = await bpTeamDescGet({ chainId: 'AELF', publicKey: 'pk-1' });
    const list = await bpTeamDescList({ chainId: 'AELF' });
    const add = await bpTeamDescAdd({
      chainId: 'AELF',
      publicKey: 'pk-1',
      address: 'address-1',
      name: 'Team A',
      intro: 'desc',
    });
    const reclaim = await bpVoteReclaim({
      chainId: 'AELF',
      voteId: 'vote-1',
      proposalId: 'proposal-1',
    });

    expect(votes.success).toBeTrue();
    expect(get.success).toBeTrue();
    expect(list.success).toBeTrue();
    expect(add.success).toBeTrue();
    expect(reclaim.success).toBeTrue();
    expect(mocked.calls.filter((x) => x.url.endsWith('/connect/token')).length).toBe(1);
  });

  test('rejects non-AELF chain', async () => {
    const result = await bpApply({ chainId: 'tDVV', args: { value: 1 }, mode: 'simulate' });
    expect(result.success).toBeFalse();
    expect(result.error?.code).toBe('UNSUPPORTED_CHAIN');
  });

  test('returns INVALID_INPUT when required fields are missing', async () => {
    const team = await bpTeamDescAdd({
      chainId: 'AELF',
      publicKey: '',
      address: '',
      name: '',
    } as any);

    expect(team.success).toBeFalse();
    expect(team.error?.code).toBe('INVALID_INPUT');
  });
});
