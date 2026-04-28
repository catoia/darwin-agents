#!/bin/bash
# Cron scheduler for automated follow-ups
# Add to crontab: 0 9 * * * /path/to/scheduler.sh

set -e

# Change to project directory
cd "$(dirname "$0")/.."

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Run follow-up checker
echo "$(date): Running follow-up checker..." >> automation/scheduler.log
python3 automation/orchestrator.py followups >> automation/scheduler.log 2>&1

echo "$(date): Follow-up check complete" >> automation/scheduler.log
