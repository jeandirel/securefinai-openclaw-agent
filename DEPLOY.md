# Deployment Guide

Run the agent 24/7 on a free cloud platform so it generates continuous trading logs during the evaluation window (April 20 - May 1, 2026).

## Option 1: Railway (recommended, easiest)

1. Go to https://railway.app and sign in with GitHub.
2. 2. Click "New Project" > "Deploy from GitHub repo".
   3. 3. Select `jeandirel/securefinai-openclaw-agent`.
      4. 4. Railway auto-detects the Dockerfile and starts the build.
         5. 5. Go to the service > "Variables" tab and add:
            6.    - `ALPACA_API_KEY` = your paper-trading key
                  -    - `ALPACA_SECRET_KEY` = your paper-trading secret
                       -    - `ALPACA_BASE_URL` = https://paper-api.alpaca.markets
                            -    - `SYMBOLS` = BTC/USD,ETH/USD,SOL/USD
                                 -    - `POLL_INTERVAL_SEC` = 60
                                      - 6. Redeploy. Check the "Logs" tab to confirm the agent is running.
                                       
                                        7. Free tier: $5 credit/month, enough for ~500 hours of a small container. Set "Sleep after inactivity" to OFF.
                                       
                                        8. ## Option 2: Fly.io
                                       
                                        9. 1. Install `flyctl`: https://fly.io/docs/hands-on/install-flyctl/
                                           2. 2. `fly auth signup` or `fly auth login`
                                              3. 3. In the repo directory:
                                                 4.    ```
                                                          fly launch --no-deploy
                                                          fly secrets set ALPACA_API_KEY=xxx ALPACA_SECRET_KEY=yyy ALPACA_BASE_URL=https://paper-api.alpaca.markets SYMBOLS=BTC/USD,ETH/USD,SOL/USD
                                                          fly deploy
                                                          ```
                                                       4. `fly logs` to watch the agent.
                                                   
                                                       5. Free tier: 3 small VMs always-on.
                                                   
                                                       6. ## Option 3: Render
                                                   
                                                       7. 1. https://render.com > New > Background Worker.
                                                          2. 2. Connect the GitHub repo.
                                                             3. 3. Environment: Docker. Plan: Free.
                                                                4. 4. Add the same environment variables as Railway.
                                                                   5. 5. Deploy.
                                                                     
                                                                      6. ## Option 4: Your own PC (simplest but not 24/7)
                                                                     
                                                                      7. ```
                                                                         git clone https://github.com/jeandirel/securefinai-openclaw-agent
                                                                         cd securefinai-openclaw-agent
                                                                         python -m venv .venv && source .venv/bin/activate
                                                                         pip install -r requirements.txt
                                                                         cp .env.example .env   # edit with your Alpaca keys
                                                                         python -m agent.main
                                                                         ```

                                                                         ## Verifying the agent is alive

                                                                         After a few minutes, check that these files are being written:
                                                                         - `logs/orders.jsonl`
                                                                         - - `logs/equity.csv`
                                                                           - - `logs/portfolio_snapshot.json`
                                                                            
                                                                             - On Railway/Fly/Render, use their log viewer. Locally, tail the files:
                                                                             - ```
                                                                               tail -f logs/equity.csv
                                                                               ```

                                                                               ## Stopping the agent

                                                                               Kill the worker from the cloud dashboard, or Ctrl+C locally.
                                                                               
