---
name: ac-realtime-media-transport
description: "Moving live audio and video between peers: the ICE gathering and connectivity checks that find a path through network address translation, STUN as the map of one's own address, TURN as the relay of last resort, the offer and answer handshake that exchanges media descriptions, the SDP blob and its many settings, secure transport as mandatory not optional, and the written realtime record. It explains how peer-to-peer realtime media connects and behaves; it never recommends a media library and never promises a call quality. Use when asking \"WebRTC\", \"ICE candidate\", \"STUN\", \"TURN\", \"SDP\", \"offer answer\", \"NAT traversal\", \"peer connection\", \"signaling\", \"media stream\", \"data channel\", \"why does my call not connect\", \"relay fallback\". Not for application-level video product design (ac-frontend-ui), not for the sending application's network edge (ac-network-edge-and-delivery), not for notification delivery (ac-notification-systems)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Realtime media transport

## Overview

Two peers behind home routers must find each other, and the network is actively in the way: address translation hides endpoints, firewalls drop unsolicited packets, and the path that works may be one relay through a third party. The ICE framework collects every candidate path — local addresses, mapped addresses a STUN server reports, and relayed addresses a TURN server offers — then probes them in order until one connects. On top of the connected path rides the media itself: RTP streams carrying audio and video, with DTLS-encapsulated keys and SRTP encryption as defaults, not options, in the modern stack.

The application's signalling — the offer, answer, and candidate exchange — is deliberately left to the application, which is why realtime systems enter the world half-built. The peer connection only establishes connectivity once the other side knows about it through channels the WebRTC standard does not define. This skill covers the transport layer: gathering, the handshake, the media path, the security defaults, and the failure modes that make a call not connect.

Primary sources: <https://webrtc.org/getting-started/overview> and <https://developer.mozilla.org/en-US/docs/Web/API/WebRTC_API>.

## When to use

- Implementing or debugging peer-to-peer audio, video, or data channels.
- Designing the signalling exchange that connects two peers.
- Diagnosing call connectivity failures and relay fallbacks.
- Reviewing the mandatory security provisions of a realtime implementation.

## When NOT to use

- For video-call product design and UX (use ac-frontend-ui for the client layer).
- For CDN and edge delivery of recorded media (use ac-network-edge-and-delivery).
- For notification delivery to users' channels (use ac-notification-systems).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/nat-traversal-and-ice.md` | `software-engineering/nat-traversal-and-ice` | Candidates, checks, and the checkpoint through NAT. |
| `subskills/stun-and-turn.md` | `software-engineering/stun-and-turn` | The mapped address and the relay a symmetric NAT forces. |
| `subskills/signaling-and-handshake.md` | `software-engineering/signaling-and-handshake` | Offer, answer, and the application-owned exchange. |
| `subskills/sdp-and-media-negotiation.md` | `software-engineering/sdp-and-media-negotiation` | The session description, its codecs, and what the handshake carries. |
| `subskills/security-mandatory.md` | `software-engineering/security-mandatory` | DTLS keys and encrypted media as defaults, not options. |
| `subskills/data-channels.md` | `software-engineering/data-channels` | Datagrams and streams between the same peers. |
| `subskills/realtime-record.md` | `software-engineering/realtime-record` | The written record of candidates, paths, and connection states. |

## Status and honest limits

Realtime connectivity is situational: the candidate list is a property of two networks on the day of the call, and no measurement transfers. The security defaults have exceptions in legacy stacks and in non-browser implementations, and non-standard client libraries differ. The signalling channel itself is the application's responsibility — the transport standards deliberately do not define it — which is therefore the place implementations most often diverge in unexpected, and conventionally undocumented, ways.
