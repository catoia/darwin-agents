# Human Setup Instructions — Etsy Productivity Planners

**Agent:** etsy-productivity-planners  
**Created:** 2026-04-28  
**Status:** URGENT — needs immediate action to get to first sale  

---

## What I've Done

✅ Researched 3 underserved Etsy planner niches
✅ Designed 3 planner templates with full specifications
✅ Written 3 SEO-optimized Etsy listings (titles, descriptions, tags)

## What You Must Do (in order)

### STEP 1: Set Up Etsy Seller Account (30 minutes)

1. Go to https://www.etsy.com/sell
2. Click "Open your Etsy shop"
3. Choose shop preferences:
   - **Shop language:** English
   - **Shop country:** United States (or your location)
   - **Shop currency:** USD
4. Choose shop name:
   - **Suggestion:** "ProductivityPlannersHub" or "NicheOrganizersShop"
   - Must be unique, professional, and searchable
5. Complete payment setup:
   - Add bank account for deposits (Etsy pays out weekly)
   - Set up Etsy Payments (required)
6. Set shop policies:
   - **Return policy:** "All sales final (digital download)"
   - **Processing time:** "Instant download"
   - **Privacy policy:** Use Etsy's template

**Cost:** $0.20 per listing + 6.5% transaction fee when you make a sale

---

### STEP 2: Create the 3 Planner PDFs (2–3 hours)

I've created detailed design specifications for each planner. You need to turn these into actual PDF files.

**Option A: Use Canva (recommended, easiest)**
1. Go to canva.com (free account works)
2. Create a new design → Custom size → 8.5 × 11 inches
3. Follow the design specs in:
   - `templates/adhd-task-starter-design-spec.md`
   - `templates/phd-dissertation-tracker-design-spec.md`
   - `templates/freelance-client-dashboard-design-spec.md`
4. Create each page layout as specified
5. Download as PDF (high quality, print-ready)

**Option B: Use Microsoft Word or Google Docs**
1. Set page size to US Letter (8.5" × 11")
2. Create the layouts following the ASCII art diagrams in the design specs
3. Use tables and text boxes to match the layouts
4. Export as PDF

**Option C: Hire on Fiverr (if you're short on time)**
1. Find a designer on Fiverr ($20–40 for all 3 planners)
2. Send them the 3 design spec files
3. Request print-ready PDFs
4. Review and approve

**Output files you need:**
- `ADHD-Task-Starter-Planner-50-Printable-Sheets.pdf`
- `PhD-Dissertation-Progress-Tracker-60-Printable-Pages.pdf`
- `Freelance-Client-Project-Dashboard-55-Printable-Pages.pdf`

Save these in `projects/etsy-productivity-planners/products/`

---

### STEP 3: Create Listing Mockup Photos (1 hour)

Etsy listings need professional-looking photos. You need 7 images per listing (21 total).

**Option A: Use Canva mockup templates (easiest)**
1. In Canva, search "planner mockup" templates
2. Upload your PDF pages
3. Create these 7 images for EACH planner:
   - Cover image (clean desk scene with planner page visible)
   - Page 1 zoomed in (show the actual layout clearly)
   - Page 2 example (partially filled in as demo)
   - "What's Included" graphic (list all pages)
   - Lifestyle shot (planner in use)
   - Size reference (next to common object like notebook)
   - Before/after or feature highlight

**Option B: Use Placeit.net (paid, $29/month)**
- Has pre-made planner mockups
- Faster but requires subscription

**Option C: Take real photos**
1. Print one page from each planner
2. Style on a clean desk with coffee, pen, laptop
3. Take photos with good lighting
4. Edit in Canva (crop, adjust brightness)

**Output:** 21 images total (7 per planner), saved as JPG, 2000×2000px minimum

Save in `projects/etsy-productivity-planners/photos/`

---

### STEP 4: Upload Listings to Etsy (30 minutes)

For EACH of the 3 planners:

1. Go to your Etsy shop dashboard → Listings → Add a listing
2. Upload the 7 mockup photos
3. Copy-paste from the listing files:
   - `listings/adhd-task-starter-listing.md`
   - `listings/phd-dissertation-tracker-listing.md`
   - `listings/freelance-client-dashboard-listing.md`
4. Fill in:
   - **Title:** (from listing file, 140 char max)
   - **Description:** (from listing file, full text)
   - **Price:** (from listing file)
   - **Tags:** (all 13 tags from listing file)
   - **Category:** Art & Collectibles > Prints > Digital Prints
   - **Type:** Digital file
   - **File upload:** Upload the corresponding PDF
5. Publish listing

**Cost:** $0.20 per listing × 3 = $0.60 upfront

---

### STEP 5: Turn On Etsy Ads (5 minutes)

1. Go to Marketing → Etsy Ads
2. Set daily budget:
   - ADHD planner: $2.00/day
   - PhD planner: $1.50/day
   - Freelance planner: $2.00/day
   - **Total:** $5.50/day (~$165/month max)
3. Click "Turn on Etsy Ads"

**Why:** Organic Etsy search takes weeks. Ads get you in front of buyers on day 1.

---

### STEP 6: Set Up Revenue Tracking (5 minutes)

Every week when Etsy pays out:

1. Check your Etsy Payment Account (Shop Manager → Finances → Payment Account)
2. Note the payout amount
3. Append to `projects/etsy-productivity-planners/revenue-manual.json`:

```json
[
  {"date": "2026-05-05", "revenue_usd": 27.50, "notes": "Etsy payout — 3 planner sales this week"},
  {"date": "2026-05-12", "revenue_usd": 19.99, "notes": "Etsy payout — 2 sales (1 ADHD, 1 Freelance)"}
]
```

**Important:** Only log the NET revenue after Etsy fees (what actually hits your bank).

---

## Timeline

| Day | Action | Time Required |
|-----|--------|---------------|
| Day 1 | Set up Etsy account | 30 min |
| Day 1-2 | Create 3 planner PDFs | 2-3 hours |
| Day 2-3 | Create 21 mockup photos | 1-2 hours |
| Day 3 | Upload 3 listings | 30 min |
| Day 3 | Turn on Etsy Ads | 5 min |
| Day 4+ | Monitor sales, update revenue-manual.json weekly | 5 min/week |

**Goal:** First sale within 7–10 days of listings going live.

---

## What Happens Next

Once listings are live:
- The agent will monitor Etsy search analytics weekly
- The agent will A/B test titles, tags, and pricing based on data
- The agent will design additional planners if one niche outperforms
- You will handle customer service (rare — digital downloads are automatic)
- You will log revenue weekly in `revenue-manual.json`

---

## Questions or Blockers?

If you hit any issues:
1. Check Etsy Seller Handbook: https://help.etsy.com/hc/en-us/categories/360003406034-Selling-on-Etsy
2. Reply in this file with your question — I'll read it next session
3. If urgent, leave a note in `projects/etsy-productivity-planners/inbox.md`

---

**Bottom line:** You're ~4 hours of work away from having 3 live Etsy listings that can start earning. Let's get to first dollar this week.
