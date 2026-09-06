#!/usr/bin/env bun
import { Command } from 'commander';
import packageJson from './package.json';
import { parseJsonInput, printResult } from './cli-helpers.js';
import * as dao from './src/domains/dao.js';
import * as token from './src/domains/token.js';
import * as network from './src/domains/network.js';
import * as bp from './src/domains/bp.js';
import * as resource from './src/domains/resource.js';

const program = new Command();
program
  .name('tomorrowdao-skill')
  .description('TomorrowDAO skill CLI (DAO / Network / BP / Resource)')
  .version(packageJson.version);

function addMode(command: Command): Command {
  return command.option('--mode <mode>', 'execution mode: simulate | send', 'simulate');
}

function addInput(command: Command): Command {
  return command.option('--input <json>', 'json input', '{}');
}

function withInput(handler: (payload: any) => Promise<unknown>) {
  return async (opts: { input?: string; mode?: string }) => {
    const input = parseJsonInput(opts.input);
    if (opts.mode) input.mode = opts.mode;
    const result = await handler(input);
    printResult(result);
  };
}

const daoCmd = program.command('dao').description('DAO domain tools');

addMode(addInput(daoCmd.command('create')).action(withInput(dao.daoCreate)));
addMode(addInput(daoCmd.command('update-metadata')).action(withInput(dao.daoUpdateMetadata)));
addMode(addInput(daoCmd.command('upload-files')).action(withInput(dao.daoUploadFiles)));
addMode(addInput(daoCmd.command('remove-files')).action(withInput(dao.daoRemoveFiles)));
addMode(addInput(daoCmd.command('proposal-create')).action(withInput(dao.daoProposalCreate)));
addMode(addInput(daoCmd.command('vote')).action(withInput(dao.daoVote)));
addMode(addInput(daoCmd.command('withdraw')).action(withInput(dao.daoWithdraw)));
addMode(addInput(daoCmd.command('execute')).action(withInput(dao.daoExecute)));
addInput(daoCmd.command('discussion-list')).action(withInput(dao.discussionList));
addInput(daoCmd.command('discussion-comment')).action(withInput(dao.discussionComment));
addInput(daoCmd.command('proposal-my-info')).action(withInput(dao.daoProposalMyInfo));
addInput(daoCmd.command('token-allowance-view')).action(withInput(dao.daoTokenAllowanceView));
addInput(daoCmd.command('token-balance-view')).action(withInput(dao.daoTokenBalanceView));

const tokenCmd = program.command('token').description('Generic token read helpers');
addInput(tokenCmd.command('allowance-view')).action(withInput(token.tokenAllowanceView));
addMode(addInput(tokenCmd.command('approve')).action(withInput(token.tokenApprove)));
addInput(tokenCmd.command('balance-view')).action(withInput(token.tokenBalanceView));

const networkCmd = program.command('network').description('Network governance domain tools');
addInput(networkCmd.command('proposals-list')).action(withInput(network.networkProposalsList));
addInput(networkCmd.command('proposal-get')).action(withInput(network.networkProposalGet));
addMode(addInput(networkCmd.command('proposal-create')).action(withInput(network.networkProposalCreate)));
addMode(addInput(networkCmd.command('proposal-vote')).action(withInput(network.networkProposalVote)));
addMode(addInput(networkCmd.command('proposal-release')).action(withInput(network.networkProposalRelease)));
addMode(addInput(networkCmd.command('org-create')).action(withInput(network.networkOrganizationCreate)));
addInput(networkCmd.command('org-list')).action(withInput(network.networkOrganizationsList));
addInput(networkCmd.command('contract-name-check')).action(withInput(network.networkContractNameCheck));
addInput(networkCmd.command('contract-name-add')).action(withInput(network.networkContractNameAdd));
addInput(networkCmd.command('contract-name-update')).action(withInput(network.networkContractNameUpdate));
addMode(addInput(networkCmd.command('contract-flow-start')).action(withInput(network.networkContractFlowStart)));
addMode(addInput(networkCmd.command('contract-flow-release')).action(withInput(network.networkContractFlowRelease)));
addInput(networkCmd.command('contract-flow-status')).action(withInput(network.networkContractFlowStatus));

const bpCmd = program.command('bp').description('BP election domain tools');
addMode(addInput(bpCmd.command('apply')).action(withInput(bp.bpApply)));
addMode(addInput(bpCmd.command('quit')).action(withInput(bp.bpQuit)));
addMode(addInput(bpCmd.command('vote')).action(withInput(bp.bpVote)));
addMode(addInput(bpCmd.command('withdraw')).action(withInput(bp.bpWithdraw)));
addMode(addInput(bpCmd.command('change-vote')).action(withInput(bp.bpChangeVote)));
addMode(addInput(bpCmd.command('claim-profits')).action(withInput(bp.bpClaimProfits)));
addInput(bpCmd.command('votes-list')).action(withInput(bp.bpVotesList));
addInput(bpCmd.command('team-desc-get')).action(withInput(bp.bpTeamDescGet));
addInput(bpCmd.command('team-desc-list')).action(withInput(bp.bpTeamDescList));
addInput(bpCmd.command('team-desc-add')).action(withInput(bp.bpTeamDescAdd));
addInput(bpCmd.command('vote-reclaim')).action(withInput(bp.bpVoteReclaim));

const resourceCmd = program.command('resource').description('Resource token domain tools');
addMode(addInput(resourceCmd.command('buy')).action(withInput(resource.resourceBuy)));
addMode(addInput(resourceCmd.command('sell')).action(withInput(resource.resourceSell)));
addInput(resourceCmd.command('realtime-records')).action(withInput(resource.resourceRealtimeRecords));
addInput(resourceCmd.command('turnover')).action(withInput(resource.resourceTurnover));
addInput(resourceCmd.command('records')).action(withInput(resource.resourceRecords));

program.parseAsync(process.argv);
