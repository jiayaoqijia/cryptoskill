# Flagship Walkthrough: Vesting

Vesting is the canonical "first non-trivial validator" use case. It exercises the parts of the eUTxO model that beginners trip on — datum design, validity ranges, signer checks — without dragging in oracles, minting, or multi-step flows. This walkthrough is the recommended starting point for anyone scaffolding their first Cardano dApp.

## Spec

A vesting contract locks funds for a beneficiary until a deadline.

- **Owner** can always reclaim (clawback). This recovers funds if the beneficiary disappears or the parameters were wrong.
- **Beneficiary** can withdraw only after the deadline has passed. They sign the spending transaction and the transaction's validity range must start strictly after `lock_until`.

The datum carries `lock_until` (POSIX milliseconds), `owner` (28-byte verification key hash), and `beneficiary` (28-byte verification key hash). One script address hosts many independent vesting schedules; each UTxO at the address has its own datum.

The redeemer is unused: the validator inspects only the datum and the transaction context.

## On-chain (Aiken)

Source of truth: `../../docs/sources/cardano-use-case-templates/vesting/onchain/aiken/validators/vesting.ak`.

Datum shape:

```
pub type VestingDatum {
  lock_until: Int,
  owner: ByteArray,
  beneficiary: ByteArray,
}
```

Validator logic:

```
or {
  key_signed(tx.extra_signatories, datum.owner),
  and {
    key_signed(tx.extra_signatories, datum.beneficiary),
    valid_after(tx.validity_range, datum.lock_until),
  },
}
```

`key_signed` is a helper from `cocktail/vodka_extra_signatories`. `valid_after` is from `cocktail/vodka_validity_range` — it returns true when the transaction's validity-range lower bound is strictly greater than `lock_until`. The strictness matters: a weak inequality would let a tx exactly at the deadline through, which is a real-world surprise.

Build with `aiken build` from the project's `onchain/` directory. The resulting `plutus.json` exposes the validator with title `vesting.vesting.spend` (or similar — check the file after build).

## Off-chain by stack

The contract is identical across stacks. The off-chain code differs only in API.

### Mesh SDK

Source of truth: `../../docs/sources/cardano-use-case-templates/vesting/offchain/meshjs/vesting.ts`.

Patterns to lift into your scaffold:

- `applyParamsToScript(blueprint.validators[0].compiledCode, [], "JSON")` to get the compiled script CBOR.
- `serializePlutusScript({ code, version: "V3" }, undefined, NETWORK_ID)` to derive the script address.
- For the deposit (lock) transaction: `txOutInlineDatumValue(mConStr0([lockUntilMs, ownerVkh, beneficiaryVkh]))`.
- For the withdraw (unlock) transaction: `spendingPlutusScriptV3()`, `txIn`, `txInScript`, `txInRedeemerValue("")`, `txInInlineDatumPresent`, `txInCollateral`, `requiredSignerHash`. When the beneficiary withdraws past the deadline, also call `invalidBefore(lockShortSlot + 1)`.

Mesh quirk noted in the upstream code: do not pass an `evaluator` to `MeshTxBuilder` when running against Yaci DevKit. The default Blockfrost evaluator mis-parses Yaci's Ogmios response; Mesh's internal CPU estimator works.

### Evolution SDK

Source of truth: the complete `offchain/src/vesting.ts` in `references/layout-aiken-evolution.md` (Step 6), written for `@evolution-sdk/evolution`. The CF template's `evolutionsdk/vesting.ts` uses the older `@evolution-sdk/lucid` package; don't copy its API.

Patterns to lift:

- Script from the blueprint: `new PlutusV3.PlutusV3({ bytes: Bytes.fromHex(compiledCode) })`, and its address from `ScriptHash.fromScript(script)`.
- Inline datum: a `TSchema.Struct` with the Aiken fields in order, encoded with `Data.withSchema(...).toData(...)` and wrapped in `InlineDatum.InlineDatum`.
- Deposit: `newTx().payToAddress({ address, assets, datum }).build()`.
- Withdraw: `newTx().collectFrom({ inputs, redeemer }).attachScript({ script }).addSigner({ keyHash })`, plus `.setValidity({ from, to })` on the beneficiary path.

Evolution wraps the Effect library internally — the public API hides most of it, but you may occasionally see Effect types in advanced usage. See https://effect.website/ if you want to go deeper.

Time on Yaci DevKit: `setValidity` converts with the chain's `slotConfig`, so the layout's script builds a `Chain` from Ogmios's start time and era summaries. Use Evolution's `preview` or `preprod` chain on a public network.

