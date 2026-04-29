#!/bin/bash
# Delete Telegram webhook (switches bot back to polling mode)

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

# Load bot token
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found"
    exit 1
fi

BOT_TOKEN=$(grep TELEGRAM_BOT_TOKEN .env | cut -d= -f2)

if [ -z "$BOT_TOKEN" ]; then
    echo "❌ Error: TELEGRAM_BOT_TOKEN not found in .env"
    exit 1
fi

echo "🗑️  Deleting Telegram webhook..."

RESPONSE=$(curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/deleteWebhook")

if echo "$RESPONSE" | grep -q '"ok":true'; then
    echo "✅ Webhook deleted successfully"
    echo ""
    echo "The bot is now in polling mode."
    echo "You can use getUpdates to fetch messages manually."
else
    echo "❌ Failed to delete webhook"
    echo "$RESPONSE" | python3 -m json.tool
    exit 1
fi
