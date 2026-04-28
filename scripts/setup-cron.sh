#!/usr/bin/env bash
# scripts/setup-cron.sh
#
# Installs the daily heartbeat cron job on macOS/Linux.
# Run once after cloning the repo.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
HEARTBEAT="$REPO_ROOT/scripts/heartbeat.sh"
LOG="$REPO_ROOT/logs/heartbeat.log"
NODE_BIN="$(dirname "$(which node)")"

# Ensure the heartbeat script is executable
chmod +x "$HEARTBEAT"
chmod +x "$REPO_ROOT/scripts/fetch-metrics.sh"

# Build the cron line: run daily at 09:00 local time
# PATH includes node/npm so npx and pi are found
CRON_LINE="0 9 * * * PATH=\"$NODE_BIN:\$PATH\" $HEARTBEAT >> $LOG 2>&1"

echo "Installing cron job..."
echo "  Schedule: daily at 09:00"
echo "  Script:   $HEARTBEAT"
echo "  Log:      $LOG"
echo ""

# Add to crontab (idempotent — removes old entry first)
TMPFILE=$(mktemp)
crontab -l 2>/dev/null | grep -v "darwin-agents/scripts/heartbeat.sh" > "$TMPFILE" || true
echo "$CRON_LINE" >> "$TMPFILE"
crontab "$TMPFILE"
rm "$TMPFILE"

echo "✓ Cron installed. Verify with: crontab -l"
echo ""
echo "The ecosystem will now wake up every day at 09:00 automatically."
echo "To run manually right now: npm run heartbeat"
echo "To force an evaluation cycle: FORCE_EVAL=1 npm run heartbeat"