### cardano-client-lib (Java)

Source of truth: `../../docs/sources/cardano-use-case-templates/vesting/offchain/ccl-java/Vesting.java`.

Patterns to lift:

- Load the script via `PlutusBlueprintLoader.loadBlueprint(plutusJson.toFile())` then `PlutusBlueprintUtil.getPlutusScriptFromCompiledCode(compiledCode, PlutusVersion.v3)`.
- Derive the script address with `AddressProvider.getEntAddress(plutusScript, network)`.
- Build the datum with `ConstrPlutusData.of(0, BigIntPlutusData.of(lockUntilMs), BytesPlutusData.of(ownerVkh), BytesPlutusData.of(beneficiaryVkh))`.
- Lock with `new Tx().payToContract(scriptAddress, Amount.ada(20), datum)`.
- Unlock with `ScriptTx().collectFrom(utxos, redeemer).attachSpendingValidator(plutusScript)` and `validFrom(slot - 5)` for clock-drift slack.

### PyCardano

CF did not ship a PyCardano implementation upstream. The implementation below is purpose-written for this skill. It targets PyCardano's `TransactionBuilder` and `BlockFrostChainContext` and follows the same datum / redeemer / validity-range shape as the other three.

Project layout (monorepo scaffold from `references/layout-aiken-pycardano.md`):

```
acme-dapp/
├── onchain/
│   └── plutus.json
└── offchain/
    └── src/
        └── acme_offchain/
            ├── blueprint.py       # already in the layout
            ├── chain.py           # already in the layout
            └── vesting.py         # NEW: the module below
```

#### `src/acme_offchain/vesting.py`

