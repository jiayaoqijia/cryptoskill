import { describe, expect, test } from 'bun:test';
import { bpApply } from '../../src/domains/bp.js';
import { daoCreate, daoVote, daoWithdraw } from '../../src/domains/dao.js';
import { networkProposalCreate } from '../../src/domains/network.js';
import { resourceBuy } from '../../src/domains/resource.js';

describe('e2e simulate smoke', () => {
  test('dao create simulate', async () => {
    const res = await daoCreate({
      chainId: 'tDVV',
      args: { metadata: { name: 'simulate dao' } },
      mode: 'simulate',
    });

    expect(res.success).toBeTrue();
    expect((res.data as any).methodName).toBe('CreateDAO');
  });

  test('network proposal simulate', async () => {
    const res = await networkProposalCreate({
      chainId: 'AELF',
      proposalType: 'Parliament',
      args: {
        title: 'simulate',
        description: 'simulate',
        contractMethodName: 'Dummy',
        toAddress: '2JT8xzjR5zJ8xnBvdgBZdSjfbokFSbF5hDdpUCbXeWaJfPDmsK',
        params: '',
        expiredTime: { seconds: 0, nanos: 0 },
        organizationAddress: '2JT8xzjR5zJ8xnBvdgBZdSjfbokFSbF5hDdpUCbXeWaJfPDmsK',
      },
      mode: 'simulate',
    });

    expect(res.success).toBeTrue();
  });

  test('dao vote simulate', async () => {
    const res = await daoVote({
      chainId: 'tDVV',
      args: {
        proposalId: 'simulate-proposal',
        voteOption: 0,
        voteAmount: 100000000,
      },
      mode: 'simulate',
    });

    expect(res.success).toBeTrue();
    expect((res.data as any).args).toEqual({
      votingItemId: 'simulate-proposal',
      voteOption: 0,
      voteAmount: 100000000,
    });
  });

  test('dao withdraw simulate', async () => {
    const res = await daoWithdraw({
      chainId: 'tDVV',
      args: {
        daoId: 'simulate-dao',
        withdrawAmount: 100000000,
        proposalIds: ['simulate-proposal'],
      },
      mode: 'simulate',
    });

    expect(res.success).toBeTrue();
    expect((res.data as any).args).toEqual({
      daoId: 'simulate-dao',
      withdrawAmount: 100000000,
      votingItemIdList: {
        value: ['simulate-proposal'],
      },
    });
  });

  test('bp apply simulate', async () => {
    const res = await bpApply({
      chainId: 'AELF',
      args: { value: 1 },
      mode: 'simulate',
    });

    expect(res.success).toBeTrue();
  });

  test('resource buy simulate', async () => {
    const res = await resourceBuy({
      chainId: 'AELF',
      symbol: 'CPU',
      amount: 1,
      mode: 'simulate',
    });

    expect(res.success).toBeTrue();
  });
});
