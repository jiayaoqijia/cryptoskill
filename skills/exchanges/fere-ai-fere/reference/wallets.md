# Wallets

Fere identifies an agent by a public key. Register the key, get one EVM address and one Solana address. There is no email and no password reset. Losing the key loses the funds.

```
POST /v1/auth/register {agent_name, public_key}   -> {registration_id:"reg_…", challenge}
POST /v1/auth/verify   {registration_id, challenge, signature}  -> {agent_id:"agent_<16>"}
POST /v1/auth/token    {agent_id, timestamp:"<unix s>", signature} -> {token:"agt_…", expires_in:3600}
GET  /v1/wallets       -> {wallets:[{address, chain_type:"evm"|"solana"}], provisioning:bool}
```

- Signatures are Ed25519, base64. Sign the raw challenge string, and later the bare timestamp string.
- Poll `GET /v1/wallets` until `provisioning` is false. Do not assume the pair is ready on the first read.
- Wrong `agent_id` → `401 unknown_agent`. A timestamp more than a few minutes old → `401 stale_timestamp`. Tell the user the machine clock is off.
- Errors are nested: `{"detail":{"error":{"code","message","details"}}}`. Match on `code`.
- One EVM address covers every EVM chain, including Robinhood Chain. One Solana address covers Solana.

## One wallet

```bash
python3 scripts/fere.py new alice
python3 scripts/fere.py wallets alice
python3 scripts/fere.py holdings alice
```

A server that owns exactly one wallet can skip the keyring and set `FERE_AGENT_SEED_B64` and `FERE_AGENT_ID`, or `FERE_TOKEN` for a short-lived bearer. `fere.py` reads all three.

Two wallets means two agents. There are no sub-accounts. A wallet per end user is the `fere-multitenant` skill.

## The portable key string

```
fere_<base58check( version ‖ seed32 [‖ utf8(agent_id)] )>
        version 0x01 = seed + agent_id (preferred)
        version 0x00 = seed only → recover agent_id by re-registering the same key
```

`base58check` is the payload plus the first 4 bytes of double-SHA256. Do not validate by length; length varies with the agent id. Change `FERE_KEY_PREFIX` to brand it (`myapp_…`); `fere.py import` accepts any prefix.

```bash
python3 scripts/fere.py key alice --reveal      # prints the secret to stderr
python3 scripts/fere.py import alice2 --key fere_…
python3 scripts/fere.py recover alice2
```

Recovery of a seed-only key: re-register the same public key. Fere answers `409 {"code":"duplicate_key","message":"Public key already registered as agent_<16>"}`. Parse the id out of that body. Store `agent_id` next to the seed so recovery does not depend on that error string.

## Custody

Wallets are Coinbase CDP server wallets. Fere's backend holds the credential that instructs signing, which is how a stop-loss can fire while the user is offline.

"Non-custodial" here means there is no arbitrary-transfer endpoint, and the key is exportable in the web app. It does not mean Fere's infrastructure cannot sign.

- No API key export for key-registered agents. Export is the web app, behind a Clerk login an API agent does not have.
- No transfer to an arbitrary address. `/v1/chains` lists `transfer` under `supported_operations`; no endpoint implements it. Funds move between venues and out by swap only.
- No per-agent spend cap. Enforce caps in your own code before you call.

## Browsers

The gateway never sends `Access-Control-Allow-Origin`. A browser cannot call it. Put a stateless passthrough in front. The rules for that passthrough are in `reference/consumer-app.md`.

The bearer is a one-hour licence to trade the wallet. A leak cannot transfer funds out, but it can swap the balance into a token the holder controls. Treat a leak as a loss. There is no key rotation, only a new agent.

## Gas

No native coin is required for gas on the swap chains. Any liquid token can be deposited and sold. Do not keep a gas reserve.

Robinhood Chain is not a CDP network (`cdp_network_name: ""`). Do not promise gasless execution there until a zero-ETH agent has completed a swap on it.