```python
# src/acme_offchain/vesting.py
#
# Vesting end-to-end on PyCardano. Mirrors the validator at
# docs/sources/cardano-use-case-templates/vesting/onchain/aiken/validators/vesting.ak.
#
# Datum: (lock_until_ms: int, owner_vkh: bytes, beneficiary_vkh: bytes).
# Validator: spend allowed if owner signed OR (beneficiary signed AND validity
# range strictly after lock_until).
#
# Run (after `aiken build`):
#   poetry run python -m acme_offchain.vesting lock --ada 5 --lock-in-seconds 60
#   poetry run python -m acme_offchain.vesting withdraw --as owner
#   poetry run python -m acme_offchain.vesting withdraw --as beneficiary

from __future__ import annotations

import argparse
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv
from pycardano import (
    Address,
    BlockFrostChainContext,
    Network,
    PaymentSigningKey,
    PaymentVerificationKey,
    PlutusData,
    PlutusV3Script,
    Redeemer,
    TransactionBuilder,
    TransactionOutput,
    UTxO,
    Unit,
    plutus_script_hash,
)

from acme_offchain.blueprint import get_validator
from acme_offchain.chain import get_context


VALIDATOR_TITLE = "vesting.vesting.spend"  # confirm against your plutus.json after `aiken build`


# ---------------------------------------------------------------------------
# Datum and redeemer
# ---------------------------------------------------------------------------

@dataclass
class VestingDatum(PlutusData):
    CONSTR_ID = 0
    lock_until: int       # POSIX milliseconds
    owner: bytes          # 28-byte VerificationKeyHash
    beneficiary: bytes    # 28-byte VerificationKeyHash


# Redeemer is unused by the validator; pass a Unit (Plutus equivalent of None).


# ---------------------------------------------------------------------------
# Key loading
# ---------------------------------------------------------------------------

@dataclass
class Party:
    name: str
    skey: PaymentSigningKey
    vkey: PaymentVerificationKey
    address: Address


def _load_party(name: str, env_prefix: str, network: Network) -> Party:
    """Load a payment key pair from .keys/<name>.skey (.vkey derived).

    The dev workflow generates per-party signing keys with
    `pycardano-cli` or `cardano-cli`; for this walkthrough we assume they
    sit under .keys/. The scaffolded project ignores .keys/ in .gitignore.
    """
    keys_dir = Path(os.environ.get(f"{env_prefix}_KEYS_DIR", ".keys"))
    skey_path = keys_dir / f"{name}.skey"
    if not skey_path.exists():
        raise FileNotFoundError(
            f"Missing {skey_path}. Generate dev keys with PaymentSigningKey.generate() "
            f"and save() — see docs/sources/pycardano/tutorial.rst."
        )
    skey = PaymentSigningKey.load(str(skey_path))
    vkey = PaymentVerificationKey.from_signing_key(skey)
    return Party(
        name=name,
        skey=skey,
        vkey=vkey,
        address=Address(payment_part=vkey.hash(), network=network),
    )


# ---------------------------------------------------------------------------
# Script address
# ---------------------------------------------------------------------------

def _script_and_address(network: Network) -> tuple[PlutusV3Script, Address]:
    validator = get_validator(VALIDATOR_TITLE)
    script: PlutusV3Script = validator.script
    return script, Address(payment_part=plutus_script_hash(script), network=network)


# ---------------------------------------------------------------------------
# Lock (deposit)
# ---------------------------------------------------------------------------

def lock_funds(
    ctx: BlockFrostChainContext,
    network: Network,
    owner: Party,
    beneficiary_vkh: bytes,
    ada_amount: int,
    lock_until_ms: int,
) -> str:
    """Lock `ada_amount` ADA at the vesting script with the given deadline."""
    _script, script_address = _script_and_address(network)
    datum = VestingDatum(
        lock_until=lock_until_ms,
        owner=bytes(owner.vkey.hash()),
        beneficiary=beneficiary_vkh,
    )

    builder = TransactionBuilder(ctx)
    builder.add_input_address(owner.address)
    builder.add_output(
        TransactionOutput(
            address=script_address,
            amount=ada_amount * 1_000_000,
            datum=datum,        # inline datum (Babbage+); see CIP-32
        )
    )

    signed_tx = builder.build_and_sign([owner.skey], change_address=owner.address)
    tx_id = ctx.submit_tx(signed_tx.to_cbor())
    print(f"LOCK ok. ada={ada_amount} lock_until_ms={lock_until_ms} tx={tx_id}")
    return tx_id


# ---------------------------------------------------------------------------
# Withdraw (unlock)
# ---------------------------------------------------------------------------

def _find_locked_utxo(ctx: BlockFrostChainContext, script_address: Address) -> UTxO:
    utxos = ctx.utxos(str(script_address))
    if not utxos:
        raise RuntimeError(f"No UTxOs at {script_address}; was the lock tx indexed?")
    # In a real app, filter by datum to pick the right schedule. For the
    # walkthrough we take the first.
    return utxos[0]


def withdraw_as_owner(
    ctx: BlockFrostChainContext,
    network: Network,
    owner: Party,
) -> str:
    """Owner clawback — works at any time."""
    script, script_address = _script_and_address(network)
    utxo = _find_locked_utxo(ctx, script_address)

    builder = TransactionBuilder(ctx)
    builder.add_script_input(utxo, script=script, redeemer=Redeemer(Unit()))
    builder.add_input_address(owner.address)  # for collateral + fees
    builder.add_output(TransactionOutput(owner.address, utxo.output.amount))
    builder.required_signers = [owner.vkey.hash()]

    signed_tx = builder.build_and_sign([owner.skey], change_address=owner.address)
    tx_id = ctx.submit_tx(signed_tx.to_cbor())
    print(f"WITHDRAW (owner) ok. tx={tx_id}")
    return tx_id


def withdraw_as_beneficiary(
    ctx: BlockFrostChainContext,
    network: Network,
    beneficiary: Party,
    lock_until_ms: int,
) -> str:
    """Beneficiary withdrawal — requires the chain time to be past lock_until."""
    script, script_address = _script_and_address(network)
    utxo = _find_locked_utxo(ctx, script_address)

    # Set the validity range so its lower bound is strictly after lock_until.
    # PyCardano's TransactionBuilder exposes `validity_start` (POSIX slot
    # number) and `ttl` (slot number). Converting POSIX ms to slot requires
    # the network's protocol parameters; on testnets the helper below works.
    # For Yaci DevKit, see the slot-alignment note in the Evolution section
    # above and adjust accordingly.
    now_slot = ctx.last_block_slot
    lock_slot = _posix_ms_to_slot(ctx, lock_until_ms)
    if now_slot <= lock_slot:
        raise RuntimeError(
            f"Chain slot {now_slot} has not passed lock_until slot {lock_slot} yet. "
            f"Wait for the deadline before withdrawing as beneficiary."
        )

    builder = TransactionBuilder(ctx)
    builder.add_script_input(utxo, script=script, redeemer=Redeemer(Unit()))
    builder.add_input_address(beneficiary.address)
    builder.add_output(TransactionOutput(beneficiary.address, utxo.output.amount))
    builder.required_signers = [beneficiary.vkey.hash()]
    builder.validity_start = lock_slot + 1   # strictly after the deadline
    builder.ttl = builder.validity_start + 200

    signed_tx = builder.build_and_sign([beneficiary.skey], change_address=beneficiary.address)
    tx_id = ctx.submit_tx(signed_tx.to_cbor())
    print(f"WITHDRAW (beneficiary) ok. tx={tx_id}")
    return tx_id


def _posix_ms_to_slot(ctx: BlockFrostChainContext, posix_ms: int) -> int:
    """Convert POSIX milliseconds to a slot number using the chain context.

    On preview/preprod/mainnet the era genesis params are well-known; on
    Yaci DevKit you must align the slot config (see the Evolution walkthrough
    for the technique). For the walkthrough we assume the network's
    `genesis` field on ctx is set; in production, cache the slot-length and
    system-start at startup rather than recomputing per call.
    """
    genesis = ctx.genesis_param
    system_start_sec = int(genesis.system_start)
    slot_length_sec = genesis.slot_length
    return (posix_ms // 1000 - system_start_sec) // slot_length_sec


# ---------------------------------------------------------------------------
# CLI runner
# ---------------------------------------------------------------------------

def main(argv: Optional[list[str]] = None) -> int:
    load_dotenv()
    parser = argparse.ArgumentParser(prog="vesting")
    subparsers = parser.add_subparsers(dest="cmd", required=True)

    lock_p = subparsers.add_parser("lock", help="Lock funds at the vesting script")
    lock_p.add_argument("--ada", type=int, default=5)
    lock_p.add_argument(
        "--lock-in-seconds",
        type=int,
        default=60,
        help="Seconds from now until the beneficiary can withdraw.",
    )

    wd_p = subparsers.add_parser("withdraw", help="Withdraw funds")
    wd_p.add_argument("--as", dest="role", choices=["owner", "beneficiary"], required=True)
    wd_p.add_argument(
        "--lock-until-ms",
        type=int,
        default=None,
        help="Required for --as beneficiary; the POSIX ms used when locking.",
    )

    args = parser.parse_args(argv)
    ctx = get_context()
    network = Network.TESTNET  # default to testnet; mainnet requires explicit opt-in

    owner = _load_party("owner", "OWNER", network)
    beneficiary = _load_party("beneficiary", "BENEFICIARY", network)

    if args.cmd == "lock":
        lock_until_ms = int(time.time() * 1000) + args.lock_in_seconds * 1000
        lock_funds(
            ctx=ctx,
            network=network,
            owner=owner,
            beneficiary_vkh=bytes(beneficiary.vkey.hash()),
            ada_amount=args.ada,
            lock_until_ms=lock_until_ms,
        )
        print(f"Remember to pass --lock-until-ms {lock_until_ms} to `withdraw --as beneficiary`.")
        return 0

    if args.cmd == "withdraw":
        if args.role == "owner":
            withdraw_as_owner(ctx=ctx, network=network, owner=owner)
        else:
            if args.lock_until_ms is None:
                print("Provide --lock-until-ms (from the lock step) so we can set validity range.", file=sys.stderr)
                return 2
            withdraw_as_beneficiary(
                ctx=ctx,
                network=network,
                beneficiary=beneficiary,
                lock_until_ms=args.lock_until_ms,
            )
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
```

