import { describe, expect, test } from 'bun:test';
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';

const READ_TOOLS = [
  'tomorrowdao_discussion_list',
  'tomorrowdao_dao_proposal_my_info',
  'tomorrowdao_token_allowance_view',
  'tomorrowdao_token_balance_view',
  'tomorrowdao_dao_token_allowance_view',
  'tomorrowdao_dao_token_balance_view',
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
];

describe('MCP tool annotations', () => {
  test('read-only allowlist stays read-only and mutations stay destructive', async () => {
    const transport = new StdioClientTransport({
      command: 'bun',
      args: ['run', 'src/mcp/server.ts'],
      cwd: process.cwd(),
    });
    const client = new Client(
      {
        name: 'tomorrowdao-annotations-test',
        version: '1.0.0',
      },
      {
        capabilities: {},
      },
    );

    try {
      await client.connect(transport);
      const result = await client.listTools();

      READ_TOOLS.forEach(name => {
        const tool = result.tools.find(item => item.name === name);
        expect(tool?.annotations?.readOnlyHint).toBe(true);
        expect(tool?.annotations?.destructiveHint).not.toBe(true);
      });

      const mutation = result.tools.find(tool => tool.name === 'tomorrowdao_dao_create');
      expect(mutation?.annotations?.destructiveHint).toBe(true);
      expect(mutation?.annotations?.openWorldHint).toBe(true);
    } finally {
      await client.close();
    }
  });
});
