import { z } from 'zod';

export const chainIdSchema = z
  .enum(['AELF', 'tDVV', 'tDVW'])
  .optional()
  .describe('Chain id. Use AELF for network governance/BP/resource, tDVV/tDVW for DAO operations.');

export const modeSchema = z
  .enum(['simulate', 'send'])
  .default('simulate')
  .describe('Execution mode. simulate: dry-run without broadcast; send: broadcast transaction.');

export const skipCountSchema = z.number().int().min(0).optional().describe('Pagination offset, default 0.');
export const maxResultCountSchema = z.number().int().min(1).max(200).optional().describe('Pagination size, default 20.');

export const addressSchema = z.string().min(1).describe('AElf address string.');

export function contractArgsSchema(example: string): z.ZodTypeAny {
  return z
    .record(z.any())
    .describe(`Contract method args JSON object. Example: ${example}`);
}

export const daoFileSchema = z.object({
  cid: z.string().min(1).describe('IPFS/OSS content id.'),
  name: z.string().min(1).describe('Display name of file.'),
  url: z.string().min(1).describe('Public download URL.'),
});

export const networkProposalTypeSchema = z
  .enum(['Parliament', 'Association', 'Referendum'])
  .describe('Network governance proposal contract type.');

export const networkProposalActionSchema = z
  .enum(['Approve', 'Reject', 'Abstain', 'Release'])
  .describe('Proposal action: Approve/Reject/Abstain/Release.');

const daoIdLikeSchema = z.string().min(1);
const daoIdListSchema = z.array(daoIdLikeSchema).min(1);

export const daoVoteArgsSchema = z
  .object({
    proposalId: z.string().min(1).optional().describe('DAO proposal id alias for votingItemId.'),
    votingItemId: z.string().min(1).optional().describe('DAO voting item id (chain hash).'),
    voteOption: z.number().int().describe('Vote option enum value from DAO vote contract.'),
    voteAmount: z.number().int().nonnegative().describe('Vote amount in minimal token unit.'),
    memo: z.string().optional().describe('Optional vote memo passed to the vote contract.'),
  })
  .passthrough()
  .superRefine((value, ctx) => {
    if (!value.proposalId && !value.votingItemId) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: 'proposalId or votingItemId is required',
      });
    }
    if (value.proposalId && value.votingItemId && value.proposalId !== value.votingItemId) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: 'proposalId and votingItemId must match when both are provided',
      });
    }
  })
  .describe('DAO Vote contract args.');

export const tokenApproveArgsSchema = z
  .object({
    spender: z.string().min(1).describe('Approved spender address.'),
    symbol: z.string().min(1).describe('Token symbol.'),
    amount: z.number().int().nonnegative().describe('Approve amount in minimal token unit.'),
  })
  .passthrough()
  .describe('Token Approve contract args.');

export const daoWithdrawArgsSchema = z
  .object({
    daoId: z.string().min(1).describe('DAO id to withdraw vote from.'),
    withdrawAmount: z.number().int().positive().describe('Withdraw amount in minimal token unit.'),
    proposalId: daoIdLikeSchema.optional().describe('Single DAO proposal id alias for votingItemId.'),
    proposalIds: daoIdListSchema.optional().describe('DAO proposal id aliases for votingItemIds.'),
    votingItemId: daoIdLikeSchema.optional().describe('Single DAO voting item id (chain hash).'),
    votingItemIds: daoIdListSchema.optional().describe('DAO voting item ids (chain hashes).'),
    voteRecordId: z
      .string()
      .min(1)
      .optional()
      .describe('Deprecated. Use daoId + withdrawAmount + proposalId/proposalIds or votingItemId/votingItemIds.'),
  })
  .passthrough()
  .superRefine((value, ctx) => {
    if (value.voteRecordId) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message:
          'voteRecordId is no longer supported; use daoId + withdrawAmount + proposalId/proposalIds or votingItemId/votingItemIds',
      });
    }

    const targetCount =
      Number(Boolean(value.proposalId)) +
      Number(Boolean(value.votingItemId)) +
      Number(Boolean(value.proposalIds?.length)) +
      Number(Boolean(value.votingItemIds?.length));
    if (targetCount === 0) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: 'proposalId/proposalIds or votingItemId/votingItemIds is required',
      });
    }
  })
  .describe('DAO Withdraw contract args.');

export const bpVoteArgsSchema = z
  .object({
    candidatePubkey: z.string().min(1).describe('BP candidate public key.'),
    amount: z.number().positive().describe('Voting amount in minimal ELF unit.'),
  })
  .passthrough()
  .describe('BP Vote contract args.');

export const bpChangeVoteArgsSchema = z
  .object({
    voteId: z.string().min(1).describe('Existing vote id to update.'),
    candidatePubkey: z.string().min(1).describe('New candidate public key.'),
  })
  .passthrough()
  .describe('BP ChangeVotingOption contract args.');

export const bpWithdrawArgsSchema = z
  .object({
    voteId: z.string().min(1).describe('Vote id to withdraw.'),
  })
  .passthrough()
  .describe('BP Withdraw contract args.');
