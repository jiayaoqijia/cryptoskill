"""
Scheduler for weekly incremental registry rebuilds.

Runs the crawl+classify pipeline on a schedule, only fetching
subgraphs that were created/updated since the last sync.
Default interval: 1 week (168 hours).
"""

import asyncio
import signal
import sys
from datetime import datetime, timezone

from registry import build_registry, load_sync_state


async def run_incremental():
    """Run one incremental sync."""
    state = load_sync_state()
    last = state.get("last_sync_timestamp", 0)
    if last:
        dt = datetime.fromtimestamp(last, tz=timezone.utc)
        print(f"\nLast sync: {dt.isoformat()}")
    else:
        print("\nNo previous sync — running full crawl")

    await build_registry(incremental=last > 0, write_db=True)


async def scheduled_loop(interval_hours: float = 168):
    """Run incremental sync on a loop. Default: weekly (168h)."""
    print(f"Scheduler started: will sync every {interval_hours}h ({interval_hours/24:.0f} days)")
    print(f"Press Ctrl+C to stop\n")

    while True:
        try:
            start = datetime.now(timezone.utc)
            print(f"\n{'='*50}")
            print(f"Sync started at {start.isoformat()}")
            print(f"{'='*50}")

            await run_incremental()

            end = datetime.now(timezone.utc)
            elapsed = (end - start).total_seconds()
            print(f"\nSync completed in {elapsed:.0f}s")
            print(f"Next sync at {datetime.fromtimestamp(end.timestamp() + interval_hours * 3600, tz=timezone.utc).isoformat()}")

        except Exception as e:
            print(f"\nSync failed: {e}")
            import traceback
            traceback.print_exc()

        await asyncio.sleep(interval_hours * 3600)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--once", action="store_true", help="Run once then exit")
    parser.add_argument("--interval", type=float, default=168, help="Hours between syncs (default: 168 = 1 week)")
    args = parser.parse_args()

    if args.once:
        asyncio.run(run_incremental())
    else:
        asyncio.run(scheduled_loop(args.interval))
