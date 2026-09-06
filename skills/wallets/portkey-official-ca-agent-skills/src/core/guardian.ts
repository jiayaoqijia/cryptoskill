import type {
  PortkeyConfig,
  AddGuardianParams,
  RemoveGuardianParams,
  TransferResult,
} from '../../lib/types.js';
import { LoginTypeLabel } from '../../lib/types.js';
import { callSendMethod, type AElfWallet } from '../../lib/aelf-client.js';
import { getChainInfoByChainId } from './account.js';

/**
 * Convert a hex string to Buffer for protobuf `bytes` fields.
 * If the value is already a Buffer/Uint8Array, return it as-is.
 */
function toBytes(value: string | Buffer | Uint8Array): Buffer | Uint8Array {
  if (Buffer.isBuffer(value) || value instanceof Uint8Array) return value;
  if (typeof value === 'string') return Buffer.from(value, 'hex');
  return value;
}

// ============================================================================
// addGuardian
// ============================================================================

/**
 * Add a new guardian to a CA wallet.
 *
 * Prerequisites:
 * 1. Verify the new guardian's identity (sendVerificationCode + verifyCode)
 * 2. Get approval from existing guardians (approval count based on total)
 * 3. Call this function with all data
 *
 * Contract method: AddGuardian on CA contract
 */
export async function addGuardian(
  config: PortkeyConfig,
  wallet: AElfWallet,
  params: AddGuardianParams,
): Promise<TransferResult> {
  if (!params.caHash) throw new Error('caHash is required');
  if (!params.guardianToAdd) throw new Error('guardianToAdd is required');
  if (!params.guardiansApproved?.length) throw new Error('guardiansApproved is required');
  if (!params.chainId) throw new Error('chainId is required');

  const chainInfo = await getChainInfoByChainId(config, params.chainId);

  const result = await callSendMethod(
    chainInfo.endPoint,
    chainInfo.caContractAddress,
    wallet,
    'AddGuardian',
    {
      caHash: params.caHash,
      guardianToAdd: {
        identifierHash: params.guardianToAdd.identifierHash,
        type: params.guardianToAdd.type,
        verificationInfo: {
          id: params.guardianToAdd.verificationInfo.id,
          // protobuf `bytes` field — must be Buffer, not hex string
          signature: toBytes(params.guardianToAdd.verificationInfo.signature),
          verificationDoc: params.guardianToAdd.verificationInfo.verificationDoc,
        },
      },
      guardiansApproved: params.guardiansApproved.map((g) => ({
        type: g.type,
        identifierHash: g.identifierHash,
        verificationInfo: {
          id: g.verifierId,
          // protobuf `bytes` field — must be Buffer, not hex string
          signature: toBytes(g.signature),
          verificationDoc: g.verificationDoc,
        },
      })),
    },
  );

  return {
    transactionId: result.transactionId,
    status: result.data.Status,
  };
}

// ============================================================================
// removeGuardian
// ============================================================================

/**
 * Remove a guardian from a CA wallet.
 *
 * Prerequisites:
 * 1. Ensure the guardian is not the only login guardian
 * 2. If the guardian is a login guardian, unset it first
 * 3. Get approval from other guardians
 * 4. Call this function
 *
 * Contract method: RemoveGuardian on CA contract
 */
export async function removeGuardian(
  config: PortkeyConfig,
  wallet: AElfWallet,
  params: RemoveGuardianParams,
): Promise<TransferResult> {
  if (!params.caHash) throw new Error('caHash is required');
  if (!params.guardianToRemove) throw new Error('guardianToRemove is required');
  if (!params.guardiansApproved?.length) throw new Error('guardiansApproved is required');
  if (!params.chainId) throw new Error('chainId is required');

  const chainInfo = await getChainInfoByChainId(config, params.chainId);

  const result = await callSendMethod(
    chainInfo.endPoint,
    chainInfo.caContractAddress,
    wallet,
    'RemoveGuardian',
    {
      caHash: params.caHash,
      guardianToRemove: {
        identifierHash: params.guardianToRemove.identifierHash,
        type: params.guardianToRemove.type,
        verificationInfo: {
          id: params.guardianToRemove.verificationInfo.id,
        },
      },
      guardiansApproved: params.guardiansApproved.map((g) => ({
        type: g.type,
        identifierHash: g.identifierHash,
        verificationInfo: {
          id: g.verifierId,
          // protobuf `bytes` field — must be Buffer, not hex string
          signature: toBytes(g.signature),
          verificationDoc: g.verificationDoc,
        },
      })),
    },
  );

  return {
    transactionId: result.transactionId,
    status: result.data.Status,
  };
}
