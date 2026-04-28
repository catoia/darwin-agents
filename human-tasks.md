# Human Task Inbox

This file is the **single place** where agents queue tasks that require human judgment.
Agents append here — they never block waiting for answers.
You (the human) reply inline below each open task, then set its status to `done`.

## How to respond

Find the open task, add your reply **immediately below the Context section**, then change `**Status:** open` to `**Status:** done`. Example:

```markdown
### Context
Should we kill project X with fitness 2.1?

**Human response:** yes, confirmed — kill it
**Status:** done
```

The god agent reads this at the start of every session and acts on `done` entries with a human response.
Do not delete entries — the history is the audit trail.

---

<!-- AGENTS: append new tasks at the bottom. Never edit existing entries — only the human edits Status and adds Human response. -->


## [2026-04-28] budget-recipe-blog: Deploy site & setup monetization accounts

**Priority:** HIGH
**Project:** budget-recipe-blog
**Agent:** Project Agent (budget-recipe-blog)

### Context

The budget recipe blog is fully built and ready for deployment. I've created:
- 1 homepage with clean design
- 10 SEO-optimized recipe pages targeting long-tail keywords ("cheap dinner ideas for two", "budget chicken recipes", etc.)
- Amazon affiliate link placeholders (tag=budgetrecipe-20) throughout all pages
- Sitemap.xml for Google Search Console
- Mobile-responsive CSS

**This site is ready to earn, but I need you to:**

### Required Actions

**1. Deploy to Cloudflare Pages (15 minutes)**
   - Go to Cloudflare Dashboard → Workers & Pages → Create Application
   - Upload the `projects/budget-recipe-blog/public/` folder
   - Project name: `budget-recipe-blog`
   - Once deployed, the URL will be: `https://budget-recipe-blog.pages.dev`
   - Alternative: Set CLOUDFLARE_API_TOKEN and CLOUDFLARE_ACCOUNT_ID env vars, then I can deploy via CLI

**2. Apply for Google AdSense (10 minutes)**
   - Go to https://www.google.com/adsense/start/
   - Sign up with a Google account
   - Add site URL: `https://budget-recipe-blog.pages.dev`
   - Approval takes 1-2 weeks
   - Once approved, send me the ad unit code snippet

**3. Set up Amazon Associates Account (10 minutes)**
   - Go to https://affiliate-program.amazon.com/
   - Sign up for Amazon Associates
   - Get your Associate ID (format: `yourname-20`)
   - Tell me the ID so I can replace all instances of `budgetrecipe-20` in the HTML files

**4. Submit to Google Search Console (5 minutes)**
   - Go to https://search.google.com/search-console
   - Add property: `https://budget-recipe-blog.pages.dev`
   - Verify ownership (Cloudflare usually auto-verifies)
   - Submit sitemap: `https://budget-recipe-blog.pages.dev/sitemap.xml`

### Why this matters

Without deployment, this project earns $0. Every day we delay is lost revenue.
- Target: $200 in 6 weeks
- Reality: Can't earn a penny until the site is live and monetization is active

See full deployment guide: `projects/budget-recipe-blog/DEPLOYMENT.md`

**Human response:** Cloudflare API credentials are already in .env (CLOUDFLARE_API_TOKEN + CLOUDFLARE_ACCOUNT_ID). Deploy automatically using the API. For AdSense and Amazon Associates, set up what you can programmatically or document what I need to manually approve.

UPDATE: I've added Google validation files to the remote repo (ads.txt and google82e50ad6f8522cea.html). Pull first. Amazon Associates affiliate ID is: nunodarwin-20. Replace all placeholder affiliate IDs with this.

**Status:** done


## [2026-04-28] b2b-cold-email-consulting: Execute cold outreach to 20 B2B SaaS founders

**Priority:** HIGH
**Project:** b2b-cold-email-consulting
**Agent:** Project Agent (b2b-cold-email-consulting)

### Context

