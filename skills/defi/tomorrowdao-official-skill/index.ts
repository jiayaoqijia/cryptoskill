// SDK entry exports

export * from './src/core/types.js';
export { getConfig, resetConfigCache, CONTRACTS, getProposalContractAddress } from './src/core/config.js';
export { getAccessToken, clearTokenCache } from './src/core/auth.js';
export { apiGet, apiPost } from './src/core/http.js';
export { callView, callSend, packInput, clearAelfCache } from './src/core/chain-client.js';
export { resolvePrivateKeyContext } from './src/core/signer-context.js';
export { getAelfByRpc, clearAelfPool } from './src/core/aelf-pool.js';
export { waitForTxResult } from './src/core/tx-waiter.js';
export { SkillError } from './src/core/errors.js';
export { log, logError, newTraceId, setLogLevel, resetLogLevelFromEnv } from './src/core/logger.js';
export {
  readWalletContext,
  writeWalletContext,
  getActiveWalletProfile,
  setActiveWalletProfile,
} from './src/core/wallet-context.js';

// DAO
export {
  daoCreate,
  daoUpdateMetadata,
  daoUploadFiles,
  daoRemoveFiles,
  daoProposalCreate,
  daoVote,
  daoWithdraw,
  daoExecute,
  discussionList,
  discussionComment,
  daoProposalMyInfo,
  daoTokenAllowanceView,
  daoTokenBalanceView,
} from './src/domains/dao.js';

// Token helpers
export { tokenAllowanceView, tokenApprove, tokenBalanceView } from './src/domains/token.js';

// Network governance
export {
  networkProposalsList,
  networkProposalGet,
  networkProposalCreate,
  networkProposalVote,
  networkProposalRelease,
  networkOrganizationCreate,
  networkOrganizationsList,
  networkContractNameCheck,
  networkContractNameAdd,
  networkContractNameUpdate,
  networkContractFlowStart,
  networkContractFlowRelease,
  networkContractFlowStatus,
} from './src/domains/network.js';

// BP
export {
  bpApply,
  bpQuit,
  bpVote,
  bpWithdraw,
  bpChangeVote,
  bpClaimProfits,
  bpVotesList,
  bpTeamDescGet,
  bpTeamDescList,
  bpTeamDescAdd,
  bpVoteReclaim,
} from './src/domains/bp.js';

// Resource
export {
  resourceBuy,
  resourceSell,
  resourceRealtimeRecords,
  resourceTurnover,
  resourceRecords,
} from './src/domains/resource.js';
