#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


def _read_csv_row(path: Path) -> dict[str, str] | None:
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            return {k: str(v) for k, v in row.items()}
    return None


def _setup_light_style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "savefig.facecolor": "white",
            "axes.edgecolor": "#D9DEE7",
            "axes.grid": True,
            "grid.color": "#E9EDF4",
            "grid.alpha": 1.0,
            "font.size": 11,
            "axes.titlesize": 14,
            "axes.labelsize": 11,
            "legend.frameon": False,
        }
    )


def redraw_fig3_donut(report_dir: Path) -> bool:
    csv_path = report_dir / "packages" / "fig3" / "fig3_defi_tvl_share.csv"
    row = _read_csv_row(csv_path)
    if not row:
        return False

    labels = ["Ethereum", "Solana", "BSC", "Bitcoin", "Base", "Others"]
    vals = [
        float(row.get("ethereum_share_pct") or 0.0),
        float(row.get("solana_share_pct") or 0.0),
        float(row.get("bsc_share_pct") or 0.0),
        float(row.get("bitcoin_share_pct") or 0.0),
        float(row.get("base_share_pct") or 0.0),
        float(row.get("others_share_pct") or 0.0),
    ]
    month = row.get("month") or ""
    total_b = float(row.get("total_tvl_usd") or 0.0) / 1e9

    _setup_light_style()
    fig, ax = plt.subplots(figsize=(8.2, 5.6))
    colors = ["#4CAF50", "#66BB6A", "#F4B400", "#5C6BC0", "#2F7ED8", "#8D6E63"]

    wedges, _, autotexts = ax.pie(
        vals,
        labels=None,
        autopct=lambda p: f"{p:.1f}%" if p >= 4.0 else "",
        startangle=90,
        counterclock=False,
        colors=colors,
        pctdistance=0.80,
        wedgeprops={"width": 0.40, "edgecolor": "white", "linewidth": 1.2},
    )
    for t in autotexts:
        t.set_color("white")
        t.set_fontsize(10)
        t.set_fontweight("bold")

    ax.set_title("DeFi TVL Share by Chain", loc="left", fontsize=15, fontweight="bold", pad=14)
    ax.legend(wedges, labels, ncol=3, loc="lower center", bbox_to_anchor=(0.5, -0.08), frameon=False)
    ax.text(0, 0.10, month, ha="center", va="center", fontsize=11, color="#607080")
    ax.text(0, -0.06, f"TVL ${total_b:.2f}B", ha="center", va="center", fontsize=12, fontweight="bold", color="#2C3E50")

    fig.text(0.02, 0.02, "Source: DefiLlama protocol TVL aggregation", fontsize=9, color="#5F6B7A")
    fig.tight_layout(rect=[0, 0.06, 1, 1])

    out_main = report_dir / "charts" / "fig3_defi_tvl_share.png"
    out_pkg = report_dir / "packages" / "fig3" / "fig3_defi_tvl_share.png"
    out_main.parent.mkdir(parents=True, exist_ok=True)
    out_pkg.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_main, dpi=180)
    fig.savefig(out_pkg, dpi=180)
    plt.close(fig)
    return True


