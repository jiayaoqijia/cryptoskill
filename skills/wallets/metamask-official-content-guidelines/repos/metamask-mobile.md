---
repo: metamask-mobile
parent: content-guidelines
---

# MetaMask Content Design Guidelines — Mobile

> Source of truth: MetaMask Content Design Style Guide (internal). This skill encodes the decisions from that guide for AI-assisted development. For component-specific copy rules, read the relevant component README in MetaMask/metamask-design-system via Storybook MCP.

---

## Capitalization

**Default: sentence case.** Capitalize only the first word of a string and any words that qualify as exceptions below.

### ✅ Title case is correct for

| Category | Examples |
|----------|---------|
| Special terms | Secret Recovery Phrase, Private Key |
| MetaMask product names | MetaMask, MetaMask Card, Metal Card, Virtual Card, Snaps, Perps, Predictions, Rewards (the product) |
| Other proper nouns | Ethereum, OpenSea, Ledger, Apple, Google, Consensys |
| Network names | Ethereum Mainnet, Polygon Mainnet, Arbitrum One |
| Abbreviations | NFT, API, DAO, DeFi, ETH, BTC, SOL |

### ❌ Title case is wrong for

Everything else — including titles, subtitles, button labels, menu items, settings labels, section headers, screen headers, tags, and feature names that are not trademarked.

```
❌ "Turn on Device Authentication"
✅ "Turn on device authentication"

❌ "Enable NFT Autodetection"
✅ "Turn on NFT autodetection"   ← NFT stays caps; "autodetection" does not

❌ "Sample Banner Alert Title"
✅ "Sample banner alert title"

❌ "Start Trading"
✅ "Start trading"
```

---

## Punctuation

### Periods

Use a period when the string is a **complete sentence**. Do not use a period on labels, headings, button text, tags, tab labels, or any string that is not a complete sentence.

```
✅ "Your transaction couldn't be completed, so it was canceled."  ← body copy, complete sentence
✅ "Network fee"                                                      ← label, no period
✅ "Turn on notifications"                                            ← button, no period
❌ "Network fee."
❌ "Turn on notifications."
❌ "Incorrect password. Try again"  ← second sentence needs a period too
✅ "Incorrect password. Try again."
```

**Never** use a period after "Learn more" as a link label.

### Exclamation points

Use sparingly — only for genuinely exciting moments (new feature announcements). Never in errors, alerts, or confirmations.

```
❌ "Done!"   ❌ "Complete!"   ❌ "Error!"
✅ "The Ethereum Merge is here!"  ← rare, high-impact
```

### Ellipsis

Only in address abbreviations (`0x0000...0000`) and loading/in-progress states. Do not use to trail off a sentence.

```
✅ "Turning on notifications..."   ← loading state
✅ "0x0000...0000"                 ← address format
❌ "Are you sure you want to proceed…"
```

### Ampersands

Never use `&` when "and" works. Never use `+` in place of either.

```
❌ "Security & privacy"
✅ "Security and privacy"
```

### Commas

Use the serial (Oxford) comma in lists of three or more.

```
✅ "Tokens, NFTs, and DeFi"
❌ "Tokens, NFTs and DeFi"
```

### Colons

Do not use colons in labels or headings. Use sparingly in body copy.

---

## Voice and tone

### Active voice

```
✅ "We're investigating the problem."
❌ "The problem is being investigated."
```

### Point of view

- User's things: **your** (never "my")
- MetaMask: **we / our**
- Never first-person singular (I, me, my) for MetaMask

```
✅ "Connect your accounts"   ✅ "We're here to help"
❌ "Connect my accounts"     ❌ "I need help"
```

### Contractions

Use them. They feel more human.

```
✅ "We're here to help"   ✅ "Don't worry, you can edit this later"
❌ "We are here to help"    ❌ "Do not worry"
```

### Words to avoid

| Avoid | Reason | Instead |
|-------|--------|---------|
| "successfully" | The success state is the success | "File uploaded" |
| "please" | UI isn't asking a favor | "Enter a name" |
| "click here" / "tap to…" | Directional, not descriptive | Name the destination |
| "!" in errors or system copy | Reads as alarm | Remove it |
| "fiat" | Confusing to general users | "local currency" |
| "gas fee" / "gas fees" | Deprecated term | "network fee" / "network fees" |
| "dapp" | Jargon | "site" (unless technical context) |
| "native currency" | Technical | "network currency" |
| "token allowance" | Technical | "spending cap" |
| "cryptocurrency" | Unnecessary | "crypto" |
| "coins" | Imprecise | "tokens" |
| "delete wallet" | Alarming | "reset wallet" |

---

## Terminology reference

| Use | Not |
|-----|-----|
| Secret Recovery Phrase | seed phrase, SRP (never abbreviate in product) |
| network fee | gas fee, gas fees |
| network currency | native currency |
| spending cap | token allowance |
| site | dapp (unless writing for technical audience) |
| crypto | cryptocurrency |
| tokens | coins |
| reset wallet | delete wallet, erase wallet |
| local currency | fiat |
| smart account | smart contract account |
| back up (verb) / backup (noun) | — |
| MetaMask Card | MetaMask card |
| card (lowercase) | Card (when referring to the physical/virtual card, not the product name) |
| Snaps | snaps, SNAPS, dApps (when referring to the MetaMask Snaps platform) |
| Perps (product) / perps (generic) | — |
| Predictions (product) / predictions (generic) | — |
| Rewards (product) / rewards (generic) | — |

### Date and number formatting

- Dates: `Jun 16 at 5:55 p.m.` — never ordinals (no "16th"), never 24-hour time
- Day abbreviations: Mon, Tue, Wed, Thu, Fri, Sat, Sun
- Month abbreviations: Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec
- Large amounts: `$500K`, `$20M`, `$100B` — always uppercase letter
- Number ranges: `1-20` (hyphen, no spaces)
- Addresses: `0x0000...0000`
- Decimals: comma as separator (`100,000`) — localization handles regional variants
