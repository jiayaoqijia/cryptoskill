# Contract Deploy Flow

Use this reference for `Workflow A — trigger via transaction`.

This is the full path:

1. launch a small network
2. compile a contract
3. build `StateInit`
4. deploy with `wallet_send.py --init-boc`
5. send a trigger body
6. inspect the resulting transaction and dump the exported BoCs

The commands below were smoke-tested against a local repo with a rebuilt `build/tolk/tolk`.

## Fastest Verified Example

The fastest known-good contract for this flow is the existing repo source:

- `/path/to/repo/tolk-tester/tests/handle-msg-5.tolk`

It has:

- an internal-message handler
- a get-method with method id `101`
- no special deployment dependencies

Once this path works, replace that source file with your real contract source.

## 1. Launch The Network

```bash
python3 /path/to/skill/scripts/run_basic_network.py \
  --repo-root /path/to/repo \
  --build /path/to/repo/build \
  --validators 2 \
  --mc-seqno 3 \
  --emit-wallet-env \
  --keep-alive 240
```

Capture the printed `wallet-env.txt` path. The rest of the flow uses it.

## 2. Compile The Contract

```bash
python3 /path/to/skill/scripts/compile_tolk.py \
  --wallet-env /path/to/run/wallet-env.txt \
  --source /path/to/repo/tolk-tester/tests/handle-msg-5.tolk \
  --out-dir /tmp/contract
```

Expected outputs:

- `/tmp/contract/handle-msg-5.fif`
- `/tmp/contract/handle-msg-5.code.boc`

If this fails with a stale-build error, rebuild `tolk` first:

```bash
ninja -C /path/to/repo/build tolk
```

## 3. Build `StateInit`

```bash
python3 /path/to/skill/scripts/build_stateinit.py \
  --wallet-env /path/to/run/wallet-env.txt \
  --code-boc /tmp/contract/handle-msg-5.code.boc \
  --out-dir /tmp/contract-stateinit
```

This prints:

- raw address
- non-bounceable address
- bounceable address

Expected outputs:

- `/tmp/contract-stateinit/contract-stateinit.boc`
- `/tmp/contract-stateinit/contract.addr`

If your contract needs initial data or a library dictionary, add:

- `--data-boc /path/to/data.boc`
- `--library-boc /path/to/libs.boc`

## 4. Deploy The Contract

Use the raw address printed by `build_stateinit.py`.

```bash
python3 /path/to/skill/scripts/wallet_send.py \
  --wallet-env /path/to/run/wallet-env.txt \
  --dest-addr=0:<contract-addr-hex> \
  --auto-seqno \
  --amount 1 \
  --init-boc /tmp/contract-stateinit/contract-stateinit.boc \
  --show-seqno \
  --wait-mc-advance \
  --wait-timeout 20
```

`wallet_send.py` uses the funded built-in `main-wallet` by default when `wallet-env.txt` is present.

A deploy message sent with `wallet_send.py --init-boc` can execute the contract's internal message handler in the same transaction as the deploy. For stateful contracts, "deploy" and "first trigger" are not always separate events. If your contract increments state on any internal message, the deploy transaction itself will be the first state change.

`--wait-mc-advance` proves the network is alive. It does NOT prove the transaction succeeded, the deploy activated, or the contract state changed. Always inspect the target account directly.

## 5. Wait For Activation

Do not trigger the contract until it is active.

```bash
python3 /path/to/skill/scripts/account_state.py \
  --wallet-env /path/to/run/wallet-env.txt \
  --address 0:<contract-addr-hex> \
  --out-dir /tmp/contract-account
```

For the verified example, a stronger activation check is:

```bash
python3 /path/to/skill/scripts/get_method.py \
  --wallet-env /path/to/run/wallet-env.txt \
  --address 0:<contract-addr-hex> \
  --method 101
```

Expected result:

- `exit_code = 0`
- `top_number = 0`

## 6. Build An Arbitrary Trigger Body

Create a tiny Fift script such as:

```fift
"TonUtil.fif" include
x{DEADBEEF} s>c 2 boc+>B "body.boc" B>file
```

Then run it:

```bash
python3 /path/to/skill/scripts/run_fift_script.py \
  --wallet-env /path/to/run/wallet-env.txt \
  --script /tmp/body.fif \
  --cwd /tmp/contract-body
```

This emits:

- `/tmp/contract-body/body.boc`

Use this path whenever the trigger message must contain binary payload instead of a wallet comment.

## 7. Send The Trigger

```bash
python3 /path/to/skill/scripts/wallet_send.py \
  --wallet-env /path/to/run/wallet-env.txt \
  --dest-addr=0:<contract-addr-hex> \
  --auto-seqno \
  --amount 0.1 \
  --body-boc /tmp/contract-body/body.boc \
  --show-seqno \
  --wait-mc-advance \
  --wait-timeout 20 \
  --out-dir /tmp/trigger-send
```

Important:

- `--body-boc` is the internal payload path.
- `--body-boc` overrides `--comment`.
- Remember: `--wait-mc-advance` is only a liveness hint. Verify the target account or transaction directly.

## 8. Inspect The Result

```bash
python3 /path/to/skill/scripts/inspect_latest_transaction.py \
  --wallet-env /path/to/run/wallet-env.txt \
  --address 0:<contract-addr-hex> \
  --out-dir /tmp/contract-inspect
```

Look for:

- the latest transaction id
- the inbound source and destination
- the transferred value
- the exported `transaction-data.boc`
- the exported `in-msg-body.boc` when the inbound payload is `msg.dataRaw`

Expected artifacts in the verified binary-payload example:

- `/tmp/contract-inspect/latest-transaction.json`
- `/tmp/contract-inspect/transaction-data.boc`
- `/tmp/contract-inspect/in-msg-body.boc`

## 9. Dump The BoCs

```bash
python3 /path/to/skill/scripts/dump_boc.py \
  --wallet-env /path/to/run/wallet-env.txt \
  --boc /tmp/contract-inspect/in-msg-body.boc
```

For the verified example, this prints:

```text
x{DEADBEEF}
```

You can also dump the raw transaction blob:

```bash
python3 /path/to/skill/scripts/dump_boc.py \
  --wallet-env /path/to/run/wallet-env.txt \
  --boc /tmp/contract-inspect/transaction-data.boc
```

## Lite-Client Fallback

If the tonlib-based helpers crash, use the shared fallback guide in `liteclient_fallback.md`.

For this flow, use it for `getaccount`, `runmethodfull 0:<contract-addr-hex> 101`, `lasttransdump`, and post-trigger state checks.

## What To Change For Your Real Repro

- Replace `handle-msg-5.tolk` with your contract source.
- Replace `x{DEADBEEF}` with the actual trigger payload.
- Replace get-method `101` with your contract-specific activation or observation method if one exists.

If the deployment path works but the bug does not reproduce, use `references/diagnostic_checklist.md` before changing the network topology.
