#!/usr/bin/env python3
"""
Generate ADHD Task Starter Planner PDF
50 pages: 30 daily task pages + 10 weekly overviews + 10 task decomposition worksheets
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Design constants
PAGE_WIDTH, PAGE_HEIGHT = letter
MARGIN = 0.5 * inch
TEAL = HexColor('#2DD4BF')
CORAL = HexColor('#FB7185')
GRAY = HexColor('#6B7280')
LIGHT_GRAY = HexColor('#E5E7EB')

def draw_header(c, title, page_num):
    """Draw page header with title and page number"""
    c.setFont("Helvetica-Bold", 14)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN, title)
    c.setFont("Helvetica", 10)
    c.setFillColor(GRAY)
    c.drawRightString(PAGE_WIDTH - MARGIN, PAGE_HEIGHT - MARGIN, f"Page {page_num}")
    c.setFillColor('black')
    # Draw line under header
    c.setStrokeColor(LIGHT_GRAY)
    c.setLineWidth(1)
    c.line(MARGIN, PAGE_HEIGHT - MARGIN - 0.15*inch, 
           PAGE_WIDTH - MARGIN, PAGE_HEIGHT - MARGIN - 0.15*inch)

def draw_checkbox(c, x, y, size=0.15*inch):
    """Draw an empty checkbox"""
    c.setStrokeColor('black')
    c.setLineWidth(1)
    c.rect(x, y, size, size)

def draw_circle(c, x, y, radius=0.08*inch):
    """Draw an empty circle"""
    c.setStrokeColor('black')
    c.setLineWidth(1)
    c.circle(x + radius, y + radius, radius, stroke=1, fill=0)

def draw_daily_task_page(c, day_num):
    """Generate a daily task starter page"""
    page_num = day_num
    
    # Header
    draw_header(c, "ADHD Task Starter", page_num)
    
    y = PAGE_HEIGHT - MARGIN - 0.4*inch
    
    # Date and Energy Level
    c.setFont("Helvetica", 11)
    c.drawString(MARGIN, y, "Date: _______________")
    c.drawString(MARGIN + 3*inch, y, "Energy Level:")
    
    # Energy circles
    energy_x = MARGIN + 4.8*inch
    draw_circle(c, energy_x, y - 0.05*inch)
    c.setFont("Helvetica", 9)
    c.drawString(energy_x + 0.25*inch, y, "Low")
    
    draw_circle(c, energy_x + 0.8*inch, y - 0.05*inch)
    c.drawString(energy_x + 1.05*inch, y, "Med")
    
    draw_circle(c, energy_x + 1.6*inch, y - 0.05*inch)
    c.drawString(energy_x + 1.85*inch, y, "High")
    
    y -= 0.4*inch
    
    # Priority Task Box
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, y, "TODAY'S PRIORITY TASK")
    c.setFillColor('black')
    
    y -= 0.15*inch
    
    # Draw box around priority section
    box_height = 2.5*inch
    c.setStrokeColor(TEAL)
    c.setLineWidth(2)
    c.rect(MARGIN, y - box_height, PAGE_WIDTH - 2*MARGIN, box_height)
    
    y -= 0.3*inch
    c.setFont("Helvetica", 11)
    c.drawString(MARGIN + 0.1*inch, y, "Task:")
    c.line(MARGIN + 0.6*inch, y - 0.05*inch, PAGE_WIDTH - MARGIN - 0.1*inch, y - 0.05*inch)
    
    y -= 0.35*inch
    c.drawString(MARGIN + 0.1*inch, y, "Why it matters:")
    c.line(MARGIN + 1.2*inch, y - 0.05*inch, PAGE_WIDTH - MARGIN - 0.1*inch, y - 0.05*inch)
    
    y -= 0.35*inch
    c.drawString(MARGIN + 0.1*inch, y, "First tiny step (5 min):")
    c.line(MARGIN + 1.8*inch, y - 0.05*inch, PAGE_WIDTH - MARGIN - 0.1*inch, y - 0.05*inch)
    
    y -= 0.5*inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN + 0.1*inch, y, "Next 3 micro-steps:")
    c.setFont("Helvetica", 11)
    
    for i in range(3):
        y -= 0.3*inch
        draw_checkbox(c, MARGIN + 0.2*inch, y - 0.02*inch, 0.12*inch)
        c.line(MARGIN + 0.5*inch, y, PAGE_WIDTH - MARGIN - 0.1*inch, y)
    
    y -= 0.6*inch
    
    # Hyperfocus Session Log
    c.setFillColor(CORAL)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, y, "HYPERFOCUS SESSION LOG")
    c.setFillColor('black')
    
    y -= 0.15*inch
    c.setStrokeColor(CORAL)
    c.setLineWidth(2)
    box_height2 = 1.2*inch
    c.rect(MARGIN, y - box_height2, PAGE_WIDTH - 2*MARGIN, box_height2)
    
    y -= 0.3*inch
    c.setFont("Helvetica", 10)
    c.drawString(MARGIN + 0.1*inch, y, "Started: ___:___   |   Ended: ___:___   |   Duration: ______")
    
    y -= 0.25*inch
    c.drawString(MARGIN + 0.1*inch, y, "What I accomplished:")
    c.line(MARGIN + 1.4*inch, y - 0.05*inch, PAGE_WIDTH - MARGIN - 0.1*inch, y - 0.05*inch)
    y -= 0.2*inch
    c.line(MARGIN + 0.1*inch, y, PAGE_WIDTH - MARGIN - 0.1*inch, y)
    
    y -= 0.3*inch
    c.drawString(MARGIN + 0.1*inch, y, "Dopamine reward earned:")
    draw_checkbox(c, MARGIN + 1.8*inch, y - 0.02*inch, 0.12*inch)
    c.drawString(MARGIN + 2.05*inch, y, "Yes")
    draw_checkbox(c, MARGIN + 2.6*inch, y - 0.02*inch, 0.12*inch)
    c.drawString(MARGIN + 2.85*inch, y, "Skipped")
    
    y -= 0.5*inch
    
    # Brain Dump
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, y, "BRAIN DUMP")
    c.setFont("Helvetica", 9)
    c.drawString(MARGIN + 1.2*inch, y + 0.05*inch, "(worries, distractions, ideas)")
    
    y -= 0.15*inch
    c.setStrokeColor(GRAY)
    c.setLineWidth(1)
    for i in range(3):
        y -= 0.25*inch
        c.line(MARGIN, y, PAGE_WIDTH - MARGIN, y)
    
    y -= 0.4*inch
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(TEAL)
    c.drawString(MARGIN, y, "WIN OF THE DAY")
    c.setFont("Helvetica", 9)
    c.setFillColor(GRAY)
    c.drawString(MARGIN + 1.3*inch, y + 0.05*inch, "(even if small)")
    c.setFillColor('black')
    
    y -= 0.15*inch
    c.setStrokeColor('black')
    c.setLineWidth(1)
    c.line(MARGIN, y, PAGE_WIDTH - MARGIN, y)

def draw_weekly_overview(c, week_num):
    """Generate a weekly overview page"""
    page_num = 30 + week_num
    
    draw_header(c, f"Weekly Overview — Week {week_num}", page_num)
    
    y = PAGE_HEIGHT - MARGIN - 0.5*inch
    
    # Week dates
    c.setFont("Helvetica", 11)
    c.drawString(MARGIN, y, "Week of: _______________")
    
    y -= 0.4*inch
    
    # Top 3 Non-Negotiables
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, y, "TOP 3 NON-NEGOTIABLES THIS WEEK")
    c.setFillColor('black')
    c.setFont("Helvetica", 11)
    
    for i in range(3):
        y -= 0.35*inch
        c.drawString(MARGIN, y, f"{i+1}.")
        c.line(MARGIN + 0.3*inch, y - 0.05*inch, PAGE_WIDTH - MARGIN, y - 0.05*inch)
    
    y -= 0.5*inch
    
    # 7-Day Energy Tracking
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, y, "ENERGY & PROGRESS TRACKER")
    c.setFont("Helvetica", 10)
    
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    y -= 0.3*inch
    
    for i, day in enumerate(days):
        y -= 0.4*inch
        c.drawString(MARGIN, y, f"{day}:")
        
        # Energy circles
        energy_x = MARGIN + 0.7*inch
        draw_circle(c, energy_x, y - 0.05*inch)
        c.setFont("Helvetica", 8)
        c.drawString(energy_x + 0.25*inch, y, "L")
        
        draw_circle(c, energy_x + 0.6*inch, y - 0.05*inch)
        c.drawString(energy_x + 0.85*inch, y, "M")
        
        draw_circle(c, energy_x + 1.2*inch, y - 0.05*inch)
        c.drawString(energy_x + 1.45*inch, y, "H")
        
        # Progress line
        c.setFont("Helvetica", 10)
        c.drawString(MARGIN + 2.5*inch, y, "Progress:")
        c.line(MARGIN + 3.3*inch, y - 0.05*inch, PAGE_WIDTH - MARGIN, y - 0.05*inch)
    
    y -= 0.5*inch
    
    # Procrastination Triggers
    c.setFillColor(CORAL)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, y, "PROCRASTINATION TRIGGERS TO WATCH FOR:")
    c.setFillColor('black')
    c.setFont("Helvetica", 10)
    
    for i in range(2):
        y -= 0.25*inch
        c.line(MARGIN, y, PAGE_WIDTH - MARGIN, y)
    
    y -= 0.4*inch
    
    # Weekly Reflection
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, y, "WEEKLY REFLECTION")
    c.setFillColor('black')
    c.setFont("Helvetica", 10)
    
    y -= 0.3*inch
    c.drawString(MARGIN, y, "What worked this week:")
    for i in range(2):
        y -= 0.2*inch
        c.line(MARGIN, y, PAGE_WIDTH - MARGIN, y)
    
    y -= 0.3*inch
    c.drawString(MARGIN, y, "What I'll try differently next week:")
    for i in range(2):
        y -= 0.2*inch
        c.line(MARGIN, y, PAGE_WIDTH - MARGIN, y)

def draw_task_decomposition(c, worksheet_num):
    """Generate a task decomposition worksheet"""
    page_num = 40 + worksheet_num
    
    draw_header(c, "Task Decomposition Worksheet", page_num)
    
    y = PAGE_HEIGHT - MARGIN - 0.5*inch
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, y, "OVERWHELMING TASK BREAKDOWN")
    
    y -= 0.3*inch
    c.setFont("Helvetica", 11)
    c.drawString(MARGIN, y, "Big scary task:")
    c.line(MARGIN + 1.2*inch, y - 0.05*inch, PAGE_WIDTH - MARGIN, y - 0.05*inch)
    
    y -= 0.25*inch
    c.line(MARGIN, y, PAGE_WIDTH - MARGIN, y)
    
    y -= 0.4*inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, y, "Break it into 10+ micro-steps:")
    c.setFont("Helvetica", 10)
    
    for i in range(15):
        y -= 0.3*inch
        c.drawString(MARGIN, y, f"{i+1}.")
        draw_checkbox(c, MARGIN + 0.3*inch, y - 0.02*inch, 0.12*inch)
        c.line(MARGIN + 0.55*inch, y - 0.05*inch, PAGE_WIDTH - MARGIN, y - 0.05*inch)
    
    y -= 0.4*inch
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(CORAL)
    c.drawString(MARGIN, y, "BLOCKERS & WORKAROUNDS:")
    c.setFillColor('black')
    c.setFont("Helvetica", 10)
    
    for i in range(3):
        y -= 0.25*inch
        c.line(MARGIN, y, PAGE_WIDTH - MARGIN, y)
    
    y -= 0.3*inch
    c.setFont("Helvetica-Bold", 10)
    c.drawString(MARGIN, y, "Accountability buddy:")
    c.setFont("Helvetica", 10)
    c.line(MARGIN + 1.5*inch, y - 0.05*inch, PAGE_WIDTH - MARGIN, y - 0.05*inch)

def generate_adhd_planner():
    """Generate complete ADHD Task Starter Planner PDF"""
    output_dir = "../products"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "ADHD-Task-Starter-Planner-50-Printable-Sheets.pdf")
    
    c = canvas.Canvas(output_file, pagesize=letter)
    
    # Title page
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 2*inch, "ADHD Task Starter Planner")
    c.setFont("Helvetica", 14)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 2.5*inch, "50 Printable Sheets")
    c.setFont("Helvetica", 11)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 3*inch, "Focus-friendly task management for busy ADHD brains")
    c.showPage()
    
    # Generate 30 daily task pages
    print("Generating 30 daily task pages...")
    for day in range(1, 31):
        draw_daily_task_page(c, day)
        c.showPage()
    
    # Generate 10 weekly overviews
    print("Generating 10 weekly overview pages...")
    for week in range(1, 11):
        draw_weekly_overview(c, week)
        c.showPage()
    
    # Generate 10 task decomposition worksheets
    print("Generating 10 task decomposition worksheets...")
    for ws in range(1, 11):
        draw_task_decomposition(c, ws)
        c.showPage()
    
    c.save()
    print(f"✓ Generated: {output_file}")
    print(f"  Total pages: 51 (1 title + 30 daily + 10 weekly + 10 decomposition)")
    return output_file

if __name__ == "__main__":
    generate_adhd_planner()
