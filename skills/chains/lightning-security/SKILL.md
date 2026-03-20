---
name: lightning-security-module
description: Set up an lnd remote signer container that holds private keys separately from the agent. Exports a credentials bundle (accounts JSON, TLS cert, admin macaroon) for watch-only litd nodes. Container-first with Docker, native fallback. Use when firewalling private key material from AI agents.
---

# Lightning Security Module (Remote Signer)

Set up an lnd remote signer container that holds private keys on a separate,
secured machine. The signer never routes payments or opens channels — it only
holds keys and signs when asked by a watch-only litd node.

## Architecture

```
Agent Machine                     Signer Machine (secure)
┌─────────────────┐              ┌─────────────────────┐
│  litd (watch-only)│◄──gRPC───►│  lnd (signer)        │
│  - neutrino      │             │  - holds seed         │
│  - manages chans │             │  - signs commitments  │
│  - routes pmts   │             │  - signs on-chain txs │
│  - NO key material│            │  - no p2p networking   │
└─────────────────┘              └─────────────────────┘
```

The watch-only node handles all networking and channel management. The signer
node holds the seed and performs cryptographic signing. Even if the agent machine
is fully compromised, the attacker cannot extract private keys.

See [references/architecture.md](references/architecture.md) for the full
architecture explainer.

## Quick Start (Container — Recommended)

### On the Signer Machine

```bash
# 1. Install lnd signer image
skills/lightning-security-module/scripts/install.sh

# 2. Start signer container
skills/lightning-security-module/scripts/start-signer.sh

# 3. Set up signer wallet and export credentials
skills/lightning-security-module/scripts/setup-signer.sh

# 4. Copy the credentials bundle to the agent machine
#    The setup script prints the bundle path and base64 string.
```

### On the Agent Machine

```bash
# 5. Import credentials bundle
skills/lnd/scripts/import-credentials.sh --bundle <credentials-bundle>

# 6. Start litd in watch-only mode
skills/lnd/scripts/start-lnd.sh --watchonly

# 7. Create watch-only wallet
skills/lnd/scripts/create-wallet.sh

# 8. Check status
skills/lnd/scripts/lncli.sh getinfo
```

### Two-Container Local Setup

For testing both on the same machine:

```bash
# Start litd + signer together
skills/lnd/scripts/start-lnd.sh --watchonly

# Set up signer wallet
skills/lightning-security-module/scripts/setup-signer.sh --container litd-signer

# Import credentials and create watch-only wallet
skills/lnd/scripts/import-credentials.sh --bundle ~/.lnget/signer/credentials-bundle
skills/lnd/scripts/create-wallet.sh --container litd
```

## Installation

Default: pulls the lnd Docker image for the signer.

```bash
skills/lightning-security-module/scripts/install.sh
```

This pulls `lightninglabs/lnd:v0.20.0-beta` from Docker Hub. The signer only
needs plain lnd (not litd) since it only holds keys and signs.

### Build from Source (Fallback)

```bash
skills/lightning-security-module/scripts/install.sh --source
```

## Native Mode

For running the signer without Docker:

```bash
# Set up signer natively
skills/lightning-security-module/scripts/setup-signer.sh --native

# Start signer natively
skills/lightning-security-module/scripts/start-signer.sh --native

# Stop signer natively
skills/lightning-security-module/scripts/stop-signer.sh --native
```

## Remote Nodes

Export credentials from a remote signer:

```bash
skills/lightning-security-module/scripts/export-credentials.sh \
    --rpcserver signer-host:10012 \
    --tlscertpath ~/signer-tls.cert \
    --macaroonpath ~/signer-admin.macaroon
```

## Credential Bundle Format

The exported bundle (`~/.lnget/signer/credentials-bundle/`) contains:

| File | Purpose |
|------|---------|
| `accounts.json` | Account xpubs for watch-only wallet import |
| `tls.cert` | Signer's TLS certificate for authenticated gRPC |
| `admin.macaroon` | Signer's admin macaroon for RPC authentication |

