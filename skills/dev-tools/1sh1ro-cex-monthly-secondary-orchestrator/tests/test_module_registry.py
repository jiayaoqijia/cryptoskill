from __future__ import annotations

import sys
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from monthly_module_registry import MODULE_ORDER, MODULE_SOURCES, build_module_commands, canonical_name  # noqa: E402


class MonthlyModuleRegistryTests(unittest.TestCase):
    def test_aliases_and_sources(self) -> None:
        self.assertEqual(canonical_name("derivatives"), "deribit")
        self.assertEqual(set(MODULE_ORDER), set(MODULE_SOURCES))

    def test_commands_preserve_strict_month_contract(self) -> None:
        commands = build_module_commands("2026-06", Path("/tmp/modules"), "2026-06", 10)
        self.assertIn("--exact-history", commands["fig2"])
        self.assertEqual(commands["fig4"][commands["fig4"].index("--end-month") + 1], "2026-06")
        self.assertEqual(commands["deribit"][commands["deribit"].index("--month") + 1], "2026-06")


if __name__ == "__main__":
    unittest.main()
