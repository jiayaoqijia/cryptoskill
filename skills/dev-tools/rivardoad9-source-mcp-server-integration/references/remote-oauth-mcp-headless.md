# Remote HTTP MCP server with OAuth — headless host, user signs in on their own device

Use when the MCP server is a bare URL (no local command) and access is gated behind a
browser sign-in, while the Hermes host is a VPS/gateway the user cannot open a browser
on (they are on Telegram/Slack/CLI and you relay URLs between them and the flow).

## 1. Ask the server what OAuth it actually supports, before choosing a flow

```bash
curl -s https://<mcp-host>/.well-known/oauth-authorization-server | python3 -m json.tool
curl -s https://<mcp-host>/.well-known/oauth-protected-resource  | python3 -m json.tool
```

- `device_authorization_endpoint` present → `hermes mcp login <name> --flow device`
  (RFC 8628). Lowest friction: no callback listener, the user gets a code and a URL to
  open on their phone.
- Absent → authorization_code + PKCE only, and the callback is a loopback listener on
  the Hermes host. Use the paste-back flow in §3.
- `grant_types_supported` containing `refresh_token` means one sign-in survives restarts;
  without it, every expiry is another round-trip with the user.
- `scopes_supported` is what the server *can* grant — the consent page the user sees is
  what actually decides. Read them so you can tell the user which level to pick.
- `registration_endpoint` present (and `token_endpoint_auth_methods_supported: [none]`)
  means dynamic client registration, i.e. no client_id/secret to create by hand. When it
  is absent, the user must create an OAuth client and you add `oauth.client_id` /
  `oauth.client_secret` to the server config.

## 2. Register the server, then repair what `add` left out

`hermes mcp add <name> --url <url> --auth oauth` on a headless host prints
`non-interactive environment and no cached tokens found`, skips setting `auth`, then
(answering the "Save config anyway?" prompt) writes an entry that is `enabled: false`
and has no `auth` key. Repair it with config sets — re-running `add` has the same outcome:

```bash
hermes config set mcp_servers.<name>.auth oauth
hermes config set mcp_servers.<name>.enabled true
hermes config set mcp_servers.<name>.oauth.timeout 1800
hermes config get mcp_servers.<name>
```

- `~/.hermes/config.yaml` is guarded: direct writes/patches are refused, and a stray
  indent can corrupt the file the live gateway reads. `hermes config set` with the full
  dotted key is the supported route for nested keys.
- `oauth.timeout` is the callback window (default 300 s) and it is read when the flow
  *starts*: the login's overall bound is `max(connect_timeout, oauth.timeout + 15)`.
  Set it before launching §3 — changing it while a flow is already waiting does nothing.
- `oauth.redirect_port` pins the loopback callback port if you need the registered
  redirect to stay stable across attempts.

## 3. Launch the login in a PTY background session and relay the URL

```
terminal(command="hermes mcp login <name>", pty=true, background=true)
process_manage(action="poll", session_id="proc_…", timeout=45)
```

The process prints the authorization URL and then waits at a stdin prompt:
`Or paste the redirect URL here … Type skip + Enter to continue without this server.`

- **PTY is required.** Without a TTY the flow is refused outright; `hermes mcp login`
  forces the interactive path itself, so a pty background session is the reliable shape.
- Hand the URL over verbatim — it carries `state`, the PKCE `code_challenge` and the
  registered `redirect_uri`; any edit invalidates it.
- The redirect target is `http://127.0.0.1:<port>/callback` on the Hermes host, so the
  user's browser will show a connection error after they approve. Tell them that up front
  and give the send-back step in the same message: *copy the FULL URL from the address
  bar and send it here*. It is single-use and useless without this flow's PKCE verifier.
- Message shape that avoids a second round-trip: (a) link, (b) which access level to
  pick, (c) which add-on box to leave ticked, (d) "after approving the page will fail to
  load, that is expected, send me the full address-bar URL", (e) how long the window is.

## 4. Complete and verify

```
process_manage(action="submit", session_id="proc_…", data="<full redirect URL>")
process_manage(action="poll",   session_id="proc_…", timeout=60)
```

- Success reads `Authenticated — N tool(s) available`. A later clean probe is NOT proof:
  some servers answer `initialize`/`tools/list` unauthenticated, so verify a token landed
  (the login flow does this itself and warns "no OAuth token was obtained" otherwise).
- Confirm independently: `hermes mcp test <name>` and `hermes mcp list`.
- A bad paste prints `Could not parse pasted input` / `Pasted input did not contain
  code=` and the process keeps waiting — retry into the SAME flow rather than restarting.
- Kill the pty session before restarting a flow; a leftover listener holds the callback
  port and the next attempt dies on "callback port already in use".

## 5. Consent and scope hygiene

The consent page decides what lands, not the requested scope list. Recommend the least
privilege that does the job and say in the message which level you picked and why.
Typical ladder: inspect/read → read + control (change charts/layouts/config) → read +
control + execute (place orders, write to the account). Execution scopes normally need a
second arming step inside the user's own browser tab afterwards, so do not request them
unless placing orders is the actual task. Keep monitoring add-ons (alerts/watchlists)
whenever the follow-on work is watching rather than one-off reading.

## 6. First use of the connection

Read the server's own `llms.txt` / instructions and follow its stated sequence. If the
user named a specific object (workspace, chart, project), select that id first; if they
did not, list and ask which one they have open — never assume the last-used object. Then
call the server's status tool and report exactly what you can see before offering a
change.
