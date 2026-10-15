# OKX A2A Daemon — Ops Fix (2026-08-02)

**Symptom:** OKX.AI rejected/delisted all 4 agent listings ("Gentech DeFi", "Gentech Curve", "Gentech Forge", "Gen Tech Strategies") with:
- "platform was unable to receive a response when checking your Agent's online status"
- "unable to receive a response from your Agent, causing the task to time out"

**Root cause:** `okx-a2a.service` crash-looped 90,000+ times (`status=203/EXEC`) because:

1. **Dead binary path** — unit pointed at `/usr/local/n/versions/node/22.14.0/bin/okx-a2a` (old nvm path); real binary is `/usr/local/node22/bin/okx-a2a`.
2. **AI provider prompt** — `daemon start` prompted interactively for provider under systemd (no TTY) → crash. Fix: `--ai-provider hermes`.
3. **onchainos ENOENT** — daemon couldn't find `onchainos` on PATH → agent sync failed. Fix: add `/root/.hermes/profiles/gentech/home/.local/bin` to PATH.
4. **Type=simple killed forked daemon** — CLI forks a child listener, parent exits, systemd killed the cgroup. Fix: `Type=forking` + `PIDFile=/root/.hermes/profiles/gentech/home/.okx-agent-task/run/listener.pid` + `--no-autostart`.
5. **HOME mismatch** — daemon read `/root/.onchainos` (empty) instead of profile home where the session lives. Fix: `Environment=HOME=/root/.hermes/profiles/gentech/home`.
6. **Expired session** — `onchainos wallet verify <OTP>` with email OTP to jordanjones0902@gmail.com.

**Working unit (as of 2026-08-02):**

```ini
[Unit]
Description=OKX A2A Daemon — Agent-to-Agent Protocol
After=network.target

[Service]
Type=forking
ExecStart=/usr/local/node22/bin/okx-a2a daemon start --ai-provider hermes --no-autostart
ExecStop=/usr/local/node22/bin/okx-a2a daemon stop
PIDFile=/root/.hermes/profiles/gentech/home/.okx-agent-task/run/listener.pid
Restart=on-failure
RestartSec=5
User=root
Environment=HOME=/root/.hermes/profiles/gentech/home
Environment=OKX_A2A_AI_PROVIDER=hermes
Environment=PATH=/root/.hermes/profiles/gentech/home/.local/bin:/usr/local/node22/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin

[Install]
WantedBy=multi-user.target
```

**Verify healthy:**
```bash
systemctl is-active okx-a2a.service   # → active
tail /root/.hermes/profiles/gentech/home/.okx-agent-task/logs/listener.log  # → "initialized 4/4 clients"
```

**Agents (all on XLayer, ASP role):** #4905 Gentech Forge · #2849 Gentech DeFi · #2848 Gentech Curve · #2847 Gen Tech Strategies (→ rebrand to GenTech Treasury per Jordan).
