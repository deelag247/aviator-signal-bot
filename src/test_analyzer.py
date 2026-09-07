import pytest
from pathlib import Path
import numpy as np
from src.analyzer import RoundAnalyzer
from src.signals import SignalGenerator
from src.backtester import Backtester


SAMPLE = Path(__file__).parent.parent / "data" / "sample_rounds.csv"


def test_analyzer_loads():
    a = RoundAnalyzer(SAMPLE)
    assert len(a.multipliers) == 50
    assert a.multipliers[0] == pytest.approx(1.23)


def test_basic_stats():
    a = RoundAnalyzer(SAMPLE)
    stats = a.basic_stats()
    assert stats["count"] == 50
    assert stats["mean"] > 1.0
    assert 0 <= stats["pct_under_1_5"] <= 100


def test_streak_analysis():
    a = RoundAnalyzer(SAMPLE)
    s = a.streak_analysis()
    assert "max_low_streak" in s
    assert s["max_low_streak"] >= 0


def test_signal_generation():
    a = RoundAnalyzer(SAMPLE)
    g = SignalGenerator(a)
    signals = g.generate()
    assert len(signals) >= 1
    assert signals[0].target > 1.0


def test_backtester():
    a = RoundAnalyzer(SAMPLE)
    bt = Backtester(a.multipliers)
    res = bt.run(cashout_target=1.5, start_bankroll=100)
    assert "final_bankroll" in res
    assert res["wins"] + res["losses"] > 0