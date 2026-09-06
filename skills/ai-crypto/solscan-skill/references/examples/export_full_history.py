"""
Export full transfer/defi history for a wallet via Solscan export endpoints.

Export endpoints return CSV DIRECTLY (not async jobs). Max 5000 rows per call.
For wallets with more history, chunk by time window and concatenate.

Cost per export: ~200–400 CU (vs 5000 CU for equivalent paginated calls = ~15× cheaper).

Usage:
    SOLSCAN_API_KEY=... python export_full_history.py <wallet> transfer|defi <out_path> [days]

Examples:
    python export_full_history.py 5EMW...R transfer transfers.csv 30
    python export_full_history.py 5EMW...R defi defi.csv 90
"""
import asyncio, aiohttp, os, sys, time
from datetime import datetime

BASE = "https://pro-api.solscan.io/v2.0"
KEY = os.environ["SOLSCAN_API_KEY"]
HEADERS = {"token": KEY}

EXPORT_PATHS = {
    "transfer": "/account/transfer/export",
    "defi": "/account/defi/activities/export",
    "rewards": "/account/stake-rewards/export",
    "token_defi": "/token/defi/activities/export",
}

MAX_ROWS_PER_EXPORT = 5000
CHUNK_DAYS = 30  # start with 30-day windows, shrink if hitting 5000 row cap


async def fetch_export(session, path: str, params: dict) -> tuple[bytes, dict]:
    """Returns (csv_bytes, headers_dict). Raises on non-200."""
    async with session.get(f"{BASE}{path}", params=params) as r:
        r.raise_for_status()
        body = await r.read()
        return body, dict(r.headers)


async def export_slice(session, path: str, address: str, from_time: int, to_time: int) -> bytes:
    return (await fetch_export(session, path, {
        "address": address,
        "from_time": from_time,
        "to_time": to_time,
    }))[0]


def csv_row_count(body: bytes) -> int:
    lines = body.decode("utf-8", errors="replace").splitlines()
    return max(0, len(lines) - 1)  # minus header


async def export_full(kind: str, address: str, out_path: str, days: int):
    path = EXPORT_PATHS[kind]
    now = int(time.time())
    start = now - days * 86400

    async with aiohttp.ClientSession(headers=HEADERS) as session:
        # Check budget first
        async with session.get(f"{BASE}/monitor/usage") as r:
            usage = await r.json()
        remaining = usage["data"]["remaining_cus"]
        print(f"CU remaining: {remaining:,} / 150M")

        header_written = False
        total_rows = 0

        with open(out_path, "wb") as out:
            cursor = start
            while cursor < now:
                slice_end = min(cursor + CHUNK_DAYS * 86400, now)
                print(f"[{datetime.fromtimestamp(cursor).date()} → {datetime.fromtimestamp(slice_end).date()}] exporting…")

                body = await export_slice(session, path, address, cursor, slice_end)
                rows = csv_row_count(body)

                if rows >= MAX_ROWS_PER_EXPORT and (slice_end - cursor) > 86400:
                    # Hit cap — shrink window and retry this slice
                    print(f"  HIT {MAX_ROWS_PER_EXPORT} cap, shrinking window")
                    slice_end = cursor + max(1, (slice_end - cursor) // 2)
                    continue

                if rows > 0:
                    if header_written:
                        # skip first line (header)
                        nl = body.find(b"\n")
                        out.write(body[nl + 1:])
                    else:
                        out.write(body)
                        header_written = True
                    total_rows += rows
                    print(f"  +{rows} rows (total: {total_rows})")

                cursor = slice_end

        print(f"Done: {total_rows} rows → {out_path}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print(__doc__)
        sys.exit(1)
    addr, kind, out = sys.argv[1], sys.argv[2], sys.argv[3]
    days = int(sys.argv[4]) if len(sys.argv) > 4 else 30
    if kind not in EXPORT_PATHS:
        sys.exit(f"kind must be one of: {list(EXPORT_PATHS)}")
    asyncio.run(export_full(kind, addr, out, days))
