/**
 * telegram-god.ts
 * 
 * Telegram integration for the God Agent ecosystem.
 * Allows the human to manage projects via Telegram messages.
 * 
 * Setup:
 * 1. Create a Telegram bot via @BotFather
 * 2. Get your bot token
 * 3. Add to .env: TELEGRAM_BOT_TOKEN=your_token_here
 * 4. Add to .env: TELEGRAM_CHAT_ID=your_chat_id
 * 
 * Usage:
 * - God agent checks for messages at start of each session
 * - God agent sends updates after major actions (spawn, kill, evaluate)
 * - Human sends commands via Telegram (checked on next heartbeat)
 */

import { Extension } from "@mariozechner/pi-coding-agent";
import * as fs from "fs";
import * as path from "path";

interface TelegramMessage {
    message_id: number;
    date: number;
    text?: string;
    from?: {
        id: number;
        username?: string;
    };
}

interface TelegramUpdate {
    update_id: number;
    message?: TelegramMessage;
}

const TELEGRAM_API = "https://api.telegram.org/bot";
const REPO_ROOT = process.cwd();
const TELEGRAM_STATE_FILE = path.join(REPO_ROOT, ".pi", "telegram-state.json");

function loadEnv(): { botToken?: string; chatId?: string } {
    const envPath = path.join(REPO_ROOT, ".env");
    if (!fs.existsSync(envPath)) return {};
    
    const envContent = fs.readFileSync(envPath, "utf8");
    const botToken = envContent.match(/TELEGRAM_BOT_TOKEN=(.+)/)?.[1]?.trim();
    const chatId = envContent.match(/TELEGRAM_CHAT_ID=(.+)/)?.[1]?.trim();
    
    return { botToken, chatId };
}

function loadState(): { last_update_id: number } {
    if (!fs.existsSync(TELEGRAM_STATE_FILE)) {
        return { last_update_id: 0 };
    }
    return JSON.parse(fs.readFileSync(TELEGRAM_STATE_FILE, "utf8"));
}

function saveState(state: { last_update_id: number }) {
    const dir = path.dirname(TELEGRAM_STATE_FILE);
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(TELEGRAM_STATE_FILE, JSON.stringify(state, null, 2));
}

async function sendTelegramMessage(text: string): Promise<{ success: boolean; error?: string }> {
    const { botToken, chatId } = loadEnv();
    
    if (!botToken || !chatId) {
        return { 
            success: false, 
            error: "Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID in .env" 
        };
    }
    
    try {
        const url = `${TELEGRAM_API}${botToken}/sendMessage`;
        const response = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                chat_id: chatId,
                text: text,
                parse_mode: "Markdown",
            }),
        });
        
        if (!response.ok) {
            const error = await response.text();
            return { success: false, error: `Telegram API error: ${error}` };
        }
        
        return { success: true };
    } catch (err) {
        return { success: false, error: String(err) };
    }
}

async function checkTelegramMessages(): Promise<string[]> {
    const { botToken, chatId } = loadEnv();
    
    if (!botToken || !chatId) {
        return [];
    }
    
    try {
        const state = loadState();
        const url = `${TELEGRAM_API}${botToken}/getUpdates?offset=${state.last_update_id + 1}&timeout=0`;
        const response = await fetch(url);
        
        if (!response.ok) {
            return [];
        }
        
        const data = await response.json() as { ok: boolean; result: TelegramUpdate[] };
        if (!data.ok || !data.result.length) {
            return [];
        }
        
        const messages: string[] = [];
        let maxUpdateId = state.last_update_id;
        
        for (const update of data.result) {
            if (update.message?.from?.id?.toString() === chatId && update.message.text) {
                messages.push(update.message.text);
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
        return [];
    }
}

export default {
    name: "telegram-god",
    description: "Telegram integration for Darwin God Agent ecosystem management",
    
    tools: [
        {
            name: "telegram_send",
            description: "Send a message to the human via Telegram. Use for important updates: project spawned, project killed, evaluation complete, critical blockers. Keep messages concise.",
            input_schema: {
                type: "object",
                properties: {
                    message: {
                        type: "string",
                        description: "Message text (supports Markdown formatting)",
                    },
                },
                required: ["message"],
            },
            async execute(args: { message: string }) {
                const result = await sendTelegramMessage(args.message);
                if (!result.success) {
                    return `❌ Failed to send Telegram message: ${result.error}\n\nTo enable Telegram:\n1. Create bot via @BotFather\n2. Add TELEGRAM_BOT_TOKEN to .env\n3. Add TELEGRAM_CHAT_ID to .env (your Telegram user ID)`;
                }
                return `✅ Message sent to human via Telegram`;
            },
        },
        {
            name: "telegram_check",
            description: "Check for new messages from the human via Telegram. Returns list of unread messages. Call this at the start of God Agent sessions to check for human commands.",
            input_schema: {
                type: "object",
                properties: {},
            },
            async execute() {
                const messages = await checkTelegramMessages();
                
                if (messages.length === 0) {
                    return "No new Telegram messages from human";
                }
                
                return `📬 ${messages.length} new message(s) from human:\n\n${messages.map((m, i) => `${i + 1}. ${m}`).join("\n\n")}\n\nProcess these commands and act accordingly.`;
            },
        },
    ],
} satisfies Extension;
