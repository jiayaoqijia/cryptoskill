#!/usr/bin/env node
// ERC-8004 Agent Registration Script (basecred-8004-registration)
// Usage: node register.mjs --json registration.json [--chain 8453] [--dry-run] [--yes]
//    or: node register.mjs --name "Agent" --description "Desc" [options]
//    or: node register.mjs --template (output blank 8004.org JSON template)

import { parseArgs } from 'node:util';
import { createInterface } from 'node:readline';
import { readFileSync } from 'node:fs';

const { values: args } = parseArgs({
  options: {
    // Basic info
    name:        { type: 'string' },
    description: { type: 'string' },
    image:       { type: 'string' },
    version:     { type: 'string' },
    author:      { type: 'string' },
    license:     { type: 'string' },
    // Endpoints
    a2a:         { type: 'string' },
    mcp:         { type: 'string' },
    // Skills & domains (comma-separated)
    skills:      { type: 'string' },
    domains:     { type: 'string' },
    'custom-skills':  { type: 'string' },
    'custom-domains': { type: 'string' },
    // Wallet
    wallet:      { type: 'string' },
    // Advanced
    chain:       { type: 'string', default: process.env.CHAIN_ID || '8453' },
    storage:     { type: 'string', default: 'http' },
    trust:       { type: 'string' },
    x402:        { type: 'boolean', default: false },
    active:      { type: 'boolean', default: true },
    // Control
    json:        { type: 'string' },
    'dry-run':   { type: 'boolean', default: false },
    yes:         { type: 'boolean', default: false },
    template:    { type: 'boolean', default: false },
  },
  strict: true,
});

// --- Helper: Convert OASF paths to skill objects ---
function oasfPathToSkill(path) {
  const parts = path.split('/');
  const id = parts[parts.length - 1].replace(/_/g, '-');
  const name = parts[parts.length - 1].split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
  const tags = parts.slice(0, -1).map(p => p.replace(/_/g, '-'));
  tags.push(id);
  
  const descriptions = {
    'summarization': 'Generate concise summaries of long-form text and documents.',
    'question-answering': 'Answer questions based on provided context or general knowledge.',
    'coding-skills': 'Write, review, debug, and explain code across multiple programming languages.',
    'images-computer-vision': 'Analyze, describe, and extract information from images.',
    'agent-coordination': 'Coordinate with other AI agents via protocols like A2A.',
    'workflow-automation': 'Automate recurring tasks and multi-step workflows.',
  };
  
  return {
    id,
    name,
    description: descriptions[id] || `${name} capabilities.`,
    tags,
  };
}

// --- Template output (8004.org format) ---
if (args.template) {
  const template = {
    basicInfo: {
      agentName: '',
      agentAddress: '',
      description: '',
      image: '',
      version: '1.0.0',
      author: '',
      license: 'MIT',
    },
    endpoints: {
      mcpEndpoint: '',
      a2aEndpoint: '/.well-known/agent.json',
    },
    skillsDomains: {
      selectedSkills: [],
      selectedDomains: [],
      customSkills: [],
      customDomains: [],
    },
    advancedConfig: {
      supportedTrusts: [],
      x402support: false,
      storageMethod: 'http',
      active: true,
    },
    version: '1.0.0',
  };
  console.log(JSON.stringify(template, null, 2));
  process.exit(0);
}

// --- Parse input (CLI args or JSON file) ---
let regInput = {};
if (args.json) {
  try {
    regInput = JSON.parse(readFileSync(args.json, 'utf-8'));
  } catch (e) {
    console.error(`Error reading JSON file: ${e.message}`);
    process.exit(1);
  }
}

// --- Normalize from 8004.org format or SDK format ---
const bi = regInput.basicInfo || {};
const ep = regInput.endpoints || {};
const sd = regInput.skillsDomains || {};
const ac = regInput.advancedConfig || {};

// Helper: parse comma-separated string or use array
function csvOrArray(cliVal, jsonVal) {
  if (cliVal) return cliVal.split(',').map(s => s.trim()).filter(Boolean);
  if (Array.isArray(jsonVal)) return jsonVal;
  return [];
}

