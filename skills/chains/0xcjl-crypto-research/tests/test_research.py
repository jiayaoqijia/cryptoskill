"""Behavioral regression coverage for evidence, math, immutable judgments and review windows."""
import copy
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from common import asset_key, ensure_runtime, instant, number
from collect import collect, compact_data, configure_transport, fetch_one, import_native, prepare, public_url, resolve_source
from ledger import audit, due, outcome, record_decision, record_erratum, record_review, summary
from metrics import candles, change, concentration, delta, depth
from research import doctor
import codex_step
from install import verify as verify_manifest

ASSET = {"chain": "ethereum", "native_id": "eth"}
BTC = {"chain": "bitcoin", "native_id": "btc"}
EVIDENCE = {"records": [{"evidence_id": "p1", "status": "ok", "url": "https://example.com/price"}]}
RAW = str(Path(__file__).resolve())  # any existing file stands in for a raw capture in synthetic fixtures


def source(**override):
    value = {"evidence_ref": "p1", "source_url": "https://example.com/price", "observed_at": "2025-12-31T23:50:00Z",
             "fetched_at": "2025-12-31T23:55:00Z", "raw_path": RAW}
    value.update(override)
    return value


def quote(price=100, at="2026-01-01T00:00:00Z", asset=None):
    return {"asset": asset or ASSET, "price": price, "currency": "USD", "observed_at": at,
            "venue": "fixture", "instrument": "BTCUSD" if asset == BTC else "ETHUSD", "evidence_refs": ["p1"]}


def safety(**states):
    rows = []
    for item in ("mint", "owner_privileges", "proxy_upgrade", "pause_blacklist", "tax", "sell_simulation", "lp_lock", "source_verified"):
        state = states.get(item, "not_applicable")
        row = {"item": item, "status": state}
        if state in {"checked_none_found", "confirmed_risk"}:
            row.update(evidence_refs=["p1"], method="fixture method")
        else:
            row["note"] = "fixture: native asset has no contract"
        rows.append(row)
    return rows


def decision(signal="BUY"):
    return {"decision_id": "eth-20260101", "authored_by": "model", "execution_agent": "test-model-fixture",
            "model": "fixture-only", "as_of": "2026-01-01T00:00:00Z", "asset": ASSET,
            "signal": signal, "risk": "high", "thesis": "Fixture, not a real investment judgment",
            "signal_window": "1 week", "valid_until": "2026-01-08T00:00:00Z", "invalidation_conditions": ["fixture invalidation"],
            "recheck_conditions": ["Fixture event"], "evidence_refs": ["p1"], "reference_quote": quote(),
            "assertions": [{"id": "event1", "condition": "Fixture event by horizon", "check_by": "2026-01-31T00:00:00Z", "evidence_refs": ["p1"]}],
            "safety_checks": safety(),
            "benchmark": {"asset": BTC, "reference_quote": quote(100, asset=BTC)},
            "data_cutoff": "2025-12-31T23:59:00Z", "analysis_completed_at": "2026-01-01T00:05:00Z",
            "claims": [{"claim_id": "c1", "text": "Fixture claim", "label": "fact", "sources": [source()]}],
            "review_objections": [{"id": "o1", "source": RAW, "objection": "Fixture objection",
                                   "disposition": "retained", "retention_reason": "Fixture reason"}]}


