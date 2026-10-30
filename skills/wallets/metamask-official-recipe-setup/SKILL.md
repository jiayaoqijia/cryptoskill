---
name: recipe-setup
description: Check an engineer's machine for recipe-backed MetaMask work — harness, runtime, wallet fixture, device and installed skills — and walk through whatever is missing.
disable-model-invocation: true
maturity: experimental
---

# Setup for recipe-backed work

Use only when explicitly named.

Run `mm-harness doctor` through `scripts/setup-check`, from the MetaMask checkout. Doctor is the verdict; the script adds only what doctor does not report yet. On exit 0 print its summary and stop; a `!` warning (skills) does not block, offer its step. Otherwise follow ONLY the step named by `SETUP INCOMPLETE: <piece>`, then rerun. Show doctor's findings and next command as printed, never reworded.

## harness

This skill installs before the harness, so a missing `mm-harness` is step one: `npm i -g @deeeed/metamask-harness@0.94.7` (the recommended release), then `mm-harness --version`. Everything below runs inside a MetaMask checkout (metamask-extension, metamask-mobile, core). If the user did not start you in one, run `mm-harness setup-base --dry-run`, show what it would create, and ask before running it for real.

## doctor

Follow doctor's own next command until it passes. `--fix` repairs harness-owned runtime state; it never invents credentials or simulators. A `runtime` finding of app-not-running is advisory, not a failure.

## fixture

With no fixture, STOP and ask which wallet. Show this file, then wait:

```
temp/recipe/runtime/wallet-fixture.json
{
  "password": "<unlock password>",
  "accounts": [
    {
      "type": "mnemonic",
      "value": "<secret recovery phrase>",
      "name": "Account 1",
      "count": 1,
      "names": ["Account 1"]
    }
  ],
  "settings": { "skipPerpsTutorial": true, "autoLockNever": true }
}
```

The user gives a path (`mm-harness fixtures init --from <path>`), writes the file themselves (never paste a secret recovery phrase into chat), or explicitly picks the disposable public test wallet (`mm-harness fixtures init --dev`, never real funds). Never invent a mnemonic or a password. Continue only at READY.

## launch

Reached from doctor's next command, or when the fixture has to be applied to a running app.

- Extension: `mm-harness launch --verify`, then `mm-harness fixtures set`.
- Android: `mm-harness launch android --verify`; with several devices listed, pick one serial and repeat with `--device <serial>`; pass the same `--device` to `fixtures set`.
- iOS: pin one simulator. Reuse `simulatorUdid` from `temp/recipe/runtime/agentic-runtime.json` when set, else `mm-harness provision runway ios --device mm-local --force` (recorded UUID: `--device '<UUID>' --force`). Then `mm-harness launch ios --device '<UUID>' --verify` and `mm-harness fixtures set --device '<UUID>'`. Never grab a spare or already-booted simulator.
- Core: `mm-harness verify`; no app to launch.

## skills

Inspect `METAMASK_SKILLS_DIR` and reuse a valid clone. If missing, show the path and ask before cloning:

```
git clone https://github.com/MetaMask/skills.git ~/dev/metamask/skills
```

Export `METAMASK_SKILLS_DIR` in the current shell only; never edit a startup file without explicit consent. Then, from the checkout:

```
yarn skills --include perps/recipe-harness,perps/recipe-cook,perps/recipe-dev,perps/recipe-fix-bug,perps/recipe-qa,perps/recipe-pretty-pr,perps/recipe-setup --save
```

## actions

`mm-harness actions` is the only capability list, now and in every later session. Never invent an action or a flag.

## Rules

Evidence comes only from executed commands. A failing command names the next one — run that, do not improvise. If a step fails twice after following its error, stop and show the exact error.
