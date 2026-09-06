import {
  CONTRACTS,
  getConfig,
  getProposalContractAddress,
  type ProposalContractType,
} from '../core/config.js';
import { callSend, callView } from '../core/chain-client.js';
import { fail, ok, requireField, SkillError } from '../core/errors.js';
import { apiGet, apiPost } from '../core/http.js';
import type {
  ChainId,
  ExecutionMode,
  JsonObject,
  PagedResponse,
  SignerContextInput,
  ToolResult,
} from '../core/types.js';

export type VoteAction = 'Approve' | 'Reject' | 'Abstain' | 'Release';

type SignerAware = {
  signer?: SignerContextInput;
  signerContext?: SignerContextInput;
};

export interface NetworkProposalCreateInput extends SignerAware {
  chainId?: ChainId;
  proposalType: ProposalContractType;
  args: Record<string, unknown>;
  mode?: ExecutionMode;
}

export interface NetworkProposalVoteInput extends SignerAware {
  chainId?: ChainId;
  proposalType: ProposalContractType;
  proposalId: string;
  action: VoteAction;
  mode?: ExecutionMode;
}

export interface NetworkOrganizationCreateInput extends SignerAware {
  chainId?: ChainId;
  proposalType: ProposalContractType;
  args: Record<string, unknown>;
  mode?: ExecutionMode;
}

export interface ContractNameAddInput {
  chainId?: ChainId;
  operateChainId: ChainId;
  contractName: string;
  txId: string;
  action: number;
  address: string;
  proposalId?: string;
  createAt?: string;
}

export interface ContractNameUpdateInput {
  chainId?: ChainId;
  operateChainId?: ChainId;
  contractName: string;
  address: string;
  contractAddress: string;
  caHash?: string;
}

export interface ContractFlowStartInput extends SignerAware {
  chainId?: ChainId;
  action:
    | 'ProposeNewContract'
    | 'ProposeUpdateContract'
    | 'DeployUserSmartContract'
    | 'UpdateUserSmartContract';
  args: Record<string, unknown>;
  mode?: ExecutionMode;
}

export interface ContractFlowReleaseInput extends SignerAware {
  chainId?: ChainId;
  methodName: 'ReleaseApprovedContract' | 'ReleaseCodeCheckedContract';
  proposalId: string;
  proposedContractInputHash: string;
  mode?: ExecutionMode;
}

function networkChain(chainId?: ChainId): ChainId {
  return chainId || getConfig().defaultNetworkChain;
}

function sendOptions(input: SignerAware & { mode?: ExecutionMode }) {
  return {
    mode: input.mode || 'simulate',
    signer: input.signer,
    signerContext: input.signerContext,
  };
}

function ensureNetworkMainChain(chainId: ChainId): ChainId {
  if (chainId !== 'AELF') {
    throw new SkillError('UNSUPPORTED_CHAIN', `network governance only supports AELF, got ${chainId}`);
  }
  return chainId;
}

function hexToByteArray(hex: string): number[] {
  const pure = hex.startsWith('0x') ? hex.slice(2) : hex;
  if (pure.length % 2 !== 0) return [];
  const bytes: number[] = [];
  for (let i = 0; i < pure.length; i += 2) {
    bytes.push(parseInt(pure.slice(i, i + 2), 16));
  }
  return bytes;
}

function validateOrganizationThresholds(input: NetworkOrganizationCreateInput): void {
  const args = input.args as any;
  const t = args?.proposalReleaseThreshold || {};

  const minApproval = Number(t.minimalApprovalThreshold || 0);
  const maxRejection = Number(t.maximalRejectionThreshold || 0);
  const maxAbstention = Number(t.maximalAbstentionThreshold || 0);
  const minVote = Number(t.minimalVoteThreshold || 0);

  if (minApproval > minVote) {
    throw new SkillError('INVALID_INPUT', 'Minimal Approval Threshold must be <= Minimal Vote Threshold');
  }

  if (input.proposalType === 'Parliament') {
    if (minApproval + maxAbstention > 10000) {
      throw new SkillError('INVALID_INPUT', 'Maximal Abstention Threshold + Minimal Approval Threshold must be <= 100%');
    }
    if (minApproval + maxRejection > 10000) {
      throw new SkillError('INVALID_INPUT', 'Maximal Rejection Threshold + Minimal Approval Threshold must be <= 100%');
    }
  }

  if (input.proposalType === 'Association') {
    const members = args?.organizationMemberList?.organizationMembers || [];
    const memberCount = Array.isArray(members) ? members.length : 0;
    if (minVote > memberCount) {
      throw new SkillError('INVALID_INPUT', 'Minimal Vote Threshold must be <= organization member count');
    }
    if (minApproval + maxAbstention > memberCount) {
      throw new SkillError('INVALID_INPUT', 'Maximal Abstention Threshold + Minimal Approval Threshold must be <= organization member count');
    }
    if (minApproval + maxRejection > memberCount) {
      throw new SkillError('INVALID_INPUT', 'Maximal Rejection Threshold + Minimal Approval Threshold must be <= organization member count');
    }
  }
}

