#!/usr/bin/env bash
# scripts/fetch-metrics.sh <project-id>
#
# Fetches traffic/engagement metrics from Cloudflare Analytics API (GraphQL)
# and merges with any manually-recorded revenue data.
# Writes results to projects/<id>/metrics.json
#
# Required env vars:
#   CLOUDFLARE_API_TOKEN   — CF API token with Analytics:Read permission
#   CLOUDFLARE_ACCOUNT_ID  — your CF account ID
#
# Optional env vars (revenue):
#   ADSENSE_ACCESS_TOKEN + ADSENSE_ACCOUNT_ID  — for AdSense revenue
#   STRIPE_API_KEY                              — for Stripe revenue
#
# If none of the above are set, revenue falls back to projects/<id>/revenue-manual.json

set -euo pipefail

PROJECT_ID="${1:-}"
if [[ -z "$PROJECT_ID" ]]; then
  echo "Usage: $0 <project-id>" >&2
  exit 1
fi

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PROJECT_DIR="$REPO_ROOT/projects/$PROJECT_ID"
METRICS_FILE="$PROJECT_DIR/metrics.json"
REGISTRY_FILE="$REPO_ROOT/registry.json"

if [[ ! -d "$PROJECT_DIR" ]]; then
  echo "Error: project directory not found: $PROJECT_DIR" >&2
  exit 1
fi

