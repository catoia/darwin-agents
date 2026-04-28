#!/usr/bin/env bash
# scripts/heartbeat.sh
#
# The engine that keeps the ecosystem alive.
# Invokes every alive project agent to do its daily work,
# then optionally runs the weekly God evaluation cycle.
#
# Run daily via cron:
#   0 9 * * * /Users/nunocadete/darwin-agents/scripts/heartbeat.sh >> /Users/nunocadete/darwin-agents/logs/heartbeat.log 2>&1
#
# Weekly eval runs automatically on Mondays (or set FORCE_EVAL=1 to force).

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
REGISTRY_FILE="$REPO_ROOT/registry.json"

# Load env vars (credentials for CF, Stripe, AdSense, etc.)
if [[ -f "$REPO_ROOT/.env" ]]; then
  # shellcheck disable=SC1090
  set -a; source "$REPO_ROOT/.env"; set +a
fi
LOG_DIR="$REPO_ROOT/logs"
mkdir -p "$LOG_DIR"

DATE=$(date -u +"%Y-%m-%d")
DOW=$(date +"%u")  # 1=Monday ... 7=Sunday
NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

echo "=== Darwin heartbeat: $NOW ==="

cd "$REPO_ROOT"

# ── Step 1: God Agent does its daily work ─────────────────────────────────────
# On Mondays: full evaluation cycle (fitness scoring, kill/clone selection)
# Other days: poke cycle (stir projects, check health, fill fleet gaps)
if [[ "$DOW" == "1" || "${FORCE_EVAL:-0}" == "1" ]]; then
  echo "[heartbeat] Monday — God running weekly evaluation cycle..."
  npx tsx god/god-agent.ts evaluate
else
  echo "[heartbeat] Weekday — God running daily poke cycle..."
  npx tsx god/god-agent.ts poke
fi

# ── Step 2: Wake up every alive project agent ─────────────────────────────────
# God has already written fresh instructions to each project's inbox.md (in step 1).
# Now we invoke each project agent so it reads the inbox and does its daily work.
echo "[heartbeat] Waking up project agents..."

ALIVE_IDS=$(python3 -c "
import json
reg = json.load(open('$REGISTRY_FILE'))
ids = [p['id'] for p in reg.get('projects', []) if p.get('status') == 'alive']
print('\n'.join(ids))
" 2>/dev/null || true)

if [[ -z "$ALIVE_IDS" ]]; then
  echo "[heartbeat] No alive projects yet — God seed should have started something."
  exit 0
fi

for PROJECT_ID in $ALIVE_IDS; do
  PROJECT_DIR="$REPO_ROOT/projects/$PROJECT_ID"
  if [[ ! -d "$PROJECT_DIR" ]]; then
    echo "[heartbeat] WARNING: missing dir for $PROJECT_ID, skipping"
    continue
  fi

  echo "[heartbeat] Invoking $PROJECT_ID..."

  # Fetch latest metrics so the agent has fresh numbers to reason about
  bash "$REPO_ROOT/scripts/fetch-metrics.sh" "$PROJECT_ID" 2>&1 \
    | sed "s/^/  [metrics:$PROJECT_ID] /" || true

  # Invoke the project agent (reads inbox + runs its default work loop)
  pi --no-session \
     --provider github-copilot \
     --model claude-sonnet-4.6 \
     --context-files "$PROJECT_DIR/AGENTS.md" \
     --extension "$REPO_ROOT/.pi/extensions/human-tasks.ts" \
     --skill "$REPO_ROOT/.pi/skills/deploy-cloudflare/SKILL.md" \
     --prompt-template "$REPO_ROOT/.pi/prompts/spawn-task.md" \
     -p "Daily work session. Check inbox.md first, then run your default work loop. Be decisive and commit before exiting." \
     2>&1 | sed "s/^/  [$PROJECT_ID] /" &

done

echo "[heartbeat] Waiting for project agents to complete..."
wait
echo "[heartbeat] All project agents done."

# ── Step 3: Commit everything ──────────────────────────────────────────────────
if git diff --quiet && git diff --staged --quiet; then
  echo "[heartbeat] No file changes to commit."
else
  git add -A
  git commit -m "heartbeat($DATE): daily agent work + metrics"
  git push origin main
  echo "[heartbeat] Committed and pushed."
fi

echo "=== Heartbeat complete: $(date -u +"%Y-%m-%dT%H:%M:%SZ") ==="
