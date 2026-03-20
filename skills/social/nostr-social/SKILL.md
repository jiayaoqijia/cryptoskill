---
name: Nostr
description: Your agent wants a social life. Give it one. This skill gives your agent its own Nostr identity + ecash wallet. One mnemonic backs up everything (NIP-06). Not for you — for your agent. It owns its own keys, its own sats, posts as itself. One install, automatic bootstrap, no third parties.
tags: nostr, bitcoin, lightning, cashu, identity, social, wallet
---

# Nostr Skill

Self-sovereign Nostr identity + ecash wallet. Complete bootstrap.

## Capabilities Disclosure

This skill grants these capabilities to the agent:

- **Key generation** — Creates Nostr keypair in `~/.nostr/secret.key`
- **Wallet creation** — Cashu wallet in `~/.cocod/` (mnemonic in config.json — user backs up)
- **Nostr posting** — Posts, DMs, zaps as the agent's identity

Agent runs wallet/identity setup with explicit user consent. User is directed to back up `~/.cocod/config.json` (contains mnemonic). Agent reads mnemonic for NIP-06 key derivation but never displays or transmits it. Profile images use URLs only (no local file access).

## On Install

When skill is installed (user pastes ClawHub link), run this flow:

### Step 1: Secure Setup (User Consent Required)

**SECURITY NOTICE:** This skill will create cryptographic keys for your agent. This requires:
- Creating Nostr identity keypair in `~/.nostr/secret.key`
- Creating Cashu wallet with backup seed in `~/.cocod/config.json`
- User must explicitly backup the mnemonic seed phrase

```bash
# Install dependencies
bash {SKILL_DIR}/install.sh

# Prompt user for consent before key generation
echo "⚠️  SECURITY: This will create cryptographic keys for your agent."
echo "   - Nostr identity keypair: ~/.nostr/secret.key"  
echo "   - Cashu wallet seed: ~/.cocod/config.json"
echo "   - You MUST backup your seed phrase"
echo ""
read -p "Continue with key generation? (yes/no): " consent
if [ "$consent" != "yes" ]; then
  echo "Setup cancelled"
  exit 1
fi

# Create wallet (mnemonic saved to config file)
npx cocod init

# Derive Nostr identity from wallet mnemonic (NIP-06)
node {SKILL_DIR}/scripts/nostr.js init

# Get identity info
NPUB=$(node {SKILL_DIR}/scripts/nostr.js whoami | grep npub | awk '{print $2}')
LN_ADDR=$(npx cocod npc address)

# Set basic profile
node {SKILL_DIR}/scripts/nostr.js profile-set '{"name":"<NAME>","about":"<ABOUT>","lud16":"'$LN_ADDR'"}'
```

### Step 2: Report Results + Backup Warning

Reply to user:

---

⚡ **Nostr identity ready!**

**npub:** `npub1...`
**Lightning address:** `npub1...@npubx.cash`

---

⚠️ **IMPORTANT: Back up your recovery phrase**

Your 24-word mnemonic is stored in:
```
~/.cocod/config.json
```

This phrase recovers both your Nostr identity AND ecash wallet. Back it up securely and protect this file.

Reply "done" when you've backed it up.

---

### Step 3: Wait for "done"

Do not proceed until user confirms backup.

### Step 4: Ask for Owner's npub

---

**What's your Nostr npub?**

I'll follow you so we stay connected.

(Paste your npub1... or NIP-05 like you@domain.com)

---

Then:
```bash
# If NIP-05, resolve first
node {SKILL_DIR}/scripts/nostr.js lookup <nip05>

# Follow owner
node {SKILL_DIR}/scripts/nostr.js follow <owner_npub>
```

### Step 5: Ask for Profile Images

---

**Do you have profile images for me?**

- **Avatar:** Paste URL (square, 400x400 recommended)
- **Banner:** Paste URL (wide, 1500x500 recommended)

Or say "skip" and I'll generate unique ones automatically.

---

If URLs provided:
```bash
node {SKILL_DIR}/scripts/nostr.js profile-set '{"picture":"<avatar_url>","banner":"<banner_url>"}'
```

If skipped, use DiceBear (deterministic, unique per npub):
```bash
AVATAR="https://api.dicebear.com/7.x/shapes/png?seed=${NPUB}&size=400"
BANNER="https://api.dicebear.com/7.x/shapes/png?seed=${NPUB}-banner&size=1500x500"
node {SKILL_DIR}/scripts/nostr.js profile-set '{"picture":"'$AVATAR'","banner":"'$BANNER'"}'
```

### Step 6: First Post

---

**Ready for your first post?**

Tell me what to post, or say "skip".

Suggestion: "Hello Nostr! ⚡"

---

If user provides text (use stdin to avoid shell injection):
```bash
echo "<user's message>" | node {SKILL_DIR}/scripts/nostr.js post -
```

### Step 7: Done

---

✅ **All set!**

- Following you ✓
- First post live ✓ (if not skipped)

Try: "check my mentions" or "post <message>"

---

## Commands Reference

