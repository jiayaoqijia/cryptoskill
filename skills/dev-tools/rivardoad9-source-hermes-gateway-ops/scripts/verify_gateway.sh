#!/bin/bash
# Quick Hermes gateway health check after a restart. No secrets needed.
echo "=== service status ==="
systemctl --user status hermes-gateway --no-pager -l | head -12
echo
echo "=== recent gateway log: platform/connect lines ==="
journalctl --user -u hermes-gateway --no-pager -n 40 | grep -iE "telegram|discord|whatsapp|slack|platform|connect|error" | tail -12
echo
echo "=== error scan ==="
if grep -ilE "traceback|critical" "$HOME/.hermes/logs/gateway.log" "$HOME/.hermes/logs/errors.log" 2>/dev/null; then
    echo "ERRORS FOUND (see files above)"
    exit 1
else
    echo "no critical errors"
fi
