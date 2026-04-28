#!/usr/bin/env python3
"""
Generate PhD Dissertation Progress Tracker PDF
60 pages: dissertation dashboard + chapter planning + literature + advisor meetings
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import os

PAGE_WIDTH, PAGE_HEIGHT = letter
MARGIN = 0.5 * inch
ACADEMIC_BLUE = HexColor('#3B82F6')
GRAY = HexColor('#6B7280')
LIGHT_GRAY = HexColor('#E5E7EB')

def draw_header(c, title, page_num):
    c.setFont("Helvetica-Bold", 14)
    c.drawString(MARGIN, PAGE_HEIGHT - MARGIN, title)
    c.setFont("Helvetica", 10)
    c.setFillColor(GRAY)
    c.drawRightString(PAGE_WIDTH - MARGIN, PAGE_HEIGHT - MARGIN, f"Page {page_num}")
    c.setFillColor('black')
    c.setStrokeColor(LIGHT_GRAY)
    c.setLineWidth(1)
    c.line(MARGIN, PAGE_HEIGHT - MARGIN - 0.15*inch, 
           PAGE_WIDTH - MARGIN, PAGE_HEIGHT - MARGIN - 0.15*inch)

def draw_checkbox(c, x, y, size=0.12*inch):
    c.setStrokeColor('black')
    c.setLineWidth(1)
    c.rect(x, y, size, size)

def draw_dissertation_overview(c):
    """Generate dissertation overview dashboard"""
    draw_header(c, "Dissertation Progress Dashboard", 1)
    
    y = PAGE_HEIGHT - MARGIN - 0.5*inch
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, y, "DISSERTATION TITLE:")
    y -= 0.2*inch
    c.setFont("Helvetica", 11)
    c.line(MARGIN, y, PAGE_WIDTH - MARGIN, y)
    y -= 0.15*inch
    c.line(MARGIN, y, PAGE_WIDTH - MARGIN, y)
    
    y -= 0.4*inch
    c.setFont("Helvetica", 11)
    c.drawString(MARGIN, y, "Committee Chair:")
    c.line(MARGIN + 1.3*inch, y - 0.05*inch, MARGIN + 4*inch, y - 0.05*inch)
    c.drawString(MARGIN + 4.5*inch, y, "Next meeting:")
    c.line(MARGIN + 5.5*inch, y - 0.05*inch, PAGE_WIDTH - MARGIN, y - 0.05*inch)
    
    y -= 0.5*inch
    c.setFillColor(ACADEMIC_BLUE)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, y, "CHAPTER PROGRESS TRACKER")
    c.setFillColor('black')
    
    chapters = [
        "Ch 1 - Introduction",
        "Ch 2 - Literature Review",
        "Ch 3 - Methodology",
        "Ch 4 - Results",
        "Ch 5 - Discussion",
        "Ch 6 - Conclusion"
    ]
    
    c.setFont("Helvetica", 11)
    for ch in chapters:
        y -= 0.35*inch
        c.drawString(MARGIN, y, ch)
        # Progress bar
        bar_x = MARGIN + 3*inch
        bar_width = 2.5*inch
        c.rect(bar_x, y - 0.1*inch, bar_width, 0.15*inch)
        c.drawString(bar_x + bar_width + 0.2*inch, y, "____%")
    
    y -= 0.5*inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, y, "DEFENSE COUNTDOWN:")
    c.setFont("Helvetica", 11)
    c.drawString(MARGIN + 1.8*inch, y, "_______ days remaining")
    
    y -= 0.3*inch
    c.drawString(MARGIN, y, "Target defense date:")
    c.line(MARGIN + 1.8*inch, y - 0.05*inch, PAGE_WIDTH - MARGIN, y - 0.05*inch)

def draw_chapter_planning(c, chapter_num, page_num):
    """Generate chapter planning sheet"""
    draw_header(c, f"Chapter {chapter_num} Planning", page_num)
    
    y = PAGE_HEIGHT - MARGIN - 0.5*inch
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, y, f"CHAPTER {chapter_num}:")
    c.setFont("Helvetica", 11)
    c.line(MARGIN + 1.2*inch, y - 0.05*inch, PAGE_WIDTH - MARGIN, y - 0.05*inch)
    
    y -= 0.4*inch
    c.drawString(MARGIN, y, "Target completion:")
    c.line(MARGIN + 1.6*inch, y - 0.05*inch, MARGIN + 4*inch, y - 0.05*inch)
    c.drawString(MARGIN + 4.5*inch, y, "Word count goal:")
    c.line(MARGIN + 5.8*inch, y - 0.05*inch, PAGE_WIDTH - MARGIN, y - 0.05*inch)
    
    y -= 0.5*inch
    c.setFillColor(ACADEMIC_BLUE)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, y, "KEY ARGUMENTS TO MAKE:")
    c.setFillColor('black')
    c.setFont("Helvetica", 10)
    
    for i in range(5):
        y -= 0.3*inch
        c.drawString(MARGIN, y, f"{i+1}.")
        c.line(MARGIN + 0.3*inch, y - 0.05*inch, PAGE_WIDTH - MARGIN, y - 0.05*inch)
    
    y -= 0.5*inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, y, "LITERATURE TO CITE (must include):")
    c.setFont("Helvetica", 10)
    
    for i in range(8):
        y -= 0.25*inch
        draw_checkbox(c, MARGIN, y - 0.02*inch)
        c.line(MARGIN + 0.25*inch, y - 0.05*inch, PAGE_WIDTH - MARGIN, y - 0.05*inch)
    
    y -= 0.4*inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, y, "ADVISOR FEEDBACK INTEGRATION:")
    c.setFont("Helvetica", 10)
    
    y -= 0.25*inch
    c.drawString(MARGIN, y, "Date received:")
    c.line(MARGIN + 1.2*inch, y - 0.05*inch, MARGIN + 3*inch, y - 0.05*inch)
    c.drawString(MARGIN + 3.5*inch, y, "Status:")
    draw_checkbox(c, MARGIN + 4.2*inch, y - 0.02*inch)
    c.drawString(MARGIN + 4.5*inch, y, "Done")
    draw_checkbox(c, MARGIN + 5.2*inch, y - 0.02*inch)
    c.drawString(MARGIN + 5.5*inch, y, "WIP")
    
    y -= 0.3*inch
    c.drawString(MARGIN, y, "Key revisions needed:")
    for i in range(2):
        y -= 0.2*inch
        c.line(MARGIN, y, PAGE_WIDTH - MARGIN, y)

def draw_literature_tracker(c, page_num):
    """Generate literature review tracking page"""
    draw_header(c, "Literature Review Tracker", page_num)
    
    y = PAGE_HEIGHT - MARGIN - 0.5*inch
    
    for entry in range(4):
        c.setFont("Helvetica-Bold", 11)
        c.drawString(MARGIN, y, f"SOURCE {page_num*4 + entry - 59}:")
        
        y -= 0.25*inch
        c.setFont("Helvetica", 10)
        c.drawString(MARGIN, y, "Author:")
        c.line(MARGIN + 0.7*inch, y - 0.05*inch, MARGIN + 3.5*inch, y - 0.05*inch)
        c.drawString(MARGIN + 4*inch, y, "Year:")
        c.line(MARGIN + 4.6*inch, y - 0.05*inch, PAGE_WIDTH - MARGIN, y - 0.05*inch)
        
        y -= 0.25*inch
        c.drawString(MARGIN, y, "Key argument:")
        c.line(MARGIN + 1.1*inch, y - 0.05*inch, PAGE_WIDTH - MARGIN, y - 0.05*inch)
        
        y -= 0.25*inch
        c.drawString(MARGIN, y, "Where I'll cite it:")
        c.line(MARGIN + 1.5*inch, y - 0.05*inch, PAGE_WIDTH - MARGIN, y - 0.05*inch)
        
        y -= 0.25*inch
        c.drawString(MARGIN, y, "Notes:")
        c.line(MARGIN + 0.6*inch, y - 0.05*inch, PAGE_WIDTH - MARGIN, y - 0.05*inch)
        
        y -= 0.4*inch

def draw_advisor_meeting(c, meeting_num, page_num):
    """Generate advisor meeting prep page"""
    draw_header(c, f"Advisor Meeting #{meeting_num}", page_num)
    
    y = PAGE_HEIGHT - MARGIN - 0.5*inch
    
    c.setFont("Helvetica", 11)
    c.drawString(MARGIN, y, "Meeting date:")
    c.line(MARGIN + 1.2*inch, y - 0.05*inch, MARGIN + 3.5*inch, y - 0.05*inch)
    c.drawString(MARGIN + 4*inch, y, "Location:")
    c.line(MARGIN + 4.8*inch, y - 0.05*inch, PAGE_WIDTH - MARGIN, y - 0.05*inch)
    
    y -= 0.5*inch
    c.setFillColor(ACADEMIC_BLUE)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, y, "AGENDA:")
    c.setFillColor('black')
    c.setFont("Helvetica", 10)
    
    for i in range(5):
        y -= 0.25*inch
        c.drawString(MARGIN, y, f"{i+1}.")
        c.line(MARGIN + 0.3*inch, y - 0.05*inch, PAGE_WIDTH - MARGIN, y - 0.05*inch)
    
    y -= 0.5*inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, y, "QUESTIONS TO ASK:")
    c.setFont("Helvetica", 10)
    
    for i in range(5):
        y -= 0.25*inch
        c.line(MARGIN, y, PAGE_WIDTH - MARGIN, y)
    
    y -= 0.5*inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, y, "ACTION ITEMS:")
    c.setFont("Helvetica", 10)
    
    for i in range(6):
        y -= 0.25*inch
        draw_checkbox(c, MARGIN, y - 0.02*inch)
        c.line(MARGIN + 0.25*inch, y - 0.05*inch, PAGE_WIDTH - MARGIN, y - 0.05*inch)

def generate_phd_planner():
    """Generate complete PhD Dissertation Progress Tracker PDF"""
    output_dir = "../products"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "PhD-Dissertation-Progress-Tracker-60-Printable-Pages.pdf")
    
    c = canvas.Canvas(output_file, pagesize=letter)
    
    # Title page
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 2*inch, "PhD Dissertation")
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 2.4*inch, "Progress Tracker")
    c.setFont("Helvetica", 14)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 3*inch, "60 Printable Pages")
    c.setFont("Helvetica", 11)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 3.5*inch, "Structured planning for doctoral students")
    c.showPage()
    
    page_num = 1
    
    # Dissertation overview
    print("Generating dissertation overview...")
    draw_dissertation_overview(c)
    c.showPage()
    page_num += 1
    
    # 18 chapter planning sheets (3 per chapter, 6 chapters)
    print("Generating 18 chapter planning sheets...")
    for ch in range(1, 7):
        for rep in range(3):
            draw_chapter_planning(c, ch, page_num)
            c.showPage()
            page_num += 1
    
    # 20 literature tracker pages
    print("Generating 20 literature tracker pages...")
    for i in range(20):
        draw_literature_tracker(c, page_num)
        c.showPage()
        page_num += 1
    
    # 12 advisor meeting prep pages
    print("Generating 12 advisor meeting pages...")
    for i in range(1, 13):
        draw_advisor_meeting(c, i, page_num)
        c.showPage()
        page_num += 1
    
    # 8 weekly log pages
    print("Generating 8 weekly log pages...")
    for i in range(8):
        draw_header(c, f"Weekly Dissertation Log - Week {i+1}", page_num)
        y = PAGE_HEIGHT - MARGIN - 0.5*inch
        c.setFont("Helvetica", 11)
        c.drawString(MARGIN, y, "Week of:")
        c.line(MARGIN + 0.8*inch, y - 0.05*inch, MARGIN + 3*inch, y - 0.05*inch)
        
        y -= 0.4*inch
        c.setFont("Helvetica-Bold", 11)
        c.drawString(MARGIN, y, "Hours logged this week:")
        c.setFont("Helvetica", 11)
        c.line(MARGIN + 2*inch, y - 0.05*inch, MARGIN + 3*inch, y - 0.05*inch)
        
        y -= 0.3*inch
        c.setFont("Helvetica-Bold", 11)
        c.drawString(MARGIN, y, "Pages written:")
        c.setFont("Helvetica", 11)
        c.line(MARGIN + 1.3*inch, y - 0.05*inch, MARGIN + 3*inch, y - 0.05*inch)
        
        y -= 0.5*inch
        c.setFont("Helvetica-Bold", 11)
        c.drawString(MARGIN, y, "Progress this week:")
        c.setFont("Helvetica", 10)
        for j in range(5):
            y -= 0.25*inch
            c.line(MARGIN, y, PAGE_WIDTH - MARGIN, y)
        
        y -= 0.4*inch
        c.setFont("Helvetica-Bold", 11)
        c.drawString(MARGIN, y, "Obstacles encountered:")
        c.setFont("Helvetica", 10)
        for j in range(4):
            y -= 0.25*inch
            c.line(MARGIN, y, PAGE_WIDTH - MARGIN, y)
        
        y -= 0.4*inch
        c.setFont("Helvetica-Bold", 11)
        c.drawString(MARGIN, y, "Next week's priorities:")
        c.setFont("Helvetica", 10)
        for j in range(4):
            y -= 0.25*inch
            draw_checkbox(c, MARGIN, y - 0.02*inch)
            c.line(MARGIN + 0.25*inch, y - 0.05*inch, PAGE_WIDTH - MARGIN, y - 0.05*inch)
        
        c.showPage()
        page_num += 1
    
    c.save()
    print(f"✓ Generated: {output_file}")
    print(f"  Total pages: {page_num} (1 title + 1 overview + 18 planning + 20 literature + 12 meetings + 8 logs)")
    return output_file

if __name__ == "__main__":
    generate_phd_planner()
