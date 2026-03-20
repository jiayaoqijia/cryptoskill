#!/usr/bin/env node
// ERC-8004 Agent Search Script
import { parseArgs } from 'node:util';

const { values: args } = parseArgs({
  options: {
    name:   { type: 'string' },
    chain:  { type: 'string', default: process.env.CHAIN_ID || '8453' },
    active: { type: 'boolean', default: false },
    skills: { type: 'string' },
    tools:  { type: 'string' },
  },
  strict: true,
});

const chainId = parseInt(args.chain, 10);
const DEFAULT_RPCS = {
  8453: 'https://mainnet.base.org', 1: 'https://eth.llamarpc.com',
  137: 'https://polygon-rpc.com', 56: 'https://bsc-dataseed.binance.org',
  42161: 'https://arb1.arbitrum.io/rpc',
};
const rpcUrl = process.env.RPC_URL || DEFAULT_RPCS[chainId] || '';

try {
  const { SDK } = await import('agent0-sdk');

  const sdk = new SDK({
    chainId,
    rpcUrl,
  });

  const filters = {};
  if (args.name) filters.name = args.name;
  if (args.active) filters.active = true;
  if (args.skills) filters.skills = args.skills.split(',').map(s => s.trim());
  if (args.tools) filters.tools = args.tools.split(',').map(s => s.trim());

  const options = { chainId };
  const results = await sdk.searchAgents(filters, options);

  if (!results || results.length === 0) {
    console.log('No agents found matching criteria.');
    process.exit(0);
  }

  console.log(`Found ${results.length} agent(s):\n`);
  for (const agent of results) {
    console.log(`  ID:          ${agent.id ?? agent.agentId ?? 'N/A'}`);
    console.log(`  Name:        ${agent.name ?? 'N/A'}`);
    console.log(`  Description: ${agent.description ?? 'N/A'}`);
    console.log(`  Chain:       ${agent.chainId ?? chainId}`);
    console.log('  ---');
  }
} catch (err) {
  console.error('❌ Search failed:', err.message);
  process.exit(1);
}
