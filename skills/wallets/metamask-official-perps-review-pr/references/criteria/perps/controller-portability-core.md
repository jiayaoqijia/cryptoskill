# Controller Portability (Core)

`PerpsController` lives in `core/packages/perps-controller` and is published as `@metamask/perps-controller`; mobile and extension both consume the package. Controller code must stay platform-agnostic, and app code must go through the published surface.

- **Platform import in controller** — `react-native`, `Engine`, `Sentry`, `DevLogger`, browser APIs, or extension globals imported in `packages/perps-controller`. All platform services must flow through `PerpsPlatformDependencies` (DI), passed as the `infrastructure` constructor param.
- **Deep import from app code** — app files importing controller internals by path (`@metamask/perps-controller/dist/...`, a relative path into a linked checkout) instead of the package's public exports.
- **`__DEV__` or platform globals in controller code** — must not appear in controller files; the package has no such globals at build time.
- **New dependency not in DI interface** — controller code reaching outside its boundary (e.g., importing a hook, React context, or an app utility). Everything the controller needs must come through `PerpsPlatformDependencies`.
- **Breaking the publisher contract** — changing PerpsController's public API (state shape, method signatures, event names) without considering both consumers. Controller is a publisher — mobile and extension both consume it.
- **Controller bump treated as lockfile-only** — inspect changed controller `dist` call sites against Mobile's hand-written integration mocks, then run the Perps integration suites. Object-literal mocks cast through `jest.Mocked` can hide newly required methods from typecheck.
