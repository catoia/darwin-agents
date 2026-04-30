#!/bin/bash

echo "=== RESTARTING TELEGRAM SYSTEM ==="
echo ""

# 1. Kill everything
echo "1. Killing old processes..."
pkill -f cloudflared
pkill -f telegram-webhook-server
sleep 3
echo "   ✅ Processes killed"
echo ""

# 2. Start webhook server
echo "2. Starting webhook server..."
nohup node scripts/telegram-webhook-server.js > logs/telegram-webhook.log 2>&1 &
WEBHOOK_PID=$!
echo $WEBHOOK_PID > logs/webhook-pid.txt
sleep 2
if ps -p $WEBHOOK_PID > /dev/null; then
    echo "   ✅ Webhook server started (PID: $WEBHOOK_PID)"
else
    echo "   ❌ Webhook server failed to start"
    exit 1
fi
echo ""

# 3. Start cloudflared tunnel
echo "3. Starting cloudflared tunnel..."
nohup cloudflared tunnel --url http://localhost:3737 > logs/cloudflared.log 2>&1 &
TUNNEL_PID=$!
echo $TUNNEL_PID > logs/cloudflared-pid.txt
echo "   PID: $TUNNEL_PID"
echo ""

# 4. Wait for tunnel URL
echo "4. Waiting for tunnel URL (30 seconds)..."
for i in {1..30}; do
    TUNNEL_URL=$(grep -oE 'https://[a-z0-9-]+\.trycloudflare\.com' logs/cloudflared.log 2>/dev/null | head -1)
    if [ -n "$TUNNEL_URL" ]; then
        echo "   ✅ URL found: $TUNNEL_URL"
        break
    fi
    sleep 1
    echo -n "."
done
echo ""

if [ -z "$TUNNEL_URL" ]; then
    echo "   ❌ Timeout waiting for tunnel URL"
    echo "   Logs:"
    tail -20 logs/cloudflared.log
    exit 1
fi

# 5. Wait for DNS propagation
echo "5. Waiting for DNS propagation (15 seconds)..."
sleep 15
echo ""

# 6. Test tunnel
echo "6. Testing tunnel connectivity..."
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$TUNNEL_URL/" 2>&1)
if [ "$STATUS" = "302" ] || [ "$STATUS" = "200" ]; then
    echo "   ✅ Tunnel responding (HTTP $STATUS)"
else
    echo "   ⚠️  Tunnel returned: HTTP $STATUS"
fi
echo ""

# 7. Configure Telegram webhook
echo "7. Configuring Telegram webhook..."
source .env
WEBHOOK_RESPONSE=$(curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook" \
  -H "Content-Type: application/json" \
  -d "{\"url\": \"${TUNNEL_URL}/webhook\", \"secret_token\": \"${TELEGRAM_WEBHOOK_SECRET}\"}")

if echo "$WEBHOOK_RESPONSE" | jq -e '.ok == true' > /dev/null; then
    echo "   ✅ Webhook configured"
else
    echo "   ❌ Webhook configuration failed"
    echo "$WEBHOOK_RESPONSE" | jq .
fi
echo ""

# 8. Check pending messages
echo "8. Checking for pending messages..."
PENDING=$(echo "$WEBHOOK_RESPONSE" | jq -r '.result.pending_update_count // 0')
if [ "$PENDING" -gt 0 ]; then
    echo "   ⚠️  $PENDING pending messages (will be delivered now)"
else
    echo "   ✅ No pending messages"
fi
echo ""

echo "=== SYSTEM RESTARTED ==="
echo ""
echo "Webhook server: PID $WEBHOOK_PID"
echo "Cloudflared: PID $TUNNEL_PID"
echo "Tunnel URL: $TUNNEL_URL"
echo ""
echo "Test: Send a message to @darwin_god_bot"
