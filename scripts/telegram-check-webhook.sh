#!/bin/bash
# Check Telegram webhook status

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

echo "📊 Telegram Webhook Status"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

RESPONSE=$(curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getWebhookInfo")

if echo "$RESPONSE" | grep -q '"ok":true'; then
    echo "$RESPONSE" | python3 << 'PYEOF'
import sys, json
data = json.load(sys.stdin)
info = data['result']

url = info.get('url', '')
pending = info.get('pending_update_count', 0)
last_error = info.get('last_error_message', '')
last_error_date = info.get('last_error_date', 0)
max_connections = info.get('max_connections', 0)

if url:
    print(f"Status: ✅ Webhook configured")
    print(f"URL: {url}")
    print(f"Pending updates: {pending}")
    print(f"Max connections: {max_connections}")
    if last_error:
        import datetime
        error_date = datetime.datetime.fromtimestamp(last_error_date)
        print(f"\n⚠️  Last error:")
        print(f"   Date: {error_date}")
        print(f"   Message: {last_error}")
else:
    print("Status: ⚠️  No webhook configured")
    print("")
    print("The bot is in polling mode (or not configured)")
    print("")
    print("To set up webhook:")
    print("1. Start the webhook server: node scripts/telegram-webhook-server.js")
    print("2. Expose it: cloudflared tunnel --url http://localhost:3737")
    print("3. Configure: bash scripts/telegram-setup-webhook.sh <public-url>")
PYEOF
else
    echo "❌ Error checking webhook"
    echo "$RESPONSE"
    exit 1
fi
