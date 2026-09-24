# Workflow Notes

The bundled script uses the public Hyperliquid `info` endpoint:

- `clearinghouseState` for open positions, leverage, margin used, liquidation price
- `userFills` for recent fills and closed pnl
- `portfolio` for account-value and pnl history

## Style Inference Heuristics

- Repeated same-timestamp child fills usually mean one parent order or twap-style slicing.
- Very high leverage on majors with concentrated exposure suggests conviction momentum trading, not diversified risk budgeting.
- Large realized losses followed by immediate re-entry suggest stubbornness or aggressive reloading.
- Large open profit with tight liquidation distance means the trader is right now, but the follower still has poor entry quality if copying late.
- Empty current positions do not mean the trader is inactive overall; check recent fills and pnl history first.

## Good Questions To Answer

- `他现在到底押在哪边？`
- `这是趋势单还是抄顶抄底？`
- `最近是在加仓、止盈，还是被动止损？`
- `这个人适合学什么，不适合学什么？`

## Example

```bash
python3 skills/hyperliquid-public-trader-watch/scripts/fetch_trader_snapshot.py \
  --address 0x020ca66c30bec2c4fe3861a94e4db4a498a35872 \
  --name "Machi Big Brother"
```
