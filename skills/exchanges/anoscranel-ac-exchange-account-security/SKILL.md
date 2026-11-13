---
name: ac-exchange-account-security
description: "Securing a trading account at an exchange or broker: API key scopes and IP allowlists, withdrawal controls and whitelists, authentication and second factors, phishing and social engineering, the first hour of a compromise response, custody of secrets, and the written account-security record. It hardens access to capital; it never recommends a venue and never handles a key value. Use when asking \"exchange API key permissions\", \"withdrawal whitelist\", \"two-factor\", \"my exchange account was hacked\", \"is this email from the exchange\", \"secure my trading account\". Not for software security review (ac-security-engineer), not for venue due diligence (ac-perp-venue-diligence), not for operational incident procedure on the book (ac-trading-operations-runbook)."
license: MIT
metadata:
  domain: crypto-trading
status: seedling
---

# Exchange account security

## Overview

A trading account is a door to capital, and the door has several locks: credentials, a second factor, API keys with scopes, withdrawal controls, and the venue's own procedures. Most account losses do not defeat cryptography; they walk through a door that was left open — a key with withdrawal permission, a whitelist never configured, a support message that was not from support.

This skill hardens the access path. It does not evaluate whether a venue is safe to use, and it does not handle secret values: where a key must exist, the record names it and where it is stored, never what it is. The work is procedural and it is mostly done once, in advance, which is why it belongs in writing.

Primary sources: <https://www.cisa.gov/> and <https://www.sec.gov/investor>.

## When to use

- When opening a trading account or issuing a new API key.
- When reviewing existing keys, whitelists, and second factors.
- When an unexpected login, withdrawal, or message raises a compromise question.
- When handing account access to a person or an automated system.

## When NOT to use

- For application security review of trading software (use ac-security-engineer).
- For assessing a venue's solvency, book, or backstop (use ac-perp-venue-diligence).
- For reconciling the book during an outage (use ac-trading-operations-runbook).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/key-and-permission-hygiene.md` | `crypto-trading/key-and-permission-hygiene` | Scopes, withdrawal permissions, IP allowlists, and rotation for API keys. |
| `subskills/withdrawal-controls.md` | `crypto-trading/withdrawal-controls` | Whitelists, delays, sub-accounts, and the difference between reading and moving funds. |
| `subskills/authentication-and-2fa.md` | `crypto-trading/authentication-and-2fa` | Second factors, hardware keys, session and device control, and the weakest link in each. |
| `subskills/phishing-and-social-engineering.md` | `crypto-trading/phishing-and-social-engineering` | Lookalike domains, fake support, migration messages, and the verification habit. |
| `subskills/compromise-response.md` | `crypto-trading/compromise-response` | The first hour: revoke, freeze, change, preserve evidence, and notify. |
| `subskills/custody-of-secrets.md` | `crypto-trading/custody-of-secrets` | Where keys and recovery codes live, backups, and sharing access without exposing values. |
| `subskills/account-security-record.md` | `crypto-trading/account-security-record` | The written record: accounts, key inventory, controls in place, and review triggers. |

## Status and honest limits

Venue security features change, and a control that exists today may be removed or renamed; the record therefore carries a date and a review trigger rather than a permanent assumption. No control set makes an account immune to a determined attacker with a valid session, which is why the response procedure matters as much as the prevention. Nothing here is a guarantee, and a compromise involving material funds belongs with the venue's security team and, where relevant, law enforcement.
