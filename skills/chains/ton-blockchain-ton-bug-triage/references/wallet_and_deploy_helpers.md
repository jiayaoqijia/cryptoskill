# Wallet Smoke Path

Use this reference when you need the proven simple-wallet deploy/send flow on a local `tontester` network.

This document is intentionally narrow.

- For generic contract deployment, read `contract_deploy_flow.md`.
- For binary trigger payloads, prefer `wallet_send.py --body-boc`.
- If you already have a serialized external message BoC, use `send_boc.py --boc`.
- `--body-boc` overrides `--comment`.

## Fastest Verified Path

If you want a known-good smoke test for the full flow, run:

```bash
python3 /path/to/skill/scripts/demo_wallet_flow.py \
  --repo-root /path/to/repo \
  --build /path/to/repo/vanilla-build
```

That verifier does all of the following on a 2-validator network:

- launch validators and emit `wallet-env.txt`
- create two workchain wallets
- deploy both wallets from the funded built-in `main-wallet`
- wait until both deployed wallets become active
- send TON from wallet A to wallet B with a comment
- inspect wallet B's latest transaction and confirm sender, value, and comment

Use it when you need a quick proof that the local helper stack is healthy before doing a more specialized experiment.

## Manual Flow

### 1. Launch The Network

```bash
python3 /path/to/skill/scripts/run_basic_network.py \
  --repo-root /path/to/repo \
  --build /path/to/repo/vanilla-build \
  --validators 2 \
  --mc-seqno 3 \
  --emit-wallet-env
```

This prints the run directory and writes `wallet-env.txt`.

### 2. Build Wallet StateInit

Use the bundled Fift helper that saves `-stateinit.boc`:

```bash
python3 /path/to/skill/scripts/run_fift_script.py \
  --wallet-env /path/to/run/wallet-env.txt \
  --script /path/to/skill/scripts/fift/new-wallet-save-stateinit.fif \
  --cwd /tmp/wallet-a \
  -- 0 wallet-a
```

Repeat for `wallet-b`.

Expected outputs:

- `wallet-a.pk`
- `wallet-a.addr`
- `wallet-a-query.boc`
- `wallet-a-stateinit.boc`

### 3. Deploy From The Built-In Main Wallet

Fresh `tontester` zerostates include a funded simple wallet at `STATE_DIR/main-wallet.{pk,addr}`. `wallet_send.py` uses it by default when `wallet-env.txt` is present.

```bash
python3 /path/to/skill/scripts/wallet_send.py \
  --wallet-env /path/to/run/wallet-env.txt \
  --dest-addr <wallet-a-raw-or-friendly-address> \
  --auto-seqno \
  --amount 1 \
  --init-boc /tmp/wallet-a/wallet-a-stateinit.boc \
  --show-seqno \
  --wait-mc-advance
```

Repeat for wallet B.

Important:

- `--wait-mc-advance` is only a liveness hint.
- A newly deployed workchain wallet may still be inactive immediately after that, so confirm activation before using it.

### 4. Wait For Activation

Do not use the new wallet as a sender until it is actually active.

At minimum, confirm:

- non-empty code
- non-empty data
- `last_transaction_id` present

You can check with:

```bash
python3 /path/to/skill/scripts/account_state.py \
  --wallet-env /path/to/run/wallet-env.txt \
  --address <wallet-a-address> \
  --out-dir /tmp/wallet-a-state
```

If you need a stronger wallet-specific check, run `seqno`.

### 5. Confirm Wallet Seqno

For these generated wallets, numeric method id `85143` is reliable:

```bash
python3 /path/to/skill/scripts/get_method.py \
  --wallet-env /path/to/run/wallet-env.txt \
  --address <wallet-a-address> \
  --method 85143
```

Expected initial result: `top_number = 0`.

`wallet_send.py --auto-seqno` already falls back to the numeric method when needed, so you usually do not need to pass a hardcoded `--seqno`.

### 6. Send From Wallet A To Wallet B With A Comment

```bash
python3 /path/to/skill/scripts/wallet_send.py \
  --wallet-env /path/to/run/wallet-env.txt \
  --wallet-base /tmp/wallet-a/wallet-a \
  --dest-addr <wallet-b-address> \
  --auto-seqno \
  --amount 0.1 \
  --comment "skill demo payment" \
  --show-seqno \
  --wait-mc-advance
```

After sending, wait until either:

- wallet A `seqno` increments, or
- wallet B's latest transaction changes

### Replaying A Prebuilt External Message

If you want to replay the same payment later, first build it without sending it:

```bash
python3 /path/to/skill/scripts/wallet_send.py \
  --wallet-env /path/to/run/wallet-env.txt \
  --wallet-base /tmp/wallet-a/wallet-a \
  --dest-addr <wallet-b-address> \
  --auto-seqno \
  --amount 0.1 \
  --comment "skill demo payment" \
  --dry-run \
  --out-dir /tmp/wallet-a-send
```

Then send the serialized external message exactly as produced:

```bash
python3 /path/to/skill/scripts/send_boc.py \
  --wallet-env /path/to/run/wallet-env.txt \
  --boc /tmp/wallet-a-send/wallet-query.boc \
  --show-seqno \
  --wait-mc-advance
```

Use this path for replay and transport debugging. It sends the serialized message exactly as provided.

### 7. Inspect The Resulting Transaction

Use the dedicated inspection helper instead of relying only on `account_state.py`:

```bash
python3 /path/to/skill/scripts/inspect_latest_transaction.py \
  --wallet-env /path/to/run/wallet-env.txt \
  --address <wallet-b-address>
```

This prints JSON including:

- transaction lt/hash
- inbound source and destination
- transferred value
- fees
- decoded comment text when tonlib exposes it as `msg.dataText` or raw comment bytes

For a successful comment transfer, expect the latest transaction to show:

- source = wallet A
- destination = wallet B
- value = transfer amount in nanotons
- comment = expected text

## Lite-Client Fallback

If the tonlib-based helpers crash, use the shared fallback guide in `liteclient_fallback.md`.

For this flow, use it for wallet activation checks, manual wallet `seqno`, and `lasttransdump` on wallet B.

## Address Handling

Helpers accept either raw `workchain:hex` or tonlib-serialized/base64 forms.

If a raw address begins with `-`, prefer the `--flag=value` form:

- `--address=-1:...`
- `--dest-addr=-1:...`

Use `address_info.py` to normalize between forms when needed.

## Common Failure Modes

- Deploy seemed to work, but the new wallet still has empty code/data.
  Most often this means you checked too early. Wait for activation before declaring the deploy broken.

- Sending from the new wallet fails with unpack-state errors.
  The wallet usually is not active yet, or you signed with the wrong seqno.

- The network advanced, but you still do not see the expected transfer.
  `mc_seqno` movement is not transaction proof. Inspect the latest account transaction directly.