// Resolve all fields (CLI overrides JSON)
const reg = {
  // Basic info
  name:        args.name || bi.agentName || regInput.name || '',
  description: args.description || bi.description || regInput.description || '',
  image:       args.image || bi.image || regInput.image || '',
  version:     args.version || bi.version || regInput.version || '1.0.0',
  author:      args.author || bi.author || '',
  license:     args.license || bi.license || 'MIT',
  // Endpoints
  a2a: args.a2a || ep.a2aEndpoint || ep.a2a || (Array.isArray(regInput.endpoints) ? regInput.endpoints.find(e => e.type === 'a2a')?.value : '') || '',
  mcp: args.mcp || ep.mcpEndpoint || ep.mcp || (Array.isArray(regInput.endpoints) ? regInput.endpoints.find(e => e.type === 'mcp')?.value : '') || '',
  // Skills & domains
  selectedSkills:  csvOrArray(args.skills, sd.selectedSkills),
  selectedDomains: csvOrArray(args.domains, sd.selectedDomains),
  customSkills:    csvOrArray(args['custom-skills'], sd.customSkills),
  customDomains:   csvOrArray(args['custom-domains'], sd.customDomains),
  // Advanced
  trusts:   args.trust ? args.trust.split(',').map(s => s.trim()) : (ac.supportedTrusts || []),
  x402:     args.x402 || ac.x402support || false,
  storage:  args.storage || ac.storageMethod || 'http',
  active:   args.active ?? ac.active ?? true,
};

if (!reg.name || !reg.description) {
  console.error('Error: name and description are required (via --name/--description or --json)');
  process.exit(1);
}

// --- Chain ---
const chainId = parseInt(args.chain, 10);
const SUPPORTED_CHAINS = {
  8453:   { name: 'Base',      rpc: 'https://mainnet.base.org' },
  1:      { name: 'Ethereum',  rpc: 'https://eth.llamarpc.com' },
  137:    { name: 'Polygon',   rpc: 'https://polygon-rpc.com' },
  56:     { name: 'BNB Chain', rpc: 'https://bsc-dataseed.binance.org' },
  42161:  { name: 'Arbitrum',  rpc: 'https://arb1.arbitrum.io/rpc' },
  42220:  { name: 'Celo',      rpc: 'https://forno.celo.org' },
  100:    { name: 'Gnosis',    rpc: 'https://rpc.gnosischain.com' },
  534352: { name: 'Scroll',    rpc: 'https://rpc.scroll.io' },
};

if (!SUPPORTED_CHAINS[chainId]) {
  console.error(`Error: Chain ${chainId} not supported. Use: ${Object.entries(SUPPORTED_CHAINS).map(([id, c]) => `${c.name}(${id})`).join(', ')}`);
  process.exit(1);
}

const chainInfo = SUPPORTED_CHAINS[chainId];
const rpcUrl = process.env.RPC_URL || chainInfo.rpc;

// --- Private key ---
const privateKey = process.env.PRIVATE_KEY || process.env.AGENT_PRIVATE_KEY || process.env.MAIN_WALLET_PRIVATE_KEY;
if (!privateKey && !args['dry-run']) {
  console.error('Error: PRIVATE_KEY, AGENT_PRIVATE_KEY, or MAIN_WALLET_PRIVATE_KEY env var required');
  process.exit(1);
}

// Derive wallet address — from CLI --wallet, JSON agentAddress, or private key
let walletAddress = args.wallet || bi.agentAddress || '';
let walletSource = 'pasted';
if (!walletAddress && privateKey) {
  try {
    const { privateKeyToAccount } = await import('viem/accounts');
    const pk = privateKey.startsWith('0x') ? privateKey : `0x${privateKey}`;
    walletAddress = privateKeyToAccount(pk).address;
    walletSource = 'auto (.env)';
  } catch { /* ignore in dry-run */ }
}
if (!walletAddress) {
  walletAddress = '(not set)';
  walletSource = '⚠️ missing';
}

// --- DRAFT ---
console.log('\n╔══════════════════════════════════════╗');
console.log('║     AGENT REGISTRATION — DRAFT       ║');
console.log('╚══════════════════════════════════════╝');

console.log('\n  ── Basic Info ──');
console.log(`  Name:        ${reg.name}`);
console.log(`  Address:     ${walletAddress} (${walletSource})`);
console.log(`  Description: ${reg.description}`);
console.log(`  Image:       ${reg.image || '(none)'}`);
console.log(`  Version:     ${reg.version}`);
console.log(`  Author:      ${reg.author || '(none)'}`);
console.log(`  License:     ${reg.license}`);

console.log('\n  ── Endpoints ──');
console.log(`  A2A:         ${reg.a2a || '(none)'}`);
console.log(`  MCP:         ${reg.mcp || '(none)'}`);

