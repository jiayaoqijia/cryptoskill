# Local Devnode Setup

## Overview

The nitro-devnode provides a local Arbitrum chain for development and testing. It runs via Docker and exposes an RPC endpoint at `http://localhost:8547`.

## Prerequisites

- Docker Desktop running
- Ports 8547 and 8548 available

## Setup

```bash
git clone https://github.com/OffchainLabs/nitro-devnode.git
cd nitro-devnode
./run-dev-node.sh
```

The node is ready when you can query it:

```bash
cast chain-id --rpc-url http://localhost:8547
# Should return: 412346
```

## Pre-funded Accounts

The devnode ships with pre-funded accounts for development. The master deployer account:

```
Address:     0x3f1Eae7D46d88F08fc2F8ed27FCb2AB183EB2d0E
Private key: 0xb6b15c8cb491557369f3c7d2c287b053eb229daa9c22138887752191c9520659
```

This account has a large ETH balance for contract deployment and testing.

## Additional Test Accounts

For multi-user testing, fund additional accounts from the deployer:

```bash
cast send --rpc-url http://localhost:8547 \
  --private-key 0xb6b15c8cb491557369f3c7d2c287b053eb229daa9c22138887752191c9520659 \
  --value 1ether \
  0xYOUR_TEST_ADDRESS
```

## Troubleshooting

### Node won't start

```bash
# Stop and remove existing containers
docker compose down -v
# Restart
./run-dev-node.sh
```

### Port conflicts

If port 8547 is in use, check for existing containers:

```bash
docker ps | grep nitro
```

### Verifying the node is working

```bash
# Check block number is advancing
cast block-number --rpc-url http://localhost:8547

# Check deployer balance
cast balance --rpc-url http://localhost:8547 \
  0x3f1Eae7D46d88F08fc2F8ed27FCb2AB183EB2d0E
```

## CORS and Browser Access

The nitro-devnode does **not** return CORS headers. Browser-based frontends (React, Next.js) running on `localhost:3000` will have their RPC requests to `localhost:8547` blocked by the browser's same-origin policy.

**Solution:** Proxy RPC calls through a Next.js API route:

```typescript
// app/api/rpc/route.ts
import { NextRequest, NextResponse } from "next/server";

const RPC_URL = "http://localhost:8547";

export async function POST(req: NextRequest) {
  const body = await req.text();
  const res = await fetch(RPC_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body,
  });
  const data = await res.text();
  return new NextResponse(data, {
    status: res.status,
    headers: { "Content-Type": "application/json" },
  });
}
```

Then point the wagmi/viem transport at the proxy:

```typescript
transports: {
  [arbitrumLocal.id]: http("/api/rpc"),
}
```

This only affects browser reads. CLI tools (`cast`, `forge`) connect directly to `localhost:8547` without issues.

## RPC Endpoint Reference

| Endpoint | Port | Purpose |
|----------|------|---------|
| L2 RPC | 8547 | Main interaction endpoint |
| L2 WS | 8548 | WebSocket subscriptions |
