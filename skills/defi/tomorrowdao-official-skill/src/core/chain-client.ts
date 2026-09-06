import AElf from 'aelf-sdk';
import { getConfig, getContracts } from './config.js';
import { SkillError } from './errors.js';
import type {
  ChainCallInput,
  ChainId,
  ChainSimulatePayload,
  ExecutionMode,
  JsonObject,
  SendOptions,
  TxReceipt,
} from './types.js';
import { getWalletByPrivateKey } from './signature.js';
import { waitForTxResult } from './tx-waiter.js';
import { clearAelfPool, getAelfByRpc } from './aelf-pool.js';
import { resolvePrivateKeyContext } from './signer-context.js';
import { SIGNER_ERROR_CODES } from './signer-error-codes.js';
import type { SignerContextInput } from './wallet-context.js';

export function clearAelfCache(): void {
  clearAelfPool();
}

async function getContract(input: ChainCallInput, privateKey?: string): Promise<any> {
  const config = getConfig();
  const rpc = config.rpc[input.chainId];
  if (!rpc) throw new SkillError('UNSUPPORTED_CHAIN', `No rpc configured for ${input.chainId}`);

  const aelf = getAelfByRpc(rpc);
  const wallet = privateKey ? getWalletByPrivateKey(privateKey) : AElf.wallet.createNewWallet();
  const contract = await aelf.chain.contractAt(input.contractAddress, wallet);
  return {
    aelf,
    rpc,
    contract,
  };
}

function getMethod(contract: any, methodName: string): any {
  const method = contract[methodName];
  if (!method) {
    throw new SkillError('METHOD_NOT_FOUND', `method ${methodName} not found on contract`);
  }
  return method;
}

export async function callView(input: ChainCallInput): Promise<any> {
  const { contract } = await getContract(input);
  const method = getMethod(contract, input.methodName);
  const raw = await method.call(input.args);
  if (raw?.error || raw?.Error || raw?.code) {
    throw new SkillError('CONTRACT_VIEW_ERROR', `view call failed: ${input.methodName}`, raw);
  }
  return raw?.result ?? raw;
}

export async function callSend(
  input: ChainCallInput,
  options?: SendOptions & {
    privateKey?: string;
    signer?: SignerContextInput;
    signerContext?: SignerContextInput;
  },
): Promise<{ tx?: TxReceipt; result?: JsonObject | ChainSimulatePayload | unknown; simulated: boolean }> {
  const mode: ExecutionMode = options?.mode || 'simulate';
  if (mode === 'simulate') {
    return {
      simulated: true,
      result: {
        chainId: input.chainId,
        contractAddress: input.contractAddress,
        methodName: input.methodName,
        args: input.args,
      } as ChainSimulatePayload,
    };
  }

  const resolved = resolvePrivateKeyContext({
    signerMode: 'auto',
    ...(options?.signerContext || {}),
    ...(options?.signer || {}),
    privateKey: options?.privateKey,
  });
  if (resolved.identity.walletType === 'CA') {
    throw new SkillError(
      SIGNER_ERROR_CODES.CA_DIRECT_SEND_FORBIDDEN,
      'current signer resolves to a CA-backed identity; tomorrowdao-skill does not support direct contract send for CA signers, use an explicit CA forward transport instead',
      {
        provider: resolved.provider,
        walletType: resolved.identity.walletType,
        caHash: resolved.identity.caHash,
        caAddress: resolved.identity.caAddress,
      },
    );
  }
  const privateKey = resolved.privateKey;

  const { contract, rpc } = await getContract(input, privateKey);
  const method = getMethod(contract, input.methodName);
  const raw = await method(input.args);

  if (raw?.error || raw?.Error || raw?.code) {
    throw new SkillError('CONTRACT_SEND_ERROR', `send failed: ${input.methodName}`, raw);
  }

  const txId = raw?.transactionId || raw?.TransactionId || raw?.result?.TransactionId;
  if (!txId) {
    throw new SkillError('TX_ID_MISSING', 'transaction id missing from contract send result', raw);
  }

  let status = 'SUBMITTED';
  let logs: unknown[] | undefined;
  if (options?.waitForMined !== false) {
    const mined = await waitForTxResult(rpc, txId);
    status = mined.status;
    logs = mined.raw?.Logs || mined.raw?.logs || [];
  }

  return {
    simulated: false,
    result: raw,
      tx: {
        txId,
        status,
        logs,
        explorerUrl: `${getContracts().explorer[input.chainId]}/tx/${txId}`,
      },
    };
}

export async function packInput(
  chainId: string,
  contractAddress: string,
  methodName: string,
  args: unknown,
): Promise<string> {
  const cid = chainId as ChainId;
  const { contract } = await getContract({ chainId: cid, contractAddress, methodName, args });
  const method = getMethod(contract, methodName);
  if (typeof method.packInput !== 'function') {
    throw new SkillError('PACK_INPUT_UNSUPPORTED', `method ${methodName} does not expose packInput`);
  }
  const packed = method.packInput(args as any);
  return Buffer.from(packed || []).toString('base64');
}