def redraw_fig6_stacked(report_dir: Path) -> bool:
    csv_path = report_dir / "packages" / "fig6" / "fig6_altcoin_outside_top10_share.csv"
    row = _read_csv_row(csv_path)
    if not row:
        return False

    total = float(row.get("total_market_cap_usd") or 0.0)
    btc = float(row.get("btc_market_cap_usd") or 0.0)
    top10_alt = float(row.get("top10_alt_market_cap_usd") or 0.0)
    outside = float(row.get("outside_top10_alt_market_cap_usd") or 0.0)
    month = row.get("month") or ""

    if total <= 0:
        return False

    btc_pct = btc / total * 100.0
    top10_alt_pct = top10_alt / total * 100.0
    outside_pct = outside / total * 100.0
    total_t = total / 1e12

    _setup_light_style()
    fig, ax = plt.subplots(figsize=(10.6, 4.3))

    y = [0]
    ax.barh(y, [btc_pct], color="#4F8CD6", height=0.42, label="BTC")
    ax.barh(y, [top10_alt_pct], left=[btc_pct], color="#66BB6A", height=0.42, label="Top10 Alt")
    ax.barh(y, [outside_pct], left=[btc_pct + top10_alt_pct], color="#F5A623", height=0.42, label="Outside Top10")

    ax.set_xlim(0, 100)
    ax.set_yticks([])
    ax.set_xlabel("Share of total market cap (%)")
    ax.set_title("Altcoin Market Breadth Composition", loc="left", fontweight="bold")

    if btc_pct >= 7:
        ax.text(btc_pct / 2, 0, f"BTC\\n{btc_pct:.1f}%", ha="center", va="center", color="white", fontsize=10, fontweight="bold")
    if top10_alt_pct >= 7:
        ax.text(btc_pct + top10_alt_pct / 2, 0, f"Top10 Alt\\n{top10_alt_pct:.1f}%", ha="center", va="center", color="white", fontsize=10, fontweight="bold")
    if outside_pct >= 5:
        ax.text(btc_pct + top10_alt_pct + outside_pct / 2, 0, f"Outside\\n{outside_pct:.1f}%", ha="center", va="center", color="white", fontsize=10, fontweight="bold")

    ax.annotate(
        f"Outside Top10 share: {outside_pct:.2f}%",
        xy=(btc_pct + top10_alt_pct + outside_pct * 0.5, 0),
        xytext=(0, 36),
        textcoords="offset points",
        ha="center",
        fontsize=11,
        fontweight="bold",
        color="#C26C00",
        arrowprops={"arrowstyle": "-|>", "color": "#C26C00", "lw": 1.1},
    )

    ax.legend(loc="lower center", bbox_to_anchor=(0.5, -0.35), ncol=3)
    fig.text(0.02, 0.06, f"Month: {month} | Total market cap: ${total_t:.2f}T", fontsize=10, color="#5F6B7A")
    fig.text(0.02, 0.02, "Source: CMC historical global metrics + top10 aggregation", fontsize=9, color="#5F6B7A")
    fig.tight_layout(rect=[0, 0.10, 1, 1])

    out_main = report_dir / "charts" / "fig6_altcoin_outside_top10_share.png"
    out_pkg = report_dir / "packages" / "fig6" / "fig6_altcoin_outside_top10_share.png"
    out_main.parent.mkdir(parents=True, exist_ok=True)
    out_pkg.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_main, dpi=180)
    fig.savefig(out_pkg, dpi=180)
    plt.close(fig)
    return True


def _read_deribit_prices_and_funding(report_dir: Path) -> list[tuple[str, float, float, float]]:
    csv_path = report_dir / "packages" / "deribit" / "deribit_funding_monthly.csv"
    out: list[tuple[str, float, float, float]] = []
    if not csv_path.exists():
        return out
    with csv_path.open("r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            c = str(row.get("currency") or "").upper().strip()
            if c not in ("BTC", "ETH"):
                continue
            avg = float(row.get("average_funding_8h") or 0.0) * 10000.0
            ending = float(row.get("ending_funding_8h") or 0.0) * 10000.0
            out.append((c, avg, ending, 0.0))
    order = {"BTC": 0, "ETH": 1}
    out.sort(key=lambda x: order.get(x[0], 99))
    return out


def redraw_deribit_funding_light(report_dir: Path) -> bool:
    rows = _read_deribit_prices_and_funding(report_dir)
    if not rows:
        return False
    labels = [r[0] for r in rows]
    f8 = [r[1] for r in rows]
    cur = [r[2] for r in rows]

    _setup_light_style()
    fig, ax = plt.subplots(figsize=(9.2, 4.8))

    x = np.arange(len(labels))
    w = 0.32
    b1 = ax.bar(x - w / 2, f8, width=w, color="#F97316", label="Monthly average 8h (bps)")
    b2 = ax.bar(x + w / 2, cur, width=w, color="#4F8CD6", label="Month-end 8h (bps)")

    ax.axhline(0, color="#AEB6C2", linewidth=1)
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("bps")
    ax.set_title("Deribit Monthly Perp Funding", loc="left", fontweight="bold")
    ax.legend(loc="upper right")

    max_abs = max([abs(v) for v in f8 + cur] + [0.8])
    ax.set_ylim(-max_abs * 1.5, max_abs * 1.5)
    for bars in (b1, b2):
        for bar in bars:
            h = bar.get_height()
            x0 = bar.get_x() + bar.get_width() / 2
            y0 = h + max_abs * 0.06 if h >= 0 else h - max_abs * 0.08
            va = "bottom" if h >= 0 else "top"
            ax.text(x0, y0, f"{h:+.2f}", ha="center", va=va, fontsize=10)

    fig.text(0.01, 0.01, "Source: Deribit public/get_funding_rate_history", fontsize=9, color="#5F6B7A")
    fig.tight_layout(rect=[0, 0.04, 1, 1])

    out_main = report_dir / "charts" / "chart_deribit_funding.png"
    out_pkg = report_dir / "packages" / "deribit" / "chart_deribit_funding.png"
    out_main.parent.mkdir(parents=True, exist_ok=True)
    out_pkg.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_main, dpi=180)
    fig.savefig(out_pkg, dpi=180)
    plt.close(fig)
    return True


