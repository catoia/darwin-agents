#!/bin/bash
# Check status of the Telegram listener daemon

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PID_FILE="$REPO_ROOT/logs/telegram-listener.pid"
LOG_FILE="$REPO_ROOT/logs/telegram-listener.log"

echo "📊 Telegram Listener Status"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

if [ ! -f "$PID_FILE" ]; then
    echo "Status: ❌ Not running"
    echo ""
    echo "To start: bash scripts/telegram-start.sh"
    exit 0
fi

PID=$(cat "$PID_FILE")

if ps -p $PID > /dev/null 2>&1; then
    echo "Status: ✅ Running"
    echo "PID: $PID"
    echo "Uptime: $(ps -o etime= -p $PID | xargs)"
    echo "Memory: $(ps -o rss= -p $PID | xargs) KB"
    echo "Log: $LOG_FILE"
    echo ""
    echo "Recent activity (last 10 lines):"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    tail -10 "$LOG_FILE"
    echo ""
    echo "To stop: bash scripts/telegram-stop.sh"
    echo "To view live logs: tail -f $LOG_FILE"
else
    echo "Status: ❌ Not running (stale PID file)"
    rm "$PID_FILE"
    echo ""
    echo "To start: bash scripts/telegram-start.sh"
fi
