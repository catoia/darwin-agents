#!/bin/bash
# Quick setup script for the automation system

set -e

echo "🚀 Setting up B2B Cold Email Automation System..."
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required. Please install it first."
    exit 1
fi

# Create virtual environment
echo "📦 Creating virtual environment..."
cd automation
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies..."
pip install -q --upgrade pip
pip install -q -r requirements.txt

echo ""
echo "✅ Dependencies installed"
echo ""

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating template..."
    cat > .env << 'EOF'
# SendGrid (required for sending emails)
export SENDGRID_API_KEY="YOUR_SENDGRID_API_KEY"

# OpenAI (required for email personalization)
export OPENAI_API_KEY="YOUR_OPENAI_API_KEY"

# Apollo.io (optional - for prospect finding)
export APOLLO_API_KEY="YOUR_APOLLO_API_KEY"

# Hunter.io (optional - for email enrichment)
export HUNTER_API_KEY="YOUR_HUNTER_API_KEY"
EOF
    echo "📝 Created .env template. Please edit automation/.env with your API keys."
    echo ""
fi

# Update config.json with human's email
echo "📝 Configuring campaign..."
echo ""
echo "What email should we send FROM?"
read -p "From email: " from_email
read -p "Your name: " from_name

python3 << EOF
import json
with open('config.json', 'r') as f:
    config = json.load(f)
config['from_email'] = '${from_email}'
config['from_name'] = '${from_name}'
config['reply_to'] = '${from_email}'
with open('config.json', 'w') as f:
    json.dump(config, f, indent=2)
EOF

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit automation/.env with your API keys (SendGrid + OpenAI required)"
echo "2. Run: source automation/.env"
echo "3. Run: python3 automation/orchestrator.py initial 20"
echo ""
echo "See automation/README.md for full documentation."