console.log('\n  ── Skills & Domains ──');
console.log(`  Skills:      ${reg.selectedSkills.length ? reg.selectedSkills.join(', ') : '(none)'}`);
console.log(`  Domains:     ${reg.selectedDomains.length ? reg.selectedDomains.join(', ') : '(none)'}`);
console.log(`  Custom Skills:  ${reg.customSkills.length ? reg.customSkills.join(', ') : '(none)'}`);
console.log(`  Custom Domains: ${reg.customDomains.length ? reg.customDomains.join(', ') : '(none)'}`);

console.log('\n  ── Config ──');
console.log(`  Chain:       ${chainInfo.name} (${chainId})`);
console.log(`  Storage:     ${reg.storage === 'http' ? 'Fully onchain' : 'IPFS'}`);
console.log(`  Active:      ${reg.active}`);
console.log(`  x402:        ${reg.x402}`);
console.log(`  Trust:       ${reg.trusts.length ? reg.trusts.join(', ') : '(none)'}`);
console.log(`  Dry Run:     ${args['dry-run']}`);
console.log();

if (args['dry-run']) {
  // Generate skills array from OASF paths
  const allSkillPaths = [...reg.selectedSkills, ...reg.customSkills];
  const skillsArray = allSkillPaths.map(oasfPathToSkill);
  
  // Build A2A service endpoint
  const a2aEndpoint = reg.a2a || '/.well-known/agent.json';
  
  // Output merged A2A + ERC-8004 format
  const preview = {
    // A2A top-level fields
    name: reg.name,
    description: reg.description,
    version: reg.version,
    image: reg.image,
    icon_url: reg.image,
    provider: {
      organization: reg.author || reg.name,
      url: a2aEndpoint.startsWith('http') ? a2aEndpoint.split('/')[0] + '//' + a2aEndpoint.split('/')[2] : '',
    },
    supported_interfaces: [
      {
        url: a2aEndpoint,
        protocol_binding: 'HTTP+JSON',
        protocol_version: '0.3',
      },
    ],
    capabilities: {
      streaming: false,
      pushNotifications: false,
    },
    default_input_modes: ['text/plain', 'application/json'],
    default_output_modes: ['text/plain', 'application/json'],
    skills: skillsArray,
    
    // ERC-8004 fields
    type: 'https://eips.ethereum.org/EIPS/eip-8004#registration-v1',
    services: [
      {
        name: 'A2A',
        endpoint: a2aEndpoint,
        version: '0.3.0',
      },
      {
        name: 'OASF',
        endpoint: 'https://github.com/agntcy/oasf/',
        version: '0.8.0',
        skills: allSkillPaths,
        domains: [...reg.selectedDomains, ...reg.customDomains],
      },
    ],
    x402Support: reg.x402,
    active: reg.active,
    registrations: [],
    supportedTrust: reg.trusts,
  };
  
  console.log('📋 Registration file (merged A2A + ERC-8004 format):');
  console.log(JSON.stringify(preview, null, 2));
  console.log('\n🏁 Dry run complete. No transaction submitted.');
  process.exit(0);
}

// --- Confirm ---
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

// --- Safeguard: duplicate check ---
const REGISTRY_ADDRESSES = {
  IDENTITY: '0x8004A169FB4a3325136EB29fA0ceB6D2e539a432',
  REPUTATION: '0x8004BAa17C55a88189AE136b182e5fdA19dE9b63',
};

if (walletAddress && walletAddress !== '(not set)') {
  try {
    const { createPublicClient, http: viemHttp } = await import('viem');
    const pubClient = createPublicClient({ transport: viemHttp(rpcUrl) });
    const balance = await pubClient.readContract({
      address: REGISTRY_ADDRESSES.IDENTITY,
      abi: [{ name: 'balanceOf', type: 'function', stateMutability: 'view', inputs: [{ name: 'owner', type: 'address' }], outputs: [{ type: 'uint256' }] }],
      functionName: 'balanceOf',
      args: [walletAddress],
    });
    if (Number(balance) > 0) {
      console.log(`\n⚠️  Warning: This wallet already owns ${balance} agent(s) on ${chainInfo.name}.`);
      console.log('   Registering again will create a duplicate.');
      console.log('   Use update.mjs to modify an existing agent instead.');
      if (!args.yes) {
        if (!(await confirm('   Continue anyway?'))) {
          console.log('Aborted.');
          process.exit(0);
        }
      }
    }
  } catch { /* non-blocking — proceed if check fails */ }
}

if (!(await confirm('Submit this registration on-chain?'))) {
  console.log('Aborted.');
  process.exit(0);
}

