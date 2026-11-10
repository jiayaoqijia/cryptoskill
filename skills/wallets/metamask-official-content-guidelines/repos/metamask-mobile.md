---
repo: metamask-mobile
parent: content-guidelines
---

# MetaMask Content Design Guidelines — Mobile

Shared rules are in the content-guidelines skill. This overlay is MetaMask Mobile only: where strings live, and drafts that apply to this client. If the two seem to disagree, follow the shared skill.

## Where strings live

- English source: `locales/languages/en.json`. Feature-first nested keys (`perps.order.validation.please_set_a_limit_price`).
- UI reads them with `strings(name, params)` from `locales/i18n.js`. Placeholders are `{{name}}` only.
- Edit the English source. Do not hand-edit the other files in `locales/languages/` to keep them in sync. Translation owns those files.
- Judge the string a person sees, not the key. `transaction.gas_fee`, `swaps.gas_fee`, and `activity_details.gas_token_fee` already display "Network fee".

The generated skill under `.claude/skills/mms-content-guidelines/`, `.cursor/rules/mms-content-guidelines/`, and `.agents/skills/mms-content-guidelines/` is overwritten on the next sync. Change this overlay or the shared skill, then sync.

On mobile, do not say "clicking" in a consent line. "Tap to…" is allowed in this client. It is not allowed in the extension. Say tap, not click. The Apple Pay side button stays "double-click" (`card.apple_pay_confirmation.instructions`). Drop "Simply". Keep "double-click" only because that is the platform's name for that control.

## Predictions labels

Market-type and group labels we write are sentence case. Keep team names and league names as proper nouns.

```
❌ "Exact Score" (`predict.sports_market_types.exact_score`)
✅ "Exact score"

❌ "1st Half Team Totals" (`predict.sports_market_types.soccer_first_half_team_totals`)
✅ "1st half team totals"

❌ "Both Teams Slay Baron Nashor"
✅ "Both teams slay Baron Nashor"
```

Those labels are our strings: `predict.sports_market_types.*`, `predict.outcome_groups.*`, and `predict.market_groups.*` in `locales/languages/en.json`.

The question on a market card is not one of those strings. `PolymarketProvider` copies Polymarket's `question`, `groupItemTitle`, and event `title`, with light formatting only. Do not sentence-case that feed text. Team and league names inside it stay as the feed sent them.

Developer-only strings (`app_settings.developer_options.*`, debug screens) are out of scope. The shared skill states that rule.

## PROPOSED

Drafts. Do not enforce them until content design confirms them.

1. **Locale file.** If a person can read it, it belongs in `locales/languages/en.json`. That includes accessibility labels and empty states. Hardcoded examples to move when you touch them: "Date of Birth" in `app/components/UI/Card/components/Onboarding/PersonalDetails.tsx`, "Games couldn't be loaded." / "No games available." / "Retry" in `FeedPreviewSection.tsx`, and "Unable to load price history" in `PredictGameChartContent.tsx`.
2. **Do not run `toSentenceCase` on product copy.** `app/util/string/index.ts` lowercases everything after the first character. Bridge quote UI calls it on `bridge.network_fee`. It will also lowercase "NFT" and "Secret Recovery Phrase".
