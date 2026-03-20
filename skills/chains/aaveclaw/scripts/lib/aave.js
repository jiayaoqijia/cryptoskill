import { ethers } from "ethers";
import { ADDRESSES, getSigner, getProvider } from "./config.js";
import { txLink, printAccountSummary } from "./utils.js";

// Human-readable ABI fragments for Aave V3 Pool
const POOL_ABI = [
  "function supply(address asset, uint256 amount, address onBehalfOf, uint16 referralCode)",
  "function borrow(address asset, uint256 amount, uint256 interestRateMode, uint16 referralCode, address onBehalfOf)",
  "function repay(address asset, uint256 amount, uint256 interestRateMode, address onBehalfOf) returns (uint256)",
  "function withdraw(address asset, uint256 amount, address to) returns (uint256)",
  "function getUserAccountData(address user) view returns (uint256 totalCollateralBase, uint256 totalDebtBase, uint256 availableBorrowsBase, uint256 currentLiquidationThreshold, uint256 ltv, uint256 healthFactor)",
];

const ERC20_ABI = [
  "function balanceOf(address owner) view returns (uint256)",
  "function allowance(address owner, address spender) view returns (uint256)",
  "function approve(address spender, uint256 amount) returns (bool)",
  "function decimals() view returns (uint8)",
];

const WETH_ABI = [...ERC20_ABI, "function deposit() payable"];

const FAUCET_ABI = ["function mint(address token, address to, uint256 amount)"];

// Variable rate mode (stable rate is deprecated in Aave V3)
const VARIABLE_RATE = 2;

async function ensureAllowance(tokenContract, spender, amount, signer) {
  const current = await tokenContract.allowance(signer.address, spender);
  if (current < amount) {
    console.log("Approving token spend...");
    const tx = await tokenContract.approve(spender, ethers.MaxUint256);
    await tx.wait();
    console.log(`Approval tx: ${txLink(tx.hash)}`);
  }
}

export async function getAccountData(address) {
  const provider = getProvider();
  const pool = new ethers.Contract(ADDRESSES.pool, POOL_ABI, provider);
  const result = await pool.getUserAccountData(address);
  return {
    totalCollateralBase: result[0],
    totalDebtBase: result[1],
    availableBorrowsBase: result[2],
    currentLiquidationThreshold: result[3],
    ltv: result[4],
    healthFactor: result[5],
  };
}

export async function deposit(amountEth) {
  const signer = getSigner();
  const amount = ethers.parseEther(amountEth);

  const weth = new ethers.Contract(ADDRESSES.weth, WETH_ABI, signer);
  const pool = new ethers.Contract(ADDRESSES.pool, POOL_ABI, signer);

  // Check WETH balance, auto-wrap ETH if needed
  const wethBalance = await weth.balanceOf(signer.address);
  if (wethBalance < amount) {
    const shortfall = amount - wethBalance;
    const ethBalance = await signer.provider.getBalance(signer.address);
    if (ethBalance < shortfall) {
      throw new Error(
        `Insufficient balance. Need ${ethers.formatEther(shortfall)} more WETH (or native ETH to wrap). ` +
          `WETH balance: ${ethers.formatEther(wethBalance)}, ETH balance: ${ethers.formatEther(ethBalance)}`,
      );
    }
    console.log(`Wrapping ${ethers.formatEther(shortfall)} ETH to WETH...`);
    const wrapTx = await weth.deposit({ value: shortfall });
    await wrapTx.wait();
    console.log(`Wrap tx: ${txLink(wrapTx.hash)}`);
  }

  // Approve Pool to spend WETH
  await ensureAllowance(weth, ADDRESSES.pool, amount, signer);

  // Supply WETH to Aave
  console.log(`Depositing ${amountEth} WETH as collateral...`);
  const tx = await pool.supply(ADDRESSES.weth, amount, signer.address, 0);
  const receipt = await tx.wait();
  console.log(`Deposit tx: ${txLink(tx.hash)}`);

  const data = await getAccountData(signer.address);
  printAccountSummary(data);
  return { tx: tx.hash, data };
}

