#!/usr/bin/env python3
"""
Send personalized cold emails to ALL verified prospects from prospects-verified.csv
Uses SendGrid with BCC to b2bemails@solvd.studio for tracking.
Skips prospects already contacted in the first campaign (prospects.csv).
"""

import os
import sys
import csv
import json
import time
from datetime import datetime
from pathlib import Path

# Add automation directory to path
sys.path.insert(0, str(Path(__file__).parent / 'automation'))

# Load .env manually (source doesn't work in subprocess)
env_path = Path(__file__).parent / 'automation' / '.env'
if env_path.exists():
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                # Handle 'export KEY="VALUE"' format
                line = line.replace('export ', '')
                key, _, val = line.partition('=')
                val = val.strip().strip('"').strip("'")
                os.environ[key.strip()] = val

from email_sender import EmailSender

BCC_EMAIL = "b2bemails@solvd.studio"

# Prospects already emailed in the first (unverified) batch
ALREADY_EMAILED = {
    "alex@screendesk.io",
    "sarah@buildbuddy.io",
    "marcus@clarityhq.com",
    "priya@flowtest.dev",
    "david@revenueops.ai",
    "emma@talentgrid.io",
    "james@secureapi.dev",
    "lisa@marketpulse.io",
    "tom@devplatform.io",
    "sophie@bizflow.ai",
}


def get_hook_for_prospect(prospect):
    why = prospect.get('why_they_need_help', '').lower()
    company = prospect.get('company', '')

    if 'funding' in why or 'raised' in why or 'seed' in why or 'yc' in why.lower() or prospect.get('source', '').upper() in ('YC',):
        return f"Congrats on the funding — scaling a B2B pipeline after a raise is where most founders get stuck"
    elif 'product hunt' in why or 'launched' in why or prospect.get('source', '') == 'ProductHunt':
        return f"Congrats on launching {company} on Product Hunt — converting that attention into pipeline is the hard part"
    elif 'posted' in why and 'linkedin' in why:
        return f"I saw your recent LinkedIn post on cold outreach challenges"
    elif 'hiring' in why:
        return f"I noticed {company} is hiring for sales roles — that usually means cold outreach is about to scale up"
    elif 'indiehacker' in why.lower() or prospect.get('source', '') == 'IndieHackers':
        return f"I've been following {company}'s journey on Indie Hackers"
    else:
        return f"I've been following {company}'s growth"


def get_tip_for_prospect(prospect):
    desc = prospect.get('product_description', '').lower()
    why = prospect.get('why_they_need_help', '').lower()

    # Devtools / API / infra
    if any(w in desc for w in ['dev', 'engineer', 'api', 'testing', 'build', 'platform', 'infrastructure', 'sdk', 'integration', 'bot', 'automation']):
        return "Your emails lead with architecture and integrations. Engineering buyers still answer to a budget. Open with the ROI, then prove the tech."
    # Fintech / compliance / security
    elif any(w in desc for w in ['fintech', 'financial', 'payment', 'security', 'compliance', 'risk', 'billing']):
        return "Finance and security buyers live in a compliance-first world. Email 1 with no social proof reads as risk. Add one client name or a one-line result (e.g., 'We helped Team X cut reconciliation time by 3 hrs/week')."
    # HR / talent / onboarding
    elif any(w in desc for w in ['hr', 'talent', 'onboarding', 'recruiting']):
        return "HR leaders are bought on outcomes tied to retention or compliance, not features. Open with the cost of the status quo: 'Most HR teams lose 8 hours/week on X.' Then show the fix."
    # Marketing / analytics / SEO
    elif any(w in desc for w in ['marketing', 'attribution', 'analytics', 'campaign', 'seo', 'content']):
        return "Marketing buyers have shifted from vanity metrics to revenue attribution. If your email mentions impressions or engagement — reframe everything around pipeline and closed-won."
    # Sales / CRM / revenue
    elif any(w in desc for w in ['sales', 'revenue', 'crm', 'outbound', 'pipeline', 'deal']):
        return "Most B2B cold emails bury the CTA after three paragraphs. Move your ask to line 3. Response rates typically jump 20–35%."
    # Support / feedback / docs / knowledge
    elif any(w in desc for w in ['support', 'customer', 'feedback', 'documentation', 'knowledge', 'wiki', 'onboard']):
        return "Operations buyers need one sharp insight, not a product tour. 'Your team spends 10 hrs/week on X — here's a 2-minute fix' converts far better than a feature list."
    # Community / DevRel
    elif any(w in desc for w in ['community', 'devrel', 'open source']):
        return "Community-led growth is powerful but hits a ceiling with enterprise buyers. Your cold email needs a different hook for procurement: ROI, risk reduction, and a peer reference."
    # Default
    else:
        return "Your subject line is likely too generic. B2B founders get 50 of these per day. Try something specific: '[Company]'s emails have a 12% response rate — here's why that's low and how to fix it.'"


def personalize_email(prospect):
    first_name = prospect['name'].split()[0]
    company = prospect['company']
    hook = get_hook_for_prospect(prospect)
    tip = get_tip_for_prospect(prospect)

    subject = f"{first_name}, quick cold email feedback for {company}?"

    body = f"""Hi {first_name},

{hook}.

I help B2B SaaS founders improve cold email response rates — and I spotted a quick win for {company}:

{tip}

Want a free 15-min teardown of your current emails? I'll find 3 more fixes like this.

→ https://calendly.com/coldemailteardown/15min

Best,
Nuno
--
Nuno Cadete | Cold Email Consultant
Helping B2B SaaS founders build pipelines that convert
Unsubscribe: reply with "unsubscribe" """

    return subject, body


