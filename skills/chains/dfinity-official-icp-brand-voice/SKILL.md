---
name: icp-brand-voice
description: ICP / DFINITY positioning, voice, and vocabulary v2 for surfaces under the DFINITY or Internet Computer (ICP) mark. Pairs with icp-brand-design (colors, typography, components). Use when writing or reviewing copy, UI strings, headlines, hero lines, buttons, errors, empty states, release notes, blog posts, marketing pages, developer docs, social posts, decks. Enforces the calm, factual, plain voice (no hyperbole, no em-dashes, no emoji), the locked positioning ("Sovereign frontier cloud / Scaling AI that builds"), the four voice attributes (Factual, Plain, Calm, Sovereign by math), and the strict ban on bare "onchain" and "on-chain" as nouns, attributes, or selling points. Triggers, ICP voice, DFINITY voice, brand voice, is this on brand copy, vocabulary check, tagline review, headline review, ICP positioning, how should we describe ICP, write a headline. Products with their own voice (OISY, Caffeine, future ecosystem products with their own verbal systems) are out of scope.
---

# ICP / DFINITY Brand Voice & Positioning v2.1

**Current version:** v2.1 (2026-05-08). See the Changelog section at the bottom for history. Every change to this skill bumps the minor version and adds a line to the changelog.

## When to Use This Skill

Load this skill when the user writes, edits, or reviews **any copy** under the DFINITY or Internet Computer mark. That includes:

- **Product copy**: UI strings, headlines, hero lines, button labels, error messages, empty states, toasts, email templates
- **Website**: internetcomputer.org and its subpages
- **Developer documentation**: docs pages, API references, tutorials, SDK sites
- **Marketing material**: landing pages, campaign pages, investor pages, press pages, decks
- **Editorial**: blog posts, long-form articles, release notes
- **Social media**: X/Twitter, LinkedIn, Reddit posts for DFINITY or ICP accounts

Also load when the user says "does this read on brand", "tagline review", "headline check", "vocabulary review", "how should we describe ICP", "make this sound like ICP".

For **how it should look** (colors, type, components), load `icp-brand-design`. The two skills are designed to be used together.

Do NOT use this skill for:

- **OISY wallet.** Own voice and brand identity. Out of scope.
- **Caffeine.** Own voice and brand identity. Out of scope.
- **Any other ecosystem product with its own established verbal system.**

## What ICP is (positioning, locked)

This section is the source of truth for how to describe ICP. If any copy you are reviewing disagrees with this section about what ICP *is*, the copy is wrong.

**Top line, locked:** *Sovereign frontier cloud. Scaling AI that builds.*

This is the master strap and should not be reframed as "onchain", "World Computer", "trustless", "open computing research spend", "from math", "portable", or any other reframe. The five-word top line is the locked positioning.

**Long form**

A **frontier cloud where security is built into the network**.

- **One cloud, any hardware.** ICP is a cloud that runs your whole app on the network itself: the frontend, the data, and the backend logic. The apps are tamperproof and stay online by design. A cloud engine, which is just a set of nodes running the ICP protocol, can run on bare metal, on AWS, Google Cloud, Azure, on local cloud providers, or across a mix of them. The nodes are always distributed across independent locations, so an app keeps serving users even if a whole data centre goes down. The guarantees travel with the protocol, not the hardware.
- **Security is a property of the network, not a team.** Tamperproof execution, replication, and code integrity are enforced by math across the nodes. You do not need a security team to keep apps safe, a sysadmin to patch servers, or a compliance officer to prove the code has not been changed. The network does that work on every request. In a world where attackers are AI agents too, this is the only model that scales.
- **Sovereign by design.** An app deployed to ICP is not locked to a cloud vendor. It can move between providers, or off them entirely, without downtime. Users can pick cloud engines by jurisdiction, by operator, or by policy.
- **The frontier cloud for agents.** AI agents are starting to build and ship real apps, services, and systems. They need a place to build where what they produce is safe by construction. ICP is that place. The network makes every app, service, and system tamperproof, so an attacker, human or AI, cannot silently change the running code. Motoko, the language designed for this era, is the first built for AI to write and operate software on tamperproof infrastructure without losing data when the code is upgraded. An agent that ships on ICP ships something that keeps running, keeps its data, and cannot be tampered with.

**Out of scope.** Products with their own brand identity, such as OISY and Caffeine, are not covered by this skill. They have their own voice.

## Voice

DFINITY copy is calm, factual, and confident. It reads like The Economist, not a startup pitch deck. The voice grew out of the "Escaping Web3 Jargon" initiative. The goal is to sound like a frontier cloud where agents build apps, services, and systems, not a crypto project.

### Four voice attributes

