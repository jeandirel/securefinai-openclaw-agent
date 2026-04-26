"""Structured logging: orders.jsonl + equity.csv as required by the contest."""
from __future__ import annotations

import csv
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

LOG_DIR = Path(os.getenv("LOG_DIR", "logs"))
ORDERS_FILE = LOG_DIR / "orders.jsonl"
EQUITY_FILE = LOG_DIR / "equity.csv"
AGENT_LOG = LOG_DIR / "agent.log"


def _now_iso() -> str:
    return datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _ensure_dir() -> None:
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def log_info(msg: str) -> None:
    _ensure_dir()
    line = f"[{_now_iso()}] {msg}"
    print(line, flush=True)
    with AGENT_LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def log_order(
      symbol: str,
      side: str,
      qty: float,
      status: str,
      order_id: Optional[str] = None,
      reason: str = "",
      signal_score: float = 0.0,
      llm_approved: Optional[bool] = None,
      price_hint: Optional[float] = None,
) -> None:
    _ensure_dir()
    payload = {
        "timestamp": _now_iso(),
        "symbol": symbol,
        "side": side,
        "qty": qty,
        "status": status,
        "order_id": order_id,
        "reason": reason,
        "signal_score": signal_score,
        "llm_approved": llm_approved,
        "price_hint": price_hint,
    }
    with ORDERS_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload) + "\n")


def append_equity(equity: float, cash: float) -> None:
    _ensure_dir()
    header_needed = not EQUITY_FILE.exists()
    with EQUITY_FILE.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if header_needed:
            writer.writerow(["timestamp", "equity", "cash"])
        writer.writerow([_now_iso(), round(equity, 2), round(cash, 2)])
