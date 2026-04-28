#!/usr/bin/env python3
"""
Generate Freelance Client & Project Dashboard PDF
55 pages: client management + project tracking + invoicing
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import os

PAGE_WIDTH, PAGE_HEIGHT = letter
MARGIN = 0.5 * inch
PROFESSIONAL_GREEN = HexColor('#10B981')
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

def draw_circle(c, x, y, radius=0.08*inch):
    c.setStrokeColor('black')
    c.setLineWidth(1)
    c.circle(x + radius, y + radius, radius, stroke=1, fill=0)

def draw_master_client_list(c, page_num):
    """Generate master client list page"""
    draw_header(c, f"Active Clients — Page {page_num}", page_num)
    
    y = PAGE_HEIGHT - MARGIN - 0.5*inch
    
    c.setFillColor(PROFESSIONAL_GREEN)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, y, "ACTIVE CLIENTS")
    c.setFillColor('black')
    
    y -= 0.3*inch
    
    # Table header
    c.setFont("Helvetica-Bold", 10)
    c.drawString(MARGIN, y, "Client Name")
    c.drawString(MARGIN + 2.5*inch, y, "Status")
    c.drawString(MARGIN + 4*inch, y, "Next Deadline")
    c.drawString(MARGIN + 6*inch, y, "Revenue")
    
    c.setStrokeColor(GRAY)
    c.setLineWidth(1)
    c.line(MARGIN, y - 0.1*inch, PAGE_WIDTH - MARGIN, y - 0.1*inch)
    
    y -= 0.3*inch
    c.setFont("Helvetica", 10)
    
    # 10 client rows
    for i in range(10):
        c.line(MARGIN, y, MARGIN + 2.3*inch, y)
        c.line(MARGIN + 2.5*inch, y, MARGIN + 3.8*inch, y)
        c.line(MARGIN + 4*inch, y, MARGIN + 5.8*inch, y)
        c.line(MARGIN + 6*inch, y, PAGE_WIDTH - MARGIN, y)
        y -= 0.35*inch
    
    y -= 0.3*inch
    
    # Revenue summary
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, y, "REVENUE THIS MONTH:")
    c.setFont("Helvetica", 11)
    c.drawString(MARGIN + 2*inch, y, "$_____________")
    
    y -= 0.3*inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, y, "Outstanding invoices:")
    c.setFont("Helvetica", 11)
    c.drawString(MARGIN + 2*inch, y, "$_____________")
    
    y -= 0.3*inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, y, "Pipeline value:")
    c.setFont("Helvetica", 11)
    c.drawString(MARGIN + 2*inch, y, "$_____________")

def draw_client_intake(c, page_num):
    """Generate client intake form"""
    draw_header(c, "New Client Intake", page_num)
    
    y = PAGE_HEIGHT - MARGIN - 0.5*inch
    
    c.setFillColor(PROFESSIONAL_GREEN)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, y, "NEW CLIENT INTAKE")
    c.setFillColor('black')
    
    y -= 0.4*inch
    c.setFont("Helvetica", 11)
    c.drawString(MARGIN, y, "Client name:")
    c.line(MARGIN + 1.2*inch, y - 0.05*inch, PAGE_WIDTH - MARGIN, y - 0.05*inch)
    
    y -= 0.3*inch
    c.drawString(MARGIN, y, "Company:")
    c.line(MARGIN + 1*inch, y - 0.05*inch, PAGE_WIDTH - MARGIN, y - 0.05*inch)
    
    y -= 0.3*inch
    c.drawString(MARGIN, y, "Contact:")
    c.line(MARGIN + 0.9*inch, y - 0.05*inch, MARGIN + 4*inch, y - 0.05*inch)
    c.drawString(MARGIN + 4.5*inch, y, "Email:")
    c.line(MARGIN + 5.1*inch, y - 0.05*inch, PAGE_WIDTH - MARGIN, y - 0.05*inch)
    
    y -= 0.5*inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, y, "PROJECT SCOPE:")
    c.setFont("Helvetica", 10)
    
    y -= 0.25*inch
    c.drawString(MARGIN, y, "Service requested:")
    c.line(MARGIN + 1.5*inch, y - 0.05*inch, PAGE_WIDTH - MARGIN, y - 0.05*inch)
    
    y -= 0.25*inch
    c.drawString(MARGIN, y, "Deliverables:")
    for i in range(3):
        y -= 0.2*inch
        c.line(MARGIN, y, PAGE_WIDTH - MARGIN, y)
    
    y -= 0.4*inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, y, "BUDGET & TIMELINE:")
    c.setFont("Helvetica", 10)
    
    y -= 0.25*inch
    c.drawString(MARGIN, y, "Budget: $")
    c.line(MARGIN + 0.8*inch, y - 0.05*inch, MARGIN + 2.5*inch, y - 0.05*inch)
    c.drawString(MARGIN + 3*inch, y, "Deposit: $")
    c.line(MARGIN + 3.9*inch, y - 0.05*inch, PAGE_WIDTH - MARGIN, y - 0.05*inch)
    
    y -= 0.25*inch
    c.drawString(MARGIN, y, "Start date:")
    c.line(MARGIN + 1*inch, y - 0.05*inch, MARGIN + 3*inch, y - 0.05*inch)
    c.drawString(MARGIN + 3.5*inch, y, "Deadline:")
    c.line(MARGIN + 4.4*inch, y - 0.05*inch, PAGE_WIDTH - MARGIN, y - 0.05*inch)
    
    y -= 0.4*inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, y, "COMMUNICATION PREFERENCES:")
    c.setFont("Helvetica", 10)
    
    y -= 0.25*inch
    c.drawString(MARGIN, y, "Preferred contact:")
    draw_checkbox(c, MARGIN + 1.6*inch, y - 0.02*inch)
    c.drawString(MARGIN + 1.9*inch, y, "Email")
    draw_checkbox(c, MARGIN + 2.7*inch, y - 0.02*inch)
    c.drawString(MARGIN + 3*inch, y, "Slack")
    draw_checkbox(c, MARGIN + 3.8*inch, y - 0.02*inch)
    c.drawString(MARGIN + 4.1*inch, y, "Phone")
    
    y -= 0.25*inch
    c.drawString(MARGIN, y, "Meeting frequency:")
    draw_checkbox(c, MARGIN + 1.6*inch, y - 0.02*inch)
    c.drawString(MARGIN + 1.9*inch, y, "Weekly")
    draw_checkbox(c, MARGIN + 2.9*inch, y - 0.02*inch)
    c.drawString(MARGIN + 3.2*inch, y, "Biweekly")
    
    y -= 0.4*inch
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(HexColor('#DC2626'))
    c.drawString(MARGIN, y, "RED FLAGS TO WATCH:")
    c.setFillColor('black')
    c.setFont("Helvetica", 10)
    
    y -= 0.25*inch
    draw_checkbox(c, MARGIN, y - 0.02*inch)
    c.drawString(MARGIN + 0.25*inch, y, "Vague scope")
    draw_checkbox(c, MARGIN + 2*inch, y - 0.02*inch)
    c.drawString(MARGIN + 2.25*inch, y, "Unrealistic timeline")
    
    y -= 0.25*inch
    draw_checkbox(c, MARGIN, y - 0.02*inch)
    c.drawString(MARGIN + 0.25*inch, y, "Low budget")
    draw_checkbox(c, MARGIN + 2*inch, y - 0.02*inch)
    c.drawString(MARGIN + 2.25*inch, y, "Too many decision-makers")
    
    y -= 0.4*inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, y, "DECISION:")
    draw_checkbox(c, MARGIN + 1*inch, y - 0.02*inch)
    c.setFont("Helvetica", 10)
    c.drawString(MARGIN + 1.25*inch, y, "Accept")
    draw_checkbox(c, MARGIN + 2.2*inch, y - 0.02*inch)
    c.drawString(MARGIN + 2.45*inch, y, "Decline")
    draw_checkbox(c, MARGIN + 3.5*inch, y - 0.02*inch)
    c.drawString(MARGIN + 3.75*inch, y, "Negotiate")

def draw_project_milestone_tracker(c, page_num):
    """Generate project milestone tracking page"""
    draw_header(c, "Project Milestone Tracker", page_num)
    
    y = PAGE_HEIGHT - MARGIN - 0.5*inch
    
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, y, "PROJECT:")
    c.line(MARGIN + 0.9*inch, y - 0.05*inch, MARGIN + 4*inch, y - 0.05*inch)
    c.drawString(MARGIN + 4.5*inch, y, "CLIENT:")
    c.line(MARGIN + 5.3*inch, y - 0.05*inch, PAGE_WIDTH - MARGIN, y - 0.05*inch)
    
    y -= 0.5*inch
    c.setFillColor(PROFESSIONAL_GREEN)
    c.drawString(MARGIN, y, "MILESTONE TIMELINE:")
    c.setFillColor('black')
    c.setFont("Helvetica", 10)
    
    phases = ["Phase 1", "Phase 2", "Phase 3"]
    for i, phase in enumerate(phases):
        y -= 0.35*inch
        c.setFont("Helvetica-Bold", 10)
        c.drawString(MARGIN, y, f"{phase}:")
        c.setFont("Helvetica", 10)
        c.line(MARGIN + 0.8*inch, y - 0.05*inch, MARGIN + 3*inch, y - 0.05*inch)
        c.drawString(MARGIN + 3.5*inch, y, "Due:")
        c.line(MARGIN + 4*inch, y - 0.05*inch, MARGIN + 5.5*inch, y - 0.05*inch)
        draw_checkbox(c, MARGIN + 6*inch, y - 0.02*inch)
        c.drawString(MARGIN + 6.3*inch, y, "Done")
        
        y -= 0.25*inch
        c.drawString(MARGIN + 0.2*inch, y, "Tasks:")
        c.line(MARGIN + 0.7*inch, y - 0.05*inch, PAGE_WIDTH - MARGIN, y - 0.05*inch)
        y -= 0.2*inch
        c.line(MARGIN + 0.7*inch, y, PAGE_WIDTH - MARGIN, y)
    
    y -= 0.5*inch
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(HexColor('#DC2626'))
    c.drawString(MARGIN, y, "SCOPE CREEP LOG:")
    c.setFillColor('black')
    
    y -= 0.25*inch
    c.setFont("Helvetica", 9)
    c.drawString(MARGIN, y, "Date")
    c.drawString(MARGIN + 1*inch, y, "Request")
    c.drawString(MARGIN + 4.5*inch, y, "Response")
    
    c.setLineWidth(1)
    c.line(MARGIN, y - 0.1*inch, PAGE_WIDTH - MARGIN, y - 0.1*inch)
    
    y -= 0.25*inch
    for i in range(5):
        c.line(MARGIN, y, MARGIN + 0.8*inch, y)
        c.line(MARGIN + 1*inch, y, MARGIN + 4.3*inch, y)
        draw_checkbox(c, MARGIN + 4.5*inch, y - 0.02*inch, 0.1*inch)
        c.drawString(MARGIN + 4.7*inch, y, "In scope")
        draw_checkbox(c, MARGIN + 5.6*inch, y - 0.02*inch, 0.1*inch)
        c.drawString(MARGIN + 5.8*inch, y, "Out of scope")
        y -= 0.3*inch
    
    y -= 0.3*inch
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, y, "CLIENT FEEDBACK:")
    c.setFont("Helvetica", 10)
    for i in range(3):
        y -= 0.25*inch
        c.line(MARGIN, y, PAGE_WIDTH - MARGIN, y)

def draw_invoice_tracker(c, page_num):
    """Generate invoice tracking page"""
    draw_header(c, "Invoice Tracker", page_num)
    
    y = PAGE_HEIGHT - MARGIN - 0.5*inch
    
    c.setFillColor(PROFESSIONAL_GREEN)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(MARGIN, y, "INVOICE TRACKING")
    c.setFillColor('black')
    
    y -= 0.3*inch
    
    # Table header
    c.setFont("Helvetica-Bold", 9)
    c.drawString(MARGIN, y, "Invoice #")
    c.drawString(MARGIN + 1*inch, y, "Client")
    c.drawString(MARGIN + 2.8*inch, y, "Amount")
    c.drawString(MARGIN + 4*inch, y, "Sent")
    c.drawString(MARGIN + 5*inch, y, "Due")
    c.drawString(MARGIN + 6*inch, y, "Paid")
    
    c.setLineWidth(1)
    c.line(MARGIN, y - 0.1*inch, PAGE_WIDTH - MARGIN, y - 0.1*inch)
    
    y -= 0.3*inch
    c.setFont("Helvetica", 9)
    
    # 10 invoice rows
    for i in range(10):
        c.line(MARGIN, y, MARGIN + 0.9*inch, y)
        c.line(MARGIN + 1*inch, y, MARGIN + 2.7*inch, y)
        c.line(MARGIN + 2.8*inch, y, MARGIN + 3.9*inch, y)
        c.line(MARGIN + 4*inch, y, MARGIN + 4.9*inch, y)
        c.line(MARGIN + 5*inch, y, MARGIN + 5.9*inch, y)
        c.line(MARGIN + 6*inch, y, PAGE_WIDTH - MARGIN, y)
        y -= 0.35*inch

def generate_freelance_planner():
    """Generate complete Freelance Client & Project Dashboard PDF"""
    output_dir = "../products"
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "Freelance-Client-Project-Dashboard-55-Printable-Pages.pdf")
    
    c = canvas.Canvas(output_file, pagesize=letter)
    
    # Title page
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 2*inch, "Freelance Client &")
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 2.4*inch, "Project Dashboard")
    c.setFont("Helvetica", 14)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 3*inch, "55 Printable Pages")
    c.setFont("Helvetica", 11)
    c.drawCentredString(PAGE_WIDTH/2, PAGE_HEIGHT - 3.5*inch, "Professional client management for freelancers")
    c.showPage()
    
    page_num = 1
    
    # 2 master client list pages
    print("Generating 2 master client list pages...")
    for i in range(2):
        draw_master_client_list(c, page_num)
        c.showPage()
        page_num += 1
    
    # 15 client intake forms
    print("Generating 15 client intake forms...")
    for i in range(15):
        draw_client_intake(c, page_num)
        c.showPage()
        page_num += 1
    
    # 15 project milestone trackers
    print("Generating 15 project milestone trackers...")
    for i in range(15):
        draw_project_milestone_tracker(c, page_num)
        c.showPage()
        page_num += 1
    
    # 10 invoice trackers
    print("Generating 10 invoice tracker pages...")
    for i in range(10):
        draw_invoice_tracker(c, page_num)
        c.showPage()
        page_num += 1
    
    # 12 weekly dashboards
    print("Generating 12 weekly dashboard pages...")
    for week in range(1, 13):
        draw_header(c, f"Weekly Freelance Dashboard — Week {week}", page_num)
        y = PAGE_HEIGHT - MARGIN - 0.5*inch
        
        c.setFont("Helvetica", 11)
        c.drawString(MARGIN, y, "Week of:")
        c.line(MARGIN + 0.8*inch, y - 0.05*inch, MARGIN + 3*inch, y - 0.05*inch)
        
        y -= 0.4*inch
        c.setFont("Helvetica-Bold", 11)
        c.drawString(MARGIN, y, "HOURS LOGGED BY CLIENT:")
        c.setFont("Helvetica", 10)
        
        for i in range(6):
            y -= 0.3*inch
            c.line(MARGIN, y, MARGIN + 3*inch, y)
            c.line(MARGIN + 3.5*inch, y, MARGIN + 4.5*inch, y)
            c.drawString(MARGIN + 4.7*inch, y, "hrs")
        
        y -= 0.4*inch
        c.setFont("Helvetica-Bold", 11)
        c.drawString(MARGIN, y, "REVENUE EARNED THIS WEEK:")
        c.setFont("Helvetica", 11)
        c.drawString(MARGIN + 2.5*inch, y, "$____________")
        
        y -= 0.4*inch
        c.setFont("Helvetica-Bold", 11)
        c.drawString(MARGIN, y, "UPCOMING DEADLINES:")
        c.setFont("Helvetica", 10)
        for i in range(5):
            y -= 0.25*inch
            c.line(MARGIN, y, MARGIN + 3*inch, y)
            c.line(MARGIN + 3.5*inch, y, MARGIN + 5*inch, y)
        
        y -= 0.4*inch
        c.setFont("Helvetica-Bold", 11)
        c.drawString(MARGIN, y, "TASKS BLOCKED / WAITING ON CLIENT:")
        c.setFont("Helvetica", 10)
        for i in range(4):
            y -= 0.25*inch
            c.line(MARGIN, y, PAGE_WIDTH - MARGIN, y)
        
        c.showPage()
        page_num += 1
    
    c.save()
    print(f"✓ Generated: {output_file}")
    print(f"  Total pages: {page_num} (1 title + 2 client lists + 15 intakes + 15 trackers + 10 invoices + 12 weekly)")
    return output_file

if __name__ == "__main__":
    generate_freelance_planner()
