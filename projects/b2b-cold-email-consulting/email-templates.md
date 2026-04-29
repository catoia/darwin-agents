# Cold Email Sequence — B2B SaaS Founders

> **Target:** B2B SaaS founders (Seed–Series A) with low cold email response rates  
> **Offer:** Free 15-min cold email teardown → $200 paid 90-min strategy session  
> **Goal:** Book teardown calls that convert to paid sessions  
> **Calendar link:** https://calendly.com/coldemailteardown

---

## Email 1: The Hook (Day 0)

**Subject:** {{FirstName}}, quick cold email feedback?

**Body:**

Hi {{FirstName}},

{{Hook}}.

I help B2B SaaS founders improve cold email response rates — and I spotted a quick win for {{Company}}:

{{SpecificTip}}

Want a free 15-min teardown of your current emails? I'll find 3 more fixes like this.

→ https://calendly.com/coldemailteardown

Best,
Nuno

---

## Email 2: The Nudge (Day 3)

**Subject:** Re: quick cold email feedback?

**Body:**

Hi {{FirstName}},

I know you're slammed — just one more thing worth knowing:

Most B2B cold emails bury the CTA at the bottom after three paragraphs of context. By then, the reader's gone.

Move your ask to line 3. Response rates typically jump 20–35%.

Still happy to do a free 15-min teardown of {{Company}}'s outreach. No prep needed.

→ https://calendly.com/coldemailteardown

Best,
Nuno

---

## Email 3: The Breakup (Day 7)

**Subject:** Last one, then I'll stop

**Body:**

Hi {{FirstName}},

I won't keep filling your inbox. But one last thing most founders miss: your email signature is selling against you — a wall of links and titles reads as "vendor," not "advisor."

Strip it to name + one line. Trust goes up.

If you ever want the full teardown, just reply or grab a slot: https://calendly.com/coldemailteardown

Take care,
Nuno

---

## Personalization Guide

### Variable Reference

| Variable | Source | Example |
|---|---|---|
| `{{FirstName}}` | prospects.csv col: first_name | "Alex" |
| `{{Company}}` | prospects.csv col: company | "Screendesk" |
| `{{Hook}}` | See Hook Variants below | "Congrats on the Seed round" |
| `{{SpecificTip}}` | See Tips by Industry below | "Your subject line is too feature-led..." |

---

### Hook Variants (choose the most recent/relevant trigger)

**1. LinkedIn post about sales/GTM:**
> "I saw your post about struggling with cold email response rates"

**2. Fundraise announcement:**
> "Congrats on the Seed round — growing a sales pipeline fast is the next big challenge"

**3. Product Hunt launch:**
> "Congrats on launching {{Company}} on Product Hunt — converting that attention into pipeline is the hard part"

**4. Hiring for sales roles:**
> "I noticed {{Company}} is hiring for sales roles — that usually means cold outreach is about to scale up"

**5. Recent blog post / podcast appearance:**
> "I caught your piece on [GTM strategy / outbound sales / growth] — solid take"

**Selection logic for pi automation:**
1. Check LinkedIn for posts in last 14 days → use Hook 1
2. Check Crunchbase/LinkedIn for funding < 60 days → use Hook 2
3. Check Product Hunt for launch < 30 days → use Hook 3
4. Check LinkedIn Jobs for SDR/AE roles → use Hook 4
5. Fallback → use Hook 5 with a relevant content reference

---

### Specific Tips by Industry

#### Devtools / Developer Tools

**Tip A — Subject line is feature-led:**
> "Your subject line reads like a product announcement ('Introducing [Tool]'). Engineers skim it. Try: 'Cut deployment time by 40%' — lead with the outcome."

**Tip B — Body is too technical:**
> "Your emails lead with architecture and integrations. Engineering buyers still answer to a budget. Open with the ROI, then prove the tech."

**Tip C — CTA is too demo-heavy:**
> "Asking for a demo in email 1 is high friction for devs. Offer something lighter — a 10-min Loom walkthrough or a sandbox link they can try solo."

---

#### Fintech / Financial Services SaaS

**Tip A — Missing trust signals:**
> "Finance buyers live in a compliance-first world. Email 1 with no social proof reads as risk. Add one client name or a one-line result ('We helped [Bank X] cut reconciliation time by 3 hours/week')."

**Tip B — CTA language is generic:**
> "Your CTA 'Book a demo' doesn't clear the compliance anxiety. Try: 'See how [Company X] saved $50k on [specific process]' — specificity earns clicks in fintech."

**Tip C — Email is too long:**
> "Fintech buyers are senior, time-poor, and skeptical. If your email is over 100 words, it's already too long. Cut to hook → one proof point → ask."

---

#### HR Tech / People Operations SaaS

**Tip A — Leading with features, not outcomes:**
> "HR leaders are bought on outcomes that tie to retention or compliance, not features. Open with: 'Most HR teams using [old process] lose 8 hours/week on X.' Then show the fix."

**Tip B — Subject line is too vague:**
> "Your subject line could apply to any SaaS. Try something specific to their pain: 'Reduce onboarding time for remote hires' or 'Fix [specific compliance gap] before it costs you.'"

**Tip C — No risk mitigation:**
> "HR buyers are risk-averse — one bad vendor choice affects the whole company. Mention one relevant compliance certification or a quick 'no setup required / cancel anytime' in your first touch. Lowers the barrier to reply."

---

#### Martech / Marketing SaaS

**Tip A — Talking to the wrong metric:**
> "Marketing buyers have shifted from vanity metrics to revenue attribution. If your email mentions impressions, reach, or engagement — reframe everything around pipeline and closed-won."

**Tip B — Subject line is overused:**
> "Subject lines like 'Improve your email marketing ROI' are deleted without a read. Try pattern-interrupting with specificity: '{{Company}}'s onboarding emails have a 12% open rate — here's why that's low.'"

**Tip C — CTA is too open-ended:**
> "Asking 'would love to connect' gives the reader nothing to grab. Make the next step obvious and low-friction: '15 mins this week — I'll show you the one change that moved [Company X] from 12% to 31% reply rate.'"

---

## Sequence Timing

```
Day 0  → Email 1: The Hook        (personalized, value-first)
Day 3  → Email 2: The Nudge       (new tip, soft re-offer)
Day 7  → Email 3: The Breakup     (final tip, graceful exit)
```

No follow-up after Day 7. If they reply at any point, pause the sequence and switch to manual conversation.

---

## Quality Checklist Before Sending

- [ ] Subject line is ≤ 7 words, no punctuation at end
- [ ] Hook references something specific and recent (< 30 days preferred)
- [ ] SpecificTip is relevant to their industry
- [ ] CTA is one clear link, not multiple options
- [ ] Email is plain text — no images, no HTML buttons, no logo
- [ ] From name is "Nuno" not "Nuno Cadete from [Company]"
- [ ] Signature is clean: name + one-liner only
- [ ] No attachments in cold outreach
