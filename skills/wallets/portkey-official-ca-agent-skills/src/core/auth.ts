import type {
  PortkeyConfig,
  ChainId,
  VerifierItem,
  OperationType,
  SendVerificationCodeParams,
  SendVerificationCodeResult,
  VerifyCodeParams,
  VerifyCodeResult,
  RegisterParams,
  RecoverParams,
  RecoveryApprovedGuardian,
  RegisterOrRecoverResult,
  StatusCheckType,
  StatusCheckResult,
} from '../../lib/types.js';
import { LoginTypeLabel, LoginType } from '../../lib/types.js';
import { createHttpClient } from '../../lib/http.js';
import { withPortkeyRecoveryHint } from '../../lib/error-hints.js';
import { extractOperationTypeFromVerificationDoc, parseLoginType } from './guardian-approval.js';

// ============================================================================
// getVerifierServer
// ============================================================================

export interface GetVerifierServerParams {
  chainId: ChainId;
}

/**
 * Get an assigned verifier server for verification operations.
 *
 * API: POST /api/app/account/getVerifierServer
 */
export async function getVerifierServer(
  config: PortkeyConfig,
  params: GetVerifierServerParams,
): Promise<VerifierItem> {
  if (!params?.chainId) throw new Error('chainId is required');
  const http = createHttpClient(config);

  const result = await http.post<VerifierItem>('/api/app/account/getVerifierServer', {
    data: { chainId: params.chainId },
  });

  if (!result?.id) {
    throw new Error('Failed to get verifier server');
  }

  return result;
}

// ============================================================================
// sendVerificationCode
// ============================================================================

/**
 * Send a verification code to an email address.
 *
 * API: POST /api/app/account/sendVerificationRequest
 */
export async function sendVerificationCode(
  config: PortkeyConfig,
  params: SendVerificationCodeParams,
): Promise<SendVerificationCodeResult> {
  if (!params.email) throw new Error('email is required');
  if (!params.verifierId) throw new Error('verifierId is required');
  if (!params.chainId) throw new Error('chainId is required');
  if (params.operationType === undefined) throw new Error('operationType is required');

  const http = createHttpClient(config);

  const result = await http.post<SendVerificationCodeResult>(
    '/api/app/account/sendVerificationRequest',
    {
      data: {
        type: LoginTypeLabel[LoginType.Email],
        guardianIdentifier: params.email,
        verifierId: params.verifierId,
        chainId: params.chainId,
        operationType: params.operationType,
      },
    },
  );

  if (!result?.verifierSessionId) {
    throw new Error('Failed to send verification code');
  }

  return result;
}

// ============================================================================
// verifyCode
// ============================================================================

/**
 * Verify a 6-digit code sent to an email address.
 * Returns the verifier's signature and verificationDoc needed for registration/recovery.
 *
 * API: POST /api/app/account/verifyCode
 */
export async function verifyCode(
  config: PortkeyConfig,
  params: VerifyCodeParams,
): Promise<VerifyCodeResult> {
  if (!params.email) throw new Error('email is required');
  if (!params.verificationCode) throw new Error('verificationCode is required');
  if (!params.verifierId) throw new Error('verifierId is required');
  if (!params.verifierSessionId) throw new Error('verifierSessionId is required');

  const http = createHttpClient(config);

  const result = await http.post<VerifyCodeResult>('/api/app/account/verifyCode', {
    data: {
      type: LoginTypeLabel[LoginType.Email],
      guardianIdentifier: params.email,
      verifierSessionId: params.verifierSessionId,
      verificationCode: params.verificationCode,
      verifierId: params.verifierId,
      chainId: params.chainId,
      operationType: params.operationType,
    },
  });

  if (!result?.signature || !result?.verificationDoc) {
    throw new Error('Verification failed: no signature or verificationDoc returned');
  }

  return result;
}

// ============================================================================
// registerWallet
// ============================================================================

/**
 * Register a new Portkey CA wallet with email.
 *
 * Prerequisites:
 * 1. Call getVerifierServer() to get a verifier
 * 2. Call sendVerificationCode() to send a code
 * 3. Call verifyCode() to get signature + verificationDoc
 * 4. Create a manager wallet via createWallet()
 * 5. Call this function with all the above data
 *
 * API: POST /api/app/account/register/request
 */
export async function registerWallet(
  config: PortkeyConfig,
  params: RegisterParams,
): Promise<RegisterOrRecoverResult> {
  if (!params.email) throw new Error('email is required');
  if (!params.manager) throw new Error('manager address is required');
  if (!params.verifierId) throw new Error('verifierId is required');
  if (!params.verificationDoc) throw new Error('verificationDoc is required');
  if (!params.signature) throw new Error('signature is required');
  if (!params.chainId) throw new Error('chainId is required');

  const http = createHttpClient(config);

  const requestId = generateRequestId();

  const result = await http.post<RegisterOrRecoverResult>(
    '/api/app/account/register/request',
    {
      data: {
        type: LoginTypeLabel[LoginType.Email],
        loginGuardianIdentifier: params.email,
        manager: params.manager,
        extraData: params.extraData || String(Date.now()),
        chainId: params.chainId,
        verifierId: params.verifierId,
        verificationDoc: params.verificationDoc,
        signature: params.signature,
        context: params.context || {
          clientId: params.manager,
          requestId,
        },
      },
    },
  );

  if (!result?.sessionId) {
    throw new Error('Registration request failed: no sessionId returned');
  }

  return result;
}

