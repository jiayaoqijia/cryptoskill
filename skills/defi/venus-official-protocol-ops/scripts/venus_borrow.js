#!/usr/bin/env node
/** Venus borrow helper (BNB Chain). Default mode: simulate */
const { ethers } = require('ethers');
const API_BASE='https://api.venus.io';
const DEFAULT_RPC='https://bsc-dataseed.binance.org/';

const VTOKEN_ABI=[
  'function borrow(uint256) returns (uint256)',
  'function borrowBalanceStored(address) view returns (uint256)',
  'function symbol() view returns (string)',
  'function underlying() view returns (address)'
];
const ERC20_ABI=[
  'function decimals() view returns (uint8)',
  'function balanceOf(address) view returns (uint256)',
  'function symbol() view returns (string)'
];

function parseArgs(){
  const args=process.argv.slice(2); const out={mode:'simulate', rpc:DEFAULT_RPC};
  for(let i=0;i<args.length;i++){
    const k=args[i], v=args[i+1];
    if(k==='--asset') out.asset=v;
    if(k==='--amount') out.amount=v;
    if(k==='--wallet') out.wallet=v;
    if(k==='--private-key') out.privateKey=v;
    if(k==='--rpc-url') out.rpc=v;
    if(k==='--mode') out.mode=v;
    if(k==='--confirm') out.confirm=v;
    if(k.startsWith('--')) i++;
  }
  return out;
}

async function fetchMarket(symbol){
  const u=`${API_BASE}/markets?chainId=56&limit=200&symbol=${encodeURIComponent(symbol)}`;
  const r=await fetch(u); if(!r.ok) throw new Error(`market api failed: ${r.status}`);
  const d=await r.json(); const m=(d.result||[])[0]; if(!m) throw new Error(`market not found: ${symbol}`);
  return m;
}

async function main(){
  const a=parseArgs();
  if(!a.asset||!a.amount){
    console.log('Usage: node venus_borrow.js --asset vUSDT --amount 1 --wallet 0x... [--mode simulate|broadcast] [--private-key 0x...] [--confirm YES]');
    process.exit(1);
  }
  const provider=new ethers.JsonRpcProvider(a.rpc);
  const market=await fetchMarket(a.asset);
  const wallet=a.wallet || (a.privateKey? new ethers.Wallet(a.privateKey).address:null);
  if(!wallet) throw new Error('wallet required (or provide --private-key)');

  const vToken=new ethers.Contract(market.address, VTOKEN_ABI, provider);
  const underlying=new ethers.Contract(market.underlyingAddress, ERC20_ABI, provider);
  const dec=Number(await underlying.decimals());
  const amount=ethers.parseUnits(a.amount, dec);
  const liqUsd=Number(market.liquidityCents||0)/100;
  const priceUsd=Number(market.tokenPriceCents||0)/100;
  const reqUsd=Number(a.amount)*priceUsd;
  const borrowBefore=await vToken.borrowBalanceStored(wallet);
  const uBalBefore=await underlying.balanceOf(wallet);

  const out={mode:a.mode,asset:a.asset,amountInput:a.amount,wallet,vToken:market.address,underlying:market.underlyingAddress,steps:[
    {action:'check_market_liquidity', liquidityUsd:liqUsd, requestedUsd:reqUsd},
    {action:'check_borrow_balance_before', borrowBalance:borrowBefore.toString()},
    {action:'check_underlying_balance_before', underlyingBalance:uBalBefore.toString()}
  ]};

  if(a.mode==='broadcast'){
    if(!a.privateKey) throw new Error('broadcast mode requires --private-key');
    if(a.confirm!=='YES') throw new Error('broadcast mode requires --confirm YES');
    const signer=new ethers.Wallet(a.privateKey, provider);
    const v=new ethers.Contract(market.address, VTOKEN_ABI, signer);
    const tx=await v['borrow(uint256)'](amount);
    const rc=await tx.wait();
    const borrowAfter=await vToken.borrowBalanceStored(wallet);
    const uBalAfter=await underlying.balanceOf(wallet);
    out.steps.push({action:'borrow',txHash:tx.hash,status:rc.status});
    out.steps.push({action:'check_borrow_balance_after', borrowBalance:borrowAfter.toString()});
    out.steps.push({action:'check_underlying_balance_after', underlyingBalance:uBalAfter.toString()});
  }else{
    out.steps.push({action:'preview', note:'No tx sent in simulate mode'});
  }

  console.log(JSON.stringify(out,null,2));
}
main().catch(e=>{console.error(JSON.stringify({error:e.message},null,2));process.exit(1);});
