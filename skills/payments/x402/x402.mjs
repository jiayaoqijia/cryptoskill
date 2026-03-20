/**
 * x402 Protocol Implementation
 * 
 * HTTP 402 payment protocol for machine-to-machine USDC payments on Base.
 * 
 * Usage:
 *   import { x402Fetch } from './x402.mjs';
 *   const response = await x402Fetch(account, url);
 * 
 * Author: Lumen (https://x.com/LumenFTFuture)
 * License: MIT
 */

// Supported networks
export const SUPPORTED_NETWORKS = {
  "eip155:8453": {
    chainId: 8453,
    name: "Base",
    usdcAddress: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
  },
  "eip155:84532": {
    chainId: 84532,
    name: "Base Sepolia",
    usdcAddress: "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
  },
};

/**
 * Parse x402 payment requirements from a 402 response
 */
export async function parsePaymentRequired(response) {
  // Try X-Payment-Required header first
  const header = response.headers.get("X-Payment-Required");
  if (header) {
    try {
      // Try direct JSON parse
      const parsed = JSON.parse(header);
      if (parsed.accepts) return parsed;
    } catch {
      // Try base64 decode
      try {
        const decoded = atob(header);
        const parsed = JSON.parse(decoded);
        if (parsed.accepts) return parsed;
      } catch {}
    }
  }
  
  // Try JSON body
  try {
    const body = await response.clone().json();
    if (body.accepts) return body;
  } catch {}
  
  return null;
}

/**
 * Create EIP-3009 transferWithAuthorization signature
 */
export async function createPaymentSignature(account, requirement, x402Version = 1) {
  const network = SUPPORTED_NETWORKS[requirement.network];
  if (!network) {
    throw new Error(`Unsupported network: ${requirement.network}`);
  }
  
  // Generate random nonce
  const nonce = `0x${Buffer.from(crypto.getRandomValues(new Uint8Array(32))).toString("hex")}`;
  
  // Calculate timestamps
  const now = Math.floor(Date.now() / 1000);
  const validAfter = BigInt(now - 60);
  const validBefore = BigInt(now + (requirement.maxTimeoutSeconds || requirement.requiredDeadlineSeconds || 300));
  
  // Parse amount
  const maxAmount = requirement.maxAmountRequired;
  let value;
  if (typeof maxAmount === "string" && maxAmount.includes(".")) {
    // Decimal format (e.g., "5.00")
    value = BigInt(Math.floor(parseFloat(maxAmount) * 1e6));
  } else if (x402Version >= 2 || String(maxAmount).length > 6) {
    // Already in base units
    value = BigInt(maxAmount);
  } else {
    // Legacy: whole token amount
    value = BigInt(maxAmount) * BigInt(1e6);
  }
  
  // Authorization struct
  const authorization = {
    from: account.address,
    to: requirement.payTo || requirement.payToAddress,
    value,
    validAfter,
    validBefore,
    nonce,
  };
  
  // EIP-712 domain
  const domain = {
    name: requirement.extra?.name || "USD Coin",
    version: requirement.extra?.version || "2",
    chainId: network.chainId,
    verifyingContract: requirement.asset || requirement.usdcAddress,
  };
  
  // EIP-712 types
  const types = {
    TransferWithAuthorization: [
      { name: "from", type: "address" },
      { name: "to", type: "address" },
      { name: "value", type: "uint256" },
      { name: "validAfter", type: "uint256" },
      { name: "validBefore", type: "uint256" },
      { name: "nonce", type: "bytes32" },
    ],
  };
  
  // Sign
  const signature = await account.signTypedData({
    domain,
    types,
    primaryType: "TransferWithAuthorization",
    message: authorization,
  });
  
  return {
    x402Version: 1,
    scheme: requirement.scheme,
    network: requirement.network,
    payload: {
      signature,
      authorization,
    },
  };
}

/**
 * Encode payment payload as X-Payment header value
 */
export function encodePaymentHeader(payment) {
  const serializable = {
    ...payment,
    payload: {
      ...payment.payload,
      authorization: {
        ...payment.payload.authorization,
        value: payment.payload.authorization.value.toString(),
        validAfter: payment.payload.authorization.validAfter.toString(),
        validBefore: payment.payload.authorization.validBefore.toString(),
      },
    },
  };
  return btoa(JSON.stringify(serializable));
}

/**
 * Fetch with automatic x402 payment handling
 */
export async function x402Fetch(account, url, options = {}) {
  // Initial request
  const response = await fetch(url, options);
  
  if (response.status !== 402) {
    return response;
  }
  
  // Parse payment requirements
  const requirements = await parsePaymentRequired(response);
  if (!requirements) {
    throw new Error("Received 402 but could not parse payment requirements");
  }
  
  // Find supported payment option
  const requirement = requirements.accepts.find(
    r => r.scheme === "exact" && SUPPORTED_NETWORKS[r.network]
  );
  
  if (!requirement) {
    throw new Error("No supported payment options found");
  }
  
  // Create and sign payment
  const payment = await createPaymentSignature(account, requirement, requirements.x402Version);
  
  // Retry with payment header
  const paidResponse = await fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      "X-Payment": encodePaymentHeader(payment),
    },
  });
  
  return paidResponse;
}

/**
 * Check if a URL requires x402 payment
 */
export async function checkX402(url, method = "GET") {
  const response = await fetch(url, { method });
  
  if (response.status === 402) {
    const requirements = await parsePaymentRequired(response);
    return { requiresPayment: true, requirements };
  }
  
  return { requiresPayment: false };
}