The bundle is also available as a single base64-encoded tar.gz file
(`credentials-bundle.tar.gz.b64`) for easy copy-paste transfer between machines.

## Scripts

| Script | Purpose |
|--------|---------|
| `install.sh` | Pull lnd signer image (or build from source) |
| `docker-start.sh` | Start signer container |
| `docker-stop.sh` | Stop signer container |
| `setup-signer.sh` | Create signer wallet and export credentials |
| `start-signer.sh` | Start signer (delegates to Docker by default) |
| `stop-signer.sh` | Stop signer (delegates to Docker by default) |
| `export-credentials.sh` | Re-export credentials from running signer |

## Managing the Signer

### Start

```bash
# Docker (default)
skills/lightning-security-module/scripts/start-signer.sh

# With network override
skills/lightning-security-module/scripts/start-signer.sh --network mainnet
```

### Stop

```bash
# Docker stop (preserve data)
skills/lightning-security-module/scripts/stop-signer.sh

# Docker stop + remove volumes
skills/lightning-security-module/scripts/stop-signer.sh --clean
```

### Re-export Credentials

If TLS certificates or macaroons have been regenerated:

```bash
skills/lightning-security-module/scripts/export-credentials.sh
```

## Configuration

### Container Config

The signer compose template is at
`skills/lightning-security-module/templates/docker-compose-signer.yml`. Config
is passed via command-line arguments.

### Native Config

The native signer config template is at
`skills/lightning-security-module/templates/signer-lnd.conf.template`. Key
differences from a standard lnd node:

- **No P2P listening** (`--listen=`) — signer doesn't route
- **RPC on 0.0.0.0:10012** — accepts connections from watch-only node
- **REST on localhost:10013** — local only, for wallet creation
- **TLS extra IP 0.0.0.0** — watch-only on a different machine can connect
- **No autopilot, no routing fees** — signer is signing-only

## Security Model

**What stays on the signer:**
- 24-word seed mnemonic
- All private keys (funding, revocation, HTLC)
- Wallet database with key material

**What gets exported:**
- Account xpubs (public keys only — cannot spend)
- TLS certificate (for authenticated connection)
- Admin macaroon (for RPC auth — scope down for production)

**Threat model:**
- Compromised agent machine cannot sign transactions or extract keys
- Attacker with agent access can see balances and channel state but not spend
- Signer machine should have minimal attack surface

**Production hardening:**
- Replace admin macaroon with a signer-only macaroon (see `macaroon-bakery`)
- Restrict signer RPC to specific IP addresses via firewall
- Run signer on dedicated hardware or a hardened VM
- Use Lightning Node Connect (LNC) via `lightning-mcp-server` for read-only agent access

## Macaroon Bakery for Signer

For production, bake a signing-only macaroon:

```bash
skills/macaroon-bakery/scripts/bake.sh --role signer-only \
    --container litd-signer --rpc-port 10012
```

Then re-export the credentials bundle with the scoped macaroon.

## Container & Ports

| Container | Purpose | Ports |
|-----------|---------|-------|
| `litd-signer` | Remote signer (lnd) | 10012, 10013 |

| Port  | Service | Interface | Description |
|-------|---------|-----------|-------------|
| 10012 | gRPC | 0.0.0.0 | Signer RPC (watch-only connects here) |
| 10013 | REST | 0.0.0.0 | REST for wallet creation |

## File Locations

| Path | Purpose |
|------|---------|
| `~/.lnget/signer/wallet-password.txt` | Signer wallet passphrase (0600) |
| `~/.lnget/signer/seed.txt` | Signer seed mnemonic (0600) |
| `~/.lnget/signer/credentials-bundle/` | Exported credentials |
| `~/.lnget/signer/signer-lnd.conf` | Signer config (native mode) |
| `versions.env` | Pinned container image versions |
