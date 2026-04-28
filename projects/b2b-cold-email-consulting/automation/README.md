# B2B Cold Email Automation System

**Fully automated cold email campaign system** for B2B SaaS consulting services. Zero manual work required.

## What This Does

This system automatically:

1. **Finds prospects** - Scrapes Product Hunt, Apollo.io, YC Directory, and Indie Hackers for B2B SaaS founders
2. **Personalizes emails** - Uses AI (OpenAI GPT-4) to generate highly personalized cold emails
3. **Sends emails** - Delivers via SendGrid API with rate limiting and tracking
4. **Follows up** - Automatically sends 3 follow-up emails at 3, 7, and 14 days
5. **Tracks results** - Monitors opens, clicks, replies, and bounces in SQLite database

**No human intervention required** - Set it up once, let it run.

---

## Setup Instructions

### 1. Install Dependencies

```bash
cd automation
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Get API Keys

You need these API keys (free tiers available for most):

- **SendGrid** (required for sending): https://sendgrid.com/
  - Sign up → API Keys → Create API Key (Full Access)
  - Get 100 emails/day free
  
- **OpenAI** (required for personalization): https://platform.openai.com/
  - Sign up → API Keys → Create new secret key
  - Cost: ~$0.02 per email (GPT-4)
  
- **Apollo.io** (optional, for prospect finding): https://apollo.io/
  - Sign up → Settings → API → Copy API key
  - Free tier: 50 contacts/month
  
- **Hunter.io** (optional, for email enrichment): https://hunter.io/
  - Sign up → API → Copy API key
  - Free tier: 50 searches/month

### 3. Set Environment Variables

```bash
# Create .env file
cat > .env << 'EOF'
export SENDGRID_API_KEY="SG.xxxxx"
export OPENAI_API_KEY="sk-xxxxx"
export APOLLO_API_KEY="xxxxx"  # Optional
export HUNTER_API_KEY="xxxxx"  # Optional
EOF

# Load environment
source .env
```

### 4. Configure Campaign

Edit `automation/config.json`:

```json
{
  "from_email": "your-email@yourdomain.com",
  "from_name": "Your Name - Cold Email Consultant",
  "reply_to": "your-email@yourdomain.com",
  
  "rate_limits": {
    "emails_per_hour": 10,
    "emails_per_day": 50
  }
}
```

**Important**: Use a domain you own for `from_email`. Free email providers (Gmail, Yahoo) will likely bounce.

### 5. Verify SendGrid Setup

SendGrid requires domain authentication for deliverability:

1. Go to SendGrid → Settings → Sender Authentication
2. Authenticate your domain (add DNS records)
3. Wait for verification (~10 minutes)

---

## Usage

### Run Initial Campaign (20 Prospects)

```bash
cd automation
source venv/bin/activate
source .env

python3 orchestrator.py initial 20
```

This will:
- Find 20 B2B SaaS founders
- Personalize initial emails with AI
- Send emails via SendGrid
- Store all data in `campaign.db`

**Time**: ~10 minutes (with delays between emails)

### Check Campaign Stats

```bash
python3 orchestrator.py stats
```

Output:
```
📊 CAMPAIGN STATISTICS
============================================================
Total Prospects: 20
Emails Sent: 20
Opens: 8 (40.0%)
Clicks: 3 (15.0%)
Replies: 2 (10.0%)
Bounces: 0 (0.0%)
============================================================
```

### Run Follow-Ups Manually

```bash
python3 orchestrator.py followups
```

This checks the database for prospects due for follow-up emails (based on config delays) and sends them automatically.

### Automate Follow-Ups (Cron)

Set up daily automation:

```bash
# Edit crontab
crontab -e

# Add this line (runs daily at 9am)
0 9 * * * cd /path/to/darwin-agents/projects/b2b-cold-email-consulting && automation/scheduler.sh
```

Now follow-ups run automatically every day at 9am.

---

## Email Sequence

### Email 1: Initial (Day 0)
- Subject: Personalized based on their company/product
- Body: 80-120 words, personalized observation + value prop + free offer
- CTA: "Want a free 15-min cold email teardown?"

### Email 2: Follow-up (Day 3)
- Subject: Re: [original] or new angle
- Body: 60-80 words, acknowledge they're busy + add new value
- CTA: "Just reply 'yes' for the calendar link"

### Email 3: Follow-up (Day 7)
- Subject: "Last attempt: [specific benefit]"
- Body: 50-70 words, breakup pattern + quick tip + final CTA
- Give them an out: "If not interested, no worries"

### Email 4: Breakup (Day 14)
- Subject: "Moving on (+ free resource)"
- Body: 40-60 words, acknowledge not interested + free resource with no strings
- Leave door open for future

---

## Architecture

```
orchestrator.py          Main automation coordinator
├── prospect_finder.py   Scrapes/finds B2B SaaS founders
├── email_personalizer.py  AI-powered email personalization
├── email_sender.py      SendGrid integration + rate limiting
├── database.py          SQLite tracking database
└── scheduler.sh         Cron automation script

