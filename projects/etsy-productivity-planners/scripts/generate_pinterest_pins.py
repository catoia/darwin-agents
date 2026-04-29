#!/usr/bin/env python3
"""
Pinterest Pin Generator for Etsy Productivity Planners
Generates 21 Pinterest-optimized pins (1000×1500px) from existing mockups.

Usage: python3 scripts/generate_pinterest_pins.py
Output: pinterest-content/pin-*.jpg (21 files)
"""

import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

# ─────────────────────────────────────────────────────────────
# PALETTE
# ─────────────────────────────────────────────────────────────
COLORS = {
    "adhd": {
        "brand":    (100, 149, 237),   # cornflower blue
        "dark":     (30,  50,  100),   # dark navy
        "light":    (240, 245, 255),   # near white blue
        "accent":   (255, 200, 80),    # warm amber
        "text_on_dark": (255, 255, 255),
        "text_on_light": (30, 50, 100),
    },
    "phd": {
        "brand":    (72, 120, 168),    # academic blue
        "dark":     (20, 40,  80),     # oxford navy
        "light":    (245, 248, 255),
        "accent":   (200, 160, 80),    # gold
        "text_on_dark": (255, 255, 255),
        "text_on_light": (20, 40, 80),
    },
    "freelance": {
        "brand":    (60, 160, 120),    # professional green
        "dark":     (20, 60,  45),     # forest dark
        "light":    (240, 252, 247),
        "accent":   (255, 180, 50),    # amber
        "text_on_dark": (255, 255, 255),
        "text_on_light": (20, 60, 45),
    },
}

PIN_W, PIN_H = 1000, 1500

