import { CONTRACTS, getConfig } from '../core/config.js';
import { fail, ok, requireField, SkillError } from '../core/errors.js';
import { callSend, callView } from '../core/chain-client.js';
import { apiGet, apiPost } from '../core/http.js';
import { tokenAllowanceView, tokenBalanceView } from './token.js';
import type {
  ChainId,
  ExecutionMode,
  JsonObject,
  PagedResponse,
  SignerContextInput,
  ToolResult,
} from '../core/types.js';

type SignerAware = {
  signer?: SignerContextInput;
  signerContext?: SignerContextInput;
};

export interface DaoCreateInput extends SignerAware {
  chainId?: ChainId;
  args: Record<string, unknown>;
  mode?: ExecutionMode;
}

export interface DaoUpdateMetadataInput extends SignerAware {
  chainId?: ChainId;
  daoId: string;
  metadata: Record<string, unknown>;
  mode?: ExecutionMode;
}

export interface DaoUploadFilesInput extends SignerAware {
  chainId?: ChainId;
  daoId: string;
  files: Array<{ cid: string; name: string; url: string }>;
  mode?: ExecutionMode;
}

export interface DaoRemoveFilesInput extends SignerAware {
  chainId?: ChainId;
  daoId: string;
  fileCids: string[];
  mode?: ExecutionMode;
}

export interface DaoProposalCreateInput extends SignerAware {
  chainId?: ChainId;
  methodName: 'CreateTransferProposal' | 'CreateProposal' | 'CreateVetoProposal';
  args: Record<string, unknown>;
  mode?: ExecutionMode;
}

export interface DaoVoteInput extends SignerAware {
  chainId?: ChainId;
  args: Record<string, unknown>;
  mode?: ExecutionMode;
}

export interface DaoWithdrawInput extends SignerAware {
  chainId?: ChainId;
  args: Record<string, unknown>;
  mode?: ExecutionMode;
}

export interface DaoExecuteInput extends SignerAware {
  chainId?: ChainId;
  proposalId: string;
  mode?: ExecutionMode;
}

export interface DiscussionListInput {
  chainId?: ChainId;
  proposalId?: string;
  alias?: string;
  skipCount?: number;
  maxResultCount?: number;
}

export interface DiscussionCommentInput {
  chainId?: ChainId;
  comment: string;
  proposalId?: string;
  alias?: string;
  parentId?: string;
}

function daoChain(chainId?: ChainId): ChainId {
  return chainId || getConfig().defaultDaoChain;
}

function sendOptions(input: SignerAware & { mode?: ExecutionMode }) {
  return {
    mode: input.mode || 'simulate',
    signer: input.signer,
    signerContext: input.signerContext,
  };
}

function readOptionalStringField(args: Record<string, unknown>, name: string): string | undefined {
  const value = args[name];
  if (value === undefined || value === null) return undefined;
  if (typeof value !== 'string' || value.trim().length === 0) {
    throw new SkillError('INVALID_INPUT', `${name} must be a non-empty string`);
  }
  return value;
}

function readStringArrayField(args: Record<string, unknown>, name: string): string[] {
  const value = args[name];
  if (value === undefined || value === null) return [];
  if (!Array.isArray(value) || value.length === 0) {
    throw new SkillError('INVALID_INPUT', `${name} must be a non-empty string array`);
  }
  return value.map((item, index) => {
    if (typeof item !== 'string' || item.trim().length === 0) {
      throw new SkillError('INVALID_INPUT', `${name}[${index}] must be a non-empty string`);
    }
    return item;
  });
}

function readIntegerField(
  args: Record<string, unknown>,
  name: string,
  opts: { min?: number } = {},
): number {
  const value = args[name];
  if (typeof value !== 'number' || !Number.isInteger(value)) {
    throw new SkillError('INVALID_INPUT', `${name} must be an integer`);
  }
  if (opts.min !== undefined && value < opts.min) {
    const qualifier = opts.min === 0 ? 'non-negative' : `>= ${opts.min}`;
    throw new SkillError('INVALID_INPUT', `${name} must be ${qualifier}`);
  }
  return value;
}