export async function borrow(amountUsdc) {
  const signer = getSigner();
  const amount = ethers.parseUnits(amountUsdc, 6); // USDC has 6 decimals

  const pool = new ethers.Contract(ADDRESSES.pool, POOL_ABI, signer);

  // Check available borrows
  const accountData = await getAccountData(signer.address);
  if (accountData.availableBorrowsBase === 0n) {
    throw new Error("No borrowing power. Deposit collateral first.");
  }

  console.log(`Borrowing ${amountUsdc} USDC...`);
  const tx = await pool.borrow(ADDRESSES.usdc, amount, VARIABLE_RATE, 0, signer.address);
  const receipt = await tx.wait();
  console.log(`Borrow tx: ${txLink(tx.hash)}`);

  const data = await getAccountData(signer.address);
  printAccountSummary(data);
  return { tx: tx.hash, data };
}

export async function repay(amountOrMax) {
  const signer = getSigner();
  const isMax = amountOrMax.toLowerCase() === "max";
  const amount = isMax ? ethers.MaxUint256 : ethers.parseUnits(amountOrMax, 6);

  const usdc = new ethers.Contract(ADDRESSES.usdc, ERC20_ABI, signer);
  const pool = new ethers.Contract(ADDRESSES.pool, POOL_ABI, signer);

  // Check USDC balance (unless max, which Aave handles)
  if (!isMax) {
    const balance = await usdc.balanceOf(signer.address);
    if (balance < amount) {
      throw new Error(
        `Insufficient USDC balance. Have ${ethers.formatUnits(balance, 6)}, need ${amountOrMax}`,
      );
    }
  }

  // Approve Pool to spend USDC
  await ensureAllowance(usdc, ADDRESSES.pool, amount, signer);

  const label = isMax ? "all" : amountOrMax;
  console.log(`Repaying ${label} USDC debt...`);
  const tx = await pool.repay(ADDRESSES.usdc, amount, VARIABLE_RATE, signer.address);
  const receipt = await tx.wait();
  console.log(`Repay tx: ${txLink(tx.hash)}`);

  const data = await getAccountData(signer.address);
  printAccountSummary(data);
  return { tx: tx.hash, data };
}

export async function withdraw(amountOrMax) {
  const signer = getSigner();
  const isMax = amountOrMax.toLowerCase() === "max";
  const amount = isMax ? ethers.MaxUint256 : ethers.parseEther(amountOrMax);

  const pool = new ethers.Contract(ADDRESSES.pool, POOL_ABI, signer);

  const label = isMax ? "all" : `${amountOrMax} WETH`;
  console.log(`Withdrawing ${label} from Aave...`);
  const tx = await pool.withdraw(ADDRESSES.weth, amount, signer.address);
  const receipt = await tx.wait();
  console.log(`Withdraw tx: ${txLink(tx.hash)}`);

  const data = await getAccountData(signer.address);
  printAccountSummary(data);
  return { tx: tx.hash, data };
}

export async function getHealthFactor(address) {
  const resolvedAddress = address || getSigner().address;
  const data = await getAccountData(resolvedAddress);
  console.log(`\nAccount: ${resolvedAddress}`);
  printAccountSummary(data);
  return data;
}

export async function mintTestTokens(token, amount) {
  const signer = getSigner();

  const tokenLower = token.toLowerCase();
  let tokenAddr, decimals;
  if (tokenLower === "weth") {
    tokenAddr = ADDRESSES.weth;
    decimals = 18;
  } else if (tokenLower === "usdc") {
    tokenAddr = ADDRESSES.usdc;
    decimals = 6;
  } else {
    throw new Error(`Unknown token "${token}". Supported: weth, usdc`);
  }

  const parsedAmount = ethers.parseUnits(amount, decimals);
  const faucet = new ethers.Contract(ADDRESSES.faucet, FAUCET_ABI, signer);

  console.log(`Minting ${amount} ${token.toUpperCase()} via faucet...`);
  const tx = await faucet.mint(tokenAddr, signer.address, parsedAmount);
  const receipt = await tx.wait();
  console.log(`Faucet tx: ${txLink(tx.hash)}`);

  // Show new balance
  const tokenContract = new ethers.Contract(tokenAddr, ERC20_ABI, signer.provider);
  const balance = await tokenContract.balanceOf(signer.address);
  console.log(`New ${token.toUpperCase()} balance: ${ethers.formatUnits(balance, decimals)}`);

  return { tx: tx.hash };
}
