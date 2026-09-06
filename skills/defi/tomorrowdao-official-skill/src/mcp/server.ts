#!/usr/bin/env bun
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';
import packageJson from '../../package.json';
import * as dao from '../domains/dao.js';
import * as token from '../domains/token.js';
import * as network from '../domains/network.js';
import * as bp from '../domains/bp.js';
import * as resource from '../domains/resource.js';
import { runTool } from './runtime.js';
import {
  addressSchema,
  bpChangeVoteArgsSchema,
  bpVoteArgsSchema,
  bpWithdrawArgsSchema,
  chainIdSchema,
  contractArgsSchema,
  daoVoteArgsSchema,
  daoWithdrawArgsSchema,
  daoFileSchema,
  maxResultCountSchema,
  modeSchema,
  networkProposalActionSchema,
  networkProposalTypeSchema,
  skipCountSchema,
  tokenApproveArgsSchema,
} from './schemas.js';

const server = new McpServer({
  name: 'tomorrowdao-agent-skills',
  version: packageJson.version,
});

const READ_ONLY_ANNOTATIONS = {
  readOnlyHint: true,
  read_only_hint: true,
} as const;

const NETWORK_WRITE_ANNOTATIONS = {
  destructiveHint: true,
  destructive_hint: true,
  openWorldHint: true,
  side_effects_hint: true,
} as const;

const READ_ONLY_TOOLS = new Set([
  'tomorrowdao_discussion_list',
  'tomorrowdao_dao_proposal_my_info',
  'tomorrowdao_dao_token_allowance_view',
  'tomorrowdao_dao_token_balance_view',
  'tomorrowdao_token_allowance_view',
  'tomorrowdao_token_balance_view',
  'tomorrowdao_network_proposals_list',
  'tomorrowdao_network_proposal_get',
  'tomorrowdao_network_org_list',
  'tomorrowdao_network_contract_flow_status',
  'tomorrowdao_bp_votes_list',
  'tomorrowdao_bp_team_desc_get',
  'tomorrowdao_bp_team_desc_list',
  'tomorrowdao_resource_realtime_records',
  'tomorrowdao_resource_turnover',
  'tomorrowdao_resource_records',
]);

const signerInputSchema = z
  .object({
    signerMode: z.enum(['auto', 'explicit', 'context', 'env', 'daemon']).optional(),
    walletType: z.enum(['EOA', 'CA']).optional(),
    address: z.string().optional(),
    password: z.string().optional(),
    privateKey: z.string().optional(),
    caHash: z.string().optional(),
    caAddress: z.string().optional(),
    network: z.enum(['mainnet', 'testnet']).optional(),
  })
  .optional()
  .describe(
    'Optional signer input. signerMode=auto resolves explicit -> active context -> env. daemon is reserved. Send mode rejects direct contract send when the resolved signer is CA-backed; use an explicit CA forward transport instead.',
  );

function registerTool(
  name: string,
  description: string,
  inputSchema: Record<string, z.ZodTypeAny>,
  handler: (payload: any) => Promise<unknown>,
): void {
  const normalizedInputSchema =
    Object.prototype.hasOwnProperty.call(inputSchema, 'mode')
      ? {
          ...inputSchema,
          signer: signerInputSchema,
          signerContext: signerInputSchema,
        }
      : inputSchema;

  server.registerTool(
    name,
    {
      description,
      inputSchema: normalizedInputSchema,
      annotations: READ_ONLY_TOOLS.has(name)
        ? READ_ONLY_ANNOTATIONS
        : NETWORK_WRITE_ANNOTATIONS,
    },
    async (input) => runTool(name, input, handler),
  );
}

registerTool(
  'tomorrowdao_dao_create',
  'Create DAO on chain',
  {
    chainId: chainIdSchema,
    args: contractArgsSchema('{"metadata":{"name":"Demo DAO"}}'),
    mode: modeSchema,
  },
  dao.daoCreate,
);

registerTool(
  'tomorrowdao_dao_update_metadata',
  'Update DAO metadata',
  {
    chainId: chainIdSchema,
    daoId: z.string().min(1).describe('DAO id.'),
    metadata: z.record(z.any()).describe('DAO metadata patch object.'),
    mode: modeSchema,
  },
  dao.daoUpdateMetadata,
);

registerTool(
  'tomorrowdao_dao_upload_files',
  'Upload DAO files',
  {
    chainId: chainIdSchema,
    daoId: z.string().min(1).describe('DAO id.'),
    files: z.array(daoFileSchema).min(1).describe('File list to upload.'),
    mode: modeSchema,
  },
  dao.daoUploadFiles,
);

