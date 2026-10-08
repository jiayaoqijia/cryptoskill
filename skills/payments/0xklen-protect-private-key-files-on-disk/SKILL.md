---
name: protect-private-key-files-on-disk
description: Use when a private key, keystore, or .env holding a signing key must live on a workstation or server. Sets permissions, keeps secrets out of argv and shell history, and verifies nothing leaked.
---

# Protect private key files on disk

A key is only as safe as the worst place it was ever echoed. This skill keeps key material in 0600 files or encrypted keystores and injects it through the process environment, never through a command line that lands in shell history or `ps`.

## Procedure

1. Set a restrictive umask before creating key material so nothing is world-readable by accident:
   `umask 077`
2. Create the key file at mode 600 and confirm it:
   `install -m 600 /dev/null ~/.keys/deployer.key`
3. Prefer an encrypted keystore over a raw hex file on any shared machine. Import interactively so the key never appears in argv:
   `cast wallet import deployer --interactive`
   Keystores land in `~/.foundry/keystores/` and decrypt only with your passphrase.
4. When a raw key is unavoidable, load it from the file into the environment, not onto a command line:
   `export DEPLOYER_KEY="$(tr -d '\n' < ~/.keys/deployer.key)"`
   Read it in code, never as a flag:
   ```python
   import os
   from eth_account import Account
   print(Account.from_key(os.environ["DEPLOYER_KEY"]).address)
   ```
5. Stop the shell recording the command that touches the secret:
   `set +o history` in bash, or prefix the line with a space and set `HISTCONTROL=ignorespace`.
6. Never pass a key as `--private-key 0x...`. That writes it into `~/.bash_history` and exposes it in `ps aux` to every user on the host. Use `--account deployer` or `--ledger`.
7. Audit for leaks before you finish.

## Pitfalls

- A single `set -x` during debugging dumps every `export` to stderr and into CI logs; keep it off in any script that loads keys.
- `.env` files get committed. Add `.env`, `*.key`, and `keystores/` to `.gitignore` before the first commit, not after an incident.
- Docker `ENV` and `ARG` persist in image layers; pass secrets at runtime with `--env-file` or a mounted secret.
- macOS uses `stat -f` and Linux uses `stat -c`; the permission check silently does nothing if you use the wrong one.

## Verification

    stat -f "%Lp %N" ~/.keys/*.key && grep -c "DEPLOYER_KEY=0x" ~/.zsh_history
    # expect mode 600 on every key, and grep to print 0

Report the observed file mode and the zero-match leak scan, quoting the commands run.
