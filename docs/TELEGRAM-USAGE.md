# Telegram Bot Usage Guide

## Quick Reference

Send these commands to **@darwin_god_bot** in Telegram:

### Fleet Management

**Check status:**
```
status
```
Shows active projects, cycle info, and fleet health.

**Spawn new project:**
```
spawn <idea>
```
Example: `spawn newsletter about AI tools with paid tier`

**Poke a project:**
```
poke <project-id>
```
Example: `poke budget-recipe-blog`

**Evaluate fleet:**
```
evaluate
```
Runs full selection cycle - kills bottom 25%, clones top 25%.

**Kill a project:**
```
kill <project-id>
```
Example: `kill budget-recipe-blog`

---

### Questions & Instructions

You can also just ask questions or give instructions:

```
How's the recipe blog doing?
```

```
Give the B2B project a challenge
```

```
Check which projects need attention
```

The God Agent will understand natural language and act accordingly.

---

## What Happens When You Send a Message

1. **Telegram → Webhook** (instant)
   - Your message POSTs to webhook server
   - Secret token verified
   - Chat ID checked against whitelist

2. **Spawn God Agent** (~1 second)
   - New pi session starts
   - Agent receives your message
   - Context loaded (AGENTS.md, registry.json)

3. **Agent Processes** (~20-40 seconds)
   - Reads relevant files
   - Executes command
   - Updates files (registry, inbox, metrics)
   - **Commits changes to git**
   - Pushes to GitHub

4. **Agent Replies** (instant)
   - Sends response via Telegram API
   - You see reply in Telegram
   - Agent session exits

5. **Dashboard Updates** (real-time)
   - Watch at: http://localhost:3737/dashboard
   - Shows agent running → completing

---

## Git Commits from Telegram

Every Telegram command that modifies files will result in a git commit:

### Commit Convention

- `[god]` - God Agent actions (status checks, evaluations, spawns)
- `[project-id]` - Project-specific changes

### Examples

```bash
# User sends "status" in Telegram
[god] Process Telegram status command - check fleet health

# User sends "poke budget-recipe-blog"
[budget-recipe-blog] Telegram poke - challenge project to improve metrics

# User sends "spawn AI newsletter"
[god] Spawn new project: ai-newsletter from Telegram command

# User sends "evaluate"
[god] Weekly evaluation triggered via Telegram - killed 1, spawned 1
```

### Verify Commits

After sending a command:

```bash
# Check latest commit
git log -1

# Check recent Telegram-triggered commits
git log --grep="Telegram" --oneline
```

---

## Response Time

| Stage | Duration |
|-------|----------|
| Telegram → Webhook | <1s |
| Spawn God Agent | ~1s |
| Agent Processing | 20-40s |
| Reply Sent | <1s |
| **Total** | **~25-45s** |

The dashboard shows real-time progress while the agent runs.

---

## Security Features

✅ **Secret token verification** - Only Telegram can POST to webhook  
✅ **Chat ID whitelist** - Only your messages trigger actions  
✅ **Dashboard locked down** - Localhost-only by default  
✅ **HTTPS encryption** - All traffic encrypted  

**Test security:**
- Have a friend message the bot → their messages are ignored
- Try accessing public dashboard → 403 Forbidden
- Check logs: `tail -f logs/telegram-webhook.log`

---

## Monitoring

### Dashboard (Real-Time)

**URL:** http://localhost:3737/dashboard

Shows:
- Active agents (currently running)
- Messages processed (total count)
- Activity log (last 50 events)
- Security status

**Auto-refreshes every 2 seconds.**

### Logs

**Webhook activity:**
```bash
tail -f logs/telegram-webhook.log
```

**Cloudflared tunnel:**
```bash
tail -f logs/cloudflared.log
```

**Git commits:**
```bash
git log --oneline | head -10
```

---

## Troubleshooting

### Agent doesn't reply

**Check dashboard:** http://localhost:3737/dashboard
- Is agent showing as active?
- Did it complete or error?
- Check exit code in activity log

