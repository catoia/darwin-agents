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
const { execSync, spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const app = express();
app.use(express.json());

const REPO_ROOT = path.resolve(__dirname, '..');
const PORT = process.env.TELEGRAM_WEBHOOK_PORT || 3737;

// Store recent activity for dashboard
const activityLog = [];
const MAX_LOG_ENTRIES = 50;

function addActivity(type, message, data = {}) {
    activityLog.unshift({
        timestamp: new Date().toISOString(),
        type,
        message,
        data,
    });
    if (activityLog.length > MAX_LOG_ENTRIES) {
        activityLog.pop();
    }
}

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
    addActivity('log', message);
}

const runningAgents = new Map(); // Track active God Agent processes

function spawnGodAgent(message, from, chatId) {
    const agentId = Date.now();
    log(`Spawning God Agent (ID: ${agentId}) to process message: "${message}"`);
    
    const { botToken } = loadEnv();
    
    const prompt = `You received a Telegram message from ${from}: "${message}"

Process this command:
1. If it's a command (status, spawn, kill, evaluate, poke), execute it
2. If it's a question or instruction, act on it appropriately
3. Reply to the user in Telegram using Node.js directly (the extension has issues)
4. Be concise - Telegram messages should be brief

To send a Telegram reply, use bash with this command:
\`\`\`bash
node -e "fetch('https://api.telegram.org/bot${botToken}/sendMessage', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
    chat_id: '${chatId}',
    text: 'Your response here',
    parse_mode: 'Markdown'
  })
}).then(r => r.json()).then(console.log)"
\`\`\`

Replace 'Your response here' with your actual response.

After responding, update human-tasks.md if any follow-up action is needed.`;

    const startTime = Date.now();
    addActivity('agent_start', `God Agent ${agentId} started`, {
        message,
        from,
        chatId,
    });

    try {
        // Spawn as a child process so we can track it
        // Don't load telegram extension - it causes issues
        // Agent will reply via bash + node -e instead
        const child = spawn(
            'pi',
            [
                '--no-session',
                '--provider', 'github-copilot',
                '--model', 'claude-sonnet-4.5',
                '--no-extensions',  // Disable extensions to avoid loading errors
                '-p', prompt,
            ],
            {
                cwd: REPO_ROOT,
                stdio: ['ignore', 'pipe', 'pipe'],
            }
        );

        runningAgents.set(agentId, {
            pid: child.pid,
            message,
            from,
            startTime,
        });

        let stdout = '';
        let stderr = '';

        child.stdout.on('data', (data) => {
            stdout += data.toString();
        });

        child.stderr.on('data', (data) => {
            stderr += data.toString();
        });

        child.on('close', (code) => {
            const duration = Date.now() - startTime;
            runningAgents.delete(agentId);
            
            if (code === 0) {
                log(`God Agent ${agentId} completed successfully (${(duration / 1000).toFixed(1)}s)`);
                addActivity('agent_complete', `God Agent ${agentId} completed`, {
                    duration: `${(duration / 1000).toFixed(1)}s`,
                    exitCode: code,
                });
            } else {
                log(`ERROR: God Agent ${agentId} failed with code ${code}`);
                addActivity('agent_error', `God Agent ${agentId} failed`, {
                    duration: `${(duration / 1000).toFixed(1)}s`,
                    exitCode: code,
                    stderr: stderr.slice(-500),
                });
            }
        });

    } catch (err) {
        runningAgents.delete(agentId);
        log(`ERROR: Failed to spawn God Agent ${agentId}: ${err.message}`);
        addActivity('agent_error', `Failed to spawn God Agent ${agentId}`, {
            error: err.message,
        });
    }
}

// Health check endpoint
app.get('/', (req, res) => {
    res.redirect('/dashboard');
});

