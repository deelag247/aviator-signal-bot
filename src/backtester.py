from __future__ import annotations

from typing import List, Dict
import numpy as np
from .signals import Signal


class Backtester:
    """Simple strategy backtester on historical multipliers."""

    def __init__(self, multipliers: np.ndarray):
        self.multipliers = multipliers

    def run(
        self,
        cashout_target: float,
        bet_size: float = 1.0,
        start_bankroll: float = 100.0,
    ) -> Dict:
        bankroll = start_bankroll
        wins = 0
        losses = 0
        history: List[float] = [bankroll]

        for crash in self.multipliers:
            if bankroll < bet_size:
                break
            bankroll -= bet_size
            if crash >= cashout_target:
                bankroll += bet_size * cashout_target
                wins += 1
            else:
                losses += 1
            history.append(bankroll)

        total = wins + losses
        return {
            "final_bankroll": round(bankroll, 2),
            "profit": round(bankroll - start_bankroll, 2),
            "wins": wins,
            "losses": losses,
            "win_rate": round(wins / total * 100, 1) if total else 0.0,
            "max_drawdown": self._max_drawdown(history),
            "history": history,
        }

    def _max_drawdown(self, equity: List[float]) -> float:
        peak = equity[0]
        max_dd = 0.0
        for v in equity:
            peak = max(peak, v)
            dd = (peak - v) / peak if peak > 0 else 0
            max_dd = max(max_dd, dd)
        return round(max_dd * 100, 1)