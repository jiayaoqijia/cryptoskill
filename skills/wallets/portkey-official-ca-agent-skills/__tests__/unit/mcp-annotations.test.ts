import { describe, expect, test } from 'bun:test';
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';

const READ_TOOLS = [
  'portkey_check_account',
  'portkey_prepare_auth_flow',
  'portkey_get_guardian_list',
  'portkey_get_holder_info',
  'portkey_manager_sync_status',
  'portkey_get_chain_info',
  'portkey_get_verifier',
  'portkey_check_status',
  'portkey_balance',
  'portkey_token_list',
  'portkey_nft_collections',
  'portkey_nft_items',
  'portkey_token_price',
  'portkey_tx_result',
  'portkey_transfer_preflight',
  'portkey_view_call',
  'portkey_wallet_status',
  'portkey_list_wallet_profiles',
  'portkey_get_active_wallet',
];

const LOCAL_WRITE_TOOLS = [
  'portkey_create_wallet',
  'portkey_save_keystore',
  'portkey_unlock',
  'portkey_lock',
  'portkey_set_active_wallet',
];

const NETWORK_WRITE_TOOLS = [
  'portkey_send_code',
  'portkey_verify_code',
  'portkey_register',
  'portkey_recover',
  'portkey_recover_and_save',
  'portkey_transfer',
  'portkey_cross_chain_transfer',
  'portkey_recover_stuck_transfer',
  'portkey_add_guardian',
  'portkey_remove_guardian',
  'portkey_forward_call',
];

describe('MCP tool annotations', () => {
  test('read, local write, and network write tools expose the expected annotations', async () => {
    const transport = new StdioClientTransport({
      command: 'bun',
      args: ['run', 'src/mcp/server.ts'],
      cwd: process.cwd(),
    });
    const client = new Client(
      {
        name: 'portkey-ca-annotations-test',
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

      LOCAL_WRITE_TOOLS.forEach(name => {
        const tool = result.tools.find(item => item.name === name);
        expect(tool?.annotations?.destructiveHint).toBe(true);
        expect(tool?.annotations?.openWorldHint).not.toBe(true);
      });

      NETWORK_WRITE_TOOLS.forEach(name => {
        const tool = result.tools.find(item => item.name === name);
        expect(tool?.annotations?.destructiveHint).toBe(true);
        expect(tool?.annotations?.openWorldHint).toBe(true);
      });
    } finally {
      await client.close();
    }
  });
});
