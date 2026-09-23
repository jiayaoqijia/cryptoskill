---
name: wallet-integration
description: "Integrate an external wallet (signer) into an IC dapp with @icp-sdk/signer — the relying-party side of the ICRC signer standards. Covers picking a transport (popup via ICRC-29 / top-level redirect via ICRC-167 / browser extension via ICRC-94) then negotiating capabilities, the permission and account lifecycle, and executing canister calls the user approves through SignerAgent (ICRC-49). Uses OISY as the worked example but applies to any ICRC-25 signer. Do NOT use for Internet Identity login (use the internet-identity skill) or for implementing a wallet yourself. Use when the developer mentions wallet integration or OISY or @icp-sdk/signer or approving a transaction in a wallet popup."
license: Apache-2.0
compatibility: "Node.js >= 22, a browser (secure context: HTTPS, localhost, or 127.0.0.1)"
metadata:
  title: Wallet Integration
  category: DeFi
---

# Wallet Integration

## What This Is

Connecting an **external wallet** to your dapp so the user approves actions in the wallet rather than handing your app a key. `@icp-sdk/signer` is the **relying-party** client: your app is the relying party, the wallet is the signer, and they exchange JSON-RPC 2.0 messages over a transport defined by the ICRC signer standards.

This skill covers **integrating a signer**. Implementing one is out of scope — consent screens, prompt registration and account custody are the wallet's job.

