# Telegram Webhook Setup (Instant, Event-Driven)

The God Agent now uses **Telegram webhooks** for instant message delivery. No polling, no delays - your messages are processed in <1 second.

## How It Works

1. **You send a message** to your bot in Telegram
2. **Telegram POSTs instantly** to your webhook URL
3. **Local server receives it** and spawns God Agent
4. **God Agent processes** and replies via Telegram
5. **Done** - zero cost when idle, instant when active

## Quick Setup (5 minutes)

### 1. Install Dependencies

```bash
cd /Users/nunocadete/darwin-agents
npm install
```

### 2. Start Webhook Server

```bash
node scripts/telegram-webhook-server.js
```

Output:
```
[2026-04-28T22:00:00.000Z] Telegram webhook server started on port 3737
[2026-04-28T22:00:00.000Z] Waiting for webhooks...

Next steps:
1. Expose this server with: cloudflared tunnel --url http://localhost:3737
2. Or use ngrok: ngrok http 3737
3. Configure webhook: bash scripts/telegram-setup-webhook.sh <public-url>
```

### 3. Expose Server (New Terminal)

**Option A: Cloudflared (Free, No Signup)**

```bash
# Install cloudflared
brew install cloudflared

# Expose your server
cloudflared tunnel --url http://localhost:3737
```

Output:
```
Your quick Tunnel has been created! Visit it at:
https://abc123xyz.trycloudflare.com  ← Copy this URL
```

**Option B: ngrok (Requires Free Account)**

```bash
# Install ngrok
brew install ngrok

# Expose your server
ngrok http 3737
```

Output:
```
Forwarding  https://abc123.ngrok.io -> http://localhost:3737  ← Copy this URL
```

### 4. Configure Webhook (New Terminal)

```bash
bash scripts/telegram-setup-webhook.sh https://abc123xyz.trycloudflare.com/webhook
```

Output:
```
🔧 Configuring Telegram webhook...
   Bot token: 8790113592...
   Webhook URL: https://abc123xyz.trycloudflare.com/webhook

✅ Webhook configured successfully!

📊 Webhook info:
   URL: https://abc123xyz.trycloudflare.com/webhook
   Pending updates: 0
   Last error: None

✅ All set! Send a message to your bot and it will be processed instantly.
```

### 5. Test It!

Open Telegram, send a message to **@darwin_god_bot**:

```
You: status
```

Within 1 second, your webhook server will show:
```
[2026-04-28T22:05:00.000Z] Received message from Nuno (chat 8709239624): "status"
[2026-04-28T22:05:00.000Z] Spawning God Agent to process message: "status"
```

And you'll get an instant reply in Telegram! 🎉

---

## Management

### Check Webhook Status

```bash
bash scripts/telegram-check-webhook.sh
```

Output:
```
📊 Telegram Webhook Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Status: ✅ Webhook configured
URL: https://abc123xyz.trycloudflare.com/webhook
Pending updates: 0
Max connections: 40
```

### Delete Webhook

If you want to stop using webhooks:

```bash
bash scripts/telegram-delete-webhook.sh
```

---

## Production Setup (Optional)

For permanent deployment, deploy the webhook server to a cloud service:

### Option 1: Cloudflare Workers

Deploy the webhook as a serverless function (always-on, free, instant):

```bash
# Install wrangler
npm install -g wrangler

# Deploy
wrangler deploy scripts/telegram-webhook-server.js
```

### Option 2: Railway / Render / Fly.io

Deploy the Node.js server to any hosting platform. It's just a simple Express server.

### Option 3: Keep It Local

Just run:
- `node scripts/telegram-webhook-server.js` in a tmux/screen session
- `cloudflared tunnel` in another tmux/screen session

The tunnel URL stays stable for hours/days. When it changes, just re-run `telegram-setup-webhook.sh`.

---

## Troubleshooting

### Webhook not receiving messages

```bash
# Check webhook status
bash scripts/telegram-check-webhook.sh

# If there's a last_error, fix it and reconfigure
bash scripts/telegram-delete-webhook.sh
bash scripts/telegram-setup-webhook.sh <new-url>
```

### Server crashed

Just restart it:
```bash
node scripts/telegram-webhook-server.js
```

The webhook URL stays configured. No need to reconfigure unless the URL changed.

### Tunnel expired

Cloudflared free tunnels expire after ~24 hours. When that happens:
1. Stop old tunnel (Ctrl+C)
2. Start new tunnel: `cloudflared tunnel --url http://localhost:3737`
3. Reconfigure webhook: `bash scripts/telegram-setup-webhook.sh <new-url>`

For permanent tunnels, use `cloudflared tunnel create` (requires Cloudflare account).

---

## Cost Comparison

| Approach | Idle Cost | Active Cost | Latency | Complexity |
|----------|-----------|-------------|---------|------------|
| **Polling (old)** | ~60MB RAM, background process | Same | 30-60s | Low |
| **Webhooks (new)** | $0 (server off when not needed) | 1 pi session/msg | <1s | Medium |
| **Webhooks + CF Workers** | $0 (serverless) | $0 (free tier) | <1s | Medium |

---

## Commands

All commands from the old system still work:

- `status` - Fleet overview
- `spawn <idea>` - Create new project
- `kill <project-id>` - Kill a project
- `poke <project-id>` - Wake a project
- `evaluate` - Run selection cycle
- `help` - List commands

Just send them to your bot in Telegram! 🚀