class MetricsTests(unittest.TestCase):
    def test_unknown_zero_and_nan(self):
        self.assertIsNone(number(None))
        self.assertEqual(number(0), 0)
        self.assertIsNone(change(0, 5))
        self.assertAlmostEqual(change(100, 110), 10)
        with self.assertRaises(ValueError): number("nan")
        with self.assertRaises(ValueError): instant("2026-01-01")

    def test_address_case(self):
        self.assertEqual(asset_key({"chain": "base", "address": "0x" + "A" * 40}),
                         asset_key({"chain": "base", "address": "0x" + "a" * 40}))
        self.assertNotEqual(asset_key({"chain": "solana", "address": "ABC"}),
                            asset_key({"chain": "solana", "address": "abc"}))
        with self.assertRaises(ValueError): asset_key({"chain": "ethereum", "address": "0xpool"})

    def test_sui_coin_identity(self):
        self.assertEqual(asset_key({"chain": "sui", "address": "0x2::sui::SUI"}), "sui:native:sui")
        self.assertEqual(asset_key({"chain": "sui", "address": "0xAb::m::C"}),
                         asset_key({"chain": "sui", "address": "0x" + "0" * 62 + "ab::m::C"}))
        self.assertNotEqual(asset_key({"chain": "sui", "address": "0xab::m::C"}),
                            asset_key({"chain": "sui", "address": "0xab::m::c"}))
        with self.assertRaises(ValueError): asset_key({"chain": "sui", "address": "0x" + "a" * 64})
        self.assertEqual(asset_key(ASSET), "ethereum:native:eth")

    def test_read_only_chain_probes(self):
        self.assertEqual(resolve_source({"kind": "rpc", "url": "https://example.com", "params": {"method": "eth_chainId"}})[2]["method"], "eth_chainId")
        with self.assertRaises(ValueError): resolve_source({"kind": "rpc", "url": "https://example.com", "params": {"method": "eth_sendRawTransaction"}})
        url, _, body = resolve_source({"kind": "sui-checkpoint"})
        self.assertEqual(url, "https://graphql.mainnet.sui.io/graphql")
        self.assertTrue(body["query"].startswith("query { checkpoint"))
        with tempfile.TemporaryDirectory() as tmp:
            with patch("collect.request", return_value=(b'{"errors":[{"message":"bad field"}]}', "application/json")):
                result = fetch_one({"id": "sui", "kind": "sui-checkpoint"}, Path(tmp))
            self.assertEqual(result["status"], "error")
            self.assertTrue(Path(result["raw_path"]).exists())

    def test_concentration_exclusions_and_sample(self):
        data = {"chain": "solana", "total_supply": 1000, "holders": [
            {"address": "Pool", "balance": 500, "exclude": True, "label_source": "https://example.com"},
            {"address": "Alice", "balance": 200}, {"address": "Bob", "balance": 100}]}
        result = concentration(data)
        self.assertEqual(result["raw_top10_pct"], 80)
        self.assertEqual(result["adjusted_top10_pct"], 60)
        self.assertEqual(result["coverage"], "partial")
        del data["holders"][0]["label_source"]
        with self.assertRaises(ValueError): concentration(data)

    def test_no_fabricated_history(self):
        data = {"instrument": "fixture", "interval": "1d", "candles": [
            {"time": f"2026-01-{i:02d}T00:00:00Z", "close": i} for i in range(1, 16)]}
        result = candles(data)
        self.assertIsNone(result["sma_20"])
        self.assertEqual(result["rsi14_wilder"], 100)
        data["candles"].reverse()
        with self.assertRaises(ValueError): candles(data)

    def test_depth_partial_book_not_executable(self):
        result = depth({"quote_amount": 10000, "bids": [[99, 1]], "asks": [[101, 1]]})
        self.assertIsNone(result["buy_vwap"])
        self.assertIsNone(result["roundtrip_quote_return_pct"])

    def test_snapshot_comparability(self):
        a = {"asset": ASSET, "observed_at": "2026-01-01T00:00:00Z",
             "metrics": {"holders": {"value": 100, "unit": "addresses", "scope": "chain"}}}
        b = copy.deepcopy(a)
        b["observed_at"] = "2026-01-02T00:00:00Z"
        b["metrics"]["holders"]["value"] = 120
        self.assertEqual(delta({"before": a, "after": b})["metrics"]["holders"]["delta"], 20)
        b["metrics"]["holders"]["scope"] = "pool"
        with self.assertRaises(ValueError): delta({"before": a, "after": b})


class EvidenceTests(unittest.TestCase):
    def test_transport_invalid_types_raise_validation_error(self):
        with tempfile.TemporaryDirectory() as folder, patch.dict("os.environ", {}, clear=True):
            path = Path(folder) / "transport.json"
            for settings in ([], {"trusted_proxy_ip": None, "trusted_public_hosts": ["example.com"]},
                             {"trusted_proxy_ip": "198.18.0.1", "trusted_public_hosts": [123]}):
                path.write_text(json.dumps(settings))
                with self.assertRaises(ValueError): configure_transport(Path(folder))

    def test_platform_proxy_requires_exact_ip_and_named_host(self):
        env = {"CRYPTO_RESEARCH_PROXY_IP": "198.18.0.1", "CRYPTO_RESEARCH_PROXY_HOSTS": "api.dexscreener.com"}
        with patch.dict("os.environ", env, clear=True):
            with patch("collect.socket.getaddrinfo", return_value=[(2, 1, 6, "", ("198.18.0.1", 443))]):
                self.assertEqual(public_url("https://api.dexscreener.com/"), "https://api.dexscreener.com/")
                with self.assertRaises(ValueError): public_url("https://unknown.example.com/")
            for ip in ("127.0.0.1", "10.0.0.1", "169.254.169.254", "198.18.0.2"):
                with patch("collect.socket.getaddrinfo", return_value=[(2, 1, 6, "", (ip, 443))]):
                    with self.assertRaises(ValueError): public_url("https://api.dexscreener.com/")

    def test_bad_proxy_configuration_is_rejected(self):
        with patch.dict("os.environ", {"CRYPTO_RESEARCH_PROXY_IP": "127.0.0.1", "CRYPTO_RESEARCH_PROXY_HOSTS": "api.dexscreener.com"}, clear=True):
            with self.assertRaises(ValueError): public_url("https://api.dexscreener.com/")
        with patch.dict("os.environ", {"CRYPTO_RESEARCH_PROXY_IP": "198.18.0.1", "CRYPTO_RESEARCH_PROXY_HOSTS": "*.com"}, clear=True):
            with self.assertRaises(ValueError): public_url("https://api.dexscreener.com/")

    def test_doctor_reports_network_degradation(self):
        with patch("research.request", side_effect=ValueError("Non-public address refused")):
            report = doctor(True)
        self.assertEqual(report["status"], "degraded")
        self.assertEqual(report["network"]["dexscreener"]["reason"], "Non-public address refused")

    def test_rpc_read_only(self):
        with self.assertRaises(ValueError): resolve_source({"kind": "rpc", "url": "https://example.com", "params": {"method": "eth_sendTransaction"}})

    def test_private_url_and_credentials(self):
        with self.assertRaises(ValueError): public_url("http://example.com")
        with self.assertRaises(ValueError): public_url("https://example.com?api_key=x")
        with patch("collect.socket.getaddrinfo", return_value=[(2, 1, 6, "", ("127.0.0.1", 443))]):
            with self.assertRaises(ValueError): public_url("https://example.com")

    def test_cache_preserves_original_timestamp(self):
        with tempfile.TemporaryDirectory() as folder:
            source = {"id": "one", "kind": "dex-search", "params": {"query": "ETH"}, "cache_ttl": 3600}
            with patch("collect.request", return_value=(b'{"pairs": []}', "application/json")) as req:
                first = fetch_one(source, Path(folder))
                second = fetch_one({**source, "id": "two"}, Path(folder))
            self.assertEqual(req.call_count, 1)
            self.assertEqual(first["retrieved_at"], second["retrieved_at"])
            self.assertTrue(second["cache_hit"])
            self.assertIsNone(first["observed_at"])

    def test_errors_do_not_become_zero_data(self):
        with tempfile.TemporaryDirectory() as folder:
            with patch("collect.request", side_effect=TimeoutError()):
                result = collect({"target": "ETH", "sources": [{"id": "p", "kind": "dex-search", "params": {"query": "ETH"}}]}, Path(folder))
            self.assertEqual(result["records"][0]["status"], "error")
            self.assertNotIn("data", result["records"][0])
            self.assertEqual(len(result["gaps"]), 1)

    def test_native_dedup_preserves_provenance(self):
        native = import_native({"records": [{"evidence_id": "x1", "url": "https://x.com/a/status/1",
            "retrieved_at": "2026-01-01T00:00:00Z", "content": "actual captured post", "tool": "x.search_posts_all"}]})
        two = {**native[0], "evidence_id": "x2", "url": "https://x.com/b/status/2"}
        result = prepare({"records": native}, [two])
        self.assertEqual(result["records"][1]["duplicate_of"], "x1")
        self.assertEqual(result["records"][1]["url"], "https://x.com/b/status/2")
        with self.assertRaises(ValueError): import_native({"records": [{"evidence_id": "bad", "url": "https://x.com"}]})


class LedgerTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def test_immutable_due_and_hash_chain(self):
        original = record_decision(decision(), EVIDENCE, self.root)
        self.assertEqual(len(due(self.root, "2026-01-30T23:59:59Z")), 0)
        self.assertEqual(len(due(self.root, "2026-01-31T00:00:00Z")), 1)
        with self.assertRaises(ValueError): record_decision(decision(), EVIDENCE, self.root)
        self.assertEqual(audit(self.root)["entries"], 1)
        path = self.root / "judgments.jsonl"
        path.write_text(path.read_text().replace('"high"', '"low"'))
        with self.assertRaises(ValueError): audit(self.root)

    def test_separate_direction_relative_and_no_watch_win(self):
        original = record_decision(decision(), EVIDENCE, self.root)
        review = {"horizon_days": 30, "reviewed_at": "2026-01-31T01:00:00Z",
                  "quote": quote(110, "2026-01-31T00:00:00Z"),
                  "benchmark_quote": quote(120, "2026-01-31T00:00:00Z", BTC)}
        result = outcome(original, review, EVIDENCE)
        self.assertTrue(result["direction_hit"])
        self.assertFalse(result["relative_direction_hit"])
        self.assertAlmostEqual(result["excess_return_pp"], -10)
        original["signal"] = "WATCH"
        self.assertIsNone(outcome(original, review, EVIDENCE)["direction_hit"])
        original["signal"] = "SELL"
        self.assertFalse(outcome(original, review, EVIDENCE)["direction_hit"])

    def test_pending_retry_complete_idempotency(self):
        record_decision(decision(), EVIDENCE, self.root)
        review = {"decision_id": "eth-20260101", "horizon_days": 30, "authored_by": "model",
                  "execution_agent": "test-fixture", "model": "unknown", "reviewed_at": "2026-01-31T01:00:00Z",
                  "assessment": "Fixture review", "status": "pending_data", "data_gap": "No quote", "benchmark_gap": "No benchmark"}
        record_review(review, EVIDENCE, self.root)
        self.assertEqual(len(due(self.root, "2026-01-31T02:00:00Z")), 1)
        review.update(status="complete", quote=quote(90, "2026-01-31T00:00:00Z"),
                      benchmark_quote=quote(100, "2026-01-31T00:00:00Z", BTC),
                      assertion_results=[{"id": "event1", "status": "unknown"}])
        record_review(review, EVIDENCE, self.root)
        self.assertEqual(len(due(self.root, "2026-01-31T02:00:00Z")), 0)
        self.assertEqual(summary(self.root)["groups"]["30d_BUY"]["n"], 1)
        with self.assertRaises(ValueError): record_review(review, EVIDENCE, self.root)

    def test_future_stale_wrong_asset_and_unsourced(self):
        value = decision()
        value["reference_quote"]["observed_at"] = "2025-12-31T23:00:00Z"
        with self.assertRaises(ValueError): record_decision(value, EVIDENCE, self.root)
        value = decision()
        value["evidence_refs"] = ["missing"]
        with self.assertRaises(ValueError): record_decision(value, EVIDENCE, self.root)
        original = record_decision(decision(), EVIDENCE, self.root)
        review = {"horizon_days": 30, "reviewed_at": "2026-01-31T00:00:00Z", "quote": quote(110, "2026-02-05T00:00:00Z")}
        with self.assertRaises(ValueError): outcome(original, review, EVIDENCE)

    def test_missing_benchmark_cannot_close_temporary_gap(self):
        record_decision(decision(), EVIDENCE, self.root)
        review = {"decision_id": "eth-20260101", "horizon_days": 30, "authored_by": "model",
                  "execution_agent": "fixture", "model": "unknown", "reviewed_at": "2026-01-31T01:00:00Z",
                  "assessment": "Missing benchmark", "status": "complete", "quote": quote(110, "2026-01-31T00:00:00Z"),
                  "assertion_results": [{"id": "event1", "status": "unknown"}]}
        with self.assertRaises(ValueError): record_review(review, EVIDENCE, self.root)
        review["benchmark_gap"] = "Temporarily unavailable"
        with self.assertRaises(ValueError): record_review(review, EVIDENCE, self.root)
        review["status"] = "pending_data"
        review["data_gap"] = "Benchmark unavailable"
        record_review(review, EVIDENCE, self.root)
        self.assertEqual(len(due(self.root, "2026-01-31T02:00:00Z")), 1)
        review["status"] = "complete"
        review["final_data_unavailable_reason"] = "Fixture permanent loss of source"
        record_review(review, EVIDENCE, self.root)
        self.assertEqual(summary(self.root)["groups"]["30d_BUY"]["relative_not_evaluable"], 1)

    def test_changed_venue_or_instrument_not_scored(self):
        original = record_decision(decision(), EVIDENCE, self.root)
        endpoint = quote(10000, "2026-01-31T00:00:00Z")
        review = {"horizon_days": 30, "reviewed_at": "2026-01-31T01:00:00Z", "quote": endpoint}
        endpoint["venue"] = "unrelated-illiquid-pool"
        with self.assertRaises(ValueError): outcome(original, review, EVIDENCE)
        endpoint["venue"] = "fixture"
        endpoint["instrument"] = "wrapped-ETHUSD"
        with self.assertRaises(ValueError): outcome(original, review, EVIDENCE)
        review["quote"] = quote(110, "2026-01-31T00:00:00Z", BTC)
        with self.assertRaises(ValueError): outcome(original, review, EVIDENCE)


