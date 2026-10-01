# Copy-trade addresses vs. realized PnL — corrected 2026-09-30

**Correction:** 3 of the 8 verdicts we published on 2026-09-28 were wrong — our bug, not the
wallets. Solana now has version-1 transactions; our data fetcher requested version 0 and
silently lost them, so three wallets looked "unverifiable" (rows marked ¹ below). Fixed on
2026-09-30 and re-run.

**Re-run 2026-09-30 (evening, UTC): 0 of 8 TRUSTED, 4 of 8 UNTRUSTED.**

| listed as | address | verdict | realized SOL | coins | published 2026-09-28 |
|---|---|---|---|---|---|
| LJC | `6HJetMbdHBuk3mLUainxAPpBpWzDgYbHGTS2TqDAUSX2` | INSUFFICIENT | 0.0 | 1 | INSUFFICIENT |
| Ansem-label | `AVAZvHLR2PcWpDf8BXY4rVxNHYRBytycHkcB5z5QNXYm` | **UNTRUSTED** | −2.4 | 7 | INSUFFICIENT (window moved) |
| OGAntD | `215nhcAHjQQGgwpQSJQ7zR26etbjjtVdW74NLzwEgQjP` | INSUFFICIENT | −82.7 | 3 | INSUFFICIENT |
| SKX | `C4eZg1rJX6v1u7LzqermPrA1pDNNxQe6g3vyY5cHHoWq` | **UNTRUSTED** | −3.4 | 11 | UNVERIFIABLE ¹ |
| Cooker | `8deJ9xeUvXSJwicYptA9mHsU2rN2pDx37KWzkDkEXhU6` | **UNTRUSTED** | −28.0 | 31 | TRUSTED +6.2 — lost since, not a bug |
| ozark | `DZAa55HwXgv5hStwaTEJGXZz1DhHejvpb7Yr762urXam` | NEUTRAL | +0.1 | 8 | UNKNOWN ¹ |
| rayan | `BNahnx13rLru9zxuWNGBD7vVv1pGQXB11Q7qeTyupdWf` | **UNTRUSTED** | −115.0 | 7 | UNVERIFIABLE ¹ |
| trunoest | `ardinRsN1mNYVeoJWTBsWeYeXvuR9UUDGMsCDKpb6AT` | UNKNOWN (no DEX trades in window) | — | — | UNKNOWN |

¹ **Our bug, not the wallet:** on 2026-09-28 the old and the fixed code disagreed exactly on
these rows when both were run at the same moment on 2026-09-30. Where they agreed (e.g.
Cooker), the change is real trading since 09-28.

Verdicts cover a **recent window** of trades, not a lifetime. Active wallets can flip within
hours — ozark and SKX changed between our morning and evening re-runs on 2026-09-30. Re-check
before every copy: https://pnllabs.com/GATE.md

"listed as" = the label a public copy-trade list attaches to the address. It is **not** a
claim about who controls the wallet. This is a test of the leaderboard metric, not of any person.

## Original table 2026-09-28 (superseded)

Rows marked ¹ were wrong because of our bug (see footnote above).

| listed as | address | verdict | realized SOL | coins | recheck 2026-09-28 (evening) |
|---|---|---|---|---|---|
| LJC | `6HJetMbdHBuk3mLUainxAPpBpWzDgYbHGTS2TqDAUSX2` | INSUFFICIENT | 0.0 | 2 | same |
| Ansem-label | `AVAZvHLR2PcWpDf8BXY4rVxNHYRBytycHkcB5z5QNXYm` | INSUFFICIENT | −42.5 | 3 | same |
| OGAntD | `215nhcAHjQQGgwpQSJQ7zR26etbjjtVdW74NLzwEgQjP` | INSUFFICIENT | 15.1 | 3 | same |
| ¹ SKX | `C4eZg1rJX6v1u7LzqermPrA1pDNNxQe6g3vyY5cHHoWq` | UNVERIFIABLE | 0.0 | 1 | same |
| Cooker | `8deJ9xeUvXSJwicYptA9mHsU2rN2pDx37KWzkDkEXhU6` | **TRUSTED** | 6.2 | 10 | same — only pass |
| ¹ ozark | `DZAa55HwXgv5hStwaTEJGXZz1DhHejvpb7Yr762urXam` | UNKNOWN (RPC timeout) | — | — | UNVERIFIABLE, 1 coin |
| ¹ rayan | `BNahnx13rLru9zxuWNGBD7vVv1pGQXB11Q7qeTyupdWf` | UNVERIFIABLE | 0.0 | 1 | same |
| trunoest | `ardinRsN1mNYVeoJWTBsWeYeXvuR9UUDGMsCDKpb6AT` | UNKNOWN (RPC timeout) | — | — | UNKNOWN (COMPUTE_TIMEOUT) |

## What the verdicts mean

- **TRUSTED** — enough realized trades in the window, net realized SOL clearly positive.
- **INSUFFICIENT** — too few closed coins in the window (< 4) to call it either way.
  A −42.5 SOL or +15.1 SOL figure on 3 coins is not a track record.
- **UNVERIFIABLE** — the numbers could not be reconstructed reliably; we refuse to guess.
- **UNKNOWN** — we could not compute (e.g. RPC throttle / timeout). Not billed.

UNKNOWN / UNVERIFIABLE / INSUFFICIENT are correct refusals, not bugs. A leaderboard
never says "I don't know". We do.

## Older internal sample (Ältere interne Stichprobe) — 2026-07-29

