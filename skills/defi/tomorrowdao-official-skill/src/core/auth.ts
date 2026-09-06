import { getConfig } from './config.js';
import { SkillError } from './errors.js';
import { buildSignaturePayload } from './signature.js';
import type { ApiResponse, AuthToken } from './types.js';

const TOKEN_SCOPE = 'TomorrowDAOServer';
const TOKEN_CLIENT_ID = 'TomorrowDAOServer_App';

let tokenCache: AuthToken | null = null;

function toFormData(entries: Record<string, string>): string {
  const p = new URLSearchParams();
  Object.entries(entries).forEach(([k, v]) => p.set(k, v));
  return p.toString();
}

function isTokenValid(token: AuthToken | null): boolean {
  if (!token) return false;
  const now = Date.now();
  return token.expiresAt - now > 30_000;
}

export function clearTokenCache(): void {
  tokenCache = null;
}

export async function getAccessToken(forceRefresh = false): Promise<AuthToken> {
  if (!forceRefresh && isTokenValid(tokenCache)) {
    return tokenCache as AuthToken;
  }

  const previousCache = tokenCache;
  if (forceRefresh) {
    tokenCache = null;
  }

  const config = getConfig();
  if (!config.privateKey) {
    throw new SkillError('AUTH_PRIVATE_KEY_REQUIRED', 'TMRW_PRIVATE_KEY is required for authenticated APIs');
  }

  try {
    const payload = buildSignaturePayload(config.privateKey);
    const body = toFormData({
      grant_type: 'signature',
      scope: TOKEN_SCOPE,
      client_id: TOKEN_CLIENT_ID,
      timestamp: String(payload.timestamp),
      signature: payload.signature,
      source: config.source,
      publickey: payload.publicKey,
      chain_id: config.authChainId,
      address: payload.address,
      ...(config.caHash ? { ca_hash: config.caHash } : {}),
    });

    const resp = await fetch(`${config.authBase}/connect/token`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body,
    });

    if (!resp.ok) {
      const text = await resp.text().catch(() => '');
      throw new SkillError('AUTH_HTTP_ERROR', `token request failed: ${resp.status}`, text);
    }

    const json = (await resp.json()) as ApiResponse<{ access_token: string; token_type: string; expires_in: number }>;
    const accessToken = (json as any).access_token || json?.data?.access_token;
    const tokenType = (json as any).token_type || json?.data?.token_type || 'Bearer';
    const expiresIn = Number((json as any).expires_in || json?.data?.expires_in || 0);

    if (!accessToken || !expiresIn) {
      throw new SkillError('AUTH_RESPONSE_INVALID', 'token response missing access_token or expires_in', json);
    }

    tokenCache = {
      accessToken,
      tokenType,
      expiresIn,
      expiresAt: Date.now() + expiresIn * 1000,
    };

    return tokenCache;
  } catch (err) {
    if (forceRefresh) {
      tokenCache = null;
    } else {
      tokenCache = previousCache;
    }
    throw err;
  }
}