class EvidenceGateTests(unittest.TestCase):
    """0.1.3: claim-level provenance, separated times, and the review-objection release gate."""
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def test_missing_claim_fields_rejected(self):
        for field in ("source_url", "observed_at", "fetched_at", "raw_path"):
            value = decision()
            del value["claims"][0]["sources"][0][field]
            with self.assertRaisesRegex(ValueError, field): record_decision(value, EVIDENCE, self.root)
        value = decision()
        value["claims"][0]["sources"][0]["observed_at"] = None
        with self.assertRaisesRegex(ValueError, "observed_at_unknown_reason"): record_decision(value, EVIDENCE, self.root)
        value["claims"][0]["sources"][0]["observed_at_unknown_reason"] = "Source gives no data time"
        record_decision(value, EVIDENCE, self.root)
        value = decision()
        value["decision_id"] = "raw-missing"
        value["claims"][0]["sources"][0]["raw_path"] = str(self.root / "absent.json")
        with self.assertRaisesRegex(ValueError, "raw_path"): record_decision(value, EVIDENCE, self.root)
        value = decision()
        del value["claims"]
        with self.assertRaisesRegex(ValueError, "claims"): record_decision(value, EVIDENCE, self.root)
        self.assertEqual(audit(self.root)["entries"], 1)

    def test_cutoff_and_completion_are_separate_and_ordered(self):
        for field in ("data_cutoff", "analysis_completed_at"):
            value = decision()
            del value[field]
            with self.assertRaisesRegex(ValueError, field): record_decision(value, EVIDENCE, self.root)
        value = decision()
        value["claims"][0]["sources"][0]["fetched_at"] = "2026-01-01T00:03:00Z"  # fetched after cutoff/as_of
        with self.assertRaisesRegex(ValueError, "data_cutoff"): record_decision(value, EVIDENCE, self.root)
        value = decision()
        value["analysis_completed_at"] = "2025-12-31T23:59:30Z"
        with self.assertRaises(ValueError): record_decision(value, EVIDENCE, self.root)
        evidence = {"records": [{**EVIDENCE["records"][0], "retrieved_at": "2025-12-31T23:00:00Z"}]}
        with self.assertRaisesRegex(ValueError, "retrieved_at"): record_decision(decision(), evidence, self.root)
        self.assertEqual(audit(self.root)["entries"], 0)

    def test_unresolved_objection_blocks_record(self):
        value = decision()
        del value["review_objections"]
        with self.assertRaisesRegex(ValueError, "review_objections"): record_decision(value, EVIDENCE, self.root)
        value["review_objections"] = []
        with self.assertRaisesRegex(ValueError, "none_reason"): record_decision(value, EVIDENCE, self.root)
        value["review_objections"] = [{"id": "o1", "source": RAW, "objection": "LP lock is only inferred"},
                                      {"id": "o2", "source": RAW, "objection": "x", "disposition": "adopted", "summary_change": "y"}]
        with self.assertRaisesRegex(ValueError, "o1, o2"): record_decision(value, EVIDENCE, self.root)
        self.assertEqual(audit(self.root)["entries"], 0)
        value["review_objections"][0].update(disposition="adopted", summary_change="Downgraded to inference", ledger_change="Thesis says inferred")
        value["review_objections"][1].update(ledger_change="Thesis updated")
        record_decision(value, EVIDENCE, self.root)
        self.assertEqual(audit(self.root)["entries"], 1)

    def test_erratum_appends_without_touching_original(self):
        original = record_decision(decision(), EVIDENCE, self.root)
        errata_file = self.root / "errata.md"
        errata_file.write_text("fixture")
        item = {"erratum_id": "eth-20260101-e1", "target_decision_id": "eth-20260101", "authored_by": "executor",
                "execution_agent": "fixture", "model": "unknown", "errata_path": str(errata_file),
                "corrections": [{"id": "k1", "original_text": "a", "original_location": "report:1", "disposition": "corrected",
                                 "corrected_text": "b", "sources": [source()]}]}
        bad = copy.deepcopy(item)
        del bad["corrections"][0]["sources"][0]["fetched_at"]
        with self.assertRaisesRegex(ValueError, "fetched_at"): record_erratum(bad, self.root)
        bad = copy.deepcopy(item)
        bad["target_decision_id"] = "missing"
        with self.assertRaises(ValueError): record_erratum(bad, self.root)
        record_erratum(item, self.root)
        with self.assertRaises(ValueError): record_erratum(item, self.root)
        rows = [json.loads(line) for line in (self.root / "judgments.jsonl").read_text().splitlines()]
        self.assertEqual(rows[0], original)
        self.assertEqual(audit(self.root)["entries"], 2)
        self.assertEqual(due(self.root, "2026-01-31T00:00:00Z")[0]["errata"], ["eth-20260101-e1"])
        self.assertEqual(summary(self.root)["groups"]["30d_BUY"]["n"], 0)


