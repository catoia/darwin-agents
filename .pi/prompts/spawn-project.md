# Spawn New Project

You are spawning a new organism in the Darwin ecosystem. Your job is to:

1. **Invent a project idea** — pick a niche/medium that has real revenue potential and hasn't been covered by existing projects in the registry. Check `registry.json` first. The project can be anything: a content site, a micro-tool, a niche blog, a single-page app, a resource directory. Let the opportunity guide the form, not the other way around.

2. **Give it an identity** — create a short slug ID (e.g. `seo-recipes-2025`), a human-readable name, and a one-sentence pitch.

3. **Define its fitness target** — what does success look like in 4 weeks? Be specific: "500 unique visitors/week from organic search" or "$20/month from affiliate links".

4. **Scaffold it** — create `projects/<id>/` with:
   - `AGENTS.md` using the template at `god/project-agent-template.md` (fill all `{{placeholders}}`)
   - `inbox.md` with header `# Inbox for <id>\n\n<!-- God Agent writes instructions here -->`
   - `metrics.json` (zeroed out, with `updated_at` set to now)
   - `experiments.md` (header only)
   - `task-log.md` (header only)
   - `index.html` or whatever the project entry point is
   - `tasks/` directory (empty, for task briefs)

5. **Deploy it** to Cloudflare Pages using `/skill:deploy-cloudflare`

6. **Register it** — add an entry to `registry.json`:
   ```json
   {
     "id": "<slug>",
     "name": "<Human Name>",
     "pitch": "<one sentence>",
     "generation": 1,
     "parent_id": null,
     "status": "alive",
     "created_at": "<ISO date>",
     "cf_project": "<cloudflare project name>",
     "cf_url": "<deployed URL>",
     "fitness_target": "<your target>",
     "fitness_history": [],
     "cycles_alive": 0
   }
   ```

7. **Write the boot instruction** — append this to `projects/<id>/inbox.md` immediately after creation:
   ```markdown
   ## [<ISO date>] BOOT — first session
   Status: unread
   
   You have just been created. This is your first session.
   
   Your project is live at: <cf_url>
   Your fitness target: <fitness_target>
   
   You are in Stage 1 (zero metrics). Your entire job right now is to verify the
   foundation and get to something that could theoretically earn. Run through the
   Stage 1 checklist in your AGENTS.md before this session ends.
   
   Do not optimize. Do not redesign. Get the basics live and working first.
   ```

8. **Boot the project agent immediately** — do not wait for the next heartbeat. Invoke it now:
   ```bash
   pi --no-session \
      --provider github-copilot \
      --model claude-sonnet-4.5 \
      --context-files projects/<id>/AGENTS.md \
      --extension .pi/extensions/human-tasks.ts \
      --skill .pi/skills/deploy-cloudflare/SKILL.md \
      --prompt-template .pi/prompts/spawn-task.md \
      -p "This is your first session. Read inbox.md and complete the BOOT instruction. You are in Stage 1. Run the checklist now."
   ```
   Wait for it to finish before moving on to the next project spawn.

9. **Report to human** — call `human_task` with `low` priority: project name, live URL, fitness target, and one line on what the project agent did in its first session.

Approach the idea selection creatively. The best organisms are ones that provide genuine value in an underserved niche.