# ─────────────────────────────────────────────────────────────
# FONT HELPERS
# ─────────────────────────────────────────────────────────────
def get_font(size, bold=False):
    """Load a system font, falling back to default."""
    candidates_bold = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/liberation/LiberationSans-Bold.ttf",
    ]
    candidates_reg = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/liberation/LiberationSans-Regular.ttf",
    ]
    candidates = candidates_bold if bold else candidates_reg
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def draw_wrapped_text(draw, text, font, max_width, x, y, fill, align="left", line_spacing=8):
    """Draw text wrapped to max_width pixels. Returns final y position."""
    words = text.split()
    lines = []
    current = []
    for word in words:
        test_line = " ".join(current + [word])
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current.append(word)
        else:
            if current:
                lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))

    cur_y = y
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        line_w = bbox[2] - bbox[0]
        line_h = bbox[3] - bbox[1]
        if align == "center":
            draw.text((x - line_w // 2, cur_y), line, font=font, fill=fill)
        else:
            draw.text((x, cur_y), line, font=font, fill=fill)
        cur_y += line_h + line_spacing
    return cur_y


# ─────────────────────────────────────────────────────────────
# PIN BUILDER
# ─────────────────────────────────────────────────────────────
def build_pin(mockup_path, niche, variant, headline, subtext, cta, price_label, badge_text=None):
    """
    Build one 1000×1500 Pinterest pin.

    Layout (from top):
      [40px] top padding
      [brand band 80px]  → headline
      [mockup image ~700px]
      [text band ~400px]  → subtext + features + CTA
      [40px] bottom padding

    Returns: PIL Image
    """
    c = COLORS[niche]
    canvas = Image.new("RGB", (PIN_W, PIN_H), c["light"])
    draw = ImageDraw.Draw(canvas)

    # ── Top brand band ──────────────────────────────────────
    draw.rectangle([(0, 0), (PIN_W, 90)], fill=c["dark"])

    font_header_sm = get_font(22, bold=True)
    brand_names = {
        "adhd":      "ADHD & PRODUCTIVITY PLANNERS",
        "phd":       "PHD & ACADEMIC PLANNERS",
        "freelance": "FREELANCE & SOLOPRENEUR TOOLS",
    }
    brand_name = brand_names[niche]
    bbox = draw.textbbox((0, 0), brand_name, font=font_header_sm)
    bw = bbox[2] - bbox[0]
    draw.text(((PIN_W - bw) // 2, 30), brand_name, font=font_header_sm, fill=c["accent"])

    # ── Load and place mockup ────────────────────────────────
    try:
        mockup = Image.open(mockup_path).convert("RGB")
    except Exception:
        mockup = Image.new("RGB", (2000, 2000), (200, 200, 200))

    # Crop to a slightly taller ratio for visual impact, center-crop
    target_w = PIN_W - 40          # 20px margin each side
    target_h = int(target_w * 1.1) # slightly portrait crop of mockup
    mockup.thumbnail((target_w * 3, target_h * 3), Image.LANCZOS)
    mw, mh = mockup.size
    # Center crop
    left   = max(0, (mw - target_w) // 2)
    top_c  = max(0, (mh - target_h) // 2)
    right  = min(mw, left + target_w)
    bottom = min(mh, top_c + target_h)
    mockup = mockup.crop((left, top_c, right, bottom))
    mockup = mockup.resize((target_w, target_h), Image.LANCZOS)

    mockup_y = 100
    canvas.paste(mockup, (20, mockup_y))
    mockup_bottom = mockup_y + target_h

    # ── Subtle shadow below mockup ───────────────────────────
    for i in range(6):
        alpha = 60 - i * 10
        draw.line([(20, mockup_bottom + i), (PIN_W - 20, mockup_bottom + i)],
                  fill=(0, 0, 0, alpha) if False else (180, 180, 180))

    # ── Content band ─────────────────────────────────────────
    content_top = mockup_bottom + 20
    content_margin = 40
    content_width  = PIN_W - 2 * content_margin

    # Headline
    font_headline = get_font(38, bold=True)
    font_sub      = get_font(24, bold=False)
    font_cta      = get_font(26, bold=True)
    font_price    = get_font(22, bold=True)
    font_badge    = get_font(20, bold=True)

    # Accent divider
    draw.rectangle([(content_margin, content_top), (content_margin + 60, content_top + 5)],
                   fill=c["brand"])
    headline_y = content_top + 18

    final_y = draw_wrapped_text(draw, headline, font_headline,
                                 content_width, content_margin,
                                 headline_y, fill=c["text_on_light"],
                                 align="left", line_spacing=6)

    final_y += 12
    final_y = draw_wrapped_text(draw, subtext, font_sub,
                                 content_width, content_margin,
                                 final_y, fill=(80, 80, 80),
                                 align="left", line_spacing=5)

    # Price label
    final_y += 16
    draw.text((content_margin, final_y), price_label, font=font_price,
              fill=c["brand"])
    price_bbox = draw.textbbox((content_margin, final_y), price_label, font=font_price)
    price_h = price_bbox[3] - price_bbox[1]
    final_y += price_h + 14

    # CTA pill button
    cta_text = f"  {cta}  "
    cta_bbox = draw.textbbox((0, 0), cta_text, font=font_cta)
    cta_w = cta_bbox[2] - cta_bbox[0] + 24
    cta_h = cta_bbox[3] - cta_bbox[1] + 16
    cta_x = content_margin
    cta_y = final_y
    # Clamp to canvas
    if cta_y + cta_h + 30 > PIN_H:
        cta_y = PIN_H - cta_h - 30
    draw.rounded_rectangle(
        [(cta_x, cta_y), (cta_x + cta_w, cta_y + cta_h)],
        radius=10, fill=c["brand"]
    )
    draw.text((cta_x + 12, cta_y + 8), cta, font=font_cta,
              fill=c["text_on_dark"])

    # ── Optional badge (top-right of mockup) ─────────────────
    if badge_text:
        bx, by = PIN_W - 20 - 130, mockup_y + 10
        draw.rounded_rectangle([(bx, by), (bx + 130, by + 40)],
                                 radius=8, fill=c["accent"])
        bb = draw.textbbox((0, 0), badge_text, font=font_badge)
        bw_ = bb[2] - bb[0]
        draw.text((bx + (130 - bw_) // 2, by + 8), badge_text,
                  font=font_badge, fill=c["dark"])

    # ── Bottom strip ─────────────────────────────────────────
    draw.rectangle([(0, PIN_H - 45), (PIN_W, PIN_H)], fill=c["dark"])
    footer_font = get_font(18, bold=False)
    footer_text = "Find on Etsy  →  link in bio"
    fb = draw.textbbox((0, 0), footer_text, font=footer_font)
    fw = fb[2] - fb[0]
    draw.text(((PIN_W - fw) // 2, PIN_H - 32), footer_text,
              font=footer_font, fill=c["accent"])

    return canvas


# ─────────────────────────────────────────────────────────────
# PIN DEFINITIONS  (21 pins: 7 per niche)
# ─────────────────────────────────────────────────────────────
PINS = [
    # ── ADHD (7 pins) ──────────────────────────────────────────
    {
        "filename": "pin-adhd-01-hook.jpg",
        "mockup":   "photos/adhd-mockup-1-hero.jpg",
        "niche":    "adhd",
        "headline": "ADHD Task Starter Planner",
        "subtext":  "Break overwhelming tasks into 5-minute starter steps. Built for executive dysfunction.",
        "cta":      "Instant Download on Etsy →",
        "price":    "€9.99 | 50 Printable Pages",
        "badge":    "NEW",
    },
    {
        "filename": "pin-adhd-02-features.jpg",
        "mockup":   "photos/adhd-mockup-2-detail-top.jpg",
        "niche":    "adhd",
        "headline": "Finally: A Planner That Works for ADHD",
        "subtext":  "Energy tracking · Hyperfocus logs · Brain dump space · Task decomposition · No guilt.",
        "cta":      "Download Instantly →",
        "price":    "€9.99 | Instant PDF Download",
        "badge":    None,
    },
    {
        "filename": "pin-adhd-03-lifestyle.jpg",
        "mockup":   "photos/adhd-mockup-4-lifestyle.jpg",
        "niche":    "adhd",
        "headline": "Stop Starting Over. Start Small Instead.",
        "subtext":  "The ADHD planner that turns 'I can't start' into 'I just need 5 minutes'.",
        "cta":      "Shop on Etsy →",
        "price":    "€9.99 | Print Forever",
        "badge":    None,
    },
    {
        "filename": "pin-adhd-04-whats-inside.jpg",
        "mockup":   "photos/adhd-mockup-5-whats-included.jpg",
        "niche":    "adhd",
        "headline": "What's Inside: 50 ADHD-Specific Pages",
        "subtext":  "30 daily task starters + 10 weekly spreads + 10 task decomposition worksheets.",
        "cta":      "Get Yours on Etsy →",
        "price":    "€9.99 | Instant Download",
        "badge":    "50 PAGES",
    },
    {
        "filename": "pin-adhd-05-detail.jpg",
        "mockup":   "photos/adhd-mockup-3-detail-mid.jpg",
        "niche":    "adhd",
        "headline": "Task Decomposition for ADHD Adults",
        "subtext":  "Big scary task → 5 micro-steps → first action takes under 2 minutes. Executive dysfunction solved.",
        "cta":      "Try It Now →",
        "price":    "€9.99 | Printable PDF",
        "badge":    None,
    },
    {
        "filename": "pin-adhd-06-value.jpg",
        "mockup":   "photos/adhd-mockup-6-simple.jpg",
        "niche":    "adhd",
        "headline": "ADHD Daily Planner Printable",
        "subtext":  "Designed with ADHD adults, not just for them. Energy-matched tasks, no perfection pressure.",
        "cta":      "Download on Etsy →",
        "price":    "€9.99 | Print Unlimited Copies",
        "badge":    None,
    },
    {
        "filename": "pin-adhd-07-cta.jpg",
        "mockup":   "photos/adhd-mockup-7-full-page.jpg",
        "niche":    "adhd",
        "headline": "Neurodivergent? This Planner Gets It.",
        "subtext":  "Not another planner that assumes you're neurotypical. Built for brains that work differently.",
        "cta":      "Instant Download →",
        "price":    "€9.99 | 50 Printable Pages",
        "badge":    None,
    },

    # ── PhD (7 pins) ────────────────────────────────────────────
    {
        "filename": "pin-phd-01-hook.jpg",
        "mockup":   "photos/phd-mockup-1-hero.jpg",
        "niche":    "phd",
        "headline": "PhD Dissertation Progress Tracker",
        "subtext":  "Track chapters, literature, advisor meetings, and defense prep in one organized system.",
        "cta":      "Instant Download on Etsy →",
        "price":    "€11.99 | 60 Printable Pages",
        "badge":    "NEW",
    },
    {
        "filename": "pin-phd-02-features.jpg",
        "mockup":   "photos/phd-mockup-2-detail-top.jpg",
        "niche":    "phd",
        "headline": "The Planner Built for Dissertation Writing",
        "subtext":  "Chapter tracker · 80-source lit review · Advisor meeting prep · Defense checklist.",
        "cta":      "Download Instantly →",
        "price":    "€11.99 | Instant PDF Download",
        "badge":    None,
    },
    {
        "filename": "pin-phd-03-lifestyle.jpg",
        "mockup":   "photos/phd-mockup-4-lifestyle.jpg",
        "niche":    "phd",
        "headline": "Survive Dissertation Season. Stay Organized.",
        "subtext":  "Built for PhD students who need to manage 5 chapters, 80+ sources, and one demanding advisor.",
        "cta":      "Shop on Etsy →",
        "price":    "€11.99 | Print Forever",
        "badge":    None,
    },
    {
        "filename": "pin-phd-04-whats-inside.jpg",
        "mockup":   "photos/phd-mockup-5-whats-included.jpg",
        "niche":    "phd",
        "headline": "What's Inside: 60 Pages of Academic Tools",
        "subtext":  "1 overview + 18 chapter sheets + 20 lit review pages + 12 advisor sheets + defense checklists.",
        "cta":      "Get Yours on Etsy →",
        "price":    "€11.99 | Instant Download",
        "badge":    "60 PAGES",
    },
    {
        "filename": "pin-phd-05-detail.jpg",
        "mockup":   "photos/phd-mockup-3-detail-mid.jpg",
        "niche":    "phd",
        "headline": "Literature Review Tracker for PhD Students",
        "subtext":  "Manage 80+ sources without chaos. Citation notes, methodology tags, relevance ratings. All in one page.",
        "cta":      "Try It Now →",
        "price":    "€11.99 | Printable PDF",
        "badge":    None,
    },
    {
        "filename": "pin-phd-06-value.jpg",
        "mockup":   "photos/phd-mockup-6-simple.jpg",
        "niche":    "phd",
        "headline": "PhD Dissertation Planner Printable",
        "subtext":  "Created by someone who survived the dissertation process and wished this existed sooner.",
        "cta":      "Download on Etsy →",
        "price":    "€11.99 | 60 Printable Pages",
        "badge":    None,
    },
    {
        "filename": "pin-phd-07-cta.jpg",
        "mockup":   "photos/phd-mockup-7-full-page.jpg",
        "niche":    "phd",
        "headline": "A Perfect Gift for a PhD Student",
        "subtext":  "Know a grad student drowning in dissertation chaos? This printable planner is the gift they actually need.",
        "cta":      "Instant Download →",
        "price":    "€11.99 | 60 Printable Pages",
        "badge":    "GIFT IDEA",
    },

    # ── Freelance (7 pins) ──────────────────────────────────────
    {
        "filename": "pin-freelance-01-hook.jpg",
        "mockup":   "photos/freelance-mockup-1-hero.jpg",
        "niche":    "freelance",
        "headline": "Freelance Client Tracker Printable",
        "subtext":  "Manage 10+ projects without the chaos. Track invoices, scope creep, and deadlines in one dashboard.",
        "cta":      "Instant Download on Etsy →",
        "price":    "€10.99 | 55 Printable Pages",
        "badge":    "NEW",
    },
    {
        "filename": "pin-freelance-02-features.jpg",
        "mockup":   "photos/freelance-mockup-2-detail-top.jpg",
        "niche":    "freelance",
        "headline": "The Organized Freelancer Earns More",
        "subtext":  "Client intake forms · Scope creep log · Invoice tracker · Project milestones · Testimonial templates.",
        "cta":      "Download Instantly →",
        "price":    "€10.99 | Instant PDF Download",
        "badge":    None,
    },
    {
        "filename": "pin-freelance-03-lifestyle.jpg",
        "mockup":   "photos/freelance-mockup-4-lifestyle.jpg",
        "niche":    "freelance",
        "headline": "Get Paid On Time. Every Time.",
        "subtext":  "Never chase an invoice again. Track status, follow-up dates, and outstanding balances for every client.",
        "cta":      "Shop on Etsy →",
        "price":    "€10.99 | Print Forever",
        "badge":    None,
    },
    {
        "filename": "pin-freelance-04-whats-inside.jpg",
        "mockup":   "photos/freelance-mockup-5-whats-included.jpg",
        "niche":    "freelance",
        "headline": "What's Inside: 55 Pages for Solopreneurs",
        "subtext":  "2 client lists + 15 intake forms + 15 project trackers + 10 invoice sheets + 10 weekly dashboards.",
        "cta":      "Get Yours on Etsy →",
        "price":    "€10.99 | Instant Download",
        "badge":    "55 PAGES",
    },
    {
        "filename": "pin-freelance-05-detail.jpg",
        "mockup":   "photos/freelance-mockup-3-detail-mid.jpg",
        "niche":    "freelance",
        "headline": "Scope Creep Protection Log",
        "subtext":  "Document every out-of-scope request in real time. Charge for extras confidently. Protect your rates.",
        "cta":      "Try It Now →",
        "price":    "€10.99 | Printable PDF",
        "badge":    None,
    },
    {
        "filename": "pin-freelance-06-value.jpg",
        "mockup":   "photos/freelance-mockup-6-simple.jpg",
        "niche":    "freelance",
        "headline": "Freelance Dashboard Printable",
        "subtext":  "Built by a freelancer who got tired of losing invoices. One system for all your clients and projects.",
        "cta":      "Download on Etsy →",
        "price":    "€10.99 | 55 Printable Pages",
        "badge":    None,
    },
    {
        "filename": "pin-freelance-07-cta.jpg",
        "mockup":   "photos/freelance-mockup-7-full-page.jpg",
        "niche":    "freelance",
        "headline": "From Chaos to Client System",
        "subtext":  "Managing 5+ clients from a notebook isn't sustainable. Start with a real system today.",
        "cta":      "Instant Download →",
        "price":    "€10.99 | 55 Printable Pages",
        "badge":    None,
    },
]


# ─────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────
def main():
    out_dir = "pinterest-content"
    os.makedirs(out_dir, exist_ok=True)

    print(f"Generating {len(PINS)} Pinterest pins → {out_dir}/")
    ok = 0
    for i, p in enumerate(PINS, 1):
        outpath = os.path.join(out_dir, p["filename"])
        try:
            img = build_pin(
                mockup_path = p["mockup"],
                niche       = p["niche"],
                variant     = p["filename"],
                headline    = p["headline"],
                subtext     = p["subtext"],
                cta         = p["cta"],
                price_label = p["price"],
                badge_text  = p.get("badge"),
            )
            img.save(outpath, "JPEG", quality=92, optimize=True)
            print(f"  [{i:02d}/21] ✅  {p['filename']} ({img.size[0]}×{img.size[1]})")
            ok += 1
        except Exception as e:
            print(f"  [{i:02d}/21] ❌  {p['filename']} — ERROR: {e}")

    print(f"\nDone: {ok}/{len(PINS)} pins generated in {out_dir}/")


if __name__ == "__main__":
    main()
