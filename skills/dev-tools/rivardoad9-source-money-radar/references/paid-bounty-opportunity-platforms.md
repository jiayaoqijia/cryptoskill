# Paid opportunity platforms — bounties, grants, hackathons (verified 10 Oct 2026)

Use when the ask is "cari yang bayar" and the money is NOT an SME client: bounties, grants,
hackathons, remote gigs. Companion to the SME lane in `SKILL.md` — same user, second funnel.
Everything below was pulled live from the platform's own API/pages on 10 Oct 2026, not from memory.

## Superteam Earn — the concrete one

- Region page: `https://superteam.fun/earn/regions/indonesia/` · FAQ: `/faq`, `/earn/faq`.
- **Live listings API** (the single most useful endpoint — do not scrape the site):

```bash
curl -s 'https://superteam.fun/api/listings?take=200' | python3 -c "
import json,sys
d=json.load(sys.stdin)
items=d.get('data') or d.get('listings') or d
print(len(items),'listings')
for i in items: print(i.get('type'), i.get('rewardAmount'), i.get('token'), i.get('agentAccess'), i.get('deadline'), i.get('title'))"
```

  Watch for: `type` (bounty / project / grant), `rewardAmount`, `token` (USDC / USDG / SKR),
  `deadline`, `agentAccess` (`HUMAN_ONLY` / `AGENT_ALLOWED` / `AGENT_ONLY`), and the submission
  count. The endpoint ignored every filter parameter tried — fetch all, filter in Python.
- **Judgement rule: rank by submission count, not by prize size.** On that date: 350 USDC feedback
  bounty had **133** submissions; 2 000 USDG content bounty 110; 1 000 USDC builder post 69; 500
  USDG X-content 43; 500 USDC thread 42; 500 USDC post 41; 500 USDG grow-rewards 20; 500 USDC video
  19; 250 SKR leaderboard 18; 1 800 USDG demo-day pitch 13; 2 000 USDG hackathon 12; 530 USDC
  vibeathon 9; a 2 500 USDG university track had **0**; a 4 000 USDC security-audit grant had 5.
  Reading: cheap + easy = saturated; expensive + real skill = empty. Send a beginner to the empty
  column, never to the crowd.
- Three money shapes: **bounty** (everyone competes, winners only), **project** (freelance, one
  applicant gets paid), **grant** (funding; usually members only). Commission is zero.
- Payment mechanics: submissions cannot be edited after sending; sponsor judges (brain trust
  steps in when a sponsor is unavailable); Superteam/Solana-sponsored listings pay via a payment
  form **within 7 days** and **KYC is mandatory**; external sponsors pay to the wallet linked to
  the Earn account, sometimes with their own invoice/KYC. Plagiarism > 15 % = disqualification,
  repeat = permanent ban. A team submits **once** and the money lands in **one wallet** — agree the
  split before submitting, not after.
- Reputation: 80/60/50 XP for 1st/2nd/3rd, but XP only registers once you are invited as a
  member/contributor — and some listings use the membership invite itself as the prize.
- **Grants are gated: The Touching Grass Fund (Indonesia)** pays up to 500 USDG (avg grant $427,
  6 recipients, ~1 week response) but **requires Superteam membership** first. Regional (Indonesia
  only). Also seen: Agentic Engineering Grants (200 USDG). So membership is the real unlock, and
  membership comes from winning something small first.
- Trust signals worth quoting: the Indonesia sponsor page reports **USD 678 055 paid** with a
  **100 % completion rate**.
- **Agent lane** (relevant when the user can direct agents but not code): register an agent via the
  API → `apiKey` + `claimCode`; agent-eligible listings can be submitted programmatically; the agent
  cannot KYC or sign a wallet, so a human claims at `superteam.fun/earn/claim/<claimCode>`. Reality
  check on that date: **1 of 21** open listings was agent-eligible. A real but thin lane, not a
  money printer.
- Cash-out: rewards are crypto on Solana → wallet → exchange → IDR, with KYC on both sides.
- Guardrails to state out loud: never pay to register or to "unlock a listing"; never use a joki
  (submission-for-hire) service; never share a seed phrase.

## Other Indonesian lanes verified the same day

| Lane | Where | Note |
|---|---|---|
| Superteam Indonesia community | `t.me/SuperteamId` | entry to the bounty funnel above |
| BlockDev | `blockdev.id`, `discord.gg/ATPAFDnu4U`, `t.me/blockdev_official` | free Web3 courses, active community |
| Indonesia Web3 Hackathon | `t.me/+YlJxW1ad2zlhZjBl` + Luma | 228 projects, 1 810 people, hosts Binance Academy / BNB Chain / Coinvestasi, Demo Day in Yogyakarta |
| IBM SkillsBuild National Hackathon | `hacktiv8.com/projects/ibm/hackathon` | Hacktiv8 × IBM × Komdigi |
| Xdemia AI Builder Challenge | registration 11–30 Oct 2026 | free, prizes up to Rp25 juta |
| NextDev 12 Telkomsel | 8 Oct – 9 Nov 2026 | AI-focused, has an academy track |

## How to place this lane for this user

- The value of a bounty here is **being seen working**, not the prize: it is the cheapest way to be
  in a room (or a leaderboard) where potential partners and employers already look, and it produces
  a public artefact. Frame it that way, and keep the SME outreach as the fast income lane.
- Fit filter: with basic English, English copywriting bounties are the wrong column. Prefer build,
  feedback, or operations bounties, and the Indonesian-local lanes.
- Niche to aim at: **AI × accounting/finance** (bookkeeping agents, reconciliation, reporting,
  compliance), not "become a Web3 dev".
- Target to set honestly: 3 submissions in 30 days, not "win something". Winning is a bonus.

## Creative contests and whitelist giveaways (X campaigns)

A different animal from a bounty: the entry is a post, the prize is usually a whitelist spot, and
nobody pays cash. Run the same EV filter before spending an evening on artwork.

1. **Price the prize, not the headline.** "22 GTD whitelist spots" is worth whatever the minted
   asset resells for. Pull the collection's real secondary price (see
   `agentic-wallet-ops/references/nft-bag-valuation-and-exit.md`) before treating it as a win. If
   the collection trades at cents, winning is a souvenir, not income — say that once, plainly.
2. **Odds = slots ÷ entrants.** Slots are published; entrants are not, so estimate from the
   account's reach and call it an estimate. 22 spots against a few hundred entries is a 5–10 %
   draw, and one or two entries put expected wins below 0.2. Not winning is the normal outcome,
   not evidence the work was bad; state the arithmetic instead of consoling or pushing harder.
3. **The submission step is the one people skip.** A campaign almost always makes the post count
   only if the link is submitted on its own page (waitlist/entry form), sometimes within a window,
   sometimes as a new post rather than a reply. Confirm the exact rule and the deadline from the
   campaign post before making anything, and check it again before calling an entry done.
4. **When the post has to come from the user's own account and no posting route exists, deliver
   the finished entry plus a one-tap path**: the caption with the required @mention and hashtag,
   the image/video file, and a prefilled `https://x.com/intent/post?text=<urlencoded caption>`
   link. Say plainly that it was not posted from here — a claimed post that does not exist is
   worse than a handoff.
5. **Track submissions, not wins.** Wins are a variable nobody controls; the number worth reporting
   back is how many entries were actually submitted and eligible.
