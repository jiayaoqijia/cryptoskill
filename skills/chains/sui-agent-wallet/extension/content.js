/**
 * Sui Agent Wallet - Content Script
 * Bridges between inject.js (page context) and background.js (extension context)
 */

// Inject the wallet provider into the page
const injectScript = () => {
  const script = document.createElement('script');
  script.src = chrome.runtime.getURL('inject.js');
  script.onload = () => script.remove();
  (document.head || document.documentElement).appendChild(script);
};

injectScript();

// Listen for messages from the injected script
window.addEventListener('message', async (event) => {
  if (event.source !== window) return;
  if (event.data?.type !== 'SUI_AGENT_REQUEST') return;
  
  const { requestId, method, payload } = event.data;
  
  try {
    // Forward to background script
    const response = await chrome.runtime.sendMessage({
      type: 'SUI_AGENT_REQUEST',
      method,
      payload,
      origin: window.location.origin,
      url: window.location.href
    });
    
    // Send response back to page
    window.postMessage({
      type: 'SUI_AGENT_RESPONSE',
      requestId,
      result: response.result,
      error: response.error
    }, '*');
  } catch (error) {
    window.postMessage({
      type: 'SUI_AGENT_RESPONSE',
      requestId,
      error: error.message
    }, '*');
  }
});

// Listen for events from background (e.g., account changes)
chrome.runtime.onMessage.addListener((message) => {
  if (message.type === 'SUI_AGENT_EVENT') {
    window.postMessage({
      type: 'SUI_AGENT_EVENT',
      event: message.event,
      data: message.data
    }, '*');
  }
});

console.log('[Sui Agent Wallet] Content script loaded');
