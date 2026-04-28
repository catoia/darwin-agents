# Strategy: Etsy Productivity Planners (AUTOMATION-FIRST)

## The Opportunity
Etsy has a huge market for printable planners — daily, weekly, monthly, goal trackers, habit trackers, etc. Most listings are generic templates. There's an opportunity for **niche-specific productivity planners** targeting underserved personas: ADHD-friendly planners, PhD student research planners, freelancer project trackers, etc.

The key differentiator: **targeting a specific pain point with a specific solution**, not "2026 daily planner."

## Monetization Path
1. **Digital downloads** — $7–$12 per planner PDF sold on Etsy
2. **Planner bundles** — $25 for a 3-pack targeting one niche (e.g., "ADHD productivity bundle")
3. **Custom commissions** — once traffic is proven, offer custom planner design at $50/request

---

## AUTOMATION-FIRST APPROACH

The goal is to minimize human manual labor and maximize what code can do. The agent generates everything programmatically, and the human only handles what requires a real human (Etsy account creation, legal agreements, payment setup).

### What Gets Automated (Agent Does Programmatically)

#### 1. PDF Generation (100% Automated)
**Technology stack:**
- **reportlab** (Python) — for precise layout control, drawing lines, text placement, tables
- **weasyprint** (Python) — HTML/CSS → PDF, best for complex layouts with web-like styling
- **fpdf2** (Python) — simpler alternative to reportlab for basic layouts
- **LaTeX** (via `pdflatex`) — for highly structured documents, excellent typography

**Planner template pipeline:**
1. Agent writes Python script using reportlab or weasyprint
2. Script reads design spec (dimensions, colors, fonts, layout grid)
3. Script generates multi-page PDF with all planner pages
4. Output: `products/ADHD-Task-Starter-Planner-50-Printable-Sheets.pdf`

**Example:** For a 50-page weekly planner:
```python
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def generate_adhd_planner():
    c = canvas.Canvas("ADHD-Task-Starter-Planner.pdf", pagesize=letter)
    for week in range(1, 51):
        # Draw week header
        c.setFont("Helvetica-Bold", 16)
        c.drawString(1*inch, 10*inch, f"Week {week}")
        # Draw task grid
        for row in range(10):
            y = 9*inch - (row * 0.5*inch)
            c.line(1*inch, y, 7.5*inch, y)
        c.showPage()
    c.save()
```

**Benefits:**
- No Canva subscription needed
- Instant iteration — change colors, fonts, spacing in seconds
- Version control — all design is code, tracked in git
- Batch generation — create 10 planner variants in one script run
- No manual export/download/upload steps

#### 2. Mockup Image Generation (90% Automated)
**Technology stack:**
- **Pillow (PIL)** (Python) — image composition, overlays, text rendering
- **Mockup APIs:**
  - Smartmockups.com API — $19/month for 200 mockups, REST API
  - Placeit.net API — $29/month, 500 mockups
  - Canva API (beta) — programmatic mockup generation
- **Custom composition:** Agent creates desk scene mockups by layering:
  - Background image (stock photo: desk, coffee, laptop)
  - Planner page overlay (rendered at angle, with shadow)
  - Text annotations (arrows, callouts, feature highlights)

**Mockup generation pipeline:**
1. Agent extracts page 1 from generated PDF as PNG (using `pdf2image`)
2. Agent calls Smartmockups API or uses Pillow to composite:
   - Desk background + planner page overlay + shadow + perspective transform
3. Agent generates 7 variations per planner:
   - Hero shot (full page visible)
   - Detail shot (zoomed in on specific section)
   - Lifestyle shot (planner + coffee + pen)
   - "What's Included" graphic (auto-generated text layout)
   - Size comparison (planner next to standard notebook)
   - Before/after (empty vs filled-in example)
   - Feature highlight (callout arrows pointing to key features)
4. Output: 21 images total (7 per planner), 2000×2000px JPG

**Example Pillow mockup script:**
```python
from PIL import Image, ImageDraw, ImageFont
from pdf2image import convert_from_path

# Convert PDF page to image
pages = convert_from_path('planner.pdf', first_page=1, last_page=1)
planner_page = pages[0]

# Load desk background
desk = Image.open('desk-background.jpg')

# Resize and position planner on desk
planner_page = planner_page.resize((800, 1035))
desk.paste(planner_page, (300, 200), mask=None)

# Add shadow effect
draw = ImageDraw.Draw(desk)
draw.rectangle([(295, 195), (1105, 1240)], outline='black', width=5)

# Add text callout
font = ImageFont.truetype("arial.ttf", 40)
draw.text((100, 100), "50 Weekly Task Pages", fill='white', font=font)

desk.save('mockup-hero.jpg', quality=95)
```