export async function networkProposalsList(params: {
  chainId?: ChainId;
  skipCount?: number;
  maxResultCount?: number;
  proposalType?: number;
}): Promise<ToolResult<PagedResponse>> {
  try {
    const data = await apiGet<PagedResponse>('/networkdao/proposals', {
      chainId: networkChain(params.chainId),
      skipCount: params.skipCount || 0,
      maxResultCount: params.maxResultCount || 20,
      proposalType: params.proposalType,
    });
    return ok(data);
  } catch (err) {
    return fail(err);
  }
}

export async function networkProposalGet(params: {
  chainId?: ChainId;
  proposalId: string;
}): Promise<ToolResult<JsonObject>> {
  try {
    requireField(params.proposalId, 'proposalId');
    const data = await apiGet<JsonObject>('/networkdao/proposal/info', {
      chainId: networkChain(params.chainId),
      proposalId: params.proposalId,
    });
    return ok(data);
  } catch (err) {
    return fail(err);
  }
}

export async function networkProposalCreate(input: NetworkProposalCreateInput): Promise<ToolResult<unknown>> {
  try {
    requireField(input.args, 'args');
    const chainId = ensureNetworkMainChain(networkChain(input.chainId));
    const contractAddress = getProposalContractAddress(chainId, input.proposalType);
    const result = await callSend(
      {
        chainId,
        contractAddress,
        methodName: 'CreateProposal',
        args: input.args,
      },
      sendOptions(input),
    );
    return ok(result.result, { tx: result.tx });
  } catch (err) {
    return fail(err);
  }
}

export async function networkProposalVote(input: NetworkProposalVoteInput): Promise<ToolResult<unknown>> {
  try {
    requireField(input.proposalId, 'proposalId');
    requireField(input.action, 'action');
    const chainId = ensureNetworkMainChain(networkChain(input.chainId));
    const contractAddress = getProposalContractAddress(chainId, input.proposalType);
    const result = await callSend(
      {
        chainId,
        contractAddress,
        methodName: input.action,
        args: input.proposalId,
      },
      sendOptions(input),
    );
    return ok(result.result, { tx: result.tx });
  } catch (err) {
    return fail(err);
  }
}

export async function networkProposalRelease(input: Omit<NetworkProposalVoteInput, 'action'>): Promise<ToolResult<unknown>> {
  return networkProposalVote({
    ...input,
    action: 'Release',
  });
}

export async function networkOrganizationCreate(
  input: NetworkOrganizationCreateInput,
): Promise<ToolResult<unknown>> {
  try {
    requireField(input.args, 'args');
    validateOrganizationThresholds(input);
    const chainId = ensureNetworkMainChain(networkChain(input.chainId));
    const contractAddress = getProposalContractAddress(chainId, input.proposalType);
    const result = await callSend(
      {
        chainId,
        contractAddress,
        methodName: 'CreateOrganization',
        args: input.args,
      },
      sendOptions(input),
    );
    return ok(result.result, { tx: result.tx });
  } catch (err) {
    return fail(err);
  }
}

export async function networkOrganizationsList(params: {
  chainId?: ChainId;
  proposalType?: number;
  skipCount?: number;
  maxResultCount?: number;
}): Promise<ToolResult<PagedResponse>> {
  try {
    const data = await apiGet<PagedResponse>('/networkdao/org', {
      chainId: networkChain(params.chainId),
      proposalType: params.proposalType,
      skipCount: params.skipCount || 0,
      maxResultCount: params.maxResultCount || 20,
    });
    return ok(data);
  } catch (err) {
    return fail(err);
  }
}

