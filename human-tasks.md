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
