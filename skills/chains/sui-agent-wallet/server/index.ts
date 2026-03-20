/**
 * Sui Agent Wallet - Local Control Server
 * 
 * Provides HTTP + WebSocket API for agent to control the wallet
 */

import { AgentWallet, NetworkType } from './wallet';
import { fromBase64, toBase64 } from '@mysten/sui/utils';
import { Transaction } from '@mysten/sui/transactions';

const PORT = 3847;

// Initialize wallet
const wallet = new AgentWallet();
console.log(`Wallet address: ${wallet.getAddress()}`);
console.log(`Network: ${wallet.getNetwork()}`);

// Pending signature requests
interface PendingRequest {
  id: string;
  method: string;
  payload: any;
  origin: string;
  url: string;
  timestamp: number;
  resolved: boolean;
  resolve?: (value: any) => void;
  reject?: (error: Error) => void;
}

const pendingRequests = new Map<string, PendingRequest>();

// WebSocket clients
const wsClients = new Set<any>();

// Broadcast event to all connected extensions
function broadcastEvent(event: string, data: any) {
  const message = JSON.stringify({ type: 'event', event, data });
  for (const ws of wsClients) {
    try {
      ws.send(message);
    } catch (e) {
      // Client disconnected
    }
  }
}

// Parse transaction for display
async function parseTransaction(txBytes: Uint8Array | string): Promise<any> {
  try {
    const bytes = typeof txBytes === 'string' ? fromBase64(txBytes) : txBytes;
    // Basic parsing - in production you'd want more detailed parsing
    return {
      bytesLength: bytes.length,
      bytesBase64: typeof txBytes === 'string' ? txBytes : toBase64(txBytes)
    };
  } catch (e) {
    return { error: 'Failed to parse transaction', raw: txBytes };
  }
}

