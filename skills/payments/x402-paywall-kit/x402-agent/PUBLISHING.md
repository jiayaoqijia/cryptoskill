# Publishing x402-agent to ClawHub

## Prerequisites

1. **ClawHub CLI** installed:
   ```bash
   npm install -g clawhub
   ```

2. **GitHub account** linked to ClawHub (Tara Quinn AI / tara-quinn-ai)

3. **Authenticate** with ClawHub:
   ```bash
   clawhub login
   ```

## Skill Folder Structure

```
x402-agent/
  SKILL.md                          # Skill definition (YAML frontmatter + instructions)
  VERSION                           # Semver version (1.0.0)
  references/
    policy.example.json             # Example policy config
    agent-setup.example.ts          # Complete setup example
```

## Publish

From the repo root:

```bash
cd x402-agent
clawhub publish
```

Or specify the path:

```bash
clawhub publish x402-agent/
```

## Verify

After publishing, check that the skill is live:

1. Visit https://clawhub.ai and search for "x402-agent"
2. Verify the skill page shows:
   - Name: `x402-agent`
   - Description matches SKILL.md frontmatter
   - Version: `1.0.0`
   - Requirements: `X402_WALLET_PRIVATE_KEY` env var, `node` binary
3. Test installation:
   ```bash
   clawhub install x402-agent
   ```

## Updating

To publish a new version:

1. Update `VERSION` with the new semver
2. Update `SKILL.md` frontmatter `version` to match
3. Run `clawhub publish` again

## Notes

- The SKILL.md references `@x402-kit/agent` and `@x402-kit/shared` NPM packages — ensure Task 3.1 (NPM publish) is complete before publishing to ClawHub
- This is the full skill with policy engine, logging, and domain filtering
- Task 3.6 creates a stripped-down free version for broader distribution
