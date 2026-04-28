# Mutate Project (Clone a Winner)

You are creating a genetic mutation of an existing successful project. This is how the ecosystem evolves.

**Parent project ID:** {{parent_id}}

## Steps

1. **Read the parent** — study `projects/{{parent_id}}/AGENTS.md`, its metrics in `registry.json`, and its deployed content. Understand *why* it won.

2. **Design the mutation** — pick ONE of these strategies (choose based on what the data suggests):
   - **Niche pivot**: same format, different target audience or keyword cluster
   - **Format upgrade**: same topic, different medium (e.g., text → interactive tool)
   - **Monetization upgrade**: same content, different revenue mechanism
   - **Audience expansion**: same core, broader or narrower audience
   - **Competitive differentiation**: same space, but address the gap the parent left

3. **Create the mutation** — new slug = `{{parent_id}}-m<N>` where N is the mutation number. Scaffold `projects/<new-id>/` with:
   - `AGENTS.md` referencing the parent, documenting the mutation strategy, filling all `{{placeholders}}`
   - `inbox.md` (header + boot instruction — see step 5)
   - Fresh content/code building on the parent's strengths
   - `metrics.json` (zeroed, `updated_at` set to now)
   - `experiments.md`, `task-log.md` (headers only)
   - `tasks/` directory

4. **Deploy** to Cloudflare Pages using `/skill:deploy-cloudflare`

5. **Write the boot instruction** to `projects/<new-id>/inbox.md`:
   ```markdown
   ## [<ISO date>] BOOT — first session (mutation of {{parent_id}})
   Status: unread
   
   You are a mutation of project {{parent_id}}. Your parent succeeded because: <why it won>.
   Your mutation strategy: <strategy chosen in step 2>.
   
   Your parent's live URL: <parent cf_url>
   Your live URL: <new cf_url>
   Your fitness target: <target>
   
   You are in Stage 1. Your job is not to copy your parent — it's to differentiate.
   Study your parent's content to understand what to build ON, not what to replicate.
   Run the Stage 1 checklist from your AGENTS.md before this session ends.
   ```

6. **Register** in `registry.json` with `"parent_id": "{{parent_id}}"` and `"generation": <parent_generation + 1>`

7. **Boot the project agent immediately**:
   ```bash
   pi --no-session \
      --provider github-copilot \
      --model claude-sonnet-4.5 \
      --context-files projects/<new-id>/AGENTS.md \
      --extension .pi/extensions/human-tasks.ts \
      --skill .pi/skills/deploy-cloudflare/SKILL.md \
      --prompt-template .pi/prompts/spawn-task.md \
      -p "This is your first session. You are a mutation. Read inbox.md and execute the BOOT instruction. Understand what made your parent succeed, then differentiate."
   ```

8. **Notify human** via `human_task` (low priority) — parent URL, mutation strategy, new URL, and one line on what the agent did in its first session.

The mutation should be meaningfully different from the parent, not just a copy. Evolution only works if mutations create real variation.
