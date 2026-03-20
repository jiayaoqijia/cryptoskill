#!/usr/bin/env node

/**
 * TRC-8004 Multi-Chain Agent Registration
 * 
 * Register agents on TRON or BSC
 * Usage: 
 *   node register-multichain.js --uri "ipfs://..." --chain tron --network mainnet
 *   node register-multichain.js --uri "ipfs://..." --chain bsc --network testnet
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
    uri: '',
    chain: 'tron',
    network: 'nile',
    metadata: []
  };

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--uri' && args[i + 1]) {
      options.uri = args[i + 1];
      i++;
    } else if (args[i] === '--chain' && args[i + 1]) {
      options.chain = args[i + 1];
      i++;
    } else if (args[i] === '--network' && args[i + 1]) {
      options.network = args[i + 1];
      i++;
    } else if (args[i] === '--metadata' && args[i + 1]) {
      const [key, value] = args[i + 1].split(':');
      if (key && value) {
        options.metadata.push({ key, value });
      }
      i++;
    }
  }

  return options;
}

async function register() {
  const options = parseArgs();

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

  // Check if contracts are deployed
  if (contractAddress === '0x0000000000000000000000000000000000000000') {
    console.error(`❌ TRC-8004 contracts not yet deployed on ${chainConfig.name} ${networkConfig.name}`);
    console.error('   Please check back later or deploy your own contracts');
    process.exit(1);
  }

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
    console.log('');

    // Get ABI
    let abi = getAbi(chainConfig, 'identityRegistry', 'write');

    // Get contract instance
    const contract = await client.getContract(abi, contractAddress);

    // Register agent
    console.log('📤 Registering agent...');
    
    if (options.uri) {
      console.log(`   URI: ${options.uri}`);
    } else {
      console.log('   URI: (none - set later)');
    }

    let tx;
    if (options.uri) {
      tx = await client.sendTransaction(
        contract,
        'register',
        { feeLimit: 1000000000, value: 0 },
        options.uri
      );
    } else {
      tx = await client.sendTransaction(
        contract,
        'register',
        { feeLimit: 1000000000, value: 0 }
      );
    }

    console.log('');
    console.log('✅ Registration successful!');
    console.log('');
    console.log(`📋 Transaction: ${tx}`);
    console.log(`🔍 View on explorer: ${networkConfig.explorer}/#/transaction/${tx}`);
    console.log('');

    // Wait for confirmation
    console.log('⏳ Waiting for confirmation...');
    await sleep(3000);

    console.log('');
    console.log('Next steps:');
    if (!options.uri) {
      console.log(`  1. Set agent URI: node scripts/set-uri.js --agent-id <id> --uri "ipfs://..." --chain ${options.chain} --network ${options.network}`);
    }
    console.log(`  2. Query agent: node scripts/query.js agent <id> --chain ${options.chain} --network ${options.network}`);

  } catch (error) {
    displayError(error, 'Registration');
    process.exit(1);
  }
}

// Show usage if no arguments
if (process.argv.length === 2) {
  console.log('ERC-8004 Multi-Chain Agent Registration');
  console.log('');
  console.log('Usage:');
  console.log('  node register-multichain.js --uri "ipfs://..." --chain tron --network mainnet');
  console.log('  node register-multichain.js --chain bsc --network testnet');
  console.log('');
  console.log('Options:');
  console.log('  --uri <uri>        Agent URI (IPFS hash or URL)');
  console.log('  --chain <name>     Chain: tron, bsc (default: tron)');
  console.log('  --network <name>   Network name (default: nile for tron, testnet for bsc)');
  console.log('  --metadata <k:v>   Metadata key:value pair (can be used multiple times)');
  console.log('');
  console.log('Environment:');
  console.log('  TRON_PRIVATE_KEY   Your wallet private key (required)');
  console.log('  PRIVATE_KEY        Alternative private key variable');
  console.log('');
  console.log('Examples:');
  console.log('  # Register on TRON Nile testnet');
  console.log('  export TRON_PRIVATE_KEY="your_key"');
  console.log('  node register-multichain.js --uri "ipfs://QmHash" --chain tron --network nile');
  console.log('');
  console.log('  # Register on BSC testnet');
  console.log('  node register-multichain.js --uri "ipfs://QmHash" --chain bsc --network testnet');
  console.log('');
  console.log('  # Register on TRON mainnet');
  console.log('  node register-multichain.js --uri "ipfs://QmHash" --chain tron --network mainnet');
  process.exit(0);
}

register();
