import { describe, expect, test } from 'bun:test';
import { daoCreate, daoProposalCreate, daoVote } from '../../src/domains/dao.js';

describe('dao simulate', () => {
  test('create simulate', async () => {
    const res = await daoCreate({
      chainId: 'tDVV',
      args: { metadata: { name: 'Demo DAO' } },
      mode: 'simulate',
    });
    expect(res.success).toBeTrue();
    expect((res.data as any).methodName).toBe('CreateDAO');
  });

  test('proposal simulate', async () => {
    const res = await daoProposalCreate({
      chainId: 'tDVV',
      methodName: 'CreateProposal',
      args: { proposalBasicInfo: { proposalTitle: 't' } },
      mode: 'simulate',
    });
    expect(res.success).toBeTrue();
  });

  test('vote simulate', async () => {
    const res = await daoVote({
      chainId: 'tDVV',
      args: { proposalId: 'abc', voteOption: 1, voteAmount: 0 },
      mode: 'simulate',
    });
    expect(res.success).toBeTrue();
    expect((res.data as any).args).toEqual({
      votingItemId: 'abc',
      voteOption: 1,
      voteAmount: 0,
    });
  });
});