function normalizeDaoVoteArgs(args: Record<string, unknown>): Record<string, unknown> {
  const proposalId = readOptionalStringField(args, 'proposalId');
  const votingItemId = readOptionalStringField(args, 'votingItemId');

  if (!proposalId && !votingItemId) {
    throw new SkillError('INVALID_INPUT', 'proposalId or votingItemId is required');
  }

  if (proposalId && votingItemId && proposalId !== votingItemId) {
    throw new SkillError('INVALID_INPUT', 'proposalId and votingItemId must match when both are provided');
  }

  const normalized: Record<string, unknown> = {
    votingItemId: votingItemId || proposalId,
    voteOption: readIntegerField(args, 'voteOption'),
    voteAmount: readIntegerField(args, 'voteAmount', { min: 0 }),
  };

  const memo = args.memo;
  if (memo !== undefined) {
    if (typeof memo !== 'string') {
      throw new SkillError('INVALID_INPUT', 'memo must be a string');
    }
    normalized.memo = memo;
  }

  return normalized;
}

function normalizeDaoWithdrawArgs(args: Record<string, unknown>): Record<string, unknown> {
  if (args.voteRecordId !== undefined) {
    throw new SkillError(
      'INVALID_INPUT',
      'voteRecordId is no longer supported; use daoId + withdrawAmount + proposalId/proposalIds or votingItemId/votingItemIds',
    );
  }

  const singularIds = [
    readOptionalStringField(args, 'proposalId'),
    readOptionalStringField(args, 'votingItemId'),
  ].filter((value): value is string => Boolean(value));

  const arrayIds = [
    ...readStringArrayField(args, 'proposalIds'),
    ...readStringArrayField(args, 'votingItemIds'),
  ];

  const votingItemIds = Array.from(new Set([...singularIds, ...arrayIds]));
  if (votingItemIds.length === 0) {
    throw new SkillError(
      'INVALID_INPUT',
      'proposalId/proposalIds or votingItemId/votingItemIds is required',
    );
  }

  return {
    daoId: requireField(readOptionalStringField(args, 'daoId'), 'daoId'),
    withdrawAmount: readIntegerField(args, 'withdrawAmount', { min: 1 }),
    votingItemIdList: {
      value: votingItemIds,
    },
  };
}

export async function daoCreate(input: DaoCreateInput): Promise<ToolResult<unknown>> {
  try {
    requireField(input.args, 'args');
    const chainId = daoChain(input.chainId);
    const result = await callSend(
      {
        chainId,
        contractAddress: CONTRACTS.dao.daoAddress,
        methodName: 'CreateDAO',
        args: input.args,
      },
      sendOptions(input),
    );
    return ok(result.result, { tx: result.tx });
  } catch (err) {
    return fail(err);
  }
}

export async function daoUpdateMetadata(input: DaoUpdateMetadataInput): Promise<ToolResult<unknown>> {
  try {
    requireField(input.daoId, 'daoId');
    requireField(input.metadata, 'metadata');
    const chainId = daoChain(input.chainId);
    const result = await callSend(
      {
        chainId,
        contractAddress: CONTRACTS.dao.daoAddress,
        methodName: 'UpdateMetadata',
        args: {
          daoId: input.daoId,
          metadata: input.metadata,
        },
      },
      sendOptions(input),
    );
    return ok(result.result, { tx: result.tx });
  } catch (err) {
    return fail(err);
  }
}

export async function daoUploadFiles(input: DaoUploadFilesInput): Promise<ToolResult<unknown>> {
  try {
    requireField(input.daoId, 'daoId');
    if (!Array.isArray(input.files) || input.files.length === 0) {
      throw new SkillError('INVALID_INPUT', 'files must be a non-empty array');
    }
    const chainId = daoChain(input.chainId);
    const result = await callSend(
      {
        chainId,
        contractAddress: CONTRACTS.dao.daoAddress,
        methodName: 'UploadFileInfos',
        args: {
          daoId: input.daoId,
          files: input.files,
        },
      },
      sendOptions(input),
    );
    return ok(result.result, { tx: result.tx });
  } catch (err) {
    return fail(err);
  }
}

