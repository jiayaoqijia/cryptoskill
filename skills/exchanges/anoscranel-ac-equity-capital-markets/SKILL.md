---
name: ac-equity-capital-markets
description: "Reading primary equity issuance from the issuer's and the investor's side: bookbuilding and allocation mechanics, the greenshoe and price stabilisation, lock-up expiry and the supply it releases, follow-on and block trade structures, at-the-market programmes, rights issues and their discount arithmetic, direct listings and SPAC redemption mechanics, and the written issuance record. It explains how primary supply reaches the market; it never recommends a security and never predicts an issue's performance. Use when asking \"IPO\", \"bookbuilding\", \"greenshoe\", \"lock-up expiry\", \"follow-on offering\", \"block trade\", \"at-the-market programme\", \"rights issue discount\", \"SPAC redemption\", \"direct listing\", \"who gets allocated\". Not for secondary market trading of the shares (ac-stock-trading), not for corporate actions adjustment of existing holders (ac-corporate-actions), not for the investment case (ac-equity-research)."
license: MIT
metadata:
  domain: investing
status: seedling
---

# Equity capital markets

## Overview

Primary equity issuance is where new shares are created and sold, and its mechanics explain a great deal of what happens to a share price afterwards. An issue is priced through a process, allocated by a bookrunner, stabilised for a period, and then released from a lock-up that has been holding supply back. Each of those steps is scheduled, and each leaves a footprint in the market.

This skill covers that machinery: how a book is built and allocated, what the greenshoe does and who pays for it, what a lock-up expiry releases, how blocks and follow-ons are priced against the market, how a rights issue's discount and its rump placement work, and how a direct listing or a SPAC differs from a traditional offering. The trading of the shares afterwards belongs to the stock trading skill.

Primary sources: <https://www.sec.gov/investor> and <https://www.finra.org/>.

## When to use

- When an issuer is raising equity and the process mechanics matter.
- When a lock-up expiry or an index-driven supply event is approaching.
- When a block trade or a follow-on prices at a discount to the market.
- When a rights issue, direct listing, or SPAC transaction needs reading.

## When NOT to use

- For trading the shares in the secondary market (use ac-stock-trading).
- For the price adjustment existing holders face (use ac-corporate-actions).
- For the investment case for the company (use ac-equity-research).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/bookbuilding-and-allocation.md` | `investing/bookbuilding-and-allocation` | Building a book, pricing it, and who receives shares. |
| `subskills/greenshoe-and-stabilisation.md` | `investing/greenshoe-and-stabilisation` | The over-allotment option, stabilisation, and the syndicate's short position. |
| `subskills/lockup-expiry-flows.md` | `investing/lockup-expiry-flows` | What a lock-up releases, when, and how the supply is absorbed. |
| `subskills/follow-on-and-blocks.md` | `investing/follow-on-and-blocks` | Priced offerings, bought deals, and the concession a block carries. |
| `subskills/rights-issues.md` | `investing/rights-issues` | Subscription price, discount, renounceability, and the rump placement. |
| `subskills/direct-listings-and-spacs.md` | `investing/direct-listings-and-spacs` | No-bookbuild listings, SPAC redemption, and de-SPAC dilution. |
| `subskills/issuance-record.md` | `investing/issuance-record` | The written record: issue terms, supply calendar, and dilution. |

## Status and honest limits

Issue mechanics are documented in filings and prospectuses, but the allocation process is discretionary and lightly observed, so conclusions about who received shares are inferences rather than facts. Lock-up terms are contractual and can be waived by the bookrunner, which means a dated calendar is a schedule rather than a promise. Nothing here recommends participating in an issue, and a supply event that is known in advance is usually at least partly priced, which is the central difficulty of using it as a trading signal.