# ── Get CF project name from registry ────────────────────────────────────────
CF_PROJECT=$(python3 -c "
import json, sys
reg = json.load(open('$REGISTRY_FILE'))
proj = next((p for p in reg['projects'] if p['id'] == '$PROJECT_ID'), None)
if not proj:
    sys.exit(1)
print(proj.get('cf_project', '$PROJECT_ID'))
" 2>/dev/null || echo "$PROJECT_ID")

NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
SEVEN_DAYS_AGO=$(date -u -v-7d +"%Y-%m-%d" 2>/dev/null || date -u -d "7 days ago" +"%Y-%m-%d")
TODAY=$(date -u +"%Y-%m-%d")

# ── Cloudflare Analytics (traffic + engagement) ───────────────────────────────
UNIQUE_VISITORS=0
AVG_SESSION_SECONDS=0
RETURN_VISITOR_RATE=0
TOP_PAGES="[]"

if [[ -n "${CLOUDFLARE_API_TOKEN:-}" && -n "${CLOUDFLARE_ACCOUNT_ID:-}" ]]; then
  echo "[fetch-metrics] Querying Cloudflare Analytics for $CF_PROJECT..."

  CF_RESPONSE=$(curl -s -X POST \
    "https://api.cloudflare.com/client/v4/graphql" \
    -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
    -H "Content-Type: application/json" \
    --data "{
      \"query\": \"query {
        viewer {
          accounts(filter: {accountTag: \\\"$CLOUDFLARE_ACCOUNT_ID\\\"}) {
            pagesAnalyticsAdaptiveGroups(
              filter: {
                date_geq: \\\"$SEVEN_DAYS_AGO\\\",
                date_leq: \\\"$TODAY\\\",
                projectName: \\\"$CF_PROJECT\\\"
              },
              limit: 10,
              orderBy: [visits_DESC]
            ) {
              dimensions { requestPath }
              sum { visits pageViews }
              uniq { uniques }
            }
          }
        }
      }\"
    }" 2>/dev/null || echo '{"error":"cf_api_failed"}')

  # Parse totals from CF response
  UNIQUE_VISITORS=$(echo "$CF_RESPONSE" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    groups = d['data']['viewer']['accounts'][0]['pagesAnalyticsAdaptiveGroups']
    print(sum(g['uniq']['uniques'] for g in groups))
except Exception as e:
    print(0)
" 2>/dev/null || echo 0)

  TOP_PAGES=$(echo "$CF_RESPONSE" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    groups = d['data']['viewer']['accounts'][0]['pagesAnalyticsAdaptiveGroups']
    pages = [g['dimensions']['requestPath'] for g in groups[:5]]
    print(json.dumps(pages))
except:
    print('[]')
" 2>/dev/null || echo '[]')

  echo "[fetch-metrics] Unique visitors (7d): $UNIQUE_VISITORS"
else
  echo "[fetch-metrics] CLOUDFLARE_API_TOKEN or CLOUDFLARE_ACCOUNT_ID not set — skipping CF analytics."
  echo "[fetch-metrics] To enable: export CLOUDFLARE_API_TOKEN=... CLOUDFLARE_ACCOUNT_ID=..."
fi

# ── Revenue collection ────────────────────────────────────────────────────────
REVENUE_USD=0
REVENUE_SOURCE="none"

# Try Stripe first
if [[ -n "${STRIPE_API_KEY:-}" ]]; then
  echo "[fetch-metrics] Fetching Stripe revenue..."
  SINCE_EPOCH=$(date -v-7d +%s 2>/dev/null || date -d "7 days ago" +%s)
  STRIPE_RESPONSE=$(curl -s \
    "https://api.stripe.com/v1/charges?created[gte]=$SINCE_EPOCH&limit=100" \
    -u "${STRIPE_API_KEY}:" 2>/dev/null || echo '{"data":[]}')
  REVENUE_USD=$(echo "$STRIPE_RESPONSE" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    total = sum(c['amount'] for c in d.get('data',[]) if c.get('paid'))
    print(round(total / 100, 2))
except:
    print(0)
" 2>/dev/null || echo 0)
  REVENUE_SOURCE="stripe"
  echo "[fetch-metrics] Stripe revenue (7d): \$$REVENUE_USD"

# Try AdSense
elif [[ -n "${ADSENSE_ACCESS_TOKEN:-}" && -n "${ADSENSE_ACCOUNT_ID:-}" ]]; then
  echo "[fetch-metrics] Fetching AdSense revenue..."
  ADSENSE_RESPONSE=$(curl -s \
    "https://adsense.googleapis.com/v2/${ADSENSE_ACCOUNT_ID}/reports:generate?dateRange=LAST_7_DAYS&metrics=ESTIMATED_EARNINGS" \
    -H "Authorization: Bearer $ADSENSE_ACCESS_TOKEN" 2>/dev/null || echo '{}')
  REVENUE_USD=$(echo "$ADSENSE_RESPONSE" | python3 -c "
import json, sys
try:
    d = json.load(sys.stdin)
    print(round(float(d['totals']['cells'][0]['value']), 2))
except:
    print(0)
" 2>/dev/null || echo 0)
  REVENUE_SOURCE="adsense"
  echo "[fetch-metrics] AdSense revenue (7d): \$$REVENUE_USD"

# Fall back to manually recorded revenue file
elif [[ -f "$PROJECT_DIR/revenue-manual.json" ]]; then
  REVENUE_USD=$(python3 -c "
import json
d = json.load(open('$PROJECT_DIR/revenue-manual.json'))
if isinstance(d, list):
    print(round(sum(e.get('revenue_usd',0) for e in d), 2))
else:
    print(round(d.get('revenue_usd', 0), 2))
" 2>/dev/null || echo 0)
  REVENUE_SOURCE="affiliate-manual"
  echo "[fetch-metrics] Manual revenue (from revenue-manual.json): \$$REVENUE_USD"
fi

# ── Write metrics.json ────────────────────────────────────────────────────────
python3 -c "
import json
metrics = {
    'updated_at': '$NOW',
    'period_days': 7,
    'revenue_usd': $REVENUE_USD,
    'revenue_source': '$REVENUE_SOURCE',
    'unique_visitors': $UNIQUE_VISITORS,
    'avg_session_seconds': $AVG_SESSION_SECONDS,
    'return_visitor_rate': $RETURN_VISITOR_RATE,
    'top_pages': $TOP_PAGES,
    'notes': ''
}
# Preserve existing notes if any
try:
    existing = json.load(open('$METRICS_FILE'))
    metrics['notes'] = existing.get('notes', '')
except:
    pass
with open('$METRICS_FILE', 'w') as f:
    json.dump(metrics, f, indent=2)
print('[fetch-metrics] Written: $METRICS_FILE')
"

echo "[fetch-metrics] Done for project: $PROJECT_ID"
