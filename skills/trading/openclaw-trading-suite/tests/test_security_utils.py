from openclaw_trading_suite.security import (
    load_secret_value,
    parse_secret_ref,
    redact_sensitive,
    redact_structure,
)


def test_redact_sensitive_masks_secret_like_pairs() -> None:
    text = "api_key=abcdef1234567890 token=supersecrettokenvalue"
    redacted = redact_sensitive(text)
    assert "abcdef1234567890" not in redacted
    assert "supersecrettokenvalue" not in redacted


def test_redact_structure_masks_secret_fields() -> None:
    payload = {"api_key": "secret-value", "nested": {"token": "abc", "ok": "yes"}}
    redacted = redact_structure(payload)
    assert redacted["api_key"] == "***"
    assert redacted["nested"]["token"] == "***"
    assert redacted["nested"]["ok"] == "yes"


def test_parse_secret_ref_supports_shorthand_and_json() -> None:
    shorthand = parse_secret_ref("openclaw:env:default:ALPACA_API_KEY")
    json_ref = parse_secret_ref('{"source":"file","provider":"default","id":"trading/alpaca"}')
    assert shorthand is not None
    assert shorthand.source == "env"
    assert json_ref is not None
    assert json_ref.provider == "default"


def test_load_secret_value_prefers_ref_over_plaintext(monkeypatch) -> None:
    monkeypatch.setenv("ALPACA_API_KEY", "plaintext-value")
    monkeypatch.setenv("ALPACA_API_KEY_REF", "openclaw:env:default:ALPACA_API_KEY")
    value, ref = load_secret_value("ALPACA_API_KEY")
    assert value is None
    assert ref is not None
    assert ref.source == "env"
