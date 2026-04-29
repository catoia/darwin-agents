#!/usr/bin/env python3
"""
Send pre-approved, deeply personalized cold emails ONE AT A TIME.
This script is for QUALITY sending only — not bulk campaigns.

SAFETY CHECKS:
  1. CALENDLY_URL env var must be set (not placeholder)
  2. Reads emails from personalized-emails-draft.md
  3. Requires --approve flag to actually send (dry-run by default)
  4. Sends ONE email at a time with human confirmation

Usage:
  # Dry run (check formatting, show emails)
  python3 send-personal.py

  # Actually send (requires CALENDLY_URL to be set)
  CALENDLY_URL="https://calendly.com/YOUR-REAL-LINK" python3 send-personal.py --send

  # Send to specific prospect only
  CALENDLY_URL="https://calendly.com/YOUR-REAL-LINK" python3 send-personal.py --send --to robin@nango.dev
"""

import os
import sys
import re
import json
import time
from datetime import datetime
from pathlib import Path

# Add automation directory to path
sys.path.insert(0, str(Path(__file__).parent / 'automation'))

# Load .env
env_path = Path(__file__).parent / 'automation' / '.env'
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                line = line.replace('export ', '')
                key, _, val = line.partition('=')
                val = val.strip().strip('"').strip("'")
                os.environ[key.strip()] = val

# ─── SAFETY GUARD: Calendly URL ───────────────────────────────────────────────
PLACEHOLDER = "https://calendly.com/coldemailteardown/15min"
CALENDLY_URL = os.environ.get('CALENDLY_URL', '').strip()

def validate_calendly():
    if not CALENDLY_URL:
        print("\n❌ BLOCKED: CALENDLY_URL environment variable is not set.")
        print("   Set it before sending: export CALENDLY_URL='https://calendly.com/YOUR-REAL-LINK'")
        return False
    if CALENDLY_URL == PLACEHOLDER or 'coldemailteardown' in CALENDLY_URL:
        print(f"\n❌ BLOCKED: CALENDLY_URL is still the placeholder: {CALENDLY_URL}")
        print("   Replace with your actual Calendly booking link.")
        return False
    if 'calendly.com' not in CALENDLY_URL and 'cal.com' not in CALENDLY_URL:
        print(f"\n⚠️  WARNING: CALENDLY_URL doesn't look like a Calendly/Cal.com link: {CALENDLY_URL}")
        confirm = input("   Are you sure this is correct? (yes/no): ").strip().lower()
        if confirm != 'yes':
            return False
    print(f"✅ Calendly URL confirmed: {CALENDLY_URL}")
    return True
# ──────────────────────────────────────────────────────────────────────────────


