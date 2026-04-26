#!/usr/bin/env bash
# scripts/run_local.sh -- launch one OpenClaw-Agent ablation cell inside a
# detached tmux session so it survives an SSH disconnect.
#
# Usage:
#   bash scripts/run_local.sh B3        # rules+risk only (control)
#   bash scripts/run_local.sh B3_LLM    # rules+LLM+risk (treatment)
#
# Each cell needs ITS OWN .env file with a different Alpaca paper account:
#   .env.B3         -> account A keys, LLM_PROVIDER=
#   .env.B3_LLM     -> account B keys, LLM_PROVIDER=anthropic, ANTHROPIC_API_KEY=...
#
# After launch, detach with Ctrl-b then d. To re-attach later:
#   tmux attach -t openclaw-${LABEL}
#
# To stop: tmux kill-session -t openclaw-${LABEL}

set -euo pipefail

LABEL="${1:-}"
if [[ -z "${LABEL}" ]]; then
  echo "Usage: $0 LABEL    (e.g. B3 or B3_LLM)" >&2
  exit 1
fi

ENV_FILE=".env.${LABEL}"
if [[ ! -f "${ENV_FILE}" ]]; then
  echo "Missing ${ENV_FILE}. Copy .env.example to ${ENV_FILE} and fill in" >&2
  echo "the credentials for THIS ablation cell only." >&2
  exit 2
fi

if ! command -v tmux >/dev/null 2>&1; then
  echo "tmux is required. On Debian/Ubuntu: sudo apt-get install tmux" >&2
  echo "On macOS: brew install tmux" >&2
  exit 3
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 not found in PATH" >&2
  exit 4
fi

SESSION="openclaw-${LABEL}"

# Idempotent: kill an old session with the same name if any.
if tmux has-session -t "${SESSION}" 2>/dev/null; then
  echo "Session ${SESSION} already exists. Killing it before relaunch."
  tmux kill-session -t "${SESSION}"
fi

# Create a per-cell logs directory so cells don't overwrite each other.
LOGDIR="logs/${LABEL}"
mkdir -p "${LOGDIR}"

# Launch the agent inside tmux. The shell loads the env file, then execs
# the agent. ABLATION_LABEL is exposed for downstream scripts.
tmux new-session -d -s "${SESSION}" \
  "set -a; source '${ENV_FILE}'; set +a; \
   export ABLATION_LABEL='${LABEL}'; \
   export LOG_DIR='${LOGDIR}'; \
   echo 'Starting OpenClaw-Agent cell ${LABEL} in ${LOGDIR}'; \
   python3 -m agent.main 2>&1 | tee -a '${LOGDIR}/stdout.log'"

echo "Started tmux session: ${SESSION}"
echo "  Re-attach: tmux attach -t ${SESSION}"
echo "  Stop:      tmux kill-session -t ${SESSION}"
echo "  Logs:      ${LOGDIR}/"
