#!/bin/bash

echo "=== TELEGRAM SYSTEM STATUS ==="
echo ""

# Check webhook server
echo "1. WEBHOOK SERVER:"
WEBHOOK_PID=$(ps aux | grep telegram-webhook-server | grep -v grep | awk '{print $2}' | head -1)
if [ -n "$WEBHOOK_PID" ]; then
    echo "   ✅ Running (PID: $WEBHOOK_PID)"
else
    echo "   ❌ Not running"
fi
echo ""

# Check cloudflared tunnel
echo "2. CLOUDFLARE TUNNEL:"
TUNNEL_PID=$(ps aux | grep cloudflared | grep -v grep | awk '{print $2}' | head -1)
if [ -n "$TUNNEL_PID" ]; then
    echo "   ✅ Running (PID: $TUNNEL_PID)"
    
    # Try to find the tunnel URL from running process
    TUNNEL_URL=$(ps aux | grep cloudflared | grep -v grep | grep -oE 'https://[a-z0-9-]+\.trycloudflare\.com' | head -1)
    if [ -n "$TUNNEL_URL" ]; then
        echo "   URL: $TUNNEL_URL"
    else
        echo "   ⚠️  URL not found in process args"
    fi
else
    echo "   ❌ Not running"
fi
echo ""

# Check last message received
echo "3. LAST MESSAGE RECEIVED:"
LAST_MSG=$(tail -100 logs/telegram-webhook.log | grep "Received message from" | tail -1)
if [ -n "$LAST_MSG" ]; then
    echo "   $LAST_MSG"
else
    echo "   ⚠️  No messages found in recent logs"
fi
echo ""

# Check if webhook is registered with Telegram
echo "4. TELEGRAM WEBHOOK STATUS:"
source .env
WEBHOOK_INFO=$(curl -s "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/getWebhookInfo")
echo "$WEBHOOK_INFO" | jq -r '"   URL: \(.result.url)\n   Last error: \(.result.last_error_message // "none")\n   Pending updates: \(.result.pending_update_count)"'
echo ""

echo "5. TEST WEBHOOK ENDPOINT:"
echo "   Testing http://localhost:3737/webhook"
HEALTH_CHECK=$(curl -s http://localhost:3737/ 2>&1)
if [[ "$HEALTH_CHECK" == *"Telegram webhook server"* ]]; then
    echo "   ✅ Webhook server responding"
else
    echo "   ❌ Webhook server not responding"
fi