#### Notes on the PyCardano implementation

- **Validator title.** After `aiken build`, the validator appears in `plutus.json` under a title like `vesting.vesting.spend`. Verify the exact string and update `VALIDATOR_TITLE` if needed; mismatched titles fail loudly at startup.
- **Inline datum.** Pass `datum=datum` (a `PlutusData` instance) on `TransactionOutput`. PyCardano serialises it inline (CIP-32) and the off-chain caller never needs to ship the datum on the spending tx.
- **Redeemer.** The validator ignores the redeemer; `Redeemer(Unit())` is the conventional placeholder.
- **Validity range.** `TransactionBuilder.validity_start` (in slot units) is the lower bound the on-chain `valid_after` check inspects. Set it to `lock_slot + 1` for strict-after semantics matching the validator.
- **Slot conversion.** `_posix_ms_to_slot` is a best-effort helper using the chain context's `genesis_param`. On Yaci DevKit the compressed eras shift the genesis; copy the slot-alignment technique from the Evolution section. A future PyCardano helper may handle this directly.
- **Collateral.** PyCardano's `TransactionBuilder` auto-selects collateral from `add_input_address`. The dev wallet must hold at least one pure-ADA UTxO of ~5 ADA for this to succeed.
- **Key files vs mnemonic.** The walkthrough uses `.skey` files generated and stored under `.keys/`. PyCardano can also derive keys from a mnemonic via its BIP32 module (`pycardano.crypto.bip32`); switch when integrating with a multi-account dev wallet.

## Frontend (Next.js + Mesh or Evolution + Blockfrost)

