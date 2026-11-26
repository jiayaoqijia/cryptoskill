# Console Errors and Network Requests

From `mm launch` on, the daemon records console errors and HTTP(S) requests of every extension page, the background service worker, the MV3 offscreen document and the snaps iframes it runs. Read them with `mm logs` and `mm network`. Do not add `console.error` hooks or `Network.enable` listeners with `mm cdp` for this. Traffic during `mm launch` itself (unlock screen load, self-onboarding) is not recorded.

## Contents

- [Per-flow recipe](#per-flow-recipe)
- [Cursor and summary](#cursor-and-summary)
- [mm logs](#mm-logs)
- [mm network](#mm-network)
- [Baseline noise on the e2e fixture](#baseline-noise-on-the-e2e-fixture)

## Per-flow recipe

```bash
mm events mark                         # {"action":"mark","cursor":40,"summary":{"startedAt":1795609173332,"seq":40,...,"captureErrors":0}}
# ...run the flow...
mm logs --cursor 40                    # console errors since the mark
mm network --settled --cursor 40       # final status of every request that ended since the mark
mm network --errors --cursor 40        # only status >= 400, failures and rpcError
```

Then check:

- `hasMore: true`: read again with the returned `cursor`.
- `summary.startedAt` differs from the one `mark` returned: the session was relaunched. Read from `--cursor 0` and report a gap for the flow.
- `gap: true`: records after your cursor were dropped, or the cursor is from another session. Report a gap.
- `summary.captureErrors` grew during the flow: the session could not listen to a page or the worker, so some of its events can be missing.

Use only a cursor that `mm events mark` or a read returned. A cursor above the newest `seq` counts as one from an earlier session: the read starts from the oldest record and returns `gap: true`.

## Cursor and summary

| Command | Result |
|---|---|
| `mm events mark` | `{ cursor, summary }` |
| `mm events clear [--kind console\|network]` | Empties the buffer. The cursor keeps counting, so older cursors stay valid |

`summary` is `{ startedAt, seq, counts: { console, network }, dropped: { console, network }, captureErrors, lastCaptureError? }`. Console and network share one cursor (`seq`), so one mark covers both. The buffer keeps the newest 1000 console and 2000 network records; `dropped` counts the rest.

## mm logs

```bash
mm logs [--cursor <n> | --since <iso|epoch-ms>] [--limit <n>] [--grep <regex>]
mm logs configure --levels error,warning     # from now on, this session; default: error
```

Returns `{ records, cursor, hasMore, gap, summary }`, oldest first (default 500, max 2000 per read). A record:

```json
{"seq":117,"t":1795609258901,"target":{"kind":"sw","id":"6639CA21…","url":"chrome-extension://<id>/service-worker.js"},"level":"error","text":"An error occurred while executing an event for Snap \"npm:@metamask/institutional-wallet-snap\": …","location":"chrome-extension://<id>/service-worker.js:15391:9471"}
```

- `target.kind`: `page`, `sw` (the background service worker), `offscreen` or `iframe` (a snaps iframe).
- Uncaught exceptions have `"uncaught": true`. `text` is cut at 2000 characters.
- `text` is redacted for URLs, JWTs, `Bearer` values and sensitive property names (`privateKey`, `mnemonic`, `password`, …), not for a secret in free text.
- `--grep` is a case-sensitive JavaScript regular expression (max 256 characters).
- `mm logs configure` accepts only `--levels`. Any other flag is a usage error (exit 2).

## mm network

```bash
mm network [--cursor <n> | --since <iso|epoch-ms>] [--limit <n>] [--url <glob|text>] [--errors] [--settled]
mm network configure --rpc-errors            # also read JSON-RPC error bodies (off by default)
```

It only listens: it never mocks, blocks or changes a request and stores no bodies (to mock or read bodies, use [mock-network.md](mock-network.md)). Most Extension traffic comes from the service worker (`target.kind: "sw"`): RPC, gas, security alerts, tokens. A record:

```json
{"seq":398,"t":1795609382547,"target":{"kind":"iframe","id":"A60112EC…","url":"chrome-extension://<id>/snaps/index.html"},"method":"GET","url":"https://bitcoin-mainnet.infura.io/v3/[REDACTED]/esplora/blocks","type":"fetch","status":200,"settledSeq":401,"ms":180}
```

| Field | Meaning |
|---|---|
| `settledSeq` | Set when the request ended. Absent while pending |
| `status` / `ms` | HTTP status and duration. Absent while pending or when it failed before a response |
| `failure` | `net::ERR_ABORTED`, `net::ERR_FAILED (cors: …)`, `target closed`, `abandoned`, … |
| `rpcMethods` | JSON-RPC methods of the request body, for example `["eth_sendTransaction"]` |
| `rpcError` | `{ code, message }` of a JSON-RPC error. Only after `mm network configure --rpc-errors` |

The result also has `stats: { pending, ignored, rpcErrorsSkipped }`. URLs are redacted (Infura keys, `key`/`token`-like params).

| Read | Returns |
|---|---|
| No filter | Every request in start order (`seq`), pending ones included |
| `--settled` | Requests that ended since the cursor, in end order, including ones that started before it. Use it at the end of a flow |
| `--url` / `--errors` | Like `--settled`, filtered. `--url` takes a glob (`*`, `**`) or text the URL contains |

A cursor from a `--settled` or filtered read continues reads of the same mode.

The session keeps `Network` enabled on every page and on the service worker. `mm cdp Network.enable` (no params) succeeds and sends nothing. `mm cdp Network.disable`, or `Network.enable` with params, fails with `MM_CDP_BLOCKED` (exit 2); add `--fresh` if you really need it.

## Baseline noise on the e2e fixture

Basic functionality is off in the fixture, so every e2e session records these. They are not regressions; compare against a mark taken before your flow.

- `mm logs`: service-worker errors `… The Snaps platform requires basic functionality to be used …` (several per launch and unlock) and one `ExtensionLazyListener: Possible memory leak detected …`.
- `mm network --errors`: `401` from `sepolia.infura.io` and `linea-sepolia.infura.io` (`eth_blockNumber`), `400` from `gas.api.cx.metamask.io/networks/1337/suggestedGasFee` while a send is open, `400` from `accounts.api.cx.metamask.io/v5/multiaccount/transactions` on the asset page.
