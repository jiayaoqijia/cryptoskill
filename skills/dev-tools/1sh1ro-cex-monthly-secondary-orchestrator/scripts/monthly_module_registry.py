from __future__ import annotations

from pathlib import Path
from typing import Dict, List


FIG2 = "~/.claude/skills/binance-fig2-top10-monthly-performance/scripts/build_fig2_top10_monthly_performance.py"
FIG3 = "~/.claude/skills/binance-fig3-defi-tvl-share/scripts/build_fig3_defi_tvl_share.py"
FIG4 = "~/.claude/skills/binance-fig4-monthly-nft-volume/scripts/build_fig4_monthly_nft_volume.py"
FIG6 = "~/.claude/skills/binance-fig6-altcoin-outside-top10-share/scripts/build_fig6_altcoin_outside_top10_share.py"
DERIBIT = "~/.claude/skills/deribit-monthly-secondary-metrics/scripts/build_deribit_monthly_metrics.py"
CORE = "./scripts/generate_cex_monthly_report.py"

MODULE_ORDER = ("fig2", "fig3", "fig4", "fig6", "deribit", "core_report")
MODULE_ALIASES = {
    "top-assets": "fig2",
    "defi": "fig3",
    "nft": "fig4",
    "concentration": "fig6",
    "derivatives": "deribit",
    "core": "core_report",
}
MODULE_SOURCES = {
    "fig2": ["CoinGecko /coins/markets", "CoinGecko /coins/{id}/market_chart/range"],
    "fig3": ["DefiLlama historicalChainTvl"],
    "fig4": ["CryptoSlam global sales web API"],
    "fig6": ["CoinMarketCap global historical", "CoinGecko market-cap history"],
    "deribit": ["Deribit get_funding_rate_history", "Deribit DVOL", "Deribit current OI with month-end gate"],
    "core_report": ["CoinMarketCap global historical", "Alternative.me F&G", "CoinGecko price history"],
}


def canonical_name(name: str) -> str:
    return MODULE_ALIASES.get(name, name)


def build_module_commands(
    month: str,
    packages_dir: Path,
    context_start: str,
    fig6_top_alt: int = 10,
) -> Dict[str, List[str]]:
    return {
        "fig2": ["python3", FIG2, "--month", month, "--exact-history", "--outdir", str(packages_dir / "fig2")],
        "fig3": ["python3", FIG3, "--start-month", context_start, "--end-month", month, "--outdir", str(packages_dir / "fig3")],
        "fig4": ["python3", FIG4, "--start-month", context_start, "--end-month", month, "--outdir", str(packages_dir / "fig4")],
        "fig6": [
            "python3", FIG6, "--start-month", context_start, "--end-month", month,
            "--top-alt", str(fig6_top_alt), "--outdir", str(packages_dir / "fig6"),
        ],
        "deribit": ["python3", DERIBIT, "--month", month, "--outdir", str(packages_dir / "deribit")],
        "core_report": ["python3", CORE, "--month", month, "--outdir", str(packages_dir / "core_report")],
    }
