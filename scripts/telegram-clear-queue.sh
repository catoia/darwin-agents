#!/bin/bash
# Clear all pending Telegram messages without processing them
# Use this when you want to start fresh and ignore old messages

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

cd "$REPO_ROOT"

echo "🧹 Clearing Telegram message queue..."

node << 'EOFNODE'
const fs = require('fs');
const path = require('path');

const REPO_ROOT = process.cwd();
const STATE_FILE = path.join(REPO_ROOT, '.pi', 'telegram-state.json');

const envContent = fs.readFileSync('.env', 'utf8');
const botToken = envContent.match(/TELEGRAM_BOT_TOKEN=(.+)/)?.[1]?.trim();

if (!botToken) {
    console.error('❌ TELEGRAM_BOT_TOKEN not found in .env');
    process.exit(1);
}

fetch(`https://api.telegram.org/bot${botToken}/getUpdates?offset=-1`)
  .then(r => r.json())
  .then(data => {
    if (!data.ok) {
      console.error('❌ Failed to fetch updates:', data.description);
      process.exit(1);
    }
    
    const messageCount = data.result.length;
    
    if (messageCount === 0) {
      console.log('✅ Queue is already empty');
      return;
    }
    
    // Find the highest update_id
    const maxUpdateId = Math.max(...data.result.map(u => u.update_id));
    
    // Save it to state (marks all as processed)
    const dir = path.dirname(STATE_FILE);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(STATE_FILE, JSON.stringify({ last_update_id: maxUpdateId }, null, 2));
    
    console.log(`✅ Cleared ${messageCount} old message(s) from queue`);
    console.log(`   New messages will be processed starting from update_id: ${maxUpdateId + 1}`);
  })
  .catch(err => {
    console.error('❌ Error:', err.message);
    process.exit(1);
  });
EOFNODE
