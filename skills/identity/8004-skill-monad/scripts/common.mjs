import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import {
  createPublicClient,
  createWalletClient,
  defineChain,
  getAddress,
  http,
  parseAbi,
  parseEther,
} from "viem";
import { privateKeyToAccount } from "viem/accounts";

export const MAINNET_IDENTITY = "0x8004A169FB4a3325136EB29fA0ceB6D2e539a432";
export const TESTNET_IDENTITY = "0x8004A818BFB912233c491871b3d84c89A494BD9e";

export const NETWORKS = {
  "ethereum-mainnet": { chainId: 1, registry: MAINNET_IDENTITY },
  "ethereum-sepolia": { chainId: 11155111, registry: TESTNET_IDENTITY },
  "base-mainnet": { chainId: 8453, registry: MAINNET_IDENTITY },
  "base-sepolia": { chainId: 84532, registry: TESTNET_IDENTITY },
  "polygon-mainnet": { chainId: 137, registry: MAINNET_IDENTITY },
  "polygon-amoy": { chainId: 80002, registry: TESTNET_IDENTITY },
  "monad-mainnet": { chainId: 143, registry: MAINNET_IDENTITY },
  "monad-testnet": { chainId: 10143, registry: TESTNET_IDENTITY },
  "bsc-mainnet": { chainId: 56, registry: MAINNET_IDENTITY },
  "bsc-testnet": { chainId: 97, registry: TESTNET_IDENTITY },
};

export const IDENTITY_ABI = parseAbi([
  "function register() external returns (uint256 agentId)",
  "function register(string agentURI) external returns (uint256 agentId)",
  "function setAgentURI(uint256 agentId, string newURI) external",
  "function ownerOf(uint256 tokenId) external view returns (address)",
  "function tokenURI(uint256 tokenId) external view returns (string)",
  "function getAgentWallet(uint256 agentId) external view returns (address)",
  "event Registered(uint256 indexed agentId, string agentURI, address indexed owner)",
]);

export function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("--")) continue;
    const key = token.slice(2);
    const next = argv[i + 1];
    if (!next || next.startsWith("--")) {
      args[key] = true;
      continue;
    }
    args[key] = next;
    i += 1;
  }
  return args;
}

export function requiredEnv(name) {
  const value = process.env[name];
  if (!value || value.trim() === "") throw new Error(`Missing required env var: ${name}`);
  return value.trim();
}

export function resolveNetwork(args = {}) {
  const envChainId = Number(process.env.MONAD_CHAIN_ID ?? "143");
  const networkName = args.network ?? "monad-mainnet";
  const fromMap = NETWORKS[networkName];
  const chainId = args.chainId ? Number(args.chainId) : fromMap?.chainId ?? envChainId;
  const rpcUrl = args.rpcUrl ?? process.env.MONAD_RPC_URL;
  if (!rpcUrl) throw new Error("Missing RPC URL. Pass --rpcUrl or set MONAD_RPC_URL.");
  const registry = getAddress(args.registry ?? fromMap?.registry ?? MAINNET_IDENTITY);
  return { networkName, chainId, rpcUrl, registry };
}

export function createClients(params) {
  const account = privateKeyToAccount(requiredEnv("AGENT_PRIVATE_KEY"));
  const chain = defineChain({
    id: params.chainId,
    name: params.networkName,
    nativeCurrency: { name: "MON", symbol: "MON", decimals: 18 },
    rpcUrls: { default: { http: [params.rpcUrl] } },
  });
  const transport = http(params.rpcUrl);
  const publicClient = createPublicClient({ chain, transport });
  const walletClient = createWalletClient({ chain, transport, account });
  return { account, publicClient, walletClient, chain };
}

export function agentRegistryId(chainId, registry) {
  return `eip155:${chainId}:${getAddress(registry)}`;
}

export function parseMonToWei(value) {
  return parseEther(String(value));
}

export async function readJsonFile(filePath) {
  const raw = await readFile(resolve(filePath), "utf-8");
  return JSON.parse(raw);
}

export async function writeJsonFile(filePath, value) {
  await writeFile(resolve(filePath), `${JSON.stringify(value, null, 2)}\n`, "utf-8");
}

export async function writeTextFile(filePath, content) {
  await writeFile(resolve(filePath), content, "utf-8");
}
