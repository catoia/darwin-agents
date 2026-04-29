# Cold Email Strategy Session Deliverable Template

**Client:** [Client Name]  
**Company:** [Company Name]  
**Session Date:** [Date]  
**Prepared by:** Nuno — Cold Email Consultant  

---

## Executive Summary

**Current state:**
- Response rate: [X]%
- Main issues: [List 2–3 diagnosed problems from session]

**Target state:**
- Response rate: 15–20%
- Booked calls per 100 emails: 4–8

**What we built today:**
- ✅ 5-email cold outreach sequence (copy-paste ready)
- ✅ Prospect targeting strategy (ICP + sourcing)
- ✅ 4-week execution plan
- ✅ Metrics tracking system

---

## Part 1: Your 5-Email Sequence

### Email 1: Cold Outreach (Day 0)

**Subject:** [Specific subject line for their ICP]

**Body:**
```
Hi {{FirstName}},

[Hook — reference specific trigger: funding, LinkedIn post, Product Hunt launch, hiring signal, etc.]

I help [their ICP] [specific outcome]. Spotted a quick win for {{Company}}:

[One specific, actionable tip tailored to their pain point]

Want a free 15-min call to find 3 more fixes like this?

→ [Calendar link]

Best,
[Their name]
```

**Personalization instructions:**
- `{{FirstName}}` — use first name only
- `{{Company}}` — company name
- Hook should reference a real event <30 days old (LinkedIn post, funding, launch)
- Tip should be specific to their industry or product type

**Example (for your ICP):**
[Insert actual example with real hook + tip]

---

### Email 2: Follow-Up #1 (Day 3 — If No Reply)

**Subject:** Re: [same subject as Email 1]

**Body:**
```
Hi {{FirstName}},

I know you're slammed — just one more thing worth knowing:

[Second actionable tip — different from Email 1, equally specific]

Still happy to do a free 15-min call to find more wins for {{Company}}.

→ [Calendar link]

Best,
[Their name]
```

**Example (for your ICP):**
[Insert actual example]

---

### Email 3: Follow-Up #2 (Day 7 — If No Reply)

**Subject:** Last one, then I'll stop

**Body:**
```
Hi {{FirstName}},

I won't keep filling your inbox. But one last thing most [their ICP] miss:

[Third actionable tip — pattern interrupt or contrarian insight]

If you ever want the full breakdown, just reply or grab a slot: [Calendar link]

Take care,
[Their name]
```

**Example (for your ICP):**
[Insert actual example]

---

### Email 4: Breakup / Re-Engagement (Day 14 — If No Reply)

**Subject:** Are you still working on [specific pain point]?

**Body:**
```
Hi {{FirstName}},

Quick check-in — are you still focused on [specific pain point we addressed], or has that shifted?

If it's still a priority and you want help with [outcome], I'm here: [Calendar link]

If not, no worries — I'll stop emailing.

Best,
[Their name]
```

**Use this sparingly.** Only send if they opened Emails 1–3 but didn't reply.

---

### Email 5: Long-Term Re-Engagement (Day 30+ — Optional)

**Subject:** Thought of you — [specific new insight or resource]

**Body:**
```
Hi {{FirstName}},

I just [read/saw/wrote] something about [their pain point or industry trend] and thought of {{Company}}:

[One-line insight or link to useful resource]

If you're still thinking about improving [specific outcome], let's talk: [Calendar link]

Otherwise, hope [Company] is crushing it.

Best,
[Their name]
```

**Use case:** Re-engage cold prospects after 30–60 days with new value (blog post, case study, industry report).

---

## Part 2: Prospect Targeting Strategy

### Your Ideal Customer Profile (ICP)

**Demographics:**
- Title: [e.g., Founder, VP Sales, Head of Marketing]
- Company stage: [e.g., Seed to Series A, $1M–$10M ARR]
- Company type: [e.g., B2B SaaS, fintech, devtools]
- Company size: [e.g., 5–50 employees]
- Location: [e.g., North America, remote-first]

**Psychographics (pain points):**
- They are struggling with: [specific pain point]
- They currently solve it by: [manual process or inferior tool]
- They care most about: [speed, cost, compliance, ROI, etc.]

