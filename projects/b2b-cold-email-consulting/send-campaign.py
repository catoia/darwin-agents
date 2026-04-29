#!/usr/bin/env python3
"""
Send personalized cold emails using SendGrid API
Reads prospects.csv, personalizes email-templates.md, sends via SendGrid
"""

import os
import sys
import csv
import json
from datetime import datetime
from pathlib import Path

# Add automation directory to path
sys.path.insert(0, str(Path(__file__).parent / 'automation'))

from email_sender import EmailSender

def load_prospects(csv_path):
    """Load prospects from CSV file"""
    prospects = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            prospects.append(row)
    return prospects

def get_hook_for_prospect(prospect):
    """Generate appropriate hook based on prospect context"""
    why = prospect.get('why_they_need_help', '').lower()
    
    if 'funding' in why or 'raised' in why or 'seed' in why:
        return f"Congrats on the Seed round — growing a sales pipeline fast is the next big challenge"
    elif 'product hunt' in why or 'launched' in why:
        return f"Congrats on launching {prospect['company']} on Product Hunt — converting that attention into pipeline is the hard part"
    elif 'posted' in why and 'linkedin' in why:
        return f"I saw your post about cold email challenges"
    elif 'hiring' in why:
        return f"I noticed {prospect['company']} is hiring for sales roles — that usually means cold outreach is about to scale up"
    else:
        return f"I've been following {prospect['company']}'s growth"

def get_tip_for_prospect(prospect):
    """Generate industry-specific tip based on company description"""
    desc = prospect.get('product_description', '').lower()
    
    # Devtools
    if any(word in desc for word in ['dev', 'engineer', 'api', 'testing', 'build', 'platform']):
        return "Your emails lead with architecture and integrations. Engineering buyers still answer to a budget. Open with the ROI, then prove the tech."
    
    # Fintech
    elif any(word in desc for word in ['fintech', 'financial', 'payment', 'security']):
        return "Finance buyers live in a compliance-first world. Email 1 with no social proof reads as risk. Add one client name or a one-line result (e.g., 'We helped Bank X cut reconciliation time by 3 hours/week')."
    
    # HR Tech
    elif any(word in desc for word in ['hr', 'talent', 'onboarding', 'recruiting']):
        return "HR leaders are bought on outcomes that tie to retention or compliance, not features. Open with: 'Most HR teams using [old process] lose 8 hours/week on X.' Then show the fix."
    
    # Martech
    elif any(word in desc for word in ['marketing', 'attribution', 'analytics', 'campaign']):
        return "Marketing buyers have shifted from vanity metrics to revenue attribution. If your email mentions impressions, reach, or engagement — reframe everything around pipeline and closed-won."
    
    # Sales/Revenue tools
    elif any(word in desc for word in ['sales', 'revenue', 'crm', 'outbound']):
        return "Most B2B cold emails bury the CTA at the bottom after three paragraphs of context. Move your ask to line 3. Response rates typically jump 20–35%."
    
    # Support/Operations
    elif any(word in desc for word in ['support', 'customer', 'operations', 'workflow']):
        return "Your email is trying to explain the entire product in 150 words. Operations buyers need one sharp insight: 'Your team is spending 10 hours/week on [X] — here's a 2-minute fix.'"
    
    # Default
    else:
        return "Your subject line is too generic ('Improve your [X]'). B2B founders get 50 of these per day. Try something specific: '[Company name]'s emails have a 12% response rate — here's why that's low.'"

def personalize_email(prospect):
    """Generate personalized email for prospect"""
    first_name = prospect['name'].split()[0]
    company = prospect['company']
    hook = get_hook_for_prospect(prospect)
    tip = get_tip_for_prospect(prospect)
    
    subject = f"{first_name}, quick cold email feedback?"
    
    body = f"""Hi {first_name},

{hook}.

I help B2B SaaS founders improve cold email response rates — and I spotted a quick win for {company}:

{tip}

Want a free 15-min teardown of your current emails? I'll find 3 more fixes like this.

→ https://calendly.com/coldemailteardown

Best,
Nuno"""
    
    return subject, body

