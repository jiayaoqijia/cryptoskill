// Minimal ABIs: the read methods this project calls, plus the single write
// method it encodes calldata for without ever sending (`Voter.vote`).
// Struct field order transcribed directly from the official Vyper sources
// (velodrome-finance/sugar, contracts/{LpSugar,RewardsSugar,VeSugar}.vy) —
// Aerodrome is a fork of Velodrome and shares this tooling/deployment pattern.

// Voter is the source of truth for "which pools can receive votes at all" — its
// `pools` array only contains pools that had a gauge created for them (~1.8k),
// versus LpSugar's `all()` which scans literally every pool the factory has ever
// created (~28k, mostly long-tail pairs that were never gauged). Enumerating via
// Voter + isAlive is dramatically cheaper than paginating the whole factory.
// Every Aerodrome pool is itself an ERC20-like LP token exposing these directly —
// reading them straight from the pool avoids LpSugar's byAddress() entirely,
// which turned out to internally linear-scan up to 30,000 pools per lookup and
// reliably exceed a public RPC's default eth_call gas allowance.
export const POOL_ABI = [
  { type: "function", name: "symbol", stateMutability: "view", inputs: [], outputs: [{ type: "string" }] },
  { type: "function", name: "token0", stateMutability: "view", inputs: [], outputs: [{ type: "address" }] },
  { type: "function", name: "token1", stateMutability: "view", inputs: [], outputs: [{ type: "address" }] },
] as const;

export const VOTER_ABI = [
  // What one veNFT actually voted for. `poolVote` enumerates the pools it chose
  // (there is no length getter on this deployment, so the caller reads upward
  // until the call reverts), and `votes` gives the weight it put on each.
  // Together with `lastVoted` these three answer "what did this lock do last
  // Thursday" in a handful of eth_calls, without touching event logs — which
  // matters because a week of Base is ~300,000 blocks and public RPCs cap a
  // getLogs range far below that.
  {
    type: "function",
    name: "poolVote",
    stateMutability: "view",
    inputs: [{ type: "uint256" }, { type: "uint256" }],
    outputs: [{ type: "address" }],
  },
  {
    type: "function",
    name: "votes",
    stateMutability: "view",
    inputs: [{ type: "uint256" }, { type: "address" }],
    outputs: [{ type: "uint256" }],
  },
  {
    type: "function",
    name: "lastVoted",
    stateMutability: "view",
    inputs: [{ type: "uint256" }],
    outputs: [{ type: "uint256" }],
  },
  {
    type: "function",
    name: "length",
    stateMutability: "view",
    inputs: [],
    outputs: [{ type: "uint256" }],
  },
  {
    type: "function",
    name: "pools",
    stateMutability: "view",
    inputs: [{ type: "uint256" }],
    outputs: [{ type: "address" }],
  },
  {
    type: "function",
    name: "gauges",
    stateMutability: "view",
    inputs: [{ type: "address" }],
    outputs: [{ type: "address" }],
  },
  {
    type: "function",
    name: "isAlive",
    stateMutability: "view",
    inputs: [{ type: "address" }],
    outputs: [{ type: "bool" }],
  },
  // The one non-view entry in this file, and it is never called from here: it
  // exists so `encodeFunctionData` can build the bytes of a vote for the owner
  // of the veNFT to sign in their own wallet. This project holds no keys and
  // sends no transactions.
  //
  // The signature is not transcribed from documentation. Its selector,
  // 0x7ac09bf7, was checked against the deployed Voter's runtime bytecode on
  // Base mainnet, where it is present — alongside a control check that a
  // plausible four-argument variant and an invented function name are both
  // absent, so "found it in the bytecode" means something.
  {
    type: "function",
    name: "vote",
    stateMutability: "nonpayable",
    inputs: [
      { name: "_tokenId", type: "uint256" },
      { name: "_poolVote", type: "address[]" },
      { name: "_weights", type: "uint256[]" },
    ],
    outputs: [],
  },
] as const;

const LP_EPOCH_REWARD_COMPONENTS = [
  { name: "token", type: "address" },
  { name: "amount", type: "uint256" },
] as const;

const LP_EPOCH_COMPONENTS = [
  { name: "ts", type: "uint256" },
  { name: "lp", type: "address" },
  { name: "votes", type: "uint256" },
  { name: "emissions", type: "uint256" },
  { name: "bribes", type: "tuple[]", components: LP_EPOCH_REWARD_COMPONENTS },
  { name: "fees", type: "tuple[]", components: LP_EPOCH_REWARD_COMPONENTS },
] as const;

export const REWARDS_SUGAR_ABI = [
  {
    type: "function",
    name: "epochsByAddress",
    stateMutability: "view",
    inputs: [
      { name: "_limit", type: "uint256" },
      { name: "_offset", type: "uint256" },
      { name: "_address", type: "address" },
    ],
    outputs: [{ name: "", type: "tuple[]", components: LP_EPOCH_COMPONENTS }],
  },
] as const;

/**
 * VotingEscrow, the veAERO NFT contract itself.
 *
 * This replaces VeSugar's `byAccount`, which returned every lock an account
 * owns in one call but **reverts on a public RPC once an account holds enough
 * locks** — each lock in that struct carries its full vote list, so the
 * response outgrows what the node will return. Confirmed against
 * 0xbde0c70bdc242577c52dfad53389f82fd149ea5a (22 locks): `byAccount` reverts,
 * these four functions answer fine.
 *
 * Each one returns a single value, so the response size no longer depends on
 * how much an account has voted. `locked` reports a permanent lock as
 * `isPermanent = true` with `end = 0`; a fully withdrawn lock also has
 * `end = 0` but `isPermanent = false`, which is why the flag is read rather
 * than inferred from the timestamp.
 */
export const VOTING_ESCROW_ABI = [
  {
    type: "function",
    name: "balanceOf",
    stateMutability: "view",
    inputs: [{ name: "_owner", type: "address" }],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    type: "function",
    name: "ownerToNFTokenIdList",
    stateMutability: "view",
    inputs: [
      { name: "_owner", type: "address" },
      { name: "_index", type: "uint256" },
    ],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    type: "function",
    name: "balanceOfNFT",
    stateMutability: "view",
    inputs: [{ name: "_tokenId", type: "uint256" }],
    outputs: [{ name: "", type: "uint256" }],
  },
  {
    type: "function",
    name: "locked",
    stateMutability: "view",
    inputs: [{ name: "_tokenId", type: "uint256" }],
    outputs: [
      { name: "amount", type: "int128" },
      { name: "end", type: "uint256" },
      { name: "isPermanent", type: "bool" },
    ],
  },
] as const;