registerTool(
  'tomorrowdao_dao_remove_files',
  'Remove DAO files by CID',
  {
    chainId: chainIdSchema,
    daoId: z.string().min(1).describe('DAO id.'),
    fileCids: z.array(z.string().min(1)).min(1).describe('File CIDs to remove.'),
    mode: modeSchema,
  },
  dao.daoRemoveFiles,
);

registerTool(
  'tomorrowdao_dao_proposal_create',
  'Create DAO proposal',
  {
    chainId: chainIdSchema,
    methodName: z
      .enum(['CreateTransferProposal', 'CreateProposal', 'CreateVetoProposal'])
      .describe('DAO proposal contract method.'),
    args: contractArgsSchema('{"proposalBasicInfo":{"proposalTitle":"My proposal"}}'),
    mode: modeSchema,
  },
  dao.daoProposalCreate,
);

registerTool(
  'tomorrowdao_dao_vote',
  'Vote in DAO proposal by proposalId or votingItemId',
  {
    chainId: chainIdSchema,
    args: daoVoteArgsSchema,
    mode: modeSchema,
  },
  dao.daoVote,
);

registerTool(
  'tomorrowdao_dao_withdraw',
  'Withdraw DAO vote by daoId + withdrawAmount + proposalId(s)/votingItemId(s)',
  {
    chainId: chainIdSchema,
    args: daoWithdrawArgsSchema,
    mode: modeSchema,
  },
  dao.daoWithdraw,
);

registerTool(
  'tomorrowdao_dao_execute',
  'Execute DAO proposal',
  {
    chainId: chainIdSchema,
    proposalId: z.string().min(1).describe('DAO proposal id.'),
    mode: modeSchema,
  },
  dao.daoExecute,
);

registerTool(
  'tomorrowdao_discussion_list',
  'Get discussion comments list',
  {
    chainId: chainIdSchema,
    proposalId: z.string().optional().describe('Filter by proposal id.'),
    alias: z.string().optional().describe('Filter by alias.'),
    skipCount: skipCountSchema,
    maxResultCount: maxResultCountSchema,
  },
  dao.discussionList,
);

registerTool(
  'tomorrowdao_discussion_comment',
  'Create discussion comment (auth required)',
  {
    chainId: chainIdSchema,
    comment: z.string().min(1).describe('Comment content.'),
    proposalId: z.string().optional().describe('Related proposal id.'),
    alias: z.string().optional().describe('Alias for discussion board.'),
    parentId: z.string().optional().describe('Parent comment id for reply.'),
  },
  dao.discussionComment,
);

registerTool(
  'tomorrowdao_dao_proposal_my_info',
  'Get my DAO proposal info (auth required)',
  {
    chainId: chainIdSchema,
    proposalId: z.string().min(1).describe('Proposal id.'),
    address: addressSchema,
    daoId: z.string().min(1).describe('DAO id.'),
  },
  dao.daoProposalMyInfo,
);

registerTool(
  'tomorrowdao_token_allowance_view',
  'Get token allowance',
  {
    chainId: chainIdSchema,
    symbol: z.string().min(1).describe('Token symbol, e.g. ELF.'),
    owner: addressSchema.describe('Owner address.'),
    spender: addressSchema.describe('Spender address.'),
  },
  token.tokenAllowanceView,
);

registerTool(
  'tomorrowdao_token_approve',
  'Approve token allowance on the default token contract',
  {
    chainId: chainIdSchema,
    args: tokenApproveArgsSchema,
    mode: modeSchema,
  },
  token.tokenApprove,
);

registerTool(
  'tomorrowdao_token_balance_view',
  'Get token balance',
  {
    chainId: chainIdSchema,
    symbol: z.string().min(1).describe('Token symbol, e.g. ELF.'),
    owner: addressSchema.describe('Owner address.'),
  },
  token.tokenBalanceView,
);

registerTool(
  'tomorrowdao_dao_token_allowance_view',
  'Get token allowance for DAO vote token (compat alias of generic token allowance view)',
  {
    chainId: chainIdSchema,
    symbol: z.string().min(1).describe('Token symbol, e.g. ELF.'),
    owner: addressSchema.describe('Owner address.'),
    spender: addressSchema.describe('Spender address.'),
  },
  dao.daoTokenAllowanceView,
);

registerTool(
  'tomorrowdao_dao_token_balance_view',
  'Get token balance for DAO vote token (compat alias of generic token balance view)',
  {
    chainId: chainIdSchema,
    symbol: z.string().min(1).describe('Token symbol, e.g. ELF.'),
    owner: addressSchema.describe('Owner address.'),
  },
  dao.daoTokenBalanceView,
);