**Signals they're a good fit:**
- Recently raised funding (need to scale sales fast)
- Posted on LinkedIn about [pain point]
- Hiring for sales roles (scaling outbound)
- Launched on Product Hunt (need pipeline now)
- Competitor mention in LinkedIn activity

---

### Where to Find Them

**Primary sources (start here):**
1. **LinkedIn Sales Navigator**
   - Filter: Title = "Founder", Industry = "B2B SaaS", Company size = 5–50
   - Search for posts mentioning [pain point keywords]
   - Export to CSV (use tool like Phantombuster or manual scraping)

2. **Y Combinator Directory**
   - https://www.ycombinator.com/companies
   - Filter: B2B tag, recent batch (W24, S24, W25)
   - Scrape founder emails (usually firstname@company.com)

3. **Product Hunt**
   - https://www.producthunt.com/topics/b2b
   - Filter: Launched in last 6 months
   - Find founders via "Makers" section

4. **Apollo.io or Hunter.io**
   - Use filters: Title = "Founder", Company size, Industry
   - Verify emails before sending (Hunter.io email verifier)

**Target list size:**
- **Week 1 (pilot):** 50 prospects
- **Week 2–3 (if pilot works):** 100 prospects
- **Week 4+ (scale):** 200+ prospects/week

---

### Email Verification

**Before sending, verify emails to avoid bounces:**
- Use Hunter.io email verifier (free tier: 50/month)
- Use NeverBounce or ZeroBounce (paid, but worth it for large lists)
- Check domain has MX records: `dig [domain.com] MX`

**Bounce rate target:** <5%

---

## Part 3: 4-Week Execution Plan

### Week 1: Build & Launch Pilot Campaign

**Monday–Tuesday:**
- [ ] Build prospect list (50 qualified leads)
- [ ] Verify emails (use Hunter.io or manual check)
- [ ] Write CSV with columns: first_name, email, company, hook, industry

**Wednesday:**
- [ ] Personalize Email 1 for all 50 prospects (use template above)
- [ ] Load into email tool (SendGrid, Mailchimp, or manual Gmail)
- [ ] Send first batch (10–20 emails)

**Thursday–Friday:**
- [ ] Send remaining emails (spread sends across 2 days to avoid spam filters)
- [ ] Track in spreadsheet: name, email, sent_date, opened, replied

**Weekend:**
- [ ] Monitor inbox for replies
- [ ] Respond to any replies within 24 hours
- [ ] Book free teardown calls

---

### Week 2: Follow-Up & Iterate

