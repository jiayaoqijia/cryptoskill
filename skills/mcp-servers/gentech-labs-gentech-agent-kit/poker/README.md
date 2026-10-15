# 🃏 DevFun Poker Agent — Tournament Mode

Daemon-based poker agent for DevFun Arena tournaments. Optimized for 20s action clocks with continuous polling.

## Files

| File | Purpose |
|------|---------|
| `tournament_daemon.py` | Continuous-loop daemon for fast-clock competitions |
| `optimization-guide.md` | Architecture decisions, restrictions, and improvement ideas |

## Key Design Decisions

- **Daemon over cron**: Continuous loop eliminates the ~4s gap between cron ticks
- **Adaptive polling**: 3s at a table, 8s in queue
- **Reasoning field**: Tournament API requires structured reasoning per action
- **Manual rebuy**: Tournament costs MON — daemon never auto-rebuys
- **PID file**: Prevents duplicate daemon instances

## Running

```bash
python3 poker/tournament_daemon.py &
kill $(cat /tmp/poker-tournament-s7.pid)
```