registerTool(
  'tomorrowdao_network_proposals_list',
  'List network governance proposals',
  {
    chainId: chainIdSchema,
    skipCount: skipCountSchema,
    maxResultCount: maxResultCountSchema,
    proposalType: z.number().optional().describe('Optional proposal type filter.'),
  },
  network.networkProposalsList,
);

registerTool(
  'tomorrowdao_network_proposal_get',
  'Get single network proposal detail',
  {
    chainId: chainIdSchema,
    proposalId: z.string().min(1).describe('Proposal id.'),
  },
  network.networkProposalGet,
);

registerTool(
  'tomorrowdao_network_proposal_create',
  'Create network proposal',
  {
    chainId: chainIdSchema,
    proposalType: z
      .enum(['Parliament', 'Association', 'Referendum'])
      .describe('Proposal contract type.'),
    args: contractArgsSchema('{"title":"...","description":"...","contractMethodName":"..."}'),
    mode: modeSchema,
  },
  network.networkProposalCreate,
);

registerTool(
  'tomorrowdao_network_proposal_vote',
  'Vote/release network proposal',
  {
    chainId: chainIdSchema,
    proposalType: networkProposalTypeSchema,
    proposalId: z.string().min(1).describe('Proposal id.'),
    action: networkProposalActionSchema,
    mode: modeSchema,
  },
  network.networkProposalVote,
);

registerTool(
  'tomorrowdao_network_proposal_release',
  'Release network proposal',
  {
    chainId: chainIdSchema,
    proposalType: networkProposalTypeSchema,
    proposalId: z.string().min(1).describe('Proposal id.'),
    mode: modeSchema,
  },
  network.networkProposalRelease,
);

registerTool(
  'tomorrowdao_network_org_create',
  'Create organization',
  {
    chainId: chainIdSchema,
    proposalType: z
      .enum(['Parliament', 'Association', 'Referendum'])
      .describe('Organization governance type.'),
    args: contractArgsSchema('{"proposalReleaseThreshold":{"minimalApprovalThreshold":4000,...}}'),
    mode: modeSchema,
  },
  network.networkOrganizationCreate,
);

registerTool(
  'tomorrowdao_network_org_list',
  'List organizations',
  {
    chainId: chainIdSchema,
    proposalType: z.number().optional().describe('Optional organization type filter.'),
    skipCount: skipCountSchema,
    maxResultCount: maxResultCountSchema,
  },
  network.networkOrganizationsList,
);

registerTool(
  'tomorrowdao_network_contract_name_check',
  'Check network contract name availability',
  {
    chainId: chainIdSchema,
    contractName: z.string().min(1).describe('Contract name to check.'),
  },
  network.networkContractNameCheck,
);

registerTool(
  'tomorrowdao_network_contract_name_add',
  'Add network contract name (auth required)',
  {
    chainId: chainIdSchema,
    operateChainId: z.enum(['AELF', 'tDVV', 'tDVW']).describe('Operating chain id.'),
    contractName: z.string().min(1),
    txId: z.string().min(1).describe('Deployment tx id.'),
    action: z.number().describe('Action code from backend API.'),
    address: addressSchema,
    proposalId: z.string().optional(),
    createAt: z.string().optional(),
  },
  network.networkContractNameAdd,
);

registerTool(
  'tomorrowdao_network_contract_name_update',
  'Update network contract name (auth required)',
  {
    chainId: chainIdSchema,
    operateChainId: z.enum(['AELF', 'tDVV', 'tDVW']).optional(),
    contractName: z.string().min(1),
    address: addressSchema,
    contractAddress: z.string().min(1).describe('Target contract address.'),
    caHash: z.string().optional(),
  },
  network.networkContractNameUpdate,
);

registerTool(
  'tomorrowdao_network_contract_flow_start',
  'Start network contract proposal flow',
  {
    chainId: chainIdSchema,
    action: z
      .enum(['ProposeNewContract', 'ProposeUpdateContract', 'DeployUserSmartContract', 'UpdateUserSmartContract'])
      .describe('Genesis contract method to start flow.'),
    args: contractArgsSchema('{"category":0,"code":"base64/hex code"}'),
    mode: modeSchema,
  },
  network.networkContractFlowStart,
);

registerTool(
  'tomorrowdao_network_contract_flow_release',
  'Release approved/code-checked contract proposal',
  {
    chainId: chainIdSchema,
    methodName: z
      .enum(['ReleaseApprovedContract', 'ReleaseCodeCheckedContract'])
      .describe('Release method on genesis contract.'),
    proposalId: z.string().min(1),
    proposedContractInputHash: z.string().min(1),
    mode: modeSchema,
  },
  network.networkContractFlowRelease,
);

registerTool(
  'tomorrowdao_network_contract_flow_status',
  'Query contract proposal flow status',
  {
    chainId: chainIdSchema,
    proposalId: z.string().optional(),
    codeHash: z.string().optional(),
  },
  network.networkContractFlowStatus,
);

