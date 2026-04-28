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

**Human response:** 
**Status:** open


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

**Human response:** 
**Status:** open

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

**Human response:**  
**Status:** open
