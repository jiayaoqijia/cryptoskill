import { describe, expect, test } from 'bun:test';
import { networkOrganizationCreate, networkProposalCreate } from '../../src/domains/network.js';

describe('network domain integration', () => {
  test('organization threshold validation', async () => {
    const result = await networkOrganizationCreate({
      chainId: 'AELF',
      proposalType: 'Parliament',
      args: {
        proposalReleaseThreshold: {
          minimalApprovalThreshold: 6000,
          maximalRejectionThreshold: 5000,
          maximalAbstentionThreshold: 100,
          minimalVoteThreshold: 7000,
        },
      },
      mode: 'simulate',
    });

    expect(result.success).toBeFalse();
  });

  test('proposal create simulate', async () => {
    const result = await networkProposalCreate({
      chainId: 'AELF',
      proposalType: 'Parliament',
      args: {
        title: 'test',
        description: 'desc',
        contractMethodName: 'Dummy',
        toAddress: '2JT8xzjR5zJ8xnBvdgBZdSjfbokFSbF5hDdpUCbXeWaJfPDmsK',
        params: '',
        expiredTime: { seconds: 0, nanos: 0 },
        organizationAddress: '2JT8xzjR5zJ8xnBvdgBZdSjfbokFSbF5hDdpUCbXeWaJfPDmsK',
      },
      mode: 'simulate',
    });

    expect(result.success).toBeTrue();
  });
});