**Check webhook logs:**
```bash
tail -20 logs/telegram-webhook.log
```

Look for:
- "Security checks passed"
- "Spawning God Agent"
- "God Agent completed successfully"

### Agent replies but no commit

**This should be fixed now.** The prompt explicitly tells the agent to commit.

**Verify:**
```bash
git log -1
```

If no commit, check agent's response - did it actually modify files?

### Webhook server stopped

**Check if running:**
```bash
ps -p $(cat logs/webhook-pid.txt)
```

**Restart:**
```bash
node scripts/telegram-webhook-server.js &
echo $! > logs/webhook-pid.txt
```

### Tunnel expired

Cloudflared tunnels expire after a while. You'll see a new URL when restarting.

**Restart tunnel:**
```bash
# Kill old tunnel
pkill cloudflared

# Start new tunnel
cloudflared tunnel --url http://localhost:3737 &

# Wait 5 seconds for URL
sleep 5

# Get new URL
grep -o 'https://[a-z0-9-]*\.trycloudflare\.com' logs/cloudflared.log | tail -1

# Reconfigure webhook
bash scripts/telegram-setup-webhook.sh <new-url>/webhook
```

---

## Best Practices

### DO:

✅ Send clear, specific commands: "poke budget-recipe-blog"  
✅ Wait for replies before sending another command  
✅ Check dashboard to see agent progress  
✅ Verify commits after important commands  
✅ Use natural language for questions  

### DON'T:

❌ Spam multiple commands (agents take ~30s each)  
❌ Expect instant replies (God Agent needs time to work)  
❌ Send very long messages (keep it concise)  
❌ Share your bot token or webhook URL  

---

## Example Session

**You:** `status`  
**Bot:** *(30 seconds later)*  
```
📊 Darwin Fleet Status

Active Projects: 3
Cycle: 0
Next Evaluation: 2026-05-05

Projects:
1. budget-recipe-blog (fitness: 5.2)
2. b2b-cold-email-consulting (fitness: 0.0)
3. etsy-productivity-planners (fitness: 0.0)

All projects in grace period (cycle 0-1).
No kills until cycle 2.
```

**Git log:**
```bash
$ git log -1 --oneline
a1b2c3d [god] Process Telegram status command - check fleet health
```

**Dashboard:**
- Agent #1730... completed (28.3s)
- Exit code: 0
- Activity: "Message from Nuno" → "Agent started" → "Agent complete"

---

## Files Modified by Telegram Commands

Common files the God Agent updates:

| File | When Modified | Commit Convention |
|------|---------------|-------------------|
| `registry.json` | spawn, kill, evaluate | `[god]` |
| `projects/<id>/inbox.md` | poke, challenges | `[project-id]` |
| `projects/<id>/metrics.json` | status checks | `[project-id]` |
| `human-tasks.md` | agent needs approval | `[god]` |

**All modifications are committed and pushed automatically.**

---

## Advanced Usage

### Chaining Commands

Send one command, wait for reply, then send next:

```
1. status
2. (wait for reply)
3. poke budget-recipe-blog
4. (wait for reply)
5. spawn micro-SaaS for freelancers
```

### Natural Language

The God Agent understands context:

```
"The recipe blog hasn't gotten any traffic. What should we do?"
→ Agent analyzes metrics, suggests actions, may poke the project

"Show me which projects are struggling"
→ Agent checks registry, reports bottom performers

"Give all projects a challenge"
→ Agent writes to each project's inbox, spawns project agents
```

---

## Quick Start Checklist

After setup, verify everything works:

- [ ] Send "status" to bot
- [ ] Wait ~30 seconds
- [ ] Receive reply in Telegram
- [ ] Check git log shows commit
- [ ] Open dashboard, see agent completed
- [ ] Try "poke <project-id>"
- [ ] Verify that commit too

**If all checkboxes pass: ✅ System fully operational!**

---

For security details, see: `docs/TELEGRAM-SECURITY.md`  
For dashboard security, see: `docs/DASHBOARD-SECURITY.md`
