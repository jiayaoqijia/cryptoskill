#!/usr/bin/env node
/**
 * WalletConnect Requester - Secure DApp Client for AI Agents
 * 
 * This script implements WalletConnect v2 as a DApp (Proposer),
 * meaning it NEVER handles private keys. All transactions must be
 * approved by the user in their wallet.
 * 
 * Security Model:
 * - Agent acts as DApp (Requester)
 * - User wallet acts as Signer (Responder)
 * - Private keys never leave user's wallet
 * - Every transaction requires user approval
 * 
 * Usage:
 *   node wc-requester.js connect
 *   node wc-requester.js request-tx --to 0x... --data 0x... --chain 8453
 *   node wc-requester.js request-sign --message "hello" --chain 8453
 *   node wc-requester.js sessions
 *   node wc-requester.js disconnect --topic <topic>
 */

const { SignClient } = require('@walletconnect/sign-client');
const { WalletConnectError } = require('@walletconnect/utils');
const readline = require('readline');
const fs = require('fs');
const path = require('path');
const QRCode = require('qrcode');

// ============================================================================
// Configuration
// ============================================================================

const CONFIG_DIR = path.join(process.env.HOME, '.walletconnect-requester');
const SESSIONS_FILE = path.join(CONFIG_DIR, 'sessions.json');
const AUDIT_LOG = path.join(CONFIG_DIR, 'audit.log');

// Default metadata
const DEFAULT_METADATA = {
  name: process.env.WC_METADATA_NAME || 'AI Agent Requester',
  description: 'Secure WalletConnect client for AI agents - Zero custody, user controlled',
  url: process.env.WC_METADATA_URL || 'https://github.com/openclaw',
  icons: process.env.WC_METADATA_ICONS?.split(',') || ['https://avatars.githubusercontent.com/u/1234567']
};

// Default namespaces
const DEFAULT_NAMESPACES = {
  eip155: {
    chains: ['eip155:8453', 'eip155:1'],  // Base, Ethereum
    methods: ['eth_sendTransaction', 'personal_sign', 'eth_signTypedData_v4'],
    events: ['accountsChanged', 'chainChanged']
  }
};

// ============================================================================
// Utilities
// ============================================================================

function ensureConfigDir() {
  if (!fs.existsSync(CONFIG_DIR)) {
    fs.mkdirSync(CONFIG_DIR, { recursive: true });
  }
}

function loadSessions() {
  ensureConfigDir();
  if (fs.existsSync(SESSIONS_FILE)) {
    return JSON.parse(fs.readFileSync(SESSIONS_FILE, 'utf8'));
  }
  return {};
}

function saveSessions(sessions) {
  ensureConfigDir();
  fs.writeFileSync(SESSIONS_FILE, JSON.stringify(sessions, null, 2));
}

function logAudit(entry) {
  ensureConfigDir();
  const logEntry = {
    timestamp: new Date().toISOString(),
    ...entry
  };
  fs.appendFileSync(AUDIT_LOG, JSON.stringify(logEntry) + '\n');
}

function maskAddress(address) {
  if (!address) return address;
  return `${address.slice(0, 6)}...${address.slice(-4)}`;
}

async function generateQRCode(uri, outputPath) {
  await QRCode.toFile(outputPath, uri, {
    width: 400,
    margin: 2
  });
  return outputPath;
}

// ============================================================================
// WalletConnect Client
// ============================================================================

class WalletConnectRequester {
  constructor() {
    this.client = null;
    this.projectId = process.env.WC_PROJECT_ID;
    
    if (!this.projectId) {
      console.error('Error: WC_PROJECT_ID environment variable is required.');
      console.error('Get your project ID at: https://cloud.walletconnect.com');
      process.exit(1);
    }
  }

  async init() {
    this.client = await SignClient.init({
      projectId: this.projectId,
      metadata: DEFAULT_METADATA
    });

    // Set up event listeners
    this.client.on('session_delete', ({ topic }) => {
      const sessions = loadSessions();
      delete sessions[topic];
      saveSessions(sessions);
      console.log(`\nSession ${maskAddress(topic)} disconnected by user.`);
    });

    this.client.on('session_expire', ({ topic }) => {
      const sessions = loadSessions();
      delete sessions[topic];
      saveSessions(sessions);
      console.log(`\nSession ${maskAddress(topic)} expired.`);
    });

    return this.client;
  }

