---
name: l10n-record
domain: software-engineering/l10n-record
trigger: "Writing the record of locale support and its known gaps."
anti_trigger: "Not for translation quality judgement, and not for accessibility."
scope: "The written record: locales supported, coverage, and known gaps."
status: seedling
---

# Localisation record

## Standard

The localisation record states which locales are supported, at what coverage, reviewed by whom, and with which known gaps. Its purpose is to prevent the two common misrepresentations: a locale listed as supported because a file exists, and a product described as localised because the strings were translated.

The gaps section is where the record earns its place. A locale may have complete strings and an unmirrored layout, formatted dates and no localised collation, or a reviewed translation and an unreviewed legal notice. Naming those gaps per locale converts a marketing claim into a statement someone can check.

Primary sources: <https://cldr.unicode.org/> and <https://osf.io/prereg/>.

## Decision rules

- The record lists each locale with its coverage percentage and its review status.
- The CLDR and library versions used are recorded, since the rules depend on them.
- Known gaps are listed per locale by category: strings, layout, formatting, collation, content.
- The fallback locale and its behaviour are recorded.
- The release gate policy for each locale is recorded.
- Review triggers are dated: source change, CLDR release, new locale, review cycle.

## Procedure

1. List locales with coverage and review status.
2. Record the CLDR and library versions.
3. Record gaps per locale by category.
4. Record the fallback locale and behaviour.
5. Record the release gate per locale.
6. Review at each trigger and re-record.

## Anti-patterns

- Listing a locale as supported because a translation file exists.
- Recording coverage without the review status.
- Omitting the library version, which changes the rules.
- Describing gaps in aggregate rather than per locale.
- No review trigger, so the record describes a state that has passed.

## Done checklist

- [ ] Locales with coverage and review recorded.
- [ ] CLDR and library versions recorded.
- [ ] Gaps recorded per locale and category.
- [ ] Fallback behaviour recorded.
- [ ] Release gate recorded.
- [ ] Triggers dated.

The record's most useful function is to prevent a claim outrunning the evidence: a product page that lists a language as supported, and an internal record that shows the layout was never mirrored for it, is a disagreement that only the record can settle, and it settles it before a customer discovers it.


The record should also name the person accountable for each locale, because a gap without an owner is a gap that persists: a locale with complete strings, no reviewer, and an unnamed owner is not a supported locale, it is a translation file that happens to exist.

## Sources

- Unicode CLDR releases and data: <https://cldr.unicode.org/>
- Pre-registration practice for stated conditions: <https://osf.io/prereg/>
- W3C internationalisation guidance: <https://www.w3.org/International/>
