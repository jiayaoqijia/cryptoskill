---
name: rtl-and-bidi
domain: software-engineering/rtl-and-bidi
trigger: "Supporting right-to-left languages and bidirectional text."
anti_trigger: "Not for general layout and accessibility, and not for translation."
scope: "Direction, mirrored layout, and bidirectional text in mixed content."
status: seedling
---

# Right-to-left and bidirectional text

## Standard

Right-to-left support is a layout property, not a translation. A language written right to left requires the interface's direction to flip: navigation moves to the right, icons that imply direction are mirrored, and text alignment follows the reading order. Setting the direction attribute without mirroring the layout produces a page that reads correctly and navigates backwards.

Bidirectional text is the harder problem, and it appears in every locale. A username, a file path, a phone number, or a Latin brand name embedded in Arabic text changes the apparent order of the surrounding punctuation, and the result can look reversed without being wrong. The mitigation is isolation of embedded spans rather than manual reordering, which the renderer handles.

Primary sources: <https://www.w3.org/International/> and <https://cldr.unicode.org/>.

## Decision rules

- Record the interface direction and whether it is set at the document or the component level.
- Record which icons and images must be mirrored, and which must not.
- Record the spacing and padding rules that depend on direction.
- Record the isolation applied to embedded text runs that differ in direction from their context.
- Record the handling of numbers and punctuation at run boundaries.
- Record the components that assume left-to-right in their logic rather than their style.

## Procedure

1. Set the direction at the document level and record the mechanism.
2. Inventory icons and mark those that mirror.
3. Convert physical spacing properties to logical ones.
4. Isolate embedded runs whose direction differs from the context.
5. Test with mixed content including numbers and punctuation.
6. Record the components whose logic assumed direction.

## Anti-patterns

- Translating the text into Arabic and leaving the layout unmirrored.
- Mirroring logos and clock icons that carry no direction.
- Using physical left and right properties throughout.
- Reordering a display string in code to force an appearance.
- Assuming numbers inherit the surrounding direction.

## Done checklist

- [ ] Document direction mechanism recorded.
- [ ] Mirroring inventory recorded.
- [ ] Logical spacing properties recorded.
- [ ] Isolation for embedded runs recorded.
- [ ] Boundary punctuation tested.
- [ ] Direction-assuming components recorded.

The isolation point applies beyond translation: any user-generated content embedded in a fixed-direction interface can change the apparent order of adjacent punctuation, so isolation belongs on the display of names, paths, and identifiers rather than only on localised strings.


## Sources

- W3C internationalisation and bidi guidance: <https://www.w3.org/International/>
- Unicode bidirectional algorithm: <https://www.unicode.org/reports/>
- Accessibility guidance on direction: <https://www.w3.org/WAI/>
