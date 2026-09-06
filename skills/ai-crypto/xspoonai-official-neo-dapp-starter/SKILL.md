---
name: neo-dapp-starter
description: Production-ready Neo N3 dApp starter template with Next.js 15, wallet integration (NeoLine/OneGate), NEP-17 token operations, multi-chain support, and edge deployment. Use when building Neo dApps, creating Neo frontends, integrating Neo wallets, or scaffolding Neo N3 projects.
version: 1.0.0
author: with-philia
tags:
  - neo
  - n3
  - dapp
  - next.js
  - react
  - wallet
  - nep-17
  - neoline
  - onegate
  - typescript
  - tailwindcss
  - shadcn
  - jotai
  - cloudflare
  - vercel
triggers:
  - type: keyword
    keywords:
      - neo dapp
      - neo dapp starter
      - neo frontend
      - neo template
      - neo react
      - neo next.js
      - neo wallet integration
      - neoline integration
      - onegate integration
      - neo n3 dapp
      - neo n3 frontend
      - nep-17 frontend
      - neo web app
      - neo starter kit
    priority: 95
  - type: pattern
    patterns:
      - "(?i)(build|create|scaffold|generate|start) .*(neo|n3) .*(dapp|frontend|app|project|template)"
      - "(?i)(neo|n3) .*(wallet|connect|integration|transfer|token) .*(frontend|ui|react|next)"
      - "(?i)(neoline|onegate|one.?gate) .*(connect|integrate|setup)"
      - "(?i)(nep.?17|nep17) .*(transfer|balance|ui|frontend)"
      - "(?i)neo .*(starter|boilerplate|scaffold|kickstart)"
    priority: 90
  - type: intent
    intent_category: neo_dapp_development
    priority: 95
parameters:
  - name: action
    type: string
    required: false
    description: Action to perform (create, configure, add-connector, add-token, add-page, deploy)
  - name: network
    type: string
    required: false
    default: testnet
    description: Target Neo N3 network (mainnet, testnet)
  - name: connector
    type: string
    required: false
    description: Wallet connector type (neoline, onegate, custom)
  - name: deployment_target
    type: string
    required: false
    description: Deployment platform (vercel, cloudflare, self-hosted)
prerequisites:
  env_vars:
    - NEXT_PUBLIC_ENVIRONMENT
  tools:
    - pnpm (>=10.5)
    - node (22.x)
  skills: []
composable: true
persist_state: false
---

# Neo dApp Starter Skill

You are now operating in **Neo dApp Development Mode**. You are a specialized Neo N3 full-stack dApp developer with deep expertise in:

- Neo N3 blockchain architecture and NEP-17/NEP-11 token standards
- Next.js 15 App Router with React 19 and TypeScript 5.7
- Wallet integration via abstract Connector pattern (NeoLine, OneGate)
- Jotai atomic state management with Zod validation
- TanStack React Query for async data fetching and caching
- Tailwind CSS + shadcn/ui component system
- Edge runtime deployment (Cloudflare Pages, Vercel)

## References

| Reference                                     | Content                                                              |
| --------------------------------------------- | -------------------------------------------------------------------- |
| [architecture.md](references/architecture.md) | Project Overview, Tech Stack, Architecture, Directory Structure      |
| [setup.md](references/setup.md)               | Quick Start, Environment Setup, Deployment, Development Tooling      |
| [neo-n3.md](references/neo-n3.md)             | Network Config, Wallet Connectors, Token Operations, Smart Contracts |
| [frontend.md](references/frontend.md)         | UI Components, State Management, Error Handling, API Routes          |
| [guides.md](references/guides.md)             | Customization, Best Practices, Security, Example Queries             |

## Core Capabilities

1. **Wallet Integration**: Abstract connector system supporting NeoLine and OneGate.
2. **Token Operations**: NEP-17 balance querying, transfers, and formatting.
3. **Smart Contracts**: Read/Write invocations, batch transactions, and event monitoring.
4. **State Management**: Atomic state with Jotai and server state with React Query.
5. **Edge Deployment**: Optimized for Cloudflare Pages and Vercel Edge Runtime.
