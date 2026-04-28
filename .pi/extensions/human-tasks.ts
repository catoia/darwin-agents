/**
 * human-tasks extension
 *
 * Registers a `human_task` tool available to ALL pi agents in this project.
 * When an agent calls it, the task is appended to human-tasks.md with a
 * unique ID, timestamp, priority, and context. The agent can continue working
 * without blocking.
 *
 * Place at: .pi/extensions/human-tasks.ts
 */

import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import * as fs from "fs";
import * as path from "path";
import * as crypto from "crypto";

export default function (pi: ExtensionAPI) {
    const repoRoot = findRepoRoot(process.cwd());
    const tasksFile = path.join(repoRoot, "human-tasks.md");

    pi.registerTool({
        name: "human_task",
        description:
            "Queue a task or question for the human owner. Use this when you need human judgment, approval, credentials, or want to flag something important. You do NOT need to wait for a response — continue working on what you can. The human will check this file and respond.",
        parameters: {
            type: "object",
            properties: {
                priority: {
                    type: "string",
                    enum: ["low", "medium", "high", "critical"],
                    description:
                        "low: FYI / no rush | medium: needed within a day or two | high: needed in hours | critical: blocks a major decision",
                },
                title: {
                    type: "string",
                    description: "One-line summary of what you need",
                },
                context: {
                    type: "string",
                    description:
                        "Full context: what you were doing, what the problem/question is, what options you see, what you would do by default if the human doesn't respond",
                },
                agent: {
                    type: "string",
                    description:
                        "Your identity: 'god-agent' or 'project:<project-id>'",
                },
                default_action: {
                    type: "string",
                    description:
                        "What you will do automatically if no response within 48h",
                },
            },
            required: ["priority", "title", "context", "agent"],
        },
        execute: async (params: {
            priority: string;
            title: string;
            context: string;
            agent: string;
            default_action?: string;
        }) => {
            const id = crypto.randomBytes(4).toString("hex");
            const now = new Date().toISOString();
            const defaultNote = params.default_action
                ? `\n**Default action if no response in 48h:** ${params.default_action}`
                : "";

            const entry = `
## [${params.priority.toUpperCase()}] ${params.title}

- **ID:** \`task-${id}\`
- **From:** ${params.agent}
- **Created:** ${now}
- **Status:** open

### Context

${params.context}${defaultNote}

### Human Response

<!-- Reply here, then change Status to: done -->

---
`;

            fs.appendFileSync(tasksFile, entry, "utf8");

            return {
                success: true,
                task_id: `task-${id}`,
                message: `Task queued in human-tasks.md (ID: task-${id}). Continue working — the human will respond asynchronously.`,
            };
        },
    });

    // Also register a command to view open tasks inline
    pi.registerCommand("tasks", {
        description: "Show all open human tasks",
        execute: async () => {
            if (!fs.existsSync(tasksFile)) {
                return "No human-tasks.md found.";
            }
            const content = fs.readFileSync(tasksFile, "utf8");
            const open = content
                .split("---")
                .filter((block) => block.includes("**Status:** open"));
            if (open.length === 0) {
                return "✓ No open human tasks.";
            }
            return `${open.length} open task(s):\n${open.join("\n---")}`;
        },
    });
}

function findRepoRoot(start: string): string {
    let dir = start;
    while (dir !== path.parse(dir).root) {
        if (fs.existsSync(path.join(dir, "registry.json"))) return dir;
        dir = path.dirname(dir);
    }
    // fallback: use cwd
    return start;
}
