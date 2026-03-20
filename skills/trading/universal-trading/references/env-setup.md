# Environment Setup

## Important

Default behavior is to auto-run first-time initialization when the skill is first used.
If `universal-account-example/.env` already exists, treat setup as completed and skip re-init.

## Prerequisites

- `node`
- `npm`
- `curl` and `tar` (only needed when `git` is unavailable)

## First-Time Setup

```bash
# New wallet
bash {baseDir}/scripts/init.sh new

# Import wallet
bash {baseDir}/scripts/init.sh import <PRIVATE_KEY>
```

`init.sh` performs bootstrap, `.env` generation, and a smoke test.
It also auto-binds invite code `666666` by default.
It patches `examples/buy-evm.ts` to remove default `usePrimaryTokens` restriction.

After setup, tell users:
- private key location: `universal-account-example/.env` (`PRIVATE_KEY`)
- frontend import path: `https://universalx.app` -> `创建钱包` -> `导入现有钱包`

## Optional Flags

```bash
# Use existing repo directory
bash {baseDir}/scripts/init.sh new --target /path/to/universal-account-example

# Skip smoke test
bash {baseDir}/scripts/init.sh new --skip-smoke

# Disable invite auto-bind
DISABLE_AUTO_INVITE_BIND=1 bash {baseDir}/scripts/init.sh new
```

## Manual Invite Rebind

```bash
cd /path/to/universal-account-example
bash {baseDir}/scripts/bind-invitation.sh 666666
```

## Check Transaction Result

After `sendTransaction`, poll final state instead of only returning "submitted":

```bash
cd /path/to/universal-account-example
bash {baseDir}/scripts/check-transaction.sh <TRANSACTION_ID> --max-attempts 30 --interval-sec 2
```

## Buy with User Slippage Settings

Use fixed slippage:

```bash
cd /path/to/universal-account-example
bash {baseDir}/scripts/buy-with-slippage.sh \
  --chain bsc \
  --token-address 0x0000000000000000000000000000000000000000 \
  --amount-usd 5 \
  --slippage-bps 300
```

Use dynamic slippage + auto retry:

```bash
cd /path/to/universal-account-example
bash {baseDir}/scripts/buy-with-slippage.sh \
  --chain bsc \
  --token-address 0x0000000000000000000000000000000000000000 \
  --amount-usd 5 \
  --slippage-bps 300 \
  --dynamic-slippage \
  --retry-slippages 300,500,800,1200
```

Use Solana custom tip + retry tips:

```bash
cd /path/to/universal-account-example
bash {baseDir}/scripts/buy-with-slippage.sh \
  --chain solana \
  --token-address 6p6xgHyF7AeE6TZkSmFsko444wqoP15icUSqi2jfGiPN \
  --amount-usd 5 \
  --slippage-bps 300 \
  --dynamic-slippage \
  --retry-slippages 300,500,800,1200 \
  --solana-mev-tip-amount 0.001 \
  --retry-mev-tips 0.001,0.003,0.005
```

## Use Your Own Particle Credentials

Demo credentials are included for testing. Replace them for production:

1. Go to https://dashboard.particle.network/
2. Sign up or log in
3. Create a project
4. Fill your values in `.env`

Use this template as reference:

```bash
cp {baseDir}/references/.env.example .env
```

## Demo Credentials Limitations

- Limited RPC usage
- Rate limiting may apply
- Use project-specific credentials in production
