from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import json
from pathlib import Path
from uuid import uuid4

from openclaw_trading_suite.adapters import (
    AdapterCallError,
    AdapterRegistry,
    AdapterType,
    call_with_healing,
)
from openclaw_trading_suite.db import SQLiteStore


@dataclass(frozen=True)
class OvernightResearchConfig:
    report_dir: Path
    report_date: str
    autonomy_level: str
    market_symbols: list[str]
    research_topics: list[str]
    strategy_focus: list[str]
    preferred_market_adapter: str | None = None
    preferred_news_adapter: str | None = None
    fallback_market_adapters: list[str] | None = None
    fallback_news_adapters: list[str] | None = None


def _utc_now() -> str:
    return datetime.now(UTC).isoformat()


def _build_report(
    cfg: OvernightResearchConfig,
    market_sections: list[str],
    topic_sections: list[str],
    hypothesis_sections: list[str],
) -> str:
    return "\n".join(
        [
            f"# While You Were Sleeping Report ({cfg.report_date})",
            "",
            f"- Autonomy Mode: `{cfg.autonomy_level}`",
            f"- Generated At (UTC): `{_utc_now()}`",
            "",
            "## Overnight Actions",
            "- Ran market condition checks on configured symbols.",
            "- Pulled lightweight international topic headlines.",
            "- Generated strategy-linked hypothesis ideas for review/testing.",
            "",
            "## Market Conditions",
            *market_sections,
            "",
            "## International Sentiment and News",
            *topic_sections,
            "",
            "## New/Updated Hypothesis Ideas",
            *hypothesis_sections,
            "",
            "## Suggested Next Session Priorities",
            "1. Validate top 1-2 hypotheses in paper mode before promotion.",
            "2. Re-check risk budgets for strategies impacted by overnight volatility.",
            "3. Queue challenger retrain if drift persists for two consecutive sessions.",
        ]
    )


def _default_adapter_name(registry: AdapterRegistry, adapter_type: AdapterType) -> str:
    names = registry.list_names(adapter_type)
    if not names:
        raise RuntimeError(f"no_adapter_registered_for_{adapter_type.value}")
    return names[0]


def run_overnight_research(
    cfg: OvernightResearchConfig,
    adapters: AdapterRegistry,
    store: SQLiteStore,
) -> Path:
    market_adapter_name = cfg.preferred_market_adapter or _default_adapter_name(
        adapters, AdapterType.MARKET_DATA
    )
    news_adapter_name = cfg.preferred_news_adapter or _default_adapter_name(adapters, AdapterType.NEWS)

    market_sections: list[str] = []
    market_items: list[dict[str, object]] = []
    for symbol in cfg.market_symbols:
        market_outcome = call_with_healing(
            registry=adapters,
            adapter_type=AdapterType.MARKET_DATA,
            preferred_name=market_adapter_name,
            fallback_names=cfg.fallback_market_adapters,
            retries_per_adapter=2,
            call_fn=lambda adapter, s=symbol: adapter.get_latest_quote(s),
        )
        quote = market_outcome.payload
        market_sections.append(
            f"- `{symbol}` last `{quote.get('last')}` (bid `{quote.get('bid')}` / ask `{quote.get('ask')}`)."
        )
        market_items.append(
            {
                "symbol": symbol,
                "quote": quote,
                "adapter": market_outcome.adapter_name,
            }
        )

    topic_sections: list[str] = []
    topic_items: list[dict[str, object]] = []
    for topic in cfg.research_topics:
        news_outcome = call_with_healing(
            registry=adapters,
            adapter_type=AdapterType.NEWS,
            preferred_name=news_adapter_name,
            fallback_names=cfg.fallback_news_adapters,
            retries_per_adapter=2,
            call_fn=lambda adapter, t=topic: adapter.get_headlines(t, limit=3),
        )
        headlines = news_outcome.payload
        topic_sections.append(f"### {topic}")
        for item in headlines:
            topic_sections.append(f"- {item.get('headline')} [{item.get('sentiment', 'unknown')}]")
        topic_items.append(
            {
                "topic": topic,
                "headlines": headlines,
                "adapter": news_outcome.adapter_name,
            }
        )

    hypothesis_sections = [
        f"- Focus `{focus}`: test a swing setup with strict invalidation and regime tag updates."
        for focus in cfg.strategy_focus
    ]

    report_body = _build_report(cfg, market_sections, topic_sections, hypothesis_sections)

    cfg.report_dir.mkdir(parents=True, exist_ok=True)
    report_path = cfg.report_dir / f"while-you-were-sleeping-{cfg.report_date}.md"
    report_path.write_text(report_body, encoding="utf-8")
    json_path = cfg.report_dir / f"while-you-were-sleeping-{cfg.report_date}.json"
    json_payload = {
        "report_date": cfg.report_date,
        "autonomy_level": cfg.autonomy_level,
        "generated_at": _utc_now(),
        "market_conditions": market_items,
        "topic_coverage": topic_items,
        "hypothesis_ideas": hypothesis_sections,
        "priorities": [
            "Validate top 1-2 hypotheses in paper mode before promotion.",
            "Re-check risk budgets for strategies impacted by overnight volatility.",
            "Queue challenger retrain if drift persists for two consecutive sessions.",
        ],
    }
    json_path.write_text(json.dumps(json_payload, indent=2, sort_keys=True), encoding="utf-8")

    store.insert_overnight_report(
        report_id=str(uuid4()),
        report_date=cfg.report_date,
        autonomy_level=cfg.autonomy_level,
        summary_md=report_body,
        created_at=_utc_now(),
    )
    return report_path


def run_overnight_research_safe(
    cfg: OvernightResearchConfig,
    adapters: AdapterRegistry,
    store: SQLiteStore,
) -> tuple[Path | None, str | None]:
    try:
        report_path = run_overnight_research(cfg, adapters, store)
        return report_path, None
    except AdapterCallError as exc:
        return None, f"adapter_failure: {exc}"
    except Exception as exc:
        return None, f"unexpected_failure: {type(exc).__name__}: {exc}"
