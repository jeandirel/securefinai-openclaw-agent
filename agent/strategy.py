"""Strategy: turns signals + portfolio state into concrete orders."""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

import pandas as pd

from .alpaca_client import AlpacaBroker
from .config import CONFIG
from .llm import review
from .signals import SignalResult, compute_signal


@dataclass
class Decision:
    symbol: str
    action: str  # buy / sell / hold
    qty: float
    reason: str
    signal_score: float
    llm_approved: Optional[bool]


def _last_price(df: pd.DataFrame) -> float:
    return float(df["close"].iloc[-1])


def _recent_stats(df: pd.DataFrame) -> dict:
    close = df["close"].astype(float)
    return {
        "last": round(close.iloc[-1], 4),
        "ret_1h": round(close.pct_change(4).iloc[-1] or 0.0, 4),
        "ret_24h": round(close.pct_change(96).iloc[-1] or 0.0, 4),
        "vol_24h": round(close.pct_change().tail(96).std() or 0.0, 4),
    }


def decide(broker: AlpacaBroker) -> List[Decision]:
    decisions: List[Decision] = []
    equity = broker.get_equity()
    cash = broker.get_cash()
    positions = broker.get_positions()

    max_notional_per_asset = equity * CONFIG.max_position_pct

    for symbol in CONFIG.universe:
        df = broker.get_bars(symbol, CONFIG.lookback_bars, CONFIG.bar_timeframe)
        if df.empty:
            decisions.append(Decision(symbol, "hold", 0.0, "no data", 0.0, None))
            continue

        sig: SignalResult = compute_signal(df)
        price = _last_price(df)
        held_qty = positions.get(symbol, 0.0)
        held_value = held_qty * price

        # Optional LLM review
        llm_ok: Optional[bool] = None
        llm_note = ""
        if sig.action in ("buy", "sell"):
            dec = review(symbol, sig, _recent_stats(df))
            if dec is not None:
                llm_ok = dec.approve
                llm_note = f" | LLM: {dec.rationale}"
                if not dec.approve:
                    decisions.append(
                        Decision(
                            symbol,
                            "hold",
                            0.0,
                            f"LLM vetoed: {sig.reason}{llm_note}",
                            sig.score,
                            llm_ok,
                        )
                    )
                    continue

        if sig.action == "buy":
            remaining_budget = max_notional_per_asset - held_value
            if remaining_budget <= 10 or cash < 10:
                decisions.append(
                    Decision(
                        symbol,
                        "hold",
                        0.0,
                        f"at cap or no cash ({sig.reason}){llm_note}",
                        sig.score,
                        llm_ok,
                    )
                )
                continue

            notional = min(remaining_budget, cash * 0.95)
            qty = notional / price
            decisions.append(
                Decision(symbol, "buy", qty, f"{sig.reason}{llm_note}", sig.score, llm_ok)
            )
            cash -= notional
        elif sig.action == "sell" and held_qty > 0:
            decisions.append(
                Decision(symbol, "sell", held_qty, f"{sig.reason}{llm_note}", sig.score, llm_ok)
            )
        else:
            decisions.append(
                Decision(symbol, "hold", 0.0, sig.reason, sig.score, llm_ok)
            )

    return decisions