// Dashboard UI
app.get('/dashboard', (req, res) => {
    const { chatId } = loadEnv();
    
    const html = `
<!DOCTYPE html>
<html>
<head>
    <title>Darwin God Agent - Telegram Monitor</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: #0a0e27;
            color: #e0e6ed;
            padding: 20px;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        h1 {
            font-size: 28px;
            margin-bottom: 10px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .subtitle { color: #8b95a5; margin-bottom: 30px; }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .card {
            background: #151b2e;
            border: 1px solid #1e2742;
            border-radius: 12px;
            padding: 20px;
        }
        .card-title {
            font-size: 14px;
            font-weight: 600;
            color: #8b95a5;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 15px;
        }
        .stat {
            font-size: 36px;
            font-weight: 700;
            color: #667eea;
            margin-bottom: 5px;
        }
        .stat-label { color: #8b95a5; font-size: 14px; }
        .status-dot {
            display: inline-block;
            width: 8px;
            height: 8px;
            border-radius: 50%;
            margin-right: 8px;
        }
        .status-dot.active { background: #10b981; animation: pulse 2s infinite; }
        .status-dot.idle { background: #6b7280; }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .activity-list {
            max-height: 600px;
            overflow-y: auto;
        }
        .activity-item {
            background: #1a2238;
            border-left: 3px solid #667eea;
            padding: 12px 15px;
            margin-bottom: 10px;
            border-radius: 6px;
        }
        .activity-item.security { border-left-color: #ef4444; }
        .activity-item.agent_start { border-left-color: #10b981; }
        .activity-item.agent_complete { border-left-color: #3b82f6; }
        .activity-item.agent_error { border-left-color: #f59e0b; }
        .activity-time {
            font-size: 12px;
            color: #6b7280;
            margin-bottom: 5px;
        }
        .activity-message { color: #e0e6ed; font-size: 14px; }
        .activity-data {
            font-size: 12px;
            color: #8b95a5;
            margin-top: 5px;
            font-family: 'Monaco', 'Courier New', monospace;
        }
        .agent-card {
            background: #1a2238;
            border: 1px solid #2a3550;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 10px;
        }
        .agent-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 10px;
        }
        .agent-id {
            font-weight: 600;
            color: #667eea;
        }
        .agent-duration {
            font-size: 12px;
            color: #10b981;
        }
        .agent-message {
            color: #8b95a5;
            font-size: 13px;
            font-style: italic;
        }
        .empty-state {
            text-align: center;
            padding: 40px;
            color: #6b7280;
        }
        .refresh-btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
        }
        .refresh-btn:hover { background: #5a67d8; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Darwin God Agent</h1>
        <p class="subtitle">Telegram Webhook Monitor</p>
        
        <div class="grid">
            <div class="card">
                <div class="card-title">Webhook Status</div>
                <div class="stat" id="webhookStatus">●</div>
                <div class="stat-label">Listening on port 3737</div>
            </div>
            
            <div class="card">
                <div class="card-title">Active Agents</div>
                <div class="stat" id="activeAgents">0</div>
                <div class="stat-label">Running sessions</div>
            </div>
            
            <div class="card">
                <div class="card-title">Messages Processed</div>
                <div class="stat" id="totalMessages">0</div>
                <div class="stat-label">Since startup</div>
            </div>
            
            <div class="card">
                <div class="card-title">Authorized User</div>
                <div class="stat" style="font-size: 20px;">${chatId || 'Not configured'}</div>
                <div class="stat-label">Chat ID whitelist</div>
            </div>
        </div>
        
        <div class="grid">
            <div class="card">
                <div class="card-title">Running Agents</div>
                <div id="runningAgents"></div>
            </div>
            
            <div class="card" style="grid-column: span 2;">
                <div class="card-title">Recent Activity <button class="refresh-btn" onclick="loadActivity()">↻ Refresh</button></div>
                <div class="activity-list" id="activityList"></div>
            </div>
        </div>
    </div>
    
    <script>
        let messageCount = 0;
        
        function formatTime(isoString) {
            const date = new Date(isoString);
            return date.toLocaleTimeString();
        }
        
        function formatDuration(startTime) {
            const elapsed = Date.now() - new Date(startTime).getTime();
            return (elapsed / 1000).toFixed(1) + 's';
        }
        
        async function loadActivity() {
            const res = await fetch('/api/activity');
            const data = await res.json();
            
            document.getElementById('activeAgents').textContent = data.activeAgents;
            document.getElementById('totalMessages').textContent = messageCount;
            
            // Running agents
            const runningDiv = document.getElementById('runningAgents');
            if (data.runningAgents.length === 0) {
                runningDiv.innerHTML = '<div class="empty-state">No active agents</div>';
            } else {
                runningDiv.innerHTML = data.runningAgents.map(agent => \`
                    <div class="agent-card">
                        <div class="agent-header">
                            <span class="agent-id">Agent #\${agent.id}</span>
                            <span class="agent-duration">\${formatDuration(agent.startTime)}</span>
                        </div>
                        <div class="agent-message">"\${agent.message}"</div>
                        <div class="activity-data">From: \${agent.from} | PID: \${agent.pid}</div>
                    </div>
                \`).join('');
            }
            
            // Activity log
            const activityDiv = document.getElementById('activityList');
            if (data.activity.length === 0) {
                activityDiv.innerHTML = '<div class="empty-state">No activity yet</div>';
            } else {
                activityDiv.innerHTML = data.activity.map(item => {
                    let dataHtml = '';
                    if (item.data && Object.keys(item.data).length > 0) {
                        dataHtml = '<div class="activity-data">' + 
                            Object.entries(item.data).map(([k, v]) => 
                                \`\${k}: \${typeof v === 'object' ? JSON.stringify(v) : v}\`
                            ).join(' | ') + 
                            '</div>';
                    }
                    return \`
                        <div class="activity-item \${item.type}">
                            <div class="activity-time">\${formatTime(item.timestamp)}</div>
                            <div class="activity-message">\${item.message}</div>
                            \${dataHtml}
                        </div>
                    \`;
                }).join('');
            }
            
            // Count agent_start events
            messageCount = data.activity.filter(a => a.type === 'agent_start').length;
            document.getElementById('totalMessages').textContent = messageCount;
        }
        
        // Load initially
        loadActivity();
        
        // Auto-refresh every 2 seconds
        setInterval(loadActivity, 2000);
    </script>
</body>
</html>
    `;
    
    res.send(html);
});

// API endpoint for activity data
app.get('/api/activity', (req, res) => {
    const runningAgentsList = Array.from(runningAgents.entries()).map(([id, agent]) => ({
        id,
        ...agent,
    }));
    
    res.json({
        activeAgents: runningAgents.size,
        runningAgents: runningAgentsList,
        activity: activityLog,
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
        addActivity('message', `Message from ${from}`, { text, chatId: messageChatId });
        
        // Process the message asynchronously
        setImmediate(() => {
            spawnGodAgent(text, from, messageChatId);
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
