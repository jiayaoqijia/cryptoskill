#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { ethers } = require('ethers');

const a = Object.fromEntries(process.argv.slice(2).map((v,i,arr)=> v.startsWith('--') ? [v.slice(2), arr[i+1] && !arr[i+1].startsWith('--') ? arr[i+1] : 'true'] : []).filter(Boolean));
if (!a.asset || !a.amount || !a.wallet) throw new Error('usage: --asset fUSDC --amount 1 --wallet 0x... [--mode simulate|broadcast --private-key 0x... --confirm YES]');
if (!ethers.isAddress(a.wallet)) throw new Error('invalid wallet address');
if (Number(a.amount) <= 0) throw new Error('amount must be > 0');

const rpc = a.rpcUrl || 'https://bsc-dataseed.binance.org/';
const mode = a.mode || 'simulate';
if (!['simulate','broadcast'].includes(mode)) throw new Error('mode must be simulate or broadcast');
const cfgPath = a.config || path.resolve(__dirname, '../../references/flux-bnb-addresses.json');
const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
const m = (cfg.fTokens || []).find(x => x.symbol.toLowerCase() === a.asset.toLowerCase());
if (!m) throw new Error(`unknown flux market: ${a.asset}`);

const ERC20 = ['function balanceOf(address) view returns (uint256)','function allowance(address,address) view returns (uint256)','function approve(address,uint256) returns (bool)','function decimals() view returns (uint8)'];
const FTOKEN = ['function asset() view returns (address)','function deposit(uint256,address) returns (uint256)'];

(async () => {
  const provider = new ethers.JsonRpcProvider(rpc);
  const fToken = new ethers.Contract(m.address, FTOKEN, provider);
  const underlying = await fToken.asset();
  const erc20 = new ethers.Contract(underlying, ERC20, provider);
  const decimals = Number(await erc20.decimals());
  const amount = ethers.parseUnits(String(a.amount), decimals);
  const bal = await erc20.balanceOf(a.wallet);
  const allowance = await erc20.allowance(a.wallet, m.address);

  const out = { protocol:'flux', mode, asset: a.asset, wallet:a.wallet, fToken:m.address, underlying, steps:[
    { action:'check_balance', balance: bal.toString(), required: amount.toString() },
    { action:'check_allowance', allowance: allowance.toString(), required: amount.toString() }
  ]};

  if (bal < amount) throw new Error('insufficient underlying balance for lend amount');

  if (mode !== 'broadcast') {
    out.steps.push({ action:'preview', note:'No tx sent in simulate mode' });
    console.log(JSON.stringify(out,null,2));
    return;
  }

  const pk = a.privateKey || a['private-key'];
  if (!pk || a.confirm !== 'YES') throw new Error('broadcast requires --private-key and --confirm YES');
  const signer = new ethers.Wallet(pk, provider);
  if (signer.address.toLowerCase() !== a.wallet.toLowerCase()) throw new Error('wallet and private key address mismatch');
  const erc20s = erc20.connect(signer);
  const fts = fToken.connect(signer);

  if (allowance < amount) {
    const txA = await erc20s.approve(m.address, amount);
    const rcA = await txA.wait();
    out.steps.push({ action:'approve', txHash: txA.hash, status: rcA.status });
  }

  const tx = await fts.deposit(amount, a.wallet);
  const rc = await tx.wait();
  out.steps.push({ action:'deposit', txHash: tx.hash, status: rc.status });
  console.log(JSON.stringify(out,null,2));
})().catch((e)=>{ console.error(JSON.stringify({error:String(e.message||e)},null,2)); process.exit(1); });
