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
 *   npx tsx god/god-agent.ts poke          # Daily: stir all projects, check fleet health
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
import { execSync } from "child_process";

// ── Config ───────────────────────────────────────────────────────────────────
const GOD_MODEL = "claude-sonnet-4.5";

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

    const model = modelRegistry.find("github-copilot", GOD_MODEL);
    if (!model) {
        throw new Error(
            `Model not found: github-copilot/${GOD_MODEL}. ` +
            `Run 'pi --list-models' to see available models.`
        );
    }

    const { session } = await createAgentSession({
        // Auto-discovers AGENTS.md, .pi/extensions/, .pi/skills/, .pi/prompts/ from cwd
        cwd: REPO_ROOT,
        authStorage,
        modelRegistry,
        model,
        sessionManager: SessionManager.create(REPO_ROOT),
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
        `1. If registry shows cf_project is non-null, delete the Cloudflare Pages project named '${project.cf_project}' using wrangler\n` +
        `2. Set status to "killed" and killed_at to now in registry.json\n` +
        `3. git rm -r projects/${projectId}/\n` +
        `4. Commit and push\n` +
        `5. Call human_task (low) confirming the kill and noting its last fitness score.`
    );
}

async function cmdPoke() {
    const registry = loadRegistry();
    const projects = (registry.projects || []).filter((p: { status: string }) => p.status === "alive");
    const targetFleetSize: number = registry.target_fleet_size ?? 5;

    if (projects.length === 0) {
        console.log("[god] No alive projects to poke. Run: npm run seed");
        return;
    }

    console.log(`[god] Poking ${projects.length} alive projects...`);

    const session = await createGodSession("poke");
    await session.prompt(
        `Run your default cadence (from your AGENTS.md):
1. Check human-tasks.md for any human responses (Status: done with a Human response field) and act on them
2. Check registry.json fleet state — any pending-kill confirmations from human?
3. For each alive project, check if its inbox.md has been addressed recently and if metrics.json is fresh
4. Pick the lowest-performing project and write a specific challenge to its inbox.md
5. If fleet size is below target (${targetFleetSize} projects), spawn a new one
6. Write a brief summary of what you stirred up to human-tasks.md as a low-priority task

Current alive projects: ${projects.map((p: { id: string; cycles_alive?: number }) => `${p.id} (${p.cycles_alive ?? 0} cycles)`).join(", ")}`
    );

    // After god agent has written to inboxes, invoke each project agent directly
    // (mirrors what heartbeat.sh does in Step 2, so `npm run poke` also wakes projects)
    console.log(`[god] Invoking ${projects.length} project agents...`);
    for (const project of projects) {
        const projectDir = path.join(REPO_ROOT, "projects", project.id);
        if (!fs.existsSync(projectDir)) {
            console.warn(`[god] WARNING: missing dir for ${project.id}, skipping`);
            continue;
        }

        // fetch-metrics first so the agent has fresh numbers
        try {
            execSync(`bash "${path.join(REPO_ROOT, "scripts", "fetch-metrics.sh")}" "${project.id}"`, { stdio: "inherit" });
        } catch {
            console.warn(`[god] metrics fetch failed for ${project.id} (continuing)`);
        }

        const agentsFile = path.join(projectDir, "AGENTS.md");
        const extensionFile = path.join(REPO_ROOT, ".pi", "extensions", "human-tasks.ts");
        const skillFile = path.join(REPO_ROOT, ".pi", "skills", "deploy-cloudflare", "SKILL.md");
        const promptTemplate = path.join(REPO_ROOT, ".pi", "prompts", "spawn-task.md");

        try {
            execSync(
                `pi --no-session \
  --provider github-copilot \
  --model ${GOD_MODEL} \
  --context-files "${agentsFile}" \
  --extension "${extensionFile}" \
  --skill "${skillFile}" \
  --prompt-template "${promptTemplate}" \
  -p "Daily work session. Check inbox.md first, then run your default work loop. Be decisive and commit before exiting."`,
                { stdio: "inherit", cwd: REPO_ROOT }
            );
        } catch {
            console.warn(`[god] Project agent ${project.id} exited with error (continuing)`);
        }
    }
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
        case "poke":
            await cmdPoke();
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
  npx tsx god/god-agent.ts poke          # Daily: stir projects, check fleet health
  npx tsx god/god-agent.ts status        # Show fleet status table
  npx tsx god/god-agent.ts kill <id>     # Kill a specific project
`);
    }
})();
