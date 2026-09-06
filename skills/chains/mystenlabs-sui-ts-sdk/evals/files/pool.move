module example::pool;

public struct Pool has key {
  id: UID,
  balance_x: Balance<X>,
  balance_y: Balance<Y>,
}

public fun swap<X, Y>(
  pool: &mut Pool,
  coin_in: Coin<X>,
  min_out: u64,
  clock: &Clock,
  ctx: &mut TxContext,
): Coin<Y> { ... }