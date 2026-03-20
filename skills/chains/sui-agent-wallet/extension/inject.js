/**
 * Sui Agent Wallet - Injected Provider
 * Implements Sui Wallet Standard for agent-controlled signing
 */

(function() {
  'use strict';

  const WALLET_NAME = 'Sui Agent Wallet';
  
  // Wallet state
  let connectedAccounts = [];
  let currentNetwork = 'sui:devnet';
  
  // Generate unique request IDs
  let requestCounter = 0;
  const generateRequestId = () => `req_${Date.now()}_${++requestCounter}`;

  // Communication with content script
  const sendToBackground = (type, payload) => {
    return new Promise((resolve, reject) => {
      const requestId = generateRequestId();
      
      const handler = (event) => {
        if (event.data?.type === 'SUI_AGENT_RESPONSE' && event.data?.requestId === requestId) {
          window.removeEventListener('message', handler);
          if (event.data.error) {
            reject(new Error(event.data.error));
          } else {
            resolve(event.data.result);
          }
        }
      };
      
      window.addEventListener('message', handler);
      
      window.postMessage({
        type: 'SUI_AGENT_REQUEST',
        requestId,
        method: type,
        payload
      }, '*');
      
      // Timeout after 5 minutes (agent might take time to review)
      setTimeout(() => {
        window.removeEventListener('message', handler);
        reject(new Error('Request timeout'));
      }, 5 * 60 * 1000);
    });
  };

  // Event listeners storage
  const listeners = new Map();

  // Sui Wallet Standard Features
  const standardConnectFeature = {
    'standard:connect': {
      version: '1.0.0',
      connect: async () => {
        const result = await sendToBackground('connect', {});
        connectedAccounts = result.accounts || [];
        return { accounts: connectedAccounts };
      }
    }
  };

  const standardDisconnectFeature = {
    'standard:disconnect': {
      version: '1.0.0',
      disconnect: async () => {
        connectedAccounts = [];
        await sendToBackground('disconnect', {});
      }
    }
  };

  const standardEventsFeature = {
    'standard:events': {
      version: '1.0.0',
      on: (event, listener) => {
        if (!listeners.has(event)) {
          listeners.set(event, new Set());
        }
        listeners.get(event).add(listener);
        return () => {
          listeners.get(event)?.delete(listener);
        };
      }
    }
  };

  // Helper to serialize transaction
  const serializeTransaction = async (transaction) => {
    // If it's already a string (base64), return as-is
    if (typeof transaction === 'string') {
      return transaction;
    }
    // If it's a Uint8Array, convert to base64
    if (transaction instanceof Uint8Array) {
      return btoa(String.fromCharCode(...transaction));
    }
    // If it has toJSON method (Transaction object from @mysten/sui)
    if (transaction && typeof transaction.toJSON === 'function') {
      const json = await transaction.toJSON();
      return JSON.stringify(json);
    }
    // If it has build method
    if (transaction && typeof transaction.build === 'function') {
      const bytes = await transaction.build();
      return btoa(String.fromCharCode(...bytes));
    }
    // Fallback: try to stringify
    return JSON.stringify(transaction);
  };

  const suiSignTransactionFeature = {
    'sui:signTransaction': {
      version: '2.0.0',
      signTransaction: async (input) => {
        const txData = await serializeTransaction(input.transaction);
        const result = await sendToBackground('signTransaction', {
          transaction: txData,
          chain: input.chain || currentNetwork
        });
        return {
          bytes: result.bytes,
          signature: result.signature
        };
      }
    }
  };

  const suiSignAndExecuteTransactionFeature = {
    'sui:signAndExecuteTransaction': {
      version: '2.0.0',
      signAndExecuteTransaction: async (input) => {
        const txData = await serializeTransaction(input.transaction);
        const result = await sendToBackground('signAndExecuteTransaction', {
          transaction: txData,
          chain: input.chain || currentNetwork,
          options: input.options
        });
        return result;
      }
    }
  };

  const suiSignPersonalMessageFeature = {
    'sui:signPersonalMessage': {
      version: '1.0.0',
      signPersonalMessage: async (input) => {
        const result = await sendToBackground('signPersonalMessage', {
          message: input.message,
          account: input.account
        });
        return {
          bytes: result.bytes,
          signature: result.signature
        };
      }
    }
  };

  // Build the wallet object following Wallet Standard interface
  const wallet = {
    // Required: version
    version: '1.0.0',
    
    // Required: name
    name: WALLET_NAME,
    
    // Required: icon (data URL)
    icon: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiM0ZGE2ZmYiIHN0cm9rZS13aWR0aD0iMiI+PHJlY3QgeD0iMyIgeT0iNiIgd2lkdGg9IjE4IiBoZWlnaHQ9IjEyIiByeD0iMiIvPjxwYXRoIGQ9Ik0zIDEwaDciLz48Y2lyY2xlIGN4PSIxNyIgY3k9IjEyIiByPSIyIi8+PC9zdmc+',
    
    // Required: chains
    chains: ['sui:mainnet', 'sui:testnet', 'sui:devnet', 'sui:localnet'],
    
    // Required: features
    features: {
      ...standardConnectFeature,
      ...standardDisconnectFeature,
      ...standardEventsFeature,
      ...suiSignTransactionFeature,
      ...suiSignAndExecuteTransactionFeature,
      ...suiSignPersonalMessageFeature
    },
    
    // Required: accounts getter
    get accounts() {
      return connectedAccounts.map(acc => ({
        address: acc.address,
        publicKey: new Uint8Array(acc.publicKey),
        chains: acc.chains || ['sui:devnet'],
        features: ['sui:signTransaction', 'sui:signAndExecuteTransaction', 'sui:signPersonalMessage']
      }));
    }
  };

  // Register with Wallet Standard using the correct method
  // Based on @wallet-standard/wallet implementation
  function registerWallet(walletToRegister) {
    const callback = ({ register }) => register(walletToRegister);
    
    try {
      // Try to get the existing wallets API
      (window.navigator.wallets || []).push(callback);
    } catch (e) {
      console.error('[Sui Agent Wallet] Failed to push to navigator.wallets', e);
    }
    
    // Also dispatch the register event for apps that listen for it
    try {
      window.dispatchEvent(new CustomEvent('wallet-standard:register-wallet', {
        detail: callback
      }));
    } catch (e) {
      console.error('[Sui Agent Wallet] Failed to dispatch register event', e);
    }
    
    // Listen for app-ready event (for apps that start after wallet)
    window.addEventListener('wallet-standard:app-ready', ({ detail: api }) => {
      if (api && typeof api.register === 'function') {
        api.register(walletToRegister);
      }
    });
  }

  // Initialize
  registerWallet(wallet);
  
  // Expose for debugging
  window.__suiAgentWallet = wallet;
  
  console.log('[Sui Agent Wallet] Registered with Wallet Standard');
  console.log('[Sui Agent Wallet] Injected and ready');
})();
