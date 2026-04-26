"""Compute contest metrics from logs/equity.csv.

Primary: Cumulative Return (CR)
Secondary: Sharpe Ratio (SR), Maximum Drawdown (MD),
           Daily Volatility (DV), Annualized Volatility (AV)
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd


def compute_metrics(equity_csv: Path) -> dict:
    df = pd.read_csv(equity_csv, parse_dates=["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)

    # Daily equity: take last observation per UTC day
    if df["timestamp"].dt.tz is not None:
        df["date"] = df["timestamp"].dt.tz_convert("UTC").dt.date
    else:
        df["date"] = df["timestamp"].dt.date
    daily = df.groupby("date")["equity"].last().reset_index()

    start_eq = float(daily["equity"].iloc[0])
    end_eq = float(daily["equity"].iloc[-1])
    cr = end_eq / start_eq - 1

    daily_ret = daily["equity"].pct_change().dropna()
    dv = float(daily_ret.std() or 0.0)
    av = dv * np.sqrt(252)
    sr = float((daily_ret.mean() / dv) * np.sqrt(252)) if dv > 0 else 0.0

    running_max = daily["equity"].cummax()
    drawdown = daily["equity"] / running_max - 1
    md = float(drawdown.min() or 0.0)

    return {
        "days": int(len(daily)),
        "start_equity": start_eq,
        "end_equity": end_eq,
        "cumulative_return": round(cr, 6),
        "sharpe_ratio": round(sr, 4),
        "max_drawdown": round(md, 6),
        "daily_volatility": round(dv, 6),
        "annualized_volatility": round(av, 6),
    }


def main() -> int:
    equity_csv = Path("logs/equity.csv")
    if not equity_csv.exists():
        print(f"{equity_csv} not found. Run the agent first.")
        return 1

    metrics = compute_metrics(equity_csv)
    out = Path("logs/metrics.json")
    with out.open("w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print(json.dumps(metrics, indent=2))
    print(f"\nWritten to {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
