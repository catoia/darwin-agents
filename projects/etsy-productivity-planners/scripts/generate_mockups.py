#!/usr/bin/env python3
"""
Generate professional mockup images for Etsy listings
Creates 7 mockup variations per planner (21 total images)
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from pdf2image import convert_from_path
import os

def extract_pdf_page(pdf_path, page_num=1):
    """Extract a specific page from PDF as PIL Image"""
    pages = convert_from_path(pdf_path, first_page=page_num, last_page=page_num, dpi=150)
    return pages[0] if pages else None

def create_mockup_hero(planner_page, desk_bg, output_path, title_text):
    """Hero shot: planner page on desk with title overlay"""
    # Resize desk background to 2000x2000
    desk = desk_bg.resize((2000, 2000), Image.Resampling.LANCZOS)
    
    # Resize planner page and convert to RGBA
    planner_w = 800
    planner_h = int(planner_page.height * (planner_w / planner_page.width))
    planner = planner_page.resize((planner_w, planner_h), Image.Resampling.LANCZOS).convert('RGBA')
    
    # Add shadow effect
    shadow = Image.new('RGBA', (planner_w + 20, planner_h + 20), (0, 0, 0, 80))
    shadow = shadow.filter(ImageFilter.GaussianBlur(15))
    
    # Position planner on desk (center-right)
    desk = desk.convert('RGBA')
    shadow_pos = (600, 400)
    planner_pos = (610, 410)
    
    desk.paste(shadow, shadow_pos, shadow)
    desk.paste(planner, planner_pos, planner)
    
    # Add text overlay
    draw = ImageDraw.Draw(desk)
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 70)
        font_sub = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 40)
    except:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
    
    # Semi-transparent text background
    text_bg = Image.new('RGBA', (2000, 300), (255, 255, 255, 200))
    desk.paste(text_bg, (0, 100), text_bg)
    
    # Draw title text
    draw.text((100, 150), title_text, fill=(30, 30, 30), font=font_title)
    draw.text((100, 240), "50+ Printable Pages • Instant Download", fill=(80, 80, 80), font=font_sub)
    
    # Convert back to RGB for JPEG
    final = desk.convert('RGB')
    final.save(output_path, 'JPEG', quality=95)
    print(f"  ✓ {os.path.basename(output_path)}")

def create_mockup_detail(planner_page, output_path, detail_area=(0.2, 0.3, 0.8, 0.7)):
    """Detail shot: zoomed in on specific section"""
    # Crop to detail area
    w, h = planner_page.size
    left, top, right, bottom = detail_area
    crop_box = (int(w * left), int(h * top), int(w * right), int(h * bottom))
    detail = planner_page.crop(crop_box)
    
    # Resize to 2000x2000
    detail = detail.resize((2000, 2000), Image.Resampling.LANCZOS)
    
    # Enhance contrast slightly
    enhancer = ImageEnhance.Contrast(detail)
    detail = enhancer.enhance(1.1)
    
    detail.save(output_path, 'JPEG', quality=95)
    print(f"  ✓ {os.path.basename(output_path)}")

def create_mockup_lifestyle(planner_page, desk_bg, output_path):
    """Lifestyle shot: planner + coffee + pen composition"""
    desk = desk_bg.resize((2000, 2000), Image.Resampling.LANCZOS)
    
    # Smaller planner size for lifestyle feel
    planner_w = 600
    planner_h = int(planner_page.height * (planner_w / planner_page.width))
    planner = planner_page.resize((planner_w, planner_h), Image.Resampling.LANCZOS).convert('RGBA')
    
    # Add shadow
    shadow = Image.new('RGBA', (planner_w + 20, planner_h + 20), (0, 0, 0, 60))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    
    # Position off-center
    desk = desk.convert('RGBA')
    shadow_pos = (200, 600)
    planner_pos = (210, 610)
    
    desk.paste(shadow, shadow_pos, shadow)
    desk.paste(planner, planner_pos, planner)
    
    final = desk.convert('RGB')
    final.save(output_path, 'JPEG', quality=95)
    print(f"  ✓ {os.path.basename(output_path)}")

def create_mockup_whats_included(planner_page, output_path, page_count, features):
    """What's included graphic with text and sample page"""
    # White background
    canvas = Image.new('RGB', (2000, 2000), (255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    
    try:
        font_title = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 80)
        font_body = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 50)
    except:
        font_title = ImageFont.load_default()
        font_body = ImageFont.load_default()
    
    # Title
    draw.text((100, 100), "What's Included:", fill=(30, 30, 30), font=font_title)
    
    # Feature list
    y = 250
    draw.text((100, y), f"✓ {page_count} Printable Pages", fill=(60, 60, 60), font=font_body)
    y += 100
    draw.text((100, y), "✓ Instant PDF Download", fill=(60, 60, 60), font=font_body)
    y += 100
    draw.text((100, y), "✓ US Letter Size (8.5\" x 11\")", fill=(60, 60, 60), font=font_body)
    y += 100
    for feature in features[:2]:
        draw.text((100, y), f"✓ {feature}", fill=(60, 60, 60), font=font_body)
        y += 100
    
    # Small sample page thumbnail
    planner_w = 600
    planner_h = int(planner_page.height * (planner_w / planner_page.width))
    planner = planner_page.resize((planner_w, planner_h), Image.Resampling.LANCZOS).convert('RGB')
    canvas.paste(planner, (1300, 400))
    
    canvas.save(output_path, 'JPEG', quality=95)
    print(f"  ✓ {os.path.basename(output_path)}")