// --- Execute ---
try {
  const { SDK } = await import('agent0-sdk');

  const sdk = new SDK({
    chainId,
    rpcUrl,
    privateKey,
    ipfs: reg.storage === 'ipfs' ? (process.env.PINATA_JWT ? 'pinata' : 'filecoinPin') : undefined,
    pinataJwt: process.env.PINATA_JWT,
    registryOverrides: {
      [chainId]: REGISTRY_ADDRESSES,
    },
  });

  // Create agent object
  const agent = sdk.createAgent(reg.name, reg.description, reg.image);

  // Set endpoints
  if (reg.a2a) await agent.setA2A(reg.a2a);
  if (reg.mcp) await agent.setMCP(reg.mcp);

  // Set skills & domains (OASF)
  for (const skill of [...reg.selectedSkills, ...reg.customSkills]) {
    agent.addSkill(skill, false);
  }
  for (const domain of [...reg.selectedDomains, ...reg.customDomains]) {
    agent.addDomain(domain, false);
  }

  // Set trust models
  if (reg.trusts.length) {
    agent.setTrust(
      reg.trusts.includes('reputation'),
      reg.trusts.includes('crypto-economic'),
      reg.trusts.includes('tee-attestation'),
    );
  }

  // Set active/x402
  agent.setActive(reg.active);
  agent.setX402Support(reg.x402);

  // Set metadata (author, license, version)
  const meta = {};
  if (reg.author) meta.author = reg.author;
  if (reg.license) meta.license = reg.license;
  if (reg.version) meta.version = reg.version;
  if (Object.keys(meta).length) agent.setMetadata(meta);

  // Register
  let txHandle;
  if (reg.storage === 'http') {
    const agentUri = reg.a2a || '';
    console.log(`📡 Registering fully onchain (URI: ${agentUri || '(none)'})`);
    txHandle = await agent.registerHTTP(agentUri);
  } else {
    console.log('📦 Registering with IPFS storage...');
    txHandle = await agent.registerIPFS();
  }

  // Wait for confirmation
  console.log('\n⏳ Waiting for transaction confirmation...');
  const result = await txHandle.waitMined();

  console.log('\n✅ Agent registered successfully!');
  console.log(`  Agent ID:  ${result?.agentId ?? agent.agentId ?? '(check explorer)'}`);
  console.log(`  Agent URI: ${result?.agentURI ?? agent.agentURI ?? '(pending)'}`);
  console.log(`  Chain:     ${chainInfo.name} (${chainId})`);

  // Set agent wallet on-chain
  if (walletAddress && walletAddress !== '(dry-run)') {
    console.log(`\n🔑 Setting agent wallet: ${walletAddress}`);
    try {
      const walletTxHandle = await agent.setWallet(walletAddress);
      if (walletTxHandle) {
        console.log('⏳ Waiting for wallet confirmation...');
        await walletTxHandle.waitMined();
      }
      console.log(`✅ Agent wallet set: ${walletAddress}`);
    } catch (err) {
      console.error(`⚠️  Wallet set failed (can retry later): ${err.message}`);
    }
  }

  // Output full registration file in merged A2A + ERC-8004 format
  const baseRegFile = agent.getRegistrationFile();
  
  // Generate skills array from OASF paths
  const allSkillPaths = [...reg.selectedSkills, ...reg.customSkills];
  const skillsArray = allSkillPaths.map(oasfPathToSkill);
  
  // Build A2A service endpoint
  const a2aEndpoint = reg.a2a || '/.well-known/agent.json';
  
  // Merge A2A fields with ERC-8004 fields
  const regFile = {
    // A2A top-level fields
    name: reg.name,
    description: reg.description,
    version: reg.version,
    image: reg.image,
    icon_url: reg.image,
    provider: {
      organization: reg.author || reg.name,
      url: a2aEndpoint.startsWith('http') ? a2aEndpoint.split('/')[0] + '//' + a2aEndpoint.split('/')[2] : '',
    },
    supported_interfaces: [
      {
        url: a2aEndpoint,
        protocol_binding: 'HTTP+JSON',
        protocol_version: '0.3',
      },
    ],
    capabilities: {
      streaming: false,
      pushNotifications: false,
    },
    default_input_modes: ['text/plain', 'application/json'],
    default_output_modes: ['text/plain', 'application/json'],
    skills: skillsArray,
    
    // ERC-8004 fields (from SDK)
    ...baseRegFile,
  };
  
  console.log('\n📋 Registration file (merged A2A + ERC-8004 format):');
  console.log(JSON.stringify(regFile, null, 2));

} catch (err) {
  console.error('\n❌ Registration failed:', err.message);
  process.exit(1);
}
