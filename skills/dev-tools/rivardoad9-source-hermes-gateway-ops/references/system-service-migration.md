# Migrating the gateway to a system-level service (--system)

Use when the gateway should run 24/7 independent of any login (systemd system scope) instead of the default user service. Validated live: user-service → system-service migration on Ubuntu with Telegram, gateway active through the whole switch.

## The flow

1. **Install WITHOUT starting** — `--no-start-now` is critical:
   ```bash
   sudo /home/<user>/.local/bin/hermes gateway install --system --no-start-now
   ```
   - `sudo hermes` often fails with "command not found": root's PATH lacks the user launcher. Always use the absolute launcher path under sudo.
   - In non-interactive shells `start_now` defaults to **True** — without `--no-start-now` the system unit starts immediately while the user service still runs → TWO instances polling the same platform → Telegram 409 conflicts / split updates.
   - The unit's run-user is auto-detected from `SUDO_USER` (falls back to `USER`), so a sudo install runs as the invoking user with the SAME HERMES_HOME/config/token. Verify:
     ```bash
     grep -E 'User=|Group=|HERMES_HOME=|Restart=' /etc/systemd/system/hermes-gateway.service
     systemctl is-enabled hermes-gateway        # expect: enabled (multi-user.target = boots at boot)
     ```

2. **Swap detached** — a running session's terminal children are children of the gateway process itself (verify: `ps -o ppid= -p $$` → gateway PID). Stopping the user service kills the session mid-turn. Same reason restarts are scheduled via systemd-run:
   ```bash
   # /tmp/swap_gw.sh — logs to /tmp/gw_swap.log
   systemctl --user stop hermes-gateway
   systemctl --user disable hermes-gateway      # prevents double-start at next boot
   sudo -n systemctl start hermes-gateway       # the new system-scope unit
   ```
   Schedule: `systemd-run --user --on-active=8 /bin/bash /tmp/swap_gw.sh`
   - Pick a delay long enough for the final chat message to be delivered (≥8s).
   - Do ALL tool calls first, then send the final message — the interruption kills the session mid-turn.
   - Warn the user the chat will drop briefly and to send a test message afterwards.

3. **After the swap** — every service command needs `--system`:
   - `sudo hermes gateway status --system` / `start --system` / `stop --system`
   - Plain `hermes gateway status` targets the USER service and will report the old (stopped) unit.
   - The stale user unit file (`~/.config/systemd/user/hermes-gateway.service`) can stay; `disable` alone prevents boot conflicts.

## Verification

- `systemctl is-active hermes-gateway` → `active`; Main PID under `/system.slice/hermes-gateway.service`.
- `journalctl -u hermes-gateway --no-pager -n` → `[Telegram] Connecting to Telegram…` connect lines.
- End-to-end: the user's next message is answered (this is handled by the NEW service).

## Related pitfalls

- `hermes gateway install` (system or user) refuses if `EXTERNAL_GATEWAY_SUPERVISOR_ENV` is set in the calling environment — plain terminal sessions from the gateway do NOT carry it, so installs work; a supervisor-managed install returns a managed_error instead.
- Never run the install with start-now while any other gateway instance holds the platform poll.