export async function networkContractNameCheck(params: {
  chainId?: ChainId;
  contractName: string;
}): Promise<ToolResult<JsonObject>> {
  try {
    requireField(params.contractName, 'contractName');
    const data = await apiGet<JsonObject>('/networkdao/contract/check', {
      chainId: networkChain(params.chainId),
      contractName: params.contractName,
    });
    return ok(data);
  } catch (err) {
    return fail(err);
  }
}

export async function networkContractNameAdd(input: ContractNameAddInput): Promise<ToolResult<unknown>> {
  try {
    requireField(input.contractName, 'contractName');
    requireField(input.txId, 'txId');
    requireField(input.address, 'address');
    const data = await apiPost(
      '/networkdao/contract/add',
      {
        chainId: networkChain(input.chainId),
        operateChainId: input.operateChainId,
        contractName: input.contractName,
        txId: input.txId,
        action: input.action,
        address: input.address,
        proposalId: input.proposalId,
        createAt: input.createAt,
      },
      { auth: true },
    );
    return ok(data);
  } catch (err) {
    return fail(err);
  }
}

export async function networkContractNameUpdate(input: ContractNameUpdateInput): Promise<ToolResult<unknown>> {
  try {
    requireField(input.contractName, 'contractName');
    requireField(input.address, 'address');
    requireField(input.contractAddress, 'contractAddress');
    const data = await apiPost(
      '/networkdao/contract/update',
      {
        chainId: networkChain(input.chainId),
        operateChainId: input.operateChainId,
        contractName: input.contractName,
        address: input.address,
        contractAddress: input.contractAddress,
        caHash: input.caHash,
      },
      { auth: true },
    );
    return ok(data);
  } catch (err) {
    return fail(err);
  }
}

export async function networkContractFlowStart(
  input: ContractFlowStartInput,
): Promise<ToolResult<unknown>> {
  try {
    requireField(input.action, 'action');
    requireField(input.args, 'args');
    const chainId = ensureNetworkMainChain(networkChain(input.chainId));
    const result = await callSend(
      {
        chainId,
        contractAddress: CONTRACTS.network.AELF.genesis,
        methodName: input.action,
        args: input.args,
      },
      sendOptions(input),
    );
    return ok(result.result, { tx: result.tx });
  } catch (err) {
    return fail(err);
  }
}

export async function networkContractFlowRelease(
  input: ContractFlowReleaseInput,
): Promise<ToolResult<unknown>> {
  try {
    requireField(input.methodName, 'methodName');
    requireField(input.proposalId, 'proposalId');
    requireField(input.proposedContractInputHash, 'proposedContractInputHash');
    const chainId = ensureNetworkMainChain(networkChain(input.chainId));
    const result = await callSend(
      {
        chainId,
        contractAddress: CONTRACTS.network.AELF.genesis,
        methodName: input.methodName,
        args: {
          proposalId: input.proposalId,
          proposedContractInputHash: input.proposedContractInputHash,
        },
      },
      sendOptions(input),
    );
    return ok(result.result, { tx: result.tx });
  } catch (err) {
    return fail(err);
  }
}

export async function networkContractFlowStatus(params: {
  chainId?: ChainId;
  proposalId?: string;
  codeHash?: string;
}): Promise<ToolResult<JsonObject>> {
  try {
    const chainId = ensureNetworkMainChain(networkChain(params.chainId));
    const [proposalStatus, registrationStatus] = await Promise.all([
      params.proposalId
        ? callView({
            chainId,
            contractAddress: CONTRACTS.network.AELF.parliament,
            methodName: 'GetProposal',
            args: { value: hexToByteArray(params.proposalId) },
          }).catch(() => null)
        : Promise.resolve(null),
      params.codeHash
        ? callView({
            chainId,
            contractAddress: CONTRACTS.network.AELF.genesis,
            methodName: 'GetSmartContractRegistrationByCodeHash',
            args: { value: params.codeHash },
          }).catch(() => null)
        : Promise.resolve(null),
    ]);

    return ok({
      proposalStatus,
      registrationStatus,
    });
  } catch (err) {
    return fail(err);
  }
}