  async connect(options = {}) {
    const chains = options.chains || ['8453', '1'];
    const methods = options.methods || ['eth_sendTransaction', 'personal_sign'];
    
    // Build namespaces
    const namespaces = {
      eip155: {
        chains: chains.map(id => `eip155:${id}`),
        methods: methods,
        events: ['accountsChanged', 'chainChanged']
      }
    };

    const { uri, approval } = await this.client.connect({
      requiredNamespaces: namespaces
    });

    console.log('\n' + '='.repeat(60));
    console.log('WalletConnect URI:');
    console.log('='.repeat(60));
    console.log(uri);
    console.log('='.repeat(60));

    // Generate QR code if requested
    if (options.qr) {
      await generateQRCode(uri, options.qr);
      console.log(`\nQR code saved to: ${options.qr}`);
    }

    console.log('\n📱 Scan this URI with your wallet (MetaMask, Rainbow, etc.)');
    console.log('⏳ Waiting for connection...\n');

    try {
      const session = await approval();
      
      // Save session
      const sessions = loadSessions();
      sessions[session.topic] = {
        topic: session.topic,
        peer: session.peer.metadata,
        accounts: session.namespaces.eip155.accounts,
        expiry: session.expiry,
        connectedAt: new Date().toISOString()
      };
      saveSessions(sessions);

      console.log('✅ Connected successfully!');
      console.log(`   Wallet: ${session.peer.metadata.name}`);
      console.log(`   Accounts: ${session.namespaces.eip155.accounts.map(a => maskAddress(a.split(':')[2])).join(', ')}`);
      
      logAudit({
        action: 'session_connected',
        topic: session.topic,
        peer: session.peer.metadata.name
      });

      return session;
    } catch (error) {
      console.error('❌ Connection failed:', error.message);
      logAudit({
        action: 'session_connect_failed',
        error: error.message
      });
      throw error;
    }
  }

  async requestTransaction(options) {
    const { to, data, value, chainId, from } = options;
    const sessions = loadSessions();
    const sessionTopics = Object.keys(sessions);

    if (sessionTopics.length === 0) {
      console.error('❌ No active session. Run "connect" first.');
      return null;
    }

    // Use first active session (or prompt if multiple)
    let topic = sessionTopics[0];
    if (sessionTopics.length > 1) {
      console.log('Multiple sessions available. Use --topic to specify.');
      sessionTopics.forEach((t, i) => {
        console.log(`  ${i + 1}. ${sessions[t].peer?.name || maskAddress(t)}`);
      });
      return null;
    }

    const session = this.client.session.get(topic);
    if (!session) {
      console.error('❌ Session not found. It may have expired.');
      delete sessions[topic];
      saveSessions(sessions);
      return null;
    }

    // Get the account for the specified chain
    const chainAccounts = session.namespaces.eip155.accounts
      .filter(a => a.startsWith(`eip155:${chainId}:`));
    
    if (chainAccounts.length === 0) {
      console.error(`❌ No account available for chain ${chainId}`);
      return null;
    }

    const accountAddress = from || chainAccounts[0].split(':')[2];

    const tx = {
      from: accountAddress,
      to: to,
      data: data || '0x',
      value: value || '0x0'
    };

    console.log('\n📤 Requesting transaction...');
    console.log(`   Chain: ${chainId}`);
    console.log(`   From: ${maskAddress(tx.from)}`);
    console.log(`   To: ${maskAddress(tx.to)}`);
    console.log(`   Value: ${tx.value}`);
    console.log(`   Data: ${tx.data.slice(0, 30)}...`);
    console.log('\n⏳ Waiting for user approval in wallet...\n');

    logAudit({
      action: 'transaction_request',
      topic: topic,
      chain: chainId,
      to: maskAddress(to),
      value: value
    });

    try {
      const result = await this.client.request({
        topic: topic,
        chainId: `eip155:${chainId}`,
        request: {
          method: 'eth_sendTransaction',
          params: [tx]
        }
      });

      console.log('✅ Transaction approved and submitted!');
      console.log(`   TX Hash: ${result}`);
      
      logAudit({
        action: 'transaction_approved',
        topic: topic,
        tx_hash: result
      });

      return result;
    } catch (error) {
      if (error.message?.includes('User rejected')) {
        console.log('❌ User rejected the transaction.');
        logAudit({
          action: 'transaction_rejected',
          topic: topic
        });
      } else {
        console.error('❌ Transaction failed:', error.message);
        logAudit({
          action: 'transaction_failed',
          topic: topic,
          error: error.message
        });
      }
      throw error;
    }
  }

