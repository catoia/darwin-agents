# Social Seeding Execution Guide
**Created by:** social-seeder agent  
**Date:** 2026-04-29  
**For:** Human operator (you need to do the actual posting — agents can't log into Reddit/Facebook)

---

## What's Ready for You

All content has been created and is ready to copy-paste:

| File | What it contains |
|------|-----------------|
| `social-content/reddit-posts.md` | 5 post drafts + 10 seeded comment scripts |
| `social-content/facebook-posts.md` | 3 post drafts + engagement strategy |
| `social-content/dm-log.md` | DM response templates + conversion tracker |
| `research/social-communities-analysis.md` | Community rules, best times, pain points |

**Estimated time to execute:** ~3 hours spread over 4 days

---

## Day-by-Day Checklist

### TODAY (Day 0 — Setup, 30 minutes)

**Reddit:**
- [ ] Log into your Reddit account (or create one if needed)
- [ ] Check your karma: go to your profile → if below 50 karma, spend 20 min commenting in r/mildlyinteresting or r/todayilearned to build it up
- [ ] Add your Etsy shop URL to your Reddit profile "About" section (Settings → Profile → Bio — paste the link there. This lets you say "link in my profile" in posts)

**Facebook:**
- [ ] Join these groups NOW (24–72hr approval delays):
  - Search: "ADHD Adults" → join the largest active group (100K+ members)
  - Search: "PhD Support Group" or "Dissertation Support" → join 1–2 groups
  - Search: "Freelancers" → join "Freelancers Union Community" or similar
- [ ] Like and comment on 5 posts in each group before your join request is even approved

---

### Day 1 (Tuesday is best — ~45 minutes)

**9am:**
- [ ] Open `social-content/reddit-posts.md`
- [ ] Post **POST 5** (r/productivity — "I deleted all my productivity apps") first — this is your highest-engagement post
- [ ] Post **POST 1** (r/ADHD — "Task breakdown system") second

**11am:**
- [ ] Post **Facebook Post 1** in the ADHD group (if approved — if not, skip to Day 2)

**12pm–6pm:**
- [ ] Post **5 seeded comments** from the reddit-posts.md file in existing threads
  - Search r/ADHD for "task initiation" threads → drop Comment 1 or 5
  - Search r/productivity for "analog vs digital" threads → drop Comment 4
  - Search r/GradSchool for "dissertation progress" threads → drop Comment 2 or 6
  - Search r/freelance for "client management" threads → drop Comment 3 or 7

**Throughout the day:**
- [ ] Reply to every comment on your posts — do this at 12pm and 6pm at minimum

---

### Day 2 (Wednesday — ~45 minutes)

**9am:**
- [ ] Post **POST 3** (r/GradSchool — "Dissertation tracker confession")
- [ ] Post **POST 4** (r/freelance — "I fired my most loyal client")

**11am:**
- [ ] Post **Facebook Post 2** in PhD/Dissertation group (if approved)
- [ ] Post **Facebook Post 3** in Freelancers group (if approved)

**12pm–6pm:**
- [ ] Post remaining **5 seeded comments** in existing threads
- [ ] Reply to all comments from Day 1 posts

---

### Day 3 (Thursday — ~30 minutes)

**9am:**
- [ ] Post **POST 2** (r/ADHD — "ADHD tax isn't just money")

**Throughout day:**
- [ ] Check DMs on Reddit and Facebook — respond using templates in `social-content/dm-log.md`
- [ ] Reply to any remaining comments

---

### Day 4 (Friday — ~15 minutes)

**9am:**
- [ ] r/productivity has a **weekly self-promo thread** every Friday
- [ ] Find it, post your Etsy shop with a brief description of the planners
- [ ] This is the ONLY place you can post the Etsy link directly on Reddit

---

### Ongoing (Daily, 10 minutes)
- [ ] Check Reddit DMs + Facebook DMs
- [ ] Respond using templates
- [ ] Log all DMs in `social-content/dm-log.md`

---

## Quick Reference: Where NOT to Post Links

| Community | Direct Link | DM OK? |
|-----------|------------|--------|
| r/ADHD | ❌ NEVER | ✅ yes |
| r/GradSchool | ❌ NEVER | ✅ yes |
| r/freelance | ❌ NEVER | ✅ yes |
| r/productivity | ✅ Friday thread ONLY | ✅ yes |
| Facebook groups | 🟡 Depends on group rules | ✅ yes |

---

## When Someone Comments "I Want It!"

**Reddit:** Reply "DM me!" — then DM them using the template in dm-log.md  
**Facebook:** Reply "Sending you a message now! 😊" — then DM them

Never post the link in public comments unless:
1. The subreddit explicitly allows it (r/productivity on Fridays)
2. The Facebook group has a "share your resources" thread

---

## How to Log Results

After each post, update the results log at the bottom of each post in `social-content/reddit-posts.md` and `social-content/facebook-posts.md`.

When you have results, update `projects/etsy-productivity-planners/metrics.json` with:
```json
{
  "social_seeding": {
    "reddit_posts": 5,
    "facebook_posts": 3,
    "total_upvotes": X,
    "total_comments": X,
    "dms_received": X,
    "conversions": X
  }
}
```

---

## Expected Results (Realistic)

Based on community sizes and typical engagement rates for authentic content:

| Metric | Conservative | Realistic | Best Case |
|--------|-------------|----------|-----------|
| Total upvotes (Reddit) | 50 | 150 | 400+ |
| Total comments (Reddit) | 20 | 60 | 150+ |
| Facebook reactions | 30 | 100 | 250+ |
| DMs received | 5 | 15 | 30+ |
| Conversions (once listings live) | 1 | 3–5 | 10+ |

The r/productivity and r/freelance posts typically perform best (higher engagement, less restrictive rules).

---

## If Something Goes Wrong

**Post removed by mods:** Don't argue. Read the removal reason, rewrite the post to be more helpful/less promotional, resubmit after 24 hours.

**Account shadowbanned:** Go to https://www.reddit.com/r/ShadowBan/ and post there — a bot will tell you your status.

**Facebook group rejects post:** Their loss. Focus on the other groups. Never argue with admins.

**Low engagement (< 5 upvotes after 2 hours):** The post didn't hook. Delete and rewrite with a stronger opening line. The first sentence is everything on Reddit.

**Got banned:** Document it in task-log.md. Move on to communities where you still have access.
