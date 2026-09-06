# Lite-Client Fallback

Use this reference when tonlib-based helpers crash with `KeyError: '@extra'` or similar wrapper errors.

Switch observation steps to `run_liteclient.py`, and use manual `--seqno` if `wallet_send.py --auto-seqno` is unavailable.

## Generic Account Check

```bash
python3 /path/to/skill/scripts/run_liteclient.py \
  --wallet-env /path/to/run/wallet-env.txt \
  -- getaccount <address>
```

Look for:

- non-empty `code`
- non-empty `data`
- `last transaction lt/hash`

Use this as the activation check for both contract accounts and generated wallets.

## Generic Get-Method Check

```bash
python3 /path/to/skill/scripts/run_liteclient.py \
  --wallet-env /path/to/run/wallet-env.txt \
  -- runmethodfull <address> <method-id>
```

This prints the return stack and the get-method exit code.

Examples:

- use method id `101` for the verified contract example in `contract_deploy_flow.md`
- use method id `85143` for the generated-wallet `seqno` check in `wallet_and_deploy_helpers.md`

## Latest Transaction Dump

First read the latest transaction id from `getaccount`:

```text
last transaction lt = <lt> hash = <hash>
```

Then dump the transaction:

```bash
python3 /path/to/skill/scripts/run_liteclient.py \
  --wallet-env /path/to/run/wallet-env.txt \
  -- lasttransdump <address> <lt> <hash> 1
```

This prints the full transaction, including inbound source, destination, transferred value, and message body or comment when visible in the dump.

## Wallet Seqno

If tonlib-backed `--auto-seqno` is unavailable, read the wallet seqno with `runmethodfull` and pass manual `--seqno` to `wallet_send.py`.

For the generated simple-wallet flow, the reliable numeric method id is `85143`.

## State After A Trigger

After a failed or successful trigger, rerun `getaccount` on the target address to inspect the current account state directly.
