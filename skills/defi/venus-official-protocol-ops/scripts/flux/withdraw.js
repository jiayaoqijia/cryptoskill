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

const FTOKEN = [
  'function balanceOf(address) view returns (uint256)',
  'function maxWithdraw(address) view returns (uint256)',
  'function withdraw(uint256,address,address) returns (uint256)',
  'function asset() view returns (address)'
];
const ERC20 = ['function decimals() view returns (uint8)','function balanceOf(address) view returns (uint256)'];

(async () => {
  const provider = new ethers.JsonRpcProvider(rpc);
  const fToken = new ethers.Contract(m.address, FTOKEN, provider);
  const underlying = await fToken.asset();
  const erc20 = new ethers.Contract(underlying, ERC20, provider);
  const decimals = Number(await erc20.decimals());
  const amount = ethers.parseUnits(String(a.amount), decimals);
  const maxW = await fToken.maxWithdraw(a.wallet);
  const ub = await erc20.balanceOf(a.wallet);

  const out = { protocol:'flux', mode, asset: a.asset, wallet:a.wallet, fToken:m.address, underlying, steps:[
    { action:'check_max_withdraw', maxWithdraw: maxW.toString(), requested: amount.toString() },
    { action:'check_underlying_balance_before', balance: ub.toString() }
  ]};

  if (maxW < amount) throw new Error('requested amount exceeds maxWithdraw');

  if (mode !== 'broadcast') {
    out.steps.push({ action:'preview', note:'No tx sent in simulate mode' });
    console.log(JSON.stringify(out,null,2));
    return;
  }

  const pk = a.privateKey || a['private-key'];
  if (!pk || a.confirm !== 'YES') throw new Error('broadcast requires --private-key and --confirm YES');
  const signer = new ethers.Wallet(pk, provider);
  if (signer.address.toLowerCase() !== a.wallet.toLowerCase()) throw new Error('wallet and private key address mismatch');
  const fts = fToken.connect(signer);
  const tx = await fts.withdraw(amount, a.wallet, a.wallet);
  const rc = await tx.wait();
  const ub2 = await erc20.balanceOf(a.wallet);
  out.steps.push({ action:'withdraw', txHash: tx.hash, status: rc.status });
  out.steps.push({ action:'check_underlying_balance_after', balance: ub2.toString() });
  console.log(JSON.stringify(out,null,2));
})().catch((e)=>{ console.error(JSON.stringify({error:String(e.message||e)},null,2)); process.exit(1); });
