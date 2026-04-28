# Telegram Integration Setup

The God Agent can now communicate with you via Telegram! This lets you:
- Get real-time updates when projects are spawned, killed, or evaluated
- Send commands to the God Agent remotely
- Check fleet status on the go

## Quick Start (2 minutes)

```bash
# 1. Make sure you've set up the bot (see Setup section below)
# 2. Start the listener daemon
bash scripts/telegram-start.sh

# 3. Send a message to your bot in Telegram
# The God Agent will respond automatically!

# Check status anytime
bash scripts/telegram-status.sh

# Stop the listener
bash scripts/telegram-stop.sh
```

## How It Works (Zero Token Cost)

The system uses a **lightweight polling daemon** that:

1. **Runs in the background** - A simple Node.js script polls Telegram API every 60 seconds
2. **Zero cost when idle** - No pi sessions running, no tokens consumed
3. **Spawns God Agent only when needed** - When you send a message, it launches a pi session
4. **Processes your command** - God Agent reads your message, acts on it, replies via Telegram
5. **Goes back to sleep** - Daemon returns to polling mode

**Resource usage:**
- Idle: ~20 MB RAM, 0% CPU, $0 in tokens
- Active: 1 God Agent session per message (only when you send commands)
- Network: ~1 KB per poll (free Telegram API)

## Setup (5 minutes)

### 1. Create a Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Send `/newbot`
3. Choose a name (e.g., "Darwin God Agent")
4. Choose a username (e.g., "darwin_god_bot")
5. BotFather will give you a token that looks like: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

### 2. Get Your Chat ID

1. Send a message to your new bot (any message)
2. Visit this URL in your browser (replace `YOUR_BOT_TOKEN`):
   ```
   https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
   ```
3. Look for `"chat":{"id":123456789` in the JSON response
4. Copy that number (your chat ID)

### 3. Add to .env

Add these two lines to `/Users/nunocadete/darwin-agents/.env`:

```bash
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_CHAT_ID=123456789
```

### 4. Test It

Run the God Agent and it will send you a test message:

```bash
cd /Users/nunocadete/darwin-agents
pi -p "Use telegram_send to send me a test message: 'God Agent online. Telegram integration working!'"
```

You should receive a Telegram message instantly.

## How to Use

### Commands You Can Send

Send these messages to your bot from Telegram:

- `status` - Get current fleet status
- `spawn <idea>` - Spawn a new project with the given idea
- `kill <project-id>` - Kill a specific project
- `poke <project-id>` - Wake up a specific project agent
- `evaluate` - Run the weekly evaluation cycle early
- `help` - List available commands

### What the God Agent Sends You

