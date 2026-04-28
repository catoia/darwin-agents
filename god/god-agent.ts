#!/usr/bin/env node
/**
 * god-agent.ts
 *
 * The orchestration script for the Darwin ecosystem.
 * Runs as the "God Agent" — manages the fleet via the pi SDK.
 *
 * Usage:
 *   npx tsx god/god-agent.ts seed          # Spawn first wave of projects
 *   npx tsx god/god-agent.ts evaluate      # Run weekly selection cycle
 *   npx tsx god/god-agent.ts status        # Print fleet status table
 *   npx tsx god/god-agent.ts kill <id>     # Manually kill a project (after human confirmed)
 */

import {
    AuthStorage,
    createAgentSession,
    ModelRegistry,
    SessionManager,
} from "@mariozechner/pi-coding-agent";
import * as fs from "fs";
import * as path from "path";

const REPO_ROOT = path.resolve(__dirname, "..");
const REGISTRY_FILE = path.join(REPO_ROOT, "registry.json");

// ── Registry helpers ────────────────────────────────────────────────────────

function loadRegistry() {
    return JSON.parse(fs.readFileSync(REGISTRY_FILE, "utf8"));
}

function saveRegistry(data: unknown) {
    fs.writeFileSync(REGISTRY_FILE, JSON.stringify(data, null, 2), "utf8");
}

// ── Agent factory ────────────────────────────────────────────────────────────

async function createGodSession(sessionLabel: string) {
    const authStorage = AuthStorage.create();
    const modelRegistry = ModelRegistry.create(authStorage);

    const { session } = await createAgentSession({
        // Sessions saved to ~/.pi/agent/sessions/ organized by project
        sessionManager: SessionManager.create(),
        authStorage,
        modelRegistry,
        // GitHub Copilot — authenticated via `pi /login` → GitHub Copilot
        provider: "github-copilot",
        workingDir: REPO_ROOT,
        contextFiles: [path.join(REPO_ROOT, "AGENTS.md")],
        extensionPaths: [path.join(REPO_ROOT, ".pi/extensions/human-tasks.ts")],
        promptTemplatePaths: [
            path.join(REPO_ROOT, ".pi/prompts/spawn-project.md"),
            path.join(REPO_ROOT, ".pi/prompts/mutate-project.md"),
            path.join(REPO_ROOT, ".pi/prompts/evaluate.md"),
        ],
        skillPaths: [
            path.join(REPO_ROOT, ".pi/skills/deploy-cloudflare/SKILL.md"),
        ],
    });

    console.log(`[god] Session started: ${sessionLabel}`);
    return session;
}

// ── Commands ─────────────────────────────────────────────────────────────────

async function cmdSeed() {
    console.log("[god] Seeding initial project fleet...");
    const session = await createGodSession("seed");
    await session.prompt(
        "Use the /spawn-project template to create 3 diverse initial projects. " +
        "Pick niches with real revenue potential that don't overlap. " +
        "After each spawn, update registry.json and commit. " +
        "When done, call human_task (low) with a summary of what you launched."
    );
    console.log("[god] Seed complete.");
}

async function cmdEvaluate() {
    const registry = loadRegistry();
    const cycle = registry.cycle + 1;
    console.log(`[god] Starting evaluation cycle ${cycle}...`);

    const session = await createGodSession(`evaluate-cycle-${cycle}`);
    await session.prompt(
        `Run the /evaluate prompt for cycle ${cycle}. ` +
        `Current cycle count in registry is ${registry.cycle}. Update it to ${cycle} when done.`
    );

    console.log(`[god] Cycle ${cycle} evaluation complete.`);
}

async function cmdStatus() {
    const registry = loadRegistry();
    const projects = registry.projects || [];

    if (projects.length === 0) {
        console.log("Fleet is empty. Run: npx tsx god/god-agent.ts seed");
        return;
    }

    console.log(`\n=== Darwin Fleet — Cycle ${registry.cycle} ===\n`);
    console.log(
        "ID".padEnd(30) +
        "Status".padEnd(12) +
        "Gen".padEnd(6) +
        "Cycles".padEnd(8) +
        "Last Fitness"
    );
    console.log("─".repeat(70));

    for (const p of projects) {
        const lastFitness =
            p.fitness_history?.length > 0
                ? p.fitness_history[p.fitness_history.length - 1].score.toFixed(1)
                : "—";
        console.log(
            p.id.padEnd(30) +
            p.status.padEnd(12) +
            String(p.generation).padEnd(6) +
            String(p.cycles_alive || 0).padEnd(8) +
            lastFitness
        );
    }
    console.log();
}

async function cmdKill(projectId: string) {
    const registry = loadRegistry();
    const project = registry.projects.find((p: { id: string }) => p.id === projectId);
    if (!project) {
        console.error(`Project '${projectId}' not found in registry.`);
        process.exit(1);
    }

    const session = await createGodSession(`kill-${projectId}`);
    await session.prompt(
        `Kill project '${projectId}'. Steps:\n` +
        `1. Delete the Cloudflare Pages project named '${project.cf_project}' using wrangler\n` +
        `2. Set status to "killed" and killed_at to now in registry.json\n` +
        `3. git rm -r projects/${projectId}/\n` +
        `4. Commit and push\n` +
        `5. Call human_task (low) confirming the kill and noting its last fitness score.`
    );
}

// ── Entry point ───────────────────────────────────────────────────────────────

const command = process.argv[2];

(async () => {
    switch (command) {
        case "seed":
            await cmdSeed();
            break;
        case "evaluate":
            await cmdEvaluate();
            break;
        case "status":
            await cmdStatus();
            break;
        case "kill":
            await cmdKill(process.argv[3]);
            break;
        default:
            console.log(`Usage:
  npx tsx god/god-agent.ts seed          # Spawn initial project fleet
  npx tsx god/god-agent.ts evaluate      # Run weekly selection cycle  
  npx tsx god/god-agent.ts status        # Show fleet status table
  npx tsx god/god-agent.ts kill <id>     # Kill a specific project
`);
    }
})();
