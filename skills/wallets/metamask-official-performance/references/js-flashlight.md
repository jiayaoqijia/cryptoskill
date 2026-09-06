---
title: Flashlight (live Android vitals)
impact: MEDIUM
tags: flashlight, fps, cpu, ram, android, live-vitals
---

# Skill: Flashlight — live Android vitals (`flashlight measure`)

> **MetaMask note:** Flashlight is an external, Lighthouse-type tool for mobile apps and is **NOT installed in this repo** — it's **not in `package.json`**. The in-repo defaults are the in-app **Perf Monitor** (quick JS-vs-UI check) and the **RN DevTools Profiler** (primary tool). Flashlight is an optional add-on when you want a **device-level, app-agnostic live vitals view on Android** (FPS/CPU/RAM/threads + a score) without wiring anything into the app. Always measure on **Android with the power-user scenario** (~30 accounts, ~90 assets — see [mm-power-user-scenario.md](mm-power-user-scenario.md)). The JS-vs-UI-thread triage lives in [mm-tools.md](mm-tools.md).

Use `flashlight measure` to watch **live** performance vitals of a running Android app while you drive the slow flow by hand. It's a Lighthouse-like tool for mobile ([flashlight.dev](https://flashlight.dev/)) that needs **no code changes** and works even on **release/production builds**.

## Quick Command

```bash
# Android device plugged in, target app open, then:
flashlight measure              # starts a local web server (interactive live UI)
flashlight measure --port 8080  # use a custom port if the default is taken
```

## When to Use

- You want a fast, at-a-glance FPS/CPU/RAM readout on a **real Android device** while reproducing jank by hand.
- You're profiling a **release/production build** where RN DevTools / dev tooling isn't available.
- You want a single **performance score** to sanity-check "is this flow bad?" before deciding where to dig in.
- Quick, interactive triage — **not** a merge gate. For reproducible before/after or CI numbers use the in-repo Reassure + `trace()` path in [mm-tools.md](mm-tools.md).

## Prerequisites

- **Android only** (iOS support is a work in progress). Use a real device where possible — emulators/simulators don't reflect real performance.
- An Android device connected over USB (with USB debugging / `adb` working) and the target app already open.
- The Flashlight CLI installed — see below.
- **Dev Mode OFF** for accurate numbers (Dev Menu → Settings → JS Dev Mode → OFF).

### Install (from a verified release)

Per the repo security guardrail ([onboarding.md](onboarding.md)): **do not pipe a remote install script straight into a shell.** The vendor advertises `curl https://get.flashlight.dev | bash` (macOS/Linux) and `iwr https://get.flashlight.dev/windows -useb | iex` (Windows) — treat these as supply-chain dependencies: download from the official release channel, pin a version, and verify the binary before running. On Apple Silicon (arm64) you'll also need Rosetta:

```bash
softwareupdate --install-rosetta --agree-to-license
```

## Step-by-Step: live measurement

1. **Connect + open the app.** Plug in the Android device and open the target app (dev or release build). Confirm `adb devices` lists it.
2. **Start the server.** Run `flashlight measure` (or `flashlight measure --port <port>`). It boots a **local web server** and prints a `localhost` URL.
3. **Open the web UI** in your browser at that URL.
4. **Auto Detect** the running app — Flashlight finds the foreground app's package ID for you (no per-app setup).
5. **Start Measuring.** Click it, then **drive the exact slow flow by hand** on the device (the audited interaction, not idle/startup).
6. **Read the live vitals** as you interact:
   - **FPS** — a single frame-rate stream, graphed over time. <55 = dropping frames. (Flashlight does **not** split JS-thread vs UI-thread FPS — that's the in-app Perf Monitor; use the per-thread CPU below to attribute a drop.)
   - **CPU** — total and **per-thread** (e.g. `mqt_js` = JS thread, `RenderThread` = native UI), so you can see which thread is hot. This is Flashlight's real thread-level signal.
   - **RAM** — resident memory over the session.
   - **Score** — an aggregate 0–100 performance rating (higher is better).
7. **Stop** when done. `measure` is live/interactive, so treat the reading as directional, not a signed-off number.

## Interpreting Results

When FPS drops, attribute it with the **per-thread CPU** breakdown (Flashlight's real thread signal) — the same JS-vs-UI logic as the [Perf Monitor / DevTools triage](mm-tools.md):

| Live signal | Likely cause | Where to go next |
|---|---|---|
| FPS drops + **`mqt_js` (JS thread) CPU high** | Expensive renders / selectors / computation on the JS thread | RN DevTools Profiler → [mm-selector-memoization.md](mm-selector-memoization.md) / [mm-redux-antipatterns.md](mm-redux-antipatterns.md) / [mm-hook-dependency-arrays.md](mm-hook-dependency-arrays.md) |
| FPS drops + **`RenderThread` (native UI) CPU high** (`mqt_js` fine) | Native rendering / animation / too many views | [mm-layout-animations.md](mm-layout-animations.md) / [native-view-flattening.md](native-view-flattening.md) |
| FPS drops + **both threads hot** | Mixed — start on the JS side | [js-profile-react.md](js-profile-react.md) |
| **RAM climbs** across a session | Leak | [js-memory-leaks.md](js-memory-leaks.md) / [native-memory-leaks.md](native-memory-leaks.md) |

Flashlight tells you **which thread and roughly how bad** (via per-thread CPU); use RN DevTools Profiler to find the exact component/function to fix.

## Scope: live triage only

`flashlight measure` is a **live, interactive** readout — performance is **non-deterministic**, so the numbers shift with how you use the app. Treat it as directional triage, not a signed-off measurement. For reproducible before/after numbers or a merge gate, use the in-repo **Reassure** (render count) + **`trace()`** (duration) path in [mm-tools.md](mm-tools.md).

## Common Pitfalls

- **Measuring in dev mode** — JS Dev Mode inflates cost; turn it off for real numbers.
- **Using an emulator** — measure on a real (ideally lower-end) Android device; that's what users feel.
- **Trusting a single reading** — it's non-deterministic; re-run to confirm a trend.
- **Letting `measure` run for a prolonged period** — the CLI can crash on long sessions. Reset/restart it often and keep each measurement short.
- **Using it as a regression gate** — it has no averaging or gate; use Reassure + `trace()` for that.
- **Assuming it's installed here** — it isn't in this repo; install it yourself from a verified release.

## Related Skills

- [js-measure-fps.md](js-measure-fps.md) - Perf Monitor + the JS-vs-UI FPS triage this builds on
- [js-profile-react.md](js-profile-react.md) - Find the exact component/function behind a JS-thread drop
- [js-lists-flatlist-flashlist.md](js-lists-flatlist-flashlist.md) - Fix scroll-related FPS drops
- [mm-tools.md](mm-tools.md) - Symptom-first tool tree and the full measurement loop
