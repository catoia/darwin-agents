#!/bin/bash
# Restart cloudflared tunnel and reconfigure Telegram webhook

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

echo "🔄 Restarting Cloudflared Tunnel..."
echo ""

# Kill old tunnel
echo "1. Killing old tunnel..."
pkill cloudflared
sleep 2

# Start new tunnel
echo "2. Starting new tunnel..."
nohup cloudflared tunnel --url http://localhost:3737 > logs/cloudflared.log 2>&1 &
TUNNEL_PID=$!
echo "   PID: $TUNNEL_PID"

# Wait for URL
echo "3. Waiting for URL..."
sleep 8

# Extract URL
TUNNEL_URL=$(grep -o 'https://[a-z0-9-]*\.trycloudflare\.com' logs/cloudflared.log | head -1)

if [ -z "$TUNNEL_URL" ]; then
    echo "❌ Failed to get tunnel URL. Check logs/cloudflared.log"
    exit 1
fi

echo "   ✅ URL: $TUNNEL_URL"
echo "$TUNNEL_URL" > logs/tunnel-url.txt

# Reconfigure webhook
echo "4. Reconfiguring Telegram webhook..."
bash scripts/telegram-setup-webhook.sh "$TUNNEL_URL/webhook"

echo ""
echo "✅ Tunnel restarted and webhook reconfigured!"
echo ""
echo "Test it: Send a message to @darwin_god_bot"
