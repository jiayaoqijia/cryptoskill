#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path

from monthly_module_registry import (
    MODULE_ALIASES,
    MODULE_ORDER,
    MODULE_SOURCES,
    build_module_commands,
    canonical_name,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one monthly-report module")
    parser.add_argument("--module", choices=sorted(set(MODULE_ORDER) | set(MODULE_ALIASES)))
    parser.add_argument("--month", help="Target month YYYY-MM")
    parser.add_argument("--outdir", type=Path, help="Module output directory")
    parser.add_argument("--context-start", help="Optional chart context start month")
    parser.add_argument("--fig6-top-alt", type=int, default=10)
    parser.add_argument("--describe", action="store_true", help="Print module-to-source registry without collecting")
    args = parser.parse_args()

    if args.describe:
        print(json.dumps(MODULE_SOURCES, ensure_ascii=False, indent=2))
        return 0
    if not args.module or not args.month or args.outdir is None:
        parser.error("--module, --month, and --outdir are required unless --describe is used")

    name = canonical_name(args.module)
    packages_root = args.outdir.parent
    command = build_module_commands(
        args.month,
        packages_root,
        args.context_start or args.month,
        args.fig6_top_alt,
    )[name]
    out_index = command.index("--outdir") + 1
    command[out_index] = str(args.outdir)
    args.outdir.mkdir(parents=True, exist_ok=True)
    proc = subprocess.run(command, capture_output=True, text=True)
    (args.outdir / "run.log").write_text((proc.stdout or "") + "\n--- STDERR ---\n" + (proc.stderr or ""), encoding="utf-8")
    manifest = {
        "module": name,
        "month": args.month,
        "generated_at_utc": datetime.now(tz=timezone.utc).isoformat(),
        "status": "ok" if proc.returncode == 0 else "failed",
        "sources": MODULE_SOURCES[name],
        "exit_code": proc.returncode,
    }
    (args.outdir / "module_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
