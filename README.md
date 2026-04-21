> **Academic Context**
> >
> >> This repository was developed as a course deliverable for **PGE5 - AI in Finance** at aivancity (instructor: Mostapha Benhenda, Spring 2026). It is inspired by **Task V (Agentic Trading Using OpenClaw)** of the SecureFinAI Contest 2026 organized by the Open Finance Lab.
> >> >
> >> >> The project was built after the official contest deadlines had passed (Solution Submission: April 20, 2026; Paper Submission: March 10, 2026). It is therefore not a formal contest entry but a standalone academic project that follows the Task V specification end-to-end: LLM-assisted agent design, Alpaca paper trading on the crypto market (BTC/USD, ETH/USD, SOL/USD), contest-compliant log format (`orders.jsonl`, `equity.csv`, `portfolio_snapshot.json`), and a scientific paper (`paper/article.md`) covering motivation, method, experiments, and discussion.
> >> >> >
> >> >> >> Reference: SecureFinAI Contest 2026 — https://open-finance-lab.github.io/SecureFinAI_Contest_2026/
> >> >> >>
> >> >> >> # SecureFinAI OpenClaw Agent (Task V)

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
               
                - ## Project structure
               
                - ```
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

                  ## Getting started — step by step

                  Follow these 8 steps to go from a fresh clone to a contest-ready submission.

                  ### 1. Create an Alpaca paper trading account

                  - Sign up at <https://alpaca.markets>.
                  - - Switch the dashboard to **Paper trading** mode.
                    - - Open *API Keys* and generate a new key pair. Copy the **API Key** and **Secret Key** right away (the secret is shown only once).
                     
                      - ### 2. Clone the repo and install dependencies
                     
                      - ```bash
                        git clone https://github.com/jeandirel/securefinai-openclaw-agent.git
                        cd securefinai-openclaw-agent
                        python -m venv .venv
                        source .venv/bin/activate          # Windows: .venv\Scripts\activate
                        pip install -r requirements.txt
                        ```

                        ### 3. Configure your `.env`

                        ```bash
                        cp .env.example .env
                        ```

                        Edit `.env` and paste your Alpaca paper keys:

                        ```
                        ALPACA_API_KEY=PK...
                        ALPACA_SECRET_KEY=...
                        MARKET=crypto
                        ```

                        Never commit the real `.env` — it is already protected by `.gitignore`.

                        ### 4. (Optional) Enable the LLM layer

                        Still in `.env`, set either:

                        ```
                        LLM_PROVIDER=openai
                        OPENAI_API_KEY=sk-...
                        ```

                        or

                        ```
                        LLM_PROVIDER=anthropic
                        ANTHROPIC_API_KEY=sk-ant-...
                        ```

                        Leave `LLM_PROVIDER` empty to run in pure-rules mode (no external API calls).

                        ### 5. Run the agent

                        ```bash
                        python -m agent.main
                        ```

                        The agent takes a decision every `DECISION_INTERVAL_MIN` minutes (default 30).
                        Run it on a machine that stays online. Useful options:

                        - Linux/Mac in the background: `nohup python -m agent.main > logs/stdout.log 2>&1 &`
                        - - Small VPS (DigitalOcean / Hetzner / OVH) running a `tmux` or `systemd` service
                          - - Any always-on desktop
                           
                            - ### 6. Monitor the agent
                           
                            - - Tail the structured log: `tail -f logs/agent.log`
                              - - Inspect orders: `tail -f logs/orders.jsonl`
                                - - Watch your equity live on the Alpaca paper dashboard
                                  - - The agent is resilient: transient errors are logged and the next cycle keeps running
                                   
                                    - ### 7. On May 1 — stop and export
                                   
                                    - 1. Stop the agent with `Ctrl+C` (or `kill <pid>` if running in background).
                                      2. 2. Compute contest metrics (CR, Sharpe, Max Drawdown, Daily / Annualized Volatility):
                                        
                                         3.    ```bash
                                                  python scripts/export_equity.py
                                                  ```

                                               3. Take the final portfolio snapshot:
                                           
                                               4.    ```bash
                                                        python scripts/snapshot_portfolio.py
                                                        ```

                                                        This writes `logs/portfolio_snapshot.json`.

                                                 ### 8. Submit to the contest

                                           Upload these files via the official SecureFinAI Contest 2026 submission form:

                                         - `logs/orders.jsonl`
                                         - - `logs/equity.csv`
                                           - - `logs/portfolio_snapshot.json`
                                            
                                             - You can also attach `logs/metrics.json` and this repo's URL for reproducibility.
                                            
                                             - ## Contest compliance
                                            
                                             - - Time period: **April 20 – May 1, 2026**
                                               - - Initial capital: **$100,000** (Alpaca default paper balance)
                                                 - - Market: **crypto** (single account). For the stock track, create a second Alpaca account and set `MARKET=stock`.
                                                  
                                                   - ## Troubleshooting
                                                  
                                                   - - **Alpaca symbol format** (`BTC/USD` vs `BTCUSD`): behavior depends on the `alpaca-py` version. If you see a symbol error, upgrade: `pip install -U "alpaca-py>=0.30"`, or edit `_to_alpaca_symbol` in `agent/alpaca_client.py`.
                                                     - - **Not enough bars** on the first cycle: lower `LOOKBACK_BARS` or wait a few cycles so the data client warms up.
                                                       - - **Rate limits** from the LLM: lower `DECISION_INTERVAL_MIN` back up or disable `LLM_PROVIDER` temporarily.
                                                        
                                                         - ## Contest links
                                                        
                                                         - - Contest site: <https://open-finance-lab.github.io/SecureFinAI_Contest_2026/>
                                                           - - Discord: <https://discord.gg/dJY5cKzmkv>
                                                             - - Email: finrlcontest@gmail.com
                                                              
                                                               - ## License
                                                              
                                                               - MIT — see `LICENSE`.
                                                               - 
