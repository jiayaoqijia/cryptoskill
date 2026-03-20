#!/usr/bin/env node

/**
 * TRC-8004 Multi-Chain Feedback Script
 * 
 * Submit reputation feedback for agents on TRON or BSC
 * Usage: 
 *   node feedback.js --agent-id 1 --score 95 --tag1 "quality" --chain tron --network mainnet
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
    score: '',
    decimals: 0,
    tag1: '',
    tag2: '',
    endpoint: '',
    uri: '',
    chain: 'tron',
    network: 'nile'
  };

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--agent-id' && args[i + 1]) {
      options.agentId = args[i + 1];
      i++;
    } else if (args[i] === '--score' && args[i + 1]) {
      options.score = args[i + 1];
      i++;
    } else if (args[i] === '--decimals' && args[i + 1]) {
      options.decimals = parseInt(args[i + 1]);
      i++;
    } else if (args[i] === '--tag1' && args[i + 1]) {
      options.tag1 = args[i + 1];
      i++;
    } else if (args[i] === '--tag2' && args[i + 1]) {
      options.tag2 = args[i + 1];
      i++;
    } else if (args[i] === '--endpoint' && args[i + 1]) {
      options.endpoint = args[i + 1];
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

async function submitFeedback() {
  const options = parseArgs();

  if (!options.agentId || !options.score) {
    console.log('TRC-8004 Multi-Chain Feedback Submission');
    console.log('');
    console.log('Usage:');
    console.log('  node feedback.js --agent-id <id> --score <value> [options]');
    console.log('');
    console.log('Required:');
    console.log('  --agent-id <id>      Agent ID to give feedback for');
    console.log('  --score <value>      Feedback score (can be negative)');
    console.log('');
    console.log('Optional:');
    console.log('  --decimals <n>       Decimal places for score (default: 0)');
    console.log('  --tag1 <tag>         Primary tag (e.g., "quality", "uptime")');
    console.log('  --tag2 <tag>         Secondary tag');
    console.log('  --endpoint <url>     Service endpoint');
    console.log('  --uri <uri>          Feedback metadata URI');
    console.log('  --chain <name>       Chain: tron, bsc (default: tron)');
    console.log('  --network <name>     Network name (default: nile)');
    console.log('');
    console.log('Environment:');
    console.log('  TRON_PRIVATE_KEY     Your wallet private key (required)');
    console.log('');
    console.log('Examples:');
    console.log('  # Quality score 95/100 on TRON');
    console.log('  export TRON_PRIVATE_KEY="your_key"');
    console.log('  node feedback.js --agent-id 1 --score 95 --tag1 "quality" --chain tron --network nile');
    console.log('');
    console.log('  # Uptime 99.77% on BSC');
    console.log('  node feedback.js --agent-id 1 --score 9977 --decimals 2 --tag1 "uptime" --chain bsc --network testnet');
    console.log('');
    console.log('  # Negative yield -3.2%');
    console.log('  node feedback.js --agent-id 1 --score -32 --decimals 1 --tag1 "yield" --chain tron --network mainnet');
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
  const contractAddress = networkConfig.contracts.reputationRegistry;

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
    console.log(`⭐ Score: ${options.score}${options.decimals > 0 ? ` (${options.decimals} decimals)` : ''}`);
    if (options.tag1) console.log(`🏷️  Tag1: ${options.tag1}`);
    if (options.tag2) console.log(`🏷️  Tag2: ${options.tag2}`);
    console.log('');

    // Get ABI
    let abi = getAbi(chainConfig, 'reputationRegistry', 'write');

    // Get contract instance
    const contract = await client.getContract(abi, contractAddress);

    // Calculate feedback hash
    const feedbackHash = client.sha3(options.uri || '');

    // Submit feedback
    console.log('📤 Submitting feedback...');
    
    const tx = await client.sendTransaction(
      contract,
      'giveFeedback',
      { feeLimit: 1000000000, value: 0 },
      options.agentId,
      options.score,
      options.decimals,
      options.tag1 || '',
      options.tag2 || '',
      options.endpoint || '',
      options.uri || '',
      feedbackHash
    );

    console.log('');
    console.log('✅ Feedback submitted successfully!');
    console.log('');
    console.log(`📋 Transaction: ${tx}`);
    console.log(`🔍 View on explorer: ${networkConfig.explorer}/#/transaction/${tx}`);
    console.log('');

    // Wait for confirmation
    console.log('⏳ Waiting for confirmation...');
    await sleep(3000);

    console.log('');
    console.log('Next steps:');
    console.log(`  Query reputation: node scripts/query.js reputation ${options.agentId} --chain ${options.chain} --network ${options.network}`);

  } catch (error) {
    displayError(error, 'Feedback Submission');
    process.exit(1);
  }
}

submitFeedback();
