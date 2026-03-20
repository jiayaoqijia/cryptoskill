# kraken-skill

`openclaw-kraken` is a Bash CLI and ClawHub-ready skill for Kraken APIs. The source repo is https://github.com/oscraters/kraken-skill.git and it exposes a registry-driven command surface for agentic use across Spot REST, Futures REST, and Kraken WebSocket workflows.

- `0.1.0`: public market-data commands
- `0.2.0`: authenticated read-only account commands
- `0.3.0`: guarded trading commands

## Layout

- `SKILL.md`: ClawHub/OpenClaw skill entrypoint
- `bin/openclaw-kraken`: CLI
- `lib/`: auth, config, HTTP, validation, redaction
- `config/endpoints.tsv`: local endpoint registry used by `endpoints`, `describe`, and `call`
- `config/futures_endpoints.tsv`: futures endpoint registry used by `futures endpoints`, `futures describe`, and `futures call`
- `config/kraken.env.example`: environment template
- `docs/`: security, configuration, and usage notes
- `scripts/release.sh`: version bump and `clawhub publish` helper
- `scripts/ws_client.mjs`: generic websocket transport for spot/futures feeds
- `test/`: smoke and security tests

## Requirements

- `bash`
- `curl`
- `openssl`
- `base64`
- `od`
- `jq` optional for `--jq` and `--compact`

## Configuration

Source environment manually or point `OPENCLAW_KRAKEN_CONFIG` at a shell env file.

```bash
export OPENCLAW_KRAKEN_CONFIG="$PWD/config/kraken.env.example"
```

Private endpoints require:

```bash
export KRAKEN_API_KEY="..."
export KRAKEN_API_SECRET="..."
export KRAKEN_FUTURES_API_KEY="..."
export KRAKEN_FUTURES_API_SECRET="..."
```

In OpenClaw, inject those values via secret refs rather than storing plaintext in config. OpenClaw resolves env, file, and exec refs eagerly into an in-memory snapshot and fails activation if a referenced secret cannot be resolved: https://docs.openclaw.ai/gateway/secrets

## Examples

```bash
bin/openclaw-kraken endpoints trading.
bin/openclaw-kraken describe funding.withdraw
bin/openclaw-kraken call account.balance
bin/openclaw-kraken raw private QueryOrders --set txid OABCDEF-123456-XYZ789
bin/openclaw-kraken futures endpoints trading.
bin/openclaw-kraken futures call market.tickers --compact
bin/openclaw-kraken futures call trading.send-order --symbol PI_XBTUSD --side buy --size 10 --orderType lmt --limitPrice 30000 --confirm
bin/openclaw-kraken ws spot-public --message-json '{"method":"ping"}'
bin/openclaw-kraken ws spot-private --message-json '{"method":"subscribe","params":{"channel":"executions"}}'
bin/openclaw-kraken ws futures-sign-challenge '<challenge-string>'
bin/openclaw-kraken market time
bin/openclaw-kraken market ticker --pair XBTUSD --compact
bin/openclaw-kraken account balance
bin/openclaw-kraken account open-orders --jq '.result.open | length'
bin/openclaw-kraken orders add --pair XBTUSD --side buy --type limit --volume 0.01 --price 25000 --time-in-force GTC --post-only true --confirm
bin/openclaw-kraken orders cancel --txid OABCDEF-123456-XYZ789 --confirm
```

## Security

- stdout is reserved for API responses
- stderr is sanitized and excludes auth headers, API secrets, and request signatures
- optional `jq` formatting happens after the HTTP response is received and keeps secrets out of stderr
- websocket helpers never echo outbound private auth payloads to stdout or stderr
- state-changing commands require `--confirm`
- base URLs are declared in config and validated before use

See [docs/security.md](/home/noir/enna/skills/kraken/docs/security.md).

## Publishing

This repo is structured so the whole folder can be published to ClawHub. A skill is a folder with a `SKILL.md` file and optional supporting files: https://docs.openclaw.ai/tools/clawhub

Release helper:

```bash
scripts/release.sh 0.3.1 "Expanded endpoint coverage"
```

That updates [VERSION](/home/noir/enna/skills/kraken/VERSION) and prints the `clawhub publish` and `git tag` commands to run.
