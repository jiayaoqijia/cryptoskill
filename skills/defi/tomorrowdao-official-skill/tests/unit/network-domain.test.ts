import { afterEach, beforeEach, describe, expect, test } from 'bun:test';
import { clearTokenCache } from '../../src/core/auth.js';
import { resetConfigCache } from '../../src/core/config.js';
import {
  networkContractFlowRelease,
  networkContractFlowStart,
  networkContractFlowStatus,
  networkContractNameAdd,
  networkContractNameCheck,
  networkContractNameUpdate,
  networkOrganizationCreate,
  networkOrganizationsList,
  networkProposalCreate,
  networkProposalGet,
  networkProposalRelease,
  networkProposalVote,
  networkProposalsList,
} from '../../src/domains/network.js';
import { restoreTestEnv, resetTestEnv } from '../helpers/env.js';
import { installFetchMock, jsonResponse } from '../helpers/mock-fetch.js';

describe('network domain', () => {
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

  test('supports proposal/organization/contract-flow simulate calls', async () => {
    const proposal = await networkProposalCreate({
      chainId: 'AELF',
      proposalType: 'Parliament',
      args: {
        title: 'demo',
        description: 'desc',
        contractMethodName: 'Dummy',
        toAddress: '2JT8xzjR5zJ8xnBvdgBZdSjfbokFSbF5hDdpUCbXeWaJfPDmsK',
        params: '',
        expiredTime: { seconds: 0, nanos: 0 },
        organizationAddress: '2JT8xzjR5zJ8xnBvdgBZdSjfbokFSbF5hDdpUCbXeWaJfPDmsK',
      },
      mode: 'simulate',
    });

    const vote = await networkProposalVote({
      chainId: 'AELF',
      proposalType: 'Parliament',
      proposalId: 'p-1',
      action: 'Approve',
      mode: 'simulate',
    });

    const release = await networkProposalRelease({
      chainId: 'AELF',
      proposalType: 'Parliament',
      proposalId: 'p-1',
      mode: 'simulate',
    });

    const org = await networkOrganizationCreate({
      chainId: 'AELF',
      proposalType: 'Parliament',
      args: {
        proposalReleaseThreshold: {
          minimalApprovalThreshold: 4000,
          maximalRejectionThreshold: 2000,
          maximalAbstentionThreshold: 1000,
          minimalVoteThreshold: 5000,
        },
      },
      mode: 'simulate',
    });

    const flowStart = await networkContractFlowStart({
      chainId: 'AELF',
      action: 'ProposeNewContract',
      args: { category: 0, code: '0x00' },
      mode: 'simulate',
    });

    const flowRelease = await networkContractFlowRelease({
      chainId: 'AELF',
      methodName: 'ReleaseApprovedContract',
      proposalId: 'proposal-1',
      proposedContractInputHash: 'hash-1',
      mode: 'simulate',
    });

    const flowStatus = await networkContractFlowStatus({ chainId: 'AELF' });

    expect(proposal.success).toBeTrue();
    expect(vote.success).toBeTrue();
    expect(release.success).toBeTrue();
    expect(org.success).toBeTrue();
    expect(flowStart.success).toBeTrue();
    expect(flowRelease.success).toBeTrue();
    expect(flowStatus.success).toBeTrue();
  });

  test('supports read-only and auth APIs', async () => {
    const mocked = installFetchMock((url) => {
      if (url.endsWith('/connect/token')) {
        return jsonResponse({
          access_token: 'network-token',
          token_type: 'Bearer',
          expires_in: 120,
        });
      }
      if (url.includes('/networkdao/proposals')) {
        return jsonResponse({ code: '20000', data: { items: [] } });
      }
      if (url.includes('/networkdao/proposal/info')) {
        return jsonResponse({ code: '20000', data: { proposalId: 'p-1' } });
      }
      if (url.includes('/networkdao/org')) {
        return jsonResponse({ code: '20000', data: { items: [] } });
      }
      if (url.includes('/networkdao/contract/check')) {
        return jsonResponse({ code: '20000', data: { available: true } });
      }
      if (url.includes('/networkdao/contract/add')) {
        return jsonResponse({ code: '20000', data: { id: 'add-1' } });
      }
      if (url.includes('/networkdao/contract/update')) {
        return jsonResponse({ code: '20000', data: { id: 'update-1' } });
      }
      return jsonResponse({ code: '20000', data: {} });
    });
    restoreFetch = mocked.restore;

    const list = await networkProposalsList({ chainId: 'AELF', maxResultCount: 5 });
    const get = await networkProposalGet({ chainId: 'AELF', proposalId: 'p-1' });
    const orgList = await networkOrganizationsList({ chainId: 'AELF' });
    const check = await networkContractNameCheck({ chainId: 'AELF', contractName: 'MyContract' });
    const add = await networkContractNameAdd({
      chainId: 'AELF',
      operateChainId: 'AELF',
      contractName: 'MyContract',
      txId: 'tx-1',
      action: 1,
      address: 'address-1',
    });
    const update = await networkContractNameUpdate({
      chainId: 'AELF',
      contractName: 'MyContract',
      address: 'address-1',
      contractAddress: 'contract-address-1',
    });

    expect(list.success).toBeTrue();
    expect(get.success).toBeTrue();
    expect(orgList.success).toBeTrue();
    expect(check.success).toBeTrue();
    expect(add.success).toBeTrue();
    expect(update.success).toBeTrue();
    expect(mocked.calls.filter((x) => x.url.endsWith('/connect/token')).length).toBe(1);
  });

  test('rejects unsupported chain and invalid thresholds', async () => {
    const wrongChain = await networkProposalCreate({
      chainId: 'tDVV',
      proposalType: 'Parliament',
      args: {},
      mode: 'simulate',
    });

    const invalidMinVote = await networkOrganizationCreate({
      chainId: 'AELF',
      proposalType: 'Parliament',
      args: {
        proposalReleaseThreshold: {
          minimalApprovalThreshold: 6000,
          maximalRejectionThreshold: 1000,
          maximalAbstentionThreshold: 500,
          minimalVoteThreshold: 5000,
        },
      },
      mode: 'simulate',
    });

    const invalidParliamentRatio = await networkOrganizationCreate({
      chainId: 'AELF',
      proposalType: 'Parliament',
      args: {
        proposalReleaseThreshold: {
          minimalApprovalThreshold: 6000,
          maximalRejectionThreshold: 1000,
          maximalAbstentionThreshold: 5000,
          minimalVoteThreshold: 9000,
        },
      },
      mode: 'simulate',
    });

    const invalidAssociationMembers = await networkOrganizationCreate({
      chainId: 'AELF',
      proposalType: 'Association',
      args: {
        proposalReleaseThreshold: {
          minimalApprovalThreshold: 2,
          maximalRejectionThreshold: 1,
          maximalAbstentionThreshold: 1,
          minimalVoteThreshold: 5,
        },
        organizationMemberList: {
          organizationMembers: ['m1', 'm2', 'm3'],
        },
      },
      mode: 'simulate',
    });

    expect(wrongChain.success).toBeFalse();
    expect(wrongChain.error?.code).toBe('UNSUPPORTED_CHAIN');
    expect(invalidMinVote.success).toBeFalse();
    expect(invalidMinVote.error?.code).toBe('INVALID_INPUT');
    expect(invalidParliamentRatio.success).toBeFalse();
    expect(invalidParliamentRatio.error?.code).toBe('INVALID_INPUT');
    expect(invalidAssociationMembers.success).toBeFalse();
    expect(invalidAssociationMembers.error?.code).toBe('INVALID_INPUT');
  });

  test('validates required network inputs', async () => {
    const proposalGet = await networkProposalGet({ chainId: 'AELF', proposalId: '' });
    const nameCheck = await networkContractNameCheck({ chainId: 'AELF', contractName: '' });
    const flowRelease = await networkContractFlowRelease({
      chainId: 'AELF',
      methodName: 'ReleaseApprovedContract',
      proposalId: '',
      proposedContractInputHash: '',
      mode: 'simulate',
    });

    expect(proposalGet.success).toBeFalse();
    expect(proposalGet.error?.code).toBe('INVALID_INPUT');
    expect(nameCheck.success).toBeFalse();
    expect(nameCheck.error?.code).toBe('INVALID_INPUT');
    expect(flowRelease.success).toBeFalse();
    expect(flowRelease.error?.code).toBe('INVALID_INPUT');
  });
});