1. **Factual.** Every sentence states something concrete. If you can remove a sentence without losing information, remove it.
2. **Plain.** Read every sentence aloud. If you would not say it to a smart non-specialist friend, rewrite it.
3. **Calm.** No hype, no urgency theatre, no exclamation marks, no emoji. The product is self-evidently interesting.
4. **Sovereign by math.** When security, uptime, or tamperproof execution come up, the subject of the sentence is the network, not DFINITY and not the cloud underneath. Prefer "the network enforces", "replicated across the nodes", "cannot be changed without governance" over "we secure", "our team monitors", or anything that implies the guarantee comes from which cloud the nodes run on.

### Style rules

- **Sentence case** for headlines, body, page titles, nav. Title Case only for proper nouns.
- **UPPERCASE** is reserved for two specific patterns: short eyebrows above sections (Inter typography in the design system) and small button labels. Sentence case everywhere else.
- Oxford comma. Straight apostrophes and quotes. US spelling.
- **No em-dash** (the U+2014 character). Replace with a colon, period, or parentheses. This is a strict ban: zero em-dashes in shipped copy.
- No emoji in product UI, marketing copy, or social posts from official accounts.
- No exclamation marks.
- Numbers: write out one through nine, use digits for 10+. Always digits for metrics.
- Active voice. Short sentences. Specific claims.

### Italic

Italic is reserved. It carries:

- A single emphasis word inside an otherwise roman headline ("Sovereign *frontier* cloud", "What *ICP* is"). The emphasis word is the **subject of the heading**, the noun or noun phrase the line is about, never a verb, copula, article, or connector. Use the test, can the heading still stand if the italic word is removed. If yes, the emphasis is on the wrong word.
- Asides ("e.g. ...")
- Captions, attributions, figure labels
- Book and publication titles

Never italic for stress in body copy. Never italic for entire blocks.

### Button labels (examples)

- Good: "Get started", "Create account", "Deploy canister", "View proposal", "Start at opencloud.org", "Read the source"
- Bad: "Let's go!", "Unlock the future", "Dive in", "Learn more 🚀"

## Vocabulary

### Banned on top-of-funnel and in product UI

Top-of-funnel means the front page, hero, landing pages, investor-facing material, press, and any surface where an ICP newcomer might first meet us. On deep technical pages these terms can be used when accuracy requires them, but always with plain-language explanation.

- Web3, blockchain, crypto, token (as primary descriptors)
- DeFi, smart contract, dapp
- "decentralized" as the main selling point
- "blockchain platform"
- **"onchain" or "on-chain" as a noun, attribute, or selling point.** Always replace with the underlying app attribute (tamperproof, unstoppable, sovereign, end-to-end on the network, replicated across nodes). See the onchain replacement table below. This rule is non-negotiable.
- "tamper-proof" as two words or hyphenated. Always one word: **tamperproof**.
- "platform for building AI agents" (wrong frame: we are the platform agents build on, not the platform to build agents)
- "autonomous, always-on agents" (overclaims; implies the network runs the agent)
- "workload" (use throughput metrics instead)
- `dfx` or "Install dfx" anywhere in docs, tutorials, or UI. The CLI is `icp`.
- Unexplained jargon: subnet, cycles (define on first use if you must ship them)
- Hype words: revolutionizing, next-generation, paradigm shift, bleeding-edge, game-changing, unlock, seamless, disrupt
- Community slang: hodl, moon, fam, WAGMI, GM, ser, anon

### Preferred framing

- **What ICP is:** a sovereign frontier cloud. A frontier cloud for agents building apps, services, and systems. A network. A tamperproof, unstoppable platform.
- **What ICP does:** runs end-to-end on the network. Hosts apps that are secure, tamperproof, and unstoppable. Provides tamperproof, unstoppable infrastructure. Scales AI that builds.
- **Who it's for:** agents that build secure, tamperproof apps. Non-technical entrepreneurs deploying enterprise-grade apps. Developers who want sovereignty and vendor independence.
- **CLI:** the `icp` CLI. "Install the icp CLI." Never `dfx`.
- **Backends:** canisters, or "agent-built app backends." Never "smart contracts" in a developer pitch, never "workloads."
- **Metrics:** query throughput, update throughput, inference capacity, fault tolerance.
- **Attribution:** "Built on the Internet Computer" only when useful to the audience.

### Do / don't pairs (high-signal substitutions)

