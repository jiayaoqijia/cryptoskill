#!/usr/bin/env node
/** Venus collateral manager (enter/exit market). Default mode: simulate */
const { ethers } = require('ethers');
const API_BASE='https://api.venus.io';
const DEFAULT_RPC='https://bsc-dataseed.binance.org/';
const COMP_ABI=[
  'function enterMarkets(address[]) returns (uint256[])',
  'function exitMarket(address) returns (uint256)',
  'function getAssetsIn(address) view returns (address[])'
];
function parseArgs(){const args=process.argv.slice(2);const out={mode:'simulate',rpc:DEFAULT_RPC,action:'enable'};for(let i=0;i<args.length;i++){const k=args[i],v=args[i+1];if(k==='--asset')out.asset=v;if(k==='--wallet')out.wallet=v;if(k==='--private-key')out.privateKey=v;if(k==='--rpc-url')out.rpc=v;if(k==='--mode')out.mode=v;if(k==='--action')out.action=v;if(k==='--confirm')out.confirm=v;if(k.startsWith('--'))i++;}return out;}
async function fetchMarket(symbol){const u=`https://api.venus.io/markets?chainId=56&limit=200&symbol=${encodeURIComponent(symbol)}`;const r=await fetch(u);if(!r.ok) throw new Error(`market api failed: ${r.status}`);const d=await r.json();const m=(d.result||[])[0];if(!m) throw new Error(`market not found: ${symbol}`);return m;}
async function main(){
 const a=parseArgs(); if(!a.asset){console.log('Usage: node venus_collateral.js --asset vUSDC --action enable|disable --wallet 0x... [--mode simulate|broadcast] [--private-key 0x...] [--confirm YES]');process.exit(1);}
 const provider=new ethers.JsonRpcProvider(a.rpc); const m=await fetchMarket(a.asset);
 const wallet=a.wallet || (a.privateKey? new ethers.Wallet(a.privateKey).address:null); if(!wallet) throw new Error('wallet required (or provide --private-key)');
 const compAddr=m.poolComptrollerAddress; const comp=new ethers.Contract(compAddr, COMP_ABI, provider);
 const assetsIn=await comp.getAssetsIn(wallet);
 const out={mode:a.mode,action:a.action,asset:a.asset,wallet,comptroller:compAddr,vToken:m.address,steps:[{action:'check_assets_in_before', assetsIn}]};
 if(a.mode==='broadcast'){
   if(!a.privateKey) throw new Error('broadcast mode requires --private-key');
   if(a.confirm!=='YES') throw new Error('broadcast mode requires --confirm YES');
   const signer=new ethers.Wallet(a.privateKey, provider); const c=new ethers.Contract(compAddr, COMP_ABI, signer);
   let tx;
   if(a.action==='disable'){tx=await c.exitMarket(m.address);}
   else {tx=await c.enterMarkets([m.address]);}
   const rc=await tx.wait();
   const after=await comp.getAssetsIn(wallet);
   out.steps.push({action:a.action==='disable'?'exitMarket':'enterMarkets', txHash:tx.hash, status:rc.status});
   out.steps.push({action:'check_assets_in_after', assetsIn:after});
 } else out.steps.push({action:'preview', note:'No tx sent in simulate mode'});
 console.log(JSON.stringify(out,null,2));
}
main().catch(e=>{console.error(JSON.stringify({error:e.message},null,2));process.exit(1);});
