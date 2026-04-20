"""Thin wrapper around alpaca-py for trading and market data."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional

import pandas as pd
from alpaca.data.historical import CryptoHistoricalDataClient, StockHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest, StockBarsRequest
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, OrderType, TimeInForce
from alpaca.trading.requests import MarketOrderRequest

from .config import CONFIG


def _parse_timeframe(tf: str) -> TimeFrame:
      tf = tf.lower().replace(" ", "")
      if tf.endswith("min"):
                return TimeFrame(int(tf.replace("min", "")), TimeFrameUnit.Minute)
            if tf.endswith("h") or tf.endswith("hour"):
                      n = int(tf.replace("hour", "").replace("h", ""))
                      return TimeFrame(n, TimeFrameUnit.Hour)
                  if tf in ("1d", "day", "1day"):
                            return TimeFrame(1, TimeFrameUnit.Day)
                        raise ValueError(f"Unsupported timeframe: {tf}")


class AlpacaBroker:
      def __init__(self) -> None:
                CONFIG.validate()
                self.trading = TradingClient(
                    CONFIG.alpaca_api_key,
                    CONFIG.alpaca_secret_key,
                    paper=True,
                )
                if CONFIG.market == "crypto":
                              self.data = CryptoHistoricalDataClient(
                                                CONFIG.alpaca_api_key, CONFIG.alpaca_secret_key
                              )
else:
            self.data = StockHistoricalDataClient(
                              CONFIG.alpaca_api_key, CONFIG.alpaca_secret_key
            )

    # ---------- Account & positions ----------
      def get_equity(self) -> float:
                acc = self.trading.get_account()
                return float(acc.equity)

    def get_cash(self) -> float:
              acc = self.trading.get_account()
              return float(acc.cash)

    def get_positions(self) -> Dict[str, float]:
              positions = self.trading.get_all_positions()
              out: Dict[str, float] = {}
              for p in positions:
                            sym = p.symbol
                            # alpaca returns crypto symbol without slash (e.g. BTCUSD)
                            if CONFIG.market == "crypto" and "/" not in sym:
                                              sym = sym[:-3] + "/" + sym[-3:]
                                          out[sym] = float(p.qty)
                        return out

    def get_position_value(self, symbol: str) -> float:
              try:
                            p = self.trading.get_open_position(self._to_alpaca_symbol(symbol))
                            return float(p.market_value)
except Exception:
            return 0.0

    # ---------- Market data ----------
    def get_bars(self, symbol: str, lookback: int, timeframe: str) -> pd.DataFrame:
              tf = _parse_timeframe(timeframe)
        end = datetime.now(tz=timezone.utc)
        # Rough heuristic for start: lookback * bar size
        minutes_per_bar = {
                      TimeFrameUnit.Minute: 1,
                      TimeFrameUnit.Hour: 60,
                      TimeFrameUnit.Day: 60 * 24,
        }[tf.unit_value] * tf.amount_value
        start = end - timedelta(minutes=minutes_per_bar * (lookback + 5))

        if CONFIG.market == "crypto":
                      req = CryptoBarsRequest(
                                        symbol_or_symbols=[symbol],
                                        timeframe=tf,
                                        start=start,
                                        end=end,
                      )
                      bars = self.data.get_crypto_bars(req)
else:
            req = StockBarsRequest(
                              symbol_or_symbols=[symbol],
                              timeframe=tf,
                              start=start,
                              end=end,
            )
            bars = self.data.get_stock_bars(req)

        df = bars.df
        if df is None or df.empty:
                      return pd.DataFrame()
                  if isinstance(df.index, pd.MultiIndex):
                                df = df.xs(symbol, level=0)
                            return df.tail(lookback)

    # ---------- Orders ----------
    def _to_alpaca_symbol(self, symbol: str) -> str:
              # Crypto: "BTC/USD" accepted by newer alpaca-py versions; else strip slash.
              return symbol

    def submit_market_order(self, symbol: str, qty: float, side: str) -> dict:
              order_side = OrderSide.BUY if side.lower() == "buy" else OrderSide.SELL
              tif = TimeInForce.GTC if CONFIG.market == "crypto" else TimeInForce.DAY
              req = MarketOrderRequest(
                  symbol=self._to_alpaca_symbol(symbol),
                  qty=round(qty, 6),
                  side=order_side,
                  type=OrderType.MARKET,
                  time_in_force=tif,
              )
              order = self.trading.submit_order(req)
              return {
                  "id": str(order.id),
                  "symbol": symbol,
                  "side": side.lower(),
                  "qty": float(order.qty) if order.qty else qty,
                  "status": str(order.status),
              }
      
