# Notifications

Web push to a signed-in user while the app is closed. II owns the subscriptions: no push service, no VAPID keys, no device tokens in the app.

Three pieces, all required. Missing any one of them produces silence rather than an error at the point you left out.

1. The frontend asks for consent, through II.
2. The origin names the sending canister at `/.well-known/ii-notification-senders`.
3. The canister sends, through the `identity-notifications` library.

## 1. Consent, in the frontend

Needs `@icp-sdk/auth` 11.1.0 or later. Earlier 11.x has none of these methods.

```javascript
const { granted } = await authClient.requestNotificationConsent();
const { granted } = await authClient.getNotificationConsentStatus();
await authClient.revokeNotificationConsent();
```

| Call | Opens II | Needs a session | Answers |
|---|---|---|---|
| `requestNotificationConsent()` | Yes | No; signs the user in if needed | `{ granted }`, what II recorded |
| `getNotificationConsentStatus()` | No | Yes | `{ granted }`, uncertified query |
| `revokeNotificationConsent()` | No | Yes | nothing; idempotent |

- All three answer a **record**, not a bare boolean. `const granted = await ...requestNotificationConsent()` is wrong and type-checks as an object.
- `granted: false` is the user's refusal, not a failure. Render it; do not throw.
- Asking a second time when consent is already held returns `{ granted: true }` without showing a screen, because the answer is read back from the canister rather than reported from the ceremony.
- `getNotificationConsentStatus` is a query, so the answer is uncertified. Paint a toggle from it; do not gate anything on it.
- Ask from a click. The ceremony renders, so it cannot run under `prompt: 'none'`.

Errors worth branching on:

| Error | Means | Remedy |
|---|---|---|
| `InteractionRequiredError` | Client built with `prompt: 'none'` | Ask again from a click |
| `NotificationsUnsupportedError` | That II deployment does not notify at all | Hide the control; nothing to retry |
| `SessionGoneError` | No live session (status and revoke only) | Sign in again |

## 2. The senders document

Serve from the **derivation origin**, the same origin as `/.well-known/ii-app-metadata`:

```json
{ "senders": ["ryjl3-tyaaa-aaaaa-aaaba-cai"] }
```

- At most **10** canisters. A longer list is rejected whole, never truncated.
- II caches what it reads, so a canister added is not accepted instantly and one removed keeps working for a while afterwards.
- Without this document naming the sending canister, every send is refused. This is the most common cause of "nothing arrives and nothing errors".

## 3. Sending

Library: `identity-notifications`, same `send` in both languages, different wiring. Rust is on crates.io, Motoko on Mops (requires moc 2.0.0 or later).

**Rust** needs `endpoints!()` plus three stable `MemoryId`s handed to `init`, and `init` called again from `post_upgrade`. **Motoko** needs neither: the mixin brings the endpoints and keeps its own state, and there is nothing to do on upgrade. Do not tell a Motoko user to pass memory ids; there are none.

```toml
identity-notifications = "0.1"
```

```rust
use identity_notifications as notifications;
use identity_notifications::{Memories, Notification};

notifications::endpoints!();          // the endpoints II calls back on

#[init]      fn init()         { init_notifications(); }
#[post_upgrade] fn post_upgrade() { init_notifications(); }

fn init_notifications() {
    MEMORIES.with_borrow(|manager| {
        notifications::init(manager, Memories {
            entries: MemoryId::new(10),
            content: MemoryId::new(11),
            metrics: MemoryId::new(12),
        })
    });
}

notifications::send(to, Notification {
    title: "New message".into(),
    body: text,
    url: Some(format!("https://chat.example.com/chats/{from}")),
    key: Some(format!("chat-{from}")),
    ..Default::default()
});
```

```motoko
import Notifications "mo:identity-notifications";

actor {
  include Notifications<system>();

  notifications.send<system>(to, {
    title = "New message";
    body = text;
    url = ?("https://chat.example.com/chats/" # caller.toText());
    key = ?("chat-" # caller.toText());
    urgency = null;
    expiresAt = null;
    funnel = null;
  })
}
```

