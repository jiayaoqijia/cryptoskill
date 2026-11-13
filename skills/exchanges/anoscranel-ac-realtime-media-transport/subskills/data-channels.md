---
name: data-channels
domain: software-engineering/data-channels
trigger: "Using structured data between the same connected peers."
anti_trigger: "Not for the media path, and not for messaging products."
scope: "Datagrams and streams between the same peers."
status: seedling
---

# Data channels

## Standard

Between two connected peers, the same transport carries arbitrary data alongside audio and video. A data channel rides the same established path, camps on the same security provisions, and delivers either datagram semantics — each message arrives once and whole, or is lost — or a reliable stream that retransmits like TCP. The choice is intrinsic and is made when the channel is created; a game state update wants unreliability because a late world-position is worthless, while a file transfer wants the reliable mode because a missing byte poisons the whole.

The cost model of a data channel is the cost of the established path. A relayed call pays per megabit through TURN, and the data channel rides that same meter. Buffering behaviours across implementations vary on backpressure — a channel that accepts more than it can send on a constrained path queues rather than blocks — and the honest design ties quantity to what the path carries. The failure mode of data channels is abundance: a protocol that spams updates at a rate the path cannot support degrades the very media the call was established to carry.

Primary sources: <https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API> and <https://webrtcforthecurious.com/>.

## Decision rules

- Choose ordered or unordered and reliable or unreliable at channel creation based on what each message means, and record the choice as part of the feature design.
- Treat the data channel as riding the same meter as the media: a volume decision here is a bandwidth decision there.
- On constrained paths the reliable mode queues; monitoring queue depth or applying application-level flow control is the design, not silent memory growth.
- Datagrams lost on an unreliable channel are expected, not errors; the protocol above must tolerate loss by design rather than complaining about it.
- Do not multiplex unrelated logical streams over one channel without a framing protocol that could not be mistaken for the default.
- Prefer one well-designed message schema over an ad-hoc configuration; a data channel whose message format lives in the heads of two developers does not survive either of them.

## Procedure

1. Inventory the message types the feature needs and their loss tolerance.
2. Decide the channel mode per message type; unreliable and unordered demands loss-tolerant design above.
3. Define the message schema and its versioning.
4. Implement backpressure handling for the reliable mode on a constrained path, and test under a throttled network.
5. Verify the messages go through DTLS, and that no test path replaces the encrypted media transport with a plaintext alternative.
6. Record the channel modes, the schema, and the throttle test numbers in the realtime record.

## Anti-patterns

- A reliable ordered channel carrying game state, delivering a paused game a stale past rather than a late present.
- Unreliable messages whose consumers do not tolerate loss.
- Backpressure ignored on ARM devices until the tab dies in production.
- Two logical protocols mixed on one channel, with no framing to separate them.
- A message schema implied by code on both ends, never written, drifted between platforms.

## Done checklist

- [ ] Channel modes chosen per message type.
- [ ] Schema defined and versioned.
- [ ] Backpressure tested on a constrained path.
- [ ] Loss tolerance proven for unreliable channels.
- [ ] One protocol per channel or a stated framing layer.
- [ ] Choices and throttle numbers in the record.

## Sources

- WebRTC API and data channels: <https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API>
- The stack explained: <https://webrtcforthecurious.com/>
- The WebRTC overview: <https://webrtc.org/getting-started/overview/>
