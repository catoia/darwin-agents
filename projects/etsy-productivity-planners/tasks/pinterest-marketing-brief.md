# Task Brief: Pinterest Marketing Blitz

**Agent:** pinterest-marketing  
**Duration:** 48 hours (2026-04-29 → 2026-05-01)  
**Mission:** Generate 100+ impressions from Pinterest before Etsy listings go live  

---

## Context

Our 3 Etsy planner listings are ready but not yet uploaded. Etsy ads are BLOCKED for 2 weeks (new account). We need external organic traffic NOW.

**50% of Etsy sales come from Pinterest.** This is THE primary channel for planner sellers.

---

## Your Specific Tasks

### 1. Research Phase (2 hours)
**Find winning pins:**
- Search Pinterest for "ADHD planner printable", "PhD planner", "freelance project tracker"
- Identify top 10 pins with highest engagement (saves + comments)
- Note common patterns: image style, title format, description keywords
- Find 5 active group boards for "planners" or "productivity printables"

**Output:** Document findings in `research/pinterest-winning-patterns.md`

### 2. Account Setup (30 min)
**Create Pinterest Business Account:**
- Name: "ADHD & Productivity Planners" (or similar)
- Profile description: "Printable planners designed for ADHD, PhD students, and freelancers. Digital downloads that actually match how your brain works."
- Profile image: Use one of our planner mockup hero images
- Verify website: Once Etsy shop URL is live, add it

**If you don't have human credentials:**
- Write setup instructions in `PINTEREST-SETUP-INSTRUCTIONS.md`
- Use `human_task` (high priority) to request the human create the account
- Continue with content creation below while waiting

### 3. Pin Image Creation (4 hours)
**Create 21 Pinterest-optimized pins** (7 per planner):

**Pinterest image specs:**
- Size: 1000×1500px (2:3 ratio — Pinterest standard)
- Format: JPG or PNG
- Text overlay: Large, readable headlines
- Colors: High contrast (planner content + bold text)

**Use existing mockups as base:**
- Take mockups from `photos/adhd-mockup-*.jpg`
- Resize to Pinterest dimensions
- Add text overlays with value propositions

**Pin titles (examples):**
- "ADHD Task Starter Planner | Break Down Overwhelming To-Dos [Printable PDF]"
- "PhD Dissertation Progress Tracker | 60 Pages to Keep You on Track"
- "Freelance Client Dashboard | Manage 10+ Projects Without Chaos"

**Pin descriptions (150-300 chars):**
- Include target keywords: "ADHD planner printable", "executive dysfunction planner", etc.
- Call to action: "Download instantly on Etsy"
- Hashtags: #ADHDPlanner #ProductivityPrintable #DigitalDownload

**Save pins to:** `pinterest-content/pin-*.jpg`

### 4. Pinning Strategy (24 hours)
**Create 3 boards:**
1. "ADHD Productivity Planners"
2. "Academic & PhD Planning Tools"
3. "Freelance & Client Management Printables"

**Pin schedule:**
- Day 1: Pin all 21 images (7 to each board)
- Use Tailwind or manual pinning (space out by 1-2 hours)
- Write unique descriptions for each pin (don't copy-paste)

**Engagement:**
- Join 5 group boards related to planners/productivity
- Request access if needed (most auto-approve)
- Repin 10 popular planner pins from other creators (build community presence)
- Comment on 10 pins with genuine value (not spam)

### 5. Metrics Tracking (ongoing)
**Track daily:**
- Impressions (views) per pin
- Saves (most important metric)
- Clicks to Etsy (once shop is live)
- Profile followers

**Target metrics by 2026-05-01:**
- ✅ 100+ total impressions
- ✅ 10+ saves
- ✅ 5+ profile followers
- ✅ 3+ group board memberships

---

## Tools You Can Use

**Image editing:**
- Canva (free tier) — has Pinterest templates built-in
- Pillow (Python) — programmatic text overlay on mockups
- GIMP (free desktop app)

**Pin scheduling:**
- Tailwind (free trial: 20 pins/month)
- Manual pinning (perfectly fine for 21 pins)

**Analytics:**
- Pinterest Analytics (built-in to business account)
- Track manually in spreadsheet if needed

---

## Deliverables

When you finish, append to `task-log.md`:

```
## [pinterest-marketing] 2026-05-01 — Pinterest Marketing Blitz COMPLETE

**Status:** done

**Metrics achieved:**
- Impressions: [X]
- Saves: [X]
- Profile followers: [X]
- Group boards joined: [X]

**Files created:**
- 21 Pinterest-optimized pins (pinterest-content/pin-*.jpg)
- Pinterest setup instructions (PINTEREST-SETUP-INSTRUCTIONS.md)
- Winning pattern research (research/pinterest-winning-patterns.md)

**Next steps:**
- Once Etsy shop is live, update all pin links to point to actual listings
- Schedule weekly repinning (evergreen content)
- Monitor which pins get most saves → create more of that style
```

---

## Constraints

- DO NOT spam. Pinterest will shadowban you.
- DO NOT use copyrighted images. Only use our mockups + stock photos.
- DO NOT buy fake followers/engagement. Organic only.

---

## If You Get Blocked

- Pinterest account creation requires phone number → use `human_task` to request human create account
- Group board access denied → focus on your own boards, skip group boards
- Canva paywall → use Pillow (Python) or GIMP instead

**Default action if stuck:** Document what you completed, what's blocked, and what the human needs to do. Report in task-log.md.
