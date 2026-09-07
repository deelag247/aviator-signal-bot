#!/usr/bin/env python3
"""CLI entry point for the educational Aviator Signal Bot."""

from pathlib import Path
import argparse

from src.analyzer import RoundAnalyzer
from src.signals import SignalGenerator
from src.backtester import Backtester


def main():
    parser = argparse.ArgumentParser(
        description="Educational Aviator statistical analysis & signal demo"
    )
    parser.add_argument(
        "--data",
        default="data/sample_rounds.csv",
        help="Path to CSV with historical rounds",
    )
    parser.add_argument(
        "--backtest-target",
        type=float,
        default=1.5,
        help="Cash-out target for backtest (default 1.5)",
    )
    args = parser.parse_args()

    data_path = Path(args.data)
    if not data_path.exists():
        print(f"Error: data file not found → {data_path}")
        return

    print("Loading sample data...\n")
    analyzer = RoundAnalyzer(data_path)
    print(analyzer.summary())
    print()

    generator = SignalGenerator(analyzer)
    signals = generator.generate()
    print(generator.format_signals(signals))
    print()

    print("=== Simple Backtest (flat bet) ===")
    bt = Backtester(analyzer.multipliers)
    result = bt.run(cashout_target=args.backtest_target)
    print(f"Target cash-out : {args.backtest_target}x")
    print(f"Final bankroll  : {result['final_bankroll']}")
    print(f"Profit/Loss     : {result['profit']}")
    print(f"Win rate        : {result['win_rate']}%")
    print(f"Max drawdown    : {result['max_drawdown']}%")
    print()
    print(
        "Remember: past performance on sample data has no bearing on live rounds."
    )


if __name__ == "__main__":
    main()