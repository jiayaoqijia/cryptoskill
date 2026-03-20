#!/usr/bin/env node

/**
 * TRC-8004 Multi-Chain Query Script
 * 
 * Query agent information and reputation on TRON or BSC
 * Usage: 
 *   node query.js agent <id> --chain tron --network mainnet
 *   node query.js reputation <id> --chain bsc --network testnet
 */

const fs = require('fs');
const path = require('path');
const { createClient, convertAbiToEvm } = require('./chain-adapter');
const { displayError } = require('./utils');

// Load contracts configuration
const contractsConfig = JSON.parse(
  fs.readFileSync(path.join(__dirname, '../lib/contracts.json'), 'utf8')
);

// Load chain-specific ABIs
const tronAbi = JSON.parse(
  fs.readFileSync(path.join(__dirname, '../lib/tron-abi.json'), 'utf8')
);
const bscAbi = JSON.parse(
  fs.readFileSync(path.join(__dirname, '../lib/bsc-abi.json'), 'utf8')
);

// Helper function to get ABI for a chain
function getAbi(chainConfig, contractType, operation = 'query') {
  if (chainConfig.type === 'tron') {
    // TRON uses split ABIs to avoid tuple[] parsing issues
    const abiSet = tronAbi[contractType];
    if (operation === 'write') {
      return [...abiSet.query, ...abiSet.write];
    }
    return abiSet.query;
  } else if (chainConfig.type === 'evm') {
    return bscAbi[contractType];
  }
  throw new Error(`Unknown chain type: ${chainConfig.type}`);
}

function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    queryType: args[0] || '',
    agentId: args[1] || '',
    chain: 'tron',
    network: 'nile'
  };

  for (let i = 2; i < args.length; i++) {
    if (args[i] === '--chain' && args[i + 1]) {
      options.chain = args[i + 1];
      i++;
    } else if (args[i] === '--network' && args[i + 1]) {
      options.network = args[i + 1];
      i++;
    }
  }

  return options;
}

async function queryAgent(client, contract, agentId) {
  console.log(`📋 Agent ID: ${agentId}`);
  console.log('');

  try {
    // Try to get owner (this is the most reliable way to check if agent exists)
    let owner;
    try {
      owner = await client.callMethod(contract, 'ownerOf', agentId);
      console.log(`👤 Owner: ${owner}`);
    } catch (e) {
      console.log('❌ Agent does not exist');
      return;
    }

    // Get URI - try both agentURI and tokenURI for compatibility
    try {
      let uri;
      try {
        // Try agentURI first (ERC-8004 standard)
        uri = await client.callMethod(contract, 'agentURI', agentId);
      } catch (e) {
        // Fallback to tokenURI (ERC-721 standard)
        uri = await client.callMethod(contract, 'tokenURI', agentId);
      }
      console.log(`🔗 URI: ${uri || '(not set)'}`);
    } catch (e) {
      console.log(`🔗 URI: (not set)`);
    }

    // Get wallet if set (optional, may not be supported on all deployments)
    try {
      const wallet = await client.callMethod(contract, 'getAgentWallet', agentId);
      const zeroAddresses = ['0x0000000000000000000000000000000000000000', 'T9yD14Nj9j7xAB4dbGeiX9h8unkKHxuWwb'];
      if (wallet && !zeroAddresses.includes(wallet)) {
        console.log(`💼 Wallet: ${wallet}`);
      }
    } catch (e) {
      // Wallet feature not available on this deployment
    }

    console.log('');
    console.log('✅ Query successful');

  } catch (error) {
    throw error;
  }
}