def main():
    """Main execution"""
    print("\n" + "="*60)
    print("COLD EMAIL CAMPAIGN LAUNCHER")
    print("="*60 + "\n")
    
    # LOCK FILE CHECK - Prevent parallel campaigns
    lock_file = Path(__file__).parent / 'campaign.lock'
    if lock_file.exists():
        # Check if the PID in lock file is still running
        try:
            with open(lock_file, 'r') as f:
                lock_pid = int(f.read().strip())
            
            # Check if process is still running
            import signal
            try:
                os.kill(lock_pid, 0)  # Doesn't actually kill, just checks if exists
                print(f"❌ Campaign already running (PID: {lock_pid})")
                print(f"   Lock file: {lock_file}")
                print(f"   If the previous campaign crashed, delete the lock file manually.")
                return 1
            except OSError:
                # Process doesn't exist, stale lock file
                print(f"⚠️  Stale lock file found (PID {lock_pid} not running). Removing...")
                lock_file.unlink()
        except Exception as e:
            print(f"⚠️  Error checking lock file: {e}. Removing...")
            lock_file.unlink()
    
    # Create lock file
    try:
        with open(lock_file, 'w') as f:
            f.write(str(os.getpid()))
        print(f"🔒 Campaign lock created (PID: {os.getpid()})\n")
    except Exception as e:
        print(f"❌ Failed to create lock file: {e}")
        return 1
    
    # Load environment
    env_path = Path(__file__).parent / 'automation' / '.env'
    if env_path.exists():
        os.system(f'source {env_path}')
    
    # Initialize email sender
    try:
        sender = EmailSender()
        print("✅ SendGrid initialized")
    except Exception as e:
        print(f"❌ Failed to initialize SendGrid: {e}")
        return 1
    
    # Load prospects
    prospects_path = Path(__file__).parent / 'prospects.csv'
    if not prospects_path.exists():
        print(f"❌ prospects.csv not found at {prospects_path}")
        return 1
    
    prospects = load_prospects(prospects_path)
    print(f"✅ Loaded {len(prospects)} prospects from CSV")
    
    # Send emails
    results = []
    success_count = 0
    fail_count = 0
    
    print(f"\n📧 Sending personalized emails to first {len(prospects)} prospects...\n")
    
    for i, prospect in enumerate(prospects, 1):
        try:
            name = prospect['name']
            email = prospect['email']
            company = prospect['company']
            
            # Personalize
            subject, body = personalize_email(prospect)
            
            print(f"[{i}/{len(prospects)}] {name} ({company})")
            print(f"    To: {email}")
            print(f"    Subject: {subject}")
            
            # Send
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
                    'prospect': name,
                    'email': email,
                    'company': company,
                    'status': 'sent',
                    'sent_at': datetime.now().isoformat()
                })
            else:
                error = result.get('error', 'Unknown error')
                print(f"    ❌ FAILED: {error}\n")
                fail_count += 1
                results.append({
                    'prospect': name,
                    'email': email,
                    'company': company,
                    'status': 'failed',
                    'error': error,
                    'sent_at': datetime.now().isoformat()
                })
        
        except Exception as e:
            print(f"    ❌ ERROR: {e}\n")
            fail_count += 1
            results.append({
                'prospect': prospect.get('name', 'Unknown'),
                'email': prospect.get('email', 'Unknown'),
                'status': 'error',
                'error': str(e),
                'sent_at': datetime.now().isoformat()
            })
    
    # Summary
    print("="*60)
    print("CAMPAIGN SUMMARY")
    print("="*60)
    print(f"✅ Successfully sent: {success_count}/{len(prospects)}")
    print(f"❌ Failed: {fail_count}/{len(prospects)}")
    print("="*60 + "\n")
    
    # Save results
    results_path = Path(__file__).parent / 'campaign-results.json'
    with open(results_path, 'w') as f:
        json.dump({
            'campaign_date': datetime.now().isoformat(),
            'total_prospects': len(prospects),
            'sent': success_count,
            'failed': fail_count,
            'results': results
        }, f, indent=2)
    
    print(f"📊 Results saved to {results_path}")
    
    # Update task log
    task_log_path = Path(__file__).parent / 'task-log.md'
    with open(task_log_path, 'a') as f:
        f.write(f"\n## [{datetime.now().strftime('%Y-%m-%d %H:%M')}] First Campaign Launch\n\n")
        f.write(f"**Agent:** Project Agent (b2b-cold-email-consulting)  \n")
        f.write(f"**Task:** Send first batch of personalized cold emails  \n")
        f.write(f"**Results:**  \n")
        f.write(f"- Total prospects: {len(prospects)}  \n")
        f.write(f"- Successfully sent: {success_count}  \n")
        f.write(f"- Failed: {fail_count}  \n")
        f.write(f"- Success rate: {(success_count/len(prospects)*100):.1f}%  \n\n")
        f.write(f"**Sent to:**  \n")
        for r in results:
            if r['status'] == 'sent':
                f.write(f"- ✅ {r['prospect']} ({r['company']}) - {r['email']}  \n")
        if fail_count > 0:
            f.write(f"\n**Failed:**  \n")
            for r in results:
                if r['status'] != 'sent':
                    f.write(f"- ❌ {r['prospect']} - {r.get('error', 'Unknown')}  \n")
        f.write(f"\n**Next steps:**  \n")
        f.write(f"- Monitor inbox for replies over next 48 hours  \n")
        f.write(f"- Follow up with Email 2 on Day 3 for non-responders  \n")
        f.write(f"- Track open rates in SendGrid dashboard  \n")
        f.write(f"- Prepare call scripts for any replies  \n\n")
        f.write("---\n")
    
    print(f"📝 Task log updated at {task_log_path}\n")
    
    # Remove lock file
    try:
        lock_file.unlink()
        print(f"🔓 Campaign lock removed\n")
    except Exception as e:
        print(f"⚠️  Failed to remove lock file: {e}")
    
    return 0 if fail_count == 0 else 1

if __name__ == '__main__':
    sys.exit(main())