You'll automatically get Telegram notifications for:
- ✅ New project spawned (with pitch and fitness target)
- ❌ Project killed (with reason and final fitness score)
- 📊 Weekly evaluation complete (summary of changes)
- 🚨 Critical blockers (when a project can't make progress)
- 💰 First revenue milestone for each project

### Example Workflow

**Morning check:**
```
You: status
Bot: 🏁 Darwin Fleet - Cycle 2
     3 alive projects:
     1. budget-recipe-blog (fitness: 15.2)
     2. b2b-cold-email-consulting (fitness: 8.5)
     3. etsy-productivity-planners (fitness: 4.1)
```

**Remote spawn:**
```
You: spawn affiliate marketing site for pet supplies
Bot: ✅ Spawned new project: pet-affiliate-hub
     Pitch: SEO-optimized pet supply recommendations with Amazon affiliate links
     Target: $150 in 6 weeks
     Status: Booting project agent now...
```

**Emergency intervention:**
```
You: kill etsy-productivity-planners
Bot: ⚠️  Kill queued for etsy-productivity-planners (fitness: 4.1)
     Added to human-tasks.md for confirmation.
     Will execute on next heartbeat if approved.
```

## Privacy & Security

- Only messages from YOUR chat ID are processed
- Bot token is private (never share it)
- Messages are checked only when God Agent runs (not a live listener)
- No message history is stored permanently

## Troubleshooting

**"Failed to send Telegram message"**
- Check that TELEGRAM_BOT_TOKEN is correct in .env
- Check that TELEGRAM_CHAT_ID is correct in .env
- Make sure you've sent at least one message to the bot first

**No response to commands**
- God Agent only checks messages when it runs (heartbeat or manual)
- Commands are queued and processed on next session
- Reply times: ~1-5 minutes (depending on heartbeat schedule)

**Bot not sending notifications**
- Check that telegram_send calls are in God Agent code
- Verify the bot token has send message permissions
- Look for errors in God Agent logs

## Cost

**FREE** - Telegram Bot API has no costs or limits for small-scale use like this.

---

## Running the Telegram Listener

The listener daemon runs in the background and responds to your messages automatically.

### Start the Listener

```bash
bash scripts/telegram-start.sh
```

Output:
```
🚀 Starting Telegram listener...
✅ Telegram listener started successfully
   PID: 12345
   Log: /Users/nunocadete/darwin-agents/logs/telegram-listener.log
   
   To stop: bash scripts/telegram-stop.sh
   To view logs: tail -f logs/telegram-listener.log
```

### Check Status

```bash
bash scripts/telegram-status.sh
```

Output:
```
📊 Telegram Listener Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Status: ✅ Running
PID: 12345
Uptime: 01:23:45
Memory: 18432 KB
Log: logs/telegram-listener.log

Recent activity (last 10 lines):
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[2026-04-28T22:45:00.000Z] Checking for new Telegram messages...
[2026-04-28T22:45:01.000Z] No new messages
[2026-04-28T22:46:00.000Z] Checking for new Telegram messages...
[2026-04-28T22:46:02.000Z] Found 1 new message(s)
[2026-04-28T22:46:02.000Z] Spawning God Agent to process 1 message(s)...
[2026-04-28T22:46:45.000Z] God Agent session complete
```

### View Live Logs

```bash
tail -f logs/telegram-listener.log
```

Press `Ctrl+C` to exit.

### Stop the Listener

```bash
bash scripts/telegram-stop.sh
```

Output:
```
🛑 Stopping Telegram listener (PID: 12345)...
✅ Telegram listener stopped
```

### Auto-Start on Boot (Optional)

To have the listener start automatically when your computer boots:

**macOS (launchd):**
```bash
cp scripts/com.darwin.telegram-listener.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.darwin.telegram-listener.plist
```

**Linux (systemd):**
```bash
sudo cp scripts/darwin-telegram-listener.service /etc/systemd/system/
sudo systemctl enable darwin-telegram-listener
sudo systemctl start darwin-telegram-listener
```

---

## Available Commands

Send these to your bot in Telegram:

### Fleet Management
- `status` - Current fleet status and fitness scores
- `spawn <idea>` - Create a new project (e.g., "spawn affiliate site for pet supplies")
- `kill <project-id>` - Kill a specific project
- `poke <project-id>` - Wake up a project agent immediately
- `evaluate` - Run weekly evaluation cycle now

### Information
- `help` - List all commands
- `logs <project-id>` - View recent activity for a project
- `metrics <project-id>` - Get current metrics snapshot

### Examples

```
You: status
Bot: 🏁 Darwin Fleet - Cycle 0
     3 alive projects:
     1. budget-recipe-blog (fitness: 15.2) ✅
     2. b2b-cold-email-consulting (fitness: 8.5) ⏳
     3. etsy-productivity-planners (fitness: 4.1) ⏸️
     
     Next evaluation: 2026-05-05
```

```
You: spawn dropshipping store for gaming accessories
Bot: 🚀 Spawning new project...
     
     ✅ Project created: gaming-accessories-drop
     Pitch: Dropshipping store for gaming peripherals
     Target: $500 in 6 weeks
     Status: Booting project agent...
```

```
You: poke budget-recipe-blog
Bot: 👊 Poking budget-recipe-blog...
     
     ✅ Project agent invoked
     Action: Added 3 new recipe pages
     Commit: [budget-recipe-blog] Added pasta recipes batch
```

---

## What You'll Receive

The God Agent will automatically send you Telegram notifications for:

### Major Events
- ✅ **Project spawned** - Name, pitch, fitness target
- ❌ **Project killed** - Reason, final fitness score
- 📊 **Evaluation complete** - Summary of survivors, killed, cloned
- 🔄 **Project cloned** - Parent, mutation strategy

### Milestones
- 💰 **First revenue** - "budget-recipe-blog earned first $1!"
- 🎯 **Target hit** - "b2b-consulting reached $800 target!"
- 📈 **Traffic spike** - "etsy-planners: 10x traffic increase"

### Critical Alerts
- 🚨 **Blocker detected** - When a project can't progress without human action
- ⚠️ **Danger zone** - When a project is in bottom 25% before evaluation
- 🔧 **Manual action needed** - Deploy, account setup, etc.

---

## Troubleshooting

### Listener won't start
```bash
# Check if already running
bash scripts/telegram-status.sh

# View logs for errors
cat logs/telegram-listener.log

# Common issues:
# 1. Missing .env file → Add TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID
# 2. Port already in use → Stop existing listener first
# 3. Permission denied → chmod +x scripts/telegram-*.sh
```

### Not receiving messages
```bash
# 1. Check listener is running
bash scripts/telegram-status.sh

# 2. Check bot token is valid
node -e "fetch('https://api.telegram.org/bot' + require('fs').readFileSync('.env', 'utf8').match(/TELEGRAM_BOT_TOKEN=(.+)/)[1] + '/getMe').then(r=>r.json()).then(console.log)"

# 3. Check chat ID is correct
# Send a message to the bot, then:
curl -s "https://api.telegram.org/bot$(grep TELEGRAM_BOT_TOKEN .env | cut -d= -f2)/getUpdates" | python3 -m json.tool
```

### Bot not responding to commands
```bash
# Check recent logs
tail -50 logs/telegram-listener.log

# Look for:
# - "Found X new message(s)" → Listener sees your messages
# - "Spawning God Agent..." → Pi session starting
# - "God Agent session complete" → Command processed
# - "ERROR:" → Something failed

# If you see errors, restart the listener
bash scripts/telegram-stop.sh
bash scripts/telegram-start.sh
```

### High memory usage
```bash
# The listener itself uses ~20 MB
# If it's using >100 MB, restart it:
bash scripts/telegram-stop.sh
bash scripts/telegram-start.sh

# Check for runaway God Agent sessions:
ps aux | grep "pi --no-session"

# Kill any stuck sessions:
pkill -f "pi --no-session"
```
