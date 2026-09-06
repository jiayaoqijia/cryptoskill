import { CONTRACTS, getConfig } from '../core/config.js';
import { callSend } from '../core/chain-client.js';
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

type SignerAware = {
  signer?: SignerContextInput;
  signerContext?: SignerContextInput;
};

function bpChain(chainId?: ChainId): ChainId {
  return chainId || getConfig().defaultNetworkChain;
}

function ensureAelf(chainId: ChainId): ChainId {
  if (chainId !== 'AELF') throw new SkillError('UNSUPPORTED_CHAIN', `bp domain only supports AELF, got ${chainId}`);
  return chainId;
}

function sendOptions(input: SignerAware & { mode?: ExecutionMode }) {
  return {
    mode: input.mode || 'simulate',
    signer: input.signer,
    signerContext: input.signerContext,
  };
}

export async function bpApply(input: {
  chainId?: ChainId;
  args: Record<string, unknown>;
  mode?: ExecutionMode;
} & SignerAware): Promise<ToolResult<unknown>> {
  try {
    requireField(input.args, 'args');
    const chainId = ensureAelf(bpChain(input.chainId));
    const result = await callSend(
      {
        chainId,
        contractAddress: CONTRACTS.network.AELF.election,
        methodName: 'AnnounceElection',
        args: input.args,
      },
      sendOptions(input),
    );
    return ok(result.result, { tx: result.tx });
  } catch (err) {
    return fail(err);
  }
}

export async function bpQuit(input: {
  chainId?: ChainId;
  args: Record<string, unknown>;
  mode?: ExecutionMode;
} & SignerAware): Promise<ToolResult<unknown>> {
  try {
    requireField(input.args, 'args');
    const chainId = ensureAelf(bpChain(input.chainId));
    const result = await callSend(
      {
        chainId,
        contractAddress: CONTRACTS.network.AELF.election,
        methodName: 'QuitElection',
        args: input.args,
      },
      sendOptions(input),
    );
    return ok(result.result, { tx: result.tx });
  } catch (err) {
    return fail(err);
  }
}

export async function bpVote(input: {
  chainId?: ChainId;
  args: Record<string, unknown>;
  mode?: ExecutionMode;
} & SignerAware): Promise<ToolResult<unknown>> {
  try {
    requireField(input.args, 'args');
    const chainId = ensureAelf(bpChain(input.chainId));
    const result = await callSend(
      {
        chainId,
        contractAddress: CONTRACTS.network.AELF.election,
        methodName: 'Vote',
        args: input.args,
      },
      sendOptions(input),
    );
    return ok(result.result, { tx: result.tx });
  } catch (err) {
    return fail(err);
  }
}

export async function bpWithdraw(input: {
  chainId?: ChainId;
  args: unknown;
  mode?: ExecutionMode;
} & SignerAware): Promise<ToolResult<unknown>> {
  try {
    requireField(input.args, 'args');
    const chainId = ensureAelf(bpChain(input.chainId));
    const result = await callSend(
      {
        chainId,
        contractAddress: CONTRACTS.network.AELF.election,
        methodName: 'Withdraw',
        args: input.args,
      },
      sendOptions(input),
    );
    return ok(result.result, { tx: result.tx });
  } catch (err) {
    return fail(err);
  }
}

export async function bpChangeVote(input: {
  chainId?: ChainId;
  args: Record<string, unknown>;
  mode?: ExecutionMode;
} & SignerAware): Promise<ToolResult<unknown>> {
  try {
    requireField(input.args, 'args');
    const chainId = ensureAelf(bpChain(input.chainId));
    const result = await callSend(
      {
        chainId,
        contractAddress: CONTRACTS.network.AELF.election,
        methodName: 'ChangeVotingOption',
        args: input.args,
      },
      sendOptions(input),
    );
    return ok(result.result, { tx: result.tx });
  } catch (err) {
    return fail(err);
  }
}

export async function bpClaimProfits(input: {
  chainId?: ChainId;
  args: Record<string, unknown>;
  mode?: ExecutionMode;
} & SignerAware): Promise<ToolResult<unknown>> {
  try {
    requireField(input.args, 'args');
    const chainId = ensureAelf(bpChain(input.chainId));
    const result = await callSend(
      {
        chainId,
        contractAddress: CONTRACTS.network.AELF.profit,
        methodName: 'ClaimProfits',
        args: input.args,
      },
      sendOptions(input),
    );
    return ok(result.result, { tx: result.tx });
  } catch (err) {
    return fail(err);
  }
}

export async function bpVotesList(input: {
  chainId?: ChainId;
  skipCount?: number;
  maxResultCount?: number;
}): Promise<ToolResult<PagedResponse>> {
  try {
    const data = await apiGet<PagedResponse>('/networkdao/votes', {
      chainId: bpChain(input.chainId),
      skipCount: input.skipCount || 0,
      maxResultCount: input.maxResultCount || 20,
    });
    return ok(data);
  } catch (err) {
    return fail(err);
  }
}

export async function bpTeamDescGet(input: {
  chainId?: ChainId;
  publicKey: string;
}): Promise<ToolResult<JsonObject>> {
  try {
    requireField(input.publicKey, 'publicKey');
    const data = await apiGet<JsonObject>('/networkdao/vote/getTeamDesc', {
      chainId: bpChain(input.chainId),
      publicKey: input.publicKey,
    });
    return ok(data);
  } catch (err) {
    return fail(err);
  }
}

export async function bpTeamDescList(input: { chainId?: ChainId }): Promise<ToolResult<PagedResponse>> {
  try {
    const data = await apiGet<PagedResponse>('/networkdao/vote/getAllTeamDesc', {
      chainId: bpChain(input.chainId),
    });
    return ok(data);
  } catch (err) {
    return fail(err);
  }
}

export async function bpTeamDescAdd(input: {
  chainId?: ChainId;
  publicKey: string;
  address: string;
  name: string;
  avatar?: string;
  intro?: string;
  txId?: string;
  isActive?: boolean;
  socials?: string[];
  officialWebsite?: string;
  location?: string;
  mail?: string;
  updateTime?: string;
}): Promise<ToolResult<unknown>> {
  try {
    requireField(input.publicKey, 'publicKey');
    requireField(input.address, 'address');
    requireField(input.name, 'name');
    const data = await apiPost(
      '/networkdao/vote/addTeamDesc',
      {
        chainId: bpChain(input.chainId),
        publicKey: input.publicKey,
        address: input.address,
        name: input.name,
        avatar: input.avatar,
        intro: input.intro,
        txId: input.txId,
        isActive: input.isActive ?? true,
        socials: input.socials,
        officialWebsite: input.officialWebsite,
        location: input.location,
        mail: input.mail,
        updateTime: input.updateTime,
      },
      { auth: true },
    );
    return ok(data);
  } catch (err) {
    return fail(err);
  }
}

export async function bpVoteReclaim(input: {
  chainId?: ChainId;
  voteId: string;
  proposalId?: string;
}): Promise<ToolResult<unknown>> {
  try {
    requireField(input.voteId, 'voteId');
    const data = await apiPost(
      '/networkdao/vote/reclaim',
      {
        chainId: bpChain(input.chainId),
        voteId: input.voteId,
        proposalId: input.proposalId,
      },
      { auth: true },
    );
    return ok(data);
  } catch (err) {
    return fail(err);
  }
}