registerTool(
  'tomorrowdao_bp_apply',
  'Apply to become BP candidate',
  {
    chainId: chainIdSchema,
    args: contractArgsSchema('{"value":10000000000}'),
    mode: modeSchema,
  },
  bp.bpApply,
);

registerTool(
  'tomorrowdao_bp_quit',
  'Quit BP election',
  {
    chainId: chainIdSchema,
    args: contractArgsSchema('{"value":true}'),
    mode: modeSchema,
  },
  bp.bpQuit,
);

registerTool(
  'tomorrowdao_bp_vote',
  'Vote for BP candidate',
  {
    chainId: chainIdSchema,
    args: bpVoteArgsSchema,
    mode: modeSchema,
  },
  bp.bpVote,
);

registerTool(
  'tomorrowdao_bp_withdraw',
  'Withdraw BP votes',
  {
    chainId: chainIdSchema,
    args: bpWithdrawArgsSchema,
    mode: modeSchema,
  },
  bp.bpWithdraw,
);

registerTool(
  'tomorrowdao_bp_change_vote',
  'Change BP voting option',
  {
    chainId: chainIdSchema,
    args: bpChangeVoteArgsSchema,
    mode: modeSchema,
  },
  bp.bpChangeVote,
);

registerTool(
  'tomorrowdao_bp_claim_profits',
  'Claim BP profits',
  {
    chainId: chainIdSchema,
    args: contractArgsSchema('{"schemeId":"..."}'),
    mode: modeSchema,
  },
  bp.bpClaimProfits,
);

registerTool(
  'tomorrowdao_bp_votes_list',
  'List BP votes',
  {
    chainId: chainIdSchema,
    skipCount: skipCountSchema,
    maxResultCount: maxResultCountSchema,
  },
  bp.bpVotesList,
);

registerTool(
  'tomorrowdao_bp_team_desc_get',
  'Get BP team description by public key',
  {
    chainId: chainIdSchema,
    publicKey: z.string().min(1).describe('BP node public key.'),
  },
  bp.bpTeamDescGet,
);

registerTool(
  'tomorrowdao_bp_team_desc_list',
  'List all BP team descriptions',
  {
    chainId: chainIdSchema,
  },
  bp.bpTeamDescList,
);

registerTool(
  'tomorrowdao_bp_team_desc_add',
  'Add BP team description (auth required)',
  {
    chainId: chainIdSchema,
    publicKey: z.string().min(1),
    address: addressSchema,
    name: z.string().min(1),
    avatar: z.string().optional(),
    intro: z.string().optional(),
    txId: z.string().optional(),
    isActive: z.boolean().optional(),
    socials: z.array(z.string()).optional(),
    officialWebsite: z.string().optional(),
    location: z.string().optional(),
    mail: z.string().optional(),
    updateTime: z.string().optional(),
  },
  bp.bpTeamDescAdd,
);

registerTool(
  'tomorrowdao_bp_vote_reclaim',
  'Update BP vote reclaim status (auth required)',
  {
    chainId: chainIdSchema,
    voteId: z.string().min(1),
    proposalId: z.string().optional(),
  },
  bp.bpVoteReclaim,
);

registerTool(
  'tomorrowdao_resource_buy',
  'Buy resource token',
  {
    chainId: chainIdSchema,
    symbol: z.string().min(1),
    amount: z.number().positive().describe('Trade amount in token minimal unit.'),
    mode: modeSchema,
  },
  resource.resourceBuy,
);

registerTool(
  'tomorrowdao_resource_sell',
  'Sell resource token',
  {
    chainId: chainIdSchema,
    symbol: z.string().min(1),
    amount: z.number().positive().describe('Trade amount in token minimal unit.'),
    mode: modeSchema,
  },
  resource.resourceSell,
);

registerTool(
  'tomorrowdao_resource_realtime_records',
  'Get resource realtime records',
  {
    chainId: chainIdSchema,
    skipCount: skipCountSchema,
    maxResultCount: maxResultCountSchema,
  },
  resource.resourceRealtimeRecords,
);

registerTool(
  'tomorrowdao_resource_turnover',
  'Get resource turnover',
  {
    chainId: chainIdSchema,
    symbol: z.string().optional(),
  },
  resource.resourceTurnover,
);

registerTool(
  'tomorrowdao_resource_records',
  'Get resource trading records',
  {
    chainId: chainIdSchema,
    skipCount: skipCountSchema,
    maxResultCount: maxResultCountSchema,
    symbol: z.string().optional(),
  },
  resource.resourceRecords,
);

const transport = new StdioServerTransport();
await server.connect(transport);
