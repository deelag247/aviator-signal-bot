from __future__ import annotations

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any


class RoundAnalyzer:
    """Statistical analysis of historical Aviator crash multipliers."""

    def __init__(self, csv_path: str | Path):
        self.df = pd.read_csv(csv_path)
        self.df["crash_multiplier"] = self.df["crash_multiplier"].astype(float)
        self.multipliers = self.df["crash_multiplier"].values

    def basic_stats(self) -> Dict[str, float]:
        m = self.multipliers
        return {
            "count": len(m),
            "mean": float(np.mean(m)),
            "median": float(np.median(m)),
            "std": float(np.std(m)),
            "min": float(np.min(m)),
            "max": float(np.max(m)),
            "pct_under_1_5": float(np.mean(m < 1.5) * 100),
            "pct_over_2": float(np.mean(m >= 2.0) * 100),
            "pct_over_5": float(np.mean(m >= 5.0) * 100),
        }

    def rolling_mean(self, window: int = 10) -> pd.Series:
        return self.df["crash_multiplier"].rolling(window=window, min_periods=1).mean()

    def streak_analysis(self) -> Dict[str, Any]:
        """Count consecutive low (<1.5x) and high (>=2x) streaks."""
        lows = self.multipliers < 1.5
        highs = self.multipliers >= 2.0

        def max_streak(mask: np.ndarray) -> int:
            if len(mask) == 0:
                return 0
            max_s = cur = 0
            for v in mask:
                if v:
                    cur += 1
                    max_s = max(max_s, cur)
                else:
                    cur = 0
            return max_s

        return {
            "max_low_streak": max_streak(lows),
            "max_high_streak": max_streak(highs),
            "current_low_streak": self._current_streak(lows),
            "current_high_streak": self._current_streak(highs),
        }

    def _current_streak(self, mask: np.ndarray) -> int:
        streak = 0
        for v in reversed(mask):
            if v:
                streak += 1
            else:
                break
        return streak

    def summary(self) -> str:
        stats = self.basic_stats()
        streaks = self.streak_analysis()
        lines = [
            "=== Aviator Round Analyzer (Sample Data) ===",
            f"Rounds analysed : {stats['count']}",
            f"Mean multiplier : {stats['mean']:.2f}x",
            f"Median          : {stats['median']:.2f}x",
            f"% under 1.5x    : {stats['pct_under_1_5']:.1f}%",
            f"% over 2.0x     : {stats['pct_over_2']:.1f}%",
            f"% over 5.0x     : {stats['pct_over_5']:.1f}%",
            f"Max low streak  : {streaks['max_low_streak']}",
            f"Max high streak : {streaks['max_high_streak']}",
            f"Current low     : {streaks['current_low_streak']}",
            f"Current high    : {streaks['current_high_streak']}",
        ]
        return "\n".join(lines)