// ============================================================================
// recoverWallet
// ============================================================================

/**
 * Recover (login to) an existing Portkey CA wallet with email.
 *
 * Prerequisites:
 * 1. Get guardian list for the account
 * 2. Verify enough guardians (approval count = floor(count * 3/5) + 1)
 * 3. Create a new manager wallet via createWallet()
 * 4. Call this function with all guardian approvals
 *
 * API: POST /api/app/account/recovery/request
 */
export async function recoverWallet(
  config: PortkeyConfig,
  params: RecoverParams,
): Promise<RegisterOrRecoverResult> {
  if (!params.email) throw new Error('email is required');
  if (!params.manager) throw new Error('manager address is required');
  if (!params.guardiansApproved?.length) throw new Error('guardiansApproved is required');
  if (!params.chainId) throw new Error('chainId is required');

  const http = createHttpClient(config);
  const normalizedGuardians = validateRecoveryGuardiansApproved(params.guardiansApproved);

  const requestId = generateRequestId();

  const result = await http.post<RegisterOrRecoverResult>(
    '/api/app/account/recovery/request',
    {
      data: {
        loginGuardianIdentifier: params.email,
        manager: params.manager,
        extraData: params.extraData || String(Date.now()),
        chainId: params.chainId,
        guardiansApproved: normalizedGuardians.map((g) => ({
          type: LoginTypeLabel[g.type],
          identifier: g.identifier,
          // NOTE: do NOT send identifierHash — the backend computes it from identifier + salt
          verifierId: g.verifierId,
          verificationDoc: g.verificationDoc,
          signature: g.signature,
        })),
        context: params.context || {
          clientId: params.manager,
          requestId,
        },
      },
    },
  );

  if (!result?.sessionId) {
    throw new Error('Recovery request failed: no sessionId returned');
  }

  return result;
}

// ============================================================================
// checkRegisterOrRecoveryStatus
// ============================================================================

/**
 * Check the status of a registration or recovery request.
 *
 * API:
 * - Register: GET /api/app/search/accountregisterindex
 * - Recovery: GET /api/app/search/accountrecoverindex
 *
 * Status values: 'pass', 'pending', 'fail'
 */
export async function checkRegisterOrRecoveryStatus(
  config: PortkeyConfig,
  params: { sessionId: string; type: StatusCheckType },
): Promise<StatusCheckResult> {
  if (!params.sessionId) throw new Error('sessionId is required');
  if (!params.type) throw new Error('type is required ("register" or "recovery")');

  const http = createHttpClient(config);

  const endpoint =
    params.type === 'register'
      ? '/api/app/search/accountregisterindex'
      : '/api/app/search/accountrecoverindex';

  const result = await http.get<{ items: Array<Record<string, unknown>> }>(endpoint, {
    params: { filter: `_id:${params.sessionId}` },
  });

  const item = result.items?.[0];
  if (!item) {
    return { status: 'pending' };
  }

  const statusField = params.type === 'register' ? 'registerStatus' : 'recoveryStatus';
  const status = (item[statusField] as string) || 'pending';

  if (status === 'pass') {
    return {
      status: 'pass',
      caAddress: item.caAddress as string,
      caHash: item.caHash as string,
    };
  }

  if (status === 'fail') {
    const msgField = params.type === 'register' ? 'registerMessage' : 'recoveryMessage';
    return {
      status: 'fail',
      failMessage: withPortkeyRecoveryHint(
        ((item[msgField] as string) || (item.failMessage as string) || 'Unknown failure'),
      ),
    };
  }

  return { status: 'pending' };
}

// ============================================================================
// Helpers
// ============================================================================

function generateRequestId(): string {
  return `${Date.now()}-${Math.random().toString(36).slice(2, 10)}`;
}

function validateRecoveryGuardiansApproved(
  guardians: RecoverParams['guardiansApproved'],
): Array<RecoveryApprovedGuardian & { type: LoginType }> {
  if (!Array.isArray(guardians) || guardians.length === 0) {
    throw new Error('guardiansApproved is required');
  }

  return guardians.map((guardian, index) => {
    if (!guardian || typeof guardian !== 'object') {
      throw new Error(`guardiansApproved[${index}] must be an object`);
    }

    const identifier = guardian.identifier?.trim();
    if (!identifier) {
      throw new Error(`guardiansApproved[${index}].identifier is required`);
    }

    const verifierId = guardian.verifierId?.trim();
    if (!verifierId) {
      throw new Error(`guardiansApproved[${index}].verifierId is required`);
    }

    const verificationDoc = guardian.verificationDoc?.trim();
    if (!verificationDoc) {
      throw new Error(`guardiansApproved[${index}].verificationDoc is required`);
    }

    const signature = guardian.signature?.trim();
    if (!signature) {
      throw new Error(`guardiansApproved[${index}].signature is required`);
    }

    const type = parseLoginType(guardian.type, `guardiansApproved[${index}].type`);

    const operationType = extractOperationTypeFromVerificationDoc(verificationDoc);
    if (operationType !== 2) {
      throw new Error(
        `guardiansApproved[${index}].verificationDoc must be generated by verify-code with operation "recovery" (operationType=2), got ${operationType ?? 'unknown'}`,
      );
    }

    return {
      ...guardian,
      identifier,
      verifierId,
      verificationDoc,
      signature,
      type,
    };
  });
}
