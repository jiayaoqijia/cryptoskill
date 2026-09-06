---
title: Power-User Scenario (MetaMask)
impact: HIGH
tags: testing, baseline, android, scale, power-user
---

# Skill: The Power-User Scenario

A feature that is fast with 1 account and 5 tokens can be unusable with 30 accounts and hundreds of assets. Performance problems in MetaMask scale **superlinearly** with user data (broken selectors cascade, lists grow, computations repeat). So every performance measurement must use a realistic heavy profile, on the more sensitive platform.

## The two rules

1. **Always develop and measure on Android.** It is more sensitive to performance problems than the iOS simulator and closer to the bulk of the user base. A change that's smooth on an iPhone simulator can be janky on a mid-range Android.
2. **Always test against the power-user scenario:** approximately **30 accounts** and **90 assets**. Verify interactions feel instant at that scale, not just with a fresh wallet.

> The canonical persona ("Mobile User Persona Definition") lives outside the repo. Treat **~30 accounts / ~90 assets** as the working baseline; confirm the current numbers with the Mobile Platform team if precision matters for a quality gate. Ready-made power-user wallets are in the **[Power-user SRPs](https://consensyssoftware.atlassian.net/wiki/spaces/TL1/pages/401401446401/Power-user+SRPs)** Confluence page.

> **The scaling axis is feature-dependent.** "~30 accounts / ~90 assets" is the default axis (account/asset-bound features). But the axis that stresses a feature is whatever it scales on: **perps/markets → market count** (testnet, all categories); **activity → transaction count**; **notifications → notification count**; **DeFi → positions across protocols/chains**. Pick the axis the feature actually grows on, and push it.

## Why this catches what unit tests miss

- **Selectors:** a broken `createSelector` returns a new reference per dispatch. With 2 accounts the re-render storm is invisible; with 30 it's a visible stall. See [mm-selector-memoization.md](mm-selector-memoization.md).
- **Lists:** a `ScrollView`+`.map()` or an unoptimized `FlatList` is fine at 10 items and freezes at 90. See [js-lists-flatlist-flashlist.md](js-lists-flatlist-flashlist.md).
- **Per-item work:** an expensive computation in a list item multiplies by item count.
- **Memory:** leaks and large persisted state only bite over long sessions with lots of data.

## How to set it up

- Use a seed/test wallet provisioned with ~30 accounts and a spread of ~90 assets across networks. Import a ready-made one from the **[Power-user SRPs](https://consensyssoftware.atlassian.net/wiki/spaces/TL1/pages/401401446401/Power-user+SRPs)** page (handle these SRPs as test-only credentials — never reuse them for anything holding real funds).
- Run a **release / no-dev** build for timing accuracy (dev mode is artificially slow): Android Dev Menu → Settings → JS Dev Mode → OFF, or build a release variant.
- Then measure with the tools in [mm-tools.md](mm-tools.md).

## Acceptance-criteria template (Planning)

```
- [ ] No FPS drop below ~55 on a mid-range Android during [interactions], power-user data
- [ ] [Flow] completes within [X] ms under the power-user scenario (measured via trace())
- [ ] Memory stays flat over an [N]-minute session with power-user data
- [ ] Verified on Android with ~30 accounts / ~90 assets
```

## Related

- [mm-planning.md](mm-planning.md) — bake this into acceptance criteria
- [mm-tools.md](mm-tools.md) — measure once the scenario is loaded
