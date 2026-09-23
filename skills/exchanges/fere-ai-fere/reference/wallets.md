# Wallets — one, or one per user

Everything Fere knows about a user is a **public key**. Register a key, get a wallet
pair. There is no account, no email, no password reset. Losing the key loses the
funds; holding the key is full control.

```
POST /v1/auth/register {agent_name, public_key}   -> {registration_id:"reg_…", challenge}
POST /v1/auth/verify   {registration_id, challenge, signature}  -> {agent_id:"agent_<16>"}
POST /v1/auth/token    {agent_id, timestamp:"<unix s>", signature} -> {token:"agt_…", expires_in:3600}
GET  /v1/wallets       -> {wallets:[{address, chain_type:"evm"|"solana"}], provisioning:bool}
```

- Signatures are Ed25519, base64, over **the raw challenge string** and over **the bare
  timestamp string** respectively. `auth.md`'s prose shape (with a `nonce`) is wrong;
  the openapi/SDK shape above is what works.
- End-to-end in ~2.5 s; wallets come back `provisioning:false` almost immediately
  (docs say poll up to 60 s — do poll, don't assume).
- A wrong `agent_id` → `401 unknown_agent`. A timestamp more than a few minutes old →
  `401 stale_timestamp`; surface that as **"this machine's clock is off"**, not as an
  auth failure — it sends people debugging the wrong thing.
- Errors are nested: `{"detail":{"error":{"code","message","details"}}}`. Match on
  `code`, not on prose.
- **One EVM address serves every EVM chain**, Robinhood Chain included. One Solana
  address for Solana. That's the whole address book.

## One wallet

```bash
python3 scripts/fere.py new alice          # register + save to the keyring
python3 scripts/fere.py wallets alice      # addresses
python3 scripts/fere.py holdings alice     # balances everywhere
```

For a server that owns exactly one wallet, skip the keyring and set
`FERE_AGENT_SEED_B64` + `FERE_AGENT_ID` in the environment (or `FERE_TOKEN` for a
short-lived pre-minted bearer). `fere.py` reads all three.

## More than one wallet?

Two wallets is two agents — there are no sub-accounts. If you are giving a wallet to
each of your users, that is its own discipline (key custody, per-user venue setup,
funding floors, polling budgets): use **`/fere-multitenant`**, which owns it. This file
covers the mechanics that are the same either way.

## The portable key string

One string that restores a wallet anywhere:

```
fere_<base58check( version ‖ seed32 [‖ utf8(agent_id)] )>     # ~80-85 chars with the id, ~55-56 without
        version 0x01 = seed + agent_id (preferred)
        version 0x00 = seed only  -> agent_id recovered by re-registering the same key
```

`base58check` = payload + first 4 bytes of double-SHA256, so a typo is caught instead
of silently pointing at an empty wallet. The length varies a little with the agent id
and with leading zero bytes — don't validate by length, decode it. Change `FERE_KEY_PREFIX` to brand it
(`myapp_…`); `fere.py import` accepts any prefix.

```bash
python3 scripts/fere.py key alice --reveal      # SECRET — prints to stderr with a warning
python3 scripts/fere.py import alice2 --key fere_…
python3 scripts/fere.py recover alice2          # rebuild agent_id from the seed alone
```

**Recovery from a seed-only key (verified live):** re-register the *same* public key
and Fere answers `409 {"code":"duplicate_key","message":"Public key already registered
as agent_<16>"}`; the original agent keeps minting tokens. `fere.py` parses the id out
of that envelope. Treat it as a fallback — **store the `agent_id` next to the seed** so
your product never depends on an error string.

## Custody, honestly

Fere's wallets are **Coinbase CDP Server Wallets in AWS Nitro TEEs**. Keys are
generated and held in the enclave; Fere's backend holds the credential that *instructs*
signing. That is exactly how a stop-loss fires while your user is asleep — someone has
to sign, and it isn't them.

So "non-custodial" here means: **no arbitrary-transfer endpoint exists**, and the key is
exportable in the web app. It does **not** mean Fere's infrastructure cannot sign. Say
it that way to users; the honest version survives contact with a security review.

- **No API key export** for key-registered agents today (web app only, behind a Clerk login
  an API-registered agent doesn't have). If your product promises hold-to-reveal, that
  promise is currently unbacked for API-provisioned wallets.
- **No transfer/withdraw to an arbitrary address.** `/v1/chains` lists `transfer` under
  `supported_operations`; no endpoint implements it. Funds move between *venues*
  (perp ↔ wallet, Polymarket safe ↔ wallet) and out via swaps only.
- **No per-agent spending policy** is exposed. If you need caps, enforce them in your
  own code before you call.

## Browsers: there is no CORS

Fere's gateway answers preflights but **never sends `Access-Control-Allow-Origin`**
(tested from several origins). A browser cannot call it. Put a stateless passthrough in
front of it that:

- allowlists method+path with a `fullmatch`, and **hard-denies `v1/chat`** (15 credits
  a query — the one endpoint *known* to cost credits to call);
- forwards only `authorization`, `content-type`, `accept`;
- uses a 20 s default timeout, 95 s on `swap` and `limit-orders`;
- relays SSE as a stream with a cap, caps bodies at ~64 KiB, rate-limits per IP on the
  **last** `X-Forwarded-For` hop;
- logs `method path status ms` and **never the bearer**.

**A consumer product has shipped exactly this** — allowlist as written, CSP,
idempotency and fill rules, the funding journey: `reference/consumer-app.md`. Copy
that rather than re-deriving the passthrough.

The token is a bearer for a wallet with money in it. If it leaks, it is a 1-hour
window in which anyone can trade the wallet. They cannot transfer out (see above), but
they can swap the balance into a token they control — a drain by another route. Treat
a leak as a loss; there is no key rotation, only a new agent.

## Gasless, actually

No native coin is needed for gas on the swap chains. Any liquid token can be deposited
and sold, and Fere takes its fee out of whatever is being swapped. **Keep no gas
reserve** — the balance is spendable to the cent. Robinhood Chain is not a CDP network
(`cdp_network_name: ""`); our live RH trades held RH-native ETH, and a zero-ETH fresh
agent on RH is **untested**. Don't promise gasless on RH without checking it first.
