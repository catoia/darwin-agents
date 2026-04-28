# Quick Start Guide

## Get Running in 5 Minutes

### 1. Get API Keys (2 min)

**Required:**
- **SendGrid** (free): https://sendgrid.com/ → API Keys → Create
- **OpenAI** (paid): https://platform.openai.com/ → API Keys → Create

**Optional (better prospect finding):**
- **Apollo.io**: https://apollo.io/ → Settings → API
- **Hunter.io**: https://hunter.io/ → API

### 2. Setup (2 min)

```bash
# Run setup script
bash automation/setup.sh

# Edit .env with your API keys
nano automation/.env
```

### 3. Launch First Campaign (1 min)

```bash
# Load environment
source automation/.env

# Find 20 prospects, personalize, and send
python3 automation/orchestrator.py initial 20
```

**That's it!** The system will:
- Find 20 B2B SaaS founders
- Generate personalized emails with AI
- Send them via SendGrid
- Track everything in a database

### 4. Automate Follow-Ups

```bash
# Set up daily cron job (runs at 9am every day)
crontab -e

# Add this line:
0 9 * * * cd /path/to/darwin-agents/projects/b2b-cold-email-consulting && automation/scheduler.sh
```

---

## What Happens Next?

### Day 0 (Today)
- System sends 20 initial emails
- Prospects start opening them (tracking happens automatically)

### Day 3
- Cron job runs, finds prospects who haven't replied
- Sends follow-up #1 automatically

### Day 7
- Follow-up #2 sent automatically

### Day 14
- Final breakup email sent automatically

### When Replies Come In
- Human checks inbox daily (5 min)
- Books consulting calls with interested prospects
- Delivers $200 consulting sessions
- Records revenue in `revenue-manual.json`

---

## Monitor Performance

```bash
# View campaign stats
python3 automation/orchestrator.py stats

# Output:
# 📊 CAMPAIGN STATISTICS
# Total Prospects: 20
# Emails Sent: 20
# Opens: 8 (40.0%)
# Clicks: 3 (15.0%)
# Replies: 2 (10.0%)
# Bounces: 0 (0.0%)
```

---

## Troubleshooting

### Emails going to spam?
1. Authenticate your domain in SendGrid
2. Start with small volume (10-20/day)
3. Use a real business email (not Gmail/Yahoo)

### Low response rates?
1. Check if emails are too long (keep <100 words)
2. Improve personalization in `email_personalizer.py`
3. Test different subject lines

### API errors?
- Check `automation/scheduler.log` for errors
- Verify API keys in `.env`
- Check rate limits (SendGrid free tier: 100/day)

---

## Next Steps

Once you get your first reply:
1. Book a free 15-min teardown call
2. Deliver value on the call
3. Upsell to $200 paid strategy session
4. Record revenue in `revenue-manual.json`
5. Use testimonial for case studies

**Goal:** 4 paid sessions ($800) in first month.

See `automation/README.md` for full documentation.
