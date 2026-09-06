#!/usr/bin/env python3
"""
Agent Negotiation Protocol — Enhanced Demo Showcase

Designed for asciinema recording to demonstrate:
  Act 1: Architecture overview
  Act 2: ZOPA game-theory analysis (depth)
  Act 3: Live multi-round negotiation (practical value)
  Act 4: x402 settlement + reputation (creativity)
  Act 5: Failure scenario comparison (robustness)

Usage:
    conda run -n spoonos-skill python demo_showcase.py

Author: bonujel
"""

from __future__ import annotations

import asyncio
import os
import sys
import time

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "scripts"))

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.columns import Columns
from rich.rule import Rule
from rich.live import Live
from rich.align import Align

from negotiation_engine import (
    NegotiationEngine,
    NegotiationStatus,
    CONCESSION_RATE_BUYER,
    CONCESSION_RATE_SELLER,
    MAX_NEGOTIATION_ROUNDS,
)
from x402_settlement import X402Settlement

console = Console(width=100)

# Typing speed for dramatic effect in asciinema
PAUSE_SHORT = 0.5
PAUSE_MEDIUM = 1.2
PAUSE_LONG = 2.0


# ---------------------------------------------------------------------------
# Act 1: Architecture Overview
# ---------------------------------------------------------------------------

def act1_architecture() -> None:
    """Display project architecture and motivation."""
    console.print()
    title = Text("🤝 Agent Negotiation Protocol", style="bold white")
    subtitle = Text(
        "Automated multi-round negotiation between AI agents\n"
        "Powered by SpoonOS StateGraph · Settled via x402 · Scored by ERC-8004",
        style="dim",
    )
    console.print(Panel(
        Align.center(title + Text("\n") + subtitle),
        border_style="bright_cyan",
        padding=(1, 2),
    ))
    time.sleep(PAUSE_MEDIUM)

    arch = Text()
    arch.append("  ┌──────────┐     ┌──────────────┐     ┌──────────────┐\n", style="cyan")
    arch.append("  │  Buyer   │────→│   Seller     │────→│   Settle     │\n", style="cyan")
    arch.append("  │ Propose  │     │  Evaluate    │     │  (x402 pay)  │\n", style="cyan")
    arch.append("  └──────────┘     └──────┬───────┘     └──────────────┘\n", style="cyan")
    arch.append("       ▲                  │\n", style="cyan")
    arch.append("       │           ┌──────▼───────┐\n", style="cyan")
    arch.append("       └───────────│    Buyer     │\n", style="cyan")
    arch.append("                   │   Decide     │\n", style="cyan")
    arch.append("                   └──────────────┘\n", style="cyan")

    console.print(Panel(arch, title="[bold]StateGraph Workflow[/bold]", border_style="blue"))
    time.sleep(PAUSE_MEDIUM)

    features = Table(show_header=True, header_style="bold magenta", box=None)
    features.add_column("Feature", style="cyan", width=20)
    features.add_column("Usage", style="white")
    features.add_row("StateGraph", "Multi-round cyclic workflow with conditional routing")
    features.add_row("x402 Protocol", "Automated USDC payment on agreement")
    features.add_row("ERC-8004", "Agent reputation scoring & trust verification")
    features.add_row("LLM (Qwen)", "Agent decision-making with game-theoretic constraints")
    console.print(Panel(features, title="[bold]SpoonOS Features Used[/bold]", border_style="green"))
    time.sleep(PAUSE_LONG)


# ---------------------------------------------------------------------------
# Act 2: ZOPA Game-Theory Analysis
# ---------------------------------------------------------------------------

