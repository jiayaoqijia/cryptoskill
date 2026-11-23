---
name: device-capability
description: >-
  Use when creating or editing a screen or component that adds or changes
  animation (Rive, Lottie, Reanimated), lists (FlashList, FlatList), a poll
  such as a price or balance poll, prefetch, realtime or websocket data,
  heavy images, a blurred backdrop or other blur or shadows; when adding
  offline, slow-network, slow-request or low-end-device behaviour or a
  slow-connection banner; or when touching NetInfo, DeviceInfo memory
  reads, getHardwareTier, useNetworkTier or useNetworkLatency. Adapts UI
  to how capable the device and connection are, using the shared hardware
  tier, network transport tier and measured latency signals.
maturity: stable
base: true
---

# Device capability

## Purpose

Three independent signals describe how constrained the user's device and connection are: hardware tier, network transport tier and measured latency. Use them to keep the app responsive and honest on low-end and badly connected devices, while high-end devices on good links get the full designed experience.

## Why it matters

Use this section as input for your judgement. Do not recite it to the engineer.

**Why check at all.** Users range from low-RAM Android phones to current iPhones, and from offline to fast LAN. One design fails at the extremes: a blocked JS thread, the OS killing the app for memory, expensive mobile data, and timeouts that look like bugs.

**Hardware tier (memory and CPU headroom).** Drives rendering cost:

- animation weight (Rive or a static fallback);
- list window size and item complexity;
- blur and shadows;
- image decode size;
- how much work runs on mount;
- deferring below-the-fold sections until after the screen transition.

**Network tier (transport).** Drives how much the screen fetches:

- `NONE`: show local and cached data with an explicit offline state, never an endless spinner;
- `SLOW_CELLULAR`: fewer and smaller requests, no prefetch, lighter images, slower polling;
- `WIFI` and `FAST_CELLULAR` describe the transport, not the speed or the cost.

**Measured latency.** Drives honesty about waiting:

- `SLOW` is the signal to tell the user the connection is slow and to prefer cached or optimistic UI;
- show skeletons instead of blank screens;
- avoid retry storms;
- use the settled variant for UI that must not flicker on resume;
- latency is the only signal that catches a slow `WIFI`.

## Principles

- Degrade, do not remove. Core wallet actions (send, sign, swap confirmation, security warnings) are never hidden or blocked because of a tier.
- Unknown (`null` or `UNKNOWN`) falls back to the product default, never to the lowest tier.
- Keep the three signals separate. Never fold them into one "worst of" flag.
- Each adaptation names a concrete lever and the reason the user benefits.
- Do not cut everything because a screen feels slow. Measure any claimed performance gain with `performance`.

## Workflow

This skill never pauses the task and never asks the engineer to confirm. Pick the mode from the phase you are in.

**Planning mode** (plan, spec, brief or design question):

1. Name the signals that apply to the planned surface.
2. Add one "Device capability" line to the plan with the likely matrix cell and levers.
3. Do not ask a separate question, and do not block approval of the plan on this point.

**Editing mode** (code change):

1. Check whether the change touches a trigger surface: animation, lists, polling, prefetch, realtime, heavy images, blur, or offline and slow-network behaviour. If not, stop using this skill.
2. Read the hardware and network tiers, and latency when the screen waits on the network.
3. Find the matrix cell.
4. Apply that cell's levers inside the files the task already touches, without asking.
5. List anything outside that scope (a shared hook, another screen, a matrix change) as a follow-up. Do not make it.
6. If the engineer's instruction conflicts with the cell, follow the instruction. Tier handling that adds to the requested feature without contradicting it still applies, for example a static fallback around a requested animation on `LOW`.
7. In the final summary, report the cell, the levers and any conflict or follow-up in one or two lines. If the engineer's instruction conflicted with the cell, that line names the conflict. Do not ask before the edit.
8. Do not migrate unrelated screens.

## UX matrix and levers

Where this table and the repository's canonical device capability doc disagree, the doc wins.

1. Read the hardware tier and the network tier.
2. Use the cell below. `null` hardware → network column only. `null` network → never treat as LOW or `'NONE'` (use the product default / MID-safe path).
3. Report the cell and the levers you changed on **this** screen.

| Hardware \\ Network | `NONE`                                    | `SLOW_CELLULAR`                        | `FAST_CELLULAR` / `WIFI`                            | `null` network                            |
| ------------------- | ----------------------------------------- | -------------------------------------- | --------------------------------------------------- | ----------------------------------------- |
| **LOW**             | Local UI only: no fetch, no Rive, no blur | Less animation, rare poll, no prefetch | Light animation, short list, no extra work on mount | MID-safe / product default — never as LOW |
| **MID**             | Same as LOW × `NONE`                      | Debounce, fewer previews               | Product default                                     | Product default                           |
| **HIGH**            | Same as LOW × `NONE`                      | Still save radio (images, prefetch)    | Full experience                                     | Product default                           |
| **`null` hardware** | Network only (`NONE` row)                 | Network only                           | Product default                                     | Product default                           |

`WIFI` and `FAST_CELLULAR` are not speed. Measured latency is a separate signal. The difference between them is LAN (`wifi` and `ethernet`) versus cellular radio (`4g` and `5g`). Do not derive bandwidth or a data cap from either tier.

Levers: Rive vs static fallback, list window and item types, poll interval, prefetch, image quality, blur and shadows.

`HIGH` + `WIFI` / `FAST_CELLULAR` = ship the designed experience. `LOW` + `NONE` = local only. Do not "cut everything" because a screen feels slow.

## Forbidden patterns

- A parallel RAM classification. Read the shared hardware tier.
- A parallel NetInfo classifier. Read the shared network tier.
- Reimplemented latency cutoffs. Read the shared latency signal.
- A tier decision taken from simulator or emulator RAM, which can report the host machine's memory.

The repository overlay gives the exact calls and paths.

## Related skills

- `performance` to measure a claimed gain.
- `mobile-visual-testing` to check a tier-aware screen on a simulator or emulator.
