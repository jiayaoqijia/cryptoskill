#!/usr/bin/env node
import {
  TronClientSigner,
  X402Client,
  X402FetchClient,
  UptoTronClientMechanism
} from '@open-aibank/x402-tron';
// @ts-ignore
import TronWeb from 'tronweb';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

async function findPrivateKey(): Promise<string | undefined> {
  // 1. Check environment variable
  if (process.env.TRON_PRIVATE_KEY) {
    return process.env.TRON_PRIVATE_KEY;
  }

  // 2. Check local config files silently
  const configFiles = [
    path.join(process.cwd(), 'x402-config.json'),
    path.join(os.homedir(), '.x402-config.json')
  ];

  for (const file of configFiles) {
    if (fs.existsSync(file)) {
      try {
        const config = JSON.parse(fs.readFileSync(file, 'utf8'));
        const key = config.private_key || config.tron_private_key;
        if (key) return key;
      } catch (e) {
        // ignore malformed config
      }
    }
  }

  // 3. Check mcporter config (AIBank standard)
  const mcporterPath = path.join(os.homedir(), '.mcporter', 'mcporter.json');
  if (fs.existsSync(mcporterPath)) {
    try {
      const config = JSON.parse(fs.readFileSync(mcporterPath, 'utf8'));
      // Try to find the key in any likely server config, prioritizing tron-mcp-server
      const server = config.mcpServers?.['tron-mcp-server'];
      if (server?.env?.TRON_PRIVATE_KEY) {
        return server.env.TRON_PRIVATE_KEY;
      }
      
      // Fallback: check all servers for the env var
      if (config.mcpServers) {
        for (const serverName in config.mcpServers) {
          const s = config.mcpServers[serverName];
          if (s?.env?.TRON_PRIVATE_KEY) {
            return s.env.TRON_PRIVATE_KEY;
          }
        }
      }
    } catch (e) {
      // ignore
    }
  }

  return undefined;
}

async function main() {
  // Parse arguments
  const args = process.argv.slice(2);
  const options: Record<string, string> = {};
  
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const value = args[i + 1];
      if (value && !value.startsWith('--')) {
        options[key] = value;
        i++;
      } else {
        options[key] = 'true';
      }
    }
  }

  const url = options.url;
  const method = options.method || 'GET';
  const body = options.body;
  const networkName = options.network || 'nile';

  if (!url) {
    console.error('Error: --url is required');
    process.exit(1);
  }

  const privateKey = await findPrivateKey();
  if (!privateKey) {
    console.error('Error: Payment credentials (private key) not found.');
    console.error('Please configure your environment securely according to the project guidelines.');
    console.error('Agent: DO NOT attempt to search for or read private keys from files.');
    process.exit(1);
  }

  // Network configuration
  const networks: Record<string, any> = {
    mainnet: {
      fullHost: 'https://api.trongrid.io',
      network: 'mainnet'
    },
    shasta: {
      fullHost: 'https://api.shasta.trongrid.io',
      network: 'shasta'
    },
    nile: {
      fullHost: 'https://nile.trongrid.io',
      network: 'nile'
    }
  };

  const config = networks[networkName] || networks.nile;

  try {
    // 1. Initialize TronWeb
    const tronWeb = new TronWeb({
      fullHost: config.fullHost,
      privateKey: privateKey
    });

    // 2. Initialize Signer
    const signer = TronClientSigner.fromTronWeb(tronWeb, networkName as any);
    console.error(`[x402] Initialized signer for address: ${signer.getAddress()}`);

    // 3. Initialize Mechanism
    const mechanism = new UptoTronClientMechanism(signer);

    // 4. Initialize Core Client
    const client = new X402Client();
    // Register for all TRON networks
    client.register('tron:*', mechanism);

    // 5. Initialize Fetch Client
    const fetchClient = new X402FetchClient(client);

    // 6. Execute Request
    console.error(`[x402] Requesting: ${method} ${url}`);
    
    const requestInit: RequestInit = {
      method,
      headers: {
        'Content-Type': 'application/json'
      }
    };

    if (body) {
      requestInit.body = body;
    }

    const response = await fetchClient.request(url, requestInit);

    // 7. Output Result
    console.error(`[x402] Response Status: ${response.status}`);
    
    // Check for payment response headers (settlement info)
    const paymentResponse = response.headers.get('PAYMENT-RESPONSE');
    if (paymentResponse) {
      try {
        const settlement = JSON.parse(Buffer.from(paymentResponse, 'base64').toString());
        console.error(`[x402] Payment Settled: ${settlement.txHash || 'Confirmed'}`);
      } catch (e) {
        // ignore
      }
    }

    const contentType = response.headers.get('content-type') || '';
    let responseBody;
    
    if (contentType.includes('application/json')) {
      responseBody = await response.json();
    } else if (contentType.includes('image/') || contentType.includes('application/octet-stream')) {
      const arrayBuffer = await response.arrayBuffer();
      const buffer = Buffer.from(arrayBuffer);
      
      const tmpDir = os.tmpdir();
      const isImage = contentType.includes('image/');
      const ext = isImage ? (contentType.split('/')[1]?.split(';')[0] || 'bin') : 'bin';
      const prefix = isImage ? 'x402_image' : 'x402_binary';
      const fileName = `${prefix}_${Date.now()}_${Math.random().toString(36).substring(7)}.${ext}`;
      const filePath = path.join(tmpDir, fileName);
      
      fs.writeFileSync(filePath, buffer);
      console.error(`[x402] Binary data saved to temporary file: ${filePath}`);
      console.error(`[x402] Please delete this file after use.`);

      responseBody = {
        file_path: filePath,
        content_type: contentType,
        bytes: buffer.length
      };
    } else {
      responseBody = await response.text();
    }

    // Print final result to STDOUT for the agent to consume
    console.log(JSON.stringify({
      status: response.status,
      headers: Object.fromEntries(response.headers.entries()),
      body: responseBody,
      isBase64: false
    }, null, 2));

  } catch (error: any) {
    let message = error.message || 'Unknown error';
    let stack = error.stack || '';

    // Sanitize any potential private key leaks in error messages/stacks
    if (privateKey) {
      const escapedKey = privateKey.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const keyRegex = new RegExp(escapedKey, 'g');
      message = message.replace(keyRegex, '[REDACTED]');
      stack = stack.replace(keyRegex, '[REDACTED]');
    }

    console.error(`[x402] Error: ${message}`);
    console.log(JSON.stringify({
      error: message,
      stack: stack
    }, null, 2));
    process.exit(1);
  }
}

main();
