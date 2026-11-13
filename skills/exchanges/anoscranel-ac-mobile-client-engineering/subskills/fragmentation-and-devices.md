---
name: fragmentation-and-devices
domain: software-engineering/fragmentation-and-devices
trigger: "Handling OS version and device capability differences across a base."
anti_trigger: "Not for responsive layout, and not for store policy."
scope: "OS versions, screen classes, and hardware capability tiers."
status: seedling
---

# Fragmentation and devices

## Standard

A mobile app runs on a distribution of operating-system versions, screen sizes, memory limits, and hardware capabilities that you do not choose and cannot reduce. The engineering response is not to support everything equally but to define tiers: a set of capability classes that the app supports deliberately, with a stated floor and a stated degradation for devices above it.

Capability detection is more reliable than version detection. A version number tells you what the platform might support; a runtime check tells you what this device supports. Checking for the feature and degrading gracefully is robust across updates, manufacturer variations, and emulators, while branching on a version string encodes an assumption that will eventually be wrong.

Primary sources: <https://developer.android.com/> and <https://developer.apple.com/>.

## Decision rules

- Record the OS versions in the active base, by share, with a date.
- Record the capability tiers the app supports and the floor of each.
- Record the degradation path for a device below the preferred tier.
- Record the runtime capability checks and where they are performed.
- Record the screen classes supported and how layout adapts.
- Record the memory floor and what the app does when it is exceeded.

## Procedure

1. Measure the OS and device distribution and record it with a date.
2. Define capability tiers and the floor.
3. Record a degradation path for each tier boundary.
4. Implement runtime capability checks rather than version branches.
5. Record the layout adaptation across screen classes.
6. Record the memory behaviour and the low-memory path.

## Anti-patterns

- Branching on a version string where a capability check would do.
- Assuming the newest APIs exist on every device in the base.
- Supporting every screen size by scaling one layout.
- Ignoring low-memory behaviour until a crash report arrives.
- Measuring the distribution once and never again.

## Done checklist

- [ ] OS distribution measured with a date.
- [ ] Capability tiers and floor recorded.
- [ ] Degradation paths recorded.
- [ ] Runtime checks recorded.
- [ ] Screen classes recorded.
- [ ] Low-memory path recorded.

The tier definition should also state what happens at the boundary in the other direction: a device above the floor but below the preferred tier runs the degraded path, and if that path is never exercised in testing it becomes a latent defect that appears only in the field. Testing one device per tier, deliberately, is cheaper than discovering the tier boundary from crash reports.


## Sources

- Android device and version distribution guidance: <https://developer.android.com/>
- Apple device and OS support guidance: <https://developer.apple.com/>
- Web accessibility and adaptation reference: <https://www.w3.org/>