config.json              Campaign configuration
campaign.db              SQLite database (auto-created)
prospects.json           Latest prospect list (cached)
campaign-log.json        Send results log
```

---

## Monitoring & Debugging

### View Recent Sends

```bash
sqlite3 automation/campaign.db "
  SELECT p.name, p.email, e.email_type, e.sent_at, e.status
  FROM emails e
  JOIN prospects p ON e.prospect_id = p.id
  ORDER BY e.sent_at DESC
  LIMIT 10;
"
```

### View Replies

```bash
sqlite3 automation/campaign.db "
  SELECT p.name, p.email, r.reply_text, r.received_at
  FROM replies r
  JOIN prospects p ON r.prospect_id = p.id
  ORDER BY r.received_at DESC;
"
```

### Check Scheduler Log

```bash
tail -f automation/scheduler.log
```

---

## SendGrid Webhook Setup (Optional)

For real-time open/click/reply tracking, set up SendGrid webhooks:

1. Go to SendGrid → Settings → Mail Settings → Event Webhook
2. Set HTTP POST URL: `https://your-domain.com/webhook/sendgrid`
3. Enable: Opened, Clicked, Bounce, Spam Report

Then create a simple webhook receiver (Flask example):

```python
from flask import Flask, request
from database import CampaignDB

app = Flask(__name__)
db = CampaignDB()

@app.route('/webhook/sendgrid', methods=['POST'])
def sendgrid_webhook():
    events = request.json
    for event in events:
        email_id = event.get('email_id')  # You need to pass this in custom args
        
        if event['event'] == 'open':
            db.mark_email_opened(email_id)
        elif event['event'] == 'click':
            db.mark_email_clicked(email_id)
        elif event['event'] == 'bounce':
            db.mark_email_bounced(email_id)
    
    return '', 200

if __name__ == '__main__':
    app.run(port=5000)
```

---

## Scaling Up

### Increase Daily Volume

1. Upgrade SendGrid plan (up to 40k emails/day)
2. Update `config.json` rate limits
3. Add more prospect sources (scrape LinkedIn, use ZoomInfo API, etc.)

### Add More Prospect Sources

Edit `prospect_finder.py` and add methods:
- `find_from_linkedin()` - LinkedIn Sales Navigator scraping
- `find_from_crunchbase()` - Crunchbase API
- `find_from_twitter()` - Twitter API (search for "founder" + "B2B SaaS")

### Improve Personalization

Edit `email_personalizer.py` prompts to:
- Reference recent tweets/posts by the founder
- Mention specific competitors they're facing
- Include case studies from their industry

---

## Troubleshooting

### Emails Going to Spam

1. **Authenticate your domain** in SendGrid (SPF, DKIM, DMARC records)
2. **Warm up your sending domain** - Start with 10-20 emails/day for the first week
3. **Improve email content** - Remove spammy words, add more personalization
4. **Check sender reputation** - Use https://mxtoolbox.com/emailhealth

### Low Response Rates (<5%)

1. **Improve targeting** - Are you reaching the right people?
2. **Test subject lines** - A/B test different approaches
3. **Shorten emails** - Aim for 60-80 words max
4. **Increase personalization** - Generic emails get ignored

### API Errors

- **SendGrid 429**: Rate limit exceeded → Reduce `emails_per_hour` in config
- **OpenAI 429**: Rate limit exceeded → Add `time.sleep(1)` between calls
- **Apollo 403**: Invalid API key → Check your API key in .env

---

## Cost Analysis

For 100 prospects/month:

- SendGrid: $15/month (Essentials plan, 40k emails)
- OpenAI: $10/month (~500 emails * $0.02 each)
- Apollo.io: $49/month (1,000 contacts)
- Hunter.io: $49/month (500 searches)

**Total: ~$123/month** for fully automated outreach to 100 qualified prospects

**ROI**: If you convert just 1 prospect at $200, you've covered the cost.

---

## What's Next

Once this is running:

1. **Monitor metrics.json** - Track reply rate, conversion rate
2. **A/B test subject lines** - Try different angles
3. **Expand to 50-100 prospects/week** - Scale up gradually
4. **Add retargeting** - Re-engage people who opened but didn't reply
5. **Build case studies** - Use successful calls as social proof

---

## Support

For issues, check:
- `automation/scheduler.log` - Cron execution log
- `automation/campaign-log.json` - Send results
- SQLite database - All prospect/email data

Need help? File an issue or contact the human executor.
