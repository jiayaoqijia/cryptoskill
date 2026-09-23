# Hook Import Boundaries

Shared perps hooks are imported from their module file, not the `hooks/perps` barrel, stream-module mocks list every hook a component uses, and no hook mutates a caller's ref.

- **Import shared hooks from their module, not the `hooks/perps` barrel** — components rendered by many hosts must import shared hooks (e.g. `usePerpsEventTracking`) directly from their module file, not from the `hooks/perps` barrel. Several test suites partially mock the barrel, so a barrel import surfaces as `usePerpsEventTracking is not a function` at render in unrelated tests.
- **Stream-module mocks are explicit whitelists** — when a covered component imports another stream hook, update the test's stream-module mock object too. A missing hook otherwise fails behind the React Router error boundary as an unrelated `is not a function` render error.
- **`react-compiler` forbids mutating a hook argument** — a hook cannot reset a caller's `hasCommittedRef`. The reset belongs in the caller's own open/reset effect. Mobile's version does mutate the ref — do not copy that part.