Examples use [OISY](https://oisy.com) (`https://oisy.com/sign`), but nothing here is OISY-specific. For another web signer the transport URL is usually the only change, and [`BrowserExtensionTransport`](#extension-icrc-94) discovers extension signers you never hardcoded. What a given signer actually supports is a separate question from which transport reaches it — negotiate it rather than assuming (see [Negotiate capabilities](#negotiate-capabilities) and pitfall 5).

| Standard | What it gives you | API |
|----------|-------------------|-----|
| ICRC-25 | Capability discovery + permission lifecycle | `getSupportedStandards`, `requestPermissions`, `getPermissions` |
| ICRC-27 | The user's accounts | `getAccounts` |
| ICRC-29 | Popup transport over `postMessage` | `PostMessageTransport` |
| ICRC-49 | Execute a canister call | `SignerAgent` (or `callCanister`, the raw primitive) |
| ICRC-94 | Browser-extension discovery | `BrowserExtensionTransport.discover` |
| ICRC-167 | Top-level redirect transport | `UrlTransport` (**new in signer 6**) |

## What the model is

Every write is an individual, user-approved act. Your app asks the wallet to execute one canister call (ICRC-49); the wallet shows the user what it is about to do, the user approves, and the wallet signs and submits it. Your app never holds a key and never acts on the user's behalf unattended.

That is the whole shape, and it is what makes wallet integration appropriate for deliberate, high-value actions — transfers, approvals, mints — and inappropriate for anything frequent or invisible. If a user should not see a prompt per action, you do not want a wallet; you want authentication.

### When NOT to use this skill

- **A session — sign in once, then act many times.** That is authentication, not wallet integration: a delegation is scoped and issued by an identity provider. Use the **internet-identity** skill. ICRC-34 exists, but it is an auth mechanism and out of scope here.
- **Internet Identity sign-in** → the **internet-identity** skill. II is an identity provider, not an ICRC-25 signer.
- **Letting an agent or CLI act as the user** → the **agent-web-identity** skill.
- **Building a wallet** → out of scope, as above.

## Prerequisites

```bash
npm i '@icp-sdk/signer@^6' '@icp-sdk/core@^6'
```

Add `@icp-sdk/canisters@^4` if you call ICP/ICRC ledgers (it brings `@dfinity/utils@^5` as a peer). Pin `@icp-sdk/core` to `^6`: signer 6 peers it, and so do `@icp-sdk/auth@^10` and `@icp-sdk/canisters@^4`.

The transport URL must be a **secure context** — HTTPS, `localhost`, or `127.0.0.1`.

## Pick a transport

The transport is the only part that knows *how* the wallet is reached; the `Signer` API above it is identical whichever you choose.

| Transport | Mechanism | Use when |
|-----------|-----------|----------|
| `PostMessageTransport` | Popup, handshaken with `icrc29_status`, then `postMessage` | Default for web wallets like OISY |
| `UrlTransport` | Navigates the top-level window; wallet returns to your `callbackUrl` | Mobile, or anywhere popups are blocked |
| `BrowserExtensionTransport` | Extensions announce themselves on `window` events | Extension wallets; discovering unknown signers |

```typescript
import { Signer } from '@icp-sdk/signer';
import { PostMessageTransport } from '@icp-sdk/signer/web';

// One Signer per wallet connection; safe to create at module scope.
const signer = new Signer({
  transport: new PostMessageTransport({ url: 'https://oisy.com/sign' })
});
```

### Extension (ICRC-94)

```typescript
import { Signer } from '@icp-sdk/signer';
import { BrowserExtensionTransport } from '@icp-sdk/signer/extension';

// Discovery order is whichever extension announced first, not a user
// preference, so return the list rather than choosing. Each provider carries
// { uuid, name, icon, rdns } — enough to render a picker.
function discoverExtensionSigners() {
  return BrowserExtensionTransport.discover();
}

// Build the signer only from the uuid the user picked.
async function connectExtensionSigner(uuid: string) {
  const transport = await BrowserExtensionTransport.findTransport({ uuid });
  return new Signer({ transport });
}
```

### Redirect (ICRC-167)

`UrlTransport` unloads your page on every request, so it keeps a call-order journal in `sessionStorage` and replays it when the wallet returns. Two rules make or break it:

1. **Issue the same requests, in the same order, on every load.** Branch only on values recovered from earlier results. A divergence guard rejects a replay that does not match.
2. **Put anything that must come back *the same value* through `memoize()`** — a nonce above all. Its result is journaled and replayed instead of re-run. Deterministic async work needs no `memoize`: building an `HttpAgent` yields an equivalent agent on every load, so it cannot drift from the journal.

`SignerAgent` works over this transport, so a redirect flow is the same code as a popup flow:

```typescript
import { IcrcLedgerCanister, toCandidAccount, type IcrcAccount } from '@icp-sdk/canisters/ledger/icrc';
import { HttpAgent } from '@icp-sdk/core/agent';
import type { Principal } from '@icp-sdk/core/principal';
import { Signer } from '@icp-sdk/signer';
import { SignerAgent } from '@icp-sdk/signer/agent';
import { UrlTransport } from '@icp-sdk/signer/web';

const transport = new UrlTransport({
  // The path is the wallet's own; ICRC-167 does not dictate one.
  url: 'https://wallet.example.com/sign',
  // Absolute, fragment-free, on an origin you control, and declared in that
  // origin's /.well-known/ii-auth-callbacks (see pitfall 9).
  callbackUrl: 'https://app.example.com/signer-callback'
});

// Run this on the load of the callback route: a fresh arrival starts the flow,
// the wallet's return replays it. No separate resume or cleanup call.
async function transferOverRedirect(
  account: IcrcAccount, to: IcrcAccount, amount: bigint, ledgerId: Principal
) {
  const signer = new Signer({ transport });

  // Deterministic, so no memoize needed — the same agent is built on each load.
  const agent = await HttpAgent.create({ host: 'https://icp-api.io' });
  const signerAgent = await SignerAgent.create({ signer, account: account.owner, agent });

  const ledger = IcrcLedgerCanister.create({ agent: signerAgent, canisterId: ledgerId });
  return ledger.transfer({
    to: toCandidAccount(to),
    from_subaccount: account.subaccount,
    amount
  });
}
```

Going through `SignerAgent` rather than `signer.callCanister` is what gets you the content-map and certificate checks; `callCanister` is the raw ICRC-49 primitive and validates only that the reply carries both fields. Prefer the agent unless you have a specific reason to drive the primitive yourself, in which case verifying the certificate before trusting the reply is your job.

## Negotiate capabilities

Skip this only if you hardcode one wallet and know what it supports. For generic integration it is the step that keeps you honest: a signer may expose accounts without executing calls, or support a transport you have not built for.

```typescript
import { Signer } from '@icp-sdk/signer';

async function capabilities(signer: Signer) {
  const standards = await signer.getSupportedStandards(); // [{ name: 'ICRC-27', url }, ...]
  const names = new Set(standards.map(({ name }) => name));
  return {
    canListAccounts: names.has('ICRC-27'),
    canCallCanisters: names.has('ICRC-49')
  };
}
```

`getSupportedStandards` needs no permission, so it is safe as a first call.

## Permissions and accounts

Most signers start every scope at `ask_on_use`, prompting the first time each method is used — but ICRC-25 leaves the initial state to signer policy, so `getPermissions()` is the only authority. `requestPermissions` is **optional**: it trades several later prompts for one up front.

| State | Behaviour |
|-------|-----------|
| `granted` | Proceeds without prompting |
| `denied` | Rejected immediately with error `3000` |
| `ask_on_use` | Prompts on first use (the usual initial state) |

```typescript
import type { PermissionScope, Signer } from '@icp-sdk/signer';

// The two scopes this skill uses:
//   [{ method: 'icrc27_accounts' }, { method: 'icrc49_call_canister' }]
async function connect(signer: Signer, scopes?: PermissionScope[]) {
  // Omitting `scopes` sets nothing: it leaves whatever states the signer
  // already holds for your origin, which a previous session may have left
  // `granted` or `denied`. Do not count on being prompted — getPermissions()
  // is the only way to know. Supply scopes to trade several later prompts for
  // one up front, and ask only for what your path uses:
  // a scope the signer does not support is dropped before the prompt is drawn,
  // so it costs nothing, but a supported one you never exercise is shown to
  // the user for no reason.
  if (scopes !== undefined) {
    await signer.requestPermissions(scopes);
  }

  // ICRC-27 returns the accounts the user chose to share, as a list: it can be
  // empty (they declined) and it can hold several. Hand it back whole and let
  // the user pick rather than indexing blindly — see pitfall 4.
  //
  // Each element is { owner: Principal, subaccount?: Uint8Array } — already an
  // IcrcAccount. Usually there is no subaccount, since signers commonly offer
  // only the default one, but keep both halves anyway: it costs nothing.
  return signer.getAccounts();
}
```

`getPermissions()` reads the current state without prompting. Do not cache it across sessions — a wallet may expire grants, after which they silently revert to `ask_on_use`.

## Executing a call the user approves

`SignerAgent` implements `Agent`, so it drops into anything that takes one: a ledger client from `@icp-sdk/canisters`, or an actor from `@icp-sdk/bindgen` for your own canister. Each call becomes a wallet prompt.

```typescript
import { IcrcLedgerCanister, type IcrcAccount } from '@icp-sdk/canisters/ledger/icrc';
import { HttpAgent } from '@icp-sdk/core/agent';
import { Principal } from '@icp-sdk/core/principal';
import { Signer } from '@icp-sdk/signer';
import { SignerAgent } from '@icp-sdk/signer/agent';

const ICP_LEDGER = Principal.fromText('ryjl3-tyaaa-aaaaa-aaaba-cai');

// Two clients against the same ledger: one for reads, one for writes.
async function connectLedger(signer: Signer, account: IcrcAccount) {
  // One HttpAgent serves both. It answers reads directly, and SignerAgent
  // borrows it for the root key and status instead of building its own.
  const agent = await HttpAgent.create({ host: 'https://icp-api.io' });
  // SignerAgent routes calls as a principal; it has no subaccount field.
  const signerAgent = await SignerAgent.create({ signer, account: account.owner, agent });

  return {
    // Anonymous by default — public reads need no wallet and no prompt.
    read: IcrcLedgerCanister.create({ agent, canisterId: ICP_LEDGER }),
    write: IcrcLedgerCanister.create({ agent: signerAgent, canisterId: ICP_LEDGER }),
    signerAgent
  };
}
```

**Read with the plain agent, write with the signer agent.** `SignerAgent.query()` upgrades every query into a full canister call routed through the wallet, so a balance check would put an approval prompt in front of the user. Public data does not need the wallet at all — read it with an ordinary `HttpAgent`, which is anonymous by default:

```typescript
import { type IcrcAccount, toCandidAccount } from '@icp-sdk/canisters/ledger/icrc';
import { Signer } from '@icp-sdk/signer';

async function showBalanceThenTransfer(
  signer: Signer, account: IcrcAccount, to: IcrcAccount, amount: bigint
) {
  const { read, write } = await connectLedger(signer, account);

  // balance() takes an IcrcAccount directly.
  const balance = await read.balance(account);                     // no prompt

  const block = await write.transfer({                                    // prompts
    // The ledger's `to` is the Candid shape; convert rather than hand-roll it.
    to: toCandidAccount(to),
    // The subaccount the tokens leave from.
    from_subaccount: account.subaccount,
    amount
  });

  return { balance, block };
}
```

`signerAgent.replaceAccount(principal)` switches which principal later writes are signed for, without rebuilding the agent.

## Channel lifecycle and page reloads

`autoCloseTransportChannel` defaults to `true`: the channel closes ~200 ms after each response, so the popup does not linger. For a multi-step flow that awaits your own async work between requests, turn it off or the channel closes underneath you.

```typescript
import { Signer } from '@icp-sdk/signer';

async function multiStepFlow(signer: Signer) {
  signer.autoCloseTransportChannel = false;
  try {
    const accounts = await signer.getAccounts();
    await saveSelectionToYourBackend(accounts);  // your own async work; channel stays open
    return await signer.requestPermissions([{ method: 'icrc49_call_canister' }]);
  } finally {
    signer.autoCloseTransportChannel = true;
    await signer.closeChannel();
  }
}
```

**A connection does not survive a page reload.** There is no persistent session to restore — the channel is a live `postMessage` link to a popup that is gone. The workable pattern is to persist the account, render read-only state from it with an anonymous agent, and re-establish the signer lazily on the first write:

```typescript
import { type IcrcAccount, decodeIcrcAccount, encodeIcrcAccount } from '@icp-sdk/canisters/ledger/icrc';
import { HttpAgent } from '@icp-sdk/core/agent';
import { Signer } from '@icp-sdk/signer';
import { SignerAgent } from '@icp-sdk/signer/agent';

const SESSION_KEY = 'wallet-account';

// On connect: remember the account, not the channel. The ICRC-1 textual
// encoding round-trips owner and subaccount as one string, so the
// subaccount survives the reload too (see pitfall 12).
function rememberAccount(account: IcrcAccount) {
  sessionStorage.setItem(SESSION_KEY, encodeIcrcAccount(account));
}

// On reload: read-only state renders from this immediately, with no popup.
function restoreAccount(): IcrcAccount | null {
  const stored = sessionStorage.getItem(SESSION_KEY);
  if (stored === null) return null;
  try {
    return decodeIcrcAccount(stored);
  } catch {
    sessionStorage.removeItem(SESSION_KEY);  // stale or malformed
    return null;
  }
}

// On the first write after a reload. This reopens the popup, so it must run
// from the click that starts that write — pitfall 1 applies here too.
async function ensureSignerAgent(signer: Signer, account: IcrcAccount, agent: HttpAgent) {
  const offered = await signer.getAccounts();  // re-establishes the channel
  // The user may have switched accounts while the page was gone, so the stored
  // one is a guess until the wallet confirms it. Compare encodings, not owners:
  // the same principal with a different subaccount is a different account.
  const id = encodeIcrcAccount(account);
  if (!offered.some((offer) => encodeIcrcAccount(offer) === id)) {
    sessionStorage.removeItem(SESSION_KEY);
    throw new Error('the wallet no longer offers the stored account; reconnect');
  }
  return SignerAgent.create({ signer, account: account.owner, agent });
}
```

Treat "disconnect" as clearing your own state — there is no wallet-side logout to call.

## Error handling

```typescript
import { Signer, SignerError } from '@icp-sdk/signer';
import { PostMessageTransportError } from '@icp-sdk/signer/web';
import type { IcrcAccount } from '@icp-sdk/canisters/ledger/icrc';

async function safeTransfer(
  signer: Signer, account: IcrcAccount, to: IcrcAccount, amount: bigint
) {
  try {
    await showBalanceThenTransfer(signer, account, to, amount);
  } catch (err) {
    // Anything that is not a SignerError — SignerAgentError above all, where the
    // wallet responded and the response failed validation — is not handled here.
    if (!(err instanceof SignerError)) throw err;

    switch (err.code) {
      case 3001: return;                       // user cancelled — not a failure
      case 3000: showPermissionHelp(); return; // permission denied
      case 2000: showUnsupported(); return;    // wallet does not support the method
      case 4000:                               // every transport failure lands here
      case 4001:                               // only if the signer itself returns it
        // The transport error is the `cause`, never the error you caught.
        if (err.cause instanceof PostMessageTransportError) showPopupBlockedHelp();
        else promptReconnect();
        return;
    }

    // ICRC-25 numbers errors by range and a signer may return a code this
    // switch has never seen, so fall back on the range rather than rethrowing.
    switch (Math.floor(err.code / 1000)) {
      case 3:
        // 3xxx is "user action", so nothing broke — but 3001 is the only code
        // where silence is right, because there you know they cancelled on
        // purpose. For an unnamed 3xxx say the action did not go through, or
        // the UI sits unchanged after the user pressed the button.
        showActionNotCompleted();
        return;
      case 2: showUnsupported(); return;       // 2xxx not supported
      case 4: promptReconnect(); return;       // 4xxx transport channel
      default: throw err;                      // 1xxx generic, and anything else
    }
  }
}
```

ICRC-25 groups errors into ranges and names a few codes inside each. Handle the codes you know, then fall back on the range — a signer may return `3002` or `4002`, and a bare `default: throw` would mishandle it:

| Range | Code | Meaning | Handle by |
|-------|------|---------|-----------|
| `1xxx` general | `1000` | Generic error | Surfacing `err.data` to developers |
| `2xxx` not supported | `2000` | Not supported | Negotiating capabilities first |
| `3xxx` user action | `3000` | Permission not granted | Explaining what to re-grant |
| | `3001` | **Action aborted — the user cancelled** | Returning quietly; this is normal |
| `4xxx` transport | `4000` | Network error | Reconnecting — the library also reports every transport failure here |
| | `4001` | Transport channel closed | Reconnecting (signer-reported only; see below) |

Two failures do not arrive as the class you would expect, and they call for opposite reactions:

- **Transport failures arrive as `SignerError` with code `4000`.** `Signer.openChannel()` catches whatever the transport threw — `PostMessageTransportError`, `UrlTransportError`, `BrowserExtensionTransportError` — and rethrows it as a `SignerError` with the original as `cause`. So a blocked popup is *not* `instanceof PostMessageTransportError`; test `err.cause` for that. The library also never emits `4001`: "channel closed before a response" is `4000` too, and `4001` reaches you only if the signer itself returns it.
- **`SignerAgentError`** — the wallet *did* respond, and the response failed validation: the returned content map did not match the call you sent (canister, method, argument, sender, nonce), the certificate did not verify against the IC root key, or the reply was absent from the certified tree. `SignerAgent` runs those checks for you, so this is a wallet returning something it should not have. Do not treat it as a connectivity fault and retry — surface it.

## Pitfalls

1. **Opening the popup outside a click handler.** `PostMessageTransport` rejects establishment that is not user-initiated (`detectNonClickEstablishment`, default `true`) because Safari and others block such popups. Connect from an event handler, never on mount or in a `useEffect`.

   ```typescript
   // WRONG — blocked, and the transport detects it
   useEffect(() => { signer.getAccounts(); }, []);

   // CORRECT
   button.addEventListener('click', () => signer.getAccounts());
   ```

2. **Reading through `SignerAgent`.** `query()` is upgraded to an update call routed through the wallet, so every read costs the user an approval interaction. Public data — a ledger balance, token metadata — needs no wallet: read it with a plain `HttpAgent`, anonymous by default. Only writes go through `SignerAgent`.

3. **Expecting a connection to survive a reload.** No channel outlives the page. Persist the account — both halves, per pitfall 12 — for read-only rendering, and reconnect on first write. See above.

4. **Indexing `getAccounts()` blindly.** It returns a *list* of the accounts the user chose to share. ICRC-27 lets the signer prompt for that selection, so the list can be **empty** — the user declined, which is not an error — and it can hold **several**, where `[0]` silently picks for them. `accounts[0]` on an empty list is `undefined`, so the crash lands later at `.owner` rather than at the call. Check the length, and offer a picker when there is more than one.

5. **Assuming a wallet's capabilities.** Call `getSupportedStandards()`. A signer may list accounts (ICRC-27) without executing calls (ICRC-49), or speak a transport you have not built for.

6. **Coding against one wallet's non-standard error codes.** ICRC-25 owns `1xxx`–`4xxx` and names `1000`/`2000`/`3000`/`3001`/`4000`/`4001` inside them. A code outside those ranges is a vendor extension and does not port — earlier revisions of this skill documented a `503 BUSY` that exists only in `@dfinity/oisy-wallet-signer` and in no standard. Branch on the named codes, fall back on the range, and treat anything outside the ranges as generic.

7. **Journaling something non-serializable through `memoize()`.** It persists via JSON, so a `Uint8Array` round-trips as `{"0":1,"1":2,…}` and a `CryptoKey` as `{}` — silently, with the flow failing on return rather than at the call. Convert to a plain array (or hex) before memoizing and back afterwards.

8. **Diverging on a redirect replay.** With `UrlTransport`, issue the same requests and `memoize` steps in the same order on every load, and route anything a request depends on — a nonce above all — through `memoize`. Re-fetching a single-use value on the return load invalidates the flow.

9. **A `callbackUrl` that is relative, carries a fragment, or is not served correctly.** It must be absolute, fragment-free (the transport appends its own), on an origin you control, and declared in that origin's `/.well-known/ii-auth-callbacks` — matched exactly, so the full URL. Declaring it is not enough: the wallet reads that document **cross-origin**, so serve it as JSON with CORS or a correctly listed callback still fails validation.

    ```json
    { "callbacks": ["https://app.example.com/signer-callback"] }
    ```

    With `@dfinity/static-site` that is a `_headers` block:

    ```
    /.well-known/ii-auth-callbacks
      Content-Type: application/json
      Access-Control-Allow-Origin: *
    ```

    Validation fails closed — undeclared, unreadable, or not matching exactly, and the response never comes back. See the **internet-identity** skill, which documents the same file for redirect sign-in.

10. **Top-level `await` in wallet code.** Every call here is async, and with `PostMessageTransport` a module-load `await` opens the popup outside a user gesture, which the transport rejects — pitfall 1. Wrap those calls in functions the UI invokes. `UrlTransport` is the exception, and the reverse: it navigates the top level rather than opening a popup, has no gesture check, and its flow *must* re-run on the callback-route load so the journal can replay — requiring a click there would break it. Either way, do not rely on the build to catch a stray top-level `await`: Vite ≤5 defaulted to `es2020` and rejected it outright, while Vite 6+ defaults to `baseline-widely-available` and allows it.

11. **`@icp-sdk/canisters@^3` with `@icp-sdk/signer@^6`.** They cannot coexist — canisters 3 peers `@icp-sdk/core@^5` or older, signer 6 peers `^6`, so `npm install` fails with `ERESOLVE`. Move to `@icp-sdk/canisters@^4` and `@dfinity/utils@^5`. Do not reach for `--legacy-peer-deps`: it skips the peer check and installs the mismatched pair anyway, so the incompatibility surfaces at runtime instead of at install time.

12. **Treating an account as just a principal.** `getAccounts()` returns `{ owner, subaccount? }` — an `IcrcAccount`. The subaccount is usually absent, because signers commonly offer only the default one, so code that assumes a bare principal works until it meets a signer that does not. Carry the account whole and let the library helpers do the rest: **compare** with `encodeIcrcAccount()` and never `owner` alone (that encoding normalizes the default subaccount, so the same principal with a *different* one is correctly a different account), **persist** with `encodeIcrcAccount()` / `decodeIcrcAccount()`, and **send** with `from_subaccount` for the sender plus `toCandidAccount()` for the recipient. `SignerAgent` is the exception — its `account` is a `Principal`, which is why the subaccount travels in the ledger call arguments instead.

13. **Firing a call immediately after connecting.** Let the user initiate. An unprompted approval dialog straight after connect reads as an attack, and wallets are within their rights to reject it.

## Testing against a real wallet

There is no local signer to run: OISY is hosted, and the transport's secure-context requirement applies to the *signer's* URL, not to your origin — `https://oisy.com/sign` satisfies it. Serving your own frontend from `localhost` is fine, and it is a browser secure context, so WebCrypto key generation works there too. Test on testnet tokens rather than mainnet value.

```bash
icp network start -d
icp deploy
```

Get free testnet tokens from the [ICP Faucet](https://faucet.internetcomputer.org) and switch OISY to the **IC (testnet tokens)** network to see them. Useful ledgers:

| Token | Ledger canister |
|-------|-----------------|
| TESTICP | `xafvr-biaaa-aaaai-aql5q-cai` |
| TICRC1 | `3jkp5-oyaaa-aaaaj-azwqa-cai` |

Set `host: 'https://icp-api.io'` on the agent even when serving from `localhost` — `host` is the API endpoint calls go to, not the origin your app is served from.

## Expected Behavior

- The first `getAccounts()` opens the wallet and resolves with the accounts the user chose to share, as `{ owner: Principal, subaccount?: Uint8Array }` — possibly none of them.
- A ledger `transfer` through `SignerAgent` shows the user the call to approve and resolves with a `bigint` block index.
- Cancelling the **canister-call approval** rejects with `SignerError` and `code === 3001`. The other two refusals look different: declining to share accounts resolves `getAccounts()` with `[]`, and denying a permission gives code `3000`.
- After a reload, read-only state renders with no popup; the first write reopens one.

## Additional References

- **internet-identity** — II sign-in, and the place to go if you need a session rather than per-action approval
- **agent-web-identity** — letting an agent or CLI act as the user in an II app
- **icp-cli** — `@icp-sdk/bindgen` actors to call your own canister through a `SignerAgent`
- **canister-security** — verifying `msg.caller` on the backend once calls arrive
- [OISY signer demo](https://github.com/dfinity/examples/tree/master/hosting/oisy-signer-demo) — a working relying party (React) built on `@icp-sdk/signer`
- [ICRC signer standards](https://github.com/dfinity/wg-identity-authentication) — the specifications behind every method above
