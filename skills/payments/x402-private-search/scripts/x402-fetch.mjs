#!/usr/bin/env node
// x402-fetch.mjs — CLI tool for making x402-paid HTTP requests
// Usage: node x402-fetch.mjs <url> [--key <private-key>] [--key-file <path>]
//
// Must be run from the x402-client install dir (where node_modules lives):
//   cd ~/.x402-client && node /path/to/x402-fetch.mjs <url> --key-file wallet.key
//
// Automatically handles 402 Payment Required responses by signing USDC payments.
// Outputs the response body (JSON) to stdout.

import { x402Client, wrapFetchWithPayment } from "@x402/fetch";
import { registerExactEvmScheme } from "@x402/evm/exact/client";
import { privateKeyToAccount } from "viem/accounts";
import { readFileSync } from "fs";

function usage() {
  console.error(`Usage: node x402-fetch.mjs <url> [options]

Options:
  --key <hex>        EVM private key (hex, with or without 0x prefix)
  --key-file <path>  File containing the private key
  --method <GET|POST> HTTP method (default: GET)
  --body <json>      Request body (for POST)
  --header <k:v>     Extra header (repeatable)
  --quiet            Suppress stderr info messages

Environment:
  X402_PRIVATE_KEY   EVM private key (fallback if --key not provided)
  X402_KEY_FILE      Key file path (fallback if --key-file not provided)

Run from the x402-client install dir:
  cd ~/.x402-client && node /path/to/x402-fetch.mjs <url> --key-file wallet.key
`);
  process.exit(1);
}

// Parse args
const args = process.argv.slice(2);
if (args.length === 0 || args[0] === "--help") usage();

const url = args[0];
let privateKey = process.env.X402_PRIVATE_KEY || "";
let keyFile = process.env.X402_KEY_FILE || "";
let method = "GET";
let body = null;
const headers = {};
let quiet = false;

for (let i = 1; i < args.length; i++) {
  switch (args[i]) {
    case "--key": privateKey = args[++i]; break;
    case "--key-file": keyFile = args[++i]; break;
    case "--method": method = args[++i].toUpperCase(); break;
    case "--body": body = args[++i]; break;
    case "--header": {
      const [k, ...v] = args[++i].split(":");
      headers[k.trim()] = v.join(":").trim();
      break;
    }
    case "--quiet": quiet = true; break;
    default:
      console.error(`Unknown option: ${args[i]}`);
      usage();
  }
}

// Load key from file if needed
if (!privateKey && keyFile) {
  privateKey = readFileSync(keyFile, "utf-8").trim();
}

if (!privateKey) {
  console.error("Error: No private key provided. Use --key, --key-file, or X402_PRIVATE_KEY env var.");
  process.exit(1);
}

// Normalize key format
if (!privateKey.startsWith("0x")) privateKey = "0x" + privateKey;

// Create signer and x402 client
const signer = privateKeyToAccount(privateKey);
if (!quiet) console.error(`Wallet: ${signer.address}`);

const client = new x402Client();
registerExactEvmScheme(client, { signer });
const fetchWithPayment = wrapFetchWithPayment(fetch, client);

// Make the request
const fetchOpts = { method, headers };
if (body) fetchOpts.body = body;

if (!quiet) console.error(`${method} ${url}`);

try {
  const response = await fetchWithPayment(url, fetchOpts);
  
  if (!quiet) {
    console.error(`Status: ${response.status}`);
    const paymentResponse = response.headers.get("payment-response");
    if (paymentResponse) console.error("Payment: settled ✓");
  }

  const text = await response.text();
  
  // Try to pretty-print JSON
  try {
    const json = JSON.parse(text);
    console.log(JSON.stringify(json, null, 2));
  } catch {
    console.log(text);
  }

  process.exit(response.ok ? 0 : 1);
} catch (err) {
  console.error(`Error: ${err.message}`);
  process.exit(1);
}
