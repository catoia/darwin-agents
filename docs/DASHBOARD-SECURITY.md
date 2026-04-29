# Dashboard Security

## Current Protection

By default, the dashboard is **localhost-only** for security:

```
✅ Webhook endpoint (/webhook):
   - Public (via cloudflared)
   - Authenticated via secret token
   - Safe to expose

❌ Dashboard (/dashboard):
   - Localhost only by default
   - NOT accessible via public URL
   - Contains sensitive information
```

---

## What the Dashboard Shows (Sensitive Info)

- Your authorized chat ID
- Messages you send to the bot
- Active God Agent sessions
- Command history
- Error logs
- Process IDs

**This information should NOT be public.**

---

## How It Works

### Default Behavior (Localhost-Only):

**From localhost:**
```bash
curl http://localhost:3737/dashboard
# ✅ Works - you can access it
```

**From public URL:**
```bash
curl https://abc123.trycloudflare.com/dashboard
# ❌ 403 Forbidden - blocked
```

Response:
```html
🔒 Dashboard Access Restricted
Dashboard is only accessible from localhost for security.
Set DASHBOARD_PASSWORD in .env to enable remote access with authentication.
```

---

## Enable Remote Access (Optional)

If you want to access the dashboard remotely (e.g., from your phone), set a password:

### 1. Add Password to .env

```bash
echo "DASHBOARD_PASSWORD=your-strong-password-here" >> .env
```

### 2. Restart Webhook Server

```bash
# Kill current server
kill $(cat logs/webhook-pid.txt)

# Start new one
node scripts/telegram-webhook-server.js &
```

### 3. Access Dashboard

When you visit the public URL, you'll be prompted for credentials:

```
Username: admin
Password: your-strong-password-here
```

---

## Security Comparison

| Scenario | Dashboard Access | Webhook Access |
|----------|------------------|----------------|
| **Default** | Localhost only | Public + secret token |
| **With DASHBOARD_PASSWORD** | Public + basic auth | Public + secret token |

---

## Best Practices

### ✅ DO:

- Keep default localhost-only if you only need local access
- Use a strong password (20+ chars) if enabling remote access
- Never commit `.env` to git (already in `.gitignore`)
- Change password if you think it's compromised

### ❌ DON'T:

- Use weak passwords like "password123"
- Share your dashboard password
- Expose dashboard publicly without authentication
- Use the same password for multiple services

---

## Checking Current Settings

```bash
# Check if password is set
grep DASHBOARD_PASSWORD .env

# If no output: Dashboard is localhost-only ✅
# If output: Dashboard uses password authentication
```

---

## Test Security

### Test 1: Webhook is Public (Should Work)

```bash
# This should return 403 (secret token missing)
curl -X POST https://abc123.trycloudflare.com/webhook \
  -H "Content-Type: application/json" \
  -d '{"message":{"text":"test"}}'
```

Expected: `403 Forbidden` (correct - blocks fake webhooks)

### Test 2: Dashboard is Protected (Should Block)

```bash
# Without password set (default):
curl https://abc123.trycloudflare.com/dashboard
```

Expected: `403 Dashboard Access Restricted`

```bash
# With password set:
curl https://abc123.trycloudflare.com/dashboard
```

Expected: `401 Authentication required`

```bash
# With correct password:
curl -u admin:your-password https://abc123.trycloudflare.com/dashboard
```

Expected: HTML dashboard content

---

## What If Someone Finds My Dashboard URL?

### Without Password (Default):
- They get a 403 Forbidden message
- No sensitive data exposed
- ✅ Safe

### With Password:
- They're prompted for credentials
- Need correct password to access
- Failed attempts are logged
- ✅ Safe (if strong password)

---

## Recommendation

**For most users:** Keep the default localhost-only setup.

**If you need remote access:**
1. Generate a strong password: `openssl rand -base64 32`
2. Add to `.env`: `DASHBOARD_PASSWORD=<generated-password>`
3. Store password in your password manager
4. Access dashboard from anywhere with authentication

---

## Current Status

Check your webhook server startup logs:

```bash
tail logs/telegram-webhook.log
```

Look for:
```
[...] ⚠️  Dashboard: Localhost-only access (no remote access)
```
or
```
[...] ✅ Dashboard: Password authentication enabled
```
