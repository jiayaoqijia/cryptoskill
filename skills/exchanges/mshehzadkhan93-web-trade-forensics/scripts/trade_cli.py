import argparse
import json

from analyze_live_trade import analyze_live_trade


def main():
    parser = argparse.ArgumentParser(
        description="Trade Forensics Agent - analyze a trade with live Binance market data."
    )

    parser.add_argument("symbol", help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("side", choices=["long", "short"], help="Trade direction")
    parser.add_argument("entry", type=float, help="Entry price")
    parser.add_argument("stop_loss", type=float, help="Stop-loss price")
    parser.add_argument("take_profit", type=float, help="Take-profit price")
    parser.add_argument(
        "--leverage",
        type=float,
        default=1.0,
        help="Leverage (default: 1)",
    )
    parser.add_argument(
        "--position-size",
        type=float,
        default=None,
        help="Optional position size",
    )

    args = parser.parse_args()

    result = analyze_live_trade(
        symbol=args.symbol,
        side=args.side,
        entry=args.entry,
        stop_loss=args.stop_loss,
        take_profit=args.take_profit,
        leverage=args.leverage,
        position_size=args.position_size,
    )

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
