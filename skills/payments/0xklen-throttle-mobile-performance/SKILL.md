---
name: throttle-mobile-performance
description: Use when a page passes on a fast desktop but fails on phones. Reproduces mid-tier mobile CPU and slow-network conditions before optimizing.
---

# Throttle Mobile Performance

Optimizing against an M-series laptop measures the wrong machine. Your median user is on a mid-tier Android over congested 4G, and the gap is routinely a 4-6x slowdown.

## Procedure

1. Run Lighthouse in its mobile preset, which applies CPU throttling and simulated slow network:

       npx lighthouse https://shop.example.com --preset=perf --form-factor=mobile \
         --throttling-method=simulate --throttling.cpuSlowdownMultiplier=4 --chrome-flags="--headless"

2. For interactive work, use DevTools Performance with CPU throttling set to `4x slowdown` and Network to `Slow 4G` (1.6 Mbps down, 750 kbps up, 150 ms RTT).
3. Compare the same page with and without throttling; a TBT over 300 ms that shows 40 ms unthrottled is a script problem, not a network one.
4. Confirm the emulated device class matches reality by checking `navigator.hardwareConcurrency` (a mid-tier phone reports 4-6, a laptop 8+) and pick the matching CPU multiplier.
5. Inspect long tasks under throttling:

       # Performance panel -> Bottom-up -> Group by "Script" -> look for tasks over 50 ms

6. Re-test on a real low-end device over a real network at least once per milestone; emulation understates GPU and memory pressure.
7. Set the budget against the throttled profile: LCP <= 2500 ms on mobile emulation, TBT <= 200 ms.

## Pitfalls

- Trusting an unthrottled desktop score in CI as the regression gate; the mobile number is what breaks first.
- Applying only network throttling when the bottleneck is main-thread JS, or only CPU throttling when it is bytes.
- Assuming simulated throttling equals a real device; a 4x multiplier undersells a truly slow phone.
- Comparing runs on a laptop plugged in with no thermal pressure against a phone in a pocket.
- Re-running on a different machine and attributing the delta to your change rather than to the hardware.

## Verification

    npx lighthouse https://shop.example.com --preset=perf --form-factor=mobile --throttling-method=simulate --quiet --output=json | jq '{fcp:.audits."first-contentful-paint".numericValue, tbt:.audits."total-blocking-time".numericValue}'

TBT under 200 ms on the mobile preset is the pass. Report both numbers and the throttling multiplier used.
