#!/usr/bin/env node

const { ethers } = require("ethers");
const fs = require("fs");
const path = require("path");

// Contract addresses (Avalanche Mainnet)
const IDENTITY_REGISTRY = "0x8004A169FB4a3325136EB29fA0ceB6D2e539a432";
const REPUTATION_REGISTRY = "0x8004BAa17C55a88189AE136b182e5fdA19dE9b63";

// ABIs
const IDENTITY_ABI = [
  "function register() external returns (uint256)",
  "function register(string agentURI) external returns (uint256)",
  "function register(string agentURI, tuple(string metadataKey, bytes metadataValue)[] metadata) external returns (uint256)",
  "function setAgentURI(uint256 agentId, string newURI) external",
  "function setMetadata(uint256 agentId, string metadataKey, bytes metadataValue) external",
  "function getMetadata(uint256 agentId, string metadataKey) external view returns (bytes)",
  "function ownerOf(uint256 tokenId) external view returns (address)",
  "function balanceOf(address owner) external view returns (uint256)",
  "event Transfer(address indexed from, address indexed to, uint256 indexed tokenId)"
];

const TASK_AGENT_ABI = [
  "function owner() external view returns (address)",
  "function agentId() external view returns (uint256)",
  "function isRegistered() external view returns (bool)",
  "function taskPrices(uint256) external view returns (uint256)",
  "function setTaskPrice(uint256 taskId, uint256 price) external"
];

// Load config
function loadConfig() {
  const configPath = path.join(__dirname, "config", "agent.config.js");
  if (!fs.existsSync(configPath)) {
    return null;
  }
  delete require.cache[require.resolve(configPath)];
  return require(configPath);
}

// Load deployment
function loadDeployment() {
  const deployPath = path.join(__dirname, "deployment.json");
  if (!fs.existsSync(deployPath)) {
    return null;
  }
  return JSON.parse(fs.readFileSync(deployPath, "utf8"));
}

// Save deployment
function saveDeployment(data) {
  const deployPath = path.join(__dirname, "deployment.json");
  fs.writeFileSync(deployPath, JSON.stringify(data, null, 2));
}

// Get wallet
function getWallet() {
  require("dotenv").config({ path: path.join(__dirname, ".env") });
  
  const privateKey = process.env.PRIVATE_KEY;
  if (!privateKey) {
    console.error("❌ PRIVATE_KEY not found in .env");
    process.exit(1);
  }
  
  const config = loadConfig();
  const rpc = config?.network?.rpc || "https://api.avax.network/ext/bc/C/rpc";
  const provider = new ethers.JsonRpcProvider(rpc);
  return new ethers.Wallet(privateKey, provider);
}

// Commands
async function init() {
  const configDir = path.join(__dirname, "config");
  const configPath = path.join(configDir, "agent.config.js");
  
  if (!fs.existsSync(configDir)) {
    fs.mkdirSync(configDir, { recursive: true });
  }
  
  if (fs.existsSync(configPath)) {
    console.log("⚠️  Config already exists at config/agent.config.js");
    return;
  }
  
  const template = `module.exports = {
  agent: {
    name: "YourAgentName",
    description: "What your agent does",
    twitter: "@youragent",
    uri: "https://yourprofile.com"
  },
  tasks: {
    types: [
      { id: 0, name: "Research Summary", price: "0.005" },
      { id: 1, name: "Code Review", price: "0.01" },
      { id: 2, name: "Security Analysis", price: "0.02" },
      { id: 3, name: "Custom Task", price: "0.025" }
    ]
  },
  network: {
    rpc: "https://api.avax.network/ext/bc/C/rpc",
    chainId: 43114
  }
};
`;
  
  fs.writeFileSync(configPath, template);
  console.log("✅ Created config/agent.config.js");
  console.log("📝 Edit the config with your agent details");
  console.log("🔑 Create .env with PRIVATE_KEY=your_key");
}

