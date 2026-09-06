import { describe, expect, test } from 'bun:test';
import * as fs from 'node:fs';
import * as path from 'node:path';

const ROOT = path.resolve(import.meta.dir, '..', '..');
const OPENCLAW_PATH = path.join(ROOT, 'openclaw.json');
const MCP_SERVER_PATH = path.join(ROOT, 'src', 'mcp', 'server.ts');
const CLI_PATH = path.join(ROOT, 'tomorrowdao_skill.ts');

const REQUIRED_TOOLS = [
  'tomorrowdao_dao_create',
  'tomorrowdao_dao_update_metadata',
  'tomorrowdao_dao_upload_files',
  'tomorrowdao_dao_remove_files',
  'tomorrowdao_dao_proposal_create',
  'tomorrowdao_dao_vote',
  'tomorrowdao_dao_withdraw',
  'tomorrowdao_dao_execute',
  'tomorrowdao_discussion_list',
  'tomorrowdao_discussion_comment',
  'tomorrowdao_dao_proposal_my_info',
  'tomorrowdao_token_allowance_view',
  'tomorrowdao_token_approve',
  'tomorrowdao_token_balance_view',
  'tomorrowdao_dao_token_allowance_view',
  'tomorrowdao_dao_token_balance_view',
  'tomorrowdao_network_proposals_list',
  'tomorrowdao_network_proposal_get',
  'tomorrowdao_network_proposal_create',
  'tomorrowdao_network_proposal_vote',
  'tomorrowdao_network_proposal_release',
  'tomorrowdao_network_org_create',
  'tomorrowdao_network_org_list',
  'tomorrowdao_network_contract_name_check',
  'tomorrowdao_network_contract_name_add',
  'tomorrowdao_network_contract_name_update',
  'tomorrowdao_network_contract_flow_start',
  'tomorrowdao_network_contract_flow_release',
  'tomorrowdao_network_contract_flow_status',
  'tomorrowdao_bp_apply',
  'tomorrowdao_bp_quit',
  'tomorrowdao_bp_vote',
  'tomorrowdao_bp_withdraw',
  'tomorrowdao_bp_change_vote',
  'tomorrowdao_bp_claim_profits',
  'tomorrowdao_bp_votes_list',
  'tomorrowdao_bp_team_desc_get',
  'tomorrowdao_bp_team_desc_list',
  'tomorrowdao_bp_team_desc_add',
  'tomorrowdao_bp_vote_reclaim',
  'tomorrowdao_resource_buy',
  'tomorrowdao_resource_sell',
  'tomorrowdao_resource_realtime_records',
  'tomorrowdao_resource_turnover',
  'tomorrowdao_resource_records',
];

describe('tool surface', () => {
  test('openclaw tool names use tomorrowdao_* prefix', () => {
    const json = JSON.parse(fs.readFileSync(OPENCLAW_PATH, 'utf-8')) as {
      tools?: Array<{ name?: string }>;
    };
    const names = (json.tools || []).map((tool) => tool.name || '');

    expect(names.length).toBeGreaterThan(0);
    names.forEach((name) => {
      expect(name.startsWith('tomorrowdao_')).toBeTrue();
    });
  });

  test('mcp and openclaw register all required tools with parity', () => {
    const source = fs.readFileSync(MCP_SERVER_PATH, 'utf-8');
    const openclaw = JSON.parse(fs.readFileSync(OPENCLAW_PATH, 'utf-8')) as {
      tools?: Array<{ name?: string; inputSchema?: unknown }>;
    };

    const openclawNames = new Set((openclaw.tools || []).map((tool) => tool.name));

    REQUIRED_TOOLS.forEach((toolName) => {
      expect(source.includes(`'${toolName}'`)).toBeTrue();
      expect(openclawNames.has(toolName)).toBeTrue();
    });

    expect((openclaw.tools || []).length).toBe(REQUIRED_TOOLS.length);
  });

  test('cli exposes all domain handlers', () => {
    const cliSource = fs.readFileSync(CLI_PATH, 'utf-8');
    const handlerCount = [...cliSource.matchAll(/\.action\(withInput\(/g)].length;
    expect(handlerCount).toBe(REQUIRED_TOOLS.length);
  });

  test('openclaw tools expose non-null inputSchema', () => {
    const openclaw = JSON.parse(fs.readFileSync(OPENCLAW_PATH, 'utf-8')) as {
      tools?: Array<{ name?: string; inputSchema?: unknown }>;
    };

    (openclaw.tools || []).forEach((tool) => {
      expect(tool.inputSchema).toBeDefined();
      expect(tool.inputSchema).not.toBeNull();
    });
  });
});