### Posting
```bash
# Use stdin for content (prevents shell injection)
echo "message" | node {SKILL_DIR}/scripts/nostr.js post -
echo "reply text" | node {SKILL_DIR}/scripts/nostr.js reply <note1...> -
node {SKILL_DIR}/scripts/nostr.js react <note1...> 🔥
node {SKILL_DIR}/scripts/nostr.js repost <note1...>
node {SKILL_DIR}/scripts/nostr.js delete <note1...>
```

### Reading
```bash
node {SKILL_DIR}/scripts/nostr.js mentions 20
node {SKILL_DIR}/scripts/nostr.js feed 20
```

### Connections
```bash
node {SKILL_DIR}/scripts/nostr.js follow <npub>
node {SKILL_DIR}/scripts/nostr.js unfollow <npub>
node {SKILL_DIR}/scripts/nostr.js mute <npub>
node {SKILL_DIR}/scripts/nostr.js unmute <npub>
node {SKILL_DIR}/scripts/nostr.js lookup <nip05>
```

### DMs
```bash
echo "message" | node {SKILL_DIR}/scripts/nostr.js dm <npub> -
node {SKILL_DIR}/scripts/nostr.js dms 10
```

### Zaps
```bash
# Get invoice
node {SKILL_DIR}/scripts/nostr.js zap <npub> 100 "comment"
# Pay it
npx cocod send bolt11 <invoice>
```

### Wallet
```bash
npx cocod balance
npx cocod receive bolt11 1000    # Create invoice
npx cocod send bolt11 <invoice>  # Pay invoice
npx cocod npc address            # Lightning address
```

### Profile
```bash
node {SKILL_DIR}/scripts/nostr.js whoami
node {SKILL_DIR}/scripts/nostr.js profile
node {SKILL_DIR}/scripts/nostr.js profile "Name" "Bio"
node {SKILL_DIR}/scripts/nostr.js profile-set '{"name":"X","picture":"URL","lud16":"addr"}'
```

### Bookmarks
```bash
node {SKILL_DIR}/scripts/nostr.js bookmark <note1...>
node {SKILL_DIR}/scripts/nostr.js unbookmark <note1...>
node {SKILL_DIR}/scripts/nostr.js bookmarks
```

### Relays
```bash
node {SKILL_DIR}/scripts/nostr.js relays
node {SKILL_DIR}/scripts/nostr.js relays add <url>
node {SKILL_DIR}/scripts/nostr.js relays remove <url>
```

### Autoresponse (Heartbeat Integration)
```bash
# Get unprocessed mentions from WoT (JSON output)
node {SKILL_DIR}/scripts/nostr.js pending-mentions [stateFile] [limit]

# Mark mention as responded (after replying)
node {SKILL_DIR}/scripts/nostr.js mark-responded <note1...> [responseNoteId]

# Mark mention as ignored (no response needed)
node {SKILL_DIR}/scripts/nostr.js mark-ignored <note1...> [reason]

# Check hourly rate limit (max 10/hr)
node {SKILL_DIR}/scripts/nostr.js rate-limit

# Show autoresponse state summary
node {SKILL_DIR}/scripts/nostr.js autoresponse-status
```

**State file:** `~/.openclaw/workspace/memory/nostr-autoresponse-state.json`
**WoT source:** Owner's follow list (defined in nostr.js as OWNER_PUBKEY)

## User Phrases → Actions

| User says | Action |
|-----------|--------|
| "post X" | `echo "X" \| nostr.js post -` |
| "reply to X with Y" | `echo "Y" \| nostr.js reply <note> -` |
| "check mentions" | `nostr.js mentions` |
| "my feed" | `nostr.js feed` |
| "follow X" | Lookup if NIP-05 → `nostr.js follow` |
| "DM X message" | `echo "message" \| nostr.js dm <npub> -` |
| "zap X 100 sats" | `nostr.js zap` → `npx cocod send bolt11` |
| "balance" | `npx cocod balance` |
| "invoice for 1000" | `npx cocod receive bolt11 1000` |
| "my npub" | `nostr.js whoami` |
| "my lightning address" | `npx cocod npc address` |

## Defaults

| Setting | Value |
|---------|-------|
| Mint | `https://mint.minibits.cash/Bitcoin` |
| Lightning domain | `@npubx.cash` |
| Avatar fallback | `https://api.dicebear.com/7.x/shapes/png?seed=<npub>` |
| Nostr key | `~/.nostr/secret.key` |
| Wallet data | `~/.cocod/` |

## Integration

### SOUL.md
- Pull name/about from SOUL.md or IDENTITY.md
- Match posting voice/tone to agent's personality
- Don't be generic - posts should sound like the agent

### HEARTBEAT.md
Add to heartbeat rotation (every 2-4 hours):
```bash
# Check Nostr activity
node {SKILL_DIR}/scripts/nostr.js mentions 10
node {SKILL_DIR}/scripts/nostr.js dms 5
```
If mentions from WoT or zaps received → notify user.

### TOOLS.md
After setup, store for quick reference:
```markdown
## Nostr
- npub: npub1...
- Lightning: npub1...@npubx.cash  
- Owner: npub1... (followed)
```

## Profile Sources

- **Name**: IDENTITY.md or SOUL.md
- **About**: SOUL.md description
- **Picture**: User-provided URL, or DiceBear fallback
- **Banner**: User-provided URL, or DiceBear fallback
- **lud16**: From `npx cocod npc address`