**Monday (Day 3 after Email 1):**
- [ ] Send Email 2 (Follow-Up #1) to all who didn't reply
- [ ] Personalize with second tip (different from Email 1)

**Tuesday–Wednesday:**
- [ ] Continue monitoring replies
- [ ] Conduct any teardown calls booked
- [ ] Track conversion rate: calls booked / emails sent

**Thursday (Day 7 after Email 1):**
- [ ] Send Email 3 (Breakup) to all who didn't reply to Email 1 or 2

**Friday:**
- [ ] Review pilot campaign metrics:
   - Open rate (target: >40%)
   - Reply rate (target: >10%)
   - Call booking rate (target: >4%)
- [ ] Identify what worked: which hooks, which tips, which subject lines

---

### Week 3: Scale What Works

**Monday–Tuesday:**
- [ ] Build second prospect list (100 leads this time)
- [ ] Use learnings from Week 1: best hooks, best tips
- [ ] Refine Email 1 based on reply data

**Wednesday–Friday:**
- [ ] Send Email 1 to 100 new prospects (spread across 3 days)
- [ ] Continue follow-ups for Week 1 prospects (Email 2/3 as needed)
- [ ] Conduct teardown calls + pitch paid sessions

---

### Week 4: Optimize & Convert

**Monday–Wednesday:**
- [ ] Send Email 2/3 follow-ups for Week 3 prospects
- [ ] A/B test: try 2 subject line variants with 50 prospects each
- [ ] Track which variant gets more opens/replies

**Thursday–Friday:**
- [ ] Conduct paid strategy sessions (goal: 2–4 this week)
- [ ] Review full month metrics:
   - Total emails sent
   - Total replies
   - Total calls booked
   - Total paid sessions sold
   - Revenue generated
- [ ] Plan Month 2: scale to 200+ prospects/week or double down on best-performing segment

---

## Part 4: Metrics Tracking System

### What to Track (Minimum)

| Metric | Target | How to Measure |
|---|---|---|
| **Open rate** | >40% | Use email tracking tool (SendGrid, Mailchimp, Yesware) |
| **Reply rate** | >10% | Count replies / emails sent |
| **Booking rate** | >4% | Count calls booked / emails sent |
| **Show-up rate** | >80% | Count calls conducted / calls booked |
| **Paid conversion** | >30% | Count paid sessions / teardown calls |
| **Bounce rate** | <5% | Count bounces / emails sent |

### Weekly Review Cadence

**Every Friday:**
- Update metrics spreadsheet
- Identify best-performing hooks, tips, subject lines
- Kill underperforming variants (if reply rate <5% after 50 sends, stop using that hook)
- Plan next week's sends

---

### Tracking Spreadsheet Template

**Google Sheet columns:**
| Date | Prospect Name | Email | Company | Hook Used | Tip Used | Sent | Opened | Replied | Booked | Paid | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2026-05-01 | Alex Tkachuk | alex@screendesk.io | Screendesk | Funding | Dev ROI tip | ✅ | ✅ | ❌ | ❌ | ❌ | Opened but no reply |

**Download template:** [Insert Google Sheet link]

---

## Part 5: A/B Testing Plan

### What to Test (Priority Order)

**1. Subject lines (Week 2)**
- Variant A: `{{FirstName}}, quick cold email feedback?`
- Variant B: `One fix for {{Company}}'s cold emails`
- Send each to 25 prospects, compare open rates

**2. Hook type (Week 3)**
- Variant A: Funding announcement hook
- Variant B: LinkedIn post hook
- Send each to 50 prospects, compare reply rates

**3. Tip specificity (Week 4)**
- Variant A: Generic tip (subject line is too long)
- Variant B: Industry-specific tip (fintech buyers need trust signals)
- Send each to 50 prospects, compare booking rates

**Rule:** Only test ONE variable at a time. Change subject line OR hook OR tip, never all three.

---

## Part 6: Common Mistakes to Avoid

❌ **Sending 100+ emails on Day 1** → Looks like spam, damages domain reputation. Ramp up gradually: 10–20/day for first week.

❌ **Using HTML templates with images/logos** → Triggers spam filters. Plain text only.

❌ **Blasting the same email to everyone** → 0% personalization = 0% replies. Always customize the hook.

❌ **Following up more than 3 times** → Becomes harassment. Stop after Email 3 unless they engaged (opened multiple times).

❌ **Not tracking metrics** → You can't improve what you don't measure. Track everything in the spreadsheet.

❌ **Giving up after 50 emails** → Sample size is too small. Send 200+ before deciding something doesn't work.

---

## Part 7: Next Steps

**Immediate (this week):**
1. [ ] Build your first prospect list (50 leads)
2. [ ] Send Email 1 to 10 prospects (pilot batch)
3. [ ] Set up tracking spreadsheet
4. [ ] Monitor replies

**Week 2:**
1. [ ] Send follow-ups (Email 2/3)
2. [ ] Book first teardown calls
3. [ ] Scale to 50–100 emails/week

**Week 3–4:**
1. [ ] Conduct paid sessions
2. [ ] Hit $400–800 revenue target
3. [ ] Refine based on data

---

## Questions? Stuck?

**Email me:** [Your email]  
**LinkedIn:** [Your LinkedIn]  
**Book follow-up:** [Calendar link]

---

**End of Deliverable**

---

## Usage Instructions for Agent

1. **Populate this template during the 90-minute session** with the client
2. **Send within 24 hours** as a Google Doc (editable) or PDF (polished)
3. **Track completion**: Follow up in 7 days: "How's the list-building going?"
4. **Ask for testimonial**: After they see results (2–3 weeks later), request a LinkedIn recommendation or quote