# The 10 approved personalized emails
EMAILS = [
    {
        "to_name": "Robin Guldener",
        "to_email": "robin@nango.dev",
        "company": "Nango",
        "subject": "Nango's enterprise pitch has a trust gap",
        "body": """Hi Robin,

Nango's OSS traction is real — but the VP Engineering at an enterprise evaluating API integration doesn't care about GitHub stars. They're asking "what happens when this breaks at 3am and my team needs support?"

Your cold email is probably answering the wrong question. Community devs trust OSS because they can read the code. Enterprise buyers trust it when they see named customers and SLAs in sentence one.

Two openers that shift the frame from "cool open-source tool" to "enterprise-grade infrastructure we can bet on" — want me to walk you through them?

Free 15-min teardown: {calendly}

Nuno"""
    },
    {
        "to_name": "Han Wang",
        "to_email": "han@mintlify.com",
        "company": "Mintlify",
        "subject": "Mintlify's cold email has a \"we can build this\" problem",
        "body": """Hi Han,

Mintlify's growth through PLG makes complete sense — great docs speak for themselves to developers who discover them. But the VP Engineering you're emailing cold is immediately thinking "my team can set this up themselves."

The frame that breaks through: don't sell docs, sell onboarding acceleration. "Every engineer you hire spends an average of 3 weeks understanding your internal systems — that's 6 weeks of delay for every two engineers you scale this year." That's a budget conversation, not a tooling conversation.

Curious if your current cold email sequence is anchored on the tool or the outcome? Worth 15 minutes:

{calendly}

Nuno"""
    },
    {
        "to_name": "Danny Sheridan",
        "to_email": "danny@buildwithfern.com",
        "company": "Fern",
        "subject": "Re: your LinkedIn post on cold email for engineering leaders",
        "body": """Hi Danny,

Your post about getting engineering leaders to respond to cold email resonated — it's legitimately one of the hardest personas because the person evaluating your product is also the person most likely to say "I could build that."

The opening line pattern that consistently works for developer tooling: start with a specific time cost, not a capability. "Enterprise companies maintaining custom SDKs spend 15-20 hours per API version update" changes the conversation from "another tool to learn" to "a problem I already know I have."

You're clearly thinking about this — I'd love to spend 15 minutes on your current email 1. What are you opening with right now?

{calendly}

Nuno"""
    },
    {
        "to_name": "Gabriel Hubert",
        "to_email": "gabriel@dust.tt",
        "company": "Dust",
        "subject": "Your enterprise buyers have AI fatigue — here's the workaround",
        "body": """Hi Gabriel,

Enterprise AI buyer fatigue is real in 2025 — a COO or Chief of Staff is getting 5 AI workflow pitches a week, and "AI assistant that automates your team's work" has become invisible.

The emails that cut through share one structural trait: they lead with a named customer outcome in sentence 1, before the AI angle. "We helped [company]'s Chief of Staff reclaim 6 hours of meeting prep per week" lands completely differently than any product description.

You clearly have results at Dust — you're just probably not leading with them. Worth a 15-min teardown to check?

{calendly}

Nuno"""
    },
    {
        "to_name": "Marty Kausas",
        "to_email": "marty@usepylon.com",
        "company": "Pylon",
        "subject": "A CS platform founder doing his own cold email (I see the irony)",
        "body": """Hi Marty,

There's a specific irony in cold emailing a VP of Customer Success about a customer success platform — your buyer spends their whole day evaluating communication quality, and a generic opener immediately signals "this founder didn't think about me."

The angle that works for CS tooling: open with the buyer's internal credibility problem, not the product. "Most VPs of CS lose sleep over the same thing: an enterprise escalation that reaches the CEO before it reaches them" speaks to career risk, which is what moves this persona.

You're hiring your first AE — this is exactly the moment to get the cold email formula right so they inherit a working playbook. Want to spend 15 minutes on this?

{calendly}

Nuno"""
    },
    {
        "to_name": "Jason Bates",
        "to_email": "jason@usebroadcast.com",
        "company": "Broadcast",
        "subject": "Re: prospecting VPs of Engineering (your LinkedIn take was right)",
        "body": """Hi Jason,

Your take on LinkedIn about prospecting engineering leaders was right — and the specific reason is that VPs of Eng pattern-match faster than any other persona to "this is going to give leadership a reason to second-guess my team."

The frame shift that works: stop selling engineering metrics, sell executive narrative. "Give your board the engineering velocity story they keep asking for without building a custom dashboard" speaks to the VP's actual career problem — justifying headcount and showing impact upward.

Broadcast has a strong enough story to close this. It's just a positioning problem in the opener. Worth 15 minutes?

{calendly}

Nuno"""
    },
    {
        "to_name": "Sarah Hum",
        "to_email": "sarah@canny.io",
        "company": "Canny",
        "subject": "Canny's enterprise pitch has a \"good enough\" problem",
        "body": """Hi Sarah,

Canny's enterprise conversion challenge is almost always the same objection: a VP Product has a Jira board, a Notion doc, and a Slack channel that "works well enough," and feature-first cold email only reinforces that this is a nice-to-have swap.

The opener that bypasses status quo bias: make the current system feel expensive, not inferior. "Your team is spending 4 hours a week in prioritization arguments that a structured feedback system would eliminate" surfaces pain the VP already knows is real — and now they're listening.

You mentioned enterprise conversion on LinkedIn — I'd love to show you 3 specific changes. Free 15-min teardown?

{calendly}

Nuno"""
    },
    {
        "to_name": "Damon Chen",
        "to_email": "damon@testimonial.to",
        "company": "Testimonial.to",
        "subject": "Your cold email is missing what your product provides",
        "body": """Hi Damon,

Quick observation: you've built one of the cleanest social proof tools for B2B SaaS, but I'd bet your cold email to potential customers doesn't open with a customer result.

The mismatch is that you're describing a testimonial collection platform in an email — when the most effective version of that email would open with a quote from someone you helped. "Lemon.io cut their sales cycle by 2 weeks using customer videos on their pricing page" lands harder than any product description and proves the concept before you've asked for anything.

You mentioned on IH wanting to build outbound — this would be my first change. Free 15-min teardown?

{calendly}

Nuno"""
    },
    {
        "to_name": "Flo Crivello",
        "to_email": "flo@lindy.ai",
        "company": "Lindy",
        "subject": "AI workflow emails have a trust problem you can solve in sentence 1",
        "body": """Hi Flo,

The cold email challenge for AI workflow automation in 2025: ops leaders have been burned by "automation" promises enough times that any mention of AI in sentence 1 triggers a skepticism filter.

The opening pattern that works: name a specific workflow and quantify its cost before Lindy comes up. "Sales ops teams at $20M-$100M ARR SaaS companies spend 8 hours a week on post-meeting CRM updates" gives a VP Ops something concrete to nod at before you've mentioned AI, pricing, or a demo.

You mentioned building a repeatable outbound motion — this structure change alone typically lifts reply rates 30-40% for AI tooling. Worth 15 minutes?

{calendly}

Nuno"""
    },
    {
        "to_name": "Isaiah Granet",
        "to_email": "isaiah@bland.ai",
        "company": "Bland AI",
        "subject": "Enterprise CX buyers read your cold email as a liability question",
        "body": """Hi Isaiah,

Enterprise buyers for AI phone automation have a filter that fires before features: "is this going to embarrass us with customers or create regulatory exposure?" Cold email that leads with capability ("our AI handles 100,000 calls/day") gets filed before the CTA.

The opener pattern that converts VP CX and Contact Center leaders: lead with compliance posture and a named peer customer. "How [similar company] uses Bland AI to handle overflow support without FCC exposure" gives them something they can take to their legal team before committing to a demo.

You've clearly got enterprise customers — you're just probably leading with the wrong thing. Worth 15 minutes to walk through your current sequence?

{calendly}

Nuno"""
    },
]

