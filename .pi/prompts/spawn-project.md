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

7. **Report to human** — call `human_task` with a `low` priority summary of what you created and the live URL.

Approach the idea selection creatively. The best organisms are ones that provide genuine value in an underserved niche.