async function deploy() {
  const config = loadConfig();
  if (!config) {
    console.error("❌ No config found. Run: node cli.js init");
    return;
  }
  
  const wallet = getWallet();
  const balance = await wallet.provider.getBalance(wallet.address);
  
  console.log("═".repeat(50));
  console.log("     ERC-8004 Agent Deployment");
  console.log("═".repeat(50));
  console.log("Deployer:", wallet.address);
  console.log("Balance:", ethers.formatEther(balance), "AVAX");
  console.log("");
  
  if (balance < ethers.parseEther("0.05")) {
    console.error("❌ Insufficient balance. Need at least 0.05 AVAX");
    return;
  }
  
  const deployment = loadDeployment() || {};
  
  // Step 1: Register Identity
  if (!deployment.agentId) {
    console.log("1. Registering agent identity...");
    const identity = new ethers.Contract(IDENTITY_REGISTRY, IDENTITY_ABI, wallet);
    
    const tx = await identity["register()"]({ gasLimit: 200000 });
    console.log("   TX:", tx.hash);
    const receipt = await tx.wait();
    
    // Parse agent ID from Transfer event
    const transferLog = receipt.logs.find(l => 
      l.topics[0] === ethers.id("Transfer(address,address,uint256)")
    );
    const agentId = parseInt(transferLog.topics[3], 16);
    
    deployment.agentId = agentId;
    deployment.identityRegistry = IDENTITY_REGISTRY;
    deployment.reputationRegistry = REPUTATION_REGISTRY;
    saveDeployment(deployment);
    
    console.log("   ✅ Registered! Agent ID:", agentId);
  } else {
    console.log("1. Agent already registered. ID:", deployment.agentId);
  }
  
  // Step 2: Deploy ValidationRegistry
  if (!deployment.validationRegistry) {
    console.log("2. Deploying ValidationRegistry...");
    
    const ValidationRegistry = require("./artifacts/ValidationRegistry.json");
    const factory = new ethers.ContractFactory(
      ValidationRegistry.abi,
      ValidationRegistry.bytecode,
      wallet
    );
    const validationRegistry = await factory.deploy();
    await validationRegistry.waitForDeployment();
    
    deployment.validationRegistry = await validationRegistry.getAddress();
    saveDeployment(deployment);
    
    console.log("   ✅ Deployed:", deployment.validationRegistry);
  } else {
    console.log("2. ValidationRegistry exists:", deployment.validationRegistry);
  }
  
  // Step 3: Deploy TaskAgent
  if (!deployment.taskAgent) {
    console.log("3. Deploying TaskAgent...");
    
    const TaskAgent = require("./artifacts/TaskAgent.json");
    const factory = new ethers.ContractFactory(
      TaskAgent.abi,
      TaskAgent.bytecode,
      wallet
    );
    const taskAgent = await factory.deploy(
      IDENTITY_REGISTRY,
      REPUTATION_REGISTRY,
      deployment.validationRegistry
    );
    await taskAgent.waitForDeployment();
    
    deployment.taskAgent = await taskAgent.getAddress();
    saveDeployment(deployment);
    
    console.log("   ✅ Deployed:", deployment.taskAgent);
  } else {
    console.log("3. TaskAgent exists:", deployment.taskAgent);
  }
  
  // Step 4: Set task prices
  console.log("4. Setting task prices...");
  const taskAgent = new ethers.Contract(deployment.taskAgent, TASK_AGENT_ABI, wallet);
  
  for (const task of config.tasks.types) {
    const currentPrice = await taskAgent.taskPrices(task.id);
    const targetPrice = ethers.parseEther(task.price);
    
    if (currentPrice !== targetPrice) {
      const tx = await taskAgent.setTaskPrice(task.id, targetPrice);
      await tx.wait();
      console.log(`   ✅ ${task.name}: ${task.price} AVAX`);
    } else {
      console.log(`   ✓ ${task.name}: ${task.price} AVAX (already set)`);
    }
  }
  
  // Step 5: Set metadata
  console.log("5. Setting metadata...");
  const identity = new ethers.Contract(IDENTITY_REGISTRY, IDENTITY_ABI, wallet);
  
  if (config.agent.uri) {
    const tx = await identity.setAgentURI(deployment.agentId, config.agent.uri, { gasLimit: 100000 });
    await tx.wait();
    console.log("   ✅ URI set");
  }
  
  if (config.agent.name) {
    const tx = await identity.setMetadata(
      deployment.agentId, 
      "name", 
      ethers.toUtf8Bytes(config.agent.name),
      { gasLimit: 100000 }
    );
    await tx.wait();
    console.log("   ✅ Name set:", config.agent.name);
  }
  
  if (config.agent.description) {
    const tx = await identity.setMetadata(
      deployment.agentId,
      "description",
      ethers.toUtf8Bytes(config.agent.description),
      { gasLimit: 150000 }
    );
    await tx.wait();
    console.log("   ✅ Description set");
  }
  
  if (config.agent.twitter) {
    const tx = await identity.setMetadata(
      deployment.agentId,
      "twitter",
      ethers.toUtf8Bytes(config.agent.twitter),
      { gasLimit: 100000 }
    );
    await tx.wait();
    console.log("   ✅ Twitter set:", config.agent.twitter);
  }
  
  deployment.timestamp = new Date().toISOString();
  deployment.network = "avalanche";
  deployment.chainId = 43114;
  saveDeployment(deployment);
  
  console.log("");
  console.log("═".repeat(50));
  console.log("     DEPLOYMENT COMPLETE");
  console.log("═".repeat(50));
  console.log("Agent ID:          ", deployment.agentId);
  console.log("TaskAgent:         ", deployment.taskAgent);
  console.log("ValidationRegistry:", deployment.validationRegistry);
  console.log("");
  console.log("Explorer: https://snowtrace.io/nft/" + IDENTITY_REGISTRY + "/" + deployment.agentId);
  console.log("═".repeat(50));
}

