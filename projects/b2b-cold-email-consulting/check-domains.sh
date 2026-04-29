#!/bin/bash
# Quick domain MX record check for the 10 prospects

echo "🔍 Checking MX records for the 10 email domains..."
echo ""

domains=(
  "screendesk.io"
  "buildbuddy.io"
  "clarityhq.com"
  "flowtest.dev"
  "revenueops.ai"
  "talentgrid.io"
  "secureapi.dev"
  "marketpulse.io"
  "devplatform.io"
  "bizflow.ai"
)

valid=0
invalid=0

for domain in "${domains[@]}"; do
  echo -n "Checking $domain... "
  
  mx_records=$(dig +short MX "$domain" 2>/dev/null)
  
  if [ -z "$mx_records" ]; then
    echo "❌ NO MX RECORDS (email will bounce)"
    ((invalid++))
  else
    echo "✅ Valid mail server"
    ((valid++))
  fi
done

echo ""
echo "📊 Summary:"
echo "  ✅ Valid domains (have MX records): $valid"
echo "  ❌ Invalid domains (no MX records): $invalid"
echo ""

if [ $invalid -gt 0 ]; then
  echo "⚠️  $invalid domains will definitely bounce (no mail server)."
  echo "   This confirms pattern-guessed emails are unreliable."
fi

if [ $valid -eq 10 ]; then
  echo "✅ All domains have mail servers."
  echo "   Bounces might be due to invalid mailbox names (firstname@)."
  echo "   Email verification (Hunter.io) is still needed."
fi
