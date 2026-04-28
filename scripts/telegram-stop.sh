#!/bin/bash
# Stop the Telegram listener daemon

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PID_FILE="$REPO_ROOT/logs/telegram-listener.pid"

if [ ! -f "$PID_FILE" ]; then
    echo "❌ Telegram listener is not running (no PID file found)"
    exit 1
fi

PID=$(cat "$PID_FILE")

if ! ps -p $PID > /dev/null 2>&1; then
    echo "❌ Telegram listener is not running (PID $PID not found)"
    rm "$PID_FILE"
    exit 1
fi

echo "🛑 Stopping Telegram listener (PID: $PID)..."
kill $PID

# Wait up to 5 seconds for graceful shutdown
for i in {1..5}; do
    if ! ps -p $PID > /dev/null 2>&1; then
        echo "✅ Telegram listener stopped"
        rm "$PID_FILE"
        exit 0
    fi
    sleep 1
done

# Force kill if still running
if ps -p $PID > /dev/null 2>&1; then
    echo "⚠️  Forcing shutdown..."
    kill -9 $PID
    sleep 1
fi

if ! ps -p $PID > /dev/null 2>&1; then
    echo "✅ Telegram listener stopped"
    rm "$PID_FILE"
else
    echo "❌ Failed to stop Telegram listener"
    exit 1
fi
