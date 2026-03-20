#!/usr/bin/env node
// ERC-8004 Agent Feedback Script
import { parseArgs } from 'node:util';
import { createInterface } from 'node:readline';

const { values: args } = parseArgs({
  options: {
    'agent-id': { type: 'string' },
    value:      { type: 'string' },
    tag1:       { type: 'string' },
    tag2:       { type: 'string' },
    yes:        { type: 'boolean', default: false },
  },
  strict: true,
});

if (!args['agent-id'] || !args.value) {
  console.error('Error: --agent-id and --value are required');
  process.exit(1);
}

const value = parseInt(args.value, 10);
if (value < 1 || value > 5) {
  console.error('Error: --value must be 1-5');
  process.exit(1);
}

const privateKey = process.env.PRIVATE_KEY || process.env.AGENT_PRIVATE_KEY;
if (!privateKey) {
  console.error('Error: PRIVATE_KEY or AGENT_PRIVATE_KEY env var required');
  process.exit(1);
}

// --- DRAFT ---
console.log('\n╔══════════════════════════════════════╗');
console.log('║      AGENT FEEDBACK — DRAFT          ║');
console.log('╚══════════════════════════════════════╝\n');
console.log(`  Agent ID: ${args['agent-id']}`);
console.log(`  Value:    ${value}/5`);
console.log(`  Tag 1:    ${args.tag1 || '(none)'}`);
console.log(`  Tag 2:    ${args.tag2 || '(none)'}`);
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

if (!(await confirm('Submit this feedback on-chain?'))) {
  console.log('Aborted.');
  process.exit(0);
}

try {
  const { SDK } = await import('agent0-sdk');
  const [cid] = args['agent-id'].split(':');
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
  });

  const result = await sdk.giveFeedback(
    args['agent-id'],
    value,
    args.tag1 || '',
    args.tag2 || '',
  );

  console.log('\n✅ Feedback submitted!');
  console.log(`  TX: ${result?.tx ?? result?.transactionHash ?? '(pending)'}`);
} catch (err) {
  console.error('\n❌ Feedback failed:', err.message);
  process.exit(1);
}