class V014Tests(unittest.TestCase):
    """0.1.4: file:// sources, WATCH baseline tracking, four-state safety, manifest + codex step accounting."""
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def test_file_source_must_exist(self):
        value = decision()
        value["claims"][0]["sources"] = [source(source_url="file://" + RAW)]
        record_decision(value, EVIDENCE, self.root)
        value = decision(); value["decision_id"] = "eth-20260101-b"
        value["claims"][0]["sources"] = [source(source_url="file:///nonexistent/x.json")]
        with self.assertRaisesRegex(ValueError, "must exist"): record_decision(value, EVIDENCE, self.root)

    def test_watch_requires_baseline_and_events_or_explicit_gap(self):
        for field, gap in (("reference_quote", "baseline_gap"), ("assertions", "no_assertion_reason")):
            value = decision("WATCH"); value.pop(field)
            with self.assertRaisesRegex(ValueError, gap): record_decision(value, EVIDENCE, self.root)
            value[gap] = "fixture: no tradable venue"
            value["decision_id"] = f"eth-20260101-{field[:3]}"
            record_decision(value, EVIDENCE, self.root)
        value = decision("WATCH"); value["decision_id"] = "eth-20260101-w"; value["assertions"][0].pop("check_by")
        with self.assertRaisesRegex(ValueError, "check_by"): record_decision(value, EVIDENCE, self.root)

    def test_watch_review_is_evaluated_but_not_scored(self):
        record_decision(decision("WATCH"), EVIDENCE, self.root)
        review = {"decision_id": "eth-20260101", "horizon_days": 30, "authored_by": "model", "status": "complete",
                  "assessment": "fixture", "execution_agent": "fixture", "model": "fixture-only",
                  "reviewed_at": "2026-01-31T01:00:00Z", "quote": quote(90, "2026-01-31T00:00:00Z"),
                  "benchmark_quote": quote(100, "2026-01-31T00:00:00Z", BTC),
                  "assertion_results": [{"id": "event1", "status": "occurred", "evidence_refs": ["p1"]}]}
        row = record_review(review, EVIDENCE, self.root)
        self.assertEqual(row["outcome"]["price_status"], "evaluable")
        self.assertAlmostEqual(row["outcome"]["return_pct"], -10)
        self.assertIsNone(row["outcome"]["direction_hit"])
        self.assertFalse(row["outcome"]["counts_toward_hit_rate"])
        self.assertEqual(row["outcome"]["event_status"], "evaluable")
        groups = summary(self.root)["groups"]
        self.assertEqual(groups["WATCH_tracking"]["n_reviews"], 1)
        self.assertEqual(groups["WATCH_tracking"]["events"]["occurred"], 1)
        self.assertEqual(sum(groups[k]["n"] for k in groups if k != "WATCH_tracking"), 0)

    def test_safety_four_states(self):
        value = decision(); value.pop("safety_checks")
        with self.assertRaisesRegex(ValueError, "safety_checks"): record_decision(value, EVIDENCE, self.root)
        for bad in ({"status": "safe"}, {"status": "checked_none_found", "evidence_refs": [], "method": "x"},
                    {"status": "unverified", "note": ""}):
            value = decision(); value["safety_checks"][0] = {"item": "mint", **bad}
            with self.assertRaises(ValueError): record_decision(value, EVIDENCE, self.root)
        value = decision(); value["safety_checks"] = value["safety_checks"][1:]
        with self.assertRaisesRegex(ValueError, "missing required items: mint"): record_decision(value, EVIDENCE, self.root)
        value = decision(); value["safety_checks"] = safety(mint="confirmed_risk", tax="checked_none_found", sell_simulation="unverified")
        record_decision(value, EVIDENCE, self.root)
        self.assertEqual(audit(self.root)["entries"], 1)

    def test_template_lists_all_safety_items_with_valid_states(self):
        import re
        from ledger import SAFETY_ITEMS, SAFETY_STATES
        text = (Path(__file__).resolve().parents[1] / "references/templates.md").read_text(encoding="utf-8")
        rows = re.findall(r'\{"item": "([a-z_]+)", "status": "([a-z_]+)"', text)
        self.assertEqual({item for item, _ in rows}, set(SAFETY_ITEMS))
        self.assertTrue(all(state in SAFETY_STATES for _, state in rows))

    def test_supersedes_must_exist(self):
        value = decision(); value["supersedes"] = "missing"
        with self.assertRaisesRegex(ValueError, "supersedes"): record_decision(value, EVIDENCE, self.root)

    def test_manifest_pins_models_md_and_doctor_checks_it(self):
        package = Path(__file__).resolve().parents[1]
        self.assertIn("references/models.md", verify_manifest(package))
        self.assertEqual(doctor(False)["manifest"]["status"], "ok")
        import shutil
        copy_root = self.root / "pkg"
        shutil.copytree(package, copy_root, ignore=shutil.ignore_patterns("__pycache__"))
        (copy_root / "references/models.md").write_text("tampered", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Checksum mismatch: references/models.md"): verify_manifest(copy_root)

    def test_codex_step_has_no_bypass_and_parses_tokens(self):
        cmd = codex_step.build_cmd(Path("/tmp/x"), "m", "medium", "prompt")
        self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", cmd)
        self.assertIn("workspace-write", cmd)
        self.assertNotIn("dangerously", (Path(__file__).resolve().parents[1] / "references/models.md").read_text())
        lines = [json.dumps({"type": "turn.completed", "usage": {"input_tokens": 10, "cached_input_tokens": 4, "output_tokens": 3, "reasoning_output_tokens": 1}}),
                 "not json", json.dumps({"type": "turn.completed", "usage": {"input_tokens": 5, "output_tokens": 2}})]
        usage = codex_step.parse_usage("\n".join(lines))
        self.assertEqual((usage["input_tokens"], usage["output_tokens"], usage["total_tokens"]), (15, 5, 20))
        self.assertEqual(codex_step.parse_usage("no usage here"), "unknown")


if __name__ == "__main__":
    unittest.main()


class V015Tests(unittest.TestCase):
    """0.1.5: append-only review-run log; request-time fetched_at with seconds, HTTP Date and time_precision."""
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def cli(self, *extra):
        import subprocess
        script = Path(__file__).resolve().parents[1] / "scripts" / "research.py"
        done = subprocess.run([sys.executable, str(script), "review-log", "--runtime", str(self.root), *extra],
                              capture_output=True, text=True, check=True)
        return json.loads(done.stdout)

    def lines(self):
        return [json.loads(line) for line in (self.root / "review_runs.jsonl").read_text().splitlines()]

    def test_review_log_writes_when_nothing_due(self):
        result = self.cli("--agent", "fixture-agent")
        rows = self.lines()
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["run_outcome"], "none")
        self.assertEqual(rows[0]["due_ids"], [])
        self.assertEqual(rows[0]["model"], "unknown")
        self.assertEqual(rows[0]["execution_agent"], "fixture-agent")
        self.assertRegex(rows[0]["run_started_at"]["utc"], r"T\d{2}:\d{2}:\d{2}Z$")
        self.assertTrue(rows[0]["run_finished_at"]["bangkok"].endswith("+07:00"))
        self.assertIn(rows[0]["doctor_status"], {"local_ready", "degraded", "error"})
        self.assertEqual(result["review_runs_path"], str(self.root / "review_runs.jsonl"))

    def test_review_log_per_item_outcomes_and_append_only(self):
        record_decision(decision(), EVIDENCE, self.root)
        self.cli("--at", "2026-02-01T00:00:00Z", "--model", "fixture-model")
        first = (self.root / "review_runs.jsonl").read_text()
        self.cli("--at", "2026-02-01T00:00:00Z", "--outcome", "eth-20260101:30=reviewed", "--outcome", "nope:30=failed")
        rows = self.lines()
        self.assertTrue((self.root / "review_runs.jsonl").read_text().startswith(first))
        self.assertEqual(rows[0]["due_ids"], ["eth-20260101:30"])
        self.assertEqual(rows[0]["items"][0]["outcome"], "pending_data")
        self.assertFalse(rows[0]["items"][0]["outcome_reported"])
        self.assertEqual(rows[1]["items"][0]["outcome"], "reviewed")
        self.assertEqual(rows[1]["run_outcome"], "reviewed")
        self.assertTrue(any("not due" in e for e in rows[1]["errors"]))

    def test_review_log_records_due_failure(self):
        (self.root / "judgments.jsonl").write_text("{broken\n")
        self.cli()
        row = self.lines()[0]
        self.assertEqual(row["run_outcome"], "failed")
        self.assertTrue(any(e.startswith("due:") for e in row["errors"]))

    def test_fetch_records_request_time_and_http_date(self):
        def fake(url, headers=None, body=None, meta=None):
            meta.update(fetched_at="2026-01-01T00:00:01Z", http_date="Thu, 01 Jan 2026 00:00:01 GMT")
            return b'{"pairs": []}', "application/json"
        with patch("collect.request", side_effect=fake):
            row = fetch_one({"id": "a", "kind": "dex-search", "params": {"query": "ETH"}}, self.root)
        self.assertEqual(row["fetched_at"], "2026-01-01T00:00:01Z")
        self.assertEqual(row["http_date"], "Thu, 01 Jan 2026 00:00:01 GMT")
        self.assertEqual(row["time_precision"], "second")
        with patch("collect.request", return_value=(b'{"pairs": []}', "application/json")):
            row = fetch_one({"id": "b", "kind": "dex-search", "params": {"query": "BTC"}}, self.root)
        self.assertRegex(row["fetched_at"], r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
        self.assertIsNone(row["http_date"])

    def test_request_reads_date_header(self):
        import collect as module

        class Response:
            headers = {"Content-Type": "application/json", "Date": "Thu, 01 Jan 2026 00:00:02 GMT"}
            def read(self, n): return b"{}"
            def __enter__(self): return self
            def __exit__(self, *a): return False

        class Opener:
            def open(self, req, timeout): return Response()
        meta = {}
        with patch("collect.public_url", side_effect=lambda u: u), patch("collect.urllib.request.build_opener", return_value=Opener()):
            module.request("https://example.com/x", meta=meta)
        self.assertEqual(meta["http_date"], "Thu, 01 Jan 2026 00:00:02 GMT")
        self.assertRegex(meta["fetched_at"], r"T\d{2}:\d{2}:\d{2}Z$")

    def test_native_precision_and_ledger_accepts_new_fetched_at(self):
        rows = import_native({"records": [
            {"evidence_id": "m", "url": "https://x.com/a/status/1", "retrieved_at": "2026-01-01T00:00Z", "content": "c"},
            {"evidence_id": "s", "url": "https://x.com/a/status/2", "retrieved_at": "2026-01-01T00:00:05Z", "content": "c"},
            {"evidence_id": "f", "url": "https://x.com/a/status/3", "retrieved_at": "2026-01-01T00:00:05Z", "content": "c",
             "time_precision": "file_mtime"}]})
        self.assertEqual([r["time_precision"] for r in rows], ["minute", "second", "file_mtime"])
        with self.assertRaises(ValueError):
            import_native({"records": [{"evidence_id": "z", "url": "https://x.com/a", "retrieved_at": "2026-01-01T00:00:05Z",
                                        "content": "c", "time_precision": "hour"}]})
        evidence = {"records": [{"evidence_id": "p1", "status": "ok", "url": "https://example.com/price",
                                 "retrieved_at": "2025-12-31T23:55:00.400000Z", "fetched_at": "2025-12-31T23:55:00Z"}]}
        record_decision(decision(), evidence, self.root)
        bad = decision(); bad["decision_id"] = "eth-20260102"
        bad["claims"][0]["sources"][0]["time_precision"] = "hour"
        with self.assertRaises(ValueError):
            record_decision(bad, evidence, self.root)


class V016Tests(unittest.TestCase):
    """0.1.6: quick fact-check mode; no training-memory facts (fetched_at / this-run evidence enforcement)."""
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)

    def tearDown(self):
        self.temporary.cleanup()

    def filled(self, **override):
        from factcheck import skeleton
        value = skeleton("Project X raised $10M led by Fund Y", "bot", "X 情报", "fc-test-1")
        value.update(verdict="true", completed_at="2026-01-01T00:10:00Z", execution_agent="fixture", model="fixture-only",
                     evidence=[{"evidence_id": "e1", "source_url": "https://example.com/pr", "source_type": "primary",
                                "fetched_at": "2026-01-01T00:05:00Z", "data_time": None, "data_time_unknown_reason": "fixture",
                                "freshness": "this_run", "note": "fixture"}],
                     notes={"fact": [{"text": "fixture fact", "evidence_ids": ["e1"]}], "self_claim": [], "inference": [], "unknown": []})
        value.update(override)
        return value

    def cli(self, *args, check=True):
        import subprocess
        script = Path(__file__).resolve().parents[1] / "scripts" / "research.py"
        return subprocess.run([sys.executable, str(script), "factcheck", *args], capture_output=True, text=True, check=check)

    def test_skeleton_has_no_signal_and_nulls(self):
        out = json.loads(self.cli("new", "--claim", "Token Z lists on Binance", "--requested-by", "bot", "--id", "fc-a").stdout)
        self.assertEqual(out["record_type"], "factcheck")
        self.assertIsNone(out["verdict"])
        self.assertNotIn("signal", out)
        self.assertFalse((self.root / "factchecks").exists())

    def test_validate_good_and_finalize_append_only(self):
        from factcheck import finalize, validate
        self.assertEqual(validate(self.filled())["errors"], [])
        result = finalize(self.filled(), self.root)
        self.assertEqual(result["verdict_zh"], "属实")
        saved = json.loads(Path(result["factcheck_path"]).read_text())
        self.assertEqual(saved["status"], "final")
        self.assertNotIn("_template", saved)
        with self.assertRaises(ValueError):
            finalize(self.filled(), self.root)
        with self.assertRaises(ValueError):
            finalize(self.filled(factcheck_id="fc-test-2", supersedes="missing"), self.root)
        finalize(self.filled(factcheck_id="fc-test-2", supersedes="fc-test-1", verdict="partly_true"), self.root)
        self.assertFalse((self.root / "judgments.jsonl").exists())

    def test_rejects_signals_missing_fetch_and_memory_facts(self):
        from factcheck import validate
        self.assertTrue(validate(self.filled(signal="BUY"))["errors"])
        self.assertTrue(validate(self.filled(verdict="WATCH"))["errors"])
        bad = self.filled(); del bad["evidence"][0]["fetched_at"]
        self.assertTrue(any("fetched_at" in e for e in validate(bad)["errors"]))
        bad = self.filled(); bad["evidence"][0]["fetched_at"] = "2026-01-01T00:05Z"
        self.assertTrue(any("seconds" in e for e in validate(bad)["errors"]))
        bad = self.filled(); bad["notes"]["fact"] = [{"text": "from memory"}]
        self.assertTrue(validate(bad)["errors"])
        stale = self.filled(); stale["evidence"][0]["freshness"] = "stale"
        self.assertTrue(any("this run" in e for e in validate(stale)["errors"]))
        ok = self.filled(verdict="unverifiable", evidence=[], notes={"fact": [], "self_claim": [], "inference": [], "unknown": ["no source"]})
        self.assertEqual(validate(ok)["errors"], [])

    def test_cli_validate_exit_code(self):
        path = self.root / "fc.json"
        path.write_text(json.dumps(self.filled(verdict=None)))
        done = self.cli("validate", "--input", str(path), check=False)
        self.assertEqual(done.returncode, 2)

    def test_ledger_fact_requires_this_run_source_and_unverified_label(self):
        evidence = {"records": [{"evidence_id": "p1", "status": "ok", "url": "https://example.com/price", "retrieved_at": "2025-12-31T23:55:00Z"}]}
        bad = decision()
        bad["claims"].append({"claim_id": "c2", "text": "memory", "label": "fact",
                              "sources": [source(freshness="stale", evidence_ref="old-1", fetched_at="2025-11-01T00:00:00Z")]})
        with self.assertRaises(ValueError):
            record_decision(bad, evidence, self.root)
        good = decision()
        good["claims"].append({"claim_id": "c2", "text": "background", "label": "unverified", "unverified_reason": "model memory only"})
        good["claims"].append({"claim_id": "c3", "text": "older", "label": "inference",
                               "sources": [source(freshness="stale", evidence_ref="old-1", fetched_at="2025-11-01T00:00:00Z",
                                                  observed_at=None, observed_at_unknown_reason="fixture")]})
        row = record_decision(good, evidence, self.root)
        self.assertNotIn("validation_warnings", row)
        nounv = decision(); nounv["decision_id"] = "eth-x2"
        nounv["claims"].append({"claim_id": "c2", "text": "bg", "label": "unverified"})
        with self.assertRaises(ValueError):
            record_decision(nounv, evidence, self.root)

    def test_missing_pack_fetch_time_warns_and_old_records_still_audit(self):
        row = record_decision(decision(), EVIDENCE, self.root)
        self.assertTrue(row["validation_warnings"])
        # Simulate a historical 0.1.5 ledger record: audit re-checks only the hash chain, not new 0.1.6 rules.
        from ledger import append
        old = copy.deepcopy(decision()); old.update(decision_id="old-015", record_type="decision", skill_version="0.1.5",
                   due_at={"30": "2026-01-31T00:00:00Z", "90": "2026-04-01T00:00:00Z"})
        old["claims"] = [{"claim_id": "c1", "text": "legacy", "label": "fact", "sources": [{"source_url": "https://example.com"}]}]
        append(self.root, old)
        self.assertEqual(audit(self.root)["status"], "ok")
        self.assertIsInstance(due(self.root, "2026-06-01T00:00:00Z"), list)
