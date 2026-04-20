"""Main decision loop for the OpenClaw paper-trading agent."""
from __future__ import annotations

import signal
import sys
import time
from datetime import datetime, timezone

from .alpaca_client import AlpacaBroker
from .config import CONFIG
from .logger import append_equity, log_info, log_order
from .strategy import decide

_RUNNING = True


def _handle_sigterm(signum, frame):  # noqa: ANN001
      global _RUNNING
      _RUNNING = False
      log_info(f"Received signal {signum}, shutting down after current cycle...")


def run_once(broker: AlpacaBroker) -> None:
      equity = broker.get_equity()
      cash = broker.get_cash()
      append_equity(equity, cash)
      log_info(f"Equity={equity:.2f} Cash={cash:.2f}")

    decisions = decide(broker)
    for d in decisions:
              log_info(
                            f"{d.symbol}: {d.action} qty={d.qty:.6f} score={d.signal_score} "
                            f"llm={d.llm_approved} reason={d.reason}"
              )
              if d.action in ("buy", "sell") and d.qty > 0:
                            try:
                                              resp = broker.submit_market_order(d.symbol, d.qty, d.action)
                                              log_order(
                                                  symbol=d.symbol,
                                                  side=d.action,
                                                  qty=resp["qty"],
                                                  status=resp["status"],
                                                  order_id=resp["id"],
                                                  reason=d.reason,
                                                  signal_score=d.signal_score,
                                                  llm_approved=d.llm_approved,
                                              )
except Exception as e:
                log_info(f"ORDER FAILED {d.symbol} {d.action} {d.qty}: {e}")
                log_order(
                                      symbol=d.symbol,
                                      side=d.action,
                                      qty=d.qty,
                                      status=f"error: {e}",
                                      reason=d.reason,
                                      signal_score=d.signal_score,
                                      llm_approved=d.llm_approved,
                )


def main() -> int:
      signal.signal(signal.SIGINT, _handle_sigterm)
      signal.signal(signal.SIGTERM, _handle_sigterm)

    log_info("Starting SecureFinAI OpenClaw Agent")
    log_info(
              f"Market={CONFIG.market} Universe={CONFIG.universe} "
              f"Interval={CONFIG.decision_interval_min}min LLM={CONFIG.llm_provider or 'off'}"
    )

    broker = AlpacaBroker()
    log_info(f"Connected to Alpaca paper. Starting equity = {broker.get_equity():.2f}")

    interval_sec = CONFIG.decision_interval_min * 60

    while _RUNNING:
              cycle_start = time.time()
              try:
                            run_once(broker)
except Exception as e:
            log_info(f"Cycle error: {e!r}")

        # Sleep until next cycle, checking the running flag frequently.
        elapsed = time.time() - cycle_start
        to_sleep = max(5.0, interval_sec - elapsed)
        log_info(f"Sleeping {to_sleep:.0f}s until next cycle")
        step = 5
        slept = 0.0
        while _RUNNING and slept < to_sleep:
                      time.sleep(min(step, to_sleep - slept))
                      slept += step

    log_info("Agent stopped.")
    return 0


if __name__ == "__main__":
      sys.exit(main())
  
