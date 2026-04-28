# darwin-agents

Darwinian self-evolving project ecosystem powered by [pi](https://github.com/mariozechner/pi-coding-agent) coding agents. Projects compete for fitness (revenue, traffic, engagement), are evaluated weekly, and the weakest are killed while the strongest are mutated and cloned.

## Prerequisites

- Node.js 18+
- [pi](https://github.com/mariozechner/pi-coding-agent) installed globally (`npm install -g @mariozechner/pi-coding-agent`)
- `pi /login` completed with GitHub Copilot (or another provider)
- [wrangler](https://developers.cloudflare.com/workers/wrangler/install-and-update/) installed for Cloudflare Pages deploys
- A Cloudflare account with Pages enabled

## Setup

```bash
# 1. Install dependencies
npm install

# 2. Copy env template and fill in your credentials
cp .env.example .env
# edit .env with your CF token, account ID, etc.

# 3. Install the daily cron (macOS/Linux)
bash scripts/setup-cron.sh

# 4. Spawn the first wave of projects
npm run seed
```

## Daily commands

```bash
npm run seed        # Spawn initial 5 projects (run once)
npm run status      # Print fleet fitness table
npm run poke        # God agent daily cycle: stir all projects
npm run evaluate    # Force a full weekly evaluation cycle
npm run heartbeat   # Full heartbeat: poke + invoke all project agents
FORCE_EVAL=1 npm run heartbeat  # Heartbeat with forced evaluation
```

## How it works

```
Heartbeat (cron, daily)
  └──▶ god-agent: check humans tasks, stir projects, write inbox.md instructions
  └──▶ for each alive project: fetch metrics → invoke project agent
          └──▶ project agent: reads inbox, picks highest-impact action, may spawn task agents
                └──▶ task agent: bounded work, reports to task-log.md, exits
```

Fitness formula: `(revenue × 0.6) + (traffic_score × 0.25) + (engagement_score × 0.15)`

Weekly selection: bottom 25% killed, top 25% mutated/cloned, fleet refilled to `target_fleet_size`.

## Required credentials (`.env`)

| Variable | Purpose |
|---|---|
| `CLOUDFLARE_API_TOKEN` | CF Analytics read + Pages deploy |
| `CLOUDFLARE_ACCOUNT_ID` | Your CF account ID |
| `STRIPE_API_KEY` | Revenue from Stripe (optional) |
| `ADSENSE_ACCESS_TOKEN` | Revenue from AdSense (optional) |
| `ADSENSE_ACCOUNT_ID` | AdSense account ID (optional) |

## Human tasks

Agents queue decisions in `human-tasks.md`. Check it daily. Reply inline using the format:
```
**Human response:** your answer here
**Status:** done
```
