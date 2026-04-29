# Task Brief: Email Copywriter

**Agent type:** Task agent  
**Project:** b2b-cold-email-consulting  
**Mission:** Write cold email sequence (3 emails) optimized for B2B SaaS founders  

## Context

**Who we're emailing:** B2B SaaS founders (Seed–Series A) struggling with cold email response rates  
**What we offer:** Free 15-min cold email teardown → $200 paid 90-min strategy session  
**Goal:** Book free teardown calls that convert to paid sessions  

## Email Sequence Structure

### Email 1: The Hook (Day 0)
**Subject:** "{{FirstName}}, quick cold email feedback?"  
**Body:**
- Hook: Reference something specific (their LinkedIn post, recent Product Hunt launch, fundraising)
- Quick credibility: "I help B2B SaaS founders improve cold email response rates"
- Value prop: "I noticed [specific issue with their outreach] — here's one quick fix:"
- Give ONE actionable tip (e.g., "Your subject line is too salesy — try: [rewrite]")
- Soft CTA: "Want a free 15-min teardown of your current cold email? I'll find 3 more fixes."
- Link to calendar (Calendly placeholder: calendly.com/coldemailteardown)

**Length:** 80–120 words max  
**Tone:** Direct, helpful, no fluff  

### Email 2: The Nudge (Day 3)
**Subject:** "Re: quick cold email feedback?"  
**Body:**
- Acknowledge they're busy
- Add NEW value (don't repeat Email 1): "Here's another thing I see with B2B cold emails:"
- Give second actionable tip (e.g., "Your CTA is buried — move it up")
- Restate free offer: "15 minutes, 3 more fixes like this. Free."
- Calendar link

**Length:** 60–90 words  
**Tone:** Respectful persistence, more value  

### Email 3: The Breakup (Day 7)
**Subject:** "Last one, then I'll stop"  
**Body:**
- Pattern interrupt: "I won't keep emailing you"
- Final value drop: "But here's one last fix most founders miss: [tip]"
- Soft close: "If you ever want the full teardown, just reply or grab a slot: [calendar]"
- Exit gracefully

**Length:** 40–60 words  
**Tone:** No pressure, leaving door open  

## Personalization System

Create **email-templates.md** with:
1. Base templates (above)
2. Personalization instructions for pi CLI to use:
   - `{{FirstName}}` → extracted from prospects.csv
   - `{{Company}}` → company name
   - `{{Hook}}` → one of these patterns:
     - "I saw your post about [sales/GTM challenge]"
     - "Congrats on the [fundraise/Product Hunt launch]"
     - "I noticed [your company] is hiring for sales roles"
   - `{{SpecificTip}}` → tailored to their industry (generate 3 variants for devtools, fintech, HR tech)

## Deliverable Format

Create **email-templates.md**:

```markdown
# Cold Email Sequence — B2B SaaS Founders

## Email 1: The Hook (Day 0)

**Subject:** {{FirstName}}, quick cold email feedback?

**Body:**
Hi {{FirstName}},

I saw {{Hook}}. I help B2B SaaS founders improve cold email response rates.

I noticed {{SpecificIssue}} in your outreach. Here's a quick fix:

{{SpecificTip}}

Want a free 15-min teardown of your current emails? I'll find 3 more fixes like this.

{{Calendar}}

Best,  
Nuno

---

## Email 2: The Nudge (Day 3)

[template...]

---

## Email 3: The Breakup (Day 7)

[template...]

---

## Personalization Guide

### Hook Variants:
1. LinkedIn post: "I saw your post about [struggling with sales/cold email response rates/GTM strategy]"
2. Fundraise: "Congrats on the [Seed/Series A] round"
3. Product Hunt: "Congrats on launching {{Company}} on Product Hunt"
4. Hiring: "I noticed {{Company}} is hiring for sales roles"

### Specific Tips (by industry):
**Devtools:**
- "Your emails are too technical — developers want to see ROI first, not architecture"
- "Your subject line: 'Introducing [Tool]' → Try: 'Cut deployment time by 40%'"

**Fintech:**
- "Finance buyers need trust signals — add one client logo or case study in Email 1"
- "Your CTA 'Book a demo' → Try: 'See how [Company X] saved $50k'"

**HR Tech:**
- "HR buyers are risk-averse — lead with compliance/security, not features"
- "Your subject line is too vague → Try: 'Fix [specific HR pain point]'"

[Add 3 more variants per category]

```

## Execution Instructions

1. Write all 3 email templates (clean, no fluff)
2. Create hook variants (5 options)
3. Create specific tip variants (3 per industry: devtools, fintech, HR tech, martech)
4. Write personalization guide for pi to use when sending
5. Save to `projects/b2b-cold-email-consulting/email-templates.md`
6. Append summary to `projects/b2b-cold-email-consulting/task-log.md`:
   - Template structure overview
   - Key differentiators from generic cold emails
   - Conversion hypothesis (why this will work)

**Time budget:** 1 hour max

**When done:**
- Save email-templates.md
- Append results to task-log.md
- Exit
