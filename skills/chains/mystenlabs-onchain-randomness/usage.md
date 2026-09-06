# API and Usage Patterns

> Source: [docs.sui.io/sui-stack/on-chain-primitives/randomness-onchain](https://docs.sui.io/sui-stack/on-chain-primitives/randomness-onchain)

---

## Random object

The `Random` object is a shared object at reserved address `0x8`. It serves as the foundation for all onchain randomness operations on Sui.

- `Random` is immutable for transactions. Any attempt to modify it results in transaction failure.
- Pass `Random` as a reference (`&Random`) to functions that need randomness.

## RandomGenerator

`RandomGenerator` is a pseudorandom generator (PRG) created from `Random` within individual functions.

- Must be instantiated locally within the consuming module.
- Never pass `RandomGenerator` as a `public` function parameter. Passing it to `public(package)` or private functions is acceptable for testing and in-package logic.

## Move API

The `random.move` module provides the official APIs:

| Function | Description |
|----------|-------------|
| `new_generator(r: &Random, ctx: &mut TxContext): RandomGenerator` | Creates a new pseudorandom generator from the `Random` object. |
| `generate_bool(&mut generator): bool` | Generates a random boolean value. |
| `generate_u8(&mut generator): u8` | Generates a random `u8` value. |
| `generate_u16(&mut generator): u16` | Generates a random `u16` value. |
| `generate_u32(&mut generator): u32` | Generates a random `u32` value. |
| `generate_u64(&mut generator): u64` | Generates a random `u64` value. |
| `generate_u128(&mut generator): u128` | Generates a random `u128` value. |
| `generate_u256(&mut generator): u256` | Generates a random `u256` value. |
| `generate_u8_in_range(&mut generator, min: u8, max: u8): u8` | Generates a random `u8` within the specified inclusive range. |
| `generate_u16_in_range(&mut generator, min: u16, max: u16): u16` | Generates a random `u16` within the specified inclusive range. |
| `generate_u32_in_range(&mut generator, min: u32, max: u32): u32` | Generates a random `u32` within the specified inclusive range. |
| `generate_u64_in_range(&mut generator, min: u64, max: u64): u64` | Generates a random `u64` within the specified inclusive range. |
| `generate_u128_in_range(&mut generator, min: u128, max: u128): u128` | Generates a random `u128` within the specified inclusive range. |
| `generate_u256_in_range(&mut generator, min: u256, max: u256): u256` | Generates a random `u256` within the specified inclusive range. |
| `shuffle(&mut generator, &mut vector<T>)` | Shuffles a vector in place using Fisher-Yates algorithm. |
| `generate_bytes(&mut generator, num_of_bytes: u16): vector<u8>` | Generates a specified number of random bytes. |

## Basic implementation example

A dice roll function that generates a random value between 1 and 6:

```move
entry fun roll_dice(r: &Random, ctx: &mut TxContext): Dice {
    let mut generator = r.new_generator(ctx);
    Dice { value: generator.generate_u8_in_range(1, 6) }
}
```

Key points:
- The function is declared as `entry` (not `public`) to prevent composition attacks.
- `RandomGenerator` is created locally inside the function body.
- The `Random` object is passed by reference.

## TypeScript integration

Pass the `Random` object when calling randomness-consuming Move functions from TypeScript:

```typescript
const tx = new Transaction();
tx.moveCall({
    target: "${PACKAGE_ID}::example::roll_dice",
    arguments: [tx.object.random()]
});
```

Use `tx.object.random()` or `tx.object("0x8")` to reference the `Random` object at address `0x8`.

