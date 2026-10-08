---
name: run-a-mainnet-deploy-checklist
description: Use when broadcasting a contract deploy or upgrade to mainnet and you want a gated, ordered checklist that prevents wrong-chain, nonce-race and uninitialised-proxy mistakes.
---

# Run a mainnet deploy checklist

Mainnet deploys are irreversible and expensive. Work through this list in order, with the
broadcast last and every verification step reading real state back.

## Procedure

1. Freeze the artifact. Record the keccak of the deployed bytecode you intend to ship and diff
   it against what the build produces now.

       forge build
       sha256sum out/Vault.sol/Vault.json
       cast keccak $(forge inspect src/Vault.sol:Vault bytecode)

2. Confirm the target chain *before* signing anything.

       cast chain-id --rpc-url $RPC              # must be 1 for mainnet
       echo $RPC                                  # eyeball the URL, not an env var you assumed

3. Dry-run with a simulation and no broadcast; read the printed calldata and expected address.

       forge script script/Deploy.s.sol:Deploy --rpc-url $RPC --sender $DEPLOYER
       # read the "SIMULATION COMPLETE" output; no tx sent

4. Import the signer into a keystore and read it from the environment only. Never paste a
   private key into a shell command line, a chat, a log, or a repo.

       cast wallet import deployer --interactive   # prompts for the key, encrypts it
       export ETH_RPC="$RPC"; export DEPLOYER=0xYourDeployerAddress

5. Broadcast with `--slow` (one tx at a time, waits for each receipt) and `--verify`.

       forge script script/Deploy.s.sol:Deploy --rpc-url $ETH_RPC --sender $DEPLOYER \
         --account deployer --slow --broadcast --verify --verifier etherscan

6. Read state back: receipt status, code size, proxy implementation slot, and ownership.

       cast receipt $TX --json --rpc-url $ETH_RPC | jq -r '.status, .blockNumber'
       cast codesize $ADDR --rpc-url $ETH_RPC
       cast call $ADDR "owner()(address)" --rpc-url $ETH_RPC

7. Post-deploy: transfer ownership to the multisig/timelock, call `initialize()` exactly once
   if a proxy, renounce deployer-only roles, and publish the address + block + code hash.

## Pitfalls

- Broadcasting to the wrong chain because an env var was unset and the URL defaulted to a
  public testnet RPC. Re-check `cast chain-id` immediately before and after.
- Deploying an uninitialised proxy — the implementation is left open and anyone can call
  `initialize()` and take ownership. Initialise in the same broadcast or within the same block.
- No `--slow` causes nonce races when the script sends several txs; the second is dropped or
  replaced.
- Verifying with the wrong compiler settings produces a "does not match" result and an
  unverified contract on a live network.
- Forgetting to transfer ownership, leaving the EOA deployer in control of a production
  contract.

## Verification

    cast codesize $ADDR --rpc-url $ETH_RPC              # > 0
    cast call $ADDR "owner()(address)" --rpc-url $ETH_RPC   # == multisig
    curl -s ".../getsourcecode...&address=$ADDR" | jq -r '.result[0].Match'

Report tx hash, block, runtime code size, owner, and explorer verification status for each
deployed contract.
