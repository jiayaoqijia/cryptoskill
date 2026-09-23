# Order Forms Must Preserve User Input Across Toggles

A TP/SL sign or percent toggle transforms the existing value, and the submitted order params equal what the form displays.

- **TP/SL sign or percent toggle drops value** — toggles should transform existing state, not reset it unexpectedly.
- **Displayed value differs from submit params** — submitted order must match what user sees.
