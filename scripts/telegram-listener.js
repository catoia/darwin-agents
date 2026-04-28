#!/usr/bin/env node
/**
 * telegram-listener.js
 * 
 * Lightweight Telegram polling daemon that:
 * - Polls Telegram API every 60 seconds (free, no tokens)
 * - When it detects a new message, spawns a God Agent session to process it
 * - Runs continuously in the background
 * - Zero token cost when idle
 * 
 * Usage:
 *   node scripts/telegram-listener.js
 *   
 * To run in background:
 *   nohup node scripts/telegram-listener.js > logs/telegram-listener.log 2>&1 &
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const REPO_ROOT = path.resolve(__dirname, '..');
const STATE_FILE = path.join(REPO_ROOT, '.pi', 'telegram-state.json');
const POLL_INTERVAL = 60000; // 60 seconds

function log(message) {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] ${message}`);
}

function loadEnv() {
    const envPath = path.join(REPO_ROOT, '.env');
    if (!fs.existsSync(envPath)) {
        log('ERROR: .env file not found');
        return {};
    }
    
    const envContent = fs.readFileSync(envPath, 'utf8');
    const botToken = envContent.match(/TELEGRAM_BOT_TOKEN=(.+)/)?.[1]?.trim();
    const chatId = envContent.match(/TELEGRAM_CHAT_ID=(.+)/)?.[1]?.trim();
    
    return { botToken, chatId };
}

function loadState() {
    if (!fs.existsSync(STATE_FILE)) {
        return { last_update_id: 0 };
    }
    return JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'));
}

function saveState(state) {
    const dir = path.dirname(STATE_FILE);
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));
}

async function checkForMessages() {
    const { botToken, chatId } = loadEnv();
    
    if (!botToken || !chatId) {
        log('ERROR: Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in .env');
        return [];
    }
    
    try {
        const state = loadState();
        const url = `https://api.telegram.org/bot${botToken}/getUpdates?offset=${state.last_update_id + 1}&timeout=0`;
        const response = await fetch(url);
        
        if (!response.ok) {
            log(`ERROR: Telegram API returned ${response.status}`);
            return [];
        }
        
        const data = await response.json();
        if (!data.ok || !data.result.length) {
            return [];
        }
        
        const messages = [];
        let maxUpdateId = state.last_update_id;
        
        for (const update of data.result) {
            if (update.message?.from?.id?.toString() === chatId && update.message.text) {
                messages.push({
                    text: update.message.text,
                    from: update.message.from.first_name,
                    date: new Date(update.message.date * 1000).toISOString(),
                });
            }
            if (update.update_id > maxUpdateId) {
                maxUpdateId = update.update_id;
            }
        }
        
        if (maxUpdateId > state.last_update_id) {
            saveState({ last_update_id: maxUpdateId });
        }
        
        return messages;
    } catch (err) {
        log(`ERROR: ${err.message}`);
        return [];
    }
}

async function spawnGodAgent(messages) {
    log(`Spawning God Agent to process ${messages.length} message(s)...`);
    
    const messageText = messages.map((m, i) => 
        `${i + 1}. [${m.date}] ${m.from}: "${m.text}"`
    ).join('\n');
    
    const prompt = `You received ${messages.length} message(s) from human via Telegram:

${messageText}

Process these commands:
1. If it's a command (status, spawn, kill, evaluate, poke), execute it
2. If it's a question or instruction, act on it appropriately
3. Use telegram_send to reply with the result
4. Be concise - Telegram messages should be brief

After responding, update human-tasks.md if any follow-up action is needed.`;

    try {
        // Spawn pi session for God Agent (reads AGENTS.md automatically)
        execSync(
            `pi --no-session --provider github-copilot --model claude-sonnet-4.5 -p "${prompt.replace(/"/g, '\\"')}"`,
            {
                cwd: REPO_ROOT,
                stdio: 'inherit',
                timeout: 300000, // 5 min timeout
            }
        );
        log('God Agent session complete');
    } catch (err) {
        log(`ERROR: God Agent session failed: ${err.message}`);
    }
}

async function poll() {
    log('Checking for new Telegram messages...');
    
    const messages = await checkForMessages();
    
    if (messages.length === 0) {
        log('No new messages');
    } else {
        log(`Found ${messages.length} new message(s)`);
        await spawnGodAgent(messages);
    }
}

async function main() {
    log('Telegram Listener started');
    log(`Polling interval: ${POLL_INTERVAL / 1000} seconds`);
    log('Press Ctrl+C to stop');
    log('');
    
    // Initial check
    await poll();
    
    // Poll every 60 seconds
    setInterval(poll, POLL_INTERVAL);
}

// Handle graceful shutdown
process.on('SIGINT', () => {
    log('Received SIGINT, shutting down gracefully...');
    process.exit(0);
});

process.on('SIGTERM', () => {
    log('Received SIGTERM, shutting down gracefully...');
    process.exit(0);
});

main().catch(err => {
    log(`FATAL: ${err.message}`);
    process.exit(1);
});
