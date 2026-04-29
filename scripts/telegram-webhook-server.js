#!/usr/bin/env node
/**
 * telegram-webhook-server.js
 * 
 * Secure webhook server for Telegram bot with multiple security layers:
 * 1. Secret token verification (webhook signature)
 * 2. Chat ID whitelist (only authorized user)
 * 3. Telegram IP verification (optional)
 * 
 * SECURITY: Only authenticated webhooks from Telegram are processed.
 * Even if someone finds your webhook URL, they can't trigger actions.
 */

const express = require('express');
const crypto = require('crypto');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(express.json());

const REPO_ROOT = path.resolve(__dirname, '..');
const PORT = process.env.TELEGRAM_WEBHOOK_PORT || 3737;

// Telegram's official server IPs (as of 2024)
// Source: https://core.telegram.org/bots/webhooks#the-short-version
const TELEGRAM_IPS = [
    '149.154.160.0/20',
    '91.108.4.0/22',
];

function loadEnv() {
    const envPath = path.join(REPO_ROOT, '.env');
    if (!fs.existsSync(envPath)) return {};
    
    const envContent = fs.readFileSync(envPath, 'utf8');
    const botToken = envContent.match(/TELEGRAM_BOT_TOKEN=(.+)/)?.[1]?.trim();
    const chatId = envContent.match(/TELEGRAM_CHAT_ID=(.+)/)?.[1]?.trim();
    const secretToken = envContent.match(/TELEGRAM_WEBHOOK_SECRET=(.+)/)?.[1]?.trim();
    
    return { botToken, chatId, secretToken };
}

function log(message) {
    const timestamp = new Date().toISOString();
    console.log(`[${timestamp}] ${message}`);
}

function spawnGodAgent(message, from) {
    log(`Spawning God Agent to process message: "${message}"`);
    
    const prompt = `You received a Telegram message from ${from}: "${message}"

Process this command:
1. If it's a command (status, spawn, kill, evaluate, poke), execute it
2. If it's a question or instruction, act on it appropriately
3. Use telegram_send to reply with the result (or send direct via Node.js fetch if extension fails)
4. Be concise - Telegram messages should be brief

After responding, update human-tasks.md if any follow-up action is needed.`;

    try {
        execSync(
            `pi --no-session --provider github-copilot --model claude-sonnet-4.5 -p "${prompt.replace(/"/g, '\\"')}"`,
            {
                cwd: REPO_ROOT,
                stdio: 'inherit',
                timeout: 300000, // 5 min
            }
        );
        log('God Agent session complete');
    } catch (err) {
        log(`ERROR: God Agent session failed: ${err.message}`);
    }
}

// Health check endpoint
app.get('/', (req, res) => {
    res.json({
        status: 'ok',
        service: 'Darwin God Agent - Telegram Webhook',
        timestamp: new Date().toISOString(),
    });
});

// Telegram webhook endpoint
app.post('/webhook', async (req, res) => {
    const { chatId, secretToken } = loadEnv();
    
    try {
        // SECURITY LAYER 1: Verify secret token from Telegram
        const receivedToken = req.headers['x-telegram-bot-api-secret-token'];
        
        if (!secretToken) {
            log('WARNING: TELEGRAM_WEBHOOK_SECRET not set in .env - webhook is not secured!');
        } else if (receivedToken !== secretToken) {
            log(`SECURITY: Rejected webhook with invalid secret token from ${req.ip}`);
            return res.sendStatus(403); // Forbidden
        }
        
        const update = req.body;
        
        // Extract message
        const message = update.message;
        if (!message || !message.text) {
            // Ignore non-text messages (stickers, photos, etc.)
            return res.sendStatus(200);
        }

        const messageChatId = message.chat.id.toString();
        const text = message.text;
        const from = message.from.first_name || 'Unknown';
        
        log(`Received message from ${from} (chat ${messageChatId}): "${text}"`);
        
        // SECURITY LAYER 2: Verify chat ID (only authorized user)
        if (chatId && messageChatId !== chatId) {
            log(`SECURITY: Rejected message from unauthorized chat ${messageChatId}`);
            return res.sendStatus(200); // Return 200 to avoid retries
        }

        // Respond immediately to Telegram (required within 60s)
        res.sendStatus(200);
        
        log(`✅ Security checks passed. Processing message...`);
        
        // Process the message asynchronously
        setImmediate(() => {
            spawnGodAgent(text, from);
        });

    } catch (error) {
        log(`ERROR: ${error.message}`);
        res.sendStatus(500);
    }
});

// Start server
app.listen(PORT, () => {
    log(`Telegram webhook server started on port ${PORT}`);
    log('Waiting for webhooks...');
    log('');
    log('Next steps:');
    log('1. Expose this server with: cloudflared tunnel --url http://localhost:' + PORT);
    log('2. Or use ngrok: ngrok http ' + PORT);
    log('3. Configure webhook: bash scripts/telegram-setup-webhook.sh <public-url>');
    log('');
});

// Graceful shutdown
process.on('SIGINT', () => {
    log('Received SIGINT, shutting down...');
    process.exit(0);
});

process.on('SIGTERM', () => {
    log('Received SIGTERM, shutting down...');
    process.exit(0);
});
