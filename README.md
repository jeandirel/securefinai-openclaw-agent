# SecureFinAI OpenClaw Agent (Task V)

LLM-assisted crypto paper-trading agent for the **SecureFinAI Contest 2026 – Task V (OpenClaw / Alpaca)**.

The agent trades on an Alpaca **paper** account, logs every decision and order, and produces the files required by the contest:

- `logs/orders.jsonl` — time-ordered trading actions
- - `logs/equity.csv`  — daily equity curve
  - - `logs/portfolio_snapshot.json` — final portfolio snapshot
   
    - ## Features
   
    - - Crypto market (24/7) — default universe: `BTC/USD`, `ETH/USD`, `SOL/USD`
      - - Hybrid strategy: technical signals (EMA crossover + RSI + momentum) with an optional LLM "veto" layer
        - - Conservative risk management: max 25% of equity per asset, 3% stop-loss, 6% take-profit
          - - Structured logging in the exact format required by the contest
            - - Works out-of-the-box **without** any LLM key (pure rules mode)
              - - Optional OpenAI or Anthropic hook for the LLM reasoning layer
               
                - ## Quickstart
               
                - ```bash
                  git clone https://github.com/jeandirel/securefinai-openclaw-agent.git
                  cd securefinai-openclaw-agent
                  python -m venv .venv && source .venv/bin/activate   # on Windows: .venv\Scripts\activate
                  pip install -r requirements.txt
                  cp .env.example .env
                  # edit .env and fill ALPACA_API_KEY / ALPACA_SECRET_KEY (paper account)
                  python -m agent.main
                  ```

                  The agent runs a decision loop every `DECISION_INTERVAL_MIN` minutes (default 30) until you stop it (Ctrl+C).

                  ## Project structure

                  ```
                  securefinai-openclaw-agent/
                  ├── README.md
                  ├── requirements.txt
                  ├── .env.example
                  ├── .gitignore
                  ├── LICENSE
                  ├── agent/
                  │   ├── __init__.py
                  │   ├── config.py
                  │   ├── alpaca_client.py
                  │   ├── data.py
                  │   ├── signals.py
                  │   ├── llm.py
                  │   ├── strategy.py
                  │   ├── logger.py
                  │   └── main.py
                  ├── scripts/
                  │   ├── export_equity.py
                  │   └── snapshot_portfolio.py
                  └── logs/            # created at runtime
                  ```

                  ## Contest compliance

                  - Time period: **April 20 – May 1, 2026**
                  - - Initial capital: **$100,000** (Alpaca default paper balance)
                    - - Market: **crypto** (single account). For the stock track, create a second Alpaca account and set `MARKET=stock`.
                     
                      - ## What you must do yourself
                     
                      - 1. Create an Alpaca **paper** trading account at <https://alpaca.markets>.
                        2. 2. Copy your paper API key + secret into `.env`.
                           3. 3. (Optional) Add an `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` to enable the LLM layer.
                              4. 4. Run `python -m agent.main` on a machine that stays online (or a small VPS / Colab with a keep-alive).
                                 5. 5. On May 1, run `python scripts/snapshot_portfolio.py` and submit the three log files + snapshot to the contest form.
                                   
                                    6. ## License
                                   
                                    7. MIT — see `LICENSE`.
                                    8. 
