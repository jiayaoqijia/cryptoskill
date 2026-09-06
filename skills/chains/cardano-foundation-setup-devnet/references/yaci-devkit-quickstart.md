# Yaci DevKit Quickstart

Yaci DevKit provides a local Cardano devnet using Docker for fast smart contract
development and testing. Commands and ports below match the current DevKit —
always cross-check `docs/sources/yaci-devkit/getting-started/docker.mdx` and
`docs/sources/yaci-devkit/services.mdx`, as the CLI evolves.

## Prerequisites

- Docker and Docker Compose installed
- At least 4GB RAM available for Docker

## Installing and starting the DevKit

The DevKit ships as a `devkit` script (curl installer or zip distribution) that
manages the Docker containers and drops you into the Yaci CLI:

```bash
# Install (curl-based)
curl --proto '=https' --tlsv1.2 -LsSf https://devkit.yaci.xyz/install.sh | bash

# Start containers + Yaci CLI
devkit start          # zip install: ./devkit.sh start

# Other script options: stop | cli | ssh | info | version
```

## Creating a devnet (inside the Yaci CLI)

```bash
# Create and start a default devnet (1-second blocks)
yaci-cli:> create-node -o --start

# Faster blocks (always set both flags for sub-second times)
yaci-cli:> create-node -o --block-time 0.2 --slot-length 0.2 --start
```

Once running you land in the `devnet:default>` context:

```bash
devnet:default> topup <address> <ada_amount>   # fund an address with test ADA
devnet:default> utxos <address>                # check UTxOs
devnet:default> info                           # devnet status
devnet:default> reset                          # clean state
devnet:default> stop                           # stop the devnet
```

Note: `devnet:default` is the CLI *prompt*, not a command prefix — the commands
are bare (`topup`, `info`, …).

## Service URLs and ports

| Service | URL |
|---|---|
| **Yaci Store API (Blockfrost-compatible)** | `http://localhost:8080/api/v1/` |
| Yaci Store Swagger UI | `http://localhost:8080/swagger-ui.html` |
| Yaci Viewer (block explorer) | `http://localhost:5173` |
| CLI/Admin Swagger UI | `http://localhost:10000/swagger-ui.html` |
| Wallet page / MCP endpoint | `http://localhost:10000/wallet` / `http://localhost:10000/mcp` |
| Ogmios (if enabled) | `ws://localhost:1337` |
| Kupo (if enabled) | `http://localhost:1442` |
| Cardano node (n2n) | `localhost:3001` |

The application/query API you point SDKs at is port **8080** (Yaci Store).
Port 10000 serves the CLI/admin/wallet/MCP endpoints, not chain queries.
Ports are configurable via the `config/env` file (`HOST_STORE_API_PORT`, …).

## Era and block-time configuration

- Current DevKit devnets run the Conway era (governance, Plutus V3)
- `--block-time` / `--slot-length` / `--epoch-length` flags on `create-node`
  control timing (see docker.mdx for constraints)
- Auto-fund addresses at startup via `topup_addresses=addr1:amount,...` in
  `config/env`

## Enabling Ogmios and Kupo

Prefer the DevKit's built-in services over hand-run containers:

```bash
# Inside Yaci CLI
yaci-cli:> enable-kupomios

# Or in config/env
ogmios_enabled=true
kupo_enabled=true
```

Since DevKit v0.12.0-beta5, Yaci Store evaluates scripts with `scalus` when
Ogmios is not running — Ogmios is optional for transaction evaluation.

## Connecting SDKs

### Mesh SDK (JavaScript/TypeScript)

```typescript
import { YaciProvider } from "@meshsdk/core";

const provider = new YaciProvider("http://localhost:8080/api/v1");
```

### Evolution SDK (TypeScript)

If running Ogmios + Kupo (enable-kupomios), point the client at them via `.withKupmios(...)`. Evolution SDK also ships its own first-party local devnet (`@evolution-sdk/devnet`) as a code-first alternative to Yaci DevKit — see `evolution-sdk-devnet.md` in this directory.

```typescript
import { Client, preprod } from "@evolution-sdk/evolution"

// Pick `preprod` (or `preview`) depending on which network Yaci is emulating.
const client = Client.make(preprod).withKupmios({
  ogmiosUrl: "http://localhost:1337",
  kupoUrl: "http://localhost:1442",
})
```

### PyCardano (Python)

```python
from pycardano import BlockFrostChainContext

# Yaci Store is compatible with Blockfrost API format
context = BlockFrostChainContext(
    base_url="http://localhost:8080/api/v1",
    project_id="yaci"  # Any string works locally
)
```

## Exercising a Smart Contract

Cardano has no script deployment step -- a validator rides in the witness set of the
transaction that spends from it. "Running a contract" means locking funds at the script
address, then spending them with the validator and a redeemer attached.

### Using Aiken + SDK

```bash
# 1. Build the Aiken project
aiken build

# 2. The plutus.json blueprint is generated
# 3. Use your SDK to read the blueprint, derive the script address,
#    lock funds to it, then spend them back

# Or query the node directly with the bundled cardano-cli
devkit cli    # runs cardano-cli against the DevKit node
```

## Common Issues

### Port conflicts

Update port variables in the DevKit's `config/env` file
(`HOST_STORE_API_PORT=8080`, `HOST_VIEWER_PORT=5173`,
`HOST_CLUSTER_API_PORT=10000`, …) and restart the containers.

### Devnet not producing blocks

```bash
# Inside the CLI, restart the devnet
devnet:default> stop
yaci-cli:> create-node -o --start   # or restart the existing node
```

### Transactions failing with "era mismatch"

Ensure your transaction is built for the same era as the devnet. Check with
`info` and match your SDK/CLI configuration.

### Resetting state

```bash
devnet:default> reset        # clean reset, keeps configuration
# or stop the DevKit and remove its state entirely
devkit stop
```

## CI/CD Usage

Run the DevKit containers in CI and wait for the Store API before tests:

```bash
# Wait script — Store API is the readiness signal
until curl -sf http://localhost:8080/api/v1/blocks/latest; do
  echo "Waiting for Yaci DevKit..."
  sleep 2
done
echo "DevKit ready"
```

See `docs/sources/yaci-devkit/` for the current recommended CI setup (the
distribution is compose-based; a single-image `docker run` is no longer the
documented path).
