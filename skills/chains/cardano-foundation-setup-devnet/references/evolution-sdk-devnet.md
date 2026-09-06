# Evolution SDK Devnet Quickstart

`@evolution-sdk/devnet` is a local Cardano devnet that runs as a **library inside your
TypeScript project** — not a separate CLI tool. Genesis configuration, cluster lifecycle,
and UTxO queries are all TypeScript code. It orchestrates Docker containers for
cardano-node and (optionally) Kupo and Ogmios.

Sourced from the bundled docs under
`${CLAUDE_SKILL_DIR}/../../docs/sources/evolution-sdk/devnet/`.

## When to choose it over Yaci DevKit

Both run standard `cardano-node` instances, so on-chain behaviour is identical. The
choice is about workflow (per `docs/sources/evolution-sdk/devnet/index.mdx`):

| | Yaci DevKit | Evolution SDK devnet |
|---|---|---|
| Form | Standalone CLI tool / service | Library (`@evolution-sdk/devnet`) imported into your project |
| Block explorer | Web-based explorer included | None |
| Chain APIs | Blockfrost-compatible REST built in | Kupo + Ogmios (opt-in containers) |
| Genesis / funded addresses | Configured via CLI / config file | Genesis-as-code; UTxOs deterministic and pre-computable |
| Cluster lifecycle | `create-node -o --start` in the Yaci CLI | `Cluster.make()` / `Cluster.start()` in code |
| Rollback simulation | 3-node cluster mode | Not built in |
| Best for | Visual exploration, broad SDK compatibility | Code-first workflows; devnet living inside your test suite |

Pick Yaci DevKit for visual/CLI-driven exploration. Pick Evolution SDK devnet when the
project is already TypeScript and you want the local chain managed from inside your
integration tests.

## Prerequisites

- **Docker** running (`docker --version`)
- **Node.js** 18 or higher

The devnet runs the **Conway era**. The SDK pulls missing Docker images automatically;
the first run can take several minutes.

## Install

```bash
pnpm add @evolution-sdk/devnet @evolution-sdk/evolution
```

## Minimal cluster

`Cluster.make()` pulls images, creates containers, and generates genesis files. Only a
name and ports are required.

```typescript
import { Cluster } from "@evolution-sdk/devnet";

const cluster = await Cluster.make({
  clusterName: "my-first-devnet",
  ports: { node: 3001, submit: 3002 },
});

await Cluster.start(cluster);          // begins block production
await new Promise((r) => setTimeout(r, 3000)); // let the node initialise

// ... development work ...

await Cluster.stop(cluster);           // preserves state in Docker volumes
await Cluster.remove(cluster);         // removes containers
```

## Full stack with Kupo and Ogmios

Enable the indexer and JSON-RPC services when creating the cluster:

```typescript
const cluster = await Cluster.make({
  clusterName: "full-stack-devnet",
  ports: { node: 3001, submit: 3002 },
  kupo: { enabled: true, port: 1442, logLevel: "Info" },
  ogmios: { enabled: true, port: 1337, logLevel: "info" },
});

await Cluster.start(cluster);
await new Promise((r) => setTimeout(r, 8000)); // Kupo + Ogmios need 6-8s
```

Container status is available via `Container.getStatus(cluster.cardanoNode)` (also
`cluster.kupo`, `cluster.ogmios`).

## Genesis-as-code: funded addresses

Fund any address at block 0 — no faucet needed. Addresses must be in **hex** format.

```typescript
import { Cluster, Config } from "@evolution-sdk/devnet";
import { Address } from "@evolution-sdk/evolution";

// Derive an address from a seed (synchronous, no network)
const addressHex = Address.toHex(
  Address.fromSeed(MNEMONIC, { accountIndex: 0, networkId: 0 }), // 0 = testnet
);

const genesisConfig = {
  ...Config.DEFAULT_SHELLEY_GENESIS,
  slotLength: 0.1,        // 100ms blocks (use 0.02-0.1 for fast tests, 1.0 for realistic)
  epochLength: 100,
  initialFunds: {
    [addressHex]: 1_000_000_000_000, // 1M ADA, in lovelace
  },
} satisfies Config.ShelleyGenesis;

const cluster = await Cluster.make({
  clusterName: "funded-devnet",
  ports: { node: 3001, submit: 3002 },
  shelleyGenesis: genesisConfig,
});
```

Protocol parameters (fees, size limits, Plutus cost models) are customised via
`Config.ShelleyGenesis.protocolParams`, `Config.DEFAULT_ALONZO_GENESIS`, and
`Config.ConwayGenesis` — see `docs/sources/evolution-sdk/devnet/configuration.mdx`.

