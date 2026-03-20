import { ethers } from "ethers";
import { readFileSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

export const CHAIN_ID = 84532;
export const RPC_URL = "https://sepolia.base.org";
export const EXPLORER_URL = "https://sepolia.basescan.org";

export const ADDRESSES = {
  pool: "0x8bAB6d1b75f19e9eD9fCe8b9BD338844fF79aE27",
  weth: "0x4200000000000000000000000000000000000006",
  usdc: "0xba50Cd2A20f6DA35D788639E581bca8d0B5d4D5f",
  faucet: "0xD9145b5F45Ad4519c7ACcD6E0A4A82e83bB8A6Dc",
};

const CONFIG_LOCATIONS = [
  join(process.cwd(), "x402-config.json"),
  join(homedir(), ".x402-config.json"),
];

export function loadPrivateKey() {
  // Environment variable takes precedence
  if (process.env.X402_PRIVATE_KEY) {
    return process.env.X402_PRIVATE_KEY;
  }

  for (const configPath of CONFIG_LOCATIONS) {
    try {
      const raw = readFileSync(configPath, "utf-8");
      const config = JSON.parse(raw);
      if (config.private_key) {
        return config.private_key;
      }
    } catch {
      // File not found or invalid JSON, try next
    }
  }

  throw new Error(
    'Private key not found. Set X402_PRIVATE_KEY env var or create ~/.x402-config.json with {"private_key": "0x..."}',
  );
}

export function getProvider() {
  return new ethers.JsonRpcProvider(RPC_URL, CHAIN_ID);
}

export function getSigner() {
  const provider = getProvider();
  const privateKey = loadPrivateKey();
  return new ethers.Wallet(privateKey, provider);
}
