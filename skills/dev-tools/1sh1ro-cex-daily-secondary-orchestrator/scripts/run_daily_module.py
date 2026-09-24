#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from datetime import datetime
from pathlib import Path

from cex_daily_modules.base import json_default
from cex_daily_modules.registry import MODULES, MODULE_SOURCES, collect_module


ENGINE_PATH = Path(__file__).with_name("run_cex_daily_orchestrator.py")


def _load_engine():
    spec = importlib.util.spec_from_file_location("cex_daily_engine", ENGINE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load daily engine: {ENGINE_PATH}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def main() -> int:
    parser = argparse.ArgumentParser(description="Run one composable daily-report data module")
    parser.add_argument("--module", choices=sorted(MODULES), help="Module to collect")
    parser.add_argument("--date", help="Explicit target date YYYY-MM-DD")
    parser.add_argument("--out", type=Path, help="Optional JSON output path; stdout is always printed")
    parser.add_argument("--describe", action="store_true", help="Print module-to-source registry without collecting")
    args = parser.parse_args()

    if args.describe:
        print(json.dumps(MODULE_SOURCES, ensure_ascii=False, indent=2))
        return 0
    if not args.module or not args.date:
        parser.error("--module and --date are required unless --describe is used")

    target = datetime.strptime(args.date, "%Y-%m-%d").date()
    result = collect_module(args.module, _load_engine(), target).to_dict()
    payload = json.dumps(result, ensure_ascii=False, indent=2, default=json_default)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(payload + "\n", encoding="utf-8")
    print(payload)
    return 0 if result["status"] != "degraded" else 1


if __name__ == "__main__":
    raise SystemExit(main())
