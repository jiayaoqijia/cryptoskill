# Scoped, expiring authority

Derived from [`/for-agents/concepts/privileges`](https://docs.waap.human.tech/for-agents/concepts/privileges)
and [`/for-agents/commands`](https://docs.waap.human.tech/for-agents/commands).

## The problem it solves

Asking a human to approve every action is correct for a large transfer and
unusable for anything else. A trading loop, a game, or an agent doing metered
work cannot stop for a confirmation each time.

A **Privilege** is the answer: a pre-signed permission slip. The person approves
a shape once, and actions matching that shape proceed without a prompt.

## The four axes

A Privilege must bound all four. One missing axis makes it broader than it looks.

| CLI flag | What it bounds |
|---|---|
| `--allow <scope...>` | Which recipients may be paid. An empty allowlist means anyone. Scopes: an address, `target:*`, an EVM `target:selector`, a Sui `target:module::function`, or a Solana `target:disc:0x...` |
| `--chain <chain>` | Which chain the grant is valid on. Required |
| `--amount-usd <amount>` | A **cumulative** total across every action under the grant, not a per-action limit. Default `1` |
| `--expiry-seconds <seconds>` | How long it lives. Default `900`, maximum `7200` |

The ceiling being **cumulative** is the part most often misread. It is a budget
for the whole grant, so an agent making many small actions consumes it exactly as
fast as one making a few large ones.

## Minting one from the CLI

A headless agent does not need a browser. Mint and spend entirely from the CLI:

```bash
PRIVILEGE=$(waap-cli squid privilege create \
  --chain sui:mainnet \
  --allow 0xRecipient \
  --amount-usd 50 \
  --expiry-seconds 3600 \
  --json | jq -r .permissionToken)
```

`privilege create --json` returns an object. `permissionToken` is the encoded
grant, alongside `chain`, `walletMode`, `expiry`, `allowedAddresses` and
`allowedScopes`. Extract the token before piping it.

**The wallet mode is the command path, not an option.** There is no
`--wallet-mode`:

```bash
waap-cli privilege create ...        # standard mode
waap-cli squid privilege create ...  # Squid
```

A Privilege minted on one path cannot be redeemed by the other, so mint it on the
same path the transaction will use.

By default a Privilege lets ordinary threshold findings proceed without another
2FA prompt when the policy engine accepts its scope. Add
`--require-2fa-for-high-risk-tx` to keep that challenge.

## Spending it

```bash
printf '%s' "$PRIVILEGE" | waap-cli send-tx \
  --to 0xRecipient \
  --value 0.01 \
  --chain sui:mainnet \
  --privilege-stdin
```

The transaction goes through immediately. No approval prompt, no waiting.

⚠️ **Treat a Privilege as a bearer secret.** Piping it with `--privilege-stdin`
keeps it out of shell history, `ps` output, and logs. The older
`--privilege <encoded>` and `--permission-token <encoded>` flags still work but
are deprecated, and both put the token in process arguments where anything on the
box can read it.

## From a browser application

For browser-based apps, a Privilege is requested via
`window.waap.requestPermissionToken()`:

```ts
window.waap.requestPermissionToken({
  allowedAddresses: ['0x...'],
  chainId: 1,
  requestedAmountUsd: 50,
  requestedExpirySeconds: 3600,
})
```

The origin is bound server-side to the domain that requested it, so a grant
issued to one application cannot be replayed by another. Agents should use the
CLI path above instead.

## The lifetime ceiling

**A Privilege lasts at most two hours, enforced server-side. And the default is
fifteen minutes.** Pass `--expiry-seconds` deliberately; an agent that assumes
two hours and omits the flag will stop at minute fifteen and look like it broke.

It is a session, not a standing mandate. Inside that session it does what
recurring billing wants: many charges against one approval, under a ceiling the
user set. Across a month it does not, because the grant expires long before the
next charge.

Works today: pay-per-use inside a visit, metered API calls, an agent running a
bounded task, in-game purchases during a session.

**Expiry is the control.** There is no per-grant recall. Plan the lifetime for
the blast radius you can accept, rather than assuming a short scope can be pulled
back early. Keep them short and mint again.

## Privileges are not a way around policy

A Privilege carves a narrow, expiring exemption from the **approval step** inside
limits the policy already sets. It never widens the policy itself. An agent
holding one is still subject to the daily spend limit, and a request outside its
scope falls back to the normal gate.

If a design needs the grant to exceed the policy, the policy is what should
change, deliberately, with a human making that call.

## Handoff

Because the underlying authority in WaaP Squid Mode is a Sui object rather than a
server-side flag, it can be transferred. That is what keeps a user from being
locked to one operator.

Do not let a Privilege travel with an agent that changes hands. A scope granted
to an agent under one operator should not survive the agent moving to another,
and since the grant cannot be recalled, the only safe assumption is that it stays
live until it expires.
