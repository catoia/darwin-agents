#!/bin/bash
# Start the Telegram listener daemon in the background

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
LOG_DIR="$REPO_ROOT/logs"
PID_FILE="$LOG_DIR/telegram-listener.pid"
LOG_FILE="$LOG_DIR/telegram-listener.log"

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Check if already running
if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")
    if ps -p $PID > /dev/null 2>&1; then
        echo "❌ Telegram listener is already running (PID: $PID)"
        echo "   To stop it: bash scripts/telegram-stop.sh"
        exit 1
    else
        # Stale PID file, remove it
        rm "$PID_FILE"
    fi
fi

# Start the listener
echo "🚀 Starting Telegram listener..."
nohup node "$REPO_ROOT/scripts/telegram-listener.js" > "$LOG_FILE" 2>&1 &
PID=$!

# Save PID
echo $PID > "$PID_FILE"

# Wait a second to check if it started successfully
sleep 2

if ps -p $PID > /dev/null 2>&1; then
    echo "✅ Telegram listener started successfully"
    echo "   PID: $PID"
    echo "   Log: $LOG_FILE"
    echo "   "
    echo "   To stop: bash scripts/telegram-stop.sh"
    echo "   To view logs: tail -f $LOG_FILE"
else
    echo "❌ Failed to start Telegram listener"
    echo "   Check logs: cat $LOG_FILE"
    rm "$PID_FILE"
    exit 1
fi
