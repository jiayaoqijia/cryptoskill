---
name: desktop-mesh
description: "Connect always-on servers to a desktop/laptop Hermes over a private network (Tailscale) so agents on different machines become real peers — DM each other, and wake each other the moment a handoff lands. Covers the loopback bind that silently blocks it, fail-soft push-on-handoff, and the security rules that keep an agent API off the public internet."
version: 1.0.0
author: Gentech
tags: [multi-agent, peer, mesh, tailscale, desktop, api-server, handoff, wake, synergy]
license: MIT
---

# Desktop Mesh — Peers Across Machines

## When to Use
- You run Hermes on **more than one machine** — e.g. always-on VPS agents plus a
  desktop/laptop (the Hermes desktop app, a home workstation, a GPU box).
- You want those agents to **DM each other** and **act on handoffs**, not just share files.
- You want the desktop to be **woken when work arrives**, instead of only polling.
- You are wiring agents on **different platforms** and want one addressable mesh.

## The Problem This Solves

`hermes peer dm <peer>` is the cross-machine twin of a local bot chat — but it silently
fails across machines, and the reason is not obvious:

**The api_server binds to `127.0.0.1` by default.** Loopback means *"this machine
only."* Two agents on the **same** host talk fine. Two agents on **different** hosts
cannot reach each other at all — even though both are running, both are healthy, and
both are on the same private network.

> The failure is invisible from the inside: every local check passes. Only a
> *remote* probe reveals it. Always verify from the other end.

**The mesh gap is usually symmetric.** If your desktop can't reach the server, the
server almost certainly can't reach your desktop either — don't fix one direction and
declare victory.

## Requirements
- A private network between the machines. **Tailscale** is assumed here (works through
  NAT, no public exposure, per-node identities); any private overlay (WireGuard,
  Netmaker, a LAN/VPN) substitutes.
- Hermes installed on both machines.
- Shell access to the server (to set env vars) and to the desktop.

## The Fix — Four Steps

### 1. Bind the api_server to the private interface (not loopback)

These are **environment variables**, not `config.yaml` keys. Put them in each profile's
`.env` (`~/.hermes/profiles/<profile>/.env`):

```bash
API_SERVER_ENABLED=true
API_SERVER_HOST=100.x.y.z        # ← your Tailscale IP. THIS is the whole trick.
API_SERVER_PORT=8642
API_SERVER_KEY=<long-random-secret>
```

Get the right address with `tailscale ip -4` on each machine.

> ⚠️ **Bind to the Tailscale IP (or `tailscale0`) — never `0.0.0.0`.**
> `0.0.0.0` publishes an unrestricted agent API — one that can drive the full toolset —
> to the entire internet on any host with public ports. Bind narrowly, then use
> Tailscale ACLs for the rest.

### 2. Restart so the bind takes effect
```bash
hermes gateway restart          # per profile; or the fleet equivalent
ss -tlnp | grep 8642            # confirm it now listens on the tailnet IP, not 127.0.0.1
```

### 3. Register peers — both directions
```bash
# server → desktop
hermes peer add desktop --url http://100.a.b.c:8646 --key <same-secret>
# desktop → server
hermes peer add server  --url http://100.x.y.z:8642 --key <same-secret>
```
Peer credentials are stored locally in `~/.hermes/.env`.

### 4. Verify from the OTHER machine
```bash
hermes peer list
hermes peer dm desktop "ping"    # run from the server
hermes peer dm server  "ping"    # run from the desktop
```
Test **both directions**. A one-way mesh feels like a working mesh until it matters.

## The Prize: Wake on Handoff

With an api_server reachable, a desktop is no longer pull-only. A handoff watcher on the
always-on server can **push** a prompt the moment work lands:

```
handoff-watcher (server)  →  POST http://<desktop-ip>:8646/v1/chat/completions
                             {"model":"hermes-agent",
                              "messages":[{"role":"user",
                               "content":"New handoff in INBOX/desktop — sweep your lanes"}]}
```

**Fail-soft is the point.** If the desktop is off, the call simply fails and the vault
handoff is still there for the next sweep. You gain instant wake-up when the machine is
up, and inherit **no new failure mode** when it is down. Never make the push the only
delivery path — keep the durable folder as the source of truth.

## Security Rules (do not skip)

1. **One shared key is the weak point.** It's bearer auth; anyone holding it can drive
   the agent's full toolset. Use a long random value, store it only in `.env` on both
   machines, and **never in a repo or vault.**
2. **Never bind `0.0.0.0`** on a host with public ports. Bind the overlay IP.
3. **Scope with ACLs.** Tailscale ACLs should restrict the agent port range to the
   specific nodes that need it.
4. **Key-only SSH** on any box you administer remotely:
   `PasswordAuthentication no`. Drop-ins in `/etc/ssh/sshd_config.d/` are read in
   filename order and **the first value wins** — a cloud image's `50-cloud-init.conf`
   will override `sshd_config` itself, so name your override `00-*.conf` and confirm
   with `sshd -T` (the effective config), not by reading the file.
5. **Default-deny firewall** on the server; allow the overlay range and your operator
   IP. Verify with `iptables -L INPUT -n | head -1` → policy should read `DROP`.

## Common Pitfalls

- **Loopback bind** — the #1 cause. `127.0.0.1` is unreachable cross-machine, and every
  local health check still passes.
- **Asymmetric wiring** — fixing the server side only. Test both directions.
- **`0.0.0.0` "to make it work"** — works, and exposes an agent API to the internet.
  Never the fix.
- **Assuming a port is open because the host is reachable.** `tailscale ping` succeeding
  only proves the *machine* is up — it says nothing about whether anything is listening.
  Probe the port; don't infer it.
- **Expecting a wake push to work on a sleeping machine.** It is fail-soft by design;
  the durable handoff folder remains the fallback.
- **Verifying by "it said it restarted."** Confirm the bind with `ss -tlnp` and the
  round trip with a real DM.

## Why This Matters

Most multi-agent setups are single-host: agents on one box, sharing one loopback. The
moment you span machines — a VPS plus a desktop, a laptop plus a GPU workstation — the
usual answer is file syncing or manual copy-paste.

A cross-machine peer mesh is different: agents stay **addressable**, handoffs **wake**
the right machine, and the durable vault remains the record. It's the same synergy
people are chasing between agents on different platforms, using transports that already
exist underneath.
