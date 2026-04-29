#!/usr/bin/env python3
"""
Email verification script - checks MX records and basic validity
"""
import csv
import subprocess
import re
from collections import defaultdict

def extract_domain(email):
    """Extract domain from email address"""
    return email.split('@')[1] if '@' in email else None

def check_mx_records(domain):
    """Check if domain has valid MX records"""
    try:
        result = subprocess.run(['dig', '+short', 'MX', domain], 
                              capture_output=True, text=True, timeout=5)
        mx_records = result.stdout.strip()
        return bool(mx_records), mx_records
    except Exception as e:
        return False, str(e)

def validate_email_format(email):
    """Basic regex check for email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

# Read prospects
with open('prospects.csv', 'r') as f:
    reader = csv.DictReader(f)
    prospects = list(reader)

print("=== EMAIL VERIFICATION REPORT ===\n")
print(f"Total prospects: {len(prospects)}\n")

verified = []
failed = []
domain_mx_cache = {}

for i, prospect in enumerate(prospects, 1):
    name = prospect['name']
    email = prospect['email']
    company = prospect['company']
    
    print(f"\n{i}. {name} ({company})")
    print(f"   Email: {email}")
    
    # Format check
    if not validate_email_format(email):
        print("   ❌ INVALID format")
        failed.append({**prospect, 'verification_status': 'invalid_format', 'mx_valid': False})
        continue
    
    # MX check
    domain = extract_domain(email)
    if domain not in domain_mx_cache:
        has_mx, mx_records = check_mx_records(domain)
        domain_mx_cache[domain] = (has_mx, mx_records)
    else:
        has_mx, mx_records = domain_mx_cache[domain]
    
    if has_mx:
        print(f"   ✅ Domain valid (MX: {mx_records.split()[0] if mx_records else 'found'})")
        verified.append({**prospect, 'verification_status': 'mx_valid', 'mx_valid': True})
    else:
        print(f"   ❌ No MX records (domain may not accept email)")
        failed.append({**prospect, 'verification_status': 'no_mx', 'mx_valid': False})

print("\n\n=== SUMMARY ===")
print(f"✅ MX-verified emails: {len(verified)}/{len(prospects)}")
print(f"❌ Failed verification: {len(failed)}/{len(prospects)}")
print(f"\n🎯 Usable send list: {len(verified)} prospects")

# Save verified list
with open('prospects-verified.csv', 'w', newline='') as f:
    if verified:
        writer = csv.DictWriter(f, fieldnames=list(verified[0].keys()))
        writer.writeheader()
        writer.writerows(verified)
print(f"\n✅ Verified list saved to: prospects-verified.csv")

# Save failed list for manual review
with open('prospects-failed.csv', 'w', newline='') as f:
    if failed:
        writer = csv.DictWriter(f, fieldnames=list(failed[0].keys()))
        writer.writeheader()
        writer.writerows(failed)
print(f"❌ Failed list saved to: prospects-failed.csv")

print("\n=== RECOMMENDATIONS ===")
if len(verified) < 30:
    print("⚠️  Less than 30 verified emails - consider:")
    print("   1. Manual verification of failed emails")
    print("   2. Hunter.io bulk verification (free tier: 50/month)")
    print("   3. Find alternative email addresses for failed prospects")

if len(verified) >= 20:
    print("✅ You have enough verified emails to launch a meaningful campaign")
    print(f"   Expected results from {len(verified)} sends:")
    print(f"   - 10% reply rate = ~{int(len(verified) * 0.1)} replies")
    print(f"   - 40% conversion = ~{int(len(verified) * 0.1 * 0.4)} paid sessions")
    print(f"   - Revenue estimate: ${int(len(verified) * 0.1 * 0.4 * 200)}")
