# The Dev Level

The dev level is a permanent sandbox scene/route used to test each game
system in isolation, immediately after it's built. It is created in Phase 3
and never deleted — it stays in the repo for the life of the project as the
QA harness, and gets a new entry point added every time a new system is
built.

## Why it exists

Testing a system inside the real game (through menus, level load order,
whatever state the game needs to reach it) is slow and couples the test to
systems that haven't been built yet. The dev level removes that coupling:
each system gets its own minimal, directly-reachable scene that exercises
just that system with nothing else in the way.

## Structure

- One dedicated route/scene per system, addressable directly — e.g. a URL
  query param (`?dev=movement`, `?dev=collision`) or a dedicated dev-only
  scene per system if the engine's scene system makes that more natural
  (Phaser: a `DevMovementScene`, `DevCollisionScene`, etc., started
  directly instead of going through the game's normal boot sequence).
- A simple in-page menu/index (e.g. at `?dev` or `/dev`) listing every
  system with a link/button to jump straight into its isolated test scene.
  This is what you navigate to first in the testing protocol.
- Each system's dev scene should:
  - Set up only the minimal world state that system needs (e.g. movement
    test: a floor and a controllable character, nothing else).
  - Expose whatever the system needs to be exercised by real input (see
    `references/testing-protocol.md`) — actual keyboard/touch handling
    wired up, not a mocked/stubbed version of the system.
  - Show an on-screen debug readout relevant to the system where useful
    (position/velocity for movement, collision-pair state for collision,
    current bullet count for a shooter's fire system, etc.) — this is what
    a screenshot needs to capture to actually prove the system worked,
    beyond just "something moved."
- Keep dev scenes cheap to add: a new system should mean adding one new
  dev-scene file/route and one line in the dev-level index, not a
  refactor.

## Growing it over time

As systems accumulate, later dev scenes may combine a couple of systems
that only make sense tested together (e.g. collision + camera-follow) —
that's fine, note in `SYSTEMS.md` which systems a given dev scene actually
covers. The dev level doesn't need to mirror the final game 1:1; its only
job is making each system observably testable on its own.

## After Phase 6

Once assembly is underway, keep the dev level around rather than deleting
it — it's the fastest way to re-verify a system in isolation if a
regression shows up later, and costs nothing to leave in a dev-only build.
