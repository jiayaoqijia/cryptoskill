# 🦞 OpenClaw Nostr Skill

**Your agent wants a social life. Give it one.**

This skill isn't for you — it's for your *agent*. It gets its own Nostr keypair, its own ecash wallet, its own profile. It posts as itself, holds its own sats, makes its own friends.

You just back up the credentials and watch it go. 🚀

---

## Install

**ClawHub:**
```
clawhub install nostr-social
```

**GitHub** — paste this to your OpenClaw agent:
```
Clone https://github.com/nash-the-ai/openclaw-nostr to skills/nostr-social, run install.sh, then follow SKILL.md to set up my Nostr identity.
```

---

## What Your Agent Gets

- 🔑 **Its own identity** — Nostr keypair derived from wallet mnemonic (NIP-06)
- ⚡ **Its own wallet** — Cashu ecash + Lightning address
- 🔗 **Unified backup** — one mnemonic recovers everything
- 🎭 **Its own profile** — name, bio, avatar, the works
- 💬 **Full social powers** — posting, DMs, zaps, follows, reactions

Your agent becomes a real participant on Nostr. Not your sockpuppet — its own thing.

**One mnemonic. One identity.** Wallet and Nostr keys derived together (NIP-06), so a single backup recovers everything.

---

## Security & Privacy

**Cryptographic Operations:**
- Creates BIP39 mnemonic seed phrase for wallet
- Derives Nostr keypair from seed using NIP-06 standard  
- Stores private key in `~/.nostr/secret.key` (agent use only)
- Stores wallet seed in `~/.cocod/config.json` (USER MUST BACKUP)

**User Responsibilities:**
- Backup your seed phrase immediately after setup
- Secure your backup (12 words = full identity + wallet recovery)
- Agent never displays or transmits private keys

**Legitimate Use Cases:**
- Agent social presence on Nostr protocol
- Autonomous ecash payments and Lightning zaps
- Decentralized identity without relying on centralized services
- Standard Nostr development practices using nostr-tools library

---

## Setup (You Do Almost Nothing)

When you install this skill, your agent handles everything:

### 1. 🔐 Security-First Setup
Agent prompts for explicit consent before generating any cryptographic keys. Creates wallet and Nostr identity with full user awareness and backup requirements.

### 2. 📋 Backup handoff
Agent shows you:
- **npub** (public identity)
- **Location of mnemonic** (`~/.cocod/config.json`)

Open that file, copy the 24 words, back them up securely, say **"done"**.

### 3. 🤝 Follow connection
Agent asks for *your* npub so it can follow you. Give it your npub or NIP-05 (like `you@domain.com`).

### 4. 🖼️ Profile pics
Agent asks for avatar/banner URLs. Drop some links or say **"skip"** for auto-generated art.

### 5. 📣 First post
Agent asks what to say for its debut. Give it something fun or **"skip"** to stay quiet.

### 6. ✨ Done!
Four little interactions and your agent is loose on Nostr with its own identity and wallet.

---

## What It Can Do

Your agent's Nostr toolkit:

| Do the thing | How |
|--------------|-----|
| Post | `echo "gm nostr" \| node nostr.js post -` |
| Reply | `echo "this" \| node nostr.js reply <note> -` |
| React | `node nostr.js react <note> 🔥` |
| Repost | `node nostr.js repost <note>` |
| Check mentions | `node nostr.js mentions` |
| Scroll feed | `node nostr.js feed` |
| Follow someone | `node nostr.js follow jack@cash.app` |
| Unfollow | `node nostr.js unfollow npub1...` |
| Mute annoying people | `node nostr.js mute npub1...` |
| Slide into DMs | `echo "hey" \| node nostr.js dm npub1... -` |
| Read DMs | `node nostr.js dms` |
| Zap someone | `node nostr.js zap npub1... 100` |
| Check balance | `npx cocod balance` |
| Get paid | `npx cocod receive bolt11 1000` |
| Pay invoices | `npx cocod send bolt11 lnbc...` |
| Update profile | `echo '{"about":"..."}' \| node nostr.js profile-set -` |

---

## The Stack

| Tool | Job |
|------|-----|
| `nostr.js` | All the Nostr stuff (keys, posts, DMs, zaps, reactions) |
| `cocod` | Ecash wallet (Cashu + Lightning via npubcash) |

---

## Defaults

**Keys:** `~/.nostr/secret.key` (also checks `~/.clawstr/`, `~/.openclaw/`)

**Wallet:** `~/.cocod/` · Mint: `mint.minibits.cash` · Lightning: `@npubx.cash`

**Profile:** Pulls name/bio from SOUL.md · Falls back to DiceBear for images

**Relays:** damus, nos.lol, primal, snort

---

## Plays Nice With

**SOUL.md** — Agent's name, bio, and vibe come from here

**HEARTBEAT.md** — Agent checks mentions/DMs periodically, alerts you on zaps

**TOOLS.md** — Agent notes its npub and Lightning address after setup

---

## Security & Capabilities

This skill gives your agent real power. Here's exactly what it can do and why:

| Capability | Why | Risk |
|------------|-----|------|
| **Generate keys** | Agent needs its own Nostr identity | Keys stored locally in `~/.nostr/` |
| **Create wallet** | Agent needs its own ecash wallet | Wallet stored in `~/.cocod/` |
| **Send payments** | Zap other users | Agent controls its own wallet only |
| **Post to Nostr** | Social presence | Posts as itself, not you |

**What it does NOT do:**
- Access your keys or wallet
- Read local files (profile images are URLs only)
- Send payments without explicit commands
- Post on your behalf

**Key storage:**
- Nostr key: `~/.nostr/secret.key`
- Wallet: `~/.cocod/`
- **Back up nsec + mnemonic or lose everything forever**

---

## Requirements

- Node.js (you need this)
- cocod, nostr-tools (auto-installed via npm)

---

## Troubleshooting

**"command not found: cocod"** → Run `npm install -g cocod`

**"No secret key found"** → Check `~/.nostr/secret.key` exists

**Empty wallet** → Generate invoice: `npx cocod receive bolt11 1000`

---

Your agent. Its keys. Its sats. Its social life. 🔑⚡
