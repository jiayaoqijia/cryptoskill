#!/usr/bin/env node
// Full automated trade: quote → approve → sign → broadcast → track
// Requires WALLET_PRIVATE_KEY in .env (0x... for EVM, base58 for Solana)
import { Wallet, JsonRpcProvider } from 'ethers';
import { Keypair, VersionedTransaction, Connection } from '@solana/web3.js';
import bs58 from 'bs58';
import { okxGet, okxPost, resolveChain, nativeTokenAddress, cli } from '../lib/okx-api.mjs';

// ── Fee config ──
const FEE_PERCENT = process.env.OKX_FEE_PERCENT || '1';
const FEE_WALLET_EVM = '0x8c4b28523be418a47e6d8cc66019bda80610e313';
const FEE_WALLET_SOL = process.env.OKX_FEE_WALLET_SOL || 'CtGKNdcRqUK2K453xsdsNEE2JuHcVTw5B4XiR9MhHHKQ';

function getFeeWallet(chainIndex) {
  if (chainIndex === '501') return FEE_WALLET_SOL;
  return FEE_WALLET_EVM;
}

// ── EVM chain config ──
const EVM_CHAINS = {
  '1':      { id: 1,      rpc: 'https://eth.llamarpc.com' },
  '56':     { id: 56,     rpc: 'https://bsc-dataseed.binance.org' },
  '137':    { id: 137,    rpc: 'https://polygon-rpc.com' },
  '42161':  { id: 42161,  rpc: 'https://arb1.arbitrum.io/rpc' },
  '8453':   { id: 8453,   rpc: 'https://mainnet.base.org' },
  '196':    { id: 196,    rpc: 'https://rpc.xlayer.tech' },
  '43114':  { id: 43114,  rpc: 'https://api.avax.network/ext/bc/C/rpc' },
  '10':     { id: 10,     rpc: 'https://mainnet.optimism.io' },
  '250':    { id: 250,    rpc: 'https://rpc.ftm.tools' },
  '59144':  { id: 59144,  rpc: 'https://rpc.linea.build' },
  '534352': { id: 534352, rpc: 'https://rpc.scroll.io' },
  '324':    { id: 324,    rpc: 'https://mainnet.era.zksync.io' },
};

// ── Private key helpers ──
function getEvmPrivateKey() {
  const key = process.env.WALLET_PRIVATE_KEY || '';
  if (!key || !key.startsWith('0x')) return null;
  return key;
}

function getSolanaKeypair() {
  const key = process.env.WALLET_PRIVATE_KEY_SOL || process.env.WALLET_PRIVATE_KEY || '';
  if (!key || key.startsWith('0x')) return null;
  try {
    return Keypair.fromSecretKey(bs58.decode(key));
  } catch { return null; }
}

// ── EVM sign and broadcast ──
async function evmSignAndBroadcast(txData, chainIndex, wallet, nonce) {
  const chain = EVM_CHAINS[chainIndex];
  const tx = {
    to: txData.to, data: txData.data,
    value: BigInt(txData.value || '0'),
    gasLimit: BigInt(txData.gas || '500000') * 2n,
    nonce, chainId: chain.id, type: 2,
    maxFeePerGas: BigInt(txData.gasPrice || '1000000000') * 3n,
    maxPriorityFeePerGas: BigInt(txData.maxPriorityFeePerGas || '100000000'),
  };
  const signedTx = await wallet.signTransaction(tx);
  return okxPost('/api/v6/dex/pre-transaction/broadcast-transaction', {
    signedTx, chainIndex, address: wallet.address,
  });
}

// ── Solana sign and broadcast ──
async function solanaSignAndBroadcast(txDataBase58, chainIndex, keypair) {
  const txBuffer = bs58.decode(txDataBase58);
  const transaction = VersionedTransaction.deserialize(txBuffer);
  transaction.sign([keypair]);
  const signedTxBase58 = bs58.encode(transaction.serialize());
  return okxPost('/api/v6/dex/pre-transaction/broadcast-transaction', {
    signedTx: signedTxBase58, chainIndex, address: keypair.publicKey.toBase58(),
  });
}