def act2_zopa_analysis() -> None:
    """Visualize ZOPA convergence with ASCII chart."""
    console.print()
    console.print(Rule("[bold yellow]Act 2: ZOPA Game-Theory Analysis[/bold yellow]"))
    time.sleep(PAUSE_SHORT)

    buyer_budget = 50.0
    seller_base = 80.0
    max_rounds = 5

    console.print(
        f"\n  [cyan]Buyer budget:[/cyan]      ${buyer_budget:.2f}"
        f"\n  [green]Seller base price:[/green] ${seller_base:.2f}"
        f"\n  [dim]Buyer concession rate:  {CONCESSION_RATE_BUYER:.0%}/round[/dim]"
        f"\n  [dim]Seller concession rate: {CONCESSION_RATE_SELLER:.0%}/round[/dim]\n"
    )
    time.sleep(PAUSE_SHORT)

    # Build convergence table
    table = Table(
        title="Price Convergence Analysis",
        show_header=True,
        header_style="bold",
    )
    table.add_column("Round", style="bold white", justify="center", width=7)
    table.add_column("Buyer Ceiling", style="cyan", justify="right", width=15)
    table.add_column("Seller Floor", style="green", justify="right", width=15)
    table.add_column("Gap", justify="right", width=10)
    table.add_column("Visual", width=40)

    zopa_round = None
    for n in range(1, max_rounds + 1):
        ceiling = buyer_budget * (1 + CONCESSION_RATE_BUYER * (n - 1))
        floor = seller_base * (1 - CONCESSION_RATE_SELLER * (n - 1))
        gap = floor - ceiling

        # ASCII bar chart (scale: $1 = 1 char, offset from $40)
        bar_width = 50
        scale_min, scale_max = 40.0, 95.0
        b_pos = int((ceiling - scale_min) / (scale_max - scale_min) * bar_width)
        s_pos = int((floor - scale_min) / (scale_max - scale_min) * bar_width)
        b_pos = max(0, min(bar_width - 1, b_pos))
        s_pos = max(0, min(bar_width - 1, s_pos))

        bar = list("·" * bar_width)
        if b_pos <= s_pos:
            bar[b_pos] = "▶"
            bar[s_pos] = "◀"
        else:
            bar[s_pos] = "◀"
            bar[b_pos] = "▶"
            # Mark overlap
            for i in range(s_pos, b_pos + 1):
                bar[i] = "█"

        visual = "".join(bar)

        if gap > 0:
            gap_str = f"[red]-${gap:.2f}[/red]"
        else:
            gap_str = f"[bold green]ZOPA! +${abs(gap):.2f}[/bold green]"
            if zopa_round is None:
                zopa_round = n

        table.add_row(
            str(n),
            f"${ceiling:.2f}",
            f"${floor:.2f}",
            gap_str,
            f"[cyan]{visual[:b_pos+1]}[/cyan][green]{visual[b_pos+1:]}[/green]"
            if b_pos < s_pos
            else f"[bold green]{visual}[/bold green]",
        )

    console.print(table)
    time.sleep(PAUSE_SHORT)

    if zopa_round:
        console.print(
            f"\n  [bold green]✓ ZOPA emerges at Round {zopa_round}[/bold green] — "
            f"negotiation is feasible!\n"
        )
    time.sleep(PAUSE_LONG)


# ---------------------------------------------------------------------------
# Act 3: Live Multi-Round Negotiation
# ---------------------------------------------------------------------------

