/**
 * Sui Agent Wallet - Background Service Worker
 * Communicates with the local agent server via WebSocket
 */

const SERVER_URL = 'ws://localhost:3847/ws';
const HTTP_URL = 'http://localhost:3847';

let ws = null;
let pendingRequests = new Map();
let isConnected = false;

// Connect to local server
const connectWebSocket = () => {
  if (ws && ws.readyState === WebSocket.OPEN) return;
  
  try {
    ws = new WebSocket(SERVER_URL);
    
    ws.onopen = () => {
      console.log('[Sui Agent Wallet] Connected to agent server');
      isConnected = true;
    };
    
    ws.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        
        if (data.requestId && pendingRequests.has(data.requestId)) {
          const { resolve, reject } = pendingRequests.get(data.requestId);
          pendingRequests.delete(data.requestId);
          
          if (data.error) {
            reject(new Error(data.error));
          } else {
            resolve(data.result);
          }
        }
      } catch (e) {
        console.error('[Sui Agent Wallet] Parse error:', e);
      }
    };
    
    ws.onclose = () => {
      console.log('[Sui Agent Wallet] Disconnected from agent server');
      isConnected = false;
      // Reconnect after delay
      setTimeout(connectWebSocket, 3000);
    };
    
    ws.onerror = (error) => {
      console.error('[Sui Agent Wallet] WebSocket error:', error);
    };
  } catch (e) {
    console.error('[Sui Agent Wallet] Failed to connect:', e);
    setTimeout(connectWebSocket, 3000);
  }
};

// Send request to server
const sendRequest = (method, payload, meta = {}) => {
  return new Promise((resolve, reject) => {
    const requestId = `${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    // If WebSocket not available, use HTTP fallback
    if (!ws || ws.readyState !== WebSocket.OPEN) {
      // HTTP fallback
      fetch(`${HTTP_URL}/request`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ requestId, method, payload, ...meta })
      })
        .then(res => res.json())
        .then(data => {
          if (data.error) reject(new Error(data.error));
          else resolve(data.result);
        })
        .catch(reject);
      return;
    }
    
    pendingRequests.set(requestId, { resolve, reject });
    
    ws.send(JSON.stringify({
      requestId,
      method,
      payload,
      ...meta
    }));
    
    // Timeout after 5 minutes
    setTimeout(() => {
      if (pendingRequests.has(requestId)) {
        pendingRequests.delete(requestId);
        reject(new Error('Request timeout - agent did not respond'));
      }
    }, 5 * 60 * 1000);
  });
};

// Handle messages from content scripts
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.type !== 'SUI_AGENT_REQUEST') return false;
  
  const { method, payload, origin, url } = message;
  
  sendRequest(method, payload, { origin, url, tabId: sender.tab?.id })
    .then(result => sendResponse({ result }))
    .catch(error => sendResponse({ error: error.message }));
  
  // Return true to indicate async response
  return true;
});

// Initialize connection
connectWebSocket();

console.log('[Sui Agent Wallet] Background service worker started');
