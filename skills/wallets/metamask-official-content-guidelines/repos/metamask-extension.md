---
repo: metamask-extension
parent: content-guidelines
---

# MetaMask Content Design Guidelines — Extension

Shared rules are in the content-guidelines skill. This overlay is the MetaMask browser extension only: where strings live, and drafts that apply to this client. If the two seem to disagree, follow the shared skill.

## Where strings live

- English source: `app/_locales/en/messages.json`. Flat Chrome i18n entries: `{ "key": { "message": "...", "description"?: "..." } }`.
- UI reads them with `t()`. Placeholders are `$1`, `$2`, and so on.
- Edit the English source only. Crowdin uses that file. Do not hand-edit other folders under `app/_locales/`, including `en_GB` (it matches `en` and is not a second style).
- Almost all product copy is in the locale file. A thrown `Error` message can still surface if a caller shows `error.message`. Write that message to the same rules, or do not show it raw.

The generated skill under `.claude/skills/mms-content-guidelines/`, `.cursor/rules/mms-content-guidelines/`, and `.agents/skills/mms-content-guidelines/` is overwritten on the next sync. Change this overlay or the shared skill, then sync.

"Click here" is banned. Name the control ("Connect your Ledger", not `clickToConnectLedgerViaWebHID`). Do not write "Tap to…". That phrase is mobile only. On mobile the rule is tap, not click.

Signature requests, transactions, and final review use Confirm. Do not label that button Sign. `QRHardwareSignRequestCancel` is "Reject". Do not copy it onto new screens. Do not replace that existing "Reject" until the shared skill's Cancel check is done.

Activity descriptions add the amount, the counterparty, or the reason. Do not copy the title ("Buy failed" / "Buy failed"). Do not leave the description empty (`activity_swap_failed_description` and the other empty `activity_*_failed_description` keys).

Developer-only strings (debug tabs, developer confirmation buttons) are out of scope. The shared skill states that rule.

## PROPOSED

A draft. Do not enforce it until content design confirms it.

1. **Translator descriptions.** Add a `description` on every new key so the term survives translation. Security, fee, wallet, and account strings need one when you touch them. `docs/translating-guide.md` does not require this today.