  async requestSignature(options) {
    const { message, typedData, chainId, from } = options;
    const sessions = loadSessions();
    const sessionTopics = Object.keys(sessions);

    if (sessionTopics.length === 0) {
      console.error('❌ No active session. Run "connect" first.');
      return null;
    }

    let topic = sessionTopics[0];
    const session = this.client.session.get(topic);
    
    if (!session) {
      console.error('❌ Session not found.');
      return null;
    }

    const chainAccounts = session.namespaces.eip155.accounts
      .filter(a => a.startsWith(`eip155:${chainId}:`));
    
    if (chainAccounts.length === 0) {
      console.error(`❌ No account available for chain ${chainId}`);
      return null;
    }

    const accountAddress = from || chainAccounts[0].split(':')[2];

    console.log('\n📤 Requesting signature...');
    console.log(`   Chain: ${chainId}`);
    console.log(`   Account: ${maskAddress(accountAddress)}`);
    if (message) {
      console.log(`   Message: ${message.slice(0, 50)}${message.length > 50 ? '...' : ''}`);
    }
    console.log('\n⏳ Waiting for user approval in wallet...\n');

    logAudit({
      action: 'signature_request',
      topic: topic,
      chain: chainId,
      account: maskAddress(accountAddress)
    });

    try {
      let result;
      
      if (typedData) {
        result = await this.client.request({
          topic: topic,
          chainId: `eip155:${chainId}`,
          request: {
            method: 'eth_signTypedData_v4',
            params: [accountAddress, typedData]
          }
        });
      } else {
        result = await this.client.request({
          topic: topic,
          chainId: `eip155:${chainId}`,
          request: {
            method: 'personal_sign',
            params: [message, accountAddress]
          }
        });
      }

      console.log('✅ Signature obtained!');
      console.log(`   Signature: ${result.slice(0, 30)}...`);
      
      logAudit({
        action: 'signature_approved',
        topic: topic
      });

      return result;
    } catch (error) {
      if (error.message?.includes('User rejected')) {
        console.log('❌ User rejected the signature request.');
        logAudit({
          action: 'signature_rejected',
          topic: topic
        });
      } else {
        console.error('❌ Signature failed:', error.message);
      }
      throw error;
    }
  }

  listSessions() {
    const sessions = loadSessions();
    const topics = Object.keys(sessions);

    if (topics.length === 0) {
      console.log('No active sessions.');
      console.log('Run "connect" to create a new session.');
      return;
    }

    console.log('\n' + '='.repeat(60));
    console.log('Active Sessions');
    console.log('='.repeat(60));

    topics.forEach((topic, i) => {
      const session = sessions[topic];
      console.log(`\n${i + 1}. Topic: ${maskAddress(topic)}`);
      console.log(`   Wallet: ${session.peer?.name || 'Unknown'}`);
      console.log(`   Accounts: ${session.accounts?.map(a => maskAddress(a.split(':')[2])).join(', ')}`);
      console.log(`   Connected: ${session.connectedAt}`);
      console.log(`   Expires: ${new Date(session.expiry * 1000).toISOString()}`);
    });
    console.log('\n' + '='.repeat(60));
  }

