# Mutate Project (Clone a Winner)

You are creating a genetic mutation of an existing successful project. This is how the ecosystem evolves.

**Parent project ID:** {{parent_id}}

## Steps

1. **Read the parent** — study `projects/{{parent_id}}/AGENTS.md`, `strategy.md`, its metrics in `registry.json`, and any assets. Understand *why* it won: what problem it solved, what medium it used, how money flowed in.

2. **Design the mutation** — pick ONE of these strategies (let the data guide you):
   - **Niche pivot**: same approach, different audience or vertical
   - **Medium upgrade**: same topic, different form (website → tool, pitch → course, etc.)
   - **Monetization upgrade**: same content/offer, different revenue mechanism
   - **Distribution shift**: same offer, different acquisition channel (SEO → cold email, etc.)
   - **Scale play**: same approach, 10x bigger scope
   - **Cross-domain leap**: apply the winning insight to a completely different market

   **The mutation can change the project type entirely.** If the parent was a website and
   the data suggests a service would compound faster, make it a service. Evolution has
   no loyalty to the parent's medium.

3. **Create the mutation** — new slug = `{{parent_id}}-m<N>`. Scaffold `projects/<new-id>/` with:
   - `AGENTS.md` (fill all `{{placeholders}}`, document parent and mutation strategy)
   - `inbox.md` (header + boot instruction)
   - `strategy.md` — why this mutation, what's different, first 3 steps to $1
   - Fresh assets building on parent's strengths but meaningfully differentiated
   - `metrics.json`, `experiments.md`, `task-log.md` (zeroed/headers)
   - `tasks/` directory

4. **Deploy if digital** — use `/skill:deploy-cloudflare` only if the mutation has a web presence. Otherwise skip.

5. **Write the boot instruction** to `projects/<new-id>/inbox.md`:
   ```markdown
   ## [<ISO date>] BOOT — first session (mutation of {{parent_id}})
   Status: unread

   You are a mutation of project {{parent_id}}. Your parent succeeded because: <why it won>.
   Your mutation strategy: <strategy>.
   Your type: <type>
   Your fitness target: <target>
   <if digital: Your live URL: <new cf_url>>

   Read strategy.md. Your job is not to copy your parent — it's to differentiate and improve.
   Get to first $1 faster than your parent did. Use human_task for any real-world execution.
   Run the Stage 1 checklist from your AGENTS.md.
   ```

6. **Register** in `registry.json` with `"parent_id": "{{parent_id}}"`, `"generation": <parent_generation + 1>`, and the `"type"` field.

7. **Boot the project agent immediately**:
   ```bash
   pi --no-session \
      --provider github-copilot \
      --model claude-sonnet-4.6 \
      --context-files projects/<new-id>/AGENTS.md \
      --extension .pi/extensions/human-tasks.ts \
      --skill .pi/skills/deploy-cloudflare/SKILL.md \
      --prompt-template .pi/prompts/spawn-task.md \
      -p "This is your first session. You are a mutation. Read inbox.md and execute the BOOT instruction. Read strategy.md. Differentiate and get to first dollar."
   ```

8. **Notify human** via `human_task` (low): parent ID, mutation strategy, new type, and any immediate actions the human needs to take.

Evolution only works if mutations create real variation. A clone that does the same thing is not a mutation — it's a copy. Surprise the ecosystem.
