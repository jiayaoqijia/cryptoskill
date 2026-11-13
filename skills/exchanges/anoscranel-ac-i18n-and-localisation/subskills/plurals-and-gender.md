---
name: plurals-and-gender
domain: software-engineering/plurals-and-gender
trigger: "Handling plural categories and grammatical gender in messages."
anti_trigger: "Not for translation quality, and not for copywriting."
scope: "CLDR plural categories, gender, and grammar that changes the sentence."
status: seedling
---

# Plurals and gender

## Standard

English has two plural forms; other languages have up to six, and the category a number falls into depends on the language rather than on the number. Polish distinguishes one, few, many, and other; Arabic distinguishes zero, one, two, few, many, and other. A message with a single plural branch is therefore wrong in most languages, and the error is invisible to an English speaker.

Gender compounds the problem because it can change the adjective, the past participle, and the pronoun, and the gender is sometimes the user's rather than the object's. The robust approach is a message format that carries the plural and gender variables as first-class inputs and lets the locale's rules select the form, rather than concatenating pre-translated fragments in code.

Primary sources: <https://cldr.unicode.org/> and <https://www.w3.org/International/>.

## Decision rules

- Record every message that includes a count and mark it for plural handling.
- Record the plural categories the target locales require, taken from CLDR rather than assumed.
- Record gender variables and whose gender they represent.
- Record whether the message needs an ordinal rather than a cardinal form.
- Record the message format library and its CLDR version.
- Record sentences that change structure, not only word endings.

## Procedure

1. Identify messages with counts and mark them.
2. Look up the plural categories for each target locale.
3. Record gender variables and their referents.
4. Encode both in a message format rather than in string concatenation.
5. Record the CLDR version the library uses.
6. Test with counts that fall into each category, including zero.

## Anti-patterns

- Adding a second branch for singular and plural and calling it done.
- Concatenating a number with a unit string in code.
- Assuming gender is binary or matches the user's profile.
- Using cardinal forms where ordinals are meant.
- Trusting the library without recording its CLDR version.

## Done checklist

- [ ] Count-bearing messages identified.
- [ ] Required plural categories recorded per locale.
- [ ] Gender variables recorded with referent.
- [ ] Ordinal cases marked.
- [ ] Library and CLDR version recorded.
- [ ] Each category tested.

The test that catches most plural defects is the zero case, because English treats zero as plural and several languages treat it as a distinct category: a message that reads correctly at one and at two can still be wrong at zero, and the error appears only for a user with an empty list rather than for the developer.


## Sources

- Unicode CLDR plural rules: <https://cldr.unicode.org/>
- W3C language and locale guidance: <https://www.w3.org/International/>
- Localisation industry standards: <https://www.gala-global.org/>
