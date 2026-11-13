---
name: string-externalisation
domain: software-engineering/string-externalisation
trigger: "Moving strings into resources so they can be translated."
anti_trigger: "Not for translation quality, and not for accessibility labels."
scope: "Resource files, keys, context, and the text expansion they must survive."
status: seedling
---

# String externalisation

## Standard

Externalising a string means moving it out of the code and into a resource identified by a key, so a translator can replace the value without touching the logic. The engineering decisions are the key's stability, the context given to the translator, and the layout's tolerance for a different length — and all three outlive the first translation.

Text expansion is the constraint most often missed. A German or Finnish rendering of a short English label can be twice as long, and a button sized for the original truncates or overflows. The mitigation is layout that can grow, not shorter translations, because the translator cannot shorten what the meaning requires.

Primary sources: <https://cldr.unicode.org/> and <https://www.w3.org/International/>.

## Decision rules

- Record the key naming scheme and require that keys are stable across refactors.
- Record the context supplied to translators: screen, length limit, and part of speech.
- Record the maximum expansion the layout must tolerate, as a percentage.
- Record strings that must not be translated, such as identifiers and brand names.
- Record placeholder syntax and the rule for inserting values, including order.
- Record the fallback locale and what the user sees when a key is missing.

## Procedure

1. Choose a key scheme based on meaning rather than on English text.
2. Extract strings and attach context to each.
3. Record the expansion allowance per layout region.
4. Mark non-translatable strings explicitly.
5. Define placeholder syntax and document its use.
6. Test the fallback path by removing a key.

## Anti-patterns

- Using the English text as the key, so a wording change breaks the reference.
- Sending strings without context, forcing the translator to guess.
- Sizing components for the source language.
- Concatenating fragments to build a sentence.
- Leaving missing-key behaviour to the framework's default.

## Done checklist

- [ ] Key scheme recorded and stable.
- [ ] Context supplied per string.
- [ ] Expansion allowance recorded.
- [ ] Non-translatable strings marked.
- [ ] Placeholder syntax documented.
- [ ] Fallback tested.

The expansion allowance should be recorded per region rather than globally, because a button and a paragraph fail differently: a button truncates and a paragraph wraps, and a single percentage applied to both will either over-size the paragraph or under-size the button. Region-specific allowances make the layout testable.


## Sources

- Unicode locale data and CLDR: <https://cldr.unicode.org/>
- W3C internationalisation guidance: <https://www.w3.org/International/>
- Web content accessibility guidance: <https://www.w3.org/WAI/>