I've created a complete cold email consulting service package:
- **Cold email pitch** (3-email sequence with subject lines) → `projects/b2b-cold-email-consulting/cold-email-pitch.md`
- **Service offer document** (free 15-min teardown → $200 paid 90-min strategy session) → `projects/b2b-cold-email-consulting/offer-document.md`
- **Talking points for free teardown calls** (pre-call prep + call structure + objection handling) → `projects/b2b-cold-email-consulting/teardown-talking-points.md`
- **Target list instructions** (where to find founders + tracking template) → `projects/b2b-cold-email-consulting/target-list-instructions.md`

**This is a service business. I write the strategy, you execute the outreach and deliver the consulting calls.**

### Required Actions

**1. Research 20 B2B SaaS founders (60 minutes)**
   - Use the sources in `target-list-instructions.md`:
     - Product Hunt (recent B2B SaaS launches in last 60 days)
     - Indie Hackers (active B2B founders)
     - LinkedIn search ("founder" + "B2B SaaS" + "seed")
     - Twitter/X (#buildinpublic B2B SaaS)
   - For each founder, record: Name, Company, Product, ICP (who they sell to), Email/Contact, LinkedIn URL, Personalization note
   - Create a spreadsheet or Notion doc to track responses (template in target-list-instructions.md)

**2. Send first batch of cold emails (30 minutes)**
   - **Day 1:** Send Email 1 to 10 founders (Batch A)
   - **Day 2:** Send Email 1 to 10 founders (Batch B)
   - Use the email template from `cold-email-pitch.md` (Subject: "Your cold email sequence teardown (15 min, free)")
   - **PERSONALIZE each email:** Replace [Company Name], [their ICP], [First Name], add a line about recent launch/post
   - Send from your personal email (higher deliverability than a new domain)
   - Include a calendar link (Calendly or Google Calendar) or say "reply with your availability"

**3. Send follow-up emails (ongoing)**
   - **Day 4-5:** Email 2 to Batch A non-responders (use template from cold-email-pitch.md)
   - **Day 5-6:** Email 2 to Batch B non-responders
   - **Day 9-11:** Email 3 (breakup email) to remaining non-responders

**4. Conduct free 15-minute teardown calls (as they book)**
   - Before each call: Read their email sequence (ask them to send it before the call)
   - Use the talking points from `teardown-talking-points.md`:
     - Identify their 3 biggest issues (use the checklist)
     - Give specific fixes for each
     - Pitch the paid $200 session at the end if they're engaged
   - Track outcomes in your response tracker

**5. Book & conduct paid $200 sessions (when they convert)**
   - Send payment link: Stripe / PayPal / Venmo
   - Once paid, schedule 90-minute strategy call
   - Deliver the full service (sequence rewrite, ICP strategy, testing plan)
   - **Immediately after receiving payment, record revenue:**
     ```bash
     echo '[{"date":"YYYY-MM-DD","revenue_usd":200,"notes":"Consulting session with [Founder Name] from [Company]"}]' > projects/b2b-cold-email-consulting/revenue-manual.json
     ```
     (Replace date and name — if multiple sessions, append to the array)

**6. Report back after Week 1 (5 minutes)**
   - Update me with:
     - How many emails sent
     - How many opened (if trackable)
     - How many replied
     - How many booked free teardowns
     - Any common objections or questions
   - Write this in `projects/b2b-cold-email-consulting/inbox.md` as a new entry: "[YYYY-MM-DD] Week 1 results: X sent, Y opened, Z replied, etc."

### Why this matters

**Revenue target: $800 in 4 weeks (4 paid sessions)**
- Timeline: First outreach by Day 2, first teardown call by Day 5, first paid session by Day 10
- Without outreach, fitness = 0. Without paid sessions, project gets killed at next evaluation.
- This is Stage 1 (zero revenue) — the ONLY thing that matters is getting to first dollar.

**Success metrics for Week 1:**
- 20 emails sent ✅
- 15% reply rate (3+ positive replies) ✅
- 2+ free teardown calls booked ✅
- 1 paid session booked by end of Week 2 ✅

**Payment setup:**
- Set up Stripe/PayPal/Venmo to accept $200 payments
- Preferred: Stripe payment link (create one for "$200 Cold Email Strategy Session")
- Include payment link in follow-up after successful teardown calls

**Time commitment from you:**
- Week 1: ~2 hours (research + send emails)
- Week 2: ~3-4 hours (follow-ups + 2-3 teardown calls)
- Week 3+: ~2 hours/week (1-2 paid sessions)

See all deliverables in `projects/b2b-cold-email-consulting/`:
- `cold-email-pitch.md`
- `offer-document.md`
- `teardown-talking-points.md`
- `target-list-instructions.md`

**Human response:** I will NOT manually research prospects, fill templates, or send individual emails. You need to AUTOMATE this: scrape/API for prospect lists, automated personalization, automated sending via API (SendGrid/Mailgun/etc), automated follow-ups. Figure out the technical solution to run this at scale with zero manual work from me. I'll only jump in for actual sales calls once leads are qualified.
**Status:** done

---

## [2026-04-28] URGENT: Launch Etsy Productivity Planners — Get to First Dollar

**Priority:** high  
**Requested by:** etsy-productivity-planners project agent (first session)  
**Type:** revenue  
**Estimated effort:** 4 hours total over 3 days  

### Context
I've just completed the first session for the Etsy planner project. Everything is ready for launch:

✅ Researched 3 underserved niches (ADHD Task Starter, PhD Dissertation Tracker, Freelance Client Dashboard)
✅ Designed complete planner specifications (50-60 printable pages each)
✅ Written SEO-optimized Etsy listings (titles, descriptions, 13 tags each)
✅ Created comprehensive setup instructions

**What I need from you:**
See `projects/etsy-productivity-planners/HUMAN-SETUP-INSTRUCTIONS.md` for complete details.

**Quick summary:**
1. **Day 1:** Set up Etsy seller account (30 min)
2. **Day 1-2:** Create 3 planner PDFs from design specs using Canva (2-3 hours)
3. **Day 2-3:** Create 21 mockup photos for listings (1-2 hours)
4. **Day 3:** Upload 3 listings to Etsy (30 min)
5. **Day 3:** Enable Etsy Ads ($5.50/day budget) (5 min)
6. **Ongoing:** Log weekly Etsy payouts in `revenue-manual.json` (5 min/week)

**Cost to start:**
- Etsy listing fees: $0.60 (3 listings × $0.20)
- Etsy Ads budget: $5.50/day (~$165/month max)
- Canva: Free (or $30 if you use Pro)

**Expected timeline to first sale:** 7-10 days after listings go live

**Revenue target:** $150 in 5 weeks (15 planner sales @ $10 avg)

### Files to review
- `projects/etsy-productivity-planners/HUMAN-SETUP-INSTRUCTIONS.md` ← START HERE
- `projects/etsy-productivity-planners/templates/` (3 design specs)
- `projects/etsy-productivity-planners/listings/` (3 Etsy listing drafts)

**Human response:** Automate what you can (PDF generation, mockup creation using code/APIs). For what requires manual work (Etsy account setup, uploads), document clearly and I'll execute. But maximize automation first.
**Status:** done

## [HIGH] Etsy Seller Account — CRITICAL PATH TO REVENUE (etsy-productivity-planners)

- **ID:** `task-$(openssl rand -hex 4)`
- **From:** project:etsy-productivity-planners
- **Created:** 2026-04-28T$(date +%H:%M:%S)Z
- **Status:** open

### Context

**THIS IS THE #1 BLOCKER TO ALL REVENUE.**

The agent has:
✅ Built PDF generation scripts (reportlab/weasyprint)
✅ Built mockup generation scripts (Pillow)
✅ Written all listing copy (SEO-optimized)
✅ Ready to generate 3 production-ready planner PDFs + 21 mockup images in 5 minutes

**What we're waiting on:** Etsy seller account. Cannot sell anything without it.

**WHAT YOU NEED TO DO (30 minutes, one-time):**

1. Go to https://www.etsy.com/sell
2. Click "Open your Etsy shop"
3. Choose shop name (suggestion: "ProductivityPlannersHub" or similar)
4. Fill in:
   - Legal name and address
   - Bank account for payouts  
   - Tax ID (SSN or EIN)
5. Set up Etsy Payments (required for sales)
6. Accept Terms of Service
7. Set shop policies:
   - Return policy: "All sales final (digital download)"
   - Processing time: "Instant download"

**COST:** $0 (account is free)

**TIMELINE:**
- You do this: 30 minutes today
- Agent generates PDFs + mockups: 5 minutes
- You upload 3 listings: 90 seconds
- Listings go live: immediately
- First sale: 7-10 days after live

**TARGET:** $150 revenue in 5 weeks (15 planner sales @ $10 avg)

**See complete instructions:** `projects/etsy-productivity-planners/HUMAN-SETUP-INSTRUCTIONS-AUTOMATED.md`

**Default action if no response in 48h:** Agent will document the complete automation pipeline but cannot deploy without Etsy account. Revenue stays at $0.

### Human Response

<!-- Reply here with "done + shop URL" or "blocked: [reason]", then change Status to: done -->

---

## [HIGH] API Keys + Setup Required - Automation System Blocked

- **ID:** `task-$(openssl rand -hex 4)`
- **From:** project:b2b-cold-email-consulting
- **Created:** $(date -u +"%Y-%m-%dT%H:%M:%SZ")
- **Status:** open

### Context

The B2B cold email automation system is BUILT and READY but cannot run due to missing credentials.

**WHAT'S BLOCKED:**
- ❌ Cannot send emails (no SendGrid key)
- ❌ Cannot run anything (Python dependencies not installed)
- ❌ Config still has placeholder email "nuno@example.com"

**NOTE:** Email personalization now uses local LLM (pi) - no external AI API needed!

**WHAT YOU NEED TO DO (10 minutes total):**

1. **Install dependencies** (2 min):
   ```bash
   cd /Users/nunocadete/darwin-agents/projects/b2b-cold-email-consulting
   pip3 install -r automation/requirements.txt
   ```

2. **Get SendGrid API key** (5 min) - FREE:
   - Sign up at https://sendgrid.com/
   - Settings → API Keys → Create API Key
   - Name: "Darwin Cold Email", Permissions: Full Access
   - Copy key (starts with SG....)

3. **Create automation/.env** (1 min):
   ```bash
   cat > automation/.env << 'ENVEOF'
   export SENDGRID_API_KEY="SG.your_key_here"
   export APOLLO_API_KEY="your_key_here"    # optional
   export HUNTER_API_KEY="your_key_here"    # optional
   ENVEOF
   # Then edit with your actual SendGrid key
   ```

4. **Update automation/config.json** (1 min):
   - Replace "nuno@example.com" with your real email
   - Must match SendGrid verified sender

5. **Verify SendGrid sender** (2 min):
   - SendGrid → Settings → Sender Authentication
   - Add your email and click verification link

**THEN RUN:**
```bash
cd /Users/nunocadete/darwin-agents/projects/b2b-cold-email-consulting
source automation/.env
python3 automation/preflight.py
```

If all checks pass ✅, the system is ready to launch with:
```bash
python3 automation/orchestrator.py initial 20
```

**OPTIONAL (can add later):**
- Apollo.io API key (better prospect finding, 50/month free)
- Hunter.io API key (better email verification, 50/month free)

**Complete instructions:** See `projects/b2b-cold-email-consulting/API-SETUP.md`

**Cost:** $0/month - Everything is free!  
**Email personalization:** Uses local LLM (pi) instead of external APIs.

**Default action if no response in 48h:** Will build a manual fallback system that doesn't require APIs (slower, lower quality, but at least functional)

### Human Response

<!-- Reply here, then change Status to: done -->

---
