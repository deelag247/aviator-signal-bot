from __future__ import annotations

from dataclasses import dataclass
from typing import List
import numpy as np
from .analyzer import RoundAnalyzer


@dataclass
class Signal:
    target: float
    confidence: str
    reason: str
    suggested_cashout: float


class SignalGenerator:
    """
    Generates educational 'signals' from historical statistics only.
    These are NOT predictions of future rounds.
    """

    def __init__(self, analyzer: RoundAnalyzer):
        self.analyzer = analyzer

    def generate(self, lookback: int = 20) -> List[Signal]:
        m = self.analyzer.multipliers[-lookback:]
        mean = float(np.mean(m))
        recent_low_streak = self.analyzer.streak_analysis()["current_low_streak"]

        signals: List[Signal] = []

        signals.append(
            Signal(
                target=1.5,
                confidence="medium",
                reason=f"Historical mean ≈ {mean:.2f}x; many rounds exceed 1.5x",
                suggested_cashout=1.50,
            )
        )

        if mean > 2.0 or recent_low_streak >= 3:
            signals.append(
                Signal(
                    target=2.0,
                    confidence="low",
                    reason="Recent low streak or elevated sample mean",
                    suggested_cashout=2.00,
                )
            )

        signals.append(
            Signal(
                target=5.0,
                confidence="low",
                reason="Rare high multipliers exist in sample; pure speculation",
                suggested_cashout=5.00,
            )
        )

        return signals

    def format_signals(self, signals: List[Signal]) -> str:
        lines = ["=== Educational Signals (NOT predictions) ==="]
        for i, s in enumerate(signals, 1):
            lines.append(
                f"{i}. Target {s.target:.2f}x | "
                f"Cash-out suggestion {s.suggested_cashout:.2f}x | "
                f"Confidence: {s.confidence} | {s.reason}"
            )
        lines.append(
            "\n⚠️  These signals are derived only from past sample data. "
            "Live Aviator rounds are independent and unpredictable."
        )
        return "\n".join(lines)