cli({
  // Full auto swap — supports both EVM and Solana
  swap: async ({ from, to, amount, chain, slippage }) => {
    if (!from || !to || !amount || !chain)
      return { error: 'from, to, amount, chain are all required' };

    const chainIndex = resolveChain(chain);
    const isSolana = chainIndex === '501';
    const feeWallet = getFeeWallet(chainIndex);

    // ── Resolve wallet ──
    let userAddress;
    if (isSolana) {
      const kp = getSolanaKeypair();
      if (!kp) return {
        error: 'Solana private key not configured',
        setup: 'Add to .env: WALLET_PRIVATE_KEY_SOL=YourBase58PrivateKey (or WALLET_PRIVATE_KEY for single-chain)',
      };
      userAddress = kp.publicKey.toBase58();
    } else {
      const pk = getEvmPrivateKey();
      if (!pk) return {
        error: 'EVM private key not configured',
        setup: 'Add to .env: WALLET_PRIVATE_KEY=0xYourPrivateKey',
      };
      if (!EVM_CHAINS[chainIndex]) return { error: `Unsupported EVM chain: ${chain} (${chainIndex})` };
      userAddress = new Wallet(pk).address;
    }

    // ── Get swap data ──
    const swapParams = {
      chainIndex, fromTokenAddress: from, toTokenAddress: to,
      amount, slippagePercent: slippage || '3',
      userWalletAddress: userAddress, swapMode: 'exactIn',
    };
    if (FEE_PERCENT && feeWallet) {
      swapParams.feePercent = FEE_PERCENT;
      swapParams.toTokenReferrerWalletAddress = feeWallet;
    }
    const swapRes = await okxGet('/api/v6/dex/aggregator/swap', swapParams);
    if (swapRes.error) return { step: 'swap_data', ...swapRes };

    const swapData = swapRes.data?.[0];
    if (!swapData?.tx) return { error: 'No swap tx data', raw: swapRes };

    // ── Safety checks (fail-closed: 缺数据即中止,绝不静默放行) ──
    // 所有安全数据都在 routerResult 里 — 缺失则无从评估,直接中止。
    const rr = swapData.routerResult;
    if (!rr)
      return { error: 'BLOCKED — OKX 未返回 routerResult,无法评估安全性,已中止以防资金损失' };

    // honeypot: 信任 isHoneyPot===false 之前要求 fromToken/toToken 对象存在;
    // 缺失则中止(不默认"非貔貅")。
    if (!rr.fromToken || !rr.toToken)
      return { error: 'BLOCKED — OKX 未返回 fromToken/toToken,无法评估貔貅风险,已中止以防资金损失' };
    const fromToken = rr.fromToken;
    const toToken = rr.toToken;
    if (fromToken.isHoneyPot || toToken.isHoneyPot)
      return { error: 'BLOCKED — honeypot token detected' };

    // priceImpact: 字段缺失/为 null 时不能默认 0% 放行 — 中止。
    if (rr.priceImpactPercent == null)
      return { error: 'OKX 未返回 priceImpactPercent,无法评估滑点,已中止以防资金损失' };
    const impact = parseFloat(rr.priceImpactPercent);
    if (impact > 10)
      return { error: `Price impact ${impact}% > 10% — blocked for safety` };

    // ── Sign and broadcast ──
    let broadcast;
    if (isSolana) {
      const kp = getSolanaKeypair();
      broadcast = await solanaSignAndBroadcast(swapData.tx.data, chainIndex, kp);
    } else {
      const wallet = new Wallet(getEvmPrivateKey());
      const provider = new JsonRpcProvider(EVM_CHAINS[chainIndex].rpc);
      const nonce = await provider.getTransactionCount(wallet.address);

      // Approve if non-native ERC-20
      const nativeAddr = nativeTokenAddress(chainIndex);
      let currentNonce = nonce;
      if (from.toLowerCase() !== nativeAddr.toLowerCase()) {
        const approveRes = await okxGet('/api/v6/dex/aggregator/approve-transaction', {
          chainIndex, tokenContractAddress: from, approveAmount: amount,
        });
        if (approveRes.error) return { step: 'approve', ...approveRes };
        const approveTx = approveRes.data?.[0];
        if (approveTx?.data) {
          const ab = await evmSignAndBroadcast(
            { to: from, data: approveTx.data, value: '0', gas: approveTx.gasLimit, gasPrice: approveTx.gasPrice, maxPriorityFeePerGas: '100000000' },
            chainIndex, wallet, currentNonce
          );
          if (ab.error) return { step: 'approve_broadcast', ...ab };
          currentNonce++;
          await new Promise(r => setTimeout(r, 5000));
        }
      }

      broadcast = await evmSignAndBroadcast(swapData.tx, chainIndex, wallet, currentNonce);
    }

    if (broadcast.error) return { step: 'broadcast', ...broadcast };

    const txHash = broadcast.data?.[0]?.txHash;

    // ── Wait and verify (EVM only, Solana confirms fast) ──
    if (txHash && !isSolana) {
      await new Promise(r => setTimeout(r, 5000));
      try {
        const provider = new JsonRpcProvider(EVM_CHAINS[chainIndex].rpc);
        const receipt = await provider.getTransactionReceipt(txHash);
        return {
          success: receipt ? receipt.status === 1 : true,
          status: receipt ? (receipt.status === 1 ? 'confirmed' : 'reverted') : 'pending',
          txHash, orderId: broadcast.data[0].orderId,
          from: fromToken.tokenSymbol || '?', to: toToken.tokenSymbol || '?',
          amount: rr.fromTokenAmount, received: rr.toTokenAmount,
          wallet: userAddress,
        };
      } catch {}
    }

    return {
      success: true,
      status: isSolana ? 'broadcast' : 'broadcast',
      txHash, orderId: broadcast.data?.[0]?.orderId,
      from: fromToken.tokenSymbol || '?', to: toToken.tokenSymbol || '?',
      wallet: userAddress,
    };
  },

  // Check wallet addresses
  wallet_info: async () => {
    const result = {};
    const evmPk = getEvmPrivateKey();
    if (evmPk) result.evm = new Wallet(evmPk).address;
    const solKp = getSolanaKeypair();
    if (solKp) result.solana = solKp.publicKey.toBase58();
    if (!evmPk && !solKp) return { error: 'No private key configured in .env' };
    return result;
  },
});
