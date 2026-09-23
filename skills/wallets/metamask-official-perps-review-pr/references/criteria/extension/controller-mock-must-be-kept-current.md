# Controller Mock Must Be Kept Current

Every new contract value that product code reads is added to the hand-maintained `test/mocks/metamask-perps-controller.js` in the same PR, otherwise tests silently see `undefined`.

- **New event name / property used in product code but absent from mock** — grep the new symbol in `test/mocks/metamask-perps-controller.js` before merging. If missing, add it.
- **Mock drift goes unnoticed** — tests do not warn when a mock returns `undefined`; they silently fail on downstream assertions. Do not assume the mock is up to date after a controller version bump.
