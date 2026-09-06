# Web3 UX Patterns Reference

Best practices and anti-patterns for web3 landing pages, organized by project
type. Used by the `web3-ux-feedback` skill during UX evaluation.

---

## Universal Patterns (All Web3 Projects)

### The 5-Second Test
Hero section must answer within 5 seconds:
1. What is this?
2. Who is it for?
3. What do I do next?

If it fails this test, all other optimizations are secondary.

### The Trust Stack
Web3 users are uniquely skeptical. Build trust before asking for conversion:

1. **Security audits** — logos + links (CertiK, OpenZeppelin, Trail of Bits, Halborn)
2. **On-chain transparency** — contract address visible + verified on block explorer
3. **Team credibility** — doxxed team or known pseudonyms with established reputation
4. **Track record** — time in operation, no exploits, TVL history
5. **Community** — Discord/Twitter size (weak alone, strong with above)

### The Jargon Ladder
Identify your audience's level and write to ONE level — don't split:

```
Level 1: Total newcomer    "I've heard of Bitcoin but don't own any"
Level 2: Crypto curious    "I own some ETH but haven't used DeFi"
Level 3: Crypto user       "I have MetaMask and have made a few trades"
Level 4: DeFi native       "I regularly provide liquidity and stake"
Level 5: Power user / Dev  "I read whitepapers, run nodes, audit contracts"
```

Writing for Level 4 while trying to reach Level 2 is the most common mistake.

### CTA Hierarchy
Every page needs a clear CTA hierarchy:

- **Primary:** Main conversion action — 1 per screen, high contrast
  - Examples: "Start Trading", "Launch Collection", "Join the DAO"
- **Secondary:** Lower-commitment alternative
  - Examples: "See How It Works", "Watch Demo", "Read the Docs"
- **Tertiary:** Passive engagement
  - "Follow on Twitter", "Join Discord", "Subscribe for updates"

---

## Patterns by Project Type

### DeFi Protocols (DEX, Lending, Yield)

**Lead with:**
- TVL or trading volume (if impressive — always link to on-chain verification)
- Security audits (non-negotiable — put in hero, not footer)
- Supported chains/assets above the fold

**Recommended section order:**
1. What can you earn/trade/borrow? (outcome-first)
2. Why is it safe? (audits, track record, non-custodial statement)
3. How does it work? (3-step flow, no jargon)
4. Who else uses it? (protocol logos, TVL counter)
5. CTA: "Start earning" / "Connect and trade"

**Critical trust signals:**
- Audit logos + links in hero section
- Non-custodial / "your keys, your funds" language
- TVL counter (live if possible)
- Network/chain identifiers

**Red flags:**
- Showing APY/yields without risk disclosure
- Hiding fees — always show fee structure clearly
- Requiring wallet connection before showing any information
- Supported chains only in the footer

---

### NFT Marketplaces & Launchpads

**Lead with:**
- What makes this marketplace different from OpenSea/Blur/Tensor
- Creator OR collector focus — pick one for the main message
- Current featured collections (visual-first — show the art)

**Recommended section order:**
1. Who specifically is this for? (creators, collectors — choose one to lead)
2. What can you do here that you can't elsewhere?
3. Featured/trending collections (visual)
4. Creator earnings / royalty protection stance
5. CTA: "Start creating" / "Browse collections" / "Launch your collection"

**Critical trust signals:**
- Volume traded ($) or total sales
- Royalty protection stance (crucial post-2022 royalty wars)
- Chain compatibility
- Number of creators or collectors