Internal coverage run, 30 wallets from our own local "smart money" list (Birdeye-style
scores / PnL labels), analysis window = most recent trades, RPC: Alchemy.
Result: 15 UNTRUSTED · 6 INSUFFICIENT · 4 TRUSTED · 3 NEUTRAL · 2 UNVERIFIABLE.
Older methodology and a different list — not comparable 1:1 with the table above,
not re-checked since. Kept for transparency only; do not quote it as current.

| address | verdict | realized SOL | coins |
|---|---|---|---|
| `6UwqihqyVb6pYZXZnpGwEF7a4etyR4ijpYjR7RJwn77b` | INSUFFICIENT | 0.0 | 3 |
| `J2rp1Gp2RD12YGzcfT2WgN3tYKvNhqJfExHueFZWLjfR` | TRUSTED | 103.6 | 4 |
| `2wGVz1kg3NoqWR2MAxMG2Wa5xfXb683fYknFz3qvrLcT` | UNTRUSTED | -5.4 | 20 |
| `4h3DTNWbpWVgREkEpsGWo8ya3nvR4JUxXTaQxVSgaQo6` | UNTRUSTED | -21.3 | 8 |
| `5kj4Xd4WjmPMa3zSjoM8iFbbAEgBYukQyWx71eEXgM56` | UNTRUSTED | -0.3 | 38 |
| `uDmSk1vewBHu3Ua15yJpuCMXJELVMzQ688khxfonEBu` | UNTRUSTED | -20.1 | 52 |
| `CHz3ESwSJZHSn9t4zJTfo9KD94rRUwST67UwDXR6phPZ` | UNTRUSTED | -4.7 | 54 |
| `BtZ5iEdFpUDK7hkEikWDVJfS7dMHNs2mMFbYnxa8XDzk` | NEUTRAL | 2.1 | 4 |
| `2Z4ZEZ49TdfH9ZUpgnfRUrbVVCVEV6kjQm8xjuNTTcvv` | UNTRUSTED | -1.1 | 53 |
| `F7cHoDfm1FeyLyaj9CMt7MqbkdtDNY9UzraWV8FgY8p5` | UNTRUSTED | -1.1 | 7 |
| `G4aVNGdBCXk8WvEqaKu1Zr2AHDstKAqBzgnfAcoRHhMS` | UNTRUSTED | -4.2 | 31 |
| `3AtvUZH8R9XUXRJ57dEGrPni6vFTpyB2dkigtomh1byB` | UNTRUSTED | -2.8 | 18 |
| `3pf7BV6stXQMdEuMteeHWiGPagCPxzHwj5fL7asELPWt` | UNTRUSTED | -15.1 | 15 |
| `7ruet2dg9zQfvcwQ7WB4CqVco5dvWY9CMdSvMY7FnZxL` | UNTRUSTED | -2.4 | 19 |
| `FxT2AkeoHLGXDv9kkGXv2bRo2q64FYdh93tFYqDZKjgF` | UNTRUSTED | -0.2 | 15 |
| `7F45aebyi439uQ8JG9TKiNGDyeYMoK4v3o6ee5NecEGt` | UNTRUSTED | -2.8 | 8 |
| `HcLMmNx9pcSM2cDuNMEcWKuDpiknGEb8djqGRsTtM9yo` | NEUTRAL | 0.8 | 97 |
| `AoGefnxF5CbZvbd2cvxv4Ex1E5j86dqEjehazRuMcMFe` | UNVERIFIABLE | 0.9 | 12 |
| `FxNLACMwGK3AAprfWsDnASJpFDCKNDtbbUukNbAC7xjN` | INSUFFICIENT | None | None |
| `ErBupgi9tyf8mYC4aykCAex9UhMHMGZoEFSciLJitG8F` | NEUTRAL | 0.0 | 7 |
| `ApQuAXYpNHLY6Bzn4c8kYdk4qmRyi2kubXXJ4RfYX86X` | INSUFFICIENT | -20.9 | 3 |
| `7oQm7N6FxTVWBBqzCN1giERdii7MPobWdDZ1zjQHxLjo` | TRUSTED | 212.8 | 26 |
| `Auzd43v4ep4QBMsNJPejfTq5k9nmCLhdfk7it8Xtxp6y` | INSUFFICIENT | -0.1 | 2 |
| `6e15xQYRUaLbtv5298senVwHVScGu5t1N1pqC1eVYL9A` | TRUSTED | 151.5 | 21 |
| `4q4GKBpVmXGhXYNaR4DetQjf5WjHEHhbJ9Wgybt7F8Yu` | INSUFFICIENT | None | None |
| `5RQ1UWATaMjjXC34BW6UusEUdEoCuNRECBW8nnHPiCGH` | UNTRUSTED | -1.7 | 33 |
| `Ep8r1jHZp7kojrPRbjE1TpKwBasLhdZPky9PP8HuGieT` | UNTRUSTED | -2.2 | 12 |
| `5thuyFmmroBiqvM68LY5qBDEP9McDdJgVgK8JP787gUH` | UNVERIFIABLE | -4.0 | 8 |
| `21FY9ZhWvaiAjHthh7e63JpRaQc8YVrJS8VBALeJd5Se` | INSUFFICIENT | 11.6 | 3 |
| `2p13nL2K4SYo1ZdQk38YuqjdA8tXndFZpaWkiCrrsVQi` | TRUSTED | 220.2 | 10 |

## Check it yourself

- `GET https://api.pnllabs.com/check/wallet/{address}`
- MCP: `https://api.pnllabs.com/mcp` → tool `check_wallet_trust`
- Rule for agents: [SKILL.md](https://pnllabs.com/SKILL.md) — no verdict, no trade.

Window, not lifetime: the check reads a wallet's most recent trades (up to 100
signatures). Results can change as the wallet keeps trading.
