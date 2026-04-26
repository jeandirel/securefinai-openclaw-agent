"""Take an end-of-evaluation snapshot of the Alpaca paper portfolio.

Produces `logs/portfolio_snapshot.json` with account equity, cash, positions
and the last price seen, ready to submit to the contest.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from agent.alpaca_client import AlpacaBroker
from agent.config import CONFIG


def main() -> int:
    broker = AlpacaBroker()
    acc = broker.trading.get_account()
    positions = broker.trading.get_all_positions()

    snapshot = {
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        "market": CONFIG.market,
        "equity": float(acc.equity),
        "cash": float(acc.cash),
        "buying_power": float(acc.buying_power),
        "last_equity": float(acc.last_equity),
        "positions": [
            {
                "symbol": p.symbol,
                "qty": float(p.qty),
                "avg_entry_price": float(p.avg_entry_price),
                "current_price": float(p.current_price),
                "market_value": float(p.market_value),
                "unrealized_pl": float(p.unrealized_pl),
                "unrealized_plpc": float(p.unrealized_plpc),
            }
            for p in positions
        ],
    }

    out = Path("logs/portfolio_snapshot.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2)

    print(f"Snapshot written to {out}")
    print(json.dumps(snapshot, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