def create_mockup_simple(planner_page, output_path):
    """Simple clean mockup: just the page on white background with shadow"""
    # White background
    canvas = Image.new('RGB', (2000, 2000), (255, 255, 255))
    
    # Resize planner page and convert to RGB
    planner_w = 1200
    planner_h = int(planner_page.height * (planner_w / planner_page.width))
    planner = planner_page.resize((planner_w, planner_h), Image.Resampling.LANCZOS).convert('RGB')
    
    # Center on canvas (no shadow for simplicity)
    planner_x = (2000 - planner_w) // 2
    planner_y = (2000 - planner_h) // 2
    
    canvas.paste(planner, (planner_x, planner_y))
    
    canvas.save(output_path, 'JPEG', quality=95)
    print(f"  ✓ {os.path.basename(output_path)}")

def generate_mockups_for_planner(pdf_path, desk_images, output_prefix, title_text, page_count, features):
    """Generate 7 mockup variations for one planner"""
    print(f"\nGenerating mockups for: {title_text}")
    
    # Extract first page from PDF
    planner_page = extract_pdf_page(pdf_path, page_num=2)  # Page 2 (skip title page)
    if not planner_page:
        print(f"  ✗ Failed to extract page from {pdf_path}")
        return
    
    output_dir = "../photos"
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Hero shot
    create_mockup_hero(planner_page, desk_images[0], 
                      f"{output_dir}/{output_prefix}-mockup-1-hero.jpg", title_text)
    
    # 2. Detail shot (top section)
    create_mockup_detail(planner_page, 
                        f"{output_dir}/{output_prefix}-mockup-2-detail-top.jpg",
                        detail_area=(0.1, 0.1, 0.9, 0.4))
    
    # 3. Detail shot (middle section)
    create_mockup_detail(planner_page, 
                        f"{output_dir}/{output_prefix}-mockup-3-detail-mid.jpg",
                        detail_area=(0.1, 0.35, 0.9, 0.65))
    
    # 4. Lifestyle shot
    create_mockup_lifestyle(planner_page, desk_images[1], 
                           f"{output_dir}/{output_prefix}-mockup-4-lifestyle.jpg")
    
    # 5. What's included
    create_mockup_whats_included(planner_page, 
                                f"{output_dir}/{output_prefix}-mockup-5-whats-included.jpg",
                                page_count, features)
    
    # 6. Simple clean shot
    create_mockup_simple(planner_page, 
                        f"{output_dir}/{output_prefix}-mockup-6-simple.jpg")
    
    # 7. Full page view on desk
    create_mockup_hero(planner_page, desk_images[2], 
                      f"{output_dir}/{output_prefix}-mockup-7-full-page.jpg", 
                      f"{title_text} - Printable PDF")

def main():
    """Generate all mockups for all three planners"""
    # Load desk backgrounds
    print("Loading desk backgrounds...")
    stock_dir = "../stock-photos"
    desk_images = [
        Image.open(f"{stock_dir}/desk-1.jpg"),
        Image.open(f"{stock_dir}/desk-2.jpg"),
        Image.open(f"{stock_dir}/desk-3.jpg")
    ]
    
    # ADHD Planner
    generate_mockups_for_planner(
        pdf_path="../products/ADHD-Task-Starter-Planner-50-Printable-Sheets.pdf",
        desk_images=desk_images,
        output_prefix="adhd",
        title_text="ADHD Task Starter",
        page_count="50",
        features=["Daily task breakdown pages", "Weekly overview trackers"]
    )
    
    # PhD Planner
    generate_mockups_for_planner(
        pdf_path="../products/PhD-Dissertation-Progress-Tracker-60-Printable-Pages.pdf",
        desk_images=desk_images,
        output_prefix="phd",
        title_text="PhD Dissertation Tracker",
        page_count="60",
        features=["Chapter planning sheets", "Literature review tracker"]
    )
    
    # Freelance Planner
    generate_mockups_for_planner(
        pdf_path="../products/Freelance-Client-Project-Dashboard-55-Printable-Pages.pdf",
        desk_images=desk_images,
        output_prefix="freelance",
        title_text="Freelance Project Dashboard",
        page_count="55",
        features=["Client intake forms", "Invoice tracker"]
    )
    
    print("\n✓ All mockups generated successfully!")
    print("  Total: 21 images (7 per planner)")
    print(f"  Location: ../photos/")

if __name__ == "__main__":
    main()
