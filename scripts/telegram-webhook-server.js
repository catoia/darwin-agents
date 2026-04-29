#!/usr/bin/env node
/**
 * telegram-webhook-server.js
 * 
 * Local Express server that receives Telegram webhooks instantly.
 * No polling, no delays - messages arrive in <1 second.
 * 
 * How it works:
 * 1. Run this server locally (node scripts/telegram-webhook-server.js)
 * 2. Expose it with cloudflared/ngrok to get a public URL
 * 3. Configure Telegram bot to POST to that URL
 * 4. When you send a message, Telegram POSTs here instantly
 * 5. Server spawns God Agent to process it
 * 
 * Zero cost, instant delivery, no background polling.
 */

const express = require('express');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(express.json());

const REPO_ROOT = path.resolve(__dirname, '..');
const PORT = process.env.TELEGRAM_WEBHOOK_PORT || 3737;

function loadEnv() {
    const envPath = path.join(REPO_ROOT, '.env');
    if (!fs.existsSync(envPath)) return {};
    
    const envContent = fs.readFileSync(envPath, 'utf8');
    const botToken = envContent.match(/TELEGRAM_BOT_TOKEN=(.+)/)?.[1]?.trim();
    const chatId = envContent.match(/TELEGRAM_CHAT_ID=(.+)/)?.[1]?.trim();
    
    return { botToken, chatId };
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
    const { chatId } = loadEnv();
    
    try {
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
        
        // Validate it's from the authorized chat
        if (chatId && messageChatId !== chatId) {
            log(`Ignored: unauthorized chat ${messageChatId}`);
            return res.sendStatus(200);
        }

        // Respond immediately to Telegram (required within 60s)
        res.sendStatus(200);
        
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
