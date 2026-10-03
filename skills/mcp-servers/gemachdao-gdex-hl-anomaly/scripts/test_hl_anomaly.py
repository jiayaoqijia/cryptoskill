"""Offline tests for hl_anomaly: the model's invariants, no network."""
import unittest

import hl_anomaly as H

H0 = 1_700_000_000_000
HOUR = 3600_000


def rows(premiums, fundings=None):
    fundings = fundings or [1.25e-5] * len(premiums)
    return [{"time": H0 + i * HOUR, "premium": str(p), "fundingRate": str(f)}
            for i, (p, f) in enumerate(zip(premiums, fundings))]


class Model(unittest.TestCase):
    def test_robust_z_ignores_one_past_spike(self):
        calm = [0.0001, -0.0001] * 50
        z_clean, *_ = H.robust_z(0.003, calm, H.FLOOR["premium"])
        z_spiked, *_ = H.robust_z(0.003, calm[:-1] + [0.05], H.FLOOR["premium"])
        self.assertGreater(z_spiked, 0.9 * z_clean)   # a mean/stdev baseline would drop below 1

    def test_floor_bounds_flat_history(self):
        z, _, scale = H.robust_z(1e-4, [0.0] * 100, H.FLOOR["premium"])
        self.assertEqual(scale, H.FLOOR["premium"])
        self.assertAlmostEqual(z, 2.0)

    def test_score_zero_at_threshold_and_monotonic(self):
        self.assertEqual(H.score(10.0, 10.0), 0.0)
        self.assertEqual(H.score(-9.0, 10.0), 0.0)
        self.assertLess(H.score(12, 10), H.score(20, 10))
        self.assertLessEqual(H.score(1e6, 10), 1.0)

    def test_premium_spike_fires_divergence(self):
        ps = [0.0001 * (1 if i % 2 else -1) for i in range(200)] + [0.02]
        ev, scored = H.detect_premium_funding("X", rows(ps), H0 + 200 * HOUR)
        self.assertTrue(scored)
        self.assertEqual([e["anomaly_category"] for e in ev if e["anomaly_category"] == "oracle_divergence"],
                         ["oracle_divergence"])
        self.assertEqual(ev[0]["detected_at"], (H0 + 200 * HOUR) // 1000)
        self.assertEqual(ev[0]["detected_at_utc"], H._iso(H0 + 200 * HOUR))

    def test_funding_inside_clamp_never_fires(self):
        ps = [0.0] * 200 + [0.0005]            # inside the band
        fs = [1.25e-5] * 200 + [0.01]          # absurd funding, but premium is in-band
        ev, _ = H.detect_premium_funding("X", rows(ps, fs), H0 + 200 * HOUR)
        self.assertNotIn("funding_extremity", [e["anomaly_category"] for e in ev])

    def test_funding_event_carries_premium(self):
        ps = [0.0] * 200 + [0.05] * 8
        fs = [1.25e-5] * 200 + [0.006] * 8
        ev, _ = H.detect_premium_funding("X", rows(ps, fs), H0 + 200 * HOUR)
        fe = [e for e in ev if e["anomaly_category"] == "funding_extremity"]
        self.assertTrue(fe)
        self.assertIn("premium_pct", fe[0])

    def test_short_history_not_scored(self):
        ev, scored = H.detect_premium_funding("X", rows([0.0] * 50 + [0.05]), H0 + 50 * HOUR)
        self.assertFalse(scored)
        self.assertEqual(ev, [])

    def test_delisted_zeros_are_missing_not_calm(self):
        r = rows([0.0001 * (1 if i % 2 else -1) for i in range(100)] + [0.0] * 50, [1e-5] * 100 + [0.0] * 50)
        _, scored = H.detect_premium_funding("X", r, H0 + 110 * HOUR)
        self.assertFalse(scored)

    def test_liquidity_detected_at_bar_close_spikes_only(self):
        bars = [{"t": H0 + i * HOUR, "v": "1000", "h": "1.01", "l": "1.0"} for i in range(100)]
        bars += [{"t": H0 + 100 * HOUR, "v": "1", "h": "1.01", "l": "1.0"},        # collapse
                 {"t": H0 + 101 * HOUR, "v": "500000", "h": "1.3", "l": "1.0"}]    # spike
        ev, scored = H.detect_liquidity("X", bars, 1, H0 + 100 * HOUR)
        self.assertTrue(scored)
        self.assertEqual([e["detected_at_utc"] for e in ev], [H._iso(H0 + 102 * HOUR)])


CONTRACT = {  # column -> type, per the downstream anomaly contract (v1.1 section 3a + v1.2)
    "anomaly_id": str, "entity_id": str, "entity_type": str, "chain": str, "anomaly_category": str,
    "anomaly_score": float, "detection_method": str, "model_version": str, "baseline_window": str,
    "observed_value": float, "expected_value": float, "detected_at": int, "evidence_ref": str,
    "summary": str}


class ContractShape(unittest.TestCase):
    def _events(self):
        ps = [0.0001 * (1 if i % 2 else -1) for i in range(200)] + [0.05] * 8
        fs = [1.25e-5] * 200 + [0.006] * 8
        ev, _ = H.detect_premium_funding("X", rows(ps, fs), H0 + 200 * HOUR)
        bars = [{"t": H0 + i * HOUR, "v": "1000", "h": "1.01", "l": "1.0"} for i in range(100)]
        bars += [{"t": H0 + 100 * HOUR, "v": "500000", "h": "1.3", "l": "1.0"}]
        lq, _ = H.detect_liquidity("X", bars, 1, H0 + 100 * HOUR)
        self.assertTrue(ev and lq)
        return ev + lq

    def test_every_contract_column_present_and_typed(self):
        for e in self._events():
            for col, typ in CONTRACT.items():
                self.assertIsInstance(e[col], typ, col)
            self.assertTrue(0 <= e["anomaly_score"] <= 100)
            self.assertEqual(e["detection_method"], "statistical")
            self.assertEqual(e["baseline_window"], "7d")

    def test_confidence_is_absent_not_faked(self):
        for e in self._events():
            self.assertNotIn("confidence", e)

    def test_observed_and_expected_come_from_the_named_metric(self):
        for e in self._events():
            self.assertEqual(e["observed_value"], e[e["observed_metric"]])
            self.assertEqual(e["expected_value"], e[H.EXPECTED[e["observed_metric"]]])

    def test_anomaly_id_stable_and_distinct(self):
        a, b = self._events(), self._events()
        self.assertEqual([e["anomaly_id"] for e in a], [e["anomaly_id"] for e in b])
        self.assertEqual(len({e["anomaly_id"] for e in a}), len(a))


if __name__ == "__main__":
    unittest.main()