export async function daoRemoveFiles(input: DaoRemoveFilesInput): Promise<ToolResult<unknown>> {
  try {
    requireField(input.daoId, 'daoId');
    if (!Array.isArray(input.fileCids) || input.fileCids.length === 0) {
      throw new SkillError('INVALID_INPUT', 'fileCids must be a non-empty array');
    }
    const chainId = daoChain(input.chainId);
    const result = await callSend(
      {
        chainId,
        contractAddress: CONTRACTS.dao.daoAddress,
        methodName: 'RemoveFileInfos',
        args: {
          daoId: input.daoId,
          fileCids: input.fileCids,
        },
      },
      sendOptions(input),
    );
    return ok(result.result, { tx: result.tx });
  } catch (err) {
    return fail(err);
  }
}

export async function daoProposalCreate(input: DaoProposalCreateInput): Promise<ToolResult<unknown>> {
  try {
    requireField(input.methodName, 'methodName');
    requireField(input.args, 'args');
    const chainId = daoChain(input.chainId);
    const result = await callSend(
      {
        chainId,
        contractAddress: CONTRACTS.dao.proposalAddress,
        methodName: input.methodName,
        args: input.args,
      },
      sendOptions(input),
    );
    return ok(result.result, { tx: result.tx });
  } catch (err) {
    return fail(err);
  }
}

export async function daoVote(input: DaoVoteInput): Promise<ToolResult<unknown>> {
  try {
    requireField(input.args, 'args');
    const args = normalizeDaoVoteArgs(input.args);
    const chainId = daoChain(input.chainId);
    const result = await callSend(
      {
        chainId,
        contractAddress: CONTRACTS.dao.voteAddress,
        methodName: 'Vote',
        args,
      },
      sendOptions(input),
    );
    return ok(result.result, { tx: result.tx });
  } catch (err) {
    return fail(err);
  }
}

export async function daoWithdraw(input: DaoWithdrawInput): Promise<ToolResult<unknown>> {
  try {
    requireField(input.args, 'args');
    const args = normalizeDaoWithdrawArgs(input.args);
    const chainId = daoChain(input.chainId);
    const result = await callSend(
      {
        chainId,
        contractAddress: CONTRACTS.dao.voteAddress,
        methodName: 'Withdraw',
        args,
      },
      sendOptions(input),
    );
    return ok(result.result, { tx: result.tx });
  } catch (err) {
    return fail(err);
  }
}

export async function daoExecute(input: DaoExecuteInput): Promise<ToolResult<unknown>> {
  try {
    requireField(input.proposalId, 'proposalId');
    const chainId = daoChain(input.chainId);
    const result = await callSend(
      {
        chainId,
        contractAddress: CONTRACTS.dao.proposalAddress,
        methodName: 'ExecuteProposal',
        args: input.proposalId,
      },
      sendOptions(input),
    );
    return ok(result.result, { tx: result.tx });
  } catch (err) {
    return fail(err);
  }
}

export async function discussionList(input: DiscussionListInput): Promise<ToolResult<PagedResponse>> {
  try {
    const data = await apiGet<PagedResponse>('/discussion/comment-list', {
      chainId: input.chainId || daoChain(),
      proposalId: input.proposalId,
      alias: input.alias,
      skipCount: input.skipCount || 0,
      maxResultCount: input.maxResultCount || 20,
    });
    return ok(data);
  } catch (err) {
    return fail(err);
  }
}

export async function discussionComment(input: DiscussionCommentInput): Promise<ToolResult<JsonObject>> {
  try {
    requireField(input.comment, 'comment');
    const data = await apiPost<Record<string, unknown>, JsonObject>('/discussion/new-comment', {
      chainId: input.chainId || daoChain(),
      proposalId: input.proposalId,
      alias: input.alias,
      comment: input.comment,
      parentId: input.parentId,
    }, { auth: true });
    return ok(data);
  } catch (err) {
    return fail(err);
  }
}

export async function daoProposalMyInfo(params: {
  chainId?: ChainId;
  proposalId: string;
  address: string;
  daoId: string;
}): Promise<ToolResult<JsonObject>> {
  try {
    requireField(params.proposalId, 'proposalId');
    requireField(params.address, 'address');
    requireField(params.daoId, 'daoId');
    const data = await apiGet<JsonObject>('/proposal/my-info', {
      chainId: params.chainId || daoChain(),
      proposalId: params.proposalId,
      address: params.address,
      daoId: params.daoId,
    }, { auth: true });
    return ok(data);
  } catch (err) {
    return fail(err);
  }
}

export const daoTokenAllowanceView = tokenAllowanceView;
export const daoTokenBalanceView = tokenBalanceView;