**Red flags:**
- Generic "discover, create, sell" — same as every other marketplace
- Not showing actual NFTs prominently (it's a visual product)
- Assuming users know how to mint
- No creator success stories or specific metrics

---

### DAO Tooling & Governance

**Lead with:**
- Which type of DAO this is built for (DeFi DAO? Protocol DAO? Social?)
- The specific governance problem it solves
- Notable DAOs using it (logos/names if possible)

**Recommended section order:**
1. What's broken about current governance?
2. What can DAO members do now that they couldn't?
3. Setup flow — "time to first proposal" is a powerful metric
4. Which DAOs trust this? (named logos)
5. CTA: "Set up your DAO" / "Try the demo" / "Schedule a call"

**Critical trust signals:**
- Total governance volume ($) or proposals passed
- Named DAOs using the tool
- Integration with known infrastructure (Gnosis Safe, Snapshot, etc.)

**Red flags:**
- Targeting "all DAOs" without specificity
- Ignoring the token-holder vs. core-team tension in messaging
- Not showing what a proposal actually looks like
- Missing "time to first proposal" (very compelling for adoption)

---

### Layer 2 & Infrastructure

**Lead with:**
- Speed + cost comparison vs. L1 (specific numbers — TPS, avg gas cost)
- Which ecosystems/apps are already deployed
- Security model in plain language (not "we use zk-STARKs")

**Recommended section order:**
1. The scalability problem (make it feel painful with numbers)
2. How much faster/cheaper? (specific data vs. Ethereum)
3. What's already deployed? (app and protocol logos — shows ecosystem health)
4. How do I get started? (bridge + wallet setup, 3-step flow)
5. CTA: "Bridge to [Name]" / "Deploy on [Name]" / "Explore ecosystem"

**Critical trust signals:**
- TPS vs. Ethereum (specific number)
- Average gas cost comparison
- Total value bridged
- EVM compatibility statement
- Security audit methodology (simplified)

**Red flags:**
- Too technical — users don't need to understand ZK proofs to use the chain
- Targeting developers AND end-users with the same message
- Not showing the ecosystem of apps already deployed
- No "how do I bridge" section for end-users

---

### GameFi / Web3 Gaming

**Lead with:**
- The game itself (not the token economy — lead with fun, not yield)
- Genre + what makes it different
- "Play for free" or "Free to start" if applicable

**Recommended section order:**
1. What is this game? (show gameplay — screenshots, video)
2. What makes it web3? (ownership, trading, earning — in that order)
3. How do I start? (simple onboarding, mobile-friendly if applicable)
4. Community (player count, notable tournaments, content creators)
5. CTA: "Play now" / "Start for free" / "Download"

**Critical trust signals:**
- Active player count
- Total assets owned by players
- Game studio reputation / prior games
- Partnership with known IP if applicable

**Red flags:**
- Leading with tokenomics (signals "money grab" to real gamers)
- Complex wallet setup before showing the game
- NFT language that alienates traditional gamers
- No gameplay screenshots or video above the fold

---

## Successful Web3 Landing Page Benchmarks

Reference when giving competitive inspiration:

| Project | What they do well |
|---------|------------------|
| Uniswap | "Swap tokens" in large text — clarity over everything, no jargon |
| Aave | TVL and audits above the fold — trust before product pitch |
| ENS | "Your web3 username" — perfect ICP specificity and clarity |
| Safe (Gnosis) | Enterprise trust signals throughout, B2B positioning |
| Lens Protocol | Clear developer ICP — "Build social apps on Lens" |
| Nouns DAO | Community IS the product — art-first landing page |

---

## Universal Red Flags Checklist

Flag these in every evaluation:

**Messaging:**
- [ ] "The future of [X]" or "next-gen" in headline
- [ ] No specific target user mentioned anywhere above the fold
- [ ] Features listed without benefits or capabilities
- [ ] No acknowledgment of alternatives
- [ ] No metrics or social proof
- [ ] No urgency or reason to act now

**UX:**
- [ ] Wallet connection required to view basic project information
- [ ] All CTAs say "Connect Wallet" — no value-oriented alternatives
- [ ] No mobile optimization
- [ ] No "how it works" section for newcomers
- [ ] Audit info buried in footer or docs only
- [ ] No secondary CTA for users not ready to connect
- [ ] Unexplained jargon in hero section
- [ ] Generic blockchain stock imagery (floating coins, grid backgrounds)