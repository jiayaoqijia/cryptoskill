---
name: agent-web-identity
description: "Lets an AI agent or CLI session sign in to Internet Identity and act as a user's app-specific principal (e.g. for oisy.com or nns.ic0.app) via `icp identity link web`. Use when the user asks an agent to log in to an II-powered app, obtain a delegation, or make authorized canister calls on their behalf. Do NOT use for adding II sign-in to a frontend — use the internet-identity skill instead."
license: Apache-2.0
compatibility: "icp-cli >= 0.3.0, browser on the same machine"
metadata:
  title: Agent Web Identity Sign-In
  category: Auth
---

# Agent Web Identity Sign-In

## What This Is

Internet Identity (II) supports a CLI-auth flow that issues a delegation for a
session key held *outside* the browser. `icp identity link web` uses it to let
a terminal session — including an AI agent such as Claude Code — sign canister
calls as the user's **app-specific principal**: the same principal the user has
when signed in to that app's web UI (selected with `--app <domain>`).

The user still authenticates interactively in their own browser with their
passkey; the agent only ends up holding a time-limited delegation. The private
key of the user's II identity is never exposed.

## Prerequisites

- `icp` CLI installed (https://cli.internetcomputer.org). See the `icp-cli`
  skill for general usage.
- The user must have an Internet Identity (id.ai) and be present to complete
  the browser sign-in.
- First-time use requires the user to enable the **CLI access** toggle for
  their identity in II settings (see Pitfall 1).
- The agent and the user's browser must be on the same machine: the flow
  delivers the delegation via a localhost callback. It does not work from
  remote/headless environments (containers, CI, web sessions).

## Common Pitfalls

1. **First-time sign-in fails with a "CLI access disabled" screen.** This is
   the expected first-run path, not an error. Tell the user to enable CLI
   access for their identity in II settings, then **restart the flow from
   scratch** — the previous sign-in URL is single-use (its nonce and localhost
   listener are dead). Plan for two rounds on first use.

2. **The link command waits for an Enter keypress before doing anything.** On
   0.3.x it first prints `Press Enter to log in at https://id.ai/cli` and
   blocks reading stdin; only after that does it start the flow and try to
   open the browser. In a background or non-interactive run, **pipe an actual
   newline into it** (`printf '\n' | icp identity link web ...`). Do NOT
   redirect from `/dev/null`: a bare EOF does **not** satisfy the prompt on
   0.3.2 — the command sits on `Press Enter to log in` and never starts the
   flow, so you waste the first attempt and have to restart, prompting the
   user twice. Feed the newline on the first try and the flow starts
   immediately.

3. **Don't assume the browser opened.** Sandboxed or non-interactive shells
   often can't launch a GUI browser. Read the command's output: if a full
   sign-in URL is printed, show it to the user to open themselves. If the
   output shows neither a browser launch nor a URL, report that — do not
   construct a URL by guessing, and ask the user whether a browser window
   appeared.

4. **The command blocks until sign-in completes and gets killed by tool
   timeouts.** Run `icp identity link web` as a background task, then wait for
   the user to confirm they finished signing in before checking the result.
   The command must also be able to bind a localhost port; if a sandbox blocks
   this, ask the user before rerunning unsandboxed.

5. **Relying on the default identity signs with the wrong principal.** Every
   `icp` command acting as the user must pass `--identity <NAME>` explicitly.
   Never depend on project or global default identity settings, and never
   change them.

6. **Reusing or overwriting identities.** Never reuse an existing identity,
   even if `icp identity list` already shows one linked for the same app — its
   delegation may be expired and it belongs to whoever created it. Always
   create a fresh identity per session: check `icp identity list`, then pick
   a unique name prefixed with the agent's own identifier,
   `<agent>-<app>-<YYYYMMDD-HHMM>` — e.g. `claude-oisy-20260611-1530` for
   Claude, `cursor-oisy-...` for Cursor; use `agent-` if no identifier is
   known. Never
   overwrite an existing identity. `icp identity list` is read-only context
   for picking a free name — never delete, rename, reauth, or otherwise
   modify any identity you did not create this session, even ones with the
   agent's own prefix left over from a previous run. Operate only on `$NAME`.
   Why per-session and not one reused identity per app: `--app` derives the
   *same* app principal for a given II identity, so a fresh identity grants no
   extra authority isolation — the point is **provenance and blast radius**.
   A per-session identity keeps `icp identity list` auditable (which session
   created which live delegation), lets cleanup delete exactly that one, and
   avoids a shared identity where another session's `reauth` silently mutates
   a delegation this session is mid-task with.

   When scanning `icp identity list` to pick a name, if you see multiple stale
   agent-prefixed identities for the same app from past sessions (e.g. several
   `claude-oisy-*` entries), offer to clean them up before proceeding: present
   the list, wait for the user to confirm each one, then delete them with
   `icp identity delete <NAME>`. Never delete without explicit confirmation.

7. **Wrong principal because `--app` was omitted.** Without `--app`, the
   provider uses its default derivation origin and the resulting principal
   will NOT match the user's principal in the target app. Pass the app's bare
   domain (no scheme, port, or path), e.g. `--app oisy.com`.

8. **Expired delegations.** Delegations are time-limited; the lifetime is set
   by the identity provider during sign-in. `icp identity link web` has NO
   flag to control it — do not invent one (e.g. `--ttl`; 0.3.x rejects it and
   the whole command fails). When calls start failing with signature/expiry
   errors, run `icp identity reauth <NAME>` — the user must sign in again as
   the same identity.

9. **Canister calls without explicit arguments auto-cancel.** When call
   arguments are omitted, `icp canister call` opens an interactive prompt to
   build the arguments and confirm sending (`Do you want to send this
   message? [y/N]`), which immediately cancels in a non-interactive shell
   (`User cancelled.`). Always pass arguments explicitly — including the
   empty tuple `'()'` for zero-argument methods like `whoami`.

## Implementation

Generalized flow for linking the user into `<APP_DOMAIN>` (e.g. `oisy.com`,
`nns.ic0.app`):

```bash
# 1. Pick a fresh name (never reuse an existing identity, even one
#    already linked for this app); confirm it doesn't exist
icp identity list
NAME="agent-<app>-$(date +%Y%m%d-%H%M)"
# substitute your own agent prefix for "agent" if known,
# e.g. claude-oisy-20260611-1530, cursor-oisy-...

# 2. Start the link flow IN THE BACKGROUND (keeps the localhost
#    listener alive while the user signs in). Use your harness's
#    background-execution mode if it has one; in a plain shell:
printf '\n' | icp identity link web "$NAME" --app <APP_DOMAIN> \
  > "/tmp/icp-link-$NAME.log" 2>&1 &
# Pipe a real newline to answer the "Press Enter to log in" prompt.
# Do NOT use `< /dev/null`: on 0.3.2 a bare EOF does not satisfy the
# prompt, so the command hangs and you'd have to restart it — which
# prompts the user a second time. The newline starts the flow on the
# first try.

# 3. Read the command's output (the log file above). After the Enter
#    prompt it tries to open the user's browser; if a sign-in URL is
#    printed instead, relay it to the user. Wait for them to confirm
#    sign-in (first run may require enabling CLI access in II settings
#    — restart from step 2 if so)

# 4. Confirm the identity was created
icp identity list
```

## Verify It Works

Call the public whoami canister as the linked identity:

```bash
icp canister call --identity "$NAME" --network ic \
  ivcos-eqaaa-aaaab-qablq-cai whoami '()'
```

(Adapt flags to the installed CLI version — see `icp canister call --help` —
but always keep the explicit `--identity` and the explicit `'()'` arguments;
omitting the arguments triggers an interactive prompt that auto-cancels in
non-interactive shells, see Pitfall 9.) The returned principal should
match the principal the app shows the user when they are signed in to
`<APP_DOMAIN>`; ask the user to confirm.

## Security Rules for Agents

- The delegation grants **full authority as the user's app principal** until
  it expires — it is not scoped to specific canisters. Treat it like a signed
  blank check for that app.
- Other than the whoami verification, ask the user explicitly before every
  state-changing canister call made with the linked identity.
- The delegation's lifetime is decided by the identity provider, not the CLI
  — there is no flag to shorten it.
- Never export, print, or log the identity's key material; leave it in the
  CLI's default keyring storage.
- Keep output to the minimum. When a step succeeds, don't echo command output
  or narrate progress — surface only what needs the user: the sign-in URL,
  confirmation requests, errors, and the final verified principal.
- When done, do NOT delete the linked identity on your own initiative — the
  user may want to reuse the live delegation for follow-up calls. Ask the
  user whether to clean it up, and only on their confirmation run
  `icp identity delete <NAME>` (the subcommand is `delete`; `remove` is not a
  valid subcommand on 0.3.x). If they decline, just remind them of the
  identity name and that command so they can remove it later.
- At the start of a session, when `icp identity list` reveals accumulated
  stale agent-prefixed identities from past sessions (e.g. multiple
  `claude-oisy-*` entries), offer to delete them before creating a new one.
  Present the list to the user, wait for confirmation, and delete only the
  approved ones with `icp identity delete <NAME>` — never in bulk, never
  without confirmation.
