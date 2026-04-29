#!/bin/bash
# Configure Telegram bot webhook URL
# Usage: bash scripts/telegram-setup-webhook.sh <webhook-url>
# Example: bash scripts/telegram-setup-webhook.sh https://abc123.trycloudflare.com/webhook

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

if [ -z "$1" ]; then
    echo "❌ Error: Webhook URL required"
    echo ""
    echo "Usage: bash scripts/telegram-setup-webhook.sh <webhook-url>"
    echo ""
    echo "Example:"
    echo "  bash scripts/telegram-setup-webhook.sh https://abc123.trycloudflare.com/webhook"
    echo ""
    echo "First, expose your local server:"
    echo "  cloudflared tunnel --url http://localhost:3737"
    echo "Or:"
    echo "  ngrok http 3737"
    exit 1
fi

WEBHOOK_URL="$1"

cd "$REPO_ROOT"

# Load bot token from .env
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found"
    exit 1
fi

BOT_TOKEN=$(grep TELEGRAM_BOT_TOKEN .env | cut -d= -f2)

if [ -z "$BOT_TOKEN" ]; then
    echo "❌ Error: TELEGRAM_BOT_TOKEN not found in .env"
    exit 1
fi

# Generate secret token if it doesn't exist
SECRET_TOKEN=$(grep TELEGRAM_WEBHOOK_SECRET .env 2>/dev/null | cut -d= -f2)

if [ -z "$SECRET_TOKEN" ]; then
    echo "🔐 Generating webhook secret token..."
    SECRET_TOKEN=$(openssl rand -hex 32)
    echo "" >> .env
    echo "# Telegram webhook security (auto-generated)" >> .env
    echo "TELEGRAM_WEBHOOK_SECRET=$SECRET_TOKEN" >> .env
    echo "✅ Secret token saved to .env"
    echo ""
fi

echo "🔧 Configuring Telegram webhook..."
echo "   Bot token: ${BOT_TOKEN:0:10}..."
echo "   Webhook URL: $WEBHOOK_URL"
echo ""

# Set webhook
RESPONSE=$(curl -s -X POST "https://api.telegram.org/bot${BOT_TOKEN}/setWebhook" \
  -H "Content-Type: application/json" \
  -d "{\"url\": \"${WEBHOOK_URL}\", \"secret_token\": \"${SECRET_TOKEN}\"}")

# Check response
if echo "$RESPONSE" | grep -q '"ok":true'; then
    echo "✅ Webhook configured successfully!"
    echo ""
    echo "✅ SECURITY ENABLED:"
    echo "   ✓ Secret token verification active"
    echo "   ✓ Only your chat ID can trigger actions"
    echo "   ✓ Webhook URL is useless to anyone else"
    echo ""
    echo "📊 Webhook info:"
    curl -s "https://api.telegram.org/bot${BOT_TOKEN}/getWebhookInfo" | python3 -c "import sys, json; data=json.load(sys.stdin); print(f\"   URL: {data['result']['url']}\n   Pending updates: {data['result'].get('pending_update_count', 0)}\n   Last error: {data['result'].get('last_error_message', 'None')}\")"
    echo ""
    echo "✅ All set! Send a message to your bot and it will be processed instantly."
else
    echo "❌ Failed to set webhook"
    echo ""
    echo "Response:"
    echo "$RESPONSE" | python3 -m json.tool
    exit 1
fi
