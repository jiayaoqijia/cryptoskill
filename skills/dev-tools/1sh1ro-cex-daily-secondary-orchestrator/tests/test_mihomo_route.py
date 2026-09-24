from __future__ import annotations

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from cex_daily_modules import mihomo_route  # noqa: E402


class MihomoRouteTests(unittest.TestCase):
    def test_route_prefix_only_matches_global_exchange_domains(self) -> None:
        self.assertEqual(mihomo_route.route_prefix_for_url("https://api.bybit.com/v5/market/time"), "BYBIT")
        self.assertEqual(mihomo_route.route_prefix_for_url("https://api.binance.com/api/v3/time"), "BINANCE")
        self.assertEqual(mihomo_route.route_prefix_for_url("https://fapi.binance.com/fapi/v1/time"), "BINANCE")
        self.assertEqual(mihomo_route.route_prefix_for_url("https://web3.binance.com/bapi/test"), "BINANCE")
        self.assertIsNone(mihomo_route.route_prefix_for_url("https://api.binance.us/api/v3/time"))
        self.assertIsNone(mihomo_route.route_prefix_for_url("https://notbinance.com/test"))

    def test_switches_and_restores_selector(self) -> None:
        calls = []

        def request(_socket, method, endpoint, payload=None):
            calls.append((method, endpoint, payload))
            if method == "GET" and endpoint == "/proxies/GLOBAL":
                put_targets = [c[2]["name"] for c in calls if c[0] == "PUT"]
                return {"now": put_targets[-1] if put_targets else "US", "all": ["US", "JP-Dedicated-B1-1"]}
            if method == "GET" and endpoint == "/proxies/JP-Dedicated-B1-1":
                return {"alive": True}
            return {}

        with tempfile.TemporaryDirectory() as tmpdir, patch.dict(
            os.environ,
            {
                "BYBIT_MIHOMO_MODE": "required",
                "BYBIT_MIHOMO_LOCK": str(Path(tmpdir) / "route.lock"),
            },
            clear=False,
        ), patch.object(mihomo_route, "_discover_socket", return_value=Path("/tmp/fake.sock")), patch.object(
            mihomo_route, "_controller_request", side_effect=request
        ):
            with mihomo_route.optional_mihomo_route("BYBIT") as status:
                self.assertTrue(status.active)
                self.assertEqual(status.proxy, "JP-Dedicated-B1-1")

        put_targets = [c[2]["name"] for c in calls if c[0] == "PUT"]
        self.assertEqual(put_targets, ["JP-Dedicated-B1-1", "US"])

    def test_auto_mode_falls_back_when_controller_is_missing(self) -> None:
        with patch.dict(os.environ, {"BYBIT_MIHOMO_MODE": "auto"}, clear=False), patch.object(
            mihomo_route, "_discover_socket", side_effect=RuntimeError("missing")
        ):
            with mihomo_route.optional_mihomo_route("BYBIT") as status:
                self.assertFalse(status.active)
                self.assertEqual(status.error, "missing")

    def test_required_mode_fails_when_controller_is_missing(self) -> None:
        with patch.dict(os.environ, {"BYBIT_MIHOMO_MODE": "required"}, clear=False), patch.object(
            mihomo_route, "_discover_socket", side_effect=RuntimeError("missing")
        ):
            with self.assertRaisesRegex(RuntimeError, "missing"):
                with mihomo_route.optional_mihomo_route("BYBIT"):
                    pass


if __name__ == "__main__":
    unittest.main()
