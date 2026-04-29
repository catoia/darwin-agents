#!/bin/bash
# Wrapper to run verified campaign with proper venv

cd /Users/nunocadete/darwin-agents/projects/b2b-cold-email-consulting

# Load env vars
source automation/.env

# Activate venv
source automation/venv/bin/activate

# Run with venv python
exec python3 send-verified-campaign.py
