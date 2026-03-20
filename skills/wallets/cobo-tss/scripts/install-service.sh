#!/usr/bin/env bash
set -euo pipefail

# Install Cobo TSS Node as a system service
# Usage: install-service.sh <linux|macos> [--dir DIR] [--env dev|sandbox|prod]

PLATFORM="${1:-}"
shift || true

DIR="$HOME/.cobo-tss-node"
ENV="prod"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dir) DIR="$2"; shift 2 ;;
    --env) ENV="$2"; shift 2 ;;
    *) echo "Unknown arg: $1"; exit 1 ;;
  esac
done

BIN="$DIR/cobo-tss-node"
KEYFILE="$DIR/.password"
CONFIG="$DIR/configs/cobo-tss-node-config.yaml"

[[ ! -x "$BIN" ]] && echo "❌ Binary not found: $BIN" && exit 1
[[ ! -f "$KEYFILE" ]] && echo "❌ Key file not found: $KEYFILE" && exit 1

case "$PLATFORM" in
  linux)
    SERVICE_DIR="$HOME/.config/systemd/user"
    SERVICE_FILE="$SERVICE_DIR/cobo-tss-node.service"
    mkdir -p "$SERVICE_DIR"

    cat > "$SERVICE_FILE" <<EOF
[Unit]
Description=Cobo TSS Node
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
WorkingDirectory=$DIR
ExecStart=$BIN start --${ENV} --key-file $KEYFILE --config $CONFIG --db db/secrets.db
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

# Security hardening
NoNewPrivileges=true
ProtectSystem=strict
ProtectHome=false
ReadWritePaths=$DIR/db $DIR/logs $DIR/recovery $DIR/backups
PrivateTmp=true

[Install]
WantedBy=default.target
EOF

    systemctl --user daemon-reload
    systemctl --user enable cobo-tss-node.service

    echo "✅ Systemd user service installed: $SERVICE_FILE"
    echo ""
    echo "Commands:"
    echo "  systemctl --user start cobo-tss-node"
    echo "  systemctl --user stop cobo-tss-node"
    echo "  systemctl --user status cobo-tss-node"
    echo "  journalctl --user -u cobo-tss-node -f"
    echo ""
    echo "⚠️  For service to run after logout: loginctl enable-linger $(whoami)"
    ;;

  macos)
    PLIST_DIR="$HOME/Library/LaunchAgents"
    PLIST_FILE="$PLIST_DIR/com.cobo.tss-node.plist"
    LOG_DIR="$DIR/logs"
    mkdir -p "$PLIST_DIR" "$LOG_DIR"

    cat > "$PLIST_FILE" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.cobo.tss-node</string>
    <key>ProgramArguments</key>
    <array>
        <string>$BIN</string>
        <string>start</string>
        <string>--${ENV}</string>
        <string>--key-file</string>
        <string>$KEYFILE</string>
        <string>--config</string>
        <string>$CONFIG</string>
        <string>--db</string>
        <string>db/secrets.db</string>
    </array>
    <key>WorkingDirectory</key>
    <string>$DIR</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <dict>
        <key>SuccessfulExit</key>
        <false/>
    </dict>
    <key>StandardOutPath</key>
    <string>$LOG_DIR/launchd-stdout.log</string>
    <key>StandardErrorPath</key>
    <string>$LOG_DIR/launchd-stderr.log</string>
    <key>ThrottleInterval</key>
    <integer>10</integer>
</dict>
</plist>
EOF

    echo "✅ LaunchAgent installed: $PLIST_FILE"
    echo ""
    echo "Commands:"
    echo "  launchctl load $PLIST_FILE"
    echo "  launchctl unload $PLIST_FILE"
    echo "  launchctl list | grep cobo"
    echo "  tail -f $LOG_DIR/launchd-stdout.log"
    ;;

  *)
    echo "Usage: install-service.sh <linux|macos> [--dir DIR] [--env ENV]"
    exit 1
    ;;
esac