Configuration is environment variables, not init arguments:

```yaml
canisters:
  - name: backend
    settings:
      environment_variables:
        notification_sender:      "rdmx6-jaaaa-aaaaa-aaadq-cai"   # the II canister
        notification_origin:      "https://your-app.icp0.io"
        notification_capacity_mb: "1024"   # optional
```

## The optional fields

| Field | Default | What it is for |
|---|---|---|
| `url` | none | Where acting on it takes the user. Must be the sending origin or one of its alternative origins; II refuses anything else. |
| `key` | none | What the notification is *about*. A second send under the same key **updates** that notification instead of adding another, and it is what `dismiss(recipient, key)` names. |
| `urgency` | `Normal` | `VeryLow`, `Low`, `Normal`, `High`. Schedules this notification against the origin's other traffic. **Not a rendering hint**, and honoured on channels with no tray. |
| `expiresAt` / `expires_at` | a short window | How long this is still worth sending. Set past the default for anything that matters later; short for anything worthless once the moment passes. |
| `funnel` | none | Which funnel to count it in. A label per notification is an unbounded set of rows: use one per campaign or kind, not per send. |

### Choosing `urgency` and `expiresAt`

Different questions: `urgency` is where this sits against the origin's **other traffic**, `expiresAt` is whether it is still worth showing when it could be. Pick both together.

**Unset is a short default**, so anything still worth delivering later needs an explicit value. It is not a tray lifetime: a delivered notification stays until the user clears it. `expiresAt` bounds how long the notification is still worth sending at all, and the library does not cap a longer value.

| Sending | `urgency` | `expiresAt` | Why |
|---|---|---|---|
| Security alert, new sign-in | `High` | days | Ahead of other traffic, and worth seeing late, so set well past the short default. |
| Direct message | `Normal` | unset | Worth sending now, noise much later. |
| "Your driver is outside" | `High` | minutes | Ahead of everything, worthless once passed. |
| Campaign to the whole user base | `VeryLow` | days | None is urgent and a large send must not push real notifications behind it, but each should still land. Give the campaign a `funnel` and its conversion rate is readable on its own. |
| Digest, nudge, streak reminder | `Low` | hours | Yields to anything else, and yesterday's is pointless. |

A short expiry does not make something urgent, and `High` does not make it last longer. `High` on everything removes the ordering it was reached for.

### `key`

The id is `hash(recipient, key)`, so a key reaches only that recipient's own entry: it cannot touch another user's notification or another app's. What it can do is collide with this app's other pending notification to the same recipient, and the later send wins. Derive `key` from the thing the notification is about, such as the conversation, rather than from whatever a caller passed in.

`metrics()` reports the pipeline hour by hour, and is the only place a notification's fate shows up, since `send` returns nothing.

## What the app does and does not own

- **The app addresses a user, nothing finer.** Where and how a notification reaches them is II's and the user's to manage, and an app that reasons about it is coupling itself to something it cannot see.
- **II composes what is shown**, so the app's name is not in the app's own payload. Publishing `/.well-known/ii-app-metadata` is what names the app on its notifications as well as on the sign-in screen: `references/app-metadata.md`.
- **Sending cannot fail the call it is made from.** `send` neither traps nor awaits, so a recipient who cannot be notified costs the endpoint nothing and returns nothing to branch on. What became of a notification is in `metrics()`.
- **iOS needs II added to the Home Screen** for web push. The consent ceremony walks the user through it; the app does nothing.

## Upgrades

**Motoko: nothing to do.** The mixin keeps its own state and re-arms itself.

**Rust: call `init` again from `post_upgrade`.** The library's state lives in the stable memories handed over, so an upgrade neither serialises nor restores any of it, and no timer survives an upgrade, so that second `init` is what arms a flush for anything still waiting.

Renumbering those `MemoryId`s on a canister already running abandons the old memories rather than migrating them, which discards whatever was waiting.
