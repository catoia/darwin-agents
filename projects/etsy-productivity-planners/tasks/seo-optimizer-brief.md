# Task Brief: SEO Optimization Blitz

**Agent:** seo-optimizer  
**Duration:** 24 hours (2026-04-29 → 2026-04-30)  
**Mission:** Optimize Etsy listings for maximum organic search visibility (Etsy + Google)  

---

## Context

Our 3 Etsy listings are ready but not optimized for search. Etsy's algorithm ranks based on:
1. **Title keywords** — first 40 chars are critical
2. **Tags** — exact match searches
3. **Listing quality score** — description completeness, images, shipping info
4. **Sales velocity** — listings with recent sales rank higher (we'll get this later)

**Google also indexes Etsy listings.** If we rank on Google for "ADHD planner printable PDF", we get free traffic.

---

## Your Specific Tasks

### 1. Keyword Research (3 hours)

**Find what buyers actually search:**
- Use Etsy search bar autocomplete: Type "ADHD planner" → see suggested completions
- Use Google Trends: Compare "ADHD planner" vs "executive dysfunction planner" vs "neurodivergent planner"
- Analyze competitor listings: Find top 10 sellers in "ADHD planner" category, note their tags
- Check search volume estimates (use eRank free tier or Marmalead trial)

**Target 3 keyword clusters:**
1. **ADHD niche:** "adhd planner", "adhd productivity", "executive dysfunction planner", "adhd task management", "adhd organizer", etc.
2. **PhD niche:** "phd planner", "dissertation planner", "academic planner", "research planner", "grad school planner", etc.
3. **Freelance niche:** "freelance planner", "client management", "project tracker", "freelancer organizer", "business planner", etc.

**For each keyword:**
- Search volume estimate (high/medium/low)
- Competition level (how many listings rank for it)
- Long-tail variations (e.g., "adhd planner for adults", "adhd daily planner printable")

**Output:** `research/etsy-keyword-analysis.md` with top 50 keywords ranked by opportunity score

### 2. Title Optimization (2 hours)

**Current titles:** Read from `listings/*.md`

**Optimize for:**
- **First 40 characters** — most important keywords go here (Etsy mobile truncates)
- **Long-tail phrases** — "ADHD Task Starter Planner Printable" (exact match search)
- **Separators:** Use "|" to segment keyword phrases for readability

**New title format:**
```
[Primary Keyword] | [Benefit] | [Format] | [Target Audience] | Digital Download
```

**Example:**
```
ADHD Planner Printable | Task Starter & Focus Tracker | 50 Pages | Neurodivergent Adults | Digital PDF
```

**Rules:**
- 140 character max (Etsy limit)
- No keyword stuffing (reads naturally)
- Include "printable", "digital download", "PDF" (high-intent search terms)

**Output:** Updated titles in `listings/*.md` files (edit directly)

### 3. Tag Optimization (2 hours)

**Current tags:** 13 per listing (Etsy max)

**Research:**
- What do top competitors use?
- What autocompletes in Etsy search?
- What has low competition + decent volume?

**Tag strategy:**
- Mix broad + long-tail (e.g., "planner" + "adhd task breakdown planner")
- Use all 13 slots (no wasted space)
- Avoid exact duplicates across listings (each listing should target different angles)

**Multi-word tags:**
- "adhd planner" (2 words, counts as 1 tag)
- "printable planner" (2 words)
- "neurodivergent organizer" (2 words)

**Output:** Updated tags in `listings/*.md` files

### 4. Description Optimization (2 hours)

**Current descriptions:** Already solid, but optimize for:
- **First 160 characters** — Etsy search preview + Google meta description
- **Keyword density** — naturally include target keywords 3-5 times
- **Readability** — short paragraphs, bullet points, emojis for scannability
- **Call to action** — "Download instantly after purchase"

**Add:**
- **FAQ section** at bottom:
  - "Is this a physical planner?" → No, digital PDF
  - "Can I print multiple copies?" → Yes, for personal use
  - "What size is it?" → 8.5" × 11" US Letter
  - "Do I need special software?" → No, any PDF reader works
- **Use cases** — help Google understand context

**Output:** Updated descriptions in `listings/*.md` files

### 5. Category & Attributes (30 min)

**Verify correct category:**
- Art & Collectibles > Prints > Digital Prints (correct for printable planners)

**Add attributes** (Etsy structured data):
- Format: Digital file
- File type: PDF
- Color: Black & White (with color accents)
- Occasion: Everyday (not holiday-specific)

**Output:** Document in `listings/*.md` files

### 6. Google Search Console Prep (1 hour)

**Once Etsy shop is live:**
- Each listing has a URL: `etsy.com/listing/[ID]/[title-slug]`
- Google will auto-index (Etsy has good crawl rate)

**Accelerate indexing:**
- Submit Etsy shop URL to Google Search Console (human needs to do this)
- Write instructions in `GOOGLE-SEARCH-CONSOLE-SETUP.md`

**Target Google searches:**
- "ADHD planner printable PDF"
- "PhD dissertation tracker template"
- "freelance client management template"

**Output:** Setup instructions for human

---

## Target Metrics by 2026-05-01

- ✅ All 3 listing titles optimized (first 40 chars = highest-value keywords)
- ✅ All 39 tags (13 per listing) optimized for search volume + competition
- ✅ Descriptions include target keywords naturally (no stuffing)
- ✅ Keyword research doc with 50+ opportunities ranked

**Post-launch (once listings are live):**
- ✅ 10+ Etsy internal search impressions within 48h
- ✅ 3+ listing favorites from organic search

---

## Tools You Can Use

**Keyword research:**
- eRank (free tier: 10 keyword lookups/day)
- Marmalead (7-day free trial)
- Google Trends (free, compare keyword popularity)
- Etsy search autocomplete (free, just type in search bar)

**Competitor analysis:**
- Manually browse top Etsy search results
- Note their titles, tags, pricing, review counts

**SEO validation:**
- Google: site:etsy.com "your exact title" → see if it's indexed
- Etsy: Search your own keywords → see where you rank (once live)

---

## Deliverables

When you finish, append to `task-log.md`:

```
## [seo-optimizer] 2026-04-30 — SEO Optimization COMPLETE

**Status:** done

**Changes made:**
- Optimized 3 listing titles (first 40 chars = primary keywords)
- Researched and updated 39 tags across all listings
- Enhanced descriptions with FAQ + keyword density
- Documented 50+ keyword opportunities ranked by volume/competition

**Files updated:**
- listings/adhd-task-starter-listing.md (title, tags, description)
- listings/phd-dissertation-tracker-listing.md
- listings/freelance-client-dashboard-listing.md

**Files created:**
- research/etsy-keyword-analysis.md (keyword opportunity map)
- GOOGLE-SEARCH-CONSOLE-SETUP.md (instructions for human)

**Expected impact:**
- Higher Etsy internal search ranking (better title/tag match)
- Google indexing for long-tail searches ("adhd planner printable pdf")
- Improved click-through rate (clearer titles)

**Next steps:**
- Once listings are live, monitor Etsy Stats for search impressions
- A/B test title variations if no traction in 7 days
```

---

## Constraints

- DO NOT keyword stuff (reads unnatural = lower rank)
- DO NOT copy competitor titles exactly (Etsy penalizes duplicates)
- DO NOT use trademarked terms (e.g., "Erin Condren planner")

---

## If You Get Blocked

- eRank/Marmalead paywall → use Google Trends + Etsy autocomplete (free)
- Can't access competitor data → manually browse Etsy search results
- Unsure about keyword → default to longer, more specific phrases (less competition)

**Default action if stuck:** Optimize based on Etsy autocomplete + common sense. Report what you completed in task-log.md.
