# Security and Attack Vectors

> Source: [docs.sui.io/sui-stack/on-chain-primitives/randomness-onchain](https://docs.sui.io/sui-stack/on-chain-primitives/randomness-onchain)

---

## Composition attacks (abort-filtering)

Public functions that accept `Random` as a parameter enable abort-filtering attacks. An attacker can wrap the function in their own module and revert transactions that produce unfavorable outcomes.

### How the attack works

If a dice game exposes a `public` function:

```move
// INSECURE: public function accepting Random
public fun play_dice(guess: u8, r: &Random, ctx: &mut TxContext): Ticket { ... }
```

An attacker writes a wrapper that aborts on losing outcomes:

```move
public fun attack(guess: u8, r: &Random, ctx: &mut TxContext): Ticket {
    let t = dice::play_dice(guess, r, ctx);
    assert!(!dice::is_winner(&t), 0);
    t
}
```

The attacker only pays gas for failed attempts and keeps every winning ticket. Note: this attack works when `play_dice` always returns a ticket and never aborts on its own. If the function can abort independently, the attacker's wrapper cannot distinguish between an unfavorable outcome and an internal abort.

### Compiler protection

The Move compiler lints against `public` functions with `Random` as a parameter. Define randomness-consuming functions as private `entry` functions instead.

## PTB attacks

Even with private `entry` functions, programmable transaction blocks (PTBs) can enable attacks through command chaining. An attacker could call a randomness function, inspect the result using subsequent PTB commands, and abort if the outcome is unfavorable.

### Mitigation

Sui rejects PTBs containing commands other than `TransferObjects` or `MergeCoins` following a `MoveCall` that consumes `Random`. This prevents attackers from inspecting or acting on random outcomes within the same PTB.

## RandomGenerator state leakage

If `RandomGenerator` is passed as a `public` function argument, callers can predict outputs by serializing the generator's internal state with `bcs::to_bytes(&generator)`. Passing `RandomGenerator` to `public(package)` or private functions is acceptable for testing and in-package logic.

### Compiler protection

The compiler lints against `public` functions that accept `RandomGenerator` as a parameter. Always create the generator within the function that uses it via `r.new_generator(ctx)`, and pass it only to `public(package)` or private helper functions within the same package.

## Secure implementation patterns

### Entry function restrictions

Define all randomness-dependent functions as private `entry` functions to prevent external module composition:

```move
// SECURE: private entry function
entry fun roll_dice(r: &Random, ctx: &mut TxContext): Dice {
    let mut generator = r.new_generator(ctx);
    Dice { value: generator.generate_u8_in_range(1, 6) }
}
```

This prevents other modules from wrapping the function and selectively aborting.

### Two-step commit-reveal pattern

When the outcome of randomness must not be observable before a follow-up action completes, use a two-step pattern:

**Step 1:** The first transaction fetches a random value and stores it in an unreadable object.

```move
entry fun reveal_alternative2_step1(
    nft: AirDropNFT,
    r: &Random,
    ctx: &mut TxContext
) {
    destroy_airdrop_nft(nft);
    let mut generator = r.new_generator(ctx);
    let v = generator.generate_u8_in_range(1, 100);
    transfer::public_transfer(
        RandomnessNFT { id: object::new(ctx), value: v },
        ctx.sender(),
    );
}
```

**Step 2:** The second transaction reads the committed value and completes operations.

```move
public fun reveal_alternative2_step2(
    nft: RandomnessNFT,
    ctx: &mut TxContext
): MetalNFT {
    let RandomnessNFT { id, value } = nft;
    id.delete();
    let metal = if (value <= 10) GOLD
        else if (10 < value && value <= 40) SILVER
        else BRONZE;
    MetalNFT { id: object::new(ctx), metal }
}
```

The first step is a private `entry` function (consumes `Random`), while the second step can be `public` because it does not use randomness.

### Balanced gas usage

Ensure winning and losing execution paths consume approximately equal total gas (both compute and storage). If branches differ significantly in gas consumption, attackers can infer outcomes from gas usage without seeing the result. The success path should cost equal or more gas than the failure path.

To achieve balanced gas, either perform a simple standard update (e.g., set a bool flag) in the randomness function and claim the result object in a follow-up function, or create an equally sized object (e.g., a dynamic field) in the failure path.

For example, if a winning path creates three objects and a losing path creates one, the gas difference reveals the outcome. Gas values must be measured carefully and tested in each published environment before going live.
