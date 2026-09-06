---
name: deploy-on-vercel
description: Deploy applications and websites to Vercel instantly without authentication. Use when the user wants to "deploy my app", "push this live", or "create a preview link". Returns a live preview URL and a claimable link.
version: 1.0.0
author: with-philia
license: MIT
tags: [Vercel, Deployment, Cloud, Hosting, Instant]
dependencies: [curl, tar]
allowed-tools: Bash(scripts/deploy.sh)
---

# Vercel Instant Deploy

Deploy any web project to Vercel instantly. No authentication or API keys required.

## How It Works

1.  **Package**: Compresses your project into a tarball (excluding `node_modules` and `.git`).
2.  **Detect**: Automatically identifies the framework (Next.js, Vue, Svelte, etc.) from `package.json`.
3.  **Upload**: Sends the package to the Vercel Instant Deploy service.
4.  **Result**: Returns a **Preview URL** (live site) and a **Claim URL** (to transfer ownership to your Vercel account).

## Usage

```bash
bash scripts/deploy.sh [path]
```

**Arguments:**

- `path`: Directory to deploy (defaults to current directory `.`).

**Examples:**

```bash
# Deploy current directory
bash scripts/deploy.sh

# Deploy specific project
bash scripts/deploy.sh ./my-app
```

## Output

The script outputs progress logs to stderr and the final JSON result to stdout.

```
Preparing deployment...
Detected framework: nextjs
Creating deployment package...
Deploying...
✓ Deployment successful!

Preview URL: https://skill-deploy-abc123.vercel.app
Claim URL:   https://vercel.com/claim-deployment?code=...
```

## Supported Frameworks

Auto-detection supports 30+ frameworks including:

- **React**: Next.js, Remix, Gatsby, Create React App
- **Vue**: Nuxt, VitePress, VuePress
- **Svelte**: SvelteKit, Svelte
- **Others**: Astro, SolidStart, Angular, Express, NestJS, Hono

_Static HTML projects are also supported._

## Troubleshooting

### Network Issues

If deployment fails due to network restrictions (e.g., in restricted environments), ensure `*.vercel.com` is allowed.

### Build Failures

If the deployed site shows a build error, check the logs in the Preview URL. Common issues include missing dependencies or incorrect build scripts in `package.json`.