**Benefits:**
- No manual photo editing
- Consistent style across all mockups
- Instant regeneration if design changes
- Batch process 100 mockups in minutes

#### 3. Etsy Listing Copy (100% Automated)
**Already done:** Agent writes SEO-optimized titles, descriptions, and tags.
- Stored in `listings/*.md` files
- Human copy-pastes into Etsy (30 seconds per listing)

**Future enhancement:**
- Etsy API (if available) for programmatic listing creation
- Currently Etsy Open API v3 does NOT support creating listings (only reading)
- Human must manually paste copy and upload files

#### 4. A/B Testing & Optimization (80% Automated)
**Etsy Analytics API:**
- Agent reads Etsy Stats API (views, favorites, cart adds per listing)
- Agent compares variant performance (e.g., "$9 ADHD Planner" vs "$12 ADHD Planner")
- Agent automatically generates new variants, swaps underperformers

**Manual step:** Human uploads new listing variants to Etsy (API limitation)

#### 5. Batch Variant Generation (100% Automated)
Once one planner design works, agent can spawn variants:
- **Color schemes:** Generate 5 color variants (pastel, dark mode, minimal, vibrant, corporate)
- **Page counts:** 25-page, 50-page, 100-page versions
- **Layouts:** Portrait vs landscape, half-page, full-page
- **Niches:** Clone "ADHD planner" structure for "Anxiety", "Autism", "Chronic Pain", etc.

**Script:** `scripts/generate-planner-variant.py --base adhd --niche anxiety --colors pastel`

Output: New PDF + 7 mockups + Etsy listing copy in 2 minutes.

---

### What Requires Human (Cannot Be Automated)

#### 1. Etsy Account Creation (One-time, 30 minutes)
**Why human:** Etsy requires:
- Legal name and address
- Bank account for payouts
- Tax ID (SSN or EIN)
- Agreement to Terms of Service (requires human signature)

**Agent provides:** Step-by-step checklist in `HUMAN-SETUP-INSTRUCTIONS.md`

**Human does:**
1. Go to etsy.com/sell
2. Create shop (choose name, set preferences)
3. Link bank account
4. Accept Terms of Service

**One-time cost:** $0 (account is free)

#### 2. Uploading Listings to Etsy (30 sec per listing)
**Why human:** Etsy Open API v3 does not support creating listings (read-only).

**Agent provides:**
- Ready-to-upload PDFs in `products/`
- Ready-to-upload mockup images in `photos/`
- Pre-written titles, descriptions, tags in `listings/*.md`

**Human does:**
1. Click "Add a listing" in Etsy dashboard
2. Upload 7 mockup images (drag-and-drop)
3. Copy-paste title, description, tags from listing file
4. Upload PDF file
5. Set price
6. Click "Publish"

**Time per listing:** 30 seconds (just copy-paste and upload)

**One-time cost per listing:** $0.20 USD

#### 3. Customer Service (Rare, 5 min per issue)
**Why human:** Etsy messages require human response.

**Agent provides:** Template responses for common questions in `customer-service-templates.md`

