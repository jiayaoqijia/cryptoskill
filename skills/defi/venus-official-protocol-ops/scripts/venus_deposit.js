#!/usr/bin/env node
/**
 * Venus deposit helper (BNB Chain).
 * Default mode is simulate (no tx broadcast).
 */
const { ethers } = require('ethers');

const API_BASE = 'https://api.venus.io';
const DEFAULT_RPC = 'https://bsc-dataseed.binance.org/';

const ERC20_ABI = [
  'function decimals() view returns (uint8)',
  'function symbol() view returns (string)',
  'function balanceOf(address) view returns (uint256)',
  'function allowance(address,address) view returns (uint256)',
  'function approve(address,uint256) returns (bool)'
];

const VTOKEN_ABI = [
  'function mint(uint256) returns (uint256)',
  'function mint() payable',
  'function underlying() view returns (address)',
  'function symbol() view returns (string)'
];

function parseArgs() {
  const args = process.argv.slice(2);
  const out = { mode: 'simulate', rpc: DEFAULT_RPC };
  for (let i = 0; i < args.length; i++) {
    const k = args[i];
    const v = args[i + 1];
    if (k === '--asset') out.asset = v;
    if (k === '--amount') out.amount = v;
    if (k === '--wallet') out.wallet = v;
    if (k === '--private-key') out.privateKey = v;
    if (k === '--rpc-url') out.rpc = v;
    if (k === '--mode') out.mode = v;
    if (k === '--confirm') out.confirm = v;
    if (k.startsWith('--')) i++;
  }
  return out;
}

async function fetchMarket(assetSymbol) {
  const url = `${API_BASE}/markets?chainId=56&limit=200&symbol=${encodeURIComponent(assetSymbol)}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`market api failed: ${res.status}`);
  const data = await res.json();
  const m = (data.result || [])[0];
  if (!m) throw new Error(`market not found for symbol ${assetSymbol}`);
  return m;
}

function isNativeLike(symbol) {
  return ['vBNB', 'vWBNB'].includes((symbol || '').toUpperCase());
}

async function main() {
  const a = parseArgs();
  if (!a.asset || !a.amount) {
    console.log('Usage: node venus_deposit.js --asset vUSDT --amount 10 --wallet 0x... [--mode simulate|broadcast] [--private-key 0x...] [--confirm YES]');
    process.exit(1);
  }

  const provider = new ethers.JsonRpcProvider(a.rpc);
  const market = await fetchMarket(a.asset);
  const vToken = market.address;
  const underlying = market.underlyingAddress;

  const walletAddr = a.wallet || (a.privateKey ? new ethers.Wallet(a.privateKey).address : null);
  if (!walletAddr) throw new Error('wallet required (or provide --private-key)');

  const out = {
    mode: a.mode,
    asset: a.asset,
    amountInput: a.amount,
    wallet: walletAddr,
    vToken,
    underlying,
    steps: []
  };

  let signer = null;
  if (a.privateKey) signer = new ethers.Wallet(a.privateKey, provider);

  if (isNativeLike(a.asset)) {
    const wei = ethers.parseEther(a.amount);
    const balance = await provider.getBalance(walletAddr);
    out.steps.push({ action: 'check_native_balance', balanceWei: balance.toString(), requiredWei: wei.toString() });

    if (a.mode === 'broadcast') {
      if (!signer) throw new Error('broadcast mode requires --private-key');
      if (a.confirm !== 'YES') throw new Error('broadcast mode requires --confirm YES');
      const c = new ethers.Contract(vToken, VTOKEN_ABI, signer);
      const tx = await c.mint({ value: wei });
      const rc = await tx.wait();
      out.steps.push({ action: 'mint_native', txHash: tx.hash, status: rc.status });
    } else {
      out.steps.push({ action: 'mint_native_preview', note: 'No tx sent in simulate mode' });
    }

    console.log(JSON.stringify(out, null, 2));
    return;
  }

  const erc20 = new ethers.Contract(underlying, ERC20_ABI, provider);
  const decimals = Number(await erc20.decimals());
  const amount = ethers.parseUnits(a.amount, decimals);
  const balance = await erc20.balanceOf(walletAddr);
  const allowance = await erc20.allowance(walletAddr, vToken);

  out.steps.push({ action: 'check_balance', decimals, balance: balance.toString(), required: amount.toString() });
  out.steps.push({ action: 'check_allowance', allowance: allowance.toString(), required: amount.toString() });

  if (a.mode === 'broadcast') {
    if (!signer) throw new Error('broadcast mode requires --private-key');
    if (a.confirm !== 'YES') throw new Error('broadcast mode requires --confirm YES');

    const erc20s = new ethers.Contract(underlying, ERC20_ABI, signer);
    if (allowance < amount) {
      const txApprove = await erc20s.approve(vToken, amount);
      const rcA = await txApprove.wait();
      out.steps.push({ action: 'approve', txHash: txApprove.hash, status: rcA.status });
    }

    const v = new ethers.Contract(vToken, VTOKEN_ABI, signer);
    const txMint = await v['mint(uint256)'](amount);
    const rcM = await txMint.wait();
    out.steps.push({ action: 'mint', txHash: txMint.hash, status: rcM.status });
  } else {
    out.steps.push({ action: 'preview', note: 'No tx sent in simulate mode' });
  }

  console.log(JSON.stringify(out, null, 2));
}

main().catch((e) => {
  console.error(JSON.stringify({ error: e.message }, null, 2));
  process.exit(1);
});
