# Task Brief: Prospect Researcher

**Agent type:** Task agent  
**Project:** b2b-cold-email-consulting  
**Mission:** Find 50 B2B SaaS founders who need cold email help  

## Target Profile

**Who we're looking for:**
- **Stage:** Seed to Series A (early-stage, growing)
- **Type:** B2B SaaS product (not consumer apps)
- **Sales motion:** Selling to enterprises/businesses
- **Pain point:** Likely struggling with cold outreach (check if they post about sales challenges on LinkedIn)
- **Reachable:** Founder is active on LinkedIn, has public email or findable via hunter.io pattern

## Research Sources

1. **Y Combinator batches** — Filter B2B companies from recent batches (W24, S24, W25)
   - https://www.ycombinator.com/companies
   - Look for "B2B" tag, enterprise software, dev tools

2. **Product Hunt** — B2B tools launched in last 6 months
   - https://www.producthunt.com/topics/b2b
   - Sort by recent, filter for early-stage

3. **LinkedIn search**
   - Query: "Founder" + "B2B SaaS" + "Seed funded"
   - Look for recent posts about GTM, sales hiring, or growth challenges

4. **Indie Hackers**
   - https://www.indiehackers.com/products
   - Filter for B2B products with <$10k MRR (still need help)

## Deliverable Format

Create **prospects.csv** with 50 leads:

```csv
name,email,company,product_description,why_they_need_help,linkedin_url,source
John Smith,john@acme.io,Acme,B2B sales automation for SMBs,Posted on LinkedIn about struggling with cold email response rates,https://linkedin.com/in/johnsmith,LinkedIn
```

**Required fields:**
- `name` — First + last name
- `email` — Verified or pattern-guessed (firstname@company.com)
- `company` — Company name
- `product_description` — One-line description of what they sell
- `why_they_need_help` — Specific evidence (LinkedIn post, fundraising news, job posting for sales role)
- `linkedin_url` — Their LinkedIn profile
- `source` — Where you found them (YC, PH, LinkedIn, IH)

## Quality Bar

- **50 total prospects minimum**
- **All emails must be plausible** (check domain has MX records if possible)
- **Prioritize founders with recent evidence of sales challenges** — posts, hiring sales roles, asking for GTM advice
- **Diversity** — mix of industries (fintech, devtools, HR tech, martech, etc.)

## Execution Instructions

1. Spend 10 minutes per source (YC, PH, LinkedIn, IH)
2. Use browser automation or manual CSV export where available
3. For missing emails, use pattern: firstname@company.com or check company website /about or /team pages
4. Write results to `projects/b2b-cold-email-consulting/prospects.csv`
5. Append summary to `projects/b2b-cold-email-consulting/task-log.md`:
   - Total found
   - Breakdown by source
   - Top 3 most promising prospects and why
   - Any challenges encountered

**Time budget:** 2 hours max

**When done:**
- Save prospects.csv
- Append results to task-log.md
- Exit
