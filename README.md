# OpenClaw-Agent

A risk-aware, LLM-assisted paper-trading agent for crypto, built on the Alpaca paper-trading API.

## Project title

**OpenClaw-Agent: A Risk-Aware LLM-Assisted Trading Agent for Secure Financial AI**

## Academic context

This repository is the artifact for the **PGE5 "AI in Finance" term paper** at **Aivancity** (school year 2025-2026). The project is inspired by the **SecureFinAI Contest 2026, Task V (OpenClaw / Alpaca)** and is intended to support an academic submission (NeurIPS-style preprint, OpenReview, HAL, arXiv cross-post).

The agent is **paper-trading only**. It is not financial advice and must not be used with real capital.

## Research contribution

The contribution of this term paper is threefold:

1. An open-source reference implementation of a risk-aware, LLM-assisted paper-trading agent on top of the Alpaca API.
2. An experimental protocol aligned with SecureFinAI Contest 2026, Task V, including the metrics to be reported and the structured logging required for reproducibility.
3. An explicit *honest reporting* policy: when ground-truth metrics are not yet available from the live paper-trading run, they are reported as `null` rather than fabricated.

## System overview

OpenClaw-Agent runs a periodic decision loop. At each step it pulls recent OHLCV bars from Alpaca, computes technical signals, optionally consults an LLM as a *review-only* filter, applies a hard risk envelope, and submits paper orders. Every cycle is logged as line-delimited JSON for offline metric computation.

## Architecture

The system is organised into five clearly separated layers:

1. **Broker layer** (`agent/alpaca_client.py`) -- thin abstraction around the Alpaca REST API for crypto paper trading.
2. **Signal layer** (`agent/signals.py`) -- deterministic technical indicators (EMA crossover, RSI, momentum) that produce a bounded score in `[-1, 1]` and a categorical action.
3. **Strategy layer** (`agent/strategy.py`) -- aggregates signals, sizes orders, and produces `Decision` objects.
4. **LLM filter** (`agent/llm.py`) -- optional review step. The LLM can only veto or confirm a candidate order; it cannot originate trades or change sizing.
5. **Risk and logging layer** (`agent/logger.py`, config in `agent/config.py`) -- enforces per-position caps, gross-exposure caps, stop-loss, and take-profit, and persists structured logs.

The main loop lives in `agent/main.py` and is deployable as a long-running container (`Dockerfile`, `Procfile`).

## Installation

```bash
git clone https://github.com/jeandirel/securefinai-openclaw-agent.git
cd securefinai-openclaw-agent
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

## Configuration

Copy `.env.example` to `.env` and fill in your **Alpaca paper** credentials. **Never commit your real `.env`.**

```bash
cp .env.example .env
```

Key environment variables:

- `ALPACA_API_KEY`, `ALPACA_SECRET_KEY`, `ALPACA_BASE_URL` -- Alpaca paper credentials.
- `MARKET` -- `crypto` or `stock`.
- `CRYPTO_UNIVERSE` / `STOCK_UNIVERSE` -- comma-separated symbols.
- `DECISION_INTERVAL_MIN`, `LOOKBACK_BARS`, `BAR_TIMEFRAME` -- loop and data settings.
- `MAX_POSITION_PCT`, `STOP_LOSS_PCT`, `TAKE_PROFIT_PCT`, `MAX_GROSS_EXPOSURE_PCT` -- risk envelope.
- `LLM_PROVIDER`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY` -- optional LLM filter (leave provider empty for pure-rules mode).

## How to run

Pure-rules mode (no LLM):

```bash
python -m agent.main
```

With the LLM filter, set `LLM_PROVIDER=openai` or `LLM_PROVIDER=anthropic` in `.env` first, then run the same command.

## How to generate logs and results

The agent writes structured logs to `logs/` (created at runtime, not committed). Helper scripts:

```bash
python scripts/snapshot_portfolio.py   # one-shot equity / positions snapshot
python scripts/export_equity.py        # export the equity curve from logs
```

Metrics defined in `results/README.md` must be computed from the **actual** Alpaca paper-trading logs and written into `results/metrics_template.json`. Do not replace `null` values with invented numbers.

## Project structure

```
securefinai-openclaw-agent/
├── agent/                 # decision loop, signals, strategy, LLM filter, logger
├── paper/                 # NeurIPS-style paper (main.tex, references.bib)
├── reviews/               # AI reviews (ChatGPT, Claude, Grok, Gemini Think)
├── results/               # metrics schema + computed metrics
├── scripts/               # utility scripts (equity export, snapshots)
├── .env.example           # configuration template (no secrets)
├── .gitignore
├── CITATION.cff
├── DEPLOY.md
├── Dockerfile
├── LICENSE
├── Procfile
├── README.md
├── SUBMISSION_CHECKLIST.md
└── requirements.txt
```

## Reproducibility notes

- All configuration is environment-variable driven; no hard-coded credentials or magic numbers in the code.
- Logs are line-delimited JSON and are sufficient to recompute every reported metric offline.
- The signal layer is deterministic and unit-testable independently of any LLM.
- The LLM filter is *advisory only* and can never originate or up-size a trade.
- The repository pins minimum versions in `requirements.txt` and provides a `Dockerfile` for environment reproduction.

## Limitations

- Paper trading only: transaction costs, slippage, and order-book impact are simplified by Alpaca paper.
- Small crypto universe (`BTC/USD`, `ETH/USD`, `SOL/USD` by default).
- LLM filter is sensitive to prompt wording and provider availability; behaviour may drift across model versions.
- Empirical results depend on the duration of the live paper-trading run.

## Ethics note

This project is a **research and educational artifact**. It does not provide financial advice and must not be used with real capital. All trading is performed in **Alpaca paper** mode. API keys are stored only in the user's local `.env` and are excluded from the repository via `.gitignore`. The LLM filter is constrained to a review-only role and cannot, by construction, originate trades. No personal data is collected.

## Term paper submission checklist

See [`SUBMISSION_CHECKLIST.md`](SUBMISSION_CHECKLIST.md) for the full checklist (GitHub public, README complete, paper compiled, reviews collected, OpenReview / HAL / arXiv submitted, no fake results, etc.).

## Links

- **GitHub repository:** https://github.com/jeandirel/securefinai-openclaw-agent
- **OpenReview submission:** *to be added after submission*
- **HAL submission:** *to be added after submission*
- **arXiv cross-post:** *to be added after submission*
- **ChatGPT review:** *to be added in `reviews/README.md`*
- **Claude review:** *to be added in `reviews/README.md`*
- **Grok review:** *to be added in `reviews/README.md`*
- **Gemini Think review:** *to be added in `reviews/README.md`*