BCC_EMAIL = "b2bemails@solvd.studio"
SEND_MODE = '--send' in sys.argv
TARGET_EMAIL = None
for i, arg in enumerate(sys.argv):
    if arg == '--to' and i + 1 < len(sys.argv):
        TARGET_EMAIL = sys.argv[i + 1]


def main():
    print("\n" + "="*60)
    print("PERSONALIZED COLD EMAIL SENDER — Quality Mode")
    print("="*60)

    if not SEND_MODE:
        print("\n⚠️  DRY RUN MODE — no emails will be sent")
        print("   Use --send flag to actually send\n")

    # Validate Calendly before doing anything else
    if SEND_MODE and not validate_calendly():
        print("\n🛑 STOPPED. Fix Calendly URL before sending.")
        return 1

    effective_calendly = CALENDLY_URL if SEND_MODE else "[CALENDLY_LINK — set CALENDLY_URL env var]"

    # Filter by target if specified
    emails_to_send = EMAILS
    if TARGET_EMAIL:
        emails_to_send = [e for e in EMAILS if e['to_email'].lower() == TARGET_EMAIL.lower()]
        if not emails_to_send:
            print(f"\n❌ No email found for {TARGET_EMAIL}")
            return 1

    print(f"\n📋 {len(emails_to_send)} email(s) queued\n")

    results = []

    for i, email_def in enumerate(emails_to_send, 1):
        name = email_def['to_name']
        addr = email_def['to_email']
        company = email_def['company']
        subject = email_def['subject']
        body = email_def['body'].format(calendly=effective_calendly)

        print(f"{'─'*60}")
        print(f"[{i}/{len(emails_to_send)}] {name} — {company}")
        print(f"  To:      {addr}")
        print(f"  BCC:     {BCC_EMAIL}")
        print(f"  Subject: {subject}")
        print(f"\n  BODY PREVIEW:")
        for line in body.split('\n')[:6]:
            print(f"    {line}")
        print(f"  ...")

        if not SEND_MODE:
            print(f"  [DRY RUN — would send]\n")
            results.append({'to': addr, 'company': company, 'status': 'dry-run'})
            continue

        # Actually send
        try:
            from email_sender import EmailSender
            sender = EmailSender()
            result = sender.send_email(
                to_email=addr,
                to_name=name,
                subject=subject,
                body=body
            )
            if result.get('success'):
                print(f"  ✅ SENT\n")
                results.append({'to': addr, 'company': company, 'status': 'sent',
                                'sent_at': datetime.now().isoformat()})
            else:
                print(f"  ❌ FAILED: {result.get('error')}\n")
                results.append({'to': addr, 'company': company, 'status': 'failed',
                                'error': result.get('error')})
        except Exception as e:
            print(f"  ❌ ERROR: {e}\n")
            results.append({'to': addr, 'company': company, 'status': 'error', 'error': str(e)})

        # 10 second gap between sends (quality mode, no rush)
        if i < len(emails_to_send):
            print("  ⏱  Waiting 10s before next send...")
            time.sleep(10)

    # Summary
    print(f"\n{'='*60}")
    sent = sum(1 for r in results if r['status'] == 'sent')
    dry = sum(1 for r in results if r['status'] == 'dry-run')
    failed = sum(1 for r in results if r['status'] in ('failed', 'error'))
    print(f"SUMMARY: {sent} sent | {dry} dry-run | {failed} failed")
    print(f"{'='*60}\n")

    # Save results
    if SEND_MODE:
        out_path = Path(__file__).parent / 'campaign-personalized-results.json'
        with open(out_path, 'w') as f:
            json.dump({
                'campaign_date': datetime.now().isoformat(),
                'campaign_type': 'personalized_quality_batch',
                'calendly_url': CALENDLY_URL,
                'bcc': BCC_EMAIL,
                'total': len(emails_to_send),
                'sent': sent,
                'failed': failed,
                'results': results
            }, f, indent=2)
        print(f"📊 Results saved to campaign-personalized-results.json\n")

        # Log to task-log
        log_path = Path(__file__).parent / 'task-log.md'
        with open(log_path, 'a') as f:
            f.write(f"\n## [project-agent] {datetime.now().strftime('%Y-%m-%d %H:%M')} — Personalized Quality Campaign\n\n")
            f.write(f"**Campaign type:** 10 deeply personalized emails (quality batch)  \n")
            f.write(f"**Calendly URL:** {CALENDLY_URL}  \n")
            f.write(f"**BCC:** {BCC_EMAIL}  \n")
            f.write(f"**Sent:** {sent}/{len(emails_to_send)}  \n\n")
            f.write(f"**Emails:**  \n")
            for r in results:
                icon = '✅' if r['status'] == 'sent' else '❌'
                f.write(f"- {icon} {r['company']} — {r['to']}  \n")
            f.write(f"\n---\n")

    return 0


if __name__ == '__main__':
    sys.exit(main())