def load_verified_prospects(csv_path):
    prospects = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('mx_valid', '').lower() in ('true', '1', 'yes') and \
               row.get('verification_status', '').lower() == 'mx_valid':
                prospects.append(row)
    return prospects


def main():
    print("\n" + "="*60)
    print("VERIFIED PROSPECT CAMPAIGN — with BCC to b2bemails@solvd.studio")
    print("="*60 + "\n")

    # Init sender
    try:
        sender = EmailSender()
        print(f"✅ SendGrid initialized")
        print(f"✅ BCC configured: {sender.bcc_email}\n")
    except Exception as e:
        print(f"❌ Failed to initialize SendGrid: {e}")
        return 1

    # Load verified prospects
    verified_path = Path(__file__).parent / 'prospects-verified.csv'
    if not verified_path.exists():
        print(f"❌ prospects-verified.csv not found")
        return 1

    all_prospects = load_verified_prospects(str(verified_path))
    # Filter out already emailed
    prospects = [p for p in all_prospects if p['email'].lower() not in ALREADY_EMAILED]

    skipped = len(all_prospects) - len(prospects)
    print(f"✅ Loaded {len(all_prospects)} verified prospects")
    print(f"⏭️  Skipping {skipped} already contacted in previous batch")
    print(f"📬 New outreach targets: {len(prospects)}\n")

    results = []
    success_count = 0
    fail_count = 0

    for i, prospect in enumerate(prospects, 1):
        name = prospect['name']
        email = prospect['email']
        company = prospect['company']
        source = prospect.get('source', 'unknown')

        subject, body = personalize_email(prospect)

        print(f"[{i}/{len(prospects)}] {name} ({company}) [{source}]")
        print(f"    To: {email}")
        print(f"    BCC: {BCC_EMAIL}")
        print(f"    Subject: {subject}")

        try:
            result = sender.send_email(
                to_email=email,
                to_name=name,
                subject=subject,
                body=body
            )

            if result.get('success'):
                print(f"    ✅ SENT\n")
                success_count += 1
                results.append({
                    'prospect': name, 'email': email, 'company': company,
                    'source': source, 'status': 'sent',
                    'sent_at': datetime.now().isoformat()
                })
            else:
                print(f"    ❌ FAILED: {result.get('error')}\n")
                fail_count += 1
                results.append({
                    'prospect': name, 'email': email, 'company': company,
                    'source': source, 'status': 'failed',
                    'error': result.get('error'), 'sent_at': datetime.now().isoformat()
                })

        except Exception as e:
            print(f"    ❌ ERROR: {e}\n")
            fail_count += 1
            results.append({
                'prospect': name, 'email': email, 'company': company,
                'status': 'error', 'error': str(e),
                'sent_at': datetime.now().isoformat()
            })

        # Rate limiting — 3 sec between emails
        if i < len(prospects):
            time.sleep(3)

    # Summary
    print("="*60)
    print("CAMPAIGN SUMMARY")
    print("="*60)
    print(f"✅ Successfully sent: {success_count}/{len(prospects)}")
    print(f"❌ Failed: {fail_count}/{len(prospects)}")
    print(f"📧 BCC on all emails: {BCC_EMAIL}")
    print("="*60 + "\n")

    # Save results
    results_path = Path(__file__).parent / 'campaign-verified-results.json'
    with open(results_path, 'w') as f:
        json.dump({
            'campaign_date': datetime.now().isoformat(),
            'campaign_type': 'verified_prospects',
            'bcc': BCC_EMAIL,
            'total_prospects': len(prospects),
            'sent': success_count,
            'failed': fail_count,
            'skipped_already_contacted': skipped,
            'results': results
        }, f, indent=2)

    print(f"📊 Results saved to campaign-verified-results.json\n")

    # Update task log
    task_log_path = Path(__file__).parent / 'task-log.md'
    with open(task_log_path, 'a') as f:
        f.write(f"\n## [task-agent] {datetime.now().strftime('%Y-%m-%d %H:%M')} — Verified Prospect Campaign\n\n")
        f.write(f"**Agent:** Project Agent (b2b-cold-email-consulting)  \n")
        f.write(f"**Task:** Send cold emails to all verified MX-valid prospects  \n")
        f.write(f"**BCC configured:** {BCC_EMAIL}  \n")
        f.write(f"**Results:**  \n")
        f.write(f"- Total verified prospects available: {len(all_prospects)}  \n")
        f.write(f"- Skipped (already emailed): {skipped}  \n")
        f.write(f"- New outreach: {len(prospects)}  \n")
        f.write(f"- Successfully sent: {success_count}  \n")
        f.write(f"- Failed: {fail_count}  \n")
        f.write(f"- Success rate: {(success_count/len(prospects)*100):.1f}% \n\n")
        f.write(f"**Sent to:**  \n")
        for r in results:
            if r['status'] == 'sent':
                f.write(f"- ✅ {r['prospect']} ({r['company']}) [{r.get('source','')}] — {r['email']}  \n")
        if fail_count > 0:
            f.write(f"\n**Failed:**  \n")
            for r in results:
                if r['status'] != 'sent':
                    f.write(f"- ❌ {r['prospect']} — {r.get('error', 'Unknown')}  \n")
        f.write(f"\n**Next steps:**  \n")
        f.write(f"- Monitor b2bemails@solvd.studio inbox for BCC copies  \n")
        f.write(f"- Watch for replies in marketing@solvd.studio  \n")
        f.write(f"- Follow-up Email 2 scheduled: Day 3 (send-followup.py)  \n")
        f.write(f"- Target: 10% reply rate = ~{max(1,int(success_count*0.10))} replies  \n\n")
        f.write("---\n")

    return 0 if fail_count == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
