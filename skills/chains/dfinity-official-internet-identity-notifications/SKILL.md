---
name: internet-identity-notifications
description: "Notify a signed-in Internet Identity user from your canister while the app is closed, with web push that II owns end to end, so there is no push service, no VAPID keys and no device tokens in the app. Covers consent in the frontend (requestNotificationConsent, getNotificationConsentStatus, revokeNotificationConsent, needing @icp-sdk/auth 11.1.0), the /.well-known/ii-notification-senders document, and sending with the identity-notifications library from Motoko or Rust. Use when an app must reach a user who is not looking at it, when adding web push or a notifications toggle, or when consent was granted and nothing arrives. Assumes sign-in already works and the app's primary origin is settled: load internet-identity first. Do NOT use for in-app notification UI or email, or for reaching anyone who is not a signed-in user of this app."
license: Apache-2.0
compatibility: "@icp-sdk/auth >= 11.1.0, moc >= 2.0.0"
metadata:
  title: Internet Identity Notifications
  category: Auth
---

# Internet Identity Notifications

## Prerequisite

Load the `internet-identity` skill first. Two things from it are load-bearing here: the sender list is served from the app's **primary origin**, the same origin `ii-app-metadata` is read from, and that metadata is what names the app on its own notifications.

A suite shares one sender list and one 10-canister cap across every app derived from that origin.

## Notifications

Your canister can notify a signed-in user while the app is closed. II owns the push subscriptions, so there is no push service, no VAPID keys, and no device tokens in the app.

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
- Consent is recorded against the identity, and the browser the user answered on is the one registered for delivery. Someone who wants your notifications on a second machine answers again there. The status call reports the consent alone and does not speak for the device in the user's hand.

### Asking with the sign-in

The sign-in button is already a click, so that is the cheapest place to ask. Run both from it and the user signs in and answers in one visit to II rather than two:

```javascript
const [identity, { granted }] = await Promise.all([
  authClient.signIn(),
  authClient.requestNotificationConsent(),
]);
```

Asking at any later moment needs a control of its own.

### A toggle, later

To show the user whether your app may notify them, and let them turn it off:

```javascript
const { granted } = await authClient.getNotificationConsentStatus();
await authClient.revokeNotificationConsent();
```

Revoking is scoped to your app. It drops your origin's consent and whatever you still had queued for that user, and leaves their device subscriptions and every other app's consent alone. So dropping someone from your own recipient table revokes nothing, and revoking is not an unsubscribe.

Errors worth branching on:

| Error | Means | Remedy |
|---|---|---|
| `InteractionRequiredError` | Client built with `prompt: 'none'` | Ask again from a click |
| `NotificationsUnsupportedError` | That II deployment does not notify at all | Hide the control; nothing to retry |
| `SessionGoneError` | No live session (status and revoke only) | Sign in again |

## 2. The senders document

Serve from the **primary origin**, the same origin as `/.well-known/ii-app-metadata`:

```json
{ "senders": ["ryjl3-tyaaa-aaaaa-aaaba-cai"] }
```

- At most **10** canisters. A longer list is rejected whole, never truncated.
- II caches what it reads, so a canister added is not accepted instantly and one removed keeps working for a while afterwards.
- Without this document naming the sending canister, every send is refused. This is the most common cause of "nothing arrives and nothing errors".

A suite shares one sender list and one cap of 10 across every app derived from that origin.

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

## Choosing `urgency` and `expiresAt`

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

## `key`

The id is `hash(recipient, key)`, so a key reaches only that recipient's own entry: it cannot touch another user's notification or another app's. What it can do is collide with this app's other pending notification to the same recipient, and the later send wins. Derive `key` from the thing the notification is about, such as the conversation, rather than from whatever a caller passed in.

`metrics()` reports the pipeline hour by hour, and is the only place a notification's fate shows up, since `send` returns nothing.

## What the app does and does not own

- **The app addresses a user, nothing finer.** II holds a queue per browser that identity has registered, so one `send` can surface on a laptop and a phone at once. Where and how a notification reaches them is II's and the user's to manage, and an app that reasons about it is coupling itself to something it cannot see.
- **II composes what is shown.** The user reads your app's name, then the title your canister sent. The name comes from `/.well-known/ii-app-metadata`, and falls back to your origin's hostname where you publish none, so do not put your app's name in `title` yourself: it arrives twice. Publishing that document is what brands the notifications as well as the sign-in screen: see "App metadata on the sign-in screen" in the `internet-identity` skill.
- **Sending cannot fail the call it is made from.** `send` neither traps nor awaits, so a recipient who cannot be notified costs the endpoint nothing and returns nothing to branch on. What became of a notification is in `metrics()`.
- **iOS needs II added to the Home Screen** for web push. The consent ceremony walks the user through it; the app does nothing.

## Upgrades

**Motoko: nothing to do.** There is no post-upgrade call to make and no ids to pass back in.

**Rust: call `init` again from `post_upgrade`.** No timer survives a canister upgrade, so without that second call anything already queued stays queued and is never sent. It is not optional and it is not a no-op on a canister that was running a moment ago.

Pass the same `MemoryId`s every time. Renumbering them on a running canister points the library at empty memories instead of the ones holding the queue, and whatever was waiting is gone.

## Mistakes That Break Your Build

1. **Asking without a click.** The ceremony has to render, so it needs a user gesture: the sign-in button, or a control of your own. See "1. Consent, in the frontend".
2. **Asking under `prompt: 'none'`.** Same reason, and it raises `InteractionRequiredError` rather than answering a refusal. Ask again from a click.
3. **Treating a refusal as an error.** `granted: false` is the user's answer. Render it, and offer the control again later.
4. **Reading the answer as a boolean.** All three calls answer a record, so `const granted = await authClient.requestNotificationConsent()` type-checks and is always truthy.
5. **Leaving the senders document out.** Without `/.well-known/ii-notification-senders` naming the sending canister, every send is refused and nothing anywhere reports it. See "2. The senders document".
6. **Putting your app's name in `title`.** II puts it in front of the title you sent, so the user reads it twice. See "What the app does and does not own".
7. **Deriving `key` from whatever a caller passed in.** Two of your own sends under one key collide in that recipient's tray and the later one wins. See "`key`".
8. **Skipping `init` in `post_upgrade`, in Rust.** Anything queued stays queued and is never sent. The Motoko mixin needs no such call. See "Upgrades".