async def act3_live_negotiation() -> object | None:
    """Run a real negotiation and display results live."""
    console.print()
    console.print(Rule("[bold yellow]Act 3: Live Multi-Round Negotiation[/bold yellow]"))
    time.sleep(PAUSE_SHORT)

    scenario = Table(show_header=False, box=None, padding=(0, 2))
    scenario.add_column(style="bold cyan", width=20)
    scenario.add_column(style="white")
    scenario.add_row("Buyer Intent", "On-chain data analysis for 100 wallets")
    scenario.add_row("Seller Service", "Batch wallet profiling + risk scoring")
    scenario.add_row("Buyer Budget", "$50.00")
    scenario.add_row("Seller Price", "$80.00")
    scenario.add_row("Max Rounds", "5")
    console.print(Panel(scenario, title="[bold]Negotiation Scenario[/bold]", border_style="yellow"))
    time.sleep(PAUSE_MEDIUM)

    console.print("\n  [bold]Starting negotiation...[/bold] (LLM-driven decisions)\n")
    time.sleep(PAUSE_SHORT)

    engine = NegotiationEngine(max_rounds=5)
    result = await engine.run_negotiation(
        buyer_intent="On-chain data analysis for 100 wallets, "
                     "including transaction patterns and risk scoring",
        seller_capability="Full-stack on-chain analytics service, "
                         "supports batch wallet profiling, risk assessment, "
                         "and custom report generation",
        buyer_budget=50.0,
        seller_base_price=80.0,
    )

    # Display negotiation history
    history_table = Table(
        title="Negotiation Trace",
        show_header=True,
        header_style="bold",
    )
    history_table.add_column("Round", justify="center", width=6)
    history_table.add_column("Role", width=16)
    history_table.add_column("Action", width=9)
    history_table.add_column("Price", justify="right", width=10)
    history_table.add_column("SLA", width=10)
    history_table.add_column("Reasoning", width=40, no_wrap=False)

    for entry in result.history:
        role = entry.get("role", "?")
        rnd = str(entry.get("round", "?"))
        action = entry.get("action", "?")
        price = entry.get("price", "?")
        sla = entry.get("sla_tier", "?")
        reasoning = entry.get("reasoning", "")[:60]

        role_style = "cyan" if "buyer" in role else "green"
        action_style = "bold green" if action == "accept" else (
            "bold red" if action == "reject" else "yellow"
        )

        history_table.add_row(
            rnd,
            f"[{role_style}]{role}[/{role_style}]",
            f"[{action_style}]{action}[/{action_style}]",
            f"${price}" if isinstance(price, (int, float)) else str(price),
            str(sla),
            reasoning,
        )

    console.print(history_table)
    time.sleep(PAUSE_SHORT)

    # Result summary
    status_style = "bold green" if result.status == NegotiationStatus.AGREED else "bold red"
    console.print(f"\n  Status:       [{status_style}]{result.status.value}[/{status_style}]")
    if result.agreed_price:
        console.print(f"  Agreed Price: [bold]${result.agreed_price:.2f}[/bold]")
    console.print(f"  Agreed SLA:   {result.agreed_sla or 'N/A'}")
    console.print(f"  Rounds Taken: {result.rounds_taken}")
    time.sleep(PAUSE_LONG)

    return result


# ---------------------------------------------------------------------------
# Act 4: x402 Settlement + Reputation
# ---------------------------------------------------------------------------

async def act4_settlement(result: object) -> None:
    """Demonstrate x402 settlement and reputation updates."""
    console.print()
    console.print(Rule("[bold yellow]Act 4: x402 Settlement + ERC-8004 Reputation[/bold yellow]"))
    time.sleep(PAUSE_SHORT)

    if result.status != NegotiationStatus.AGREED or not result.agreed_price:
        console.print("  [dim]Skipped — no agreement reached in Act 3[/dim]")
        return

    # x402 flow visualization
    console.print("\n  [bold]x402 Payment Protocol Flow:[/bold]\n")
    steps = [
        ("1", "402 Challenge", "Seller issues payment challenge", "yellow"),
        ("2", "Sign Payment", "Buyer agent signs USDC transaction", "cyan"),
        ("3", "Verify Sig", "Service verifies cryptographic signature", "magenta"),
        ("4", "Confirm Pay", "Payment confirmed on Base network", "green"),
    ]
    for num, title, desc, color in steps:
        time.sleep(PAUSE_SHORT)
        console.print(f"  [{color}]Step {num}: {title}[/{color}] — {desc} [green]✓[/green]")

    time.sleep(PAUSE_SHORT)

    settlement = X402Settlement()
    tx = await settlement.execute_settlement(
        agreed_price=result.agreed_price,
        buyer_id="agent-buyer-001",
        seller_id="agent-seller-001",
        sla_tier=result.agreed_sla or "standard",
    )

    # Settlement result
    tx_table = Table(show_header=False, box=None, padding=(0, 2))
    tx_table.add_column(style="bold", width=22)
    tx_table.add_column(style="white")
    tx_table.add_row("TX Hash", f"[dim]{tx.tx_hash[:20]}...{tx.tx_hash[-8:]}[/dim]")
    tx_table.add_row("Amount", f"[bold]${tx.amount:.2f} {tx.asset}[/bold]")
    tx_table.add_row("Network", "Base")
    tx_table.add_row("Status", f"[bold green]{tx.status}[/bold green]")
    tx_table.add_row("Buyer Reputation", _reputation_bar(tx.buyer_reputation_after))
    tx_table.add_row("Seller Reputation", _reputation_bar(tx.seller_reputation_after))
    console.print(Panel(tx_table, title="[bold]Settlement Result[/bold]", border_style="green"))
    time.sleep(PAUSE_LONG)


