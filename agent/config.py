"""Configuration loaded from environment variables."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import List, Optional

from dotenv import load_dotenv

load_dotenv()


def _split(value: str) -> List[str]:
    return [s.strip() for s in value.split(",") if s.strip()]


@dataclass
class Config:
    # Alpaca
    alpaca_api_key: str = field(default_factory=lambda: os.getenv("ALPACA_API_KEY", ""))
    alpaca_secret_key: str = field(default_factory=lambda: os.getenv("ALPACA_SECRET_KEY", ""))
    alpaca_base_url: str = field(default_factory=lambda: os.getenv("ALPACA_BASE_URL", "https://paper-api.alpaca.markets"))

    # Market
    market: str = field(default_factory=lambda: os.getenv("MARKET", "crypto").lower())
    crypto_universe: List[str] = field(default_factory=lambda: _split(os.getenv("CRYPTO_UNIVERSE", "BTC/USD,ETH/USD,SOL/USD")))
    stock_universe: List[str] = field(default_factory=lambda: _split(os.getenv("STOCK_UNIVERSE", "AAPL,MSFT,NVDA,GOOGL,TSLA,AMZN,META,SPY")))

    # Decision loop
    decision_interval_min: int = field(default_factory=lambda: int(os.getenv("DECISION_INTERVAL_MIN", "30")))
    lookback_bars: int = field(default_factory=lambda: int(os.getenv("LOOKBACK_BARS", "200")))
    bar_timeframe: str = field(default_factory=lambda: os.getenv("BAR_TIMEFRAME", "15Min"))

    # Risk
    max_position_pct: float = field(default_factory=lambda: float(os.getenv("MAX_POSITION_PCT", "0.25")))
    stop_loss_pct: float = field(default_factory=lambda: float(os.getenv("STOP_LOSS_PCT", "0.03")))
    take_profit_pct: float = field(default_factory=lambda: float(os.getenv("TAKE_PROFIT_PCT", "0.06")))
    max_gross_exposure_pct: float = field(default_factory=lambda: float(os.getenv("MAX_GROSS_EXPOSURE_PCT", "0.9")))

    # LLM
    llm_provider: Optional[str] = field(default_factory=lambda: (os.getenv("LLM_PROVIDER") or "").lower() or None)
    openai_api_key: Optional[str] = field(default_factory=lambda: os.getenv("OPENAI_API_KEY") or None)
    openai_model: str = field(default_factory=lambda: os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    anthropic_api_key: Optional[str] = field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY") or None)
    anthropic_model: str = field(default_factory=lambda: os.getenv("ANTHROPIC_MODEL", "claude-3-5-haiku-latest"))
    # Groq (free tier, OpenAI-compatible API)
    groq_api_key: Optional[str] = field(default_factory=lambda: os.getenv("GROQ_API_KEY") or None)
    groq_model: str = field(default_factory=lambda: os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"))
    groq_base_url: str = field(default_factory=lambda: os.getenv("GROQ_BASE_URL", "https://api.groq.com/openai/v1"))

    @property
    def universe(self) -> List[str]:
        return self.crypto_universe if self.market == "crypto" else self.stock_universe

    def validate(self) -> None:
        if not self.alpaca_api_key or not self.alpaca_secret_key:
            raise RuntimeError("Missing ALPACA_API_KEY / ALPACA_SECRET_KEY in .env")
        if self.market not in ("crypto", "stock"):
            raise RuntimeError(f"MARKET must be 'crypto' or 'stock', got {self.market}")


CONFIG = Config()
