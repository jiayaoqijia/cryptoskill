#!/usr/bin/env bash
# Setup wizard for Universal Trading.
# Run from universal-account-example directory.
# Usage:
#   ./setup-wizard.sh new
#   ./setup-wizard.sh import <PRIVATE_KEY>
# Optional:
#   ALLOW_NON_STANDARD_PROJECT=1 ./setup-wizard.sh new

set -euo pipefail

INVITE_CODE="666666"
PROJECT_ID="47fe67e3-5cf2-4be2-886b-1d4b4290595f"
PROJECT_CLIENT_KEY="cVbve788gN6Wna6IYA4MCU9SjN6wOyfEZtNVnbuu"
PROJECT_APP_UUID="dddd3cb1-bf66-460b-91c2-7adb0373e21c"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

LANG_CODE="$(printf '%s' "${LANG:-en}" | cut -d'_' -f1)"

print_usage() {
    echo "Usage:"
    echo "  ./setup-wizard.sh new"
    echo "  ./setup-wizard.sh import <PRIVATE_KEY>"
    echo ""
    echo "Optional override:"
    echo "  ALLOW_NON_STANDARD_PROJECT=1 ./setup-wizard.sh new"
}

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

    if ! grep -q '"name"[[:space:]]*:[[:space:]]*"universal-account-example"' package.json; then
        if [ "${ALLOW_NON_STANDARD_PROJECT:-0}" != "1" ]; then
            echo "This directory does not look like universal-account-example."
            echo "If you really want to continue, set ALLOW_NON_STANDARD_PROJECT=1."
            exit 1
        fi

        echo "ALLOW_NON_STANDARD_PROJECT=1 set, continuing on non-standard project."
    fi

    if [ ! -f examples/get-primary-asset.ts ] && [ "${ALLOW_NON_STANDARD_PROJECT:-0}" != "1" ]; then
        echo "Missing examples/get-primary-asset.ts. Run this inside universal-account-example."
        echo "Or set ALLOW_NON_STANDARD_PROJECT=1 to force run."
        exit 1
    fi
}

ensure_ethers_dependency() {
    if ! node -e "require('ethers')" >/dev/null 2>&1; then
        echo "Missing npm dependency: ethers"
        echo "Run: npm install"
        exit 1
    fi
}

mask_private_key() {
    local key="$1"
    printf '%s...%s' "${key:0:6}" "${key: -4}"
}

echo "Universal Trading Setup Wizard"
echo "===================================="
echo ""

require_command node
ensure_project_directory

ACTION="${1:-}"
if [ "$ACTION" = "new" ]; then
    echo "Generating new wallet..."

    PRIVATE_KEY="$(node -e "
const crypto = require('crypto');
console.log('0x' + crypto.randomBytes(32).toString('hex'));
")"
elif [ "$ACTION" = "import" ]; then
    PRIVATE_KEY="${2:-}"
    if [ -z "$PRIVATE_KEY" ]; then
        print_usage
        exit 1
    fi

    if [[ ! "$PRIVATE_KEY" =~ ^0x[a-fA-F0-9]{64}$ ]]; then
        echo "Invalid private key format. Expected: 0x + 64 hex chars."
        exit 1
    fi
else
    print_usage
    exit 1
fi

ensure_ethers_dependency

ADDRESS="$(node -e "
const { Wallet } = require('ethers');
const wallet = new Wallet('$PRIVATE_KEY');
console.log(wallet.address);
")"

if [ -f .env ]; then
    BACKUP_FILE=".env.bak.$(date +%Y%m%d-%H%M%S)"
    cp .env "$BACKUP_FILE"
    echo "Existing .env backed up to $BACKUP_FILE"
fi

cat > .env <<'__ENV__'
# EVM private key, which can be used by ethers.Wallet
PRIVATE_KEY=__PRIVATE_KEY__
# Particle Network credentials
PROJECT_ID=__PROJECT_ID__
PROJECT_CLIENT_KEY=__PROJECT_CLIENT_KEY__
PROJECT_APP_UUID=__PROJECT_APP_UUID__
# polymarket
EVM_RPC_137=https://polygon-rpc.com/
# user assets wss (optional, defaults to wss://universal-app-ws-proxy.particle.network)
# UNIVERSALX_WSS_URL=
__ENV__

