#!/usr/bin/env node
// ERC-8004 Agent Update Script
import { parseArgs } from 'node:util';
import { createInterface } from 'node:readline';

const { values: args } = parseArgs({
  options: {
    'agent-id':    { type: 'string' },
    name:          { type: 'string' },
    description:   { type: 'string' },
    image:         { type: 'string' },
    a2a:           { type: 'string' },
    mcp:           { type: 'string' },
    yes:           { type: 'boolean', default: false },
  },
  strict: true,
});

if (!args['agent-id']) {
  console.error('Error: --agent-id required (format: chainId:agentId, e.g. "1:42")');
  process.exit(1);
}

const privateKey = process.env.PRIVATE_KEY || process.env.AGENT_PRIVATE_KEY;
if (!privateKey) {
  console.error('Error: PRIVATE_KEY or AGENT_PRIVATE_KEY env var required');
  process.exit(1);
}

const updates = {};
if (args.name) updates.name = args.name;
if (args.description) updates.description = args.description;
if (args.image) updates.image = args.image;
if (args.a2a) updates.a2aUrl = args.a2a;
if (args.mcp) updates.mcpUrl = args.mcp;

if (Object.keys(updates).length === 0) {
  console.error('Error: Provide at least one field to update (--name, --description, --image, --a2a, --mcp)');
  process.exit(1);
}

// --- DRAFT ---
console.log('\n╔══════════════════════════════════════╗');
console.log('║       AGENT UPDATE — DRAFT           ║');
console.log('╚══════════════════════════════════════╝\n');
console.log(`  Agent ID: ${args['agent-id']}`);
for (const [k, v] of Object.entries(updates)) {
  console.log(`  ${k}: ${v}`);
}
console.log();

async function confirm(msg) {
  if (args.yes) return true;
  const rl = createInterface({ input: process.stdin, output: process.stdout });
  return new Promise(resolve => {
    rl.question(`${msg} (y/N): `, answer => {
      rl.close();
      resolve(answer.toLowerCase() === 'y');
    });
  });
}

if (!(await confirm('Submit this update on-chain?'))) {
  console.log('Aborted.');
  process.exit(0);
}

try {
  const { SDK } = await import('agent0-sdk');
  const [cid, aid] = args['agent-id'].split(':');
  const chainId = parseInt(cid, 10);

  const DEFAULT_RPCS = {
    8453: 'https://mainnet.base.org', 1: 'https://eth.llamarpc.com',
    137: 'https://polygon-rpc.com', 56: 'https://bsc-dataseed.binance.org',
    42161: 'https://arb1.arbitrum.io/rpc',
  };
  const rpcUrl = process.env.RPC_URL || DEFAULT_RPCS[chainId] || '';

  const sdk = new SDK({
    chainId,
    rpcUrl,
    privateKey,
    ipfs: process.env.PINATA_JWT ? 'pinata' : 'filecoinPin',
    pinataJwt: process.env.PINATA_JWT,
  });

  const agent = await sdk.loadAgent(args['agent-id']);
  if (updates.name) agent.name = updates.name;
  if (updates.description) agent.description = updates.description;
  if (updates.image) agent.image = updates.image;
  if (updates.a2aUrl) agent.a2aUrl = updates.a2aUrl;
  if (updates.mcpUrl) agent.mcpUrl = updates.mcpUrl;

  const result = await agent.registerIPFS();
  console.log('\n✅ Agent updated successfully!');
  console.log(`  TX: ${result?.tx ?? result?.transactionHash ?? '(pending)'}`);
} catch (err) {
  console.error('\n❌ Update failed:', err.message);
  process.exit(1);
}
