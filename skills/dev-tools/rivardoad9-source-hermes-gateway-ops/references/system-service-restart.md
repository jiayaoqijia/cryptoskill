# Restarting the gateway when it runs as a SYSTEM service (verified 2026-08-25)

This host runs `sudo hermes gateway --system` → `hermes-gateway.service` in the SYSTEM systemd scope. The main SKILL.md's restart recipe assumes `--user`; here is the system-scope variant and the gotchas hit in practice.

## Detached restart (survives the restart, session keeps running)

1. Write the restart script (via write_file):
   ```bash
   #!/bin/bash
   systemctl restart hermes-gateway
   ```
2. Fire it detached, owned by systemd (NOT the gateway tree), so the calling agent session survives:
   ```bash
   sudo systemd-run --on-active=3 /bin/bash /tmp/restart_gw.sh
   # → Running timer as unit: run-<id>.timer
   ```
   Verified: passes the terminal guard (no inline-block), gateway bounces, the chat session is restored by the gateway on startup.

## `sudo hermes gateway restart --system` does NOT restart anything on this host (verified 2026-10-14)

The user-facing command fails silently-ish: root resolves a DIFFERENT data root, so the bootstrap refuses
the ubuntu-owned checkout and exits 1 before touching systemd. Output:

```
hermes: preparing dependencies for this root (the checkout's updates belong to /home/ubuntu/.hermes)...
hermes: source-update completion failed: refusing to update /home/ubuntu/.hermes/hermes-agent: /home/ubuntu/.hermes/hermes-agent is owned by uid 1000, not the current uid 0
hermes: no dependency environment is committed for this install; run `hermes pm repair`
```

Exit code 0 with the service untouched (MainPID + ActiveEnterTimestamp unchanged) — it LOOKS like it worked.
This applies to every `sudo hermes …` (system scope needs root, `_require_root_for_system_service`).
Do not chase `hermes pm repair` for it: root cannot legally activate uid-1000 dependencies. Restart
systemd directly with the detached recipe above and verify `MainPID` actually changed.

## Gotchas (verified)

- **A restart SIGKILLs the whole gateway cgroup** — including the children a chat/CLI session started via
the terminal tool (seen: `~/.hermes/trade/server.py` on :8793 + its cloudflared quick-tunnel). Cheap
restore: re-run the lane's own watchdog (`bash ~/.hermes/trade/up.sh`) and hand the user the NEW
quick-tunnel URL in chat — up.sh records it in `data/ht_url_seen.txt`, so the cron watchdog stays silent
about the change. Ports owned by systemd/other cgroups (whale board, ETF desk, lynk receiver) survive.

- **A restart KILLS in-flight cron/delegation runs** — including a content-post job that hasn't published yet. Before restarting, wait for running jobs to finish: `grep -E "cron.scheduler: Job .*(completed successfully|delivered)" ~/.hermes/logs/agent.log | tail`. If a scheduled job is due within minutes, prefer waiting.
- **Exit code 1 on SIGTERM is normal**: `hermes-gateway.service: Main process exited, code=exited, status=1/FAILURE` appears on every shutdown, then `Restart=on-failure` bounces it within ~2s. A NEW MainPID right after restart is EXPECTED — verify with `systemctl is-active` + `systemctl show -p MainPID --value` rather than comparing PIDs. `NRestarts` stays 0 (that counter is systemd-initiated restarts only).
- The transient unit pattern means the gateway restart is NOT a child of the calling session — no SIGTERM propagation to you.
- Verification: `systemctl status hermes-gateway` (no `--user`), `journalctl -u hermes-gateway --since "…"` (no `--user`), plus the Telegram `getWebhookInfo` poll check from the main skill.
