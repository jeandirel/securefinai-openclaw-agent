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
                                                                               


---

## H1 evaluation campaign (recommended path)

This section describes the **minimal two-cell deployment** required to test the pre-registered hypothesis H1 of paper Section 5: *the LLM-veto layer reduces realised maximum drawdown by at least 2 pp relative to baseline B3 (rules+risk), at the cost of at most 1 pp in cumulative return*.

You need at minimum:

- Two **separate** Alpaca paper-trading accounts (free, sign up twice with two emails). Account A is the **B3 baseline** (rules+risk only). Account B is the **B3+LLM treatment** (rules+LLM+risk). They must NOT share an API key, otherwise the two arms trade the same equity and the comparison is meaningless.
- One LLM provider key (OpenAI or Anthropic) for the treatment arm only.
- One always-on host. Recommended: Render free Background Worker, or Fly.io free machine. Local laptop works but must stay on for ~11 days continuously.

### Step 1 -- decide the platform

Three deployment files are provided, mutually exclusive:

| Platform | File | Free tier | Notes |
|---|---|---|---|
| Render | `render.yaml` | 512 MB worker, always-on | One-click "New Blueprint", reads two services from the YAML. |
| Fly.io | `fly.toml` | 3 shared-cpu-1x@256MB always-on | Run `fly launch --copy-config` once per arm. |
| Local | `scripts/run_local.sh` | free if you already own a machine | Each arm runs in a detached `tmux` session. |

### Step 2 -- prepare the environment files

For each arm, copy `.env.example` and fill in the credentials for that arm only:

```bash
cp .env.example .env.B3
cp .env.example .env.B3_LLM

# .env.B3 (control)
# ALPACA_API_KEY=<account A>
# ALPACA_SECRET_KEY=<account A>
# LLM_PROVIDER=                  # empty -> rules only

# .env.B3_LLM (treatment)
# ALPACA_API_KEY=<account B>
# ALPACA_SECRET_KEY=<account B>
# LLM_PROVIDER=anthropic         # or openai
# ANTHROPIC_API_KEY=<your key>   # or OPENAI_API_KEY
```

Never commit `.env.B3` or `.env.B3_LLM`; the `.gitignore` already covers `.env*`.

### Step 3 -- launch

#### Option A -- Local (tmux)

```bash
chmod +x scripts/run_local.sh
bash scripts/run_local.sh B3
bash scripts/run_local.sh B3_LLM

# Detach: Ctrl+b then d
# Re-attach: tmux attach -t openclaw-B3
# Stop:      tmux kill-session -t openclaw-B3
```

#### Option B -- Render

1. Push the repo to GitHub (already done if you are reading this from github.com).
2. https://render.com -> New -> Blueprint -> select the repo. Render reads `render.yaml` and creates two background workers.
3. For each worker, open Environment and paste the `ALPACA_API_KEY` / `ALPACA_SECRET_KEY` for the corresponding account. Paste `ANTHROPIC_API_KEY` only on the `openclaw-agent-b3-llm` worker.
4. Both workers auto-deploy on every push to `main`.

#### Option C -- Fly.io

```bash
# Treatment arm
fly launch --copy-config --name openclaw-agent-b3-llm --no-deploy
fly secrets set ALPACA_API_KEY=... ALPACA_SECRET_KEY=... ANTHROPIC_API_KEY=...
fly deploy

# Baseline arm: copy fly.toml -> fly.b3.toml, change app name to
# openclaw-agent-b3 and LLM_PROVIDER="" before launching.
fly launch --copy-config --config fly.b3.toml --name openclaw-agent-b3 --no-deploy
fly secrets set ALPACA_API_KEY=... ALPACA_SECRET_KEY=...
fly deploy --config fly.b3.toml
```

### Step 4 -- monitor cycle count

The H1 stop-rule of paper Section 5 requires `T_min = 500` decision cycles per arm at `Delta_t = 30 min`, i.e. roughly 11 calendar days per arm running continuously.

Quick check (local):

```bash
wc -l logs/B3/orders.jsonl logs/B3_LLM/orders.jsonl
```

On Render / Fly, stream the logs with the dashboard or `fly logs -a openclaw-agent-b3`. The agent prints a one-line summary every cycle, so the line count of stdout is a good proxy.

### Step 5 -- export the equity curves

After T_min cycles, export the daily-equity CSV for each account. The agent already writes `logs/<LABEL>/equity.csv`. If you need to re-export from Alpaca, see `scripts/export_equity.py`.

### Step 6 -- run the H1 test

```bash
python scripts/h1_test.py \
    --equity-csv B3=logs/B3/equity.csv \
    --equity-csv B3_LLM=logs/B3_LLM/equity.csv

# Outputs:
#   results/metrics.json   (machine-readable)
#   results/h1_table.md    (paste directly into paper Section 5)
```

The script honors the same null-reporting rule as the paper: any cell with fewer than 500 cycles is reported as "insufficient data" and not imputed.

### Step 7 -- update the paper

Open `paper/main.tex`, replace the placeholder text in Section 5 with a reference to `results/h1_table.md`, and update `results/metrics.json` (the existing `results/metrics_template.json` is the schema). Then bump `CHANGELOG_REVIEW.md` to `v4 -- post H1 evaluation` and re-compile in Overleaf.

### Important honesty notes

- The bootstrap CIs in `scripts/h1_test.py` are iid, not block-stationary. For the final published version, replace the iid resampling with a stationary block bootstrap (e.g., Politis-Romano with block size `L \approx T^{1/3}`).
- A2 (OpenAI vs Anthropic) and A3 (conservative vs aggressive risk envelope) are out of scope of the minimal H1 campaign. Add them only after H1 has been tested.
- Do **not** reuse the same Alpaca paper account for B3 and B3+LLM. Same account = same equity = no comparison.
- Do **not** restart a worker to "reset" a bad-looking equity curve. That is p-hacking. The pre-registered protocol forbids it.
