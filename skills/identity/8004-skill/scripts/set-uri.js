#!/usr/bin/env node

/**
 * TRC-8004 Multi-Chain Set URI Script
 * 
 * Update agent metadata URI on TRON or BSC
 * Usage: 
 *   node set-uri.js --agent-id 1 --uri "ipfs://..." --chain tron --network mainnet
 */

const fs = require('fs');
const path = require('path');
const { createClient, convertAbiToEvm } = require('./chain-adapter');
const { getPrivateKeyOrExit, displayError, sleep } = require('./utils');

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
    agentId: '',
    uri: '',
    chain: 'tron',
    network: 'nile'
  };

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--agent-id' && args[i + 1]) {
      options.agentId = args[i + 1];
      i++;
    } else if (args[i] === '--uri' && args[i + 1]) {
      options.uri = args[i + 1];
      i++;
    } else if (args[i] === '--chain' && args[i + 1]) {
      options.chain = args[i + 1];
      i++;
    } else if (args[i] === '--network' && args[i + 1]) {
      options.network = args[i + 1];
      i++;
    }
  }

  return options;
}

async function setUri() {
  const options = parseArgs();

  if (!options.agentId || !options.uri) {
    console.log('TRC-8004 Multi-Chain Set URI');
    console.log('');
    console.log('Usage:');
    console.log('  node set-uri.js --agent-id <id> --uri <uri> [options]');
    console.log('');
    console.log('Required:');
    console.log('  --agent-id <id>      Agent ID to update');
    console.log('  --uri <uri>          New metadata URI (IPFS hash or URL)');
    console.log('');
    console.log('Optional:');
    console.log('  --chain <name>       Chain: tron, bsc (default: tron)');
    console.log('  --network <name>     Network name (default: nile)');
    console.log('');
    console.log('Environment:');
    console.log('  TRON_PRIVATE_KEY     Your wallet private key (required)');
    console.log('');
    console.log('Examples:');
    console.log('  # Update URI on TRON');
    console.log('  export TRON_PRIVATE_KEY="your_key"');
    console.log('  node set-uri.js --agent-id 1 --uri "ipfs://QmNewHash" --chain tron --network nile');
    console.log('');
    console.log('  # Update URI on BSC');
    console.log('  node set-uri.js --agent-id 1 --uri "ipfs://QmNewHash" --chain bsc --network testnet');
    console.log('');
    console.log('Note: Only the agent owner can update the URI');
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
  const contractAddress = networkConfig.contracts.identityRegistry;

  console.log(`🔗 Chain: ${chainConfig.name}`);
  console.log(`🌐 Network: ${networkConfig.name}`);
  console.log(`📝 Contract: ${contractAddress}`);
  console.log('');

  try {
    // Get private key
    const privateKey = getPrivateKeyOrExit();

    // Create chain client
    const client = await createClient({ ...networkConfig, type: chainConfig.type }, privateKey);
    const walletAddress = client.getAddress();
    
    console.log(`👛 Wallet: ${walletAddress}`);
    console.log(`📋 Agent ID: ${options.agentId}`);
    console.log(`🔗 New URI: ${options.uri}`);
    console.log('');

    // Get ABI
    let abi = getAbi(chainConfig, 'identityRegistry', 'write');

    // Get contract instance
    const contract = await client.getContract(abi, contractAddress);

    // Verify ownership
    console.log('🔍 Verifying ownership...');
    const owner = await client.callMethod(contract, 'ownerOf', options.agentId);
    
    if (owner.toLowerCase() !== walletAddress.toLowerCase()) {
      console.error('');
      console.error(`❌ Error: You are not the owner of agent ${options.agentId}`);
      console.error(`   Owner: ${owner}`);
      console.error(`   Your wallet: ${walletAddress}`);
      process.exit(1);
    }

    // Update URI
    console.log('📤 Updating URI...');
    
    const tx = await client.sendTransaction(
      contract,
      'setAgentURI',
      { feeLimit: 1000000000, value: 0 },
      options.agentId,
      options.uri
    );

    console.log('');
    console.log('✅ URI updated successfully!');
    console.log('');
    console.log(`📋 Transaction: ${tx}`);
    console.log(`🔍 View on explorer: ${networkConfig.explorer}/#/transaction/${tx}`);
    console.log('');

    // Wait for confirmation
    console.log('⏳ Waiting for confirmation...');
    await sleep(3000);

    console.log('');
    console.log('Next steps:');
    console.log(`  Query agent: node scripts/query.js agent ${options.agentId} --chain ${options.chain} --network ${options.network}`);

  } catch (error) {
    displayError(error, 'Set URI');
    process.exit(1);
  }
}

setUri();