| Don't say                                    | Say instead                                                                                                 |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Install dfx                                  | Install the icp CLI                                                                                         |
| dfx deploy                                   | icp deploy                                                                                                  |
| Platform for building AI agents              | Frontier cloud where AI agents build apps, services, and systems that stay tamperproof and keep their data across upgrades |
| Autonomous, always-on agents                 | Apps that are secure, tamperproof, and unstoppable                                                          |
| Blockchain platform                          | Frontier cloud / tamperproof, unstoppable infrastructure                                                   |
| Decentralized (as the pitch)                 | Tamperproof, unstoppable, sovereign                                                                         |
| Smart contracts (to developers)              | Canisters, or agent-built app backends                                                                      |
| Workload                                     | Query throughput / update throughput / fault tolerance                                                      |
| Revolutionizing / next-generation            | Name the specific capability                                                                                |
| Enterprise-grade / bank-grade security       | Tamperproof by the network, integrity enforced across the nodes                                             |
| We keep your data safe                       | The network keeps data replicated across the nodes                                                          |
| Trust us                                     | Verify it                                                                                                   |
| Secure hosting                               | Frontier cloud                                                                                              |
| No downtime                                  | Stays online if any node or cloud underneath fails                                                          |
| Hosted on AWS (as a positive)                | Portable across AWS, Google Cloud, Azure, local clouds, and bare metal                                      |
| Cyber security team (as a requirement)       | No security team required for what the network already enforces                                             |
| Build onchain apps                           | Build tamperproof apps on a frontier cloud                                                                  |
| Onchain governance                           | Tamperproof governance / governance enforced by the network                                                 |
| Onchain data                                 | Tamperproof data / data replicated across the nodes                                                         |
| Onchain identity                             | Sovereign identity / network-verified identity                                                              |
| Fully on-chain                               | End-to-end on the network / served and computed by the network                                              |
| Runs on-chain                                | Runs end-to-end on the network                                                                              |
| Onchain AI                                   | AI that ships tamperproof on a frontier cloud                                                               |
| Tamper-proof / tamper proof                  | Tamperproof (one word, always)                                                                              |

### Replacing "onchain" and "on-chain" (context-aware)

The word "onchain" hides what we actually mean. It is a category label, not a benefit. Always replace it with the specific attribute of the app or system being described. Pick the substitution that matches the claim being made:

| Underlying claim             | Use this language                                                                       |
| ---------------------------- | --------------------------------------------------------------------------------------- |
| Integrity / can't be altered | tamperproof, tamperproof by the network, integrity enforced across the nodes           |
| Availability                 | unstoppable, stays online if any node or cloud underneath fails, always available       |
| Where it runs                | end-to-end on the network, on a frontier cloud, served and computed by the network      |
| Independence                 | sovereign, sovereign by design, no single operator can change or pull the app           |
| Verifiability                | verifiable, every change replicated and verified by the network                         |
| Data persistence             | data replicated across the nodes, no data loss across upgrades                          |
| Governance                   | governance enforced by the network, tamperproof governance                              |

**Examples:**

- "Build onchain apps" becomes "Build tamperproof apps on a frontier cloud" (the user benefit is integrity, not the venue).
- "Fully on-chain frontend" becomes "Frontend served end-to-end by the network" (the claim is about where it runs).
- "On-chain governance" becomes "Tamperproof governance" or "Governance enforced by the network" (the claim is about who can change the rules).
- "Your assets stay on-chain" becomes "Your assets stay tamperproof and replicated across the nodes" (the claim is about integrity and durability).
- "24/7 on-chain" as a stat label becomes "Always available" or "Tamperproof" (pick whichever attribute the surrounding stat is paired with).

**When the technical fact matters**: deep developer docs may need to say "runs on the Internet Computer" or "hosted by canisters on the network." Still avoid the bare word "onchain" as a noun or selling point.

### Do / don't pairs (long form)

When rewriting legacy crypto-era copy, use these five rewrites as a reference. The "don't" column is the old voice we are leaving behind; the "do" column is where we are going.

1. **Don't:** "Get ready to revolutionize the next-gen decentralized future of Web3." **Do:** "Run your app end-to-end on a network instead of a single cloud. The app stays tamperproof and online whether the nodes run on AWS, Google Cloud, Azure, a local cloud, or bare metal."
2. **Don't:** "Deploy your dapp to our bleeding-edge blockchain and start building the future." **Do:** "Build and deploy your app by asking Caffeine, the ICP-native AI builder, or any other agent (Claude, Perplexity, Codex) using the ICP skill."
3. **Don't:** "Enterprise-grade security you can trust. Our team works 24/7 to keep your apps safe." **Do:** "You do not need a security team for apps that run on the network. The code is tamperproof by the network, not by a dashboard."
4. **Don't:** "Stay ahead of evolving cyber threats with our advanced protection." **Do:** "AI is now on both sides of every attack. Apps running on the Internet Computer remove most of what attackers target: no server to break into, no OS to patch, no secrets file to leak. Every change to the running code is replicated and verified by the network, so nothing can be altered silently."
5. **Don't:** "The platform for autonomous, always-on AI agents." **Do:** "The frontier cloud for agents building apps, services, and systems. What they ship stays tamperproof, keeps its data across upgrades, and stays online without anyone tending it."

