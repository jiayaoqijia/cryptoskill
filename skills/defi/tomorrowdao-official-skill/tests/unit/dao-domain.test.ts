import { afterEach, beforeEach, describe, expect, test } from 'bun:test';
import { clearTokenCache } from '../../src/core/auth.js';
import { resetConfigCache } from '../../src/core/config.js';
import {
  daoCreate,
  daoExecute,
  daoProposalCreate,
  daoProposalMyInfo,
  daoTokenBalanceView,
  daoRemoveFiles,
  daoTokenAllowanceView,
  daoUpdateMetadata,
  daoUploadFiles,
  daoVote,
  daoWithdraw,
  discussionComment,
  discussionList,
} from '../../src/domains/dao.js';
import { restoreTestEnv, resetTestEnv } from '../helpers/env.js';
import { installFetchMock, jsonResponse } from '../helpers/mock-fetch.js';

describe('dao domain', () => {
  let restoreFetch: (() => void) | undefined;

  beforeEach(() => {
    resetTestEnv({
      TMRW_PRIVATE_KEY: '1'.repeat(64),
      TMRW_API_BASE: 'https://api.tmrwdao.com',
      TMRW_AUTH_BASE: 'https://api.tmrwdao.com',
      TMRW_CHAIN_DEFAULT_DAO: 'tDVV',
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

  test('supports simulate chain operations', async () => {
    const create = await daoCreate({
      chainId: 'tDVV',
      args: { metadata: { name: 'DAO A' } },
      mode: 'simulate',
    });
    const update = await daoUpdateMetadata({
      chainId: 'tDVV',
      daoId: 'dao-1',
      metadata: { intro: 'updated' },
      mode: 'simulate',
    });
    const upload = await daoUploadFiles({
      chainId: 'tDVV',
      daoId: 'dao-1',
      files: [{ cid: 'cid-1', name: 'doc', url: 'https://x.test/doc' }],
      mode: 'simulate',
    });
    const remove = await daoRemoveFiles({
      chainId: 'tDVV',
      daoId: 'dao-1',
      fileCids: ['cid-1'],
      mode: 'simulate',
    });
    const proposal = await daoProposalCreate({
      chainId: 'tDVV',
      methodName: 'CreateProposal',
      args: { proposalBasicInfo: { proposalTitle: 'P1' } },
      mode: 'simulate',
    });
    const vote = await daoVote({
      chainId: 'tDVV',
      args: { proposalId: 'p-1', voteOption: 1, voteAmount: 0 },
      mode: 'simulate',
    });
    const withdraw = await daoWithdraw({
      chainId: 'tDVV',
      args: { daoId: 'dao-1', withdrawAmount: 1000, proposalId: 'p-1' },
      mode: 'simulate',
    });
    const execute = await daoExecute({
      chainId: 'tDVV',
      proposalId: 'p-1',
      mode: 'simulate',
    });

    expect(create.success).toBeTrue();
    expect((create.data as any).methodName).toBe('CreateDAO');
    expect(update.success).toBeTrue();
    expect(upload.success).toBeTrue();
    expect(remove.success).toBeTrue();
    expect(proposal.success).toBeTrue();
    expect(vote.success).toBeTrue();
    expect(withdraw.success).toBeTrue();
    expect(execute.success).toBeTrue();
    expect((vote.data as any).args).toEqual({
      votingItemId: 'p-1',
      voteOption: 1,
      voteAmount: 0,
    });
    expect((withdraw.data as any).args).toEqual({
      daoId: 'dao-1',
      withdrawAmount: 1000,
      votingItemIdList: {
        value: ['p-1'],
      },
    });
  });

  test('supports votingItemId directly for dao vote', async () => {
    const result = await daoVote({
      chainId: 'tDVV',
      args: { votingItemId: 'hash-1', voteOption: 0, voteAmount: 100 },
      mode: 'simulate',
    });

    expect(result.success).toBeTrue();
    expect((result.data as any).args).toEqual({
      votingItemId: 'hash-1',
      voteOption: 0,
      voteAmount: 100,
    });
  });

  test('fails when proposalId and votingItemId differ for dao vote', async () => {
    const result = await daoVote({
      chainId: 'tDVV',
      args: { proposalId: 'proposal-1', votingItemId: 'proposal-2', voteOption: 0, voteAmount: 100 },
      mode: 'simulate',
    });

    expect(result.success).toBeFalse();
    expect(result.error?.code).toBe('INVALID_INPUT');
    expect(result.error?.message).toContain('must match');
  });

  test('normalizes dao withdraw target ids into votingItemIdList', async () => {
    const result = await daoWithdraw({
      chainId: 'tDVV',
      args: {
        daoId: 'dao-1',
        withdrawAmount: 300,
        proposalId: 'proposal-1',
        votingItemIds: ['proposal-2', 'proposal-1'],
      },
      mode: 'simulate',
    });

    expect(result.success).toBeTrue();
    expect((result.data as any).args).toEqual({
      daoId: 'dao-1',
      withdrawAmount: 300,
      votingItemIdList: {
        value: ['proposal-1', 'proposal-2'],
      },
    });
  });

  test('fails fast for deprecated dao withdraw voteRecordId', async () => {
    const result = await daoWithdraw({
      chainId: 'tDVV',
      args: {
        daoId: 'dao-1',
        withdrawAmount: 100,
        proposalId: 'proposal-1',
        voteRecordId: 'vote-record-1',
      },
      mode: 'simulate',
    });

    expect(result.success).toBeFalse();
    expect(result.error?.code).toBe('INVALID_INPUT');
    expect(result.error?.message).toContain('voteRecordId is no longer supported');
  });

  test('supports discussion and my-info APIs', async () => {
    const mocked = installFetchMock((url) => {
      if (url.endsWith('/connect/token')) {
        return jsonResponse({
          access_token: 'dao-token',
          token_type: 'Bearer',
          expires_in: 120,
        });
      }
      if (url.includes('/discussion/comment-list')) {
        return jsonResponse({ code: '20000', data: { items: [{ id: 'c-1' }] } });
      }
      if (url.includes('/discussion/new-comment')) {
        return jsonResponse({ code: '20000', data: { id: 'new-comment' } });
      }
      if (url.includes('/proposal/my-info')) {
        return jsonResponse({ code: '20000', data: { voteAmount: '1000' } });
      }
      return jsonResponse({ code: '20000', data: {} });
    });
    restoreFetch = mocked.restore;

    const list = await discussionList({ chainId: 'tDVV', proposalId: 'p-1', maxResultCount: 5 });
    const comment = await discussionComment({ chainId: 'tDVV', proposalId: 'p-1', comment: 'hello' });
    const myInfo = await daoProposalMyInfo({
      chainId: 'tDVV',
      proposalId: 'p-1',
      address: 'address-1',
      daoId: 'dao-1',
    });

    expect(list.success).toBeTrue();
    expect(comment.success).toBeTrue();
    expect(myInfo.success).toBeTrue();
    expect(mocked.calls.filter((x) => x.url.endsWith('/connect/token')).length).toBe(1);
  });

  test('returns fail result when send mode has no private key', async () => {
    resetTestEnv({
      TMRW_PRIVATE_KEY: undefined,
      TMRW_CHAIN_DEFAULT_DAO: 'tDVV',
    });
    clearTokenCache();
    resetConfigCache();

    const result = await daoVote({
      chainId: 'tDVV',
      args: { proposalId: 'p-1', voteOption: 1, voteAmount: 0 },
      mode: 'send',
    });

    expect(result.success).toBeFalse();
    expect(result.error?.code).toBe('SIGNER_CONTEXT_NOT_FOUND');
  });

  test('returns fail result when send mode resolves to CA signer', async () => {
    resetTestEnv({
      TMRW_PRIVATE_KEY: '1'.repeat(64),
      PORTKEY_CA_HASH: 'ca_hash_1',
      PORTKEY_CA_ADDRESS: 'ELF_ca_1_AELF',
      TMRW_CHAIN_DEFAULT_DAO: 'tDVV',
    });
    clearTokenCache();
    resetConfigCache();

    const result = await daoVote({
      chainId: 'tDVV',
      args: { proposalId: 'p-1', voteOption: 1, voteAmount: 0 },
      mode: 'send',
    });

    expect(result.success).toBeFalse();
    expect(result.error?.code).toBe('SIGNER_CA_DIRECT_SEND_FORBIDDEN');
  });

  test('returns fail result for token allowance on unsupported chain', async () => {
    const result = await daoTokenAllowanceView({
      chainId: 'UNKNOWN' as any,
      symbol: 'ELF',
      owner: 'owner',
      spender: 'spender',
    });

    expect(result.success).toBeFalse();
    expect(result.error?.code).toBe('UNSUPPORTED_CHAIN');
  });

  test('returns fail result for token balance on unsupported chain', async () => {
    const result = await daoTokenBalanceView({
      chainId: 'UNKNOWN' as any,
      symbol: 'AIBOUNTY',
      owner: 'owner',
    });

    expect(result.success).toBeFalse();
    expect(result.error?.code).toBe('UNSUPPORTED_CHAIN');
  });

  test('validates required dao input fields', async () => {
    const missingComment = await discussionComment({ chainId: 'tDVV', comment: '' });
    const emptyFiles = await daoUploadFiles({ chainId: 'tDVV', daoId: 'dao-1', files: [], mode: 'simulate' });

    expect(missingComment.success).toBeFalse();
    expect(missingComment.error?.code).toBe('INVALID_INPUT');
    expect(emptyFiles.success).toBeFalse();
    expect(emptyFiles.error?.code).toBe('INVALID_INPUT');
  });
});
