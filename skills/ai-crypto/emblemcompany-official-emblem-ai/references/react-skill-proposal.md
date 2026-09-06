# React Skill Proposal

## Recommendation

If EmblemAI is split beyond the current umbrella developer skill, React should be the first internal cluster to become its own standalone skill.

The right next shape is one React skill, not three separate skills.

## Proposed Skill Shape

### Future skill name

- `emblem-ai-react`

### What it should cover

- React authentication flows via `@emblemvault/emblem-auth-react`
- EmblemAI chat integration via `@emblemvault/hustle-react`
- Component composition patterns for auth plus chat
- Shared React prompt examples and app recipes

### What should stay as references inside that skill

- `auth-react.md`
- `emblem-ai-react.md`
- `react-components.md`
- [../../emblem-ai-prompt-examples/SKILL.md](../../emblem-ai-prompt-examples/SKILL.md) (shared prompt catalog with React-specific recipes)

## Why This Split Makes Sense

React developers are a coherent audience with a strong framework-specific install intent.

This is stronger than splitting by document type:

- one skill for `auth-react`
- one skill for `emblem-ai-react`
- one skill for `react-components`

That three-way split is too granular for marketplace discovery and weakens the install decision.

## What Is Still Missing Before A Standalone React Skill

### Higher-value implementation examples

- Full-page React example with auth plus chat
- Auth-only React example for apps that do not need chat yet
- Shared layout and provider composition examples
- Error/loading state examples
- A recipe-oriented section: dashboard, embedded assistant, analytics console, onboarding flow

### Product framing

- Clear title and description aimed at the query: "Add EmblemAI to a React app"
- Explicit note that legacy package names may still use `hustle` branding
- Separation from backend/SDK-only integration flows

## Suggested Internal Clustering Today

Until that standalone React skill exists, keep the React material grouped as an internal cluster under `emblem-ai`:

- `auth-react.md`
- `emblem-ai-react.md`
- `react-components.md`
- [../../emblem-ai-prompt-examples/SKILL.md](../../emblem-ai-prompt-examples/SKILL.md) (shared prompt catalog with React-specific recipes)

This preserves a clean split between:

- React
- SDK and backend
- Advanced tooling and introspection
