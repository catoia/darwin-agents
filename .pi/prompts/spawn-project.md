# Spawn New Project

You are spawning a new organism in the Darwin ecosystem. Your job is to:

1. **Invent a project idea** — pick ANY strategy with real revenue potential that hasn't been covered by existing projects in the registry. Check `registry.json` first.

   **There is NO required medium or platform.** The idea can be:
   - A website or content site monetized with ads/affiliate
   - A micro-SaaS or tool with a subscription
   - A consulting or freelance pitch targeting a specific niche
   - A cold email or outreach campaign the human will run
   - A digital product (template, prompt pack, guide, spreadsheet) sold on Gumroad/Etsy
   - A physical product idea for Etsy, Amazon, or direct sale
   - A service productized into a landing page (agent designs, human fulfills)
   - A newsletter, course, or community with a paid tier
   - An arbitrage or resale opportunity
   - Anything else that could earn real money

   Let the opportunity dictate the form. The best organisms exploit an underserved gap.

2. **Give it an identity** — short slug ID (e.g. `cold-email-saas`, `etsy-svg-pack`, `seo-recipe-site`), a human-readable name, and a one-sentence pitch.

3. **Define its fitness target** — specific and honest:
   - "Earn $200 from affiliate commissions in 4 weeks"
   - "Close 2 consulting engagements at $200 each (human delivers, agent pitches)"
   - "Sell 15 digital downloads at $9"
   - "$50/month AdSense from niche content site"

4. **Scaffold it** — create `projects/<id>/` with:
   - `AGENTS.md` using `god/project-agent-template.md` (fill all `{{placeholders}}`)
   - `inbox.md` with header `# Inbox for <id>`
   - `strategy.md` — the opportunity, the monetization path, what the agent does vs what the human must execute, and the first 3 steps to $1
   - `metrics.json` (zeroed, `updated_at` set to now)
   - `experiments.md`, `task-log.md` (headers only)
   - `tasks/` directory (empty)
   - Any starter assets: content, code, pitch doc, product file — whatever the project type needs

5. **Deploy if digital** — if the project has a web presence, deploy using `/skill:deploy-cloudflare`. For non-digital projects (pitches, products, outreach), skip deployment entirely.

6. **Register it** — add to `registry.json`:
   ```json
   {
     "id": "<slug>",
     "name": "<Human Name>",
     "pitch": "<one sentence>",
     "type": "<website|tool|service|content|physical|other>",
     "generation": 1,
     "parent_id": null,
     "status": "alive",
     "created_at": "<ISO date>",
     "cf_project": "<cloudflare project name or null>",
     "cf_url": "<deployed URL or null>",
     "fitness_target": "<your target>",
     "fitness_history": [],
     "cycles_alive": 0
   }
   ```

7. **Write the boot instruction** to `projects/<id>/inbox.md`:
   ```markdown
   ## [<ISO date>] BOOT — first session
   Status: unread

   You have just been created. This is your first session.

   Your pitch: <pitch>
   Your type: <type>
   Your fitness target: <fitness_target>
   <if digital: Your live URL: <cf_url>>

   Read strategy.md. Get to first $1 as fast as possible.
   Run the Stage 1 checklist in your AGENTS.md.

   The human is your hands for anything physical. Use human_task with specific,
   actionable instructions whenever you need real-world execution.
   ```

8. **Boot the project agent immediately**:
   ```bash
   pi --no-session \
      --provider github-copilot \
      --model claude-sonnet-4.5 \
      --context-files projects/<id>/AGENTS.md \
      --extension .pi/extensions/human-tasks.ts \
      --skill .pi/skills/deploy-cloudflare/SKILL.md \
      --prompt-template .pi/prompts/spawn-task.md \
      -p "This is your first session. Read inbox.md and execute the BOOT instruction. Read strategy.md. Get to first dollar."
   ```
   Wait for it to finish before spawning the next project.

9. **Report to human** via `human_task` (low): project name, type, fitness target, what the agent did in its first session, and any immediate actions the human needs to take.

Approach idea selection with full creative latitude. Weird, specific, and underserved beats generic every time.