  async disconnect(topic) {
    const sessions = loadSessions();

    if (!topic) {
      const topics = Object.keys(sessions);
      if (topics.length === 0) {
        console.log('No active sessions to disconnect.');
        return;
      }
      topic = topics[0];
      console.log(`Disconnecting: ${maskAddress(topic)}`);
    }

    try {
      await this.client.disconnect({
        topic: topic,
        reason: {
          code: 6000,
          message: 'User disconnected'
        }
      });
    } catch (e) {
      // Session might already be disconnected
    }

    delete sessions[topic];
    saveSessions(sessions);

    console.log('✅ Session disconnected.');
    logAudit({
      action: 'session_disconnected',
      topic: topic
    });
  }
}

// ============================================================================
// CLI
// ============================================================================

function printHelp() {
  console.log(`
WalletConnect Requester - Secure DApp Client for AI Agents

Usage:
  node wc-requester.js <command> [options]

Commands:
  connect               Create a new WalletConnect session
  request-tx            Request a transaction (user must approve)
  request-sign          Request a signature (user must approve)
  sessions              List active sessions
  disconnect            End a session

Options:
  connect:
    --chains <ids>      Comma-separated chain IDs (default: 8453,1)
    --methods <list>    Comma-separated methods (default: eth_sendTransaction,personal_sign)
    --qr <path>         Generate QR code to file
    --json              Output as JSON

  request-tx:
    --to <address>      Recipient address (required)
    --data <hex>        Transaction data (default: 0x)
    --value <wei>       Value in wei (default: 0)
    --chain <id>        Chain ID (default: 8453)
    --from <address>    Sender address (optional, uses first available)

  request-sign:
    --message <text>    Message to sign (for personal_sign)
    --typed-data <json> Typed data to sign (for eth_signTypedData_v4)
    --chain <id>        Chain ID (default: 8453)
    --from <address>    Signer address (optional)

  disconnect:
    --topic <topic>     Session topic to disconnect (optional, uses first)

Environment Variables:
  WC_PROJECT_ID         WalletConnect Cloud Project ID (required)
  WC_METADATA_NAME      DApp name shown in wallet
  WC_METADATA_URL       DApp URL
  WC_METADATA_ICONS     DApp icon URLs (comma-separated)

Examples:
  # Connect to wallet
  WC_PROJECT_ID=xxx node wc-requester.js connect --qr wallet.png

  # Request USDC transfer
  node wc-requester.js request-tx \\
    --to 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 \\
    --data 0xa9059cbb... \\
    --chain 8453

  # Request signature
  node wc-requester.js request-sign \\
    --message "Verify ownership" \\
    --chain 1
`);
}

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || command === '--help' || command === '-h') {
    printHelp();
    process.exit(0);
  }

  // Parse options
  const options = {};
  for (let i = 1; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].slice(2).replace(/-/g, '_');
      const value = args[i + 1] && !args[i + 1].startsWith('--') ? args[i + 1] : true;
      options[key] = value;
      if (value !== true) i++;
    }
  }

  const requester = new WalletConnectRequester();
  await requester.init();

  switch (command) {
    case 'connect':
      await requester.connect({
        chains: options.chains?.split(','),
        methods: options.methods?.split(','),
        qr: options.qr
      });
      break;

    case 'request-tx':
      if (!options.to) {
        console.error('Error: --to is required for request-tx');
        process.exit(1);
      }
      await requester.requestTransaction({
        to: options.to,
        data: options.data,
        value: options.value,
        chainId: options.chain || '8453',
        from: options.from
      });
      break;

    case 'request-sign':
      if (!options.message && !options.typed_data) {
        console.error('Error: --message or --typed-data is required for request-sign');
        process.exit(1);
      }
      await requester.requestSignature({
        message: options.message,
        typedData: options.typed_data,
        chainId: options.chain || '8453',
        from: options.from
      });
      break;

    case 'sessions':
      requester.listSessions();
      break;

    case 'disconnect':
      await requester.disconnect(options.topic);
      break;

    default:
      console.error(`Unknown command: ${command}`);
      printHelp();
      process.exit(1);
  }
}

main().catch(console.error);