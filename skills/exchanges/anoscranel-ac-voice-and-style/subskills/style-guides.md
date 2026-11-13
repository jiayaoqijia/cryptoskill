---
name: style-guides
domain: writing/style-guides
trigger: "\"which style guide\", \"AP or Chicago\", \"build a style sheet\", \"make it match house style\", \"our house rules\"."
anti_trigger: "Applying the sheet during the consistency pass; inclusive-language term choices inside the sheet."
scope: "Picking AP/CMOS/APA/house guide; building a project style sheet"
status: "seedling"
---

# Style guides & style sheet

## Standard

- **Division of labour is by register, not by rule quality.** AP for news; CMOS for publishing; APA 7 for psychology and social science; MLA 9 for humanities; CSE 8th ed. for scientific nomenclature; the Microsoft Writing Style Guide for product content (<https://owl.purdue.edu/owl/subject_specific_writing/journalism_and_journalistic_writing/ap_style.html>).
- **Current editions.** CMOS 18 released 19 Sep 2024 (https://www.chicagomanualofstyle.org/help-tools/what-s-new.html ⚠️ body text paywalled). Its free "What's New" page records generic singular "they" (5.51, 5.266) and a capital after a colon (6.67). AP Stylebook 58th ed. released 28 May 2026, with an expanded AI chapter (AI agent, AI slop, vibe coding) (https://www.ap.org/media-center/press-releases/2026/new-ap-stylebook-features-expanded-artificial-intelligence-chapter/). It also spells "healthcare" one word and adds a standalone Native Americans / Indigenous peoples entry. APA 7th ed. (2020) carries the bias-free-language chapters (https://apastyle.apa.org/style-grammar-guidelines/bias-free-language).
- **The sheet closes the open field.** "A style guide is a default layer over an open field; the sheet is the closure operation."
CSE states its own limit: recommendations "focus primarily on nomenclature and symbolization", with no comprehensive term lists (https://scientificstyleandformat.org/book/ed8/front/pref.html; <https://scientificstyleandformat.org/book/ed8/front/pref.html>).
- **Every guide governs the frame; only two govern the sentence.** Structure, citation form, capitalisation and labels are covered. Sentence diction is not; no guide targets argument prose.
## Decision rules

1. Venue rules come first. A journal's guide for authors or a publisher's house guide outranks any general guide.
2. Then choose one base guide by register, and record the choice in the sheet header.
3. Then write the project sheet for every decision the base guide leaves open. 10–20 entries is a normal size.
4. The sheet holds decisions, not copies of guide text. Each entry: the ruling, the example, the reason.
5. Record an exception process: who may override, with what note. Most guides publish none.

## Procedure

1. Collect the venue's rules: word limits, structure, citation style, heading style, required sections, legal wording.
2. Choose the base guide by register. Record the edition and date.
3. Draft the sheet:
   ```markdown
   Base guide (name, edition, date):
   Venue overrides (rule, source):
   1. <decision> — rule, do/don't example, reason
   Exceptions (who may override, what note):
   ```
4. Seed entries from real questions met while drafting: hyphenation, capitalisation, number and date formats, serial comma, acronyms, pronoun use, bias-free terms.
5. Apply the sheet in the copyedit pass (out of scope for this leaf: the copyedit procedure) and add every new decision it settles.
6. Review the sheet at each release. Supersede retired entries; never leave two live rulings on one point.

## Anti-patterns

- A sheet that copies the guide and so drifts from it.
- Enforcing unwritten conventions from memory, so each editor enforces a different house.
- Mixing two base guides in one document.
- Using the guide to settle diction — it does not do that.
- An exception process nobody can name.

## Done checklist

- [ ] Venue rules collected and recorded.
- [ ] One base guide chosen, with edition and date.
- [ ] Project sheet written, 10–20 entries, each with example and reason.
- [ ] Exception route recorded with an owner.
- [ ] Sheet applied in copyedit and updated.
- [ ] One live ruling per point; retired entries superseded.

## Sources

- <https://owl.purdue.edu/owl/subject_specific_writing/journalism_and_journalistic_writing/ap_style.html>
- https://www.chicagomanualofstyle.org/help-tools/what-s-new.html
- https://www.ap.org/media-center/press-releases/2026/new-ap-stylebook-features-expanded-artificial-intelligence-chapter/
- https://scientificstyleandformat.org/book/ed8/front/pref.html
