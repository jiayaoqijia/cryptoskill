# Inventory across layers (Mobile)

Run from the metamask-mobile repo root. Scope `ROOT` to the ticket/path (e.g. `app/components/UI/Perps`).

## Find sibling unit + CV pairs

```bash
ROOT="${ROOT:-app}"
python3 - <<PY
from pathlib import Path
root = Path("$ROOT")
for vt in sorted(root.rglob("*.view.test.tsx")):
    base = vt.name.replace(".view.test.tsx", "")
    unit = vt.parent / f"{base}.test.tsx"
    if unit.exists():
        print(f"{unit} | {vt}")
PY
```

Also list shallow screen units **without** CV (candidates for ADD CV):

```bash
# Heuristic: *.test.tsx next to a .tsx component, excluding *.view.test.tsx / *.integration.test.*
find "$ROOT" -name '*.test.tsx' ! -name '*.view.test.tsx' | head -200
```

## Integration

```bash
find "$ROOT" -name '*.integration.test.ts' -o -name '*.integration.test.tsx'
# Domain harnesses often live under tests/integration/
ls tests/integration 2>/dev/null | head
```

## E2E

Search Appium specs/page objects that mention the feature screen names / testIDs:

```bash
rg -l "FeatureName|ScreenName" tests/smoke-appium/ 2>/dev/null | head -50
```

Prefer existing Appium conventions for exact folders in this checkout.

## Count `it(` for metrics

```bash
python3 - <<'PY'
from pathlib import Path
import re, sys
paths = [Path(p) for p in sys.argv[1:]]
for p in paths:
    if not p.exists():
        continue
    n = len(re.findall(r"\bit\s*\(", p.read_text()))
    print(f"{n}\t{p}")
PY
```

## Coverage snapshot (diagnostic only)

Coverage does **not** decide deletes. Optional before/after for risk diagnosis — same commands as unit↔CV overlap reference.