# Replace placeholders after writing to avoid heredoc delimiter conflicts.
sed -i.bak "s|__PRIVATE_KEY__|$PRIVATE_KEY|" .env
sed -i.bak "s|__PROJECT_ID__|$PROJECT_ID|" .env
sed -i.bak "s|__PROJECT_CLIENT_KEY__|$PROJECT_CLIENT_KEY|" .env
sed -i.bak "s|__PROJECT_APP_UUID__|$PROJECT_APP_UUID|" .env
rm -f .env.bak

chmod 600 .env 2>/dev/null || true
ENV_FILE_PATH="$(pwd)/.env"

DISPLAY_PRIVATE_KEY="$(mask_private_key "$PRIVATE_KEY")"
if [ "${SHOW_PRIVATE_KEY:-0}" = "1" ]; then
    DISPLAY_PRIVATE_KEY="$PRIVATE_KEY"
fi

echo ""
if [ "$LANG_CODE" = "zh" ]; then
    echo "钱包已就绪！"
    echo "================================"
    echo "地址: $ADDRESS"
    echo "私钥: $DISPLAY_PRIVATE_KEY"
    if [ "${SHOW_PRIVATE_KEY:-0}" != "1" ]; then
        echo "如需显示完整私钥，执行: SHOW_PRIVATE_KEY=1 ./setup-wizard.sh $ACTION ${2:-}"
    fi
    echo "================================"
else
    echo "Wallet ready!"
    echo "================================"
    echo "Address: $ADDRESS"
    echo "Private Key: $DISPLAY_PRIVATE_KEY"
    if [ "${SHOW_PRIVATE_KEY:-0}" != "1" ]; then
        echo "To print full key, run: SHOW_PRIVATE_KEY=1 ./setup-wizard.sh $ACTION ${2:-}"
    fi
    echo "================================"
fi

echo ""
if [ "$LANG_CODE" = "zh" ]; then
    echo "已保存到: $ENV_FILE_PATH"
    echo "私钥位置: $ENV_FILE_PATH"
    echo "私钥字段: PRIVATE_KEY"
    echo "可直接在前端导入: https://universalx.app -> 创建钱包 -> 导入现有钱包"
else
    echo "Saved to: $ENV_FILE_PATH"
    echo "Private key location: $ENV_FILE_PATH"
    echo "Private key field: PRIVATE_KEY"
    echo "You can import this wallet at: https://universalx.app -> Create Wallet -> Import Existing Wallet"
fi

echo ""
if [ "$LANG_CODE" = "zh" ]; then
    echo "================================"
    echo "自动绑定邀请码"
    echo "================================"
    if [ "${DISABLE_AUTO_INVITE_BIND:-0}" = "1" ]; then
        echo "已跳过 (DISABLE_AUTO_INVITE_BIND=1)。"
    elif bash "$SCRIPT_DIR/bind-invitation.sh" "$INVITE_CODE"; then
        echo "邀请码自动绑定已完成。"
    else
        echo "邀请码自动绑定失败，但初始化会继续。"
        echo "可手动重试："
        echo "  bash $SCRIPT_DIR/bind-invitation.sh $INVITE_CODE"
    fi
else
    echo "================================"
    echo "Auto-bind invite code"
    echo "================================"
    if [ "${DISABLE_AUTO_INVITE_BIND:-0}" = "1" ]; then
        echo "Skipped (DISABLE_AUTO_INVITE_BIND=1)."
    elif bash "$SCRIPT_DIR/bind-invitation.sh" "$INVITE_CODE"; then
        echo "Invite auto-bind finished."
    else
        echo "Invite auto-bind failed, setup will continue."
        echo "Retry manually:"
        echo "  bash $SCRIPT_DIR/bind-invitation.sh $INVITE_CODE"
    fi
fi

if [ "$LANG_CODE" = "zh" ]; then
    echo ""
    echo "================================"
    echo "邀请码信息"
    echo "================================"
    echo "邀请码: $INVITE_CODE"
    echo "绑定福利："
    echo "  - 升级到 2 级交易等级"
    echo "  - 获得 1.5 倍钻石倍数"
    echo "  - 享受 12.5% 现金奖励"
    echo "  - 获得高返佣"
    echo "手动绑定链接: https://universalx.app/?inviteCode=$INVITE_CODE"
    echo ""
    echo "测试命令: npx tsx examples/get-primary-asset.ts"
else
    echo ""
    echo "================================"
    echo "Invite code info"
    echo "================================"
    echo "Invite code: $INVITE_CODE"
    echo "Manual bind URL: https://universalx.app/?inviteCode=$INVITE_CODE"
    echo ""
    echo "Test command: npx tsx examples/get-primary-asset.ts"
fi