// HTTP Server
const server = Bun.serve({
  port: PORT,
  
  async fetch(req) {
    const url = new URL(req.url);
    const path = url.pathname;
    
    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type'
    };
    
    if (req.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    // WebSocket upgrade
    if (path === '/ws') {
      const upgraded = server.upgrade(req);
      if (upgraded) return undefined;
      return new Response('WebSocket upgrade failed', { status: 400 });
    }

    // === Agent API ===
    
    // Get wallet address
    if (path === '/address' && req.method === 'GET') {
      return Response.json({
        address: wallet.getAddress(),
        publicKey: toBase64(wallet.getPublicKey()),
        network: wallet.getNetwork()
      }, { headers: corsHeaders });
    }
    
    // Get balance
    if (path === '/balance' && req.method === 'GET') {
      const balance = await wallet.getBalance();
      return Response.json({
        balance,
        balanceSui: (parseInt(balance) / 1_000_000_000).toFixed(9)
      }, { headers: corsHeaders });
    }
    
    // Get pending requests
    if (path === '/pending' && req.method === 'GET') {
      const pending = Array.from(pendingRequests.values())
        .filter(r => !r.resolved)
        .map(r => ({
          id: r.id,
          method: r.method,
          origin: r.origin,
          url: r.url,
          timestamp: r.timestamp,
          payload: r.payload
        }));
      return Response.json({ pending }, { headers: corsHeaders });
    }
    
    // Get specific request details
    if (path.startsWith('/tx/') && req.method === 'GET') {
      const id = path.slice(4);
      const request = pendingRequests.get(id);
      if (!request) {
        return Response.json({ error: 'Request not found' }, { status: 404, headers: corsHeaders });
      }
      
      let parsedTx = null;
      if (request.payload?.transaction) {
        parsedTx = await parseTransaction(request.payload.transaction);
      }
      
      return Response.json({
        ...request,
        parsedTransaction: parsedTx
      }, { headers: corsHeaders });
    }
    
    // Approve request
    if (path.startsWith('/approve/') && req.method === 'POST') {
      const id = path.slice(9);
      const request = pendingRequests.get(id);
      if (!request) {
        return Response.json({ error: 'Request not found' }, { status: 404, headers: corsHeaders });
      }
      if (request.resolved) {
        return Response.json({ error: 'Request already resolved' }, { status: 400, headers: corsHeaders });
      }
      
      try {
        let result;
        let txBytes: Uint8Array;
        
        const txData = request.payload.transaction;
        
        // Handle different transaction formats
        if (typeof txData === 'string') {
          // Check if it's JSON (starts with { or ")
          const trimmed = txData.trim();
          if (trimmed.startsWith('{') || trimmed.startsWith('"')) {
            // It's JSON - parse and rebuild transaction
            const jsonStr = trimmed.startsWith('"') ? JSON.parse(trimmed) : trimmed;
            const txJson = typeof jsonStr === 'string' ? JSON.parse(jsonStr) : jsonStr;
            
            // Build a new transaction from the JSON structure
            const tx = new Transaction();
            tx.setSender(wallet.getAddress());
            
            // Add commands from JSON
            for (const cmd of txJson.commands || []) {
              if (cmd.MoveCall) {
                const mc = cmd.MoveCall;
                tx.moveCall({
                  target: `${mc.package}::${mc.module}::${mc.function}`,
                  typeArguments: mc.typeArguments || [],
                  arguments: (mc.arguments || []).map((arg: any) => {
                    if (arg.Input !== undefined) {
                      // Reference to input
                      const input = txJson.inputs[arg.Input];
                      if (input?.UnresolvedObject) {
                        return tx.object(input.UnresolvedObject.objectId);
                      }
                      if (input?.Pure) {
                        return tx.pure(input.Pure);
                      }
                    }
                    return arg;
                  })
                });
              }
            }
            
            txBytes = await tx.build({ client: wallet.getClient() });
          } else {
            // Assume base64
            txBytes = fromBase64(txData);
          }
        } else {
          txBytes = txData;
        }
        
        if (request.method === 'signTransaction') {
          result = await wallet.signTransaction(txBytes);
        } else if (request.method === 'signAndExecuteTransaction') {
          result = await wallet.signAndExecuteTransaction(txBytes, request.payload.options);
        } else if (request.method === 'signPersonalMessage') {
          const msgBytes = typeof request.payload.message === 'string'
            ? fromBase64(request.payload.message)
            : request.payload.message;
          result = await wallet.signPersonalMessage(msgBytes);
        }
        
        request.resolved = true;
        request.resolve?.(result);
        
        return Response.json({ success: true, result }, { headers: corsHeaders });
      } catch (e: any) {
        return Response.json({ error: e.message }, { status: 500, headers: corsHeaders });
      }
    }
    
    // Reject request
    if (path.startsWith('/reject/') && req.method === 'POST') {
      const id = path.slice(8);
      const request = pendingRequests.get(id);
      if (!request) {
        return Response.json({ error: 'Request not found' }, { status: 404, headers: corsHeaders });
      }
      if (request.resolved) {
        return Response.json({ error: 'Request already resolved' }, { status: 400, headers: corsHeaders });
      }
      
      request.resolved = true;
      request.reject?.(new Error('User rejected the request'));
      
      return Response.json({ success: true }, { headers: corsHeaders });
    }
    
    // === Network Management ===
    
    // Get current network
    if (path === '/network' && req.method === 'GET') {
      return Response.json({ 
        network: wallet.getNetwork(),
        rpcUrl: `https://fullnode.${wallet.getNetwork()}.sui.io:443`
      }, { headers: corsHeaders });
    }
    
    // Switch network
    if (path === '/network' && req.method === 'POST') {
      const body = await req.json() as { network: NetworkType };
      const result = wallet.switchNetwork(body.network);
      
      // Notify connected extensions
      broadcastEvent('networkChanged', { network: result.network });
      
      return Response.json({ 
        success: true, 
        ...result
      }, { headers: corsHeaders });
    }
    
    // === Account Management ===
    
    // Get all accounts
    if (path === '/accounts' && req.method === 'GET') {
      return Response.json({
        accounts: wallet.getAccounts(),
        activeAddress: wallet.getAddress()
      }, { headers: corsHeaders });
    }
    
    // Create new account
    if (path === '/accounts' && req.method === 'POST') {
      const body = await req.json().catch(() => ({})) as { index?: number };
      const result = wallet.createAccount(body.index);
      return Response.json({
        success: true,
        ...result
      }, { headers: corsHeaders });
    }
    
    // Switch account
    if (path === '/accounts/switch' && req.method === 'POST') {
      const body = await req.json() as { index: number };
      const result = wallet.switchAccount(body.index);
      
      // Notify connected extensions
      broadcastEvent('accountChanged', { 
        address: result.address,
        index: result.index
      });
      
      return Response.json({
        success: true,
        ...result
      }, { headers: corsHeaders });
    }
    
    // === Direct Signing (for CLI integration) ===
    
    // Sign raw transaction bytes (for sui client --serialize-unsigned-transaction)
    if (path === '/sign-raw' && req.method === 'POST') {
      try {
        const body = await req.json() as { txBytes: string };
        const txBytes = fromBase64(body.txBytes);
        const result = await wallet.signTransaction(txBytes);
        
        // Return in format compatible with sui client execute-signed-tx
        return Response.json({
          success: true,
          txBytes: result.bytes,
          signature: result.signature,
          // Combined format for execute-signed-tx
          signedTx: `${result.bytes}:${result.signature}`
        }, { headers: corsHeaders });
      } catch (e: any) {
        return Response.json({ error: e.message }, { status: 500, headers: corsHeaders });
      }
    }
    
    // Sign and execute raw transaction bytes
    if (path === '/sign-and-execute' && req.method === 'POST') {
      try {
        const body = await req.json() as { txBytes: string };
        const txBytes = fromBase64(body.txBytes);
        const result = await wallet.signAndExecuteTransaction(txBytes);
        
        return Response.json({
          success: true,
          digest: result.digest,
          effects: result.effects
        }, { headers: corsHeaders });
      } catch (e: any) {
        return Response.json({ error: e.message }, { status: 500, headers: corsHeaders });
      }
    }
    
    // === Seed Phrase Management ===
    
    // Get seed phrase (DANGEROUS - only for backup)
    if (path === '/mnemonic' && req.method === 'GET') {
      return Response.json({
        mnemonic: wallet.getMnemonic(),
        warning: 'NEVER share this with anyone!'
      }, { headers: corsHeaders });
    }
    
    // Import from seed phrase
    if (path === '/import' && req.method === 'POST') {
      const body = await req.json() as { mnemonic: string };
      const result = wallet.importMnemonic(body.mnemonic);
      return Response.json({
        success: true,
        ...result
      }, { headers: corsHeaders });
    }
    
    // === Extension API (HTTP fallback) ===
    
    if (path === '/request' && req.method === 'POST') {
      const body = await req.json() as any;
      const { requestId, method, payload, origin, url } = body;
      
      // Handle connect - return all accounts
      if (method === 'connect') {
        const accounts = wallet.getAccounts().map(acc => ({
          address: acc.address,
          publicKey: Array.from(wallet.getPublicKey()), // TODO: get per-account pubkey
          chains: [`sui:${wallet.getNetwork()}`]
        }));
        return Response.json({
          result: { accounts }
        }, { headers: corsHeaders });
      }
      
      // Handle disconnect
      if (method === 'disconnect') {
        return Response.json({ result: {} }, { headers: corsHeaders });
      }
      
      // Store pending request and wait for agent approval
      const pendingRequest: PendingRequest = {
        id: requestId,
        method,
        payload,
        origin,
        url,
        timestamp: Date.now(),
        resolved: false
      };
      
      // Create a promise that will be resolved when agent approves/rejects
      const resultPromise = new Promise((resolve, reject) => {
        pendingRequest.resolve = resolve;
        pendingRequest.reject = reject;
      });
      
      pendingRequests.set(requestId, pendingRequest);
      
      // Notify via console (agent will poll /pending)
      console.log(`\n🔔 New ${method} request from ${origin}`);
      console.log(`   Request ID: ${requestId}`);
      console.log(`   Approve: curl -X POST http://localhost:${PORT}/approve/${requestId}`);
      console.log(`   Reject:  curl -X POST http://localhost:${PORT}/reject/${requestId}`);
      
      try {
        const result = await resultPromise;
        return Response.json({ result }, { headers: corsHeaders });
      } catch (e: any) {
        return Response.json({ error: e.message }, { headers: corsHeaders });
      }
    }
    
    return new Response('Not found', { status: 404, headers: corsHeaders });
  },
  
  websocket: {
    open(ws) {
      wsClients.add(ws);
      console.log('Extension connected via WebSocket');
    },
    
    async message(ws, message) {
      try {
        const data = JSON.parse(message.toString());
        const { requestId, method, payload, origin, url } = data;
        
        // Handle connect
        if (method === 'connect') {
          ws.send(JSON.stringify({
            requestId,
            result: {
              accounts: [{
                address: wallet.getAddress(),
                publicKey: Array.from(wallet.getPublicKey()),
                chains: [`sui:${wallet.getNetwork()}`]
              }]
            }
          }));
          return;
        }
        
        // Handle disconnect
        if (method === 'disconnect') {
          ws.send(JSON.stringify({ requestId, result: {} }));
          return;
        }
        
        // Store pending request
        const pendingRequest: PendingRequest = {
          id: requestId,
          method,
          payload,
          origin,
          url,
          timestamp: Date.now(),
          resolved: false
        };
        
        const resultPromise = new Promise((resolve, reject) => {
          pendingRequest.resolve = resolve;
          pendingRequest.reject = reject;
        });
        
        pendingRequests.set(requestId, pendingRequest);
        
        console.log(`\n🔔 New ${method} request from ${origin}`);
        console.log(`   Request ID: ${requestId}`);
        
        try {
          const result = await resultPromise;
          ws.send(JSON.stringify({ requestId, result }));
        } catch (e: any) {
          ws.send(JSON.stringify({ requestId, error: e.message }));
        }
      } catch (e) {
        console.error('WebSocket message error:', e);
      }
    },
    
    close(ws) {
      wsClients.delete(ws);
      console.log('Extension disconnected');
    }
  }
});

console.log(`\n🚀 Sui Agent Wallet Server running on http://localhost:${PORT}`);
console.log(`   WebSocket: ws://localhost:${PORT}/ws`);
console.log(`\nWallet Info:`);
console.log(`   Address: ${wallet.getAddress()}`);
console.log(`   Network: ${wallet.getNetwork()}`);
console.log(`   Accounts: ${wallet.getAccounts().length}`);
console.log(`\nAPI Endpoints:`);
console.log(`   GET  /address        - Get active wallet address`);
console.log(`   GET  /balance        - Get SUI balance`);
console.log(`   GET  /accounts       - List all accounts`);
console.log(`   POST /accounts       - Create new account`);
console.log(`   POST /accounts/switch - Switch active account`);
console.log(`   GET  /network        - Get current network`);
console.log(`   POST /network        - Switch network`);
console.log(`   GET  /mnemonic       - Get seed phrase (backup)`);
console.log(`   POST /import         - Import from seed phrase`);
console.log(`   GET  /pending        - List pending signature requests`);
console.log(`   GET  /tx/:id         - Get request details`);
console.log(`   POST /approve/:id    - Approve a request`);
console.log(`   POST /reject/:id     - Reject a request`);
