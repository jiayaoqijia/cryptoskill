# Security Practices

## What This Skill Does NOT Do

❌ **No private keys** — Never requests or stores your seed phrase, private key, or signing credentials  
❌ **No signing** — Never executes transactions on-chain  
❌ **No token storage** — Telegram/Discord/Slack tokens are managed by OpenClaw, not this skill  
❌ **No sensitive logging** — API responses are parsed safely; position data is NOT logged  

## What This Skill Does

✅ **Read-only monitoring** — Queries Aave's public GraphQL API for position data  
✅ **Uses OpenClaw's message routing** — Sends alerts through your configured channels  
✅ **Local config storage** — Wallet address stored in OpenClaw's encrypted preferences  
✅ **Background monitoring** — Registers a cron job for automated checks  

---

## Architecture & Data Flow

### 1. Initial Setup (`/aave-config init`)

```
User provides wallet address
        ↓
OpenClaw stores in encrypted config (~/.openclaw/prefs)
        ↓
Wallet address never sent anywhere except Aave API
```

**Security:** Wallet addresses are public blockchain data; encryption protects them from local disk access only.

### 2. Monitoring Check (`/aave-monitor check` or cron interval)

```
Cron job triggers
        ↓
monitor.js reads wallet from OpenClaw config
        ↓
Fetches position from https://api.v3.aave.com/graphql
        ↓
Parses response for: health factor, collateral, debt
        ↓
Formats alert message (no sensitive data logged)
        ↓
Returns message to OpenClaw
        ↓
OpenClaw routes to Telegram/Discord/Slack via configured channel
```

**Security:**
- Only health factor and asset amounts are extracted
- Full API response is NOT logged
- No credentials are passed to external services
- OpenClaw's messaging system handles channel credentials

### 3. Alert Delivery

```
monitor.js returns alert message
        ↓
OpenClaw's cron system receives result
        ↓
OpenClaw routes via pre-configured Telegram/Discord/Slack
        ↓
Alert reaches your device
```

**Security:** Skill has zero access to messaging tokens. OpenClaw handles all credentials.

---

## Code Review Checklist

For security reviewers, here's what to verify:

### Scripts

**scripts/monitor.js**
- ✅ Only fetches from `https://api.v3.aave.com/graphql` (Aave public API)
- ✅ No private key handling
- ✅ No logging of full API responses
- ✅ Error messages don't include sensitive data
- ✅ Returns only parsed data (HF, collateral, debt, asset names)

**scripts/cron-runner.js**
- ✅ No credential storage
- ✅ Returns structured result for OpenClaw routing
- ✅ No external messaging calls (uses OpenClaw's system)

### Configuration

**assets/config-template.json**
- ✅ No API keys or tokens
- ✅ Wallet address marked as configuration (not hardcoded)
- ✅ Thresholds and intervals are user-configurable

### Documentation

**SKILL.md**
- ✅ Clearly states "no private keys"
- ✅ Explains credential handling via OpenClaw
- ✅ Documents what data is stored where

---

## Threat Model

### Attacks Mitigated

**Compromised OpenClaw instance:**
- Your wallet address is readable from encrypted config
- But attacker can only READ public position data (no signing possible)
- Messaging tokens remain in OpenClaw's systems, not this skill

**Man-in-the-middle (MITM):**
- Aave API uses HTTPS/TLS
- OpenClaw messaging uses HTTPS/TLS
- No credentials transmitted by this skill

**Malicious skill code:**
- Skill code is auditable (open source)
- Credentials are managed by OpenClaw, not passed to skill
- Skill can only send alerts; cannot modify Aave positions

### Assumptions

1. **OpenClaw is trustworthy** — Credentials stored in OpenClaw are handled securely
2. **Aave API is trustworthy** — Public API is from Aave Foundation
3. **HTTPS works** — TLS connections are not compromised
4. **User machine is not fully compromised** — If attacker has full local access, they can steal anything

---

## Configuration & Storage

### Wallet Address Storage

- **Where:** `~/.openclaw/prefs/aaveLiquidationMonitor.json` (encrypted at rest)
- **What:** Your Ethereum wallet address (public data)
- **Risk:** Low — wallet addresses are public blockchain data
- **Why encrypted:** To prevent casual disk inspection

### Messaging Channel

- **Where:** Configured in OpenClaw's settings (outside this skill)
- **Token storage:** OpenClaw's credential manager, NOT this skill
- **Risk:** OpenClaw's responsibility, not this skill's

### Logs

- **Health factor checks:** Logged to OpenClaw session history
- **Sensitive data:** NOT logged (wallet positions, API responses)
- **Retention:** Follows OpenClaw's log retention policy

---

## What Requires User Awareness

Users should understand:

1. **Public data:** Your wallet address is visible on-chain; monitoring it publicly is your choice
2. **Alert delivery:** Whoever has access to your Telegram/Discord/Slack account can see alerts
3. **Background execution:** Cron job runs every 6 hours; network requests go to Aave API
4. **Logging:** Your health factor is logged in OpenClaw's session history
5. **Prerequisites:** This skill relies on OpenClaw's messaging integrations being set up correctly

---

## Recommended User Setup

For maximum security:

1. ✅ Use a **read-only address** (not your hot wallet with signing keys)
2. ✅ Ensure your **Telegram/Discord/Slack channel is private**
3. ✅ Keep **OpenClaw updated** to get security patches
4. ✅ Review **OpenClaw logs** periodically
5. ✅ Don't share **ClawhHub links with untrusted sources**

---

## Incident Response

If something seems wrong:

1. **Disable monitoring immediately:**
   ```bash
   /aave-monitor disable
   ```

2. **Check logs for anomalies:**
   ```bash
   /aave-monitor logs 50
   ```

3. **Review OpenClaw audit trail:**
   ```bash
   /sessions history
   ```

4. **Reset configuration:**
   ```bash
   /aave-config reset
   /aave-config init
   ```

---

## Contact & Reporting

Found a security issue? 

- Do NOT disclose publicly
- Report directly to the skill maintainer via GitHub issues (private if available)
- Include: severity, description, reproduction steps
- Allow time for patches before public disclosure

---

## Versions & Updates

- **v1.0.0:** Initial release
- All releases are version-controlled and auditable on ClawhHub
- Security patches are released as semver updates

---

**Last updated:** 2026-02-11  
**Security level:** Transparent design, no credential storage in skill  
**Recommended for:** Read-only position monitoring on Aave V3