def redraw_deribit_oi_usd(report_dir: Path) -> bool:
    try:
        manifest = json.loads((report_dir / "packages" / "deribit" / "deribit_manifest.json").read_text(encoding="utf-8"))
    except Exception:
        manifest = {}
    if not bool((manifest.get("oi_snapshot") or {}).get("usable_as_target_month_end")):
        for stale in (
            report_dir / "charts" / "chart_deribit_oi.png",
            report_dir / "packages" / "deribit" / "chart_deribit_oi.png",
        ):
            if stale.exists():
                stale.unlink()
        return False

    prices: dict[str, float] = {}
    snapshot_csv = report_dir / "packages" / "deribit" / "deribit_funding_snapshot.csv"
    if snapshot_csv.exists():
        with snapshot_csv.open("r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                ccy = str(row.get("currency") or "").upper()
                if ccy in ("BTC", "ETH"):
                    prices[ccy] = float(row.get("last_price") or 0.0)

    oi_csv = report_dir / "packages" / "deribit" / "deribit_oi_volume_snapshot.csv"
    if not oi_csv.exists():
        return False

    oi_usd: dict[tuple[str, str], float] = {}
    with oi_csv.open("r", encoding="utf-8") as f:
        r = csv.DictReader(f)
        for row in r:
            c = str(row.get("currency") or "").upper().strip()
            k = str(row.get("kind") or "").lower().strip()
            if c not in ("BTC", "ETH") or k not in ("future", "option"):
                continue
            oi = float(row.get("open_interest_sum") or 0.0)
            if k == "future":
                oi_usd[(c, k)] = oi
            else:
                oi_usd[(c, k)] = oi * prices.get(c, 0.0)

    labels = ["BTC", "ETH"]
    fut_b = [oi_usd.get((ccy, "future"), 0.0) / 1e9 for ccy in labels]
    opt_b = [oi_usd.get((ccy, "option"), 0.0) / 1e9 for ccy in labels]

    _setup_light_style()
    fig, ax = plt.subplots(figsize=(10.2, 4.8))
    x = np.arange(len(labels))
    w = 0.34

    b1 = ax.bar(x - w / 2, fut_b, width=w, color="#4F8CD6", label="Futures OI (USD)")
    b2 = ax.bar(x + w / 2, opt_b, width=w, color="#F5A623", label="Options OI (USD converted)")

    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("USD billions")
    ax.set_title("Deribit OI by Currency (USD-normalized)", loc="left", fontweight="bold")
    ax.legend(loc="upper right")

    ymax = max(fut_b + opt_b + [1.0])
    ax.set_ylim(0, ymax * 1.18)
    for bars in (b1, b2):
        for b in bars:
            h = b.get_height()
            ax.text(b.get_x() + b.get_width() / 2, h + ymax * 0.01, f"{h:.2f}B", ha="center", va="bottom", fontsize=10)

    fig.text(
        0.01,
        0.01,
        "Source: Deribit public/get_book_summary_by_currency + public/ticker (options OI converted from native units)",
        fontsize=9,
        color="#5F6B7A",
    )
    fig.tight_layout(rect=[0, 0.04, 1, 1])

    out_main = report_dir / "charts" / "chart_deribit_oi.png"
    out_pkg = report_dir / "packages" / "deribit" / "chart_deribit_oi.png"
    out_main.parent.mkdir(parents=True, exist_ok=True)
    out_pkg.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_main, dpi=180)
    fig.savefig(out_pkg, dpi=180)
    plt.close(fig)
    return True


def patch_coinbase_style_md(report_dir: Path) -> bool:
    md = report_dir / "orchestrated_secondary_report_coinbase_style_text.md"
    if not md.exists():
        return False

    text = md.read_text(encoding="utf-8")
    old = text

    text = text.replace("![NFT月成交额](charts/fig4_monthly_nft_volume.png)\n\n", "")
    text = text.replace("![NFT月成交额](charts/fig4_monthly_nft_volume.png)\n", "")
    text = text.replace("“", "").replace("”", "")

    text = re.sub(
        r"\n### Derivatives Risk\n.*?\n### Sentiment & Volatility",
        "\n### Sentiment & Volatility",
        text,
        flags=re.S,
    )

    if text != old:
        md.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply v2 visual/text polish to orchestrated monthly report outputs")
    parser.add_argument("--report-dir", required=True, help="Report output directory, e.g. ./reports/2026-02/secondary_orchestrated")
    args = parser.parse_args()

    report_dir = Path(args.report_dir)
    if not report_dir.exists():
        raise SystemExit(f"report dir not found: {report_dir}")

    results = {
        "fig3_donut": redraw_fig3_donut(report_dir),
        "fig6_stacked": redraw_fig6_stacked(report_dir),
        "deribit_funding_light": redraw_deribit_funding_light(report_dir),
        "deribit_oi_usd": redraw_deribit_oi_usd(report_dir),
        "patch_md": patch_coinbase_style_md(report_dir),
    }

    print("[ok] v2 polish summary")
    for k, v in results.items():
        print(f" - {k}: {'updated' if v else 'skipped'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
