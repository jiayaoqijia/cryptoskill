#!/usr/bin/env node
/** Venus repay helper (BNB Chain). Default mode: simulate */
const { ethers } = require('ethers');
const API_BASE='https://api.venus.io';
const DEFAULT_RPC='https://bsc-dataseed.binance.org/';
const VTOKEN_ABI=[
  'function repayBorrow(uint256) returns (uint256)',
  'function borrowBalanceStored(address) view returns (uint256)',
  'function symbol() view returns (string)',
  'function underlying() view returns (address)'
];
const ERC20_ABI=[
  'function decimals() view returns (uint8)',
  'function balanceOf(address) view returns (uint256)',
  'function allowance(address,address) view returns (uint256)',
  'function approve(address,uint256) returns (bool)'
];
function parseArgs(){const args=process.argv.slice(2);const out={mode:'simulate',rpc:DEFAULT_RPC};for(let i=0;i<args.length;i++){const k=args[i],v=args[i+1];if(k==='--asset')out.asset=v;if(k==='--amount')out.amount=v;if(k==='--wallet')out.wallet=v;if(k==='--private-key')out.privateKey=v;if(k==='--rpc-url')out.rpc=v;if(k==='--mode')out.mode=v;if(k==='--confirm')out.confirm=v;if(k.startsWith('--'))i++;}return out;}
async function fetchMarket(symbol){const u=`${API_BASE}/markets?chainId=56&limit=200&symbol=${encodeURIComponent(symbol)}`;const r=await fetch(u);if(!r.ok) throw new Error(`market api failed: ${r.status}`);const d=await r.json();const m=(d.result||[])[0];if(!m) throw new Error(`market not found: ${symbol}`);return m;}
async function main(){
 const a=parseArgs(); if(!a.asset||!a.amount){console.log('Usage: node venus_repay.js --asset vUSDC --amount 1 --wallet 0x... [--mode simulate|broadcast] [--private-key 0x...] [--confirm YES]');process.exit(1);} 
 const provider=new ethers.JsonRpcProvider(a.rpc); const m=await fetchMarket(a.asset);
 const wallet=a.wallet || (a.privateKey? new ethers.Wallet(a.privateKey).address:null); if(!wallet) throw new Error('wallet required (or provide --private-key)');
 const vToken=new ethers.Contract(m.address, VTOKEN_ABI, provider); const erc20=new ethers.Contract(m.underlyingAddress, ERC20_ABI, provider);
 const dec=Number(await erc20.decimals()); const amount=ethers.parseUnits(a.amount, dec);
 const borrowBefore=await vToken.borrowBalanceStored(wallet); const bal=await erc20.balanceOf(wallet); const allowance=await erc20.allowance(wallet,m.address);
 const out={mode:a.mode,asset:a.asset,amountInput:a.amount,wallet,vToken:m.address,underlying:m.underlyingAddress,steps:[
   {action:'check_borrow_balance_before', borrowBalance:borrowBefore.toString()},
   {action:'check_underlying_balance', balance:bal.toString(), required:amount.toString()},
   {action:'check_allowance', allowance:allowance.toString(), required:amount.toString()}
 ]};
 if(a.mode==='broadcast'){
   if(!a.privateKey) throw new Error('broadcast mode requires --private-key');
   if(a.confirm!=='YES') throw new Error('broadcast mode requires --confirm YES');
   const signer=new ethers.Wallet(a.privateKey, provider);
   const erc20s=new ethers.Contract(m.underlyingAddress, ERC20_ABI, signer);
   if(allowance<amount){const txA=await erc20s.approve(m.address, amount); const rcA=await txA.wait(); out.steps.push({action:'approve', txHash:txA.hash, status:rcA.status});}
   const v=new ethers.Contract(m.address, VTOKEN_ABI, signer); const tx=await v.repayBorrow(amount); const rc=await tx.wait();
   const borrowAfter=await vToken.borrowBalanceStored(wallet); out.steps.push({action:'repay', txHash:tx.hash, status:rc.status}); out.steps.push({action:'check_borrow_balance_after', borrowBalance:borrowAfter.toString()});
 } else out.steps.push({action:'preview', note:'No tx sent in simulate mode'});
 console.log(JSON.stringify(out,null,2));
}
main().catch(e=>{console.error(JSON.stringify({error:e.message},null,2));process.exit(1);});
