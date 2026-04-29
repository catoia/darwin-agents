# Telegram Webhook Security

## Is It Safe?

**YES!** The webhook system has multiple security layers that prevent unauthorized access:

## Security Layers

### Layer 1: Secret Token Verification ✅

**What it is:** A random 64-character secret that only Telegram and your server know.

**How it works:**
1. When you set up the webhook, a secret token is generated: `openssl rand -hex 32`
2. This secret is sent to Telegram AND saved in your `.env` file
3. Every webhook POST from Telegram includes header: `X-Telegram-Bot-Api-Secret-Token: <your-secret>`
4. Your server verifies the header matches before processing
5. **Without the secret, requests are rejected with 403 Forbidden**

**What this means:**
- Even if someone finds your webhook URL (e.g., `https://abc123.trycloudflare.com/webhook`)
- They CAN'T trigger actions because they don't have the secret token
- Only Telegram servers can successfully POST to your webhook

### Layer 2: Chat ID Whitelist ✅

**What it is:** Only messages from YOUR Telegram chat ID are processed.

**How it works:**
1. Your `TELEGRAM_CHAT_ID` is stored in `.env`
2. Every message includes the sender's chat ID
3. Server checks: `if (messageChatId !== authorizedChatId) reject()`
4. **Messages from any other chat ID are silently ignored**

**What this means:**
- Anyone CAN find your bot (e.g., search @darwin_god_bot)
- Anyone CAN send messages to your bot
- But **only YOUR messages trigger the God Agent**
- Everyone else's messages are dropped

### Layer 3: HTTPS Encryption 🔒

**What it is:** All traffic between Telegram and your webhook is encrypted.

**How it works:**
- Cloudflared/ngrok automatically provides HTTPS
- Telegram REQUIRES webhooks to use HTTPS
- All data is encrypted in transit

**What this means:**
- No one can intercept your messages
- No man-in-the-middle attacks possible

---

## What If Someone...

### ...finds my webhook URL?

**They can't do anything with it.**

Without the secret token (which only Telegram knows), any POST request returns:
```
403 Forbidden
```

### ...discovers my bot username?

**They can message the bot, but nothing happens.**

The bot receives their message and silently ignores it because their chat ID doesn't match yours.

### ...gets my bot token?

**This is the only real risk.**

If someone gets your `TELEGRAM_BOT_TOKEN`, they could:
- Send messages as your bot
- Change your webhook URL
- Impersonate the bot

**Protection:**
- Never commit `.env` to git (it's in `.gitignore`)
- Never share your `.env` file
- Keep your bot token secret

If compromised:
1. Go to @BotFather in Telegram
2. `/revoke` your bot token
3. Get a new token
4. Update `.env`

### ...sends fake POSTs to my webhook?

**They're blocked by secret token verification.**

Example:
```bash
# Attacker tries to fake a webhook
curl -X POST https://abc123.trycloudflare.com/webhook \
  -H "Content-Type: application/json" \
  -d '{"message":{"text":"malicious command"}}'

# Response: 403 Forbidden (no secret token header)
```

Your server logs:
```
[...] SECURITY: Rejected webhook with invalid secret token from 1.2.3.4
```

---

## Security Best Practices

### ✅ DO:

- Keep `.env` file private
- Use cloudflared or ngrok (they provide HTTPS)
- Check webhook status regularly: `bash scripts/telegram-check-webhook.sh`
- Monitor logs for suspicious activity

### ❌ DON'T:

- Commit `.env` to git (already in `.gitignore`)
- Share your bot token publicly
- Share your webhook URL (though it's useless without the secret)
- Disable secret token verification (never remove `TELEGRAM_WEBHOOK_SECRET`)

---

## Verification

### Check Your Security Is Active:

```bash
bash scripts/telegram-check-webhook.sh
```

Look for:
```
✅ SECURITY ENABLED:
   ✓ Secret token verification active
   ✓ Only your chat ID can trigger actions
```

### Test It:

1. Create a second Telegram account (or ask a friend)
2. Have them search for your bot: `@darwin_god_bot`
3. Have them send: `status`
4. Check your server logs - you'll see:
   ```
   SECURITY: Rejected message from unauthorized chat 123456789
   ```
5. The God Agent is NOT spawned for unauthorized users

---

## Comparison to Other Approaches

| Approach | Security Level | Attack Surface |
|----------|---------------|----------------|
| **Public API (no auth)** | ❌ None | Anyone can call |
| **API key in URL** | ⚠️ Low | URL sniffing exposes key |
| **Basic Auth** | ✅ Medium | Username:password can leak |
| **Webhook + Secret Token** | ✅✅ High | Multi-layer verification |
| **mTLS** | ✅✅✅ Highest | Requires client certificates |

Our webhook approach is industry-standard for bot webhooks and used by:
- Telegram (this implementation)
- GitHub webhooks
- Stripe webhooks
- Twilio webhooks

---

## What Telegram Can See

Telegram (the company) can see:
- Your bot token (they issued it)
- Your webhook URL
- Your secret token (they store it)
- Messages you send to the bot
- The bot's replies

**They CANNOT see:**
- Your local files
- Your God Agent's internal state
- Your other projects or code
- Your cloudflared/ngrok tunnel unless you expose it elsewhere

---

## TL;DR

✅ **YES, it's safe!**

- Secret token prevents fake webhooks
- Chat ID whitelist prevents unauthorized users
- HTTPS prevents interception
- Only YOUR messages trigger the God Agent
- Even if someone finds your webhook URL, it's useless without the secret

**The only way someone could compromise it:**
- Steal your bot token (don't share `.env`)
- Hack Telegram's servers (extremely unlikely)
- Physically access your computer (standard security applies)
