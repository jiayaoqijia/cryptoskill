#!/usr/bin/env bash
# Auto-bind UniversalX invitation code for the current universal-account-example wallet.
# Run from universal-account-example directory.
# Usage:
#   ./bind-invitation.sh [INVITE_CODE]

set -euo pipefail

INVITE_CODE="${1:-${INVITE_CODE:-666666}}"
API_BASE_URL="${UNIVERSALX_INVITATIONS_API_URL:-https://universal-app-api-proxy.particle.network}"
LANG_CODE="$(printf '%s' "${LANG:-en}" | cut -d'_' -f1)"

require_command() {
    if ! command -v "$1" >/dev/null 2>&1; then
        echo "Missing required command: $1"
        exit 1
    fi
}

ensure_project_directory() {
    if [ ! -f package.json ]; then
        echo "package.json not found. Run this script from universal-account-example."
        exit 1
    fi
}

if [ "$LANG_CODE" = "zh" ]; then
    echo "UniversalX 邀请码自动绑定"
    echo "===================================="
    echo "邀请码: $INVITE_CODE"
else
    echo "UniversalX Invitation Auto-Bind"
    echo "===================================="
    echo "Invite code: $INVITE_CODE"
fi

require_command node
ensure_project_directory

if [ -z "$INVITE_CODE" ]; then
    if [ "$LANG_CODE" = "zh" ]; then
        echo "邀请码为空，已跳过。"
    else
        echo "Invite code is empty, skipping."
    fi
    exit 0
fi

INVITE_CODE="$INVITE_CODE" API_BASE_URL="$API_BASE_URL" node - <<'__NODE__'
const axios = require('axios');
const stringify = require('fast-json-stable-stringify');
const { sha256 } = require('@noble/hashes/sha256');
const { config } = require('dotenv');
const { Wallet } = require('ethers');
const { v4: uuidv4 } = require('uuid');
const {
  UniversalAccount,
  createUnsignedMessage,
  PROJECT_UUID,
  PROJECT_CLIENT_KEY,
  PROJECT_APP_UUID,
} = require('@particle-network/universal-account-sdk');

config();

function toHex(bytes) {
  return Buffer.from(bytes).toString('hex').toLowerCase();
}

function buildSignedParams({ token, macKey, deviceId, extraParams = {}, body }) {
  const params = {
    ...extraParams,
    particleAuthToken: token,
    mode: 'mainnet',
    timestamp: Math.round(Date.now() / 1000),
    random_str: uuidv4(),
    device_id: deviceId,
    sdk_version: 'web_0.10.5',
    time_zone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    locale: Intl.DateTimeFormat().resolvedOptions().locale,
    project_uuid: PROJECT_UUID,
    project_client_key: PROJECT_CLIENT_KEY,
    project_app_uuid: PROJECT_APP_UUID,
  };

  const signObj = { ...params };
  if (body && typeof body === 'object') {
    Object.assign(signObj, body);
  }
  signObj.mac_key = macKey;

  const mac = toHex(sha256(new TextEncoder().encode(stringify(signObj))));
  return { ...params, mac };
}

function throwApiError(context, data) {
  const err = new Error(`${context}: ${JSON.stringify(data)}`);
  err.data = data;
  throw err;
}

async function main() {
  const inviteCode = process.env.INVITE_CODE || '666666';
  const apiBaseUrl = process.env.API_BASE_URL || 'https://universal-app-api-proxy.particle.network';

  const privateKey = process.env.PRIVATE_KEY || '';
  const projectId = process.env.PROJECT_ID || '';
  const projectClientKey = process.env.PROJECT_CLIENT_KEY || '';
  const projectAppUuid = process.env.PROJECT_APP_UUID || '';

  if (!/^0x[a-fA-F0-9]{64}$/.test(privateKey)) {
    throw new Error('PRIVATE_KEY is missing or invalid in .env');
  }
  if (!projectId || !projectClientKey || !projectAppUuid) {
    throw new Error('PROJECT_ID / PROJECT_CLIENT_KEY / PROJECT_APP_UUID missing in .env');
  }

  const wallet = new Wallet(privateKey);
  const ua = new UniversalAccount({
    projectId,
    projectClientKey,
    projectAppUuid,
    ownerAddress: wallet.address,
  });

  const smartOptions = await ua.getSmartAccountOptions();
  const smartAddress = smartOptions.smartAccountAddress;
  if (!smartAddress) {
    throw new Error('smartAccountAddress not found');
  }

  const deviceId = uuidv4();
  const timestampMs = Date.now();
  const message = createUnsignedMessage(smartAddress, deviceId, timestampMs);
  const signature = await wallet.signMessage(message);
  const login = await ua.register(inviteCode, deviceId, timestampMs, signature);

  if (!login || typeof login !== 'object' || !login.token || !login.macKey) {
    throwApiError('register failed', login);
  }

  const token = login.token;
  const macKey = login.macKey;
  const endpoint = `${apiBaseUrl.replace(/\/$/, '')}/invitations`;

  const getParams = buildSignedParams({
    token,
    macKey,
    deviceId,
    extraParams: { address: smartAddress },
  });

  const getRes = await axios.get(endpoint, { params: getParams, timeout: 15000 });
  const getData = getRes.data || {};
  const currentCode = getData?.invitation?.code || '';
  if (getData.success && currentCode) {
    if (currentCode === inviteCode) {
      console.log(`Invite already bound: ${currentCode}`);
      return;
    }

    console.log(`Invite already bound to another code: ${currentCode}. Skip rebind.`);
    return;
  }

  const body = { code: inviteCode };
  const postParams = buildSignedParams({ token, macKey, deviceId, body });
  const postRes = await axios.post(endpoint, body, { params: postParams, timeout: 15000 });
  const postData = postRes.data || {};

  if (postData.success === true || postData.error_code === 20005) {
    console.log(postData.error_code === 20005 ? 'Invite already bound (idempotent).' : 'Invite bind success.');
    return;
  }

  throwApiError('bind invitation failed', postData);
}

main().catch((err) => {
  const lang = (process.env.LANG || 'en').split('_')[0];
  if (lang === 'zh') {
    console.error('自动绑定失败:', err.message);
  } else {
    console.error('Auto-bind failed:', err.message);
  }
  process.exit(1);
});
__NODE__