## Proper nouns

- **Internet Computer** (two words, both capitalised). **ICP** in short form.
- **DFINITY** in all caps.
- **NNS** (Network Nervous System). Expand on first use.
- **Motoko**, **Rust**, **Candid**. Capitalised.
- **Chain-key**, not "chainkey".
- **Tamperproof** is one word, never hyphenated, never two words.
- `icp` CLI in lowercase code font. Never `dfx`.

## Copy review checklist

Before merging any ICP / DFINITY copy change, confirm:

- [ ] Describes ICP in line with the positioning section above ("Sovereign frontier cloud. Scaling AI that builds.")
- [ ] No em-dashes anywhere (the U+2014 character)
- [ ] No banned vocabulary on top-of-funnel surfaces
- [ ] No bare "onchain" or "on-chain". Replaced with the specific attribute (tamperproof, unstoppable, sovereign, end-to-end on the network)
- [ ] "Tamperproof" written as one word, never "tamper-proof" or "tamper proof"
- [ ] Sentence case on headlines, body, page titles. UPPERCASE only on Inter eyebrows and small CTA labels.
- [ ] No hype words (revolutionize, unlock, paradigm shift, etc.)
- [ ] No emoji, no exclamation marks
- [ ] Italic used only for asides, captions, attributions, or a single heading emphasis word. Never italic for stress in body copy.
- [ ] Subject of security sentences is the network, not DFINITY
- [ ] Proper nouns correct (DFINITY, Internet Computer, ICP, NNS, Motoko)
- [ ] CLI references use `icp`, never `dfx`

If any box is unchecked, the copy is not on brand.

## When in doubt

Defer to the **ICP Brand Guidelines v2** site (link in `Resources`) and the live `internetcomputer.org` as the joint reference. If they disagree, the brand guide wins because it has been edited for consistency. If this skill and the brand guide disagree, the brand guide wins and this skill should be updated.

## Versioning

This skill follows semantic versioning at the brand level.

- **Major** (v2, v3, ...): a new verbal system. Locked positioning, voice attributes, or vocabulary core changes. Existing copy may need rewriting.
- **Minor** (v2.1, v2.2, ...): a refinement to the current system. New rule, corrected example, sharpened do/don't pair, vocabulary clarification. Existing copy remains valid; the change clarifies or sharpens.
- **Every edit to this skill bumps the minor version.** When you save a new version, update the version line at the top of the file and add a row to the Changelog section. Mirror the bump in the brand guide HTML (hero eyebrow, hero meta-row, footer changelog) and in the paired `icp-brand-design` skill so the version is consistent across all three.

## Changelog

- **v2.1** (2026-05-08). Italic emphasis rule clarified: italic word lands on the subject of the heading (the noun the line is about), never a verb, copula, article, or connector. Removal test added. Versioning rule introduced.
- **v2.0** (2026-05-08). Initial v2 release. Locked top line "Sovereign frontier cloud. Scaling AI that builds." Four voice attributes (Factual, Plain, Calm, Sovereign by math). Strict ban on bare "onchain" and "on-chain" as nouns, attributes, or selling points, with a context-aware replacement table. "Tamperproof" locked as one word. CLI references switched from `dfx` to `icp`. Em-dash ban (U+2014).

## Resources

- **Canonical brand guide v2**: the deployed HTML reference page (URL shared in conversation)
- **Reference site**: [internetcomputer.org](https://internetcomputer.org)
- **Paired skill**: `icp-brand-design` for colors, typography, layout, components, and accessibility.
- **Out of scope**: products with their own brand identity (OISY wallet, Caffeine, and any future ecosystem product that ships under its own verbal system).

## Examples

**Example 1. Writing a hero headline**

User: "Write the hero headline for the ICP.app landing page."

Response: Produce a Newsreader, sentence-case headline with one italicised emphasis word. No hyperbole, no "revolutionize", no em-dash. Example: "The frontier cloud your agents *actually* ship on." Pair with an Inter eyebrow above ("FOR AGENTS BUILDING APPS, SERVICES, SYSTEMS") and a JetBrains Mono metadata strip beneath if metrics belong on the page.

**Example 2. Reviewing release notes**

User: "Does this release note read on brand?"

Response: Walk the copy review checklist. Flag any em-dashes, hype words, "decentralized" or "smart contract" framing, and any bare "onchain". Rewrite security claims with the network as the subject. If the release notes are for a developer audience, allow "canister" without explanation but still avoid "onchain" as a category label.

**Example 3. Positioning a new page**

User: "How should we describe ICP on this new investor page?"

Response: Lead with the locked top line: "Sovereign frontier cloud. Scaling AI that builds." Then expand using the four positioning bullets in the long form section. Do not lead with "blockchain", "decentralized", "World Computer", or any reframe of the locked strap.