async function setMetadata(key, value) {
  const deployment = loadDeployment();
  if (!deployment?.agentId) {
    console.error("❌ No deployment found. Run: node cli.js deploy");
    return;
  }
  
  const wallet = getWallet();
  const identity = new ethers.Contract(IDENTITY_REGISTRY, IDENTITY_ABI, wallet);
  
  console.log(`Setting ${key} = "${value}"...`);
  const tx = await identity.setMetadata(
    deployment.agentId,
    key,
    ethers.toUtf8Bytes(value),
    { gasLimit: 150000 }
  );
  await tx.wait();
  console.log("✅ Done! TX:", tx.hash);
}

async function setUri(uri) {
  const deployment = loadDeployment();
  if (!deployment?.agentId) {
    console.error("❌ No deployment found. Run: node cli.js deploy");
    return;
  }
  
  const wallet = getWallet();
  const identity = new ethers.Contract(IDENTITY_REGISTRY, IDENTITY_ABI, wallet);
  
  console.log(`Setting URI = "${uri}"...`);
  const tx = await identity.setAgentURI(deployment.agentId, uri, { gasLimit: 100000 });
  await tx.wait();
  console.log("✅ Done! TX:", tx.hash);
}

async function setPrice(taskId, price) {
  const deployment = loadDeployment();
  if (!deployment?.taskAgent) {
    console.error("❌ No TaskAgent found. Run: node cli.js deploy");
    return;
  }
  
  const wallet = getWallet();
  const taskAgent = new ethers.Contract(deployment.taskAgent, TASK_AGENT_ABI, wallet);
  
  console.log(`Setting task ${taskId} price to ${price} AVAX...`);
  const tx = await taskAgent.setTaskPrice(taskId, ethers.parseEther(price));
  await tx.wait();
  console.log("✅ Done! TX:", tx.hash);
}

async function status() {
  const deployment = loadDeployment();
  if (!deployment) {
    console.log("❌ No deployment found.");
    console.log("Run: node cli.js init && node cli.js deploy");
    return;
  }
  
  console.log("═".repeat(50));
  console.log("     ERC-8004 Agent Status");
  console.log("═".repeat(50));
  console.log("Agent ID:          ", deployment.agentId || "Not registered");
  console.log("TaskAgent:         ", deployment.taskAgent || "Not deployed");
  console.log("ValidationRegistry:", deployment.validationRegistry || "Not deployed");
  console.log("Identity Registry: ", IDENTITY_REGISTRY);
  console.log("Reputation Registry:", REPUTATION_REGISTRY);
  console.log("Deployed:          ", deployment.timestamp || "Unknown");
  console.log("");
  
  if (deployment.agentId) {
    console.log("Explorer: https://snowtrace.io/nft/" + IDENTITY_REGISTRY + "/" + deployment.agentId);
  }
  
  if (deployment.taskAgent) {
    console.log("TaskAgent: https://snowtrace.io/address/" + deployment.taskAgent);
  }
  console.log("═".repeat(50));
}

// Main
const command = process.argv[2];
const args = process.argv.slice(3);

switch (command) {
  case "init":
    init();
    break;
  case "deploy":
    deploy().catch(console.error);
    break;
  case "set-metadata":
    if (args.length < 2) {
      console.error("Usage: node cli.js set-metadata <key> <value>");
      process.exit(1);
    }
    setMetadata(args[0], args.slice(1).join(" ")).catch(console.error);
    break;
  case "set-uri":
    if (args.length < 1) {
      console.error("Usage: node cli.js set-uri <uri>");
      process.exit(1);
    }
    setUri(args[0]).catch(console.error);
    break;
  case "set-price":
    if (args.length < 2) {
      console.error("Usage: node cli.js set-price <taskId> <priceAVAX>");
      process.exit(1);
    }
    setPrice(args[0], args[1]).catch(console.error);
    break;
  case "status":
    status().catch(console.error);
    break;
  default:
    console.log("ERC-8004 Identity CLI");
    console.log("");
    console.log("Commands:");
    console.log("  init           Initialize agent config");
    console.log("  deploy         Deploy agent identity");
    console.log("  set-metadata   Set metadata (key value)");
    console.log("  set-uri        Set profile URI");
    console.log("  set-price      Set task price");
    console.log("  status         Show deployment status");
}
