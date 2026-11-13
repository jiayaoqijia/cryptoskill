---
name: ac-i18n-and-localisation
description: "Making software correct in more than one language and locale: externalising strings and the text expansion they cause, plural and gender rules through CLDR, right-to-left layout and mirrored icons, collation and search across scripts, dates time zones and calendars, number and currency formatting, and the localisation workflow that keeps translations from drifting. Use when asking \"i18n\", \"L10n\", \"plural rules\", \"right to left\", \"RTL\", \"text expansion\", \"collation\", \"locale formatting\", \"translation workflow\", \"why does this date look wrong in German\". Not for accessibility and WCAG conformance (ac-frontend-ui), not for brand voice and terminology (ac-brand-guidelines), not for document translation as an editorial task (ac-editing)."
license: MIT
metadata:
  domain: software-engineering
status: seedling
---

# Internationalisation and localisation

## Overview

Internationalisation is the engineering work that makes localisation possible: strings externalised, layouts that tolerate length changes, formats driven by locale rather than hard-coded, and logic that does not assume a language's grammar. Localisation is the translation and adaptation that follows. Confusing the two produces the classic failure where a translated product still shows American dates, breaks on a longer word, and pluralises incorrectly.

This skill covers the parts that are engineering rather than editorial: string externalisation and expansion, plural and gender rules, right-to-left support, collation across scripts, the formatting of dates, times, numbers, and currency, and the workflow that keeps a translation in step with the source. Accessibility and brand terminology belong to other skills.

Primary sources: <https://cldr.unicode.org/> and <https://www.w3.org/International/>.

## When to use

- When externalising strings or preparing a product for a new locale.
- When plural, gender, or grammatical case changes the message.
- When a layout must support right-to-left text.
- When sorting, searching, or formatting depends on locale.

## When NOT to use

- For accessibility and WCAG conformance (use ac-frontend-ui).
- For terminology and voice consistency (use ac-brand-guidelines).
- For translating documents as an editorial task (use ac-editing).

## Subskill Index

| Leaf | Domain segment | Scope (one line) |
|---|---|---|
| `subskills/string-externalisation.md` | `software-engineering/string-externalisation` | Resource files, keys, context, and the text expansion they must survive. |
| `subskills/plurals-and-gender.md` | `software-engineering/plurals-and-gender` | CLDR plural categories, gender, and grammar that changes the sentence. |
| `subskills/rtl-and-bidi.md` | `software-engineering/rtl-and-bidi` | Direction, mirrored layout, and bidirectional text in mixed content. |
| `subskills/collation-and-search.md` | `software-engineering/collation-and-search` | Sorting, case folding, and search across scripts and diacritics. |
| `subskills/locale-formatting.md` | `software-engineering/locale-formatting` | Dates, times, time zones, calendars, numbers, and currency. |
| `subskills/localisation-workflow.md` | `software-engineering/localisation-workflow` | Key stability, translation memory, review, and keeping pace with source. |
| `subskills/l10n-record.md` | `software-engineering/l10n-record` | The written record: locales supported, coverage, and known gaps. |

## Status and honest limits

Locale data changes with each CLDR release, and a rule that is correct today can be refined next year; the library version is part of the behaviour. Translation quality cannot be assessed by an engineer who does not read the language, so the record states coverage and reviewer rather than claiming correctness. Nothing here makes a product localised, and a string table with a hundred percent coverage can still be wrong in every plural form.
