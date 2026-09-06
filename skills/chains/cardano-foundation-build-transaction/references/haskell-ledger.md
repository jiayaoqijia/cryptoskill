# Haskell off-chain: Aiken + cardano-ledger + CHaP + haskell.nix

This is the node-adjacent Haskell path: validators in **Aiken**, transactions
in **cardano-ledger** types, built with **haskell.nix**. It is not Plinth
(Haskell-on-chain) and not Atlas.

Ground every snippet below in the bundled sources before changing it.

## When to pick this path

- The service is Haskell and must share types with the node (era `Tx`,
  Conway certs, phase-1 validation).
- Validators are already (or will be) Aiken and emit CIP-57 `plutus.json`.
- You need a reproducible Nix shell, not cabal on a system GHC.

Use `cardano-api` instead when you want a client façade over
ledger/consensus/network. Use Mesh / Evolution / PyCardano when the
team is not Haskell.

## Cabal: CHaP

From `docs/sources/chap/README.md`. Add the repository, then pin **both**
indexes (a second `index-state` stanza overrides the first entirely):

```cabal
repository cardano-haskell-packages
  url: https://chap.intersectmbo.org/
  secure: True
  root-keys:
    3e0cce471cf09815f930210f7827266fd09045445d65923e6d0238a6cd15126f
    443abb7fb497a134c343faf52f0b659bd7999bc06b7f63fa76dc99d631f9bea1
    a86a1f6ce86c449c46666bda44268677abf29b5b2d2eb5ec7af903ec2f117a82
    bcec67e8e99cabfa7764d75ad9b158d72bfacf70ca1d0ec8bc6b4406d1bf8413
    c00aae8461a256275598500ea0e187588c35a5d5d7454fb57eac18d9edb86a56
    d4a35cd3121aa00d18544bb0ac01c3e1691d618f462c46129271bccf39f7e8ee

index-state:
  , hackage.haskell.org      2022-12-31T00:00:00Z
  , cardano-haskell-packages 2022-08-25T00:00:00Z
```

Replace those timestamps with the `index-state` of the `cardano-node`
release you align to — do not ship the 2022 example dates. Run
`cabal update` once so cabal downloads the CHaP index.

`source-repository-package` always wins over CHaP and Hackage (CHaP README).
haskell.nix needs a `--sha256` comment on each such stanza
(`docs/sources/haskell-nix/tutorials/source-repository-hashes.md`).
Prefer nix32 hashes (`nix flake prefetch` then
`nix hash convert --to nix32`).

Typical `build-depends` (versions from CHaP at your `index-state`, not
from memory): `cardano-ledger-api`, `cardano-ledger-conway`,
`cardano-ledger-core`, `plutus-tx`, `plutus-ledger-api`.

## Nix: haskell.nix + CHaP + iohk-nix

From `docs/sources/chap/README.md` ("… with haskell.nix"):

1. Keep the CHaP stanza in `cabal.project`.
2. Flake input on the **`index-only`** branch (plan resolution only;
   haskell.nix fetches each package tarball by URL+sha256):

```nix
inputs.CHaP = {
  url = "github:intersectmbo/cardano-haskell-packages?ref=index-only";
  flake = false;
};
```

3. Map the CHaP URL into haskell.nix:

```nix
cabalProject {
  # ...
  inputMap = { "https://chap.intersectmbo.org/" = CHaP; };
}
```

4. Apply the iohk-nix overlays the CHaP README names so C libraries
   exist (`plutus-core` needs `libblst`): `crypto` and
   `haskell-nix-crypto`. Search `docs/sources/iohk-nix/`.

5. Update CHaP with `nix flake lock --update-input CHaP`.

Inside a haskell.nix shell, `cabal build` must **not** compile CHaP
packages from source (CHaP README). If it does, the `inputMap` or
overlays are wrong.

IOG cache (used by haskell.nix / Intersect flakes):

```nix
nixConfig.extra-substituters = [ "https://cache.iog.io" ];
nixConfig.extra-trusted-public-keys = [
  "hydra.iohk.io:f/Ea+s+dFdN+3Y/G+FDgSq+a5NEWhJGzdjvKNGv0/EQ="
];
```

## Aiken blueprint → ledger types

1. `aiken build` produces `plutus.json` (CIP-57). Search
   `docs/sources/aiken/` and `docs/sources/cips/` (CIP-57).
2. Read the validator's `compiledCode` (hex, single-wrapped CBOR of
   flat UPLC — the blueprint form, not the double-wrapped on-chain
   witness).
3. Attach it as a Conway script witness on the ledger `Tx`. Datums
   and redeemers are `plutus-tx` `ToData` values, not JSON.
4. Phase-1 checks (fees, min-UTxO, collateral, value conservation)
   live in `cardano-ledger`. Search `docs/sources/cardano-ledger/`.
5. Any Plutus spend still needs a pure-ADA collateral input.

Do not reconstruct the script hash by hand if the blueprint already
has it — compare, do not invent.

## Aligning to a cardano-node release

Pick the node version the service will talk to. Use that release's
CHaP pin (`flake.lock` `CHaP` input, or the node's `cabal.project`
`index-state`) so `cardano-ledger-*` / `plutus-*` versions match what
the node runs. Mismatched CHaP pins are the usual solver / iserv
failure.

## What not to do

- Teach cabal-on-system-GHC as this stack. The Nix path is haskell.nix.
- Default new Haskell services to Atlas or to Plinth validators.
- Paste CHaP `_sources/` or pin `?ref=repo` (downloads every tarball).
