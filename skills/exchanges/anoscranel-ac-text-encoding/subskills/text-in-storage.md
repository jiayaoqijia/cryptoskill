---
name: text-in-storage
domain: software-engineering/text-in-storage
trigger: "Storing text in databases and files without silent corruption."
anti_trigger: "Not for input validation rules (that is utf8-and-malformed-input)."
scope: "Column encodings, collation interactions, and lengths that lie."
status: seedling
---

# Text in storage

## Standard

A database column has a character set and a collation, and both are decisions that outlive the code that made them. The character set decides what can be stored: a legacy set silently transforms or rejects characters outside its range. The collation decides what compares equal: one that ignores accents makes two different strings match, one that is byte-ordered makes two visually equal strings differ when their normalisation differs.

The other lying number is length. A column declared with a character limit counts characters — but which unit, and per the column's own rules, varies by engine and version — while the wire and the application may count bytes or graphemes. A validation in the application that permits what the column rejects produces an insert error nobody tested for, and one that is stricter wastes space; the two must be derived from one definition.

## Decision rules

- Record the character set and collation of every text-bearing store, explicitly.
- Prefer a Unicode character set for all new stores; treat legacy sets as edge conversions.
- Know each collation's equality rule: case, accent, and trailing-space handling.
- Derive the application's length limit from the column's definition and unit.
- Test stores with characters outside ASCII: combining accents, emoji, right-to-left scripts.
- Check file stores too: declared encodings in headers versus reality.

## Procedure

1. Inventory text columns and their declared character sets and collations.
2. Verify each collation's equality rule against the system's comparison needs.
3. Align application length limits with the column unit.
4. Insert the non-ASCII test set and observe what stores and what transforms.
5. Audit any legacy-set columns for silent transformation history.
6. Record the inventory and decisions in the text policy.

## Anti-patterns

- Trusting the default collation because rows went in without error.
- A length validation in the application counting a different unit than the column.
- Storing into a legacy character set and discovering the transformations later.
- Migrating stores without recording the source encoding of the old data.
- Testing inserts with ASCII only.

## Done checklist

- [ ] Character sets and collations inventoried.
- [ ] Collation equality rules verified.
- [ ] Length units aligned with the column.
- [ ] Non-ASCII insert tests pass untransformed.
- [ ] Legacy columns audited.
- [ ] Policy records the store decisions.

## Sources

- Unicode collation algorithm overview: <https://www.unicode.org/reports/tr10/>
- The Unicode Standard: <https://www.unicode.org/versions/latest/>
- SQL standard text handling: <https://www.iso.org/standard.html>
