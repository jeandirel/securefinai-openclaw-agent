"""Technical signals: EMA crossover, RSI, momentum."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import pandas as pd

Action = Literal["buy", "sell", "hold"]


@dataclass
class SignalResult:
    action: Action
    score: float  # in [-1, 1]
    reason: str


def ema(series: pd.Series, period: int) -> pd.Series:
    return series.ewm(span=period, adjust=False).mean()


def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    up = delta.clip(lower=0)
    down = -delta.clip(upper=0)
    roll_up = up.ewm(alpha=1 / period, adjust=False).mean()
    roll_down = down.ewm(alpha=1 / period, adjust=False).mean()
    rs = roll_up / (roll_down + 1e-12)
    return 100 - (100 / (1 + rs))


def momentum(series: pd.Series, period: int = 20) -> pd.Series:
    return series.pct_change(period)


def compute_signal(df: pd.DataFrame) -> SignalResult:
    if df is None or df.empty or len(df) < 50:
        return SignalResult(action="hold", score=0.0, reason="not enough bars")

    close = df["close"].astype(float)
    e_fast = ema(close, 12)
    e_slow = ema(close, 26)
    r = rsi(close, 14)
    m = momentum(close, 20)

    last_fast = e_fast.iloc[-1]
    last_slow = e_slow.iloc[-1]
    prev_fast = e_fast.iloc[-2]
    prev_slow = e_slow.iloc[-2]
    last_rsi = r.iloc[-1]
    last_mom = m.iloc[-1] if not pd.isna(m.iloc[-1]) else 0.0

    crossed_up = prev_fast <= prev_slow and last_fast > last_slow
    crossed_dn = prev_fast >= prev_slow and last_fast < last_slow

    score = 0.0
    reasons = []

    # Trend
    if last_fast > last_slow:
        score += 0.3
        reasons.append("EMA12>EMA26")
    else:
        score -= 0.3
        reasons.append("EMA12<EMA26")

    # Crossover bonus
    if crossed_up:
        score += 0.4
        reasons.append("bullish crossover")
    elif crossed_dn:
        score -= 0.4
        reasons.append("bearish crossover")

    # Momentum
    if last_mom > 0.01:
        score += 0.2
        reasons.append(f"mom20={last_mom:.2%}")
    elif last_mom < -0.01:
        score -= 0.2
        reasons.append(f"mom20={last_mom:.2%}")

    # RSI filter: avoid buying overbought / selling oversold
    if last_rsi > 75:
        score -= 0.3
        reasons.append(f"RSI={last_rsi:.0f} overbought")
    elif last_rsi < 25:
        score += 0.3
        reasons.append(f"RSI={last_rsi:.0f} oversold")

    score = max(-1.0, min(1.0, score))

    if score >= 0.4:
        action: Action = "buy"
    elif score <= -0.4:
        action = "sell"
    else:
        action = "hold"

    return SignalResult(action=action, score=round(score, 3), reason="; ".join(reasons))
