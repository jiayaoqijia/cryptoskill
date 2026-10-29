# Wallet, Approvals and Execution Safety

DeFi risk is not only in the protocol. The investor's wallet, approvals and transaction path are part of the position.

## Wallet architecture

- Hardware wallet for long-term holdings; separate hot wallet for experimentation.
- A dedicated DeFi wallet, not the wallet that holds the main portfolio or NFTs.
- Multisig (Safe or equivalent) for size; threshold and signer independence.
- Seed phrase offline, never photographed, typed into a website or stored in a password manager.
- Test recovery before funding; verify the backup works.
- Separate wallets per chain/cluster when isolation matters.

## Site and front-end authenticity

- Use a bookmarked official domain, not a search result or DM link.
- Check the domain, TLS, official docs/social links and contract address against the protocol's primary source.
- A branded front end can be a clone. Compare the backend/RPC hosts with a pre-incident archive snapshot when possible.
- WalletConnect/AppKit session requests should match the expected domain and chain.
- Do not sign because a page says "verify", "unlock", "claim" or "support" asks.

## Transaction simulation

Before signing, decode:

- chain ID, to, value, calldata and function selector;
- spender/operator and allowance amount;
- `approve`, `increaseAllowance`, `permit`, `setApprovalForAll`;
- `transfer`, `transferFrom`, `safeTransferFrom`;
- proxy upgrade/admin calls;
- bridge deposit/mint and destination chain/address.

Simulate with a trusted RPC or wallet; check balance changes and approvals. A transaction that only signs a message cannot move funds; an approval or permit can.

## Approval hygiene

- Prefer exact allowances over unlimited; revoke unused approvals.
- Review Permit2 and signature-based approvals; they can outlive the UI.
- Never sign a blind `eth_sign`; use typed data only when the domain and message are understood.
- Check spender address, not just the token symbol.
- Revoke approvals after exiting a position; monitor for new approvals.
- Treat "free mint", "airdrop claim" and "revoke" sites as phishing surfaces.

## RPC, MEV and execution

- Use a trusted RPC; public RPCs can be stale, censored or rate-limited.
- For large swaps, use MEV protection/private routing and limit slippage.
- Check gas, nonce, deadline and route; a failed tx still costs gas.
- For bridges, verify chain IDs, contract addresses, rate limits and destination address; test a small amount first.
- For loops/leverage, simulate the full sequence and the unwind; a single failed leg can trap the position.

## Operational controls

- Position caps per wallet, protocol and chain.
- Two-person approval for large transactions.
- A written emergency plan: pause, revoke, bridge back, exit, contact.
- Monitor wallet approvals, protocol admin actions and oracle deviations.
- Never share screen/seed with "support"; no legitimate support asks for a seed.
- The agent is read-only: it may prepare a plan, but never signs, approves, bridges, deposits or executes.

## Checklist

- [ ] Wallet type and seed backup verified.
- [ ] Official domain/contract checked against a primary source.
- [ ] Calldata, spender, allowance and destination decoded.
- [ ] Transaction simulated; balance changes understood.
- [ ] Approval amount and revocation plan set.
- [ ] RPC/MEV protection appropriate for size.
- [ ] Bridge/loop unwind path tested.
- [ ] Emergency contacts and caps written down.
