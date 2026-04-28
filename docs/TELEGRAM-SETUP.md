# Telegram Integration Setup

The God Agent can now communicate with you via Telegram! This lets you:
- Get real-time updates when projects are spawned, killed, or evaluated
- Send commands to the God Agent remotely
- Check fleet status on the go

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