The frontend is the same shape regardless of which backend stack you picked. It does its own transaction building client-side and talks directly to Blockfrost. Wallet integration uses CIP-30 via Mesh or Evolution.

Three components:

1. **Wallet connect button.** Hand off to `connect-wallet` skill for the CIP-30 details. Mesh's `<CardanoWallet />` component is the fastest path; Evolution exposes `selectWallet.fromAPI(walletApi)`.
2. **Lock funds form.** Fields: beneficiary address (bech32), unlock deadline (datetime-local input → POSIX ms), ADA amount. On submit, build the lock tx client-side using the same patterns as the off-chain code above, sign through the wallet, submit via Blockfrost.
3. **Unlock funds button.** Visible only to the beneficiary (compare `wallet.getUsedAddresses()` against the datum's `beneficiary` field). Disabled until the deadline passes. On click, build the unlock tx with `invalidBefore` set strictly after the deadline.

Project layout: the frontend is a sibling Next.js App Router app. For TypeScript backends (Mesh/Evolution) it lives in the same monorepo and can share types via a small shared package. For Python/Java backends the frontend is its own Next.js app and reads the same `plutus.json` (committed under `onchain/`) for the validator hex.

```
acme-dapp/
├── onchain/
│   └── plutus.json
├── offchain/                    # TS / Python / Java backend
└── frontend/                    # Next.js App Router
    ├── package.json
    ├── app/
    │   ├── layout.tsx           # MeshProvider wrapper
    │   ├── page.tsx             # WalletButton + lock form + unlock list
    │   └── lib/
    │       ├── blueprint.ts     # imports ../../onchain/plutus.json
    │       └── tx.ts            # buildLockTx / buildUnlockTx
    └── .env.local.example       # NEXT_PUBLIC_BLOCKFROST_PROJECT_ID, NEXT_PUBLIC_NETWORK
```

Important Next.js notes (lifted from `connect-wallet`):

- CIP-30 needs `window`. Use `"use client"` and dynamic imports for any wallet-touching module.
- Don't expose your Blockfrost project ID as `NEXT_PUBLIC_*` if you can avoid it. Front the Blockfrost calls behind a small `/api/` route in Next.js so the project ID stays server-side. Wallet calls (sign / submit) remain client-side because the wallet has no server.

## End-to-end run

### On Yaci DevKit (fastest)

1. Start Yaci DevKit. Hand off to `setup-devnet` for the launch command.
2. Note the dev wallet mnemonic Yaci prints and copy it into `.env` as `DEV_WALLET_MNEMONIC`.
3. From `onchain/`: `aiken build` to emit `plutus.json`.
4. From your off-chain directory:
   - **Mesh:** `npm install`, then `npm run tx:lock` and `npm run tx:redeem`.
   - **Evolution:** same as Mesh, with the Evolution-specific scripts.
   - **PyCardano:** `poetry install`, then `poetry run python -m acme_offchain.vesting lock --ada 5 --lock-in-seconds 60`. Wait for the deadline, then `poetry run python -m acme_offchain.vesting withdraw --as beneficiary --lock-until-ms <value>`.
   - **cardano-client-lib:** `mvn -q exec:java -Dexec.mainClass=org.acme.offchain.vesting.Vesting`.
5. (Optional) Start the frontend with `npm run dev` from `frontend/`. Connect a browser wallet on the devnet network and exercise the lock / unlock UI.

### On preview testnet (closer to production)

1. Get a free Blockfrost project ID at https://blockfrost.io. Use a Preview-tier key.
2. Fund a testnet address at https://docs.cardano.org/cardano-testnets/tools/faucet (Preview).
3. Set `CARDANO_NETWORK=preview` and `BLOCKFROST_PROJECT_ID=<your key>` in `.env`.
4. Same `aiken build` and off-chain commands as above. Block times are slower (~20s); expect each step to take a block before confirming.

Never run this scaffold against mainnet. The validator has not been audited and bugs can lock real funds permanently.

## Where to go next

- Replace the unused redeemer with a tagged action (`Clawback` / `Beneficiary`) if you want a self-documenting on-chain trace. Bump `CONSTR_ID` accordingly.
- Add per-schedule fees by extending the datum with a `fee_pkh` and paying out to a third party on withdrawal.
- For multiple-beneficiary vesting (a typical employee-grant pattern), shift to a parameterised validator and emit one UTxO per beneficiary at lock time.
- Hand off to `write-validator` for richer on-chain logic, `build-transaction` for advanced off-chain flows, `review-contract` before deploying anything non-trivial.