async function queryReputation(client, contract, agentId) {
  console.log(`📊 Reputation for Agent ID: ${agentId}`);
  console.log('');

  try {
    // First, get the list of clients who gave feedback
    console.log('🔍 Checking for feedback clients...');
    let clients = [];
    try {
      const clientsResult = await client.callMethod(contract, 'getClients', agentId);
      // Create a new array to avoid read-only issues
      clients = Array.isArray(clientsResult) ? [...clientsResult] : [];
      console.log(`   Found ${clients.length} client(s) who gave feedback`);
      if (clients.length > 0) {
        console.log(`   Clients: ${clients.slice(0, 3).join(', ')}${clients.length > 3 ? '...' : ''}`);
      }
    } catch (e) {
      console.log(`   Could not get clients list: ${e.message}`);
    }
    console.log('');

    // Get summary - use clients list if available, otherwise empty array
    console.log('📊 Querying reputation summary...');
    const summary = await client.callMethod(
      contract,
      'getSummary',
      agentId,
      clients, // use actual clients list
      '', // no tag1 filter
      ''  // no tag2 filter
    );

    const count = summary[0] || summary.count;
    const value = summary[1] || summary.summaryValue;
    const decimals = summary[2] || summary.summaryValueDecimals;

    console.log(`📈 Total Feedback: ${count.toString()}`);
    
    if (count > 0) {
      const actualValue = Number(value) / Math.pow(10, Number(decimals));
      console.log(`⭐ Average Score: ${actualValue.toFixed(Number(decimals))}`);
    } else {
      console.log(`⭐ Average Score: No feedback yet`);
    }

    console.log('');
    console.log('✅ Query successful');

  } catch (error) {
    // Show the actual error for debugging
    console.log('⚠️  Error querying reputation:');
    console.log(`   ${error.message || error}`);
    console.log('');
    console.log('   This usually means:');
    console.log('   - The reputation registry is not initialized');
    console.log('   - Agent has no feedback yet');
    console.log('   - Or the contract requires specific parameters');
  }
}

async function query() {
  const options = parseArgs();

  if (!options.queryType || !options.agentId) {
    console.log('TRC-8004 Multi-Chain Query');
    console.log('');
    console.log('Usage:');
    console.log('  node query.js agent <id> --chain tron --network mainnet');
    console.log('  node query.js reputation <id> --chain bsc --network testnet');
    console.log('');
    console.log('Query Types:');
    console.log('  agent        Query agent information (owner, URI, wallet)');
    console.log('  reputation   Query reputation summary');
    console.log('');
    console.log('Options:');
    console.log('  --chain <name>     Chain: tron, bsc (default: tron)');
    console.log('  --network <name>   Network name (default: nile)');
    console.log('');
    console.log('Examples:');
    console.log('  # Query agent on TRON');
    console.log('  node query.js agent 1 --chain tron --network nile');
    console.log('');
    console.log('  # Query reputation on BSC');
    console.log('  node query.js reputation 1 --chain bsc --network testnet');
    process.exit(0);
  }

  // Validate chain
  if (!contractsConfig.chains[options.chain]) {
    console.error(`❌ Invalid chain: ${options.chain}`);
    console.error(`Available chains: ${Object.keys(contractsConfig.chains).join(', ')}`);
    process.exit(1);
  }

  const chainConfig = contractsConfig.chains[options.chain];
  
  // Validate network
  if (!chainConfig.networks[options.network]) {
    console.error(`❌ Invalid network: ${options.network}`);
    console.error(`Available networks for ${options.chain}: ${Object.keys(chainConfig.networks).join(', ')}`);
    process.exit(1);
  }

  const networkConfig = chainConfig.networks[options.network];

  console.log(`🔗 Chain: ${chainConfig.name}`);
  console.log(`🌐 Network: ${networkConfig.name}`);
  console.log('');

  try {
    // Create chain client (no private key needed for queries)
    const client = await createClient({ ...networkConfig, type: chainConfig.type });

    if (options.queryType === 'agent') {
      // Query identity registry
      const contractAddress = networkConfig.contracts.identityRegistry;
      let abi = getAbi(chainConfig, 'identityRegistry');
      // Don't convert TRON ABI - it's already in TRON format
      const contract = await client.getContract(abi, contractAddress);
      await queryAgent(client, contract, options.agentId);

    } else if (options.queryType === 'reputation') {
      // Query reputation registry
      const contractAddress = networkConfig.contracts.reputationRegistry;
      let abi = getAbi(chainConfig, 'reputationRegistry');
      // Don't convert TRON ABI - it's already in TRON format
      const contract = await client.getContract(abi, contractAddress);
      await queryReputation(client, contract, options.agentId);

    } else {
      console.error(`❌ Invalid query type: ${options.queryType}`);
      console.error('Valid types: agent, reputation');
      process.exit(1);
    }

  } catch (error) {
    displayError(error, 'Query');
    process.exit(1);
  }
}

query();