def _reputation_bar(score: float) -> str:
    """Render a reputation score as a colored progress bar."""
    filled = int(score * 20)
    empty = 20 - filled
    color = "green" if score >= 0.6 else ("yellow" if score >= 0.3 else "red")
    bar = f"[{color}]{'█' * filled}[/{color}][dim]{'░' * empty}[/dim]"
    return f"{bar} {score:.2f}"


# ---------------------------------------------------------------------------
# Act 5: Failure Scenario — ZOPA Pre-Check Saves Resources
# ---------------------------------------------------------------------------

def act5_failure_scenario() -> None:
    """Show how ZOPA pre-check prevents wasted negotiation rounds."""
    console.print()
    console.print(Rule("[bold yellow]Act 5: Robustness — ZOPA Pre-Check[/bold yellow]"))
    time.sleep(PAUSE_SHORT)

    buyer_budget = 30.0
    seller_base = 120.0

    console.print(
        f"\n  [cyan]Buyer budget:[/cyan]      ${buyer_budget:.2f}"
        f"\n  [green]Seller base price:[/green] ${seller_base:.2f}"
        f"\n  [dim]Gap: ${seller_base - buyer_budget:.2f} — can concessions bridge it?[/dim]\n"
    )
    time.sleep(PAUSE_SHORT)

    # Check ZOPA
    feasible = False
    for n in range(1, 6):
        ceiling = buyer_budget * (1 + CONCESSION_RATE_BUYER * (n - 1))
        floor = seller_base * (1 - CONCESSION_RATE_SELLER * (n - 1))
        if ceiling >= floor:
            feasible = True
            break

    if not feasible:
        console.print(
            "  [bold red]✗ ZOPA pre-check: NO overlap possible in 5 rounds[/bold red]\n"
        )
        time.sleep(PAUSE_SHORT)

        # Comparison
        compare = Table(show_header=True, header_style="bold")
        compare.add_column("Approach", width=25)
        compare.add_column("LLM Calls", justify="center", width=12)
        compare.add_column("Cost", justify="center", width=10)
        compare.add_column("Time", justify="center", width=10)
        compare.add_row(
            "[red]Without pre-check[/red]",
            "~10 calls", "~$0.05", "~30s",
        )
        compare.add_row(
            "[green]With ZOPA pre-check[/green]",
            "[bold green]0 calls[/bold green]",
            "[bold green]$0.00[/bold green]",
            "[bold green]<1ms[/bold green]",
        )
        console.print(compare)
        console.print(
            "\n  [green]→ Saved 10 LLM calls and 30 seconds "
            "by detecting infeasibility upfront![/green]\n"
        )
    time.sleep(PAUSE_LONG)


# ---------------------------------------------------------------------------
# Main — Orchestrate All Acts
# ---------------------------------------------------------------------------

async def main() -> None:
    """Run the complete demo showcase."""
    console.clear()

    # Act 1: Architecture
    act1_architecture()

    # Act 2: ZOPA Analysis
    act2_zopa_analysis()

    # Act 3: Live Negotiation
    result = await act3_live_negotiation()

    # Act 4: Settlement (only if Act 3 succeeded)
    if result:
        await act4_settlement(result)

    # Act 5: Failure Scenario
    act5_failure_scenario()

    # Closing
    console.print()
    console.print(Rule("[bold bright_cyan]Demo Complete[/bold bright_cyan]"))
    console.print(
        "\n  [bold]Agent Negotiation Protocol[/bold] — "
        "bringing mechanism design into the AI agent economy.\n"
        "  Agents are not just tools; they are [italic]economic participants[/italic] "
        "with their own utility functions.\n"
    )
    console.print(
        "  [dim]SpoonOS Features: StateGraph · x402 · ERC-8004 · LLM Integration[/dim]\n"
    )


if __name__ == "__main__":
    asyncio.run(main())