## Genesis UTxOs do NOT appear in Kupo

Kupo indexes from block 1; genesis UTxOs live in block 0. Derive them explicitly and
pass them to the transaction builder via `availableUtxos`:

```typescript
import { Genesis } from "@evolution-sdk/devnet";

const genesisUtxos = await Genesis.calculateUtxosFromConfig(genesisConfig);

const signBuilder = await client
  .newTx()
  .payToAddress({ address: receiver, assets: Assets.fromLovelace(10_000_000n) })
  .build({ availableUtxos: genesisUtxos });
```

Once a genesis UTxO is spent, the resulting outputs are indexed by Kupo normally.

## Connecting an Evolution SDK client

`Cluster.getChain(cluster)` returns the chain config to feed into `Client.make()`:

```typescript
import { Client } from "@evolution-sdk/evolution";

const client = Client.make(Cluster.getChain(cluster))
  .withKupmios({ kupoUrl: "http://localhost:1442", ogmiosUrl: "http://localhost:1337" })
  .withSeed({ mnemonic: MNEMONIC, accountIndex: 0 });

const params = await client.getProtocolParameters();
const txHash = await client.newTx()
  .payToAddress({ address: receiver, assets: Assets.fromLovelace(5_000_000n) })
  .build({ availableUtxos: genesisUtxos })
  .then((b) => b.sign())
  .then((b) => b.submit());

await client.awaitTx(txHash, 1000); // poll interval in ms
```

For a provider-only client (queries, no signing), omit `.withSeed(...)`.

## Integration test pattern (Vitest)

Create one cluster per test suite for isolated state:

```typescript
import { describe, it, beforeAll, afterAll, expect } from "vitest";
import { Cluster, Config } from "@evolution-sdk/devnet";
import { Address, Assets, Client } from "@evolution-sdk/evolution";

describe("transactions", () => {
  let cluster: Cluster.Cluster;
  let client: Client.SigningClient;

  beforeAll(async () => {
    const addressHex = Address.toHex(
      Address.fromSeed(MNEMONIC, { accountIndex: 0, networkId: 0 }),
    );
    cluster = await Cluster.make({
      clusterName: "test-suite-" + Date.now(),
      ports: { node: 3001, submit: 3002 },
      shelleyGenesis: {
        ...Config.DEFAULT_SHELLEY_GENESIS,
        slotLength: 0.02, // fast blocks → millisecond confirmations
        initialFunds: { [addressHex]: 10_000_000_000_000 },
      },
      kupo: { enabled: true, port: 1442 },
      ogmios: { enabled: true, port: 1337 },
    });
    await Cluster.start(cluster);
    await new Promise((r) => setTimeout(r, 8000));
    client = Client.make(Cluster.getChain(cluster))
      .withKupmios({ kupoUrl: "http://localhost:1442", ogmiosUrl: "http://localhost:1337" })
      .withSeed({ mnemonic: MNEMONIC, accountIndex: 0 });
  }, 180_000); // extended timeout for image pull + startup

  afterAll(async () => {
    await Cluster.stop(cluster);
    await Cluster.remove(cluster);
  }, 60_000);

  it("submits a payment", async () => {
    const txHash = await client.newTx()
      .payToAddress({ address: receiver, assets: Assets.fromLovelace(5_000_000n) })
      .build()
      .then((b) => b.sign())
      .then((b) => b.submit());
    expect(await client.awaitTx(txHash, 1000)).toBe(true);
  }, 30_000);
});
```

Always clean up in `afterAll` to avoid leaking containers.

## Troubleshooting

- **"Cannot connect to provider"** — wait 6-8s after `Cluster.start()` for Kupo/Ogmios.
- **"UTxO not found"** — genesis UTxOs are not in Kupo; use `calculateUtxosFromConfig`
  and `availableUtxos` for the first transaction.
- **Port conflicts** — change `ports`, or the Kupo/Ogmios ports.
- **Container won't start** — confirm the Docker daemon is running with disk space free.
- **Slow first run** — Docker image pulls take minutes once; later starts are fast.

## References

- `${CLAUDE_SKILL_DIR}/../../docs/sources/evolution-sdk/devnet/index.mdx` — overview, Yaci comparison
- `${CLAUDE_SKILL_DIR}/../../docs/sources/evolution-sdk/devnet/getting-started.mdx` — cluster lifecycle
- `${CLAUDE_SKILL_DIR}/../../docs/sources/evolution-sdk/devnet/configuration.mdx` — genesis & protocol params
- `${CLAUDE_SKILL_DIR}/../../docs/sources/evolution-sdk/devnet/integration.mdx` — end-to-end client workflow