**Human handles:**
- Refund requests (rare for digital downloads)
- Custom planner requests (forward to agent for design, then upload)
- Technical issues (buyer can't download file)

**Expected volume:** <1 message per 20 sales (digital downloads are automatic)

#### 4. Revenue Tracking (5 min per week)
**Why human:** Etsy deposits money to bank account, not accessible via API for security.

**Agent provides:** `revenue-manual.json` format and instructions

**Human does:**
1. Check Etsy Payment Account weekly (Etsy pays out deposits weekly)
2. Append to `revenue-manual.json`:
```json
[{"date": "2026-05-05", "revenue_usd": 27.50, "notes": "Etsy payout — 3 planner sales this week"}]
```

**Time:** 2 minutes per week

---

## Implementation Priority

### Phase 1: Automated PDF Generation (Days 1–2)
**Goal:** Generate 3 production-ready planner PDFs programmatically.

**Tasks:**
1. Install Python dependencies: `pip install reportlab pdf2image pillow`
2. Write `scripts/generate-planner-pdf.py` with design logic
3. Run script to generate 3 PDFs:
   - `ADHD-Task-Starter-Planner-50-Printable-Sheets.pdf`
   - `PhD-Dissertation-Progress-Tracker-60-Printable-Pages.pdf`
   - `Freelance-Client-Project-Dashboard-55-Printable-Pages.pdf`
4. Visual QA: Open PDFs, verify layout, spacing, readability
5. Save to `products/`

**Output:** 3 print-ready PDFs, zero manual design work.

### Phase 2: Automated Mockup Generation (Days 2–3)
**Goal:** Generate 21 mockup images (7 per planner) using Pillow or mockup API.

**Tasks:**
1. Acquire stock desk background images (free from Unsplash or Pexels)
2. Write `scripts/generate-mockups.py`:
   - Extract page 1 from each PDF as PNG
   - Composite onto desk background
   - Add text callouts, shadows, perspective transform
   - Generate 7 variations per planner
3. Run script → 21 images in `photos/`
4. Visual QA: Check image quality, resolution (2000×2000px min)

**Output:** 21 professional mockup images, zero manual photo editing.

### Phase 3: Human Uploads to Etsy (Day 3)
**Goal:** 3 live Etsy listings.

**Tasks:**
1. Agent writes updated `HUMAN-SETUP-INSTRUCTIONS.md` with exact upload steps
2. Human creates Etsy account (30 min, one-time)
3. Human uploads 3 listings (90 seconds per listing, just copy-paste and upload)
4. Listings go live

**Output:** 3 live Etsy listings, ready to sell.

### Phase 4: Variant Generation & Scaling (Days 4+)
**Goal:** 10+ planner variants live within 2 weeks.

**Tasks:**
1. Agent monitors Etsy Stats API (which listing gets most views/favorites)
2. Agent generates 5 variants of winning design:
   - Different color schemes
   - Different niches (ADHD → Anxiety, Autism, etc.)
   - Different page counts (50-page → 100-page)
3. Agent provides new PDFs + mockups + listing copy to human
4. Human uploads new variants (30 sec each)
5. Repeat weekly based on data

**Output:** Compounding catalog growth, minimal human effort per variant.

---

## Current Status

**Cycle 0 — Bootstrap:**
- [x] Niche research completed (ADHD, PhD, Freelance)
- [x] Design specs written (3 planners)
- [x] Etsy listing copy written (titles, descriptions, tags)
- [ ] **NEXT:** Automate PDF generation (Phase 1)
- [ ] Automate mockup generation (Phase 2)
- [ ] Human uploads to Etsy (Phase 3)

**Cycle 1 — First Sale:**
- [ ] Turn on Etsy Ads ($5.50/day)
- [ ] Monitor daily: views, favorites, cart adds
- [ ] Optimize: tweak tags/titles based on data
- [ ] Target: First sale within 7 days of going live

**Cycle 2 — Scaling:**
- [ ] Identify winning planner (most sales)
- [ ] Generate 5 variants (automated)
- [ ] Human uploads variants
- [ ] Target: $50 revenue by end of week 2

---

## Revenue Target

**$150 in 5 weeks** — 15 planner sales at $10 average.

**Breakdown:**
- Week 1: $0 (setup, first listings go live)
- Week 2: $20 (2 sales — early testers)
- Week 3: $40 (4 sales — Etsy algorithm boosts listings with sales history)
- Week 4: $50 (5 sales — more variants live, ads optimized)
- Week 5: $40 (4 sales — steady state)

**Total:** $150

---

## Tools & Dependencies

**Python libraries:**
- `reportlab` — PDF generation with precise layout control
- `weasyprint` — HTML/CSS to PDF (alternative)
- `fpdf2` — simpler PDF generation
- `pillow` (PIL) — image manipulation, mockup compositing
- `pdf2image` — extract PDF pages as PNG for mockups

**APIs (optional):**
- Smartmockups.com API — $19/month for 200 mockups
- Placeit.net API — $29/month for 500 mockups
- Etsy Stats API — free, read-only (views, favorites per listing)

**Stock assets:**
- Unsplash.com — free stock photos (desk, coffee, workspace)
- Google Fonts — free typography for planner headers

**Human-required platforms:**
- Etsy seller account (free, but requires legal name, bank account, tax ID)

---

## Key Insight

**Manual design work does not scale.** If every new planner variant requires 2 hours of Canva work, we're bottlenecked. But if the agent can generate 10 planner PDFs and 70 mockup images in 5 minutes by running a script, we can test and iterate 100x faster.

**The goal:** Agent proposes a new niche ("Chronic Pain Weekly Tracker"), runs `python scripts/generate-planner-variant.py --niche chronic-pain`, produces PDF + mockups + listing copy, and hands off to human for 30-second Etsy upload. Rinse and repeat.

**The human becomes a low-friction upload gateway, not a bottleneck.